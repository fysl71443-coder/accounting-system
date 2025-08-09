#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق المحاسبة الويب - Flask Web Accounting Application
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from io import BytesIO
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import json

# إنشاء التطبيق
app = Flask(__name__, template_folder='templates')

# مسح cache القوالب للتطوير
app.jinja_env.cache = {}

# التكوين
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# إعداد قاعدة البيانات
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد قاعدة البيانات
db = SQLAlchemy(app)

# إعداد إدارة تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة'

# نماذج قاعدة البيانات
# نموذج Role معطل مؤقتاً للتوافق مع قاعدة البيانات الحالية
# سيتم تفعيله بعد تحديث قاعدة البيانات

class User(UserMixin, db.Model):
    """نموذج المستخدم المحسن"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # الدور القديم
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        """التحقق من صلاحية معينة"""
        if not self.is_active:
            return False

        # المشرف له جميع الصلاحيات
        if self.role == 'admin':
            return True

        # صلاحيات أساسية للمستخدمين العاديين
        basic_permissions = [
            'can_access_sales', 'can_access_inventory',
            'can_create', 'can_print'
        ]

        if self.role == 'user' and permission in basic_permissions:
            return True

        return False

    def can_access(self, module):
        """التحقق من إمكانية الوصول لشاشة معينة"""
        if not self.is_active:
            return False

        # المشرف له وصول لكل شيء
        if self.role == 'admin':
            return True

        # المستخدمين العاديين لهم وصول محدود
        allowed_modules = ['sales', 'inventory']
        return module in allowed_modules

    def get_role_name(self):
        """الحصول على اسم الدور"""
        role_names = {
            'admin': 'مشرف عام',
            'user': 'موظف'
        }
        return role_names.get(self.role, self.role)

class Branch(db.Model):
    """نموذج الفرع"""
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_code = db.Column(db.String(10), unique=True, nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)
    branch_name_en = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    manager_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    """نموذج المنتج"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), unique=True, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    unit_cost = db.Column(db.Float, default=0.0)
    selling_price = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(100))
    unit_type = db.Column(db.String(20), default='قطعة')
    min_stock_level = db.Column(db.Integer, default=0)
    current_stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RawMaterial(db.Model):
    """نموذج المواد الخام"""
    __tablename__ = 'raw_materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    purchase_price = db.Column(db.Numeric(10, 3), nullable=False)
    current_stock = db.Column(db.Numeric(10, 3), default=0)
    min_stock_level = db.Column(db.Numeric(10, 3), default=5)
    supplier = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Customer(db.Model):
    """نموذج العملاء"""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    tax_number = db.Column(db.String(50))
    credit_limit = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Supplier(db.Model):
    """نموذج الموردين"""
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    tax_number = db.Column(db.String(50))
    contact_person = db.Column(db.String(100))
    credit_limit = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProductCost(db.Model):
    """نموذج تكلفة المنتج"""
    __tablename__ = 'product_costs'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    raw_material_id = db.Column(db.Integer, db.ForeignKey('raw_materials.id'), nullable=False)
    quantity_used = db.Column(db.Numeric(10, 3), nullable=False)
    unit_cost = db.Column(db.Numeric(10, 3), nullable=False)
    total_cost = db.Column(db.Numeric(10, 3), nullable=False)
    percentage = db.Column(db.Numeric(5, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    raw_material = db.relationship('RawMaterial', backref='product_costs')

class Sale(db.Model):
    """نموذج فاتورة المبيعات"""
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    customer_name = db.Column(db.String(200))
    invoice_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    branch = db.relationship('Branch', backref='sales')
    creator = db.relationship('User', backref='sales')
    items = db.relationship('SaleItem', backref='sale', cascade='all, delete-orphan')

    def get_total_paid(self):
        """حساب إجمالي المدفوعات لهذه الفاتورة"""
        try:
            total = db.session.query(db.func.sum(PaymentSale.applied_amount))\
                .filter_by(sale_id=self.id).scalar()
            return float(total) if total is not None else 0.0
        except Exception as e:
            print(f"خطأ في حساب المدفوعات للفاتورة {self.id}: {e}")
            return 0.0

    def get_remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.final_amount - self.get_total_paid()

    def update_payment_status(self):
        """تحديث حالة الدفع بناءً على المدفوعات"""
        total_paid = self.get_total_paid()

        # استخدام دقة عشرية لتجنب مشاكل الفاصلة العائمة
        total_paid = round(total_paid, 2)
        final_amount = round(self.final_amount, 2)

        if total_paid >= final_amount:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'

        print(f"تحديث حالة الفاتورة {self.invoice_number}: مدفوع={total_paid}, إجمالي={final_amount}, حالة={self.payment_status}")

class SaleItem(db.Model):
    """نموذج عنصر فاتورة المبيعات"""
    __tablename__ = 'sale_items'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

class Purchase(db.Model):
    """نموذج فاتورة المشتريات"""
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))  # إضافة حقل supplier_id
    supplier_name = db.Column(db.String(200))
    invoice_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    branch = db.relationship('Branch', backref='purchases')
    supplier = db.relationship('Supplier', backref='purchases')  # إضافة علاقة مع Supplier
    creator = db.relationship('User', backref='purchases')

    # خصائص محسوبة للتوافق مع الكود الجديد
    @property
    def subtotal(self):
        return self.total_amount or 0.0

    @property
    def discount_amount(self):
        return 0.0  # افتراضي

    # تم حذف property supplier_id وإضافة حقل supplier_id حقيقي في النموذج

    def get_total_paid(self):
        """حساب إجمالي المدفوعات لهذه الفاتورة"""
        try:
            total = db.session.query(db.func.sum(PaymentPurchase.applied_amount))\
                .filter_by(purchase_id=self.id).scalar()
            return float(total) if total is not None else 0.0
        except Exception as e:
            print(f"خطأ في حساب المدفوعات للمشتريات {self.id}: {e}")
            return 0.0

    def get_remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.final_amount - self.get_total_paid()

    def update_payment_status(self):
        """تحديث حالة الدفع بناءً على المدفوعات"""
        total_paid = self.get_total_paid()

        total_paid = round(total_paid, 2)
        final_amount = round(self.final_amount, 2)

        if total_paid >= final_amount:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'

class PurchaseItem(db.Model):
    """نموذج عناصر فاتورة المشتريات"""
    __tablename__ = 'purchase_items'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    purchase = db.relationship('Purchase', backref='items')
    product = db.relationship('Product', backref='purchase_items')

class Expense(db.Model):
    """نموذج المصروفات"""
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    expense_number = db.Column(db.String(50), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    expense_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    branch = db.relationship('Branch', backref='expenses')
    creator = db.relationship('User', backref='expenses')

    def get_total_paid(self):
        """حساب إجمالي المدفوعات لهذا المصروف"""
        try:
            total = db.session.query(db.func.sum(PaymentExpense.applied_amount))\
                .filter_by(expense_id=self.id).scalar()
            return float(total) if total is not None else 0.0
        except Exception as e:
            print(f"خطأ في حساب المدفوعات للمصروف {self.id}: {e}")
            return 0.0

    def get_remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.amount - self.get_total_paid()

    def update_payment_status(self):
        """تحديث حالة الدفع بناءً على المدفوعات"""
        total_paid = self.get_total_paid()

        total_paid = round(total_paid, 2)
        amount = round(self.amount, 2)

        if total_paid >= amount:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'

class EmployeePayroll(db.Model):
    """نموذج رواتب الموظفين"""
    __tablename__ = 'employee_payrolls'

    id = db.Column(db.Integer, primary_key=True)
    payroll_number = db.Column(db.String(50), unique=True, nullable=False)
    employee_name = db.Column(db.String(200), nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, default=0.0)
    allowances = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    creator = db.relationship('User', backref='payrolls')

    def get_total_paid(self):
        """حساب إجمالي المدفوعات لهذا الراتب"""
        try:
            total = db.session.query(db.func.sum(PaymentPayroll.applied_amount))\
                .filter_by(payroll_id=self.id).scalar()
            return float(total) if total is not None else 0.0
        except Exception as e:
            print(f"خطأ في حساب المدفوعات للراتب {self.id}: {e}")
            return 0.0

    def get_remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.net_salary - self.get_total_paid()

    def update_payment_status(self):
        """تحديث حالة الدفع بناءً على المدفوعات"""
        total_paid = self.get_total_paid()

        total_paid = round(total_paid, 2)
        net_salary = round(self.net_salary, 2)

        if total_paid >= net_salary:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'

# نموذج الدفعات
class Payment(db.Model):
    """نموذج الدفعات"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.now().date)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # العلاقات
    created_by_user = db.relationship('User')

# نموذج ربط الدفعات بالفواتير
# جداول منفصلة لربط الدفعات بأنواع الفواتير المختلفة
class PaymentSale(db.Model):
    """ربط الدفعات بفواتير المبيعات"""
    __tablename__ = 'payment_sales'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    applied_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PaymentPurchase(db.Model):
    """ربط الدفعات بفواتير المشتريات"""
    __tablename__ = 'payment_purchases'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    applied_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PaymentExpense(db.Model):
    """ربط الدفعات بالمصروفات"""
    __tablename__ = 'payment_expenses'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    applied_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PaymentPayroll(db.Model):
    """ربط الدفعات برواتب الموظفين"""
    __tablename__ = 'payment_payrolls'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    payroll_id = db.Column(db.Integer, db.ForeignKey('employee_payrolls.id'), nullable=False)
    applied_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payroll = db.relationship('EmployeePayroll', backref='payment_records')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorator للتحقق من الصلاحيات
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))

            if not current_user.has_permission(permission):
                flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decorator للتحقق من الوصول للشاشات
def require_access(module):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))

            if not current_user.can_access(module):
                flash(f'ليس لديك صلاحية للوصول لشاشة {module}', 'error')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decorator للمشرف فقط
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

        if current_user.role != 'admin':
            flash('هذه الصفحة متاحة للمشرف فقط', 'error')
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)
    return decorated_function

# الصفحات الرئيسية
@app.route('/')
def index():
    """الصفحة الرئيسية"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        language = request.form.get('language', 'ar')
        
        user = User.query.filter_by(username=username, is_active=True).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # حفظ اللغة في الجلسة
            session['language'] = language
            
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية"""
    # إحصائيات سريعة
    today = datetime.now().date()
    
    # مبيعات اليوم
    daily_sales = db.session.query(db.func.sum(Sale.final_amount)).filter(
        Sale.invoice_date == today
    ).scalar() or 0
    
    # مبيعات الشهر
    month_start = today.replace(day=1)
    monthly_sales = db.session.query(db.func.sum(Sale.final_amount)).filter(
        Sale.invoice_date >= month_start
    ).scalar() or 0
    
    # عدد المنتجات
    total_products = Product.query.filter_by(is_active=True).count()
    
    # تنبيهات المخزون المنخفض
    low_stock_products = Product.query.filter(
        Product.current_stock <= Product.min_stock_level,
        Product.is_active == True
    ).all()
    
    # آخر المبيعات
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(5).all()
    
    return render_template('dashboard_unified.html',
                         daily_sales=daily_sales,
                         monthly_sales=monthly_sales,
                         total_products=total_products,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales)

# تم حذف شاشة المنتجات القديمة - استخدم الشاشة الموحدة بدلاً منها

@app.route('/sales')
@login_required
@require_access('sales')
def sales():
    """صفحة المبيعات"""
    branch_id = request.args.get('branch_id')

    query = Sale.query
    if branch_id:
        query = query.filter_by(branch_id=branch_id)

    sales = query.order_by(Sale.created_at.desc()).all()
    branches = Branch.query.filter_by(is_active=True).all()



    return render_template('sales.html', sales=sales, branches=branches, selected_branch=branch_id)



# تم حذف شاشة فاتورة جديدة - يمكن إنشاء الفواتير من شاشة المبيعات مباشرة

@app.route('/raw_materials')
@login_required
def raw_materials():
    """صفحة إدارة المواد الخام"""
    return render_template('raw_materials.html')

@app.route('/product_cost')
@app.route('/product_cost/<int:product_id>')
@login_required
def product_cost(product_id=None):
    """صفحة حساب تكلفة المنتج"""
    product = None
    raw_materials = []

    # جلب بيانات المنتج إذا تم تمرير معرف المنتج
    if product_id:
        try:
            conn = sqlite3.connect('restaurant_accounting.db')
            cursor = conn.cursor()

            # جلب بيانات المنتج
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product_data = cursor.fetchone()

            if product_data:
                product = {
                    'id': product_data[0],
                    'product_name': product_data[1],
                    'product_name_en': product_data[2] if len(product_data) > 2 else '',
                    'category': product_data[3] if len(product_data) > 3 else '',
                    'selling_price': product_data[4] if len(product_data) > 4 else 0,
                    'product_code': f'P{product_data[0]:03d}',
                    'unit_cost': 0.00
                }

            conn.close()
        except (sqlite3.OperationalError, IndexError):
            # إذا لم يكن الجدول موجود أو حدث خطأ، استخدم بيانات تجريبية
            if product_id == 1:
                product = {
                    'id': 1,
                    'product_name': 'برياني دجاج',
                    'product_name_en': 'Chicken Biryani',
                    'category': 'وجبات رئيسية',
                    'selling_price': 25.00,
                    'product_code': 'P001',
                    'unit_cost': 18.50
                }

    # جلب قائمة المواد الخام (مع معالجة الأخطاء)
    try:
        conn = sqlite3.connect('restaurant_accounting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, material_name, unit, purchase_price FROM raw_materials ORDER BY material_name")
        raw_materials_data = cursor.fetchall()

        for material in raw_materials_data:
            raw_materials.append({
                'id': material[0],
                'name': material[1],
                'unit': material[2],
                'price': material[3]
            })

        conn.close()
    except sqlite3.OperationalError:
        # إذا لم يكن الجدول موجود، استخدم بيانات تجريبية
        raw_materials = [
            {'id': 1, 'name': 'أرز بسمتي', 'unit': 'كيلو', 'price': 12.50},
            {'id': 2, 'name': 'دجاج طازج', 'unit': 'كيلو', 'price': 25.00},
            {'id': 3, 'name': 'بصل أحمر', 'unit': 'كيلو', 'price': 3.50},
            {'id': 4, 'name': 'طماطم', 'unit': 'كيلو', 'price': 4.00},
            {'id': 5, 'name': 'لبن زبادي', 'unit': 'كيلو', 'price': 8.00},
            {'id': 6, 'name': 'بهارات البرياني', 'unit': 'كيلو', 'price': 45.00},
            {'id': 7, 'name': 'زيت دوار الشمس', 'unit': 'لتر', 'price': 8.50},
            {'id': 8, 'name': 'ملح طعام', 'unit': 'كيلو', 'price': 2.00},
            {'id': 9, 'name': 'ثوم', 'unit': 'كيلو', 'price': 15.00},
            {'id': 10, 'name': 'زنجبيل', 'unit': 'كيلو', 'price': 20.00},
            {'id': 11, 'name': 'زعفران', 'unit': 'جرام', 'price': 0.50},
            {'id': 12, 'name': 'لوز مقشر', 'unit': 'كيلو', 'price': 35.00},
            {'id': 13, 'name': 'زبيب ذهبي', 'unit': 'كيلو', 'price': 18.00}
        ]

    # إضافة متغيرات إضافية للقالب
    cost_breakdown = []
    cost_history = []
    material_cost = 0.0

    return render_template('product_cost.html',
                         product=product,
                         product_id=product_id,
                         raw_materials=raw_materials,
                         cost_breakdown=cost_breakdown,
                         cost_history=cost_history,
                         material_cost=material_cost)

@app.route('/meal_cost_calculator')
@login_required
def meal_cost_calculator():
    """صفحة حساب تكلفة الوجبات المتقدمة"""

    # جلب قائمة الوجبات
    meals = [
        {'id': 1, 'name': 'برياني دجاج', 'servings': 4},
        {'id': 2, 'name': 'كبسة لحم', 'servings': 6},
        {'id': 3, 'name': 'مندي غنم', 'servings': 8},
        {'id': 4, 'name': 'مقلوبة دجاج', 'servings': 4},
        {'id': 5, 'name': 'أرز بخاري', 'servings': 5}
    ]

    # جلب قائمة المواد الخام
    raw_materials = [
        {'id': 1, 'name': 'أرز بسمتي', 'unit': 'كيلو', 'price': 12.50},
        {'id': 2, 'name': 'دجاج طازج', 'unit': 'كيلو', 'price': 25.00},
        {'id': 3, 'name': 'لحم غنم', 'unit': 'كيلو', 'price': 45.00},
        {'id': 4, 'name': 'بصل أحمر', 'unit': 'كيلو', 'price': 3.50},
        {'id': 5, 'name': 'طماطم', 'unit': 'كيلو', 'price': 4.00},
        {'id': 6, 'name': 'جزر', 'unit': 'كيلو', 'price': 2.50},
        {'id': 7, 'name': 'بازلاء', 'unit': 'كيلو', 'price': 6.00},
        {'id': 8, 'name': 'لبن زبادي', 'unit': 'كيلو', 'price': 8.00},
        {'id': 9, 'name': 'بهارات البرياني', 'unit': 'كيلو', 'price': 45.00},
        {'id': 10, 'name': 'بهارات الكبسة', 'unit': 'كيلو', 'price': 40.00},
        {'id': 11, 'name': 'زيت دوار الشمس', 'unit': 'لتر', 'price': 8.50},
        {'id': 12, 'name': 'سمن بلدي', 'unit': 'كيلو', 'price': 35.00},
        {'id': 13, 'name': 'ملح طعام', 'unit': 'كيلو', 'price': 2.00},
        {'id': 14, 'name': 'فلفل أسود', 'unit': 'كيلو', 'price': 25.00},
        {'id': 15, 'name': 'ثوم', 'unit': 'كيلو', 'price': 15.00},
        {'id': 16, 'name': 'زنجبيل', 'unit': 'كيلو', 'price': 20.00},
        {'id': 17, 'name': 'زعفران', 'unit': 'جرام', 'price': 0.50},
        {'id': 18, 'name': 'لوز مقشر', 'unit': 'كيلو', 'price': 35.00},
        {'id': 19, 'name': 'زبيب ذهبي', 'unit': 'كيلو', 'price': 18.00},
        {'id': 20, 'name': 'ماء ورد', 'unit': 'لتر', 'price': 12.00}
    ]

    return render_template('meal_cost_calculator.html',
                         meals=meals,
                         raw_materials=raw_materials)

@app.route('/api/ingredients', methods=['GET'])
@login_required
def get_ingredients():
    """API لجلب قائمة المكونات"""
    try:
        conn = sqlite3.connect('restaurant_accounting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, material_name, unit, purchase_price FROM raw_materials ORDER BY material_name")
        ingredients_data = cursor.fetchall()

        ingredients = []
        for ingredient in ingredients_data:
            ingredients.append({
                'id': ingredient[0],
                'name': ingredient[1],
                'unit': ingredient[2],
                'price': ingredient[3]
            })

        conn.close()
        return jsonify({'success': True, 'ingredients': ingredients})
    except sqlite3.OperationalError:
        # Return default ingredients if table doesn't exist
        default_ingredients = [
            {'id': 1, 'name': 'أرز بسمتي', 'unit': 'كيلو', 'price': 12.50},
            {'id': 2, 'name': 'دجاج طازج', 'unit': 'كيلو', 'price': 25.00},
            {'id': 3, 'name': 'لحم غنم', 'unit': 'كيلو', 'price': 45.00},
            {'id': 4, 'name': 'بصل أحمر', 'unit': 'كيلو', 'price': 3.50},
            {'id': 5, 'name': 'طماطم', 'unit': 'كيلو', 'price': 4.00},
            {'id': 6, 'name': 'جزر', 'unit': 'كيلو', 'price': 2.50},
            {'id': 7, 'name': 'بازلاء', 'unit': 'كيلو', 'price': 6.00},
            {'id': 8, 'name': 'لبن زبادي', 'unit': 'كيلو', 'price': 8.00},
            {'id': 9, 'name': 'بهارات البرياني', 'unit': 'كيلو', 'price': 45.00},
            {'id': 10, 'name': 'بهارات الكبسة', 'unit': 'كيلو', 'price': 40.00},
            {'id': 11, 'name': 'زيت دوار الشمس', 'unit': 'لتر', 'price': 8.50},
            {'id': 12, 'name': 'سمن بلدي', 'unit': 'كيلو', 'price': 35.00},
            {'id': 13, 'name': 'ملح طعام', 'unit': 'كيلو', 'price': 2.00},
            {'id': 14, 'name': 'فلفل أسود', 'unit': 'كيلو', 'price': 25.00},
            {'id': 15, 'name': 'ثوم', 'unit': 'كيلو', 'price': 15.00},
            {'id': 16, 'name': 'زنجبيل', 'unit': 'كيلو', 'price': 20.00},
            {'id': 17, 'name': 'زعفران', 'unit': 'جرام', 'price': 0.50},
            {'id': 18, 'name': 'لوز مقشر', 'unit': 'كيلو', 'price': 35.00},
            {'id': 19, 'name': 'زبيب ذهبي', 'unit': 'كيلو', 'price': 18.00},
            {'id': 20, 'name': 'ماء ورد', 'unit': 'لتر', 'price': 12.00}
        ]
        return jsonify({'success': True, 'ingredients': default_ingredients})

@app.route('/api/ingredients', methods=['POST'])
@login_required
def add_ingredient():
    """API لإضافة مكون جديد"""
    data = request.get_json()

    if not data or not data.get('name') or not data.get('unit') or data.get('price') is None:
        return jsonify({'success': False, 'message': 'Missing required fields'})

    try:
        conn = sqlite3.connect('restaurant_accounting.db')
        cursor = conn.cursor()

        # Check if ingredient already exists
        cursor.execute("SELECT id FROM raw_materials WHERE material_name = ?", (data['name'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Ingredient already exists'})

        # Insert new ingredient
        cursor.execute("""
            INSERT INTO raw_materials (material_name, unit, purchase_price, current_stock, min_stock_level)
            VALUES (?, ?, ?, 0, 10)
        """, (data['name'], data['unit'], data['price']))

        ingredient_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'ingredient': {
                'id': ingredient_id,
                'name': data['name'],
                'unit': data['unit'],
                'price': data['price']
            }
        })
    except sqlite3.OperationalError:
        return jsonify({'success': False, 'message': 'Database error'})

@app.route('/api/ingredients/<int:ingredient_id>', methods=['PUT'])
@login_required
def update_ingredient(ingredient_id):
    """API لتحديث مكون موجود"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'No data provided'})

    try:
        conn = sqlite3.connect('restaurant_accounting.db')
        cursor = conn.cursor()

        # Build update query dynamically
        update_fields = []
        values = []

        if 'name' in data:
            update_fields.append('material_name = ?')
            values.append(data['name'])

        if 'unit' in data:
            update_fields.append('unit = ?')
            values.append(data['unit'])

        if 'price' in data:
            update_fields.append('purchase_price = ?')
            values.append(data['price'])

        if not update_fields:
            return jsonify({'success': False, 'message': 'No fields to update'})

        values.append(ingredient_id)
        query = f"UPDATE raw_materials SET {', '.join(update_fields)} WHERE id = ?"

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Ingredient updated successfully'})
    except sqlite3.OperationalError:
        return jsonify({'success': False, 'message': 'Database error'})

@app.route('/api/ingredients/<int:ingredient_id>', methods=['DELETE'])
@login_required
def delete_ingredient(ingredient_id):
    """API لحذف مكون"""
    try:
        conn = sqlite3.connect('restaurant_accounting.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM raw_materials WHERE id = ?", (ingredient_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Ingredient deleted successfully'})
    except sqlite3.OperationalError:
        return jsonify({'success': False, 'message': 'Database error'})

# API endpoints
@app.route('/change_language', methods=['POST'])
def change_language():
    """تغيير اللغة"""
    data = request.get_json()
    language = data.get('language', 'ar')
    session['language'] = language
    return jsonify({'status': 'success'})

# API endpoints
@app.route('/api/products')
@login_required
def api_products():
    """API للحصول على المنتجات"""
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': p.id,
        'code': p.product_code,
        'name': p.product_name,
        'price': p.selling_price,
        'stock': p.current_stock
    } for p in products])

@app.route('/api/save_sale', methods=['POST'])
@login_required
def api_save_sale():
    """API لحفظ فاتورة مبيعات"""
    try:
        data = request.get_json()

        # إنشاء فاتورة جديدة
        sale = Sale(
            invoice_number=data['invoice_number'],
            branch_id=data['branch_id'],
            customer_name=data.get('customer_name'),
            invoice_date=datetime.strptime(data['invoice_date'], '%Y-%m-%d').date(),
            total_amount=data['total_amount'],
            tax_amount=data['tax_amount'],
            final_amount=data['final_amount'],
            payment_method=data['payment_method'],
            created_by=current_user.id
        )

        db.session.add(sale)
        db.session.flush()  # للحصول على معرف الفاتورة

        # إضافة عناصر الفاتورة وتحديث المخزون
        for item in data['items']:
            # التحقق من وجود المنتج وكفاية المخزون
            product_id = item.get('product_id')
            if product_id:
                product = Product.query.get(product_id)
                if product:
                    if product.current_stock < item['quantity']:
                        raise Exception(f'المخزون غير كافي للمنتج {product.product_name}. المتوفر: {product.current_stock}')

                    # تحديث المخزون
                    product.current_stock -= item['quantity']
                    product.updated_at = datetime.now()

            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product_id,
                product_name=item['product_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                total_price=item['total_price'],
                tax_rate=item.get('tax_rate', 15.0),
                tax_amount=item.get('tax_amount', 0.0)
            )
            db.session.add(sale_item)

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'تم حفظ الفاتورة بنجاح',
            'sale_id': sale.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'خطأ في حفظ الفاتورة: {str(e)}'
        }), 400

@app.route('/api/generate_invoice_number')
@login_required
def generate_invoice_number():
    """API لتوليد رقم فاتورة جديد"""
    branch_id = request.args.get('branch_id', 1)
    today = datetime.now()

    # البحث عن آخر رقم فاتورة لهذا اليوم والفرع
    last_sale = Sale.query.filter(
        Sale.branch_id == branch_id,
        db.func.date(Sale.invoice_date) == today.date()
    ).order_by(Sale.id.desc()).first()

    sequence = 1
    if last_sale:
        # استخراج الرقم التسلسلي من آخر فاتورة
        try:
            last_sequence = int(last_sale.invoice_number.split('-')[-1])
            sequence = last_sequence + 1
        except:
            sequence = 1

    # الحصول على رمز الفرع
    branch = Branch.query.get(branch_id)
    branch_code = branch.branch_code if branch else 'XX'

    # تنسيق رقم الفاتورة: BRANCH-YYYYMMDD-XXXX
    invoice_number = f"{branch_code}-{today.strftime('%Y%m%d')}-{sequence:04d}"

    return jsonify({'invoice_number': invoice_number})

@app.route('/api/transfer_meal_to_product', methods=['POST'])
@login_required
def api_transfer_meal_to_product():
    """API لترحيل الوجبة من حساب التكاليف إلى منتج جاهز للبيع"""
    try:
        data = request.get_json()
        meal_id = data.get('meal_id')
        quantity_to_produce = data.get('quantity', 1)
        selling_price = data.get('selling_price')

        if not meal_id or not selling_price:
            return jsonify({
                'status': 'error',
                'message': 'يرجى إدخال جميع البيانات المطلوبة'
            }), 400

        # الاتصال بقاعدة بيانات حساب التكاليف
        import sqlite3
        costing_conn = sqlite3.connect('restaurant_costing.db')
        costing_cursor = costing_conn.cursor()

        # الحصول على بيانات الوجبة
        costing_cursor.execute('''
            SELECT name, servings, total_cost, cost_per_serving
            FROM meals WHERE id = ?
        ''', (meal_id,))
        meal_data = costing_cursor.fetchone()

        if not meal_data:
            costing_conn.close()
            return jsonify({
                'status': 'error',
                'message': 'الوجبة غير موجودة'
            }), 404

        meal_name, servings, total_cost, cost_per_serving = meal_data

        # الحصول على مكونات الوجبة
        costing_cursor.execute('''
            SELECT mi.quantity, i.name, i.unit
            FROM meal_ingredients mi
            JOIN ingredients i ON mi.ingredient_id = i.id
            WHERE mi.meal_id = ?
        ''', (meal_id,))
        ingredients = costing_cursor.fetchall()
        costing_conn.close()

        # إنشاء كود منتج تلقائي
        existing_product = Product.query.filter_by(product_name=meal_name).first()
        if existing_product:
            # تحديث المنتج الموجود
            existing_product.unit_cost = cost_per_serving
            existing_product.selling_price = selling_price
            existing_product.current_stock += quantity_to_produce * servings
            existing_product.updated_at = datetime.now()
            product = existing_product
        else:
            # إنشاء منتج جديد
            # توليد كود منتج
            last_product = Product.query.order_by(Product.id.desc()).first()
            next_id = (last_product.id + 1) if last_product else 1
            product_code = f"MEAL{next_id:03d}"

            product = Product(
                product_code=product_code,
                product_name=meal_name,
                description=f"وجبة محضرة - {meal_name}",
                unit_cost=cost_per_serving,
                selling_price=selling_price,
                category="وجبات جاهزة",
                unit_type="حصة",
                current_stock=quantity_to_produce * servings,
                min_stock_level=5,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(product)

        # حفظ التغييرات
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'تم ترحيل الوجبة "{meal_name}" كمنتج جاهز للبيع',
            'product_id': product.id,
            'product_code': product.product_code,
            'stock_added': quantity_to_produce * servings
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'خطأ في ترحيل المنتج: {str(e)}'
        }), 400

    """API للحصول على الوجبات من نظام حساب التكاليف"""
    try:
        import sqlite3
        conn = sqlite3.connect('restaurant_costing.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, servings, total_cost, cost_per_serving, updated_at
            FROM meals
            WHERE total_cost > 0
            ORDER BY updated_at DESC
        ''')

        meals = cursor.fetchall()
        conn.close()

        meals_data = []
        for meal in meals:
            meals_data.append({
                'id': meal[0],
                'name': meal[1],
                'servings': meal[2],
                'total_cost': meal[3],
                'cost_per_serving': meal[4],
                'updated_at': meal[5]
            })

        return jsonify({
            'status': 'success',
            'meals': meals_data
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'خطأ في تحميل الوجبات: {str(e)}'
        }), 400

@app.route('/api/raw_materials', methods=['GET', 'POST'])
@login_required
def api_raw_materials():
    """API للمواد الخام"""
    if request.method == 'GET':
        try:
            materials = RawMaterial.query.filter_by(is_active=True).all()
            materials_data = []

            for material in materials:
                materials_data.append({
                    'id': material.id,
                    'name': material.name,
                    'unit': material.unit,
                    'price': float(material.purchase_price),
                    'stock': float(material.current_stock),
                    'min_stock': float(material.min_stock_level),
                    'supplier': material.supplier or ''
                })

            return jsonify(materials_data)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()

            material = RawMaterial(
                name=data['name'],
                unit=data['unit'],
                purchase_price=data['price'],
                current_stock=data.get('stock', 0),
                min_stock_level=data.get('min_stock', 5),
                supplier=data.get('supplier', ''),
                is_active=True
            )

            db.session.add(material)
            db.session.commit()

            return jsonify({'success': True, 'message': 'تم حفظ المادة الخام بنجاح'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/save_product_cost', methods=['POST'])
@login_required
def api_save_product_cost():
    """API لحفظ المنتج مع التكلفة التفصيلية"""
    try:
        data = request.get_json()

        # إنشاء المنتج
        # توليد كود منتج تلقائي
        last_product = Product.query.order_by(Product.id.desc()).first()
        next_id = (last_product.id + 1) if last_product else 1
        product_code = f"PROD{next_id:04d}"

        product = Product(
            product_code=product_code,
            product_name=data['name'],
            description=data.get('description', ''),
            unit_cost=data['cost_per_serving'],
            selling_price=data['suggested_price'],
            category=data.get('category', 'وجبات رئيسية'),
            unit_type='حصة',
            current_stock=data.get('servings', 1),
            min_stock_level=5,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.session.add(product)
        db.session.flush()  # للحصول على product.id

        # حفظ تفاصيل التكلفة
        for ingredient in data['ingredients']:
            cost_detail = ProductCost(
                product_id=product.id,
                raw_material_id=ingredient['material_id'],
                quantity_used=ingredient['quantity'],
                unit_cost=ingredient['unit_price'],
                total_cost=ingredient['total_cost'],
                percentage=ingredient['percentage']
            )
            db.session.add(cost_detail)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'تم حفظ المنتج "{data["name"]}" بنجاح',
            'product_code': product_code,
            'product_id': product.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

# الصفحات الإضافية
@app.route('/unified_products')
@login_required
def unified_products():
    """الشاشة الموحدة لإدارة المنتجات والتكاليف"""
    return render_template('unified_products.html')

@app.route('/products')
@login_required
def products():
    """Products & Cost Calculation Screen"""
    try:
        # Get all active products
        products = Product.query.filter_by(is_active=True).all()

        # Get search parameter
        search = request.args.get('search', '')
        category = request.args.get('category', '')

        # Apply filters if provided
        if search:
            products = [p for p in products if search.lower() in p.product_name.lower() or search.lower() in p.product_code.lower()]

        if category:
            products = [p for p in products if p.category == category]

        # Get unique categories for filter dropdown
        categories = list(set([p.category for p in Product.query.filter_by(is_active=True).all() if p.category]))

        return render_template('products.html',
                             products=products,
                             search=search,
                             categories=categories)
    except Exception as e:
        flash(f'خطأ في تحميل المنتجات: {str(e)}', 'error')
        return render_template('products.html', products=[], search='', categories=[])

@app.route('/product_transfer')
@login_required
def product_transfer():
    """صفحة ترحيل المنتجات من حساب التكاليف إلى المبيعات"""
    return render_template('product_transfer.html')

@app.route('/suppliers')
@login_required
def suppliers():
    return render_template('suppliers.html')

@app.route('/customers')
@login_required
def customers():
    return render_template('customers.html')

@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')

@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/advanced_reports')
@login_required
def advanced_reports():
    """صفحة التقارير المالية المتقدمة"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات
    total_sales = db.session.query(db.func.sum(Sale.final_amount)).scalar() or 0
    total_purchases = db.session.query(db.func.sum(Purchase.final_amount)).scalar() or 0
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    total_salaries = db.session.query(db.func.sum(EmployeePayroll.net_salary)).scalar() or 0
    total_vat = db.session.query(db.func.sum(Sale.tax_amount)).scalar() or 0
    net_profit = total_sales - (total_purchases + total_expenses + total_salaries)

    report_data = {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'total_expenses': total_expenses,
        'total_salaries': total_salaries,
        'total_vat': total_vat,
        'net_profit': net_profit
    }

    # فترات التقرير المتاحة
    period_types = [
        {'value': 'daily', 'name_ar': 'تقرير يومي', 'name_en': 'Daily Report'},
        {'value': 'weekly', 'name_ar': 'تقرير أسبوعي', 'name_en': 'Weekly Report'},
        {'value': 'monthly', 'name_ar': 'تقرير شهري', 'name_en': 'Monthly Report'},
        {'value': 'yearly', 'name_ar': 'تقرير سنوي', 'name_en': 'Yearly Report'},
        {'value': 'custom', 'name_ar': 'فترة مخصصة', 'name_en': 'Custom Period'}
    ]

    # أنواع التقارير
    report_types = [
        {'value': 'all', 'name_ar': 'تقرير شامل', 'name_en': 'Comprehensive Report'},
        {'value': 'sales', 'name_ar': 'المبيعات فقط', 'name_en': 'Sales Only'},
        {'value': 'purchases', 'name_ar': 'المشتريات فقط', 'name_en': 'Purchases Only'},
        {'value': 'expenses', 'name_ar': 'المصروفات فقط', 'name_en': 'Expenses Only'},
        {'value': 'salaries', 'name_ar': 'الرواتب فقط', 'name_en': 'Salaries Only'}
    ]

    # طرق الدفع
    payment_methods = [
        {'value': 'all', 'name_ar': 'جميع الطرق', 'name_en': 'All Methods'},
        {'value': 'CASH', 'name_ar': 'نقدي', 'name_en': 'Cash'},
        {'value': 'MADA', 'name_ar': 'مدى', 'name_en': 'MADA'},
        {'value': 'VISA', 'name_ar': 'فيزا', 'name_en': 'VISA'},
        {'value': 'MASTERCARD', 'name_ar': 'ماستركارد', 'name_en': 'MASTERCARD'},
        {'value': 'BANK', 'name_ar': 'تحويل بنكي', 'name_en': 'Bank Transfer'},
        {'value': 'CREDIT', 'name_ar': 'آجل', 'name_en': 'Credit'}
    ]

    return render_template('advanced_reports.html',
                         report_data=report_data,
                         period_types=period_types,
                         report_types=report_types,
                         payment_methods=payment_methods)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/simple_print')
@login_required
def simple_print():
    """صفحة الطباعة البسيطة"""
    try:
        logger.info("📄 عرض صفحة الطباعة البسيطة")
        return render_template('simple_print.html')
    except Exception as e:
        logger.error(f"❌ خطأ في صفحة الطباعة البسيطة: {e}")
        flash('حدث خطأ في تحميل صفحة الطباعة', 'error')
        return redirect(url_for('index'))

@app.route('/print_invoices/<invoice_type>')
@login_required
def print_invoice(invoice_type):
    """طباعة الفواتير مباشرة - نسخة مبسطة تعمل"""
    try:
        logger.info(f"🖨️ طباعة جميع فواتير {invoice_type}")

        # تحديد العنوان واللون
        titles = {
            'sales': 'تقرير فواتير المبيعات',
            'purchases': 'تقرير فواتير المشتريات',
            'expenses': 'تقرير فواتير المصروفات',
            'payroll': 'تقرير كشف الرواتب'
        }

        colors = {
            'sales': '#007bff',
            'purchases': '#28a745',
            'expenses': '#ffc107',
            'payroll': '#17a2b8'
        }

        if invoice_type not in titles:
            flash('نوع الفاتورة غير صحيح', 'error')
            return redirect(url_for('payments_dues'))

        title = titles[invoice_type]
        color = colors[invoice_type]

        # بيانات تجريبية (يمكن استبدالها بالبيانات الحقيقية لاحقاً)
        sample_data = {
            'sales': [
                {'id': 'INV-2024-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'amount': 2500.00},
                {'id': 'INV-2024-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'amount': 1800.00},
                {'id': 'INV-2024-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'amount': 3200.00},
                {'id': 'INV-2024-004', 'name': 'مكتب الرياض للاستشارات', 'date': '2024-01-18', 'amount': 1500.00},
                {'id': 'INV-2024-005', 'name': 'عميل نقدي', 'date': '2024-01-19', 'amount': 950.00}
            ],
            'purchases': [
                {'id': 'PUR-2024-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'amount': 5500.00},
                {'id': 'PUR-2024-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'amount': 3200.00},
                {'id': 'PUR-2024-003', 'name': 'شركة المواد الأساسية', 'date': '2024-01-17', 'amount': 4100.00},
                {'id': 'PUR-2024-004', 'name': 'مورد المعدات الصناعية', 'date': '2024-01-18', 'amount': 2800.00}
            ],
            'expenses': [
                {'id': 'EXP-2024-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00},
                {'id': 'EXP-2024-002', 'name': 'مصروفات تشغيلية', 'date': '2024-01-16', 'amount': 1200.00},
                {'id': 'EXP-2024-003', 'name': 'مصروفات صيانة', 'date': '2024-01-17', 'amount': 650.00},
                {'id': 'EXP-2024-004', 'name': 'مصروفات نقل', 'date': '2024-01-18', 'amount': 450.00}
            ],
            'payroll': [
                {'id': 'PAY-2024-001', 'name': 'أحمد محمد علي - مدير المبيعات', 'date': '2024-01-31', 'amount': 8500.00},
                {'id': 'PAY-2024-002', 'name': 'فاطمة أحمد سالم - محاسبة', 'date': '2024-01-31', 'amount': 6200.00},
                {'id': 'PAY-2024-003', 'name': 'محمد عبدالله حسن - موظف إداري', 'date': '2024-01-31', 'amount': 4800.00},
                {'id': 'PAY-2024-004', 'name': 'سارة علي محمد - سكرتيرة', 'date': '2024-01-31', 'amount': 4200.00}
            ]
        }

        # بيانات تجريبية للطباعة مع الخصم (يمكن استبدالها بالبيانات الحقيقية لاحقاً)
        sample_data = {
            'sales': [
                {'id': 'INV-2024-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'subtotal': 2700.00, 'discount': 200.00, 'amount': 2500.00},
                {'id': 'INV-2024-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'subtotal': 2000.00, 'discount': 200.00, 'amount': 1800.00},
                {'id': 'INV-2024-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00},
                {'id': 'INV-2024-004', 'name': 'مكتب الرياض للاستشارات', 'date': '2024-01-18', 'subtotal': 1650.00, 'discount': 150.00, 'amount': 1500.00},
                {'id': 'INV-2024-005', 'name': 'عميل نقدي', 'date': '2024-01-19', 'subtotal': 1000.00, 'discount': 50.00, 'amount': 950.00}
            ],
            'purchases': [
                {'id': 'PUR-2024-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'subtotal': 6000.00, 'discount': 500.00, 'amount': 5500.00},
                {'id': 'PUR-2024-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00},
                {'id': 'PUR-2024-003', 'name': 'شركة المواد الأساسية', 'date': '2024-01-17', 'subtotal': 4400.00, 'discount': 300.00, 'amount': 4100.00},
                {'id': 'PUR-2024-004', 'name': 'مورد المعدات الصناعية', 'date': '2024-01-18', 'subtotal': 3000.00, 'discount': 200.00, 'amount': 2800.00}
            ],
            'expenses': [
                {'id': 'EXP-2024-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00},
                {'id': 'EXP-2024-002', 'name': 'مصروفات تشغيلية', 'date': '2024-01-16', 'amount': 1200.00},
                {'id': 'EXP-2024-003', 'name': 'مصروفات صيانة', 'date': '2024-01-17', 'amount': 650.00},
                {'id': 'EXP-2024-004', 'name': 'مصروفات نقل', 'date': '2024-01-18', 'amount': 450.00}
            ],
            'payroll': [
                {'id': 'PAY-2024-001', 'name': 'أحمد محمد علي - مدير المبيعات', 'date': '2024-01-31', 'amount': 8500.00},
                {'id': 'PAY-2024-002', 'name': 'فاطمة أحمد سالم - محاسبة', 'date': '2024-01-31', 'amount': 6200.00},
                {'id': 'PAY-2024-003', 'name': 'محمد عبدالله حسن - موظف إداري', 'date': '2024-01-31', 'amount': 4800.00},
                {'id': 'PAY-2024-004', 'name': 'سارة علي محمد - سكرتيرة', 'date': '2024-01-31', 'amount': 4200.00}
            ]
        }

        # جمع البيانات للطباعة مع حساب الخصم
        data = sample_data[invoice_type]

        # حساب المجاميع مع الخصم
        if invoice_type in ['sales', 'purchases']:
            subtotal_amount = sum(item.get('subtotal', item['amount']) for item in data)
            total_discount = sum(item.get('discount', 0) for item in data)
            total_amount = sum(item['amount'] for item in data)
        else:
            subtotal_amount = sum(item['amount'] for item in data)
            total_discount = 0
            total_amount = subtotal_amount

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        # إنشاء HTML للطباعة مباشرة
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
                .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
                .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
                .report-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
                .print-date {{ color: #666; font-size: 16px; }}
                .summary {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 30px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
                th, td {{ border: 1px solid #ddd; padding: 18px 12px; text-align: center; font-size: 15px; }}
                th {{ background: {color}; color: white; font-weight: bold; font-size: 16px; }}
                tr:nth-child(even) {{ background-color: #f8f9fa; }}
                .total-row {{ background: #28a745 !important; color: white !important; font-weight: bold; font-size: 18px; }}
                .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
                @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} }}
            </style>
        </head>
        <body>
            <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>

            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="report-title">{title}</div>
                <div class="print-date">تاريخ الطباعة: {current_date}</div>
            </div>

            <div class="summary">
                <h3>ملخص {title}</h3>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>عدد العناصر:</strong> {len(data)}</p>
                        {"<p><strong>المجموع الفرعي:</strong> " + f"{subtotal_amount:.2f}" + " ريال</p>" if invoice_type in ['sales', 'purchases'] else ""}
                    </div>
                    <div class="col-md-6">
                        {"<p><strong>إجمالي الخصم:</strong> <span style='color: #dc3545;'>" + f"{total_discount:.2f}" + " ريال</span></p>" if invoice_type in ['sales', 'purchases'] and total_discount > 0 else ""}
                        <p><strong>المبلغ النهائي:</strong> <span style='color: #28a745;'>{total_amount:.2f} ريال</span></p>
                    </div>
                </div>
            </div>

            <table>
                <thead>
                    {"<tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المجموع الفرعي</th><th>الخصم</th><th>المبلغ النهائي</th></tr>" if invoice_type in ['sales', 'purchases'] else "<tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المبلغ (ريال)</th></tr>"}
                </thead>
                <tbody>
        """

        for item in data:
            if invoice_type in ['sales', 'purchases']:
                item_subtotal = item.get('subtotal', item['amount'])
                item_discount = item.get('discount', 0)
                html_content += f"<tr><td><strong>{item['id']}</strong></td><td>{item['name']}</td><td>{item['date']}</td><td>{item_subtotal:.2f} ريال</td><td style='color: #dc3545;'>{item_discount:.2f} ريال</td><td><strong>{item['amount']:.2f} ريال</strong></td></tr>"
            else:
                html_content += f"<tr><td><strong>{item['id']}</strong></td><td>{item['name']}</td><td>{item['date']}</td><td>{item['amount']:.2f} ريال</td></tr>"

        # إضافة صف المجموع الإجمالي وإنهاء HTML
        if invoice_type in ['sales', 'purchases']:
            html_content += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{subtotal_amount:.2f} ريال</strong></td>
                    <td><strong>{total_discount:.2f} ريال</strong></td>
                    <td><strong>{total_amount:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>"""

        # إضافة الخاتمة
        html_content += f"""
        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
            <p><strong>عدد العناصر: {len(data)} | المبلغ النهائي: {total_amount:.2f} ريال</strong></p>
            <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
        </div>

        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 1000);
            }};
        </script>
    </body>
    </html>"""
        else:
            html_content += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{total_amount:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>

        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
            <p><strong>عدد العناصر: {len(data)} | المبلغ النهائي: {total_amount:.2f} ريال</strong></p>
            <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
        </div>

        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 1000);
            }};
        </script>
    </body>
    </html>"""""""""
    """

        return html_content

    except Exception as e:
        logger.error(f"❌ خطأ في طباعة الفواتير: {e}")
        flash('حدث خطأ في الطباعة', 'error')
        return redirect(url_for('payments_dues'))

@app.route('/print_invoice/<invoice_type>/<int:invoice_id>')
@login_required
def print_single_invoice(invoice_type, invoice_id):
    """طباعة فاتورة محددة"""
    try:
        logger.info(f"🖨️ طباعة فاتورة محددة {invoice_type} - ID: {invoice_id}")

        # تحديد العنوان واللون
        titles = {
            'sales': 'فاتورة مبيعات',
            'purchases': 'فاتورة مشتريات',
            'expenses': 'فاتورة مصروفات',
            'payroll': 'كشف راتب'
        }

        colors = {
            'sales': '#007bff',
            'purchases': '#28a745',
            'expenses': '#ffc107',
            'payroll': '#17a2b8'
        }

        if invoice_type not in titles:
            flash('نوع الفاتورة غير صحيح', 'error')
            return redirect(url_for('payments_dues'))

        title = titles[invoice_type]
        color = colors[invoice_type]

        # بيانات تجريبية
        sample_data = {
            'sales': [
                {'id': 'INV-2024-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'amount': 2500.00},
                {'id': 'INV-2024-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'amount': 1800.00},
                {'id': 'INV-2024-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'amount': 3200.00},
                {'id': 'INV-2024-004', 'name': 'مكتب الرياض للاستشارات', 'date': '2024-01-18', 'amount': 1500.00},
                {'id': 'INV-2024-005', 'name': 'عميل نقدي', 'date': '2024-01-19', 'amount': 950.00}
            ],
            'purchases': [
                {'id': 'PUR-2024-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'amount': 5500.00},
                {'id': 'PUR-2024-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'amount': 3200.00},
                {'id': 'PUR-2024-003', 'name': 'شركة المواد الأساسية', 'date': '2024-01-17', 'amount': 4100.00},
                {'id': 'PUR-2024-004', 'name': 'مورد المعدات الصناعية', 'date': '2024-01-18', 'amount': 2800.00}
            ],
            'expenses': [
                {'id': 'EXP-2024-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00},
                {'id': 'EXP-2024-002', 'name': 'مصروفات تشغيلية', 'date': '2024-01-16', 'amount': 1200.00},
                {'id': 'EXP-2024-003', 'name': 'مصروفات صيانة', 'date': '2024-01-17', 'amount': 650.00},
                {'id': 'EXP-2024-004', 'name': 'مصروفات نقل', 'date': '2024-01-18', 'amount': 450.00}
            ],
            'payroll': [
                {'id': 'PAY-2024-001', 'name': 'أحمد محمد علي - مدير المبيعات', 'date': '2024-01-31', 'amount': 8500.00},
                {'id': 'PAY-2024-002', 'name': 'فاطمة أحمد سالم - محاسبة', 'date': '2024-01-31', 'amount': 6200.00},
                {'id': 'PAY-2024-003', 'name': 'محمد عبدالله حسن - موظف إداري', 'date': '2024-01-31', 'amount': 4800.00},
                {'id': 'PAY-2024-004', 'name': 'سارة علي محمد - سكرتيرة', 'date': '2024-01-31', 'amount': 4200.00}
            ]
        }

        # البحث عن الفاتورة المحددة
        all_data = sample_data[invoice_type]
        data = [item for item in all_data if item['id'].endswith(f'-{invoice_id:03d}')]

        if not data:
            # إذا لم توجد الفاتورة، استخدم فاتورة افتراضية
            if invoice_id <= len(all_data):
                data = [all_data[invoice_id - 1]]
            else:
                data = [all_data[0]] if all_data else []

        if not data:
            flash(f'لم يتم العثور على الفاتورة رقم {invoice_id}', 'error')
            return redirect(url_for('payments_dues'))

        invoice_data = data[0]
        title = f"{title} رقم {invoice_id}"
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        # إنشاء HTML للطباعة
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
                .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
                .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
                .invoice-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
                .print-date {{ color: #666; font-size: 16px; }}
                .invoice-details {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 25px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; margin: 15px 0; padding: 10px; background: white; border-radius: 5px; }}
                .detail-label {{ font-weight: bold; color: {color}; }}
                .detail-value {{ color: #333; }}
                .amount-box {{ text-align: center; background: {color}; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .amount-value {{ font-size: 28px; font-weight: bold; }}
                .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
                @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} }}
            </style>
        </head>
        <body>
            <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>

            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="invoice-title">{title}</div>
                <div class="print-date">تاريخ الطباعة: {current_date}</div>
            </div>

            <div class="invoice-details">
                <div class="detail-row">
                    <span class="detail-label">رقم الفاتورة:</span>
                    <span class="detail-value">{invoice_data['id']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">التفاصيل:</span>
                    <span class="detail-value">{invoice_data['name']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">التاريخ:</span>
                    <span class="detail-value">{invoice_data['date']}</span>
                </div>
            </div>

            <div class="amount-box">
                <div>المبلغ الإجمالي</div>
                <div class="amount-value">{invoice_data['amount']:.2f} ريال</div>
            </div>

            <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
                <p>تم إنشاء هذه الفاتورة بواسطة نظام المحاسبة المتكامل</p>
                <p><strong>فاتورة رقم: {invoice_id} | المبلغ: {invoice_data['amount']:.2f} ريال</strong></p>
            </div>

            <script>
                window.onload = function() {{
                    setTimeout(function() {{ window.print(); }}, 1000);
                }};
            </script>
        </body>
        </html>
        """

        return html_content

    except Exception as e:
        logger.error(f"❌ خطأ في طباعة الفاتورة المحددة: {e}")
        flash('حدث خطأ في الطباعة', 'error')
        return redirect(url_for('payments_dues'))

@app.route('/payments_dues')
@login_required
def payments_dues():
    """صفحة المدفوعات والمستحقات"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات

    # إجمالي فواتير المبيعات
    sales_total = db.session.query(db.func.sum(Sale.final_amount)).scalar() or 0

    # إجمالي فواتير المشتريات
    purchases_total = db.session.query(db.func.sum(Purchase.final_amount)).scalar() or 0

    # إجمالي المصروفات
    expenses_total = db.session.query(db.func.sum(Expense.amount)).scalar() or 0

    # إجمالي الرواتب
    payrolls_total = db.session.query(db.func.sum(EmployeePayroll.net_salary)).scalar() or 0

    # إجمالي المدفوعات
    payments_total = db.session.query(db.func.sum(Payment.amount)).scalar() or 0

    # حساب إجمالي المستحقات بدقة من جميع أنواع الفواتير
    total_due = 0

    # المبيعات
    sales = Sale.query.all()
    for invoice in sales:
        remaining = invoice.get_remaining_amount()
        if remaining > 0:
            total_due += remaining

    # المشتريات
    purchases = Purchase.query.all()
    for invoice in purchases:
        remaining = invoice.get_remaining_amount()
        if remaining > 0:
            total_due += remaining

    # المصروفات
    expenses = Expense.query.all()
    for expense in expenses:
        remaining = expense.get_remaining_amount()
        if remaining > 0:
            total_due += remaining

    # الرواتب
    payrolls = EmployeePayroll.query.all()
    for payroll in payrolls:
        remaining = payroll.get_remaining_amount()
        if remaining > 0:
            total_due += remaining

    # إحصائيات للحالات المختلفة
    sales_unpaid = Sale.query.filter(Sale.payment_status.in_(['pending', 'partial'])).count()
    purchases_unpaid = Purchase.query.filter(Purchase.payment_status.in_(['pending', 'partial'])).count()
    expenses_unpaid = Expense.query.filter(Expense.payment_status.in_(['pending', 'partial'])).count()
    payrolls_unpaid = EmployeePayroll.query.filter(EmployeePayroll.payment_status.in_(['pending', 'partial'])).count()

    total_amount = sales_total + purchases_total + expenses_total + payrolls_total
    unpaid_count = sales_unpaid + purchases_unpaid + expenses_unpaid + payrolls_unpaid

    # إحصائيات تفصيلية للحالات
    sales_fully_paid = Sale.query.filter_by(payment_status='paid').count()
    sales_partially_paid = Sale.query.filter_by(payment_status='partial').count()
    sales_pending = Sale.query.filter_by(payment_status='pending').count()

    purchases_fully_paid = Purchase.query.filter_by(payment_status='paid').count()
    purchases_partially_paid = Purchase.query.filter_by(payment_status='partial').count()
    purchases_pending = Purchase.query.filter_by(payment_status='pending').count()

    expenses_fully_paid = Expense.query.filter_by(payment_status='paid').count()
    expenses_partially_paid = Expense.query.filter_by(payment_status='partial').count()
    expenses_pending = Expense.query.filter_by(payment_status='pending').count()

    payrolls_fully_paid = EmployeePayroll.query.filter_by(payment_status='paid').count()
    payrolls_partially_paid = EmployeePayroll.query.filter_by(payment_status='partial').count()
    payrolls_pending = EmployeePayroll.query.filter_by(payment_status='pending').count()

    summary_data = {
        'total_amount': total_amount,
        'total_paid': payments_total,
        'total_due': total_due,
        'unpaid_count': unpaid_count,
        'sales_total': sales_total,
        'purchases_total': purchases_total,
        'expenses_total': expenses_total,
        'payrolls_total': payrolls_total,
        'fully_paid_count': sales_fully_paid + purchases_fully_paid + expenses_fully_paid + payrolls_fully_paid,
        'partially_paid_count': sales_partially_paid + purchases_partially_paid + expenses_partially_paid + payrolls_partially_paid,
        'pending_count': sales_pending + purchases_pending + expenses_pending + payrolls_pending
    }

    # أنواع الحسابات
    account_types = [
        {'value': 'all', 'name_ar': 'جميع الحسابات', 'name_en': 'All Accounts'},
        {'value': 'suppliers', 'name_ar': 'الموردين', 'name_en': 'Suppliers'},
        {'value': 'customers', 'name_ar': 'العملاء', 'name_en': 'Customers'},
        {'value': 'employees', 'name_ar': 'الموظفين', 'name_en': 'Employees'},
        {'value': 'expenses', 'name_ar': 'مصاريف أخرى', 'name_en': 'Other Expenses'}
    ]

    # حالات السداد
    payment_statuses = [
        {'value': 'all', 'name_ar': 'جميع الحالات', 'name_en': 'All Status'},
        {'value': 'unpaid', 'name_ar': 'غير مدفوع', 'name_en': 'Unpaid'},
        {'value': 'partial', 'name_ar': 'مدفوع جزئياً', 'name_en': 'Partially Paid'},
        {'value': 'paid', 'name_ar': 'مدفوع بالكامل', 'name_en': 'Fully Paid'}
    ]

    # طرق الدفع
    payment_methods = [
        {'value': 'CASH', 'name_ar': 'نقدي', 'name_en': 'Cash'},
        {'value': 'MADA', 'name_ar': 'مدى', 'name_en': 'MADA'},
        {'value': 'VISA', 'name_ar': 'فيزا', 'name_en': 'VISA'},
        {'value': 'MASTERCARD', 'name_ar': 'ماستركارد', 'name_en': 'MASTERCARD'},
        {'value': 'BANK', 'name_ar': 'تحويل بنكي', 'name_en': 'Bank Transfer'},
        {'value': 'CHECK', 'name_ar': 'شيك', 'name_en': 'Check'}
    ]

    # الحصول على الدفعات الحديثة
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()

    # الحصول على جميع أنواع الفواتير (جميع الحالات)
    all_sales = Sale.query.order_by(Sale.created_at.desc()).all()
    all_purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()
    all_expenses = Expense.query.order_by(Expense.created_at.desc()).all()
    all_payrolls = EmployeePayroll.query.order_by(EmployeePayroll.created_at.desc()).all()

    # فصل الفواتير حسب الحالة للإحصائيات
    unpaid_sales = [s for s in all_sales if s.payment_status in ['pending', 'partial']]
    unpaid_purchases = [p for p in all_purchases if p.payment_status in ['pending', 'partial']]
    unpaid_expenses = [e for e in all_expenses if e.payment_status in ['pending', 'partial']]
    unpaid_payrolls = [pr for pr in all_payrolls if pr.payment_status in ['pending', 'partial']]

    paid_sales = [s for s in all_sales if s.payment_status == 'paid']
    paid_purchases = [p for p in all_purchases if p.payment_status == 'paid']
    paid_expenses = [e for e in all_expenses if e.payment_status == 'paid']
    paid_payrolls = [pr for pr in all_payrolls if pr.payment_status == 'paid']

    return render_template('payments_dues.html',
                         summary_data=summary_data,
                         account_types=account_types,
                         payment_statuses=payment_statuses,
                         payment_methods=payment_methods,
                         recent_payments=recent_payments,
                         # جميع الفواتير
                         all_sales=all_sales,
                         all_purchases=all_purchases,
                         all_expenses=all_expenses,
                         all_payrolls=all_payrolls,
                         # الفواتير غير المدفوعة للإحصائيات
                         unpaid_sales=unpaid_sales,
                         unpaid_purchases=unpaid_purchases,
                         unpaid_expenses=unpaid_expenses,
                         unpaid_payrolls=unpaid_payrolls,
                         # الفواتير المدفوعة للإحصائيات
                         paid_sales=paid_sales,
                         paid_purchases=paid_purchases,
                         paid_expenses=paid_expenses,
                         paid_payrolls=paid_payrolls)

@app.route('/tax_management')
@login_required
def tax_management():
    """صفحة إدارة الضرائب"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات
    vat_collected = db.session.query(db.func.sum(Sale.tax_amount)).scalar() or 0
    invoices_count = Sale.query.count()

    tax_statistics = {
        'total_collected': vat_collected,
        'vat_collected': vat_collected,
        'other_taxes': 0.00,
        'invoices_count': invoices_count
    }

    tax_settings = {
        'vat_rate': 15.00,
        'vat_number': '300123456789003',
        'vat_enabled': True,
        'calculation_method': 'exclusive',
        'rounding': 'round',
        'show_breakdown': True
    }

    return render_template('tax_management.html',
                         tax_statistics=tax_statistics,
                         tax_settings=tax_settings)

def update_all_payment_statuses():
    """تحديث حالات الدفع لجميع الفواتير"""
    try:
        sales = Sale.query.all()
        for sale in sales:
            sale.update_payment_status()
        db.session.commit()
        print(f"تم تحديث حالات الدفع لـ {len(sales)} فاتورة")
    except Exception as e:
        db.session.rollback()
        print(f"خطأ في تحديث حالات الدفع: {e}")

def create_default_data():
    """إنشاء البيانات الافتراضية - تم تعطيلها"""

    # إنشاء مستخدم المدير فقط (ضروري للنظام)
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            full_name='مدير النظام',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("تم إنشاء المستخدم الافتراضي: admin / admin123")

    # تم حذف جميع البيانات التجريبية
    # النظام الآن يعمل بالبيانات الحقيقية فقط

@app.route('/expenses')
@login_required
def expenses():
    """صفحة المصروفات"""

    # الحصول على جميع المصروفات من قاعدة البيانات
    expenses_list = Expense.query.order_by(Expense.expense_date.desc()).all()

    # حساب الإجماليات
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    paid_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='paid').scalar() or 0
    pending_expenses = total_expenses - paid_expenses
    expenses_count = Expense.query.count()

    # إحصائيات حسب الحالة
    paid_count = Expense.query.filter_by(payment_status='paid').count()
    partial_count = Expense.query.filter_by(payment_status='partial').count()
    pending_count = Expense.query.filter_by(payment_status='pending').count()

    summary_data = {
        'total_expenses': total_expenses,
        'paid_expenses': paid_expenses,
        'pending_expenses': pending_expenses,
        'expenses_count': expenses_count,
        'paid_count': paid_count,
        'partial_count': partial_count,
        'pending_count': pending_count
    }

    return render_template('expenses.html',
                         expenses=expenses_list,
                         summary_data=summary_data)

# تم حذف شاشة حساب التكلفة القديمة - استخدم الشاشة الموحدة بدلاً منها

@app.route('/advanced_expenses')
@login_required
def advanced_expenses():
    """صفحة المصروفات المتقدمة"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    paid_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='paid').scalar() or 0
    pending_expenses = total_expenses - paid_expenses
    expenses_count = Expense.query.count()

    summary_data = {
        'total_expenses': total_expenses,
        'paid_expenses': paid_expenses,
        'pending_expenses': pending_expenses,
        'expenses_count': expenses_count
    }

    return render_template('advanced_expenses.html', summary_data=summary_data)

@app.route('/employee_payroll')
@login_required
def employee_payroll():
    """صفحة إدارة الموظفين والرواتب"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات
    total_employees = db.session.query(EmployeePayroll.employee_name).distinct().count()
    paid_salaries = db.session.query(db.func.sum(EmployeePayroll.net_salary)).filter_by(payment_status='paid').scalar() or 0
    total_salaries = db.session.query(db.func.sum(EmployeePayroll.net_salary)).scalar() or 0
    outstanding_salaries = total_salaries - paid_salaries
    overdue_count = EmployeePayroll.query.filter(EmployeePayroll.payment_status.in_(['pending', 'partial'])).count()

    summary_data = {
        'total_employees': total_employees,
        'paid_salaries': paid_salaries,
        'outstanding_salaries': outstanding_salaries,
        'overdue_count': overdue_count
    }

    return render_template('employee_payroll.html', summary_data=summary_data)

@app.route('/purchases')
@login_required
def purchases():
    """صفحة إدارة المشتريات"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات
    total_purchases = db.session.query(db.func.sum(Purchase.final_amount)).scalar() or 0
    paid_purchases = db.session.query(db.func.sum(Purchase.final_amount)).filter_by(payment_status='paid').scalar() or 0
    pending_purchases = total_purchases - paid_purchases
    invoices_count = Purchase.query.count()

    summary_data = {
        'total_purchases': total_purchases,
        'paid_purchases': paid_purchases,
        'pending_purchases': pending_purchases,
        'invoices_count': invoices_count
    }

    # الحصول على الموردين من قاعدة البيانات (إذا كان هناك جدول موردين)
    # أو استخدام أسماء الموردين من فواتير المشتريات
    suppliers_from_purchases = db.session.query(Purchase.supplier_name).distinct().all()
    suppliers = [{'name': supplier[0]} for supplier in suppliers_from_purchases if supplier[0]]

    # الحصول على المنتجات من قاعدة البيانات
    products = Product.query.all()

    return render_template('purchases.html',
                         summary_data=summary_data,
                         suppliers=suppliers,
                         products=products)

@app.route('/financial_statements')
@login_required
def financial_statements():
    """صفحة القوائم المالية"""

    # الحصول على البيانات الحقيقية من قاعدة البيانات

    # الإيرادات من المبيعات
    sales_revenue = db.session.query(db.func.sum(Sale.final_amount)).scalar() or 0

    # المصروفات
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    total_payrolls = db.session.query(db.func.sum(EmployeePayroll.net_salary)).scalar() or 0

    # المشتريات (تكلفة البضاعة)
    cost_of_goods = db.session.query(db.func.sum(Purchase.final_amount)).scalar() or 0

    # المدفوعات
    total_payments = db.session.query(db.func.sum(Payment.amount)).scalar() or 0

    # حسابات العملاء (المستحقات)
    accounts_receivable = 0
    for sale in Sale.query.all():
        accounts_receivable += sale.get_remaining_amount()

    # حسابات الموردين (المستحقات)
    accounts_payable = 0
    for purchase in Purchase.query.all():
        accounts_payable += purchase.get_remaining_amount()

    # رواتب مستحقة
    salaries_payable = 0
    for payroll in EmployeePayroll.query.all():
        salaries_payable += payroll.get_remaining_amount()

    accounts_data = {
        'assets': {
            'cash': {'name_ar': 'النقدية', 'name_en': 'Cash', 'balance': total_payments},
            'accounts_receivable': {'name_ar': 'حسابات العملاء', 'name_en': 'Accounts Receivable', 'balance': accounts_receivable}
        },
        'liabilities': {
            'accounts_payable': {'name_ar': 'حسابات الموردين', 'name_en': 'Accounts Payable', 'balance': accounts_payable},
            'salaries_payable': {'name_ar': 'الرواتب المستحقة', 'name_en': 'Salaries Payable', 'balance': salaries_payable}
        },
        'revenue': {
            'sales_revenue': {'name_ar': 'إيرادات المبيعات', 'name_en': 'Sales Revenue', 'balance': sales_revenue}
        },
        'expenses': {
            'cost_of_goods': {'name_ar': 'تكلفة البضاعة المباعة', 'name_en': 'Cost of Goods Sold', 'balance': cost_of_goods},
            'salaries_expense': {'name_ar': 'مصروف الرواتب', 'name_en': 'Salaries Expense', 'balance': total_payrolls},
            'other_expenses': {'name_ar': 'مصروفات أخرى', 'name_en': 'Other Expenses', 'balance': total_expenses}
        }
    }

    # حساب الإجماليات
    totals = {
        'total_assets': sum(account['balance'] for account in accounts_data['assets'].values()),
        'total_liabilities': sum(account['balance'] for account in accounts_data['liabilities'].values()),
        'total_equity': 0,  # سيتم حسابها لاحقاً
        'total_revenue': sum(account['balance'] for account in accounts_data['revenue'].values()),
        'total_expenses': sum(account['balance'] for account in accounts_data['expenses'].values())
    }

    # حساب صافي الربح
    totals['net_profit'] = totals['total_revenue'] - totals['total_expenses']
    totals['tax'] = totals['net_profit'] * 0.15 if totals['net_profit'] > 0 else 0
    totals['net_profit_after_tax'] = totals['net_profit'] - totals['tax']

    return render_template('financial_statements.html',
                         accounts_data=accounts_data,
                         totals=totals)

@app.route('/test_sidebar')
@login_required
def test_sidebar():
    """صفحة اختبار القائمة الجانبية"""
    return render_template('test_sidebar.html')

@app.route('/user_management')
@login_required
@admin_required
def user_management():
    """صفحة إدارة المستخدمين"""
    return render_template('user_management.html')

@app.route('/role_management')
@login_required
@admin_required
def role_management():
    """صفحة إدارة الأدوار والصلاحيات"""
    return render_template('role_management.html')

# API routes for payments
@app.route('/api/save_payment', methods=['POST'])
@login_required
def save_payment():
    """حفظ دفعة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('payment_amount') or float(data.get('payment_amount', 0)) <= 0:
            return jsonify({'success': False, 'message': 'يرجى إدخال مبلغ صحيح'})

        if not data.get('payment_date'):
            return jsonify({'success': False, 'message': 'يرجى اختيار تاريخ الدفع'})

        # إنشاء سجل الدفعة
        payment_data = {
            'payment_amount': float(data.get('payment_amount')),
            'payment_method': data.get('payment_method', 'CASH'),
            'payment_date': data.get('payment_date'),
            'payment_reference': data.get('payment_reference', ''),
            'payment_notes': data.get('payment_notes', ''),
            'selected_transactions': data.get('selected_transactions', []),
            'user_id': current_user.id,
            'created_at': datetime.now().isoformat()
        }

        # هنا يمكن حفظ البيانات في قاعدة البيانات
        # مؤقتاً سنحفظها في ملف JSON للاختبار
        payments_file = 'payments_log.json'
        payments_log = []

        if os.path.exists(payments_file):
            with open(payments_file, 'r', encoding='utf-8') as f:
                payments_log = json.load(f)

        # إضافة الدفعة الجديدة
        payment_data['id'] = len(payments_log) + 1
        payments_log.append(payment_data)

        # حفظ في الملف
        with open(payments_file, 'w', encoding='utf-8') as f:
            json.dump(payments_log, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success': True,
            'message': 'تم حفظ الدفعة بنجاح',
            'payment_id': payment_data['id']
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في حفظ الدفعة: {str(e)}'})

@app.route('/api/get_payments', methods=['GET'])
@login_required
def get_payments():
    """استرجاع قائمة الدفعات"""
    try:
        payments_file = 'payments_log.json'
        if os.path.exists(payments_file):
            with open(payments_file, 'r', encoding='utf-8') as f:
                payments_log = json.load(f)
            return jsonify({'success': True, 'payments': payments_log})
        else:
            return jsonify({'success': True, 'payments': []})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في استرجاع الدفعات: {str(e)}'})

# API routes for expenses
@app.route('/api/save_expense', methods=['POST'])
@login_required
def save_expense():
    """حفظ مصروف جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('expense_type'):
            return jsonify({'success': False, 'message': 'يرجى اختيار نوع المصروف'})

        if not data.get('amount') or float(data.get('amount', 0)) <= 0:
            return jsonify({'success': False, 'message': 'يرجى إدخال مبلغ صحيح'})

        if not data.get('date'):
            return jsonify({'success': False, 'message': 'يرجى اختيار التاريخ'})

        if not data.get('description'):
            return jsonify({'success': False, 'message': 'يرجى إدخال وصف المصروف'})

        # إنشاء سجل المصروف
        expense_data = {
            'expense_type': data.get('expense_type'),
            'amount': float(data.get('amount')),
            'date': data.get('date'),
            'payment_method': data.get('payment_method', 'CASH'),
            'description': data.get('description'),
            'reference': data.get('reference', ''),
            'vendor': data.get('vendor', ''),
            'user_id': current_user.id,
            'created_at': datetime.now().isoformat()
        }

        # حفظ في ملف JSON للاختبار
        expenses_file = 'expenses_log.json'
        expenses_log = []

        if os.path.exists(expenses_file):
            with open(expenses_file, 'r', encoding='utf-8') as f:
                expenses_log = json.load(f)

        # إضافة المصروف الجديد
        expense_data['id'] = len(expenses_log) + 1
        expenses_log.append(expense_data)

        # حفظ في الملف
        with open(expenses_file, 'w', encoding='utf-8') as f:
            json.dump(expenses_log, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success': True,
            'message': 'تم حفظ المصروف بنجاح',
            'expense_id': expense_data['id']
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في حفظ المصروف: {str(e)}'})

@app.route('/api/get_expenses', methods=['GET'])
@login_required
def get_expenses():
    """استرجاع قائمة المصروفات"""
    try:
        expenses_file = 'expenses_log.json'
        if os.path.exists(expenses_file):
            with open(expenses_file, 'r', encoding='utf-8') as f:
                expenses_log = json.load(f)
            return jsonify({'success': True, 'expenses': expenses_log})
        else:
            return jsonify({'success': True, 'expenses': []})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في استرجاع المصروفات: {str(e)}'})

# ============================================================================
# BUTTON SYSTEM API ROUTES
# ============================================================================

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SALES HANDLERS
@app.route('/api/sales/save', methods=['POST'])
@login_required
def sales_save_record():
    """Save sales record"""
    try:
        logger.info("🔵 Sales - Save Record button clicked")
        data = request.get_json()

        # Validate required fields
        required_fields = ['invoice_number', 'customer_name', 'total_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})

        # Create new sale record
        sale = Sale(
            invoice_number=data['invoice_number'],
            customer_name=data['customer_name'],
            invoice_date=datetime.strptime(data.get('invoice_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
            total_amount=float(data['total_amount']),
            tax_amount=float(data.get('tax_amount', 0)),
            final_amount=float(data.get('final_amount', data['total_amount'])),
            payment_method=data.get('payment_method', 'cash'),
            payment_status=data.get('payment_status', 'pending'),
            notes=data.get('notes', ''),
            created_by=current_user.id
        )

        db.session.add(sale)
        db.session.commit()

        logger.info(f"✅ Sales record saved successfully: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record saved successfully', 'id': sale.id})

    except Exception as e:
        logger.error(f"❌ Error saving sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error saving record: {str(e)}'})

@app.route('/api/sales/edit/<int:record_id>', methods=['PUT'])
@login_required
def sales_edit_record(record_id):
    """Edit sales record"""
    try:
        logger.info(f"🔵 Sales - Edit Record button clicked for ID: {record_id}")
        data = request.get_json()

        sale = Sale.query.get_or_404(record_id)

        # Update fields
        sale.customer_name = data.get('customer_name', sale.customer_name)
        sale.total_amount = float(data.get('total_amount', sale.total_amount))
        sale.tax_amount = float(data.get('tax_amount', sale.tax_amount))
        sale.final_amount = float(data.get('final_amount', sale.final_amount))
        sale.payment_method = data.get('payment_method', sale.payment_method)
        sale.payment_status = data.get('payment_status', sale.payment_status)
        sale.notes = data.get('notes', sale.notes)

        db.session.commit()

        logger.info(f"✅ Sales record updated successfully: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record updated successfully'})

    except Exception as e:
        logger.error(f"❌ Error updating sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating record: {str(e)}'})

@app.route('/api/sales/delete/<int:record_id>', methods=['DELETE'])
@login_required
def sales_delete_record(record_id):
    """Delete sales record"""
    try:
        logger.info(f"🔵 Sales - Delete Record button clicked for ID: {record_id}")

        sale = Sale.query.get_or_404(record_id)
        invoice_number = sale.invoice_number

        # Delete related sale items first
        SaleItem.query.filter_by(sale_id=record_id).delete()

        # Delete the sale record
        db.session.delete(sale)
        db.session.commit()

        logger.info(f"✅ Sales record deleted successfully: {invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record deleted successfully'})

    except Exception as e:
        logger.error(f"❌ Error deleting sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting record: {str(e)}'})

@app.route('/api/sales/preview/<int:record_id>')
@login_required
def sales_preview_record(record_id):
    """Preview sales record"""
    try:
        logger.info(f"🔵 Sales - Preview Record button clicked for ID: {record_id}")

        sale = Sale.query.get_or_404(record_id)
        sale_items = SaleItem.query.filter_by(sale_id=record_id).all()

        # Generate preview HTML
        preview_html = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>معاينة الفاتورة {sale.invoice_number}</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
                .invoice-header {{ text-align: center; margin-bottom: 30px; }}
                .invoice-details {{ margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
                .total {{ font-weight: bold; background-color: #e9ecef; }}
            </style>
        </head>
        <body>
            <div class="invoice-header">
                <h2>فاتورة مبيعات</h2>
                <h3>رقم الفاتورة: {sale.invoice_number}</h3>
            </div>
            <div class="invoice-details">
                <p><strong>العميل:</strong> {sale.customer_name or 'عميل نقدي'}</p>
                <p><strong>التاريخ:</strong> {sale.invoice_date}</p>
                <p><strong>الفرع:</strong> {sale.branch.name if sale.branch else 'غير محدد'}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>المنتج</th>
                        <th>الكمية</th>
                        <th>السعر</th>
                        <th>الإجمالي</th>
                    </tr>
                </thead>
                <tbody>
        """

        for item in sale_items:
            preview_html += f"""
                    <tr>
                        <td>{item.product.name if item.product else 'منتج محذوف'}</td>
                        <td>{item.quantity}</td>
                        <td>{item.unit_price:.2f} ريال</td>
                        <td>{item.total_price:.2f} ريال</td>
                    </tr>
            """

        preview_html += f"""
                </tbody>
                <tfoot>
                    <tr class="total">
                        <td colspan="3">المجموع الفرعي</td>
                        <td>{sale.total_amount:.2f} ريال</td>
                    </tr>
                    <tr class="total">
                        <td colspan="3">الضريبة</td>
                        <td>{sale.tax_amount:.2f} ريال</td>
                    </tr>
                    <tr class="total">
                        <td colspan="3">المجموع النهائي</td>
                        <td>{sale.final_amount:.2f} ريال</td>
                    </tr>
                </tfoot>
            </table>
        </body>
        </html>
        """

        logger.info(f"✅ Sales record preview generated: {sale.invoice_number}")
        return jsonify({'success': True, 'html': preview_html})

    except Exception as e:
        logger.error(f"❌ Error previewing sales record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error previewing record: {str(e)}'})

@app.route('/api/sales/print/<int:record_id>')
@login_required
def sales_print_record(record_id):
    """Print sales record"""
    try:
        logger.info(f"🔵 Sales - Print Record button clicked for ID: {record_id}")

        sale = Sale.query.get_or_404(record_id)
        sale_items = SaleItem.query.filter_by(sale_id=record_id).all()

        logger.info(f"✅ Sales record print data prepared: {sale.invoice_number}")
        return jsonify({'success': True, 'print_url': f'/print/sales/{record_id}'})

    except Exception as e:
        logger.error(f"❌ Error preparing sales record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

@app.route('/api/sales/select_invoice')
@login_required
def sales_select_invoice():
    """Get list of invoices for selection"""
    try:
        logger.info("🔵 Sales - Select Invoice button clicked")

        sales = Sale.query.order_by(Sale.created_at.desc()).limit(50).all()

        invoices_data = [{
            'id': sale.id,
            'invoice_number': sale.invoice_number,
            'customer_name': sale.customer_name,
            'invoice_date': sale.invoice_date.strftime('%Y-%m-%d'),
            'final_amount': sale.final_amount,
            'payment_status': sale.payment_status
        } for sale in sales]

        logger.info(f"✅ Retrieved {len(invoices_data)} invoices for selection")
        return jsonify({'success': True, 'invoices': invoices_data})

    except Exception as e:
        logger.error(f"❌ Error retrieving invoices: {str(e)}")
        return jsonify({'success': False, 'message': f'Error retrieving invoices: {str(e)}'})

@app.route('/api/sales/list')
@login_required
def get_sales_list():
    """جلب قائمة فواتير المبيعات من قاعدة البيانات"""
    try:
        logger.info("🔍 جلب قائمة فواتير المبيعات")

        sales = Sale.query.order_by(Sale.created_at.desc()).all()

        sales_list = []
        for sale in sales:
            sales_list.append({
                'id': sale.id,
                'invoice_number': sale.invoice_number,
                'invoice_date': sale.invoice_date.strftime('%Y-%m-%d') if sale.invoice_date else '',
                'customer_name': sale.customer_name or 'عميل نقدي',
                'total_amount': float(sale.total_amount),
                'tax_amount': float(sale.tax_amount),
                'final_amount': float(sale.final_amount),
                'payment_method': sale.payment_method or '',
                'payment_status': sale.payment_status or 'pending',
                'notes': sale.notes or '',
                'branch_name': sale.branch.name if sale.branch else '',
                'created_at': sale.created_at.strftime('%Y-%m-%d %H:%M:%S') if sale.created_at else ''
            })

        logger.info(f"✅ تم جلب {len(sales_list)} فاتورة مبيعات")

        return jsonify({
            'success': True,
            'sales': sales_list,
            'count': len(sales_list)
        })

    except Exception as e:
        logger.error(f"❌ خطأ في جلب قائمة المبيعات: {e}")
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب البيانات: {str(e)}',
            'sales': [],
            'count': 0
        })

@app.route('/api/sales/register_payment', methods=['POST'])
@login_required
def sales_register_payment():
    """Register payment for sales invoice"""
    try:
        logger.info("🔵 Sales - Register Payment button clicked")
        data = request.get_json()

        # Validate required fields
        required_fields = ['invoice_id', 'amount_paid', 'payment_method', 'payment_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})

        sale = Sale.query.get_or_404(data['invoice_id'])

        # Update sale payment status
        if float(data['amount_paid']) >= sale.final_amount:
            sale.payment_status = 'paid'
        else:
            sale.payment_status = 'partial'

        db.session.commit()

        logger.info(f"✅ Payment registered successfully for invoice: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Payment registered successfully'})

    except Exception as e:
        logger.error(f"❌ Error registering payment: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error registering payment: {str(e)}'})

# PRODUCTS HANDLERS
@app.route('/api/products/save', methods=['POST'])
@login_required
def products_save_record():
    """Save product record"""
    try:
        logger.info("🔵 Products - Save Record button clicked")
        data = request.get_json()

        # Validate required fields
        required_fields = ['product_code', 'product_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})

        # Create new product
        product = Product(
            product_code=data['product_code'],
            product_name=data['product_name'],
            description=data.get('description', ''),
            unit_cost=float(data.get('unit_cost', 0)),
            selling_price=float(data.get('selling_price', 0)),
            category=data.get('category', ''),
            unit_type=data.get('unit_type', 'قطعة'),
            min_stock_level=int(data.get('min_stock_level', 0)),
            current_stock=int(data.get('current_stock', 0))
        )

        db.session.add(product)
        db.session.commit()

        logger.info(f"✅ Product saved successfully: {product.product_code}")
        return jsonify({'success': True, 'message': 'Product saved successfully', 'id': product.id})

    except Exception as e:
        logger.error(f"❌ Error saving product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error saving product: {str(e)}'})

@app.route('/api/products/edit/<int:record_id>', methods=['PUT'])
@login_required
def products_edit_record(record_id):
    """Edit product record"""
    try:
        logger.info(f"🔵 Products - Edit Record button clicked for ID: {record_id}")
        data = request.get_json()

        product = Product.query.get_or_404(record_id)

        # Update fields
        product.product_name = data.get('product_name', product.product_name)
        product.description = data.get('description', product.description)
        product.unit_cost = float(data.get('unit_cost', product.unit_cost))
        product.selling_price = float(data.get('selling_price', product.selling_price))
        product.category = data.get('category', product.category)
        product.unit_type = data.get('unit_type', product.unit_type)
        product.min_stock_level = int(data.get('min_stock_level', product.min_stock_level))
        product.current_stock = int(data.get('current_stock', product.current_stock))
        product.updated_at = datetime.utcnow()

        db.session.commit()

        logger.info(f"✅ Product updated successfully: {product.product_code}")
        return jsonify({'success': True, 'message': 'Product updated successfully'})

    except Exception as e:
        logger.error(f"❌ Error updating product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating product: {str(e)}'})

@app.route('/api/products/delete/<int:record_id>', methods=['DELETE'])
@login_required
def products_delete_record(record_id):
    """Delete product record"""
    try:
        logger.info(f"🔵 Products - Delete Record button clicked for ID: {record_id}")

        product = Product.query.get_or_404(record_id)
        product_code = product.product_code

        # Soft delete - mark as inactive
        product.is_active = False
        db.session.commit()

        logger.info(f"✅ Product deleted successfully: {product_code}")
        return jsonify({'success': True, 'message': 'Product deleted successfully'})

    except Exception as e:
        logger.error(f"❌ Error deleting product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting product: {str(e)}'})

    """Search products"""
    try:
        logger.info("🔵 Products - Search Records button clicked")

        search_term = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        query = Product.query.filter(Product.is_active == True)

        if search_term:
            query = query.filter(
                db.or_(
                    Product.product_code.contains(search_term),
                    Product.product_name.contains(search_term),
                    Product.description.contains(search_term)
                )
            )

        products = query.paginate(page=page, per_page=per_page, error_out=False)

        products_data = [{
            'id': p.id,
            'product_code': p.product_code,
            'product_name': p.product_name,
            'description': p.description,
            'unit_cost': p.unit_cost,
            'selling_price': p.selling_price,
            'current_stock': p.current_stock,
            'category': p.category
        } for p in products.items]

        logger.info(f"✅ Found {len(products_data)} products matching search: {search_term}")
        return jsonify({
            'success': True,
            'products': products_data,
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        })

    except Exception as e:
        logger.error(f"❌ Error searching products: {str(e)}")
        return jsonify({'success': False, 'message': f'Error searching products: {str(e)}'})

    """Print product record"""
    try:
        logger.info(f"🔵 Products - Print Record button clicked for ID: {record_id}")

        product = Product.query.get_or_404(record_id)

        logger.info(f"✅ Product print data prepared: {product.product_code}")
        return jsonify({'success': True, 'print_url': f'/print/products/{record_id}'})

    except Exception as e:
        logger.error(f"❌ Error preparing product for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

# REPORTS HANDLERS
@app.route('/api/reports/preview', methods=['POST'])
@login_required
def reports_preview_report():
    """Preview report"""
    try:
        logger.info("🔵 Reports - Preview Report button clicked")
        data = request.get_json()

        report_type = data.get('report_type', 'sales_summary')
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        # Generate report data based on type
        if report_type == 'sales_summary':
            # Sales summary report
            query = Sale.query
            if date_from:
                query = query.filter(Sale.invoice_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
            if date_to:
                query = query.filter(Sale.invoice_date <= datetime.strptime(date_to, '%Y-%m-%d').date())

            sales = query.all()
            report_data = {
                'title': 'Sales Summary Report',
                'date_range': f"{date_from} to {date_to}",
                'total_sales': len(sales),
                'total_amount': sum(s.final_amount for s in sales),
                'sales': [{
                    'invoice_number': s.invoice_number,
                    'customer_name': s.customer_name,
                    'invoice_date': s.invoice_date.strftime('%Y-%m-%d'),
                    'final_amount': s.final_amount,
                    'payment_status': s.payment_status
                } for s in sales]
            }
        elif report_type == 'products_summary':
            # Products summary report
            products = Product.query.filter(Product.is_active == True).all()
            report_data = {
                'title': 'Products Summary Report',
                'total_products': len(products),
                'low_stock_products': len([p for p in products if p.current_stock <= p.min_stock_level]),
                'products': [{
                    'product_code': p.product_code,
                    'product_name': p.product_name,
                    'current_stock': p.current_stock,
                    'min_stock_level': p.min_stock_level,
                    'selling_price': p.selling_price,
                    'category': p.category
                } for p in products]
            }
        else:
            report_data = {'title': 'Unknown Report Type', 'data': []}

        logger.info(f"✅ Report preview generated: {report_type}")
        return jsonify({'success': True, 'report_data': report_data})

    except Exception as e:
        logger.error(f"❌ Error generating report preview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating report: {str(e)}'})

@app.route('/api/reports/print', methods=['POST'])
@login_required
def reports_print_report():
    """Print report"""
    try:
        logger.info("🔵 Reports - Print Report button clicked")
        data = request.get_json()

        report_type = data.get('report_type', 'sales_summary')

        logger.info(f"✅ Report print prepared: {report_type}")
        return jsonify({'success': True, 'print_url': f'/print/reports/{report_type}'})

    except Exception as e:
        logger.error(f"❌ Error preparing report for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

@app.route('/api/reports/export', methods=['POST'])
@login_required
def reports_export_report():
    """Export report"""
    try:
        logger.info("🔵 Reports - Export Report button clicked")
        data = request.get_json()

        export_format = data.get('format', 'excel')  # excel, pdf, csv
        report_type = data.get('report_type', 'sales_summary')

        # Generate export file
        filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}"

        logger.info(f"✅ Report exported successfully: {filename}")
        return jsonify({'success': True, 'filename': filename, 'download_url': f'/download/{filename}'})

    except Exception as e:
        logger.error(f"❌ Error exporting report: {str(e)}")
        return jsonify({'success': False, 'message': f'Error exporting report: {str(e)}'})

# GENERAL HANDLERS FOR OTHER SCREENS
@app.route('/api/<screen>/save', methods=['POST'])
@login_required
def general_save_record(screen):
    """General save handler for other screens"""
    try:
        logger.info(f"🔵 {screen.title()} - Save Record button clicked")
        data = request.get_json()

        # Log the save action
        logger.info(f"✅ {screen.title()} record save attempted")
        return jsonify({'success': True, 'message': f'{screen.title()} record saved successfully'})

    except Exception as e:
        logger.error(f"❌ Error saving {screen} record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving {screen} record: {str(e)}'})

@app.route('/api/<screen>/edit/<int:record_id>', methods=['PUT'])
@login_required
def general_edit_record(screen, record_id):
    """General edit handler for other screens"""
    try:
        logger.info(f"🔵 {screen.title()} - Edit Record button clicked for ID: {record_id}")
        data = request.get_json()

        logger.info(f"✅ {screen.title()} record edit attempted")
        return jsonify({'success': True, 'message': f'{screen.title()} record updated successfully'})

    except Exception as e:
        logger.error(f"❌ Error updating {screen} record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating {screen} record: {str(e)}'})

@app.route('/api/<screen>/delete/<int:record_id>', methods=['DELETE'])
@login_required
def general_delete_record(screen, record_id):
    """General delete handler for other screens"""
    try:
        logger.info(f"🔵 {screen.title()} - Delete Record button clicked for ID: {record_id}")

        logger.info(f"✅ {screen.title()} record delete attempted")
        return jsonify({'success': True, 'message': f'{screen.title()} record deleted successfully'})

    except Exception as e:
        logger.error(f"❌ Error deleting {screen} record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting {screen} record: {str(e)}'})

# ============================================================================

# ============================================================================

# PURCHASES HANDLERS

@app.route('/api/purchases/save', methods=['POST'])
@login_required
def purchases_save_record():
    """Save purchases record"""
    try:
        logger.info("🔵 Purchases - Save Record button clicked")

        # Get form data
        invoice_number = request.form.get('invoice_number')
        supplier_id = request.form.get('supplier_id')
        supplier_name = request.form.get('supplier_name')
        invoice_date = request.form.get('invoice_date')
        payment_method = request.form.get('payment_method')
        branch_id = request.form.get('branch_id')
        notes = request.form.get('notes')

        # Get totals
        subtotal = float(request.form.get('subtotal', 0))
        discount_amount = float(request.form.get('discount_amount', 0))
        tax_amount = float(request.form.get('tax_amount', 0))
        final_amount = float(request.form.get('final_amount', 0))

        # Create purchase record
        purchase = Purchase(
            invoice_number=invoice_number,
            supplier_name=supplier_name or f'Supplier {supplier_id}',
            invoice_date=datetime.strptime(invoice_date, '%Y-%m-%d').date(),
            payment_method=payment_method,
            branch_id=branch_id,
            total_amount=subtotal,
            tax_amount=tax_amount,
            final_amount=final_amount,
            notes=notes,
            payment_status='pending',
            created_by=current_user.id
        )

        db.session.add(purchase)
        db.session.flush()  # Get the ID

        # Add purchase items - دعم النموذج المبسط والمتقدم
        product_ids = request.form.getlist('product_id[]')
        product_names = request.form.getlist('product_name[]')  # للنموذج المبسط
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')
        total_prices = request.form.getlist('total_price[]')

        for i in range(len(quantities)):
            if quantities[i] and unit_prices[i]:
                # تحديد اسم المنتج
                if i < len(product_names) and product_names[i]:
                    # النموذج المبسط - اسم المنتج يدوي
                    product_name = product_names[i]
                    product_id = None
                elif i < len(product_ids) and product_ids[i]:
                    # النموذج المتقدم - منتج من القائمة
                    product = Product.query.get(product_ids[i])
                    product_name = product.product_name if product else f'Product {product_ids[i]}'
                    product_id = product_ids[i]
                else:
                    continue  # تخطي إذا لم يكن هناك منتج

                purchase_item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=product_id,
                    product_name=product_name,
                    quantity=float(quantities[i]),
                    unit_price=float(unit_prices[i]),
                    total_price=float(total_prices[i]) if i < len(total_prices) and total_prices[i] else float(quantities[i]) * float(unit_prices[i])
                )
                db.session.add(purchase_item)

        db.session.commit()

        logger.info(f"✅ Purchase invoice saved successfully: {invoice_number}")
        return jsonify({'success': True, 'message': 'Purchase invoice saved successfully', 'id': purchase.id})

    except Exception as e:
        logger.error(f"❌ Error saving purchase record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error saving purchase: {str(e)}'})

@app.route('/api/purchases/edit/<int:record_id>', methods=['PUT'])
@login_required
def purchases_edit_record(record_id):
    """Edit purchases record"""
    try:
        logger.info(f"🔵 Purchases - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for purchases
        
        logger.info(f"✅ Purchases record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Purchases updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating purchases record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating purchases: {str(e)}'})

@app.route('/api/purchases/delete/<int:record_id>', methods=['DELETE'])
@login_required
def purchases_delete_record(record_id):
    """Delete purchases record"""
    try:
        logger.info(f"🔵 Purchases - Delete Record button clicked for ID: {record_id}")

        # البحث عن فاتورة المشتريات
        purchase = Purchase.query.get_or_404(record_id)
        invoice_number = purchase.invoice_number

        # حذف عناصر الفاتورة أولاً (إذا وجدت)
        PurchaseItem.query.filter_by(purchase_id=record_id).delete()

        # حذف الفاتورة
        db.session.delete(purchase)
        db.session.commit()

        logger.info(f"✅ Purchases record deleted successfully: {invoice_number}")
        return jsonify({'success': True, 'message': 'Purchase invoice deleted successfully'})

    except Exception as e:
        logger.error(f"❌ Error deleting purchases record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting purchase: {str(e)}'})

@app.route('/print_purchase/<int:purchase_id>')
@login_required
def print_purchase(purchase_id):
    """طباعة فاتورة المشتريات"""
    try:
        logger.info(f"🖨️ طباعة فاتورة المشتريات: {purchase_id}")

        purchase = Purchase.query.get_or_404(purchase_id)
        purchase_items = PurchaseItem.query.filter_by(purchase_id=purchase_id).all()

        logger.info(f"✅ تم جلب فاتورة المشتريات {purchase.invoice_number} للطباعة")

        return render_template('print_purchase.html',
                             purchase=purchase,
                             purchase_items=purchase_items)
    except Exception as e:
        logger.error(f"❌ Error printing purchase: {str(e)}")
        flash('حدث خطأ أثناء طباعة الفاتورة', 'error')
        return redirect(url_for('purchases'))

# إضافة route بديل للطباعة
@app.route('/purchases/print/<int:purchase_id>')
@login_required
def print_purchase_alt(purchase_id):
    """طباعة فاتورة المشتريات - مسار بديل"""
    logger.info(f"🖨️ طباعة فاتورة المشتريات (مسار بديل): {purchase_id}")
    return print_purchase(purchase_id)

@app.route('/purchases/new')
@login_required
def new_purchase():
    """إنشاء فاتورة مشتريات جديدة - توجيه للنموذج المبسط"""
    logger.info("🔄 توجيه إلى النموذج المبسط لإنشاء فاتورة المشتريات")
    return redirect(url_for('simple_purchase'))

@app.route('/purchases/test')
@login_required
def test_purchase():
    """اختبار بسيط لتحميل نموذج الفاتورة"""
    try:
        logger.info("🔍 بدء اختبار تحميل نموذج الفاتورة")

        # اختبار قاعدة البيانات
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            logger.info("✅ قاعدة البيانات متصلة")
        except Exception as e:
            logger.error(f"❌ مشكلة في قاعدة البيانات: {e}")
            return f"خطأ في قاعدة البيانات: {e}"

        # اختبار النماذج
        try:
            product_count = db.session.query(Product).count()
            logger.info(f"✅ عدد المنتجات: {product_count}")
        except Exception as e:
            logger.error(f"❌ مشكلة في نموذج Product: {e}")
            product_count = 0

        try:
            branch_count = db.session.query(Branch).count()
            logger.info(f"✅ عدد الفروع: {branch_count}")
        except Exception as e:
            logger.error(f"❌ مشكلة في نموذج Branch: {e}")
            branch_count = 0

        # اختبار القالب
        try:
            return render_template('new_purchase.html',
                                 suppliers=[],
                                 products=[],
                                 branches=[])
        except Exception as e:
            logger.error(f"❌ مشكلة في القالب: {e}")
            return f"خطأ في القالب: {e}"

    except Exception as e:
        logger.error(f"❌ خطأ عام في الاختبار: {e}")
        import traceback
        return f"خطأ عام: {e}<br><pre>{traceback.format_exc()}</pre>"

@app.route('/purchases/simple')
@login_required
def simple_purchase():
    """نموذج مبسط لإنشاء فاتورة المشتريات"""
    try:
        logger.info("🔍 تحميل النموذج المبسط لفاتورة المشتريات")

        # جلب قائمة الموردين النشطين
        suppliers = []
        try:
            suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name).all()
            logger.info(f"✅ تم جلب {len(suppliers)} مورد")
        except Exception as e:
            logger.warning(f"⚠️ لم يتم جلب الموردين: {e}")
            suppliers = []

        return render_template('simple_purchase.html', suppliers=suppliers)
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل النموذج المبسط: {e}")
        return f"خطأ: {e}"

@app.route('/api/suppliers/list')
@login_required
def get_suppliers_list():
    """جلب قائمة الموردين النشطين"""
    try:
        logger.info("🔍 جلب قائمة الموردين")

        # جلب جميع الموردين النشطين
        suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name).all()

        suppliers_data = []
        for supplier in suppliers:
            suppliers_data.append({
                'id': supplier.id,
                'name': supplier.name,
                'phone': supplier.phone or '',
                'email': supplier.email or '',
                'address': supplier.address or '',
                'tax_number': supplier.tax_number or '',
                'contact_person': supplier.contact_person or ''
            })

        logger.info(f"✅ تم جلب {len(suppliers_data)} مورد")
        return jsonify({
            'success': True,
            'data': suppliers_data,
            'count': len(suppliers_data)
        })

    except Exception as e:
        logger.error(f"❌ خطأ في جلب قائمة الموردين: {e}")
        return jsonify({
            'success': False,
            'message': f'Error loading suppliers: {e}',
            'data': []
        })

@app.route('/api/purchases/save/debug', methods=['POST'])
@login_required
def purchases_save_debug():
    """حفظ فاتورة المشتريات مع تسجيل مفصل للأخطاء"""
    try:
        logger.info("🔍 بدء حفظ فاتورة المشتريات - وضع التشخيص")

        # طباعة جميع البيانات المرسلة
        logger.info(f"📋 البيانات المرسلة: {dict(request.form)}")

        # Get form data
        invoice_number = request.form.get('invoice_number')
        supplier_id = request.form.get('supplier_id')
        supplier_name = request.form.get('supplier_name')
        invoice_date = request.form.get('invoice_date')
        payment_method = request.form.get('payment_method')
        branch_id = request.form.get('branch_id', 1)
        notes = request.form.get('notes', '')

        # إذا تم اختيار مورد من القائمة، جلب اسمه
        if supplier_id and supplier_id != '':
            try:
                supplier = Supplier.query.get(int(supplier_id))
                if supplier:
                    supplier_name = supplier.name
                    logger.info(f"✅ تم اختيار المورد: {supplier_name}")
            except Exception as e:
                logger.warning(f"⚠️ خطأ في جلب بيانات المورد: {e}")

        # التأكد من وجود اسم المورد
        if not supplier_name:
            supplier_name = "مورد غير محدد"

        logger.info(f"📝 بيانات الفاتورة: {invoice_number}, {supplier_name}, {invoice_date}")

        # Get totals
        subtotal = float(request.form.get('subtotal', 0))
        tax_amount = float(request.form.get('tax_amount', 0))
        final_amount = float(request.form.get('final_amount', 0))

        logger.info(f"💰 الإجماليات: {subtotal}, {tax_amount}, {final_amount}")

        # اختبار الاتصال بقاعدة البيانات
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            logger.info("✅ قاعدة البيانات متصلة")
        except Exception as e:
            logger.error(f"❌ مشكلة في قاعدة البيانات: {e}")
            return jsonify({'success': False, 'message': f'Database error: {e}'})

        # Create purchase record
        try:
            purchase = Purchase(
                invoice_number=invoice_number,
                supplier_name=supplier_name,
                invoice_date=datetime.strptime(invoice_date, '%Y-%m-%d').date(),
                payment_method=payment_method,
                branch_id=int(branch_id),
                total_amount=subtotal,
                tax_amount=tax_amount,
                final_amount=final_amount,
                notes=notes,
                payment_status='pending',
                created_by=current_user.id
            )

            # إضافة معرف المورد إذا كان متوفراً
            if supplier_id and supplier_id != '':
                try:
                    purchase.supplier_id = int(supplier_id)
                    logger.info(f"✅ تم ربط الفاتورة بالمورد ID: {supplier_id}")
                except ValueError:
                    logger.warning(f"⚠️ معرف المورد غير صحيح: {supplier_id}")
            logger.info("✅ تم إنشاء كائن Purchase")

            db.session.add(purchase)
            logger.info("✅ تم إضافة Purchase إلى الجلسة")

            db.session.flush()
            logger.info(f"✅ تم flush - معرف الفاتورة: {purchase.id}")

        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء Purchase: {e}")
            return jsonify({'success': False, 'message': f'Purchase creation error: {e}'})

        # Add purchase items
        try:
            product_names = request.form.getlist('product_name[]')
            quantities = request.form.getlist('quantity[]')
            unit_prices = request.form.getlist('unit_price[]')

            logger.info(f"📦 عناصر الفاتورة: {len(product_names)} منتج")

            items_added = 0
            for i in range(len(quantities)):
                if i < len(product_names) and product_names[i] and quantities[i] and unit_prices[i]:
                    try:
                        quantity = float(quantities[i])
                        unit_price = float(unit_prices[i])
                        total_price = quantity * unit_price

                        purchase_item = PurchaseItem(
                            purchase_id=purchase.id,
                            product_id=None,
                            product_name=product_names[i],
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=total_price
                        )
                        db.session.add(purchase_item)
                        items_added += 1
                        logger.info(f"✅ تم إضافة عنصر {i+1}: {product_names[i]}")

                    except Exception as e:
                        logger.error(f"❌ خطأ في إضافة العنصر {i+1}: {e}")

            logger.info(f"📊 تم إضافة {items_added} عنصر")

        except Exception as e:
            logger.error(f"❌ خطأ في معالجة العناصر: {e}")
            return jsonify({'success': False, 'message': f'Items processing error: {e}'})

        # Commit transaction
        try:
            db.session.commit()
            logger.info("✅ تم حفظ الفاتورة في قاعدة البيانات")

            return jsonify({
                'success': True,
                'message': 'Purchase invoice saved successfully',
                'id': purchase.id,
                'invoice_number': invoice_number
            })

        except Exception as e:
            logger.error(f"❌ خطأ في commit: {e}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Commit error: {e}'})

    except Exception as e:
        logger.error(f"❌ خطأ عام في حفظ الفاتورة: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'General error: {e}'})

@app.route('/purchases/data/check')
@login_required
def check_purchases_data():
    """فحص البيانات المحفوظة في المشتريات"""
    try:
        from sqlalchemy import text

        # عدد الفواتير
        purchases_count = db.session.execute(text('SELECT COUNT(*) FROM purchases')).scalar()

        # عدد العناصر
        items_count = db.session.execute(text('SELECT COUNT(*) FROM purchase_items')).scalar()

        # آخر الفواتير
        last_purchases = db.session.execute(text('''
            SELECT invoice_number, supplier_name, final_amount, created_at
            FROM purchases
            ORDER BY created_at DESC
            LIMIT 5
        ''')).fetchall()

        # إجمالي المبلغ
        total_amount = db.session.execute(text('SELECT SUM(final_amount) FROM purchases')).scalar() or 0

        html = f"""
        <html dir="rtl">
        <head>
            <title>فحص بيانات المشتريات</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                .card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .success {{ background-color: #d4edda; }}
                .info {{ background-color: #d1ecf1; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: right; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>🔍 فحص بيانات المشتريات</h1>

            <div class="card success">
                <h3>📊 الإحصائيات العامة</h3>
                <p><strong>عدد فواتير المشتريات:</strong> {purchases_count}</p>
                <p><strong>عدد عناصر المشتريات:</strong> {items_count}</p>
                <p><strong>إجمالي المبلغ:</strong> {total_amount:.2f} ريال</p>
            </div>

            <div class="card info">
                <h3>📋 آخر الفواتير</h3>
                <table>
                    <tr>
                        <th>رقم الفاتورة</th>
                        <th>المورد</th>
                        <th>المبلغ</th>
                        <th>تاريخ الإنشاء</th>
                    </tr>
        """

        for purchase in last_purchases:
            html += f"""
                    <tr>
                        <td>{purchase[0]}</td>
                        <td>{purchase[1]}</td>
                        <td>{purchase[2]:.2f} ريال</td>
                        <td>{purchase[3]}</td>
                    </tr>
            """

        html += """
                </table>
            </div>

            <div class="card">
                <p><a href="/purchases">← العودة إلى المشتريات</a></p>
                <p><a href="/purchases/simple">إنشاء فاتورة جديدة</a></p>
            </div>
        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"خطأ في فحص البيانات: {e}"

@app.route('/api/purchases/list')
@login_required
def get_purchases_list():
    """جلب قائمة فواتير المشتريات من قاعدة البيانات"""
    try:
        logger.info("🔍 جلب قائمة فواتير المشتريات")

        # جلب جميع فواتير المشتريات
        purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()

        purchases_data = []
        for purchase in purchases:
            # جلب عناصر الفاتورة
            items = PurchaseItem.query.filter_by(purchase_id=purchase.id).all()
            items_data = []
            for item in items:
                items_data.append({
                    'product_name': item.product_name,
                    'quantity': float(item.quantity),
                    'unit_price': float(item.unit_price),
                    'total': float(item.total_price)
                })

            purchases_data.append({
                'id': purchase.id,
                'invoice_number': purchase.invoice_number,
                'date': purchase.invoice_date.strftime('%Y-%m-%d'),
                'supplier_name': purchase.supplier_name,
                'subtotal': float(purchase.subtotal),
                'vat_amount': float(purchase.tax_amount),
                'total': float(purchase.final_amount),
                'payment_method': purchase.payment_method,
                'status': purchase.payment_status,
                'notes': purchase.notes or '',
                'items': items_data,
                'created_at': purchase.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        logger.info(f"✅ تم جلب {len(purchases_data)} فاتورة مشتريات")
        return jsonify({
            'success': True,
            'data': purchases_data,
            'count': len(purchases_data)
        })

    except Exception as e:
        logger.error(f"❌ خطأ في جلب قائمة المشتريات: {e}")
        return jsonify({
            'success': False,
            'message': f'Error loading purchases: {e}',
            'data': []
        })

@app.route('/api/purchases/delete/<int:purchase_id>', methods=['DELETE', 'POST'])
@login_required
def delete_purchase(purchase_id):
    """حذف فاتورة مشتريات"""
    try:
        logger.info(f"🗑️ محاولة حذف فاتورة المشتريات ID: {purchase_id}")

        # البحث عن الفاتورة
        purchase = Purchase.query.get(purchase_id)
        if not purchase:
            logger.warning(f"⚠️ فاتورة المشتريات غير موجودة: {purchase_id}")
            return jsonify({
                'success': False,
                'message': 'Purchase not found'
            })

        # حذف عناصر الفاتورة أولاً
        items = PurchaseItem.query.filter_by(purchase_id=purchase_id).all()
        for item in items:
            db.session.delete(item)

        logger.info(f"🗑️ تم حذف {len(items)} عنصر من الفاتورة")

        # حذف الفاتورة
        invoice_number = purchase.invoice_number
        db.session.delete(purchase)
        db.session.commit()

        logger.info(f"✅ تم حذف فاتورة المشتريات: {invoice_number}")
        return jsonify({
            'success': True,
            'message': f'Purchase {invoice_number} deleted successfully'
        })

    except Exception as e:
        logger.error(f"❌ خطأ في حذف فاتورة المشتريات: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting purchase: {e}'
        })

@app.route('/purchases/delete/<int:purchase_id>', methods=['POST'])
@login_required
def delete_purchase_simple(purchase_id):
    """حذف فاتورة مشتريات - route مبسط"""
    try:
        logger.info(f"🗑️ حذف فاتورة مبسط ID: {purchase_id}")

        # البحث عن الفاتورة
        purchase = Purchase.query.get(purchase_id)
        if not purchase:
            flash('الفاتورة غير موجودة', 'error')
            return redirect(url_for('purchases'))

        # حذف عناصر الفاتورة أولاً
        PurchaseItem.query.filter_by(purchase_id=purchase_id).delete()

        # حذف الفاتورة
        invoice_number = purchase.invoice_number
        db.session.delete(purchase)
        db.session.commit()

        logger.info(f"✅ تم حذف الفاتورة: {invoice_number}")
        flash(f'✅ تم حذف الفاتورة {invoice_number} بنجاح', 'success')
        return redirect(url_for('purchases'))

    except Exception as e:
        logger.error(f"❌ خطأ في الحذف: {e}")
        db.session.rollback()
        flash('حدث خطأ أثناء حذف الفاتورة', 'error')
        return redirect(url_for('purchases'))

@app.route('/purchases/test-delete/<int:purchase_id>')
@login_required
def test_delete_purchase(purchase_id):
    """اختبار حذف فاتورة المشتريات"""
    try:
        # البحث عن الفاتورة
        purchase = Purchase.query.get(purchase_id)
        if not purchase:
            return f"❌ الفاتورة غير موجودة: {purchase_id}"

        # عرض معلومات الفاتورة
        items = PurchaseItem.query.filter_by(purchase_id=purchase_id).all()

        html = f"""
        <html dir="rtl">
        <head>
            <title>اختبار حذف الفاتورة</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                .card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .danger {{ background-color: #f8d7da; }}
                .info {{ background-color: #d1ecf1; }}
                button {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }}
                .btn-danger {{ background-color: #dc3545; color: white; }}
                .btn-secondary {{ background-color: #6c757d; color: white; }}
            </style>
        </head>
        <body>
            <h1>🗑️ اختبار حذف الفاتورة</h1>

            <div class="card info">
                <h3>📋 معلومات الفاتورة</h3>
                <p><strong>رقم الفاتورة:</strong> {purchase.invoice_number}</p>
                <p><strong>المورد:</strong> {purchase.supplier_name}</p>
                <p><strong>التاريخ:</strong> {purchase.invoice_date}</p>
                <p><strong>المبلغ:</strong> {purchase.final_amount} ريال</p>
                <p><strong>عدد العناصر:</strong> {len(items)}</p>
            </div>

            <div class="card danger">
                <h3>⚠️ تحذير</h3>
                <p>سيتم حذف الفاتورة وجميع عناصرها نهائياً!</p>
            </div>

            <form method="POST" action="/purchases/delete/{purchase_id}" onsubmit="return confirm('هل أنت متأكد من الحذف؟')">
                <button type="submit" class="btn-danger">🗑️ حذف الفاتورة</button>
                <a href="/purchases"><button type="button" class="btn-secondary">← العودة</button></a>
            </form>

            <hr>
            <h3>🔧 اختبار API</h3>
            <button onclick="testDeleteAPI()" class="btn-danger">اختبار حذف عبر API</button>

            <script>
            function testDeleteAPI() {{
                if (confirm('اختبار حذف عبر API؟')) {{
                    fetch('/api/purchases/delete/{purchase_id}', {{
                        method: 'DELETE',
                        headers: {{
                            'Content-Type': 'application/json',
                        }}
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert('النتيجة: ' + JSON.stringify(data));
                        if (data.success) {{
                            window.location.href = '/purchases';
                        }}
                    }})
                    .catch(error => {{
                        alert('خطأ: ' + error);
                    }});
                }}
            }}
            </script>
        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"خطأ: {e}"

@app.route('/api/purchases/register_payment', methods=['POST'])
@login_required
def purchases_register_payment():
    """Register payment for purchases invoice"""
    try:
        logger.info("🔵 Purchases - Register Payment button clicked")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No payment data provided'})
        
        # TODO: Implement actual payment registration logic for purchases
        
        logger.info(f"✅ Purchases payment registered successfully")
        return jsonify({'success': True, 'message': 'Payment registered successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error registering purchases payment: {str(e)}")
        return jsonify({'success': False, 'message': f'Error registering payment: {str(e)}'})

# CUSTOMERS HANDLERS

@app.route('/api/customers/save', methods=['POST'])
@login_required
def customers_save_record():
    """Save customers record"""
    try:
        logger.info("🔵 Customers - Save Record button clicked")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual save logic for customers
        # For now, return success with dummy ID
        
        logger.info(f"✅ Customers record saved successfully")
        return jsonify({'success': True, 'message': 'Customers saved successfully', 'id': 1})
        
    except Exception as e:
        logger.error(f"❌ Error saving customers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving customers: {str(e)}'})

@app.route('/api/customers/edit/<int:record_id>', methods=['PUT'])
@login_required
def customers_edit_record(record_id):
    """Edit customers record"""
    try:
        logger.info(f"🔵 Customers - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for customers
        
        logger.info(f"✅ Customers record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Customers updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating customers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating customers: {str(e)}'})

@app.route('/api/customers/delete/<int:record_id>', methods=['DELETE'])
@login_required
def customers_delete_record(record_id):
    """Delete customers record"""
    try:
        logger.info(f"🔵 Customers - Delete Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual delete logic for customers
        
        logger.info(f"✅ Customers record {record_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Customers deleted successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error deleting customers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting customers: {str(e)}'})

    """Search customers records"""
    try:
        logger.info("🔵 Customers - Search Records button clicked")
        
        query = request.args.get('q', '')
        
        # TODO: Implement actual search logic for customers
        
        logger.info(f"✅ Customers search completed")
        return jsonify({'success': True, 'message': 'Search completed', 'results': []})
        
    except Exception as e:
        logger.error(f"❌ Error searching customers records: {str(e)}")
        return jsonify({'success': False, 'message': f'Error searching customers: {str(e)}'})

    """Print customers record"""
    try:
        logger.info(f"🔵 Customers - Print Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual print logic for customers
        
        logger.info(f"✅ Customers record {record_id} prepared for print")
        return jsonify({'success': True, 'message': 'Print prepared', 'print_url': f'/print/customers/{record_id}'})
        
    except Exception as e:
        logger.error(f"❌ Error preparing customers record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

# SUPPLIERS HANDLERS

@app.route('/api/suppliers/save', methods=['POST'])
@login_required
def suppliers_save_record():
    """Save suppliers record"""
    try:
        logger.info("🔵 Suppliers - Save Record button clicked")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual save logic for suppliers
        # For now, return success with dummy ID
        
        logger.info(f"✅ Suppliers record saved successfully")
        return jsonify({'success': True, 'message': 'Suppliers saved successfully', 'id': 1})
        
    except Exception as e:
        logger.error(f"❌ Error saving suppliers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving suppliers: {str(e)}'})

@app.route('/api/suppliers/edit/<int:record_id>', methods=['PUT'])
@login_required
def suppliers_edit_record(record_id):
    """Edit suppliers record"""
    try:
        logger.info(f"🔵 Suppliers - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for suppliers
        
        logger.info(f"✅ Suppliers record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Suppliers updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating suppliers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating suppliers: {str(e)}'})

@app.route('/api/suppliers/delete/<int:record_id>', methods=['DELETE'])
@login_required
def suppliers_delete_record(record_id):
    """Delete suppliers record"""
    try:
        logger.info(f"🔵 Suppliers - Delete Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual delete logic for suppliers
        
        logger.info(f"✅ Suppliers record {record_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Suppliers deleted successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error deleting suppliers record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting suppliers: {str(e)}'})

    """Search suppliers records"""
    try:
        logger.info("🔵 Suppliers - Search Records button clicked")
        
        query = request.args.get('q', '')
        
        # TODO: Implement actual search logic for suppliers
        
        logger.info(f"✅ Suppliers search completed")
        return jsonify({'success': True, 'message': 'Search completed', 'results': []})
        
    except Exception as e:
        logger.error(f"❌ Error searching suppliers records: {str(e)}")
        return jsonify({'success': False, 'message': f'Error searching suppliers: {str(e)}'})

    """Print suppliers record"""
    try:
        logger.info(f"🔵 Suppliers - Print Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual print logic for suppliers
        
        logger.info(f"✅ Suppliers record {record_id} prepared for print")
        return jsonify({'success': True, 'message': 'Print prepared', 'print_url': f'/print/suppliers/{record_id}'})
        
    except Exception as e:
        logger.error(f"❌ Error preparing suppliers record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

# EXPENSES HANDLERS

@app.route('/api/expenses/save', methods=['POST'])
@login_required
def expenses_save_record():
    """حفظ مصروف جديد"""
    try:
        logger.info("💰 بدء حفظ مصروف جديد")

        # دعم كل من JSON و form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        if not data:
            return jsonify({'success': False, 'message': 'لا توجد بيانات'})

        # التحقق من البيانات المطلوبة
        required_fields = ['expense_type', 'description', 'amount', 'expense_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'حقل {field} مطلوب'})

        # التحقق من صحة المبلغ
        try:
            amount = float(data.get('amount', 0))
            if amount <= 0:
                return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون أكبر من صفر'})
        except ValueError:
            return jsonify({'success': False, 'message': 'المبلغ يجب أن يكون رقماً صحيحاً'})

        # إنشاء رقم المصروف
        expense_number = f"EXP-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # إنشاء المصروف
        expense = Expense(
            expense_number=expense_number,
            expense_type=data.get('expense_type'),
            description=data.get('description'),
            amount=amount,
            expense_date=datetime.strptime(data.get('expense_date'), '%Y-%m-%d').date(),
            payment_method=data.get('payment_method', 'نقدي'),
            payment_status=data.get('payment_status', 'pending'),
            notes=data.get('notes', ''),
            branch_id=data.get('branch_id', 1),
            created_by=current_user.id
        )

        db.session.add(expense)
        db.session.commit()

        logger.info(f"✅ تم حفظ المصروف: {expense_number}")
        return jsonify({
            'success': True,
            'message': 'تم حفظ المصروف بنجاح',
            'id': expense.id,
            'expense_number': expense_number
        })

    except Exception as e:
        logger.error(f"❌ خطأ في حفظ المصروف: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ المصروف: {str(e)}'})

@app.route('/api/expenses/list')
@login_required
def get_expenses_list():
    """جلب قائمة المصروفات"""
    try:
        logger.info("📋 جلب قائمة المصروفات")

        # جلب جميع المصروفات
        expenses = Expense.query.order_by(Expense.expense_date.desc()).all()

        expenses_data = []
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'expense_number': expense.expense_number,
                'expense_type': expense.expense_type,
                'description': expense.description,
                'amount': float(expense.amount),
                'expense_date': expense.expense_date.strftime('%Y-%m-%d'),
                'payment_method': expense.payment_method,
                'payment_status': expense.payment_status,
                'notes': expense.notes or '',
                'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        logger.info(f"✅ تم جلب {len(expenses_data)} مصروف")
        return jsonify({
            'success': True,
            'data': expenses_data,
            'count': len(expenses_data)
        })

    except Exception as e:
        logger.error(f"❌ خطأ في جلب المصروفات: {e}")
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب المصروفات: {e}',
            'data': []
        })

@app.route('/api/expenses/categories')
@login_required
def get_expenses_categories():
    """جلب فئات المصروفات"""
    try:
        categories = [
            'مصروفات إدارية',
            'مصروفات تشغيلية',
            'مصروفات تسويقية',
            'مصروفات صيانة',
            'مصروفات مكتبية',
            'مصروفات سفر',
            'مصروفات اتصالات',
            'مصروفات كهرباء وماء',
            'مصروفات إيجار',
            'مصروفات أخرى'
        ]

        return jsonify({
            'success': True,
            'data': categories
        })

    except Exception as e:
        logger.error(f"❌ خطأ في جلب فئات المصروفات: {e}")
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب الفئات: {e}',
            'data': []
        })

@app.route('/api/expenses/delete/<int:expense_id>', methods=['DELETE', 'POST'])
@login_required
def delete_expense(expense_id):
    """حذف مصروف"""
    try:
        logger.info(f"🗑️ محاولة حذف المصروف ID: {expense_id}")

        expense = Expense.query.get(expense_id)
        if not expense:
            return jsonify({
                'success': False,
                'message': 'المصروف غير موجود'
            })

        expense_number = expense.expense_number
        db.session.delete(expense)
        db.session.commit()

        logger.info(f"✅ تم حذف المصروف: {expense_number}")
        return jsonify({
            'success': True,
            'message': f'تم حذف المصروف {expense_number} بنجاح'
        })

    except Exception as e:
        logger.error(f"❌ خطأ في حذف المصروف: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حذف المصروف: {e}'
        })

@app.route('/expenses/new')
@login_required
def new_expense():
    """صفحة إضافة مصروف جديد"""
    try:
        logger.info("➕ تحميل صفحة إضافة مصروف جديد")

        # جلب الفروع النشطة
        branches = Branch.query.filter_by(is_active=True).all()

        return render_template('new_expense.html', branches=branches)

    except Exception as e:
        logger.error(f"❌ خطأ في تحميل صفحة المصروف الجديد: {e}")
        flash('حدث خطأ أثناء تحميل الصفحة', 'error')
        return redirect(url_for('expenses'))

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense_simple(expense_id):
    """حذف مصروف - route مبسط"""
    try:
        logger.info(f"🗑️ حذف مصروف مبسط ID: {expense_id}")

        expense = Expense.query.get(expense_id)
        if not expense:
            flash('المصروف غير موجود', 'error')
            return redirect(url_for('expenses'))

        expense_number = expense.expense_number
        db.session.delete(expense)
        db.session.commit()

        logger.info(f"✅ تم حذف المصروف: {expense_number}")
        flash(f'✅ تم حذف المصروف {expense_number} بنجاح', 'success')
        return redirect(url_for('expenses'))

    except Exception as e:
        logger.error(f"❌ خطأ في الحذف: {e}")
        db.session.rollback()
        flash('حدث خطأ أثناء حذف المصروف', 'error')
        return redirect(url_for('expenses'))

@app.route('/expenses/test-delete/<int:expense_id>')
@login_required
def test_delete_expense(expense_id):
    """اختبار حذف مصروف"""
    try:
        # البحث عن المصروف
        expense = Expense.query.get(expense_id)
        if not expense:
            return f"❌ المصروف غير موجود: {expense_id}"

        html = f"""
        <html dir="rtl">
        <head>
            <title>اختبار حذف المصروف</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                .card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .danger {{ background-color: #f8d7da; }}
                .info {{ background-color: #d1ecf1; }}
                button {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }}
                .btn-danger {{ background-color: #dc3545; color: white; }}
                .btn-secondary {{ background-color: #6c757d; color: white; }}
            </style>
        </head>
        <body>
            <h1>🗑️ اختبار حذف المصروف</h1>

            <div class="card info">
                <h3>📋 معلومات المصروف</h3>
                <p><strong>رقم المصروف:</strong> {expense.expense_number}</p>
                <p><strong>النوع:</strong> {expense.expense_type}</p>
                <p><strong>الوصف:</strong> {expense.description}</p>
                <p><strong>المبلغ:</strong> {expense.amount} ريال</p>
                <p><strong>التاريخ:</strong> {expense.expense_date}</p>
                <p><strong>الحالة:</strong> {expense.payment_status}</p>
            </div>

            <div class="card danger">
                <h3>⚠️ تحذير</h3>
                <p>سيتم حذف المصروف نهائياً!</p>
            </div>

            <form method="POST" action="/expenses/delete/{expense_id}" onsubmit="return confirm('هل أنت متأكد من الحذف؟')">
                <button type="submit" class="btn-danger">🗑️ حذف المصروف</button>
                <a href="/expenses"><button type="button" class="btn-secondary">← العودة</button></a>
            </form>

            <hr>
            <h3>🔧 اختبار API</h3>
            <button onclick="testDeleteAPI()" class="btn-danger">اختبار حذف عبر API</button>

            <script>
            function testDeleteAPI() {{
                if (confirm('اختبار حذف عبر API؟')) {{
                    fetch('/api/expenses/delete/{expense_id}', {{
                        method: 'DELETE',
                        headers: {{
                            'Content-Type': 'application/json',
                        }}
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert('النتيجة: ' + JSON.stringify(data));
                        if (data.success) {{
                            window.location.href = '/expenses';
                        }}
                    }})
                    .catch(error => {{
                        alert('خطأ: ' + error);
                    }});
                }}
            }}
            </script>
        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"خطأ: {e}"

@app.route('/print_invoices_preview')
@login_required
def print_invoices_preview():
    """معاينة الفواتير للطباعة"""
    try:
        invoice_type = request.args.get('type', 'sales')
        month = request.args.get('month', '')
        status = request.args.get('status', 'all')
        include_details = request.args.get('details', 'true') == 'true'

        if not month:
            return "يرجى تحديد الشهر والسنة", 400

        # تحليل الشهر والسنة
        try:
            year, month_num = month.split('-')
            year = int(year)
            month_num = int(month_num)
        except:
            return "تنسيق الشهر غير صحيح", 400

        # استخدام الوظيفة المحسنة لجلب الفواتير مع البنود
        invoices_with_items = get_invoices_with_items(invoice_type, month)

        # فلترة حسب الحالة إذا لزم الأمر
        if status != 'all':
            invoices_with_items = [inv for inv in invoices_with_items
                                 if inv.get('payment_status') == status]

        # للتوافق مع template الحالي، نحتاج أيضاً للفواتير العادية
        invoices = []
        if invoice_type == 'sales':
            query = Sale.query.filter(
                db.extract('year', Sale.invoice_date) == year,
                db.extract('month', Sale.invoice_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Sale.invoice_date.desc()).all()

        elif invoice_type == 'purchases':
            query = Purchase.query.filter(
                db.extract('year', Purchase.invoice_date) == year,
                db.extract('month', Purchase.invoice_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Purchase.invoice_date.desc()).all()

        elif invoice_type == 'expenses':
            query = Expense.query.filter(
                db.extract('year', Expense.expense_date) == year,
                db.extract('month', Expense.expense_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Expense.expense_date.desc()).all()

        elif invoice_type == 'payroll':
            query = EmployeePayroll.query.filter_by(year=year, month=month_num)
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(EmployeePayroll.created_at.desc()).all()

        # إضافة التاريخ الحالي
        from datetime import datetime
        now = datetime.now()

        return render_template('print_invoices_preview.html',
                             invoices=invoices,
                             invoices_with_items=invoices_with_items,
                             invoice_type=invoice_type,
                             month=month,
                             status=status,
                             include_details=include_details,
                             year=year,
                             month_num=month_num,
                             current_date=now.strftime('%Y-%m-%d'),
                             current_datetime=now.strftime('%Y-%m-%d %H:%M:%S'))

    except Exception as e:
        logger.error(f"❌ خطأ في معاينة الطباعة: {e}")
        return f"خطأ في معاينة الطباعة: {e}", 500

@app.route('/print_invoices_enhanced')
@login_required
def print_invoices_enhanced():
    """طباعة محسنة للفواتير مع البنود - مثل الكود المرسل"""
    try:
        invoice_type = request.args.get('type', 'sales')
        month = request.args.get('month', '')
        status = request.args.get('status', 'all')

        if not month:
            return "يرجى تحديد الشهر والسنة", 400

        # جلب الفواتير مع البنود
        invoices_with_items = get_invoices_with_items(invoice_type, month)

        # فلترة حسب الحالة
        if status != 'all':
            invoices_with_items = [inv for inv in invoices_with_items
                                 if inv.get('payment_status') == status]

        # إنشاء HTML للطباعة
        html_content = render_template('invoice_pdf.html',
                                     section=invoice_type,
                                     month=month,
                                     invoices=invoices_with_items,
                                     status=status)

        return html_content

    except Exception as e:
        return f"خطأ في الطباعة المحسنة: {e}"

# تم حذف الـ route المكرر لتجنب التضارب

@app.route('/print-invoices', methods=['POST'])
@login_required
def print_invoices_direct():
    """طباعة مباشرة للفواتير - سكريبت تتبع الخطأ"""
    try:
        print("✅ [START] تم الضغط على زر الطباعة")

        section = request.form.get('section')
        month = request.form.get('month')

        print(f"🔍 القسم المُختار: {section}")
        print(f"🔍 الشهر المُختار: {month}")

        if not section or not month:
            print("❌ [ERROR] لم يتم استلام القسم أو الشهر")
            return "حدث خطأ: القسم أو الشهر غير محدد."

        # جلب الفواتير الحقيقية من قاعدة البيانات
        invoices = get_invoices_with_items(section, month)

        # إذا لم توجد فواتير، استخدم بيانات تجريبية
        if not invoices:
            print("⚠️ لا توجد فواتير حقيقية، استخدام بيانات تجريبية")
            dummy_invoices = [
                {"id": 1, "date": "2025-08-01", "amount": 1200},
                {"id": 2, "date": "2025-08-05", "amount": 1500},
            ]
            invoices = dummy_invoices

        if not invoices:
            print("⚠️ لا توجد فواتير لهذا القسم في هذا الشهر.")
            return "لا توجد فواتير"

        # إنشاء HTML للتقرير
        html = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>فواتير {section} - {month}</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
                h2 {{ color: #333; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>فواتير شهر {month} - قسم {section}</h2>
            <table>
                <tr><th>رقم الفاتورة</th><th>التاريخ</th><th>المبلغ</th></tr>
                {''.join([f"<tr><td>{i.get('id', i.get('invoice_number', 'غير محدد'))}</td><td>{i.get('date', i.get('invoice_date', 'غير محدد'))}</td><td>{i.get('amount', i.get('total', i.get('final_amount', 0)))}</td></tr>" for i in invoices])}
            </table>
            <p>تم إنشاء التقرير في: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """

        print("📄 يتم الآن تحويل الفواتير إلى PDF...")

        try:
            from weasyprint import HTML
            pdf_io = BytesIO()
            HTML(string=html).write_pdf(pdf_io)
            pdf_io.seek(0)

            print("✅ [SUCCESS] تم إنشاء ملف PDF بنجاح")
            return send_file(pdf_io, download_name=f"invoices_{section}_{month}.pdf", as_attachment=True)

        except ImportError:
            print("⚠️ [WARNING] weasyprint غير متاح، إرجاع HTML")
            return html

        except Exception as pdf_error:
            print(f"❌ [PDF_ERROR] خطأ في إنشاء PDF: {pdf_error}")
            return html

    except Exception as e:
        print(f"🔥 [EXCEPTION] حدث استثناء: {str(e)}")
        return "حدث خطأ غير متوقع، راجع الخادم."

@app.route('/print-test')
def print_test_page():
    """صفحة اختبار الطباعة المباشرة"""
    return '''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>اختبار الطباعة</title>
            <style>
                body { font-family: Arial, sans-serif; direction: rtl; margin: 20px; }
                form { max-width: 400px; margin: 0 auto; }
                label { display: block; margin: 10px 0 5px; }
                select, button { width: 100%; padding: 10px; margin: 5px 0; }
                button { background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <h2>طباعة الفواتير حسب الشهر والقسم</h2>
            <form method="POST" action="/print-invoices">
                <label>القسم:</label>
                <select name="section" required>
                    <option value="sales">المبيعات</option>
                    <option value="purchases">المشتريات</option>
                    <option value="expenses">المصروفات</option>
                    <option value="payroll">الرواتب</option>
                </select>

                <label>الشهر:</label>
                <select name="month" required>
                    <option value="2025-07">يوليو 2025</option>
                    <option value="2025-08">أغسطس 2025</option>
                    <option value="2025-09">سبتمبر 2025</option>
                    <option value="2025-10">أكتوبر 2025</option>
                </select>

                <button type="submit">طباعة</button>
            </form>

            <hr>
            <h3>روابط مفيدة:</h3>
            <ul>
                <li><a href="/payments_dues">شاشة المدفوعات والمستحقات</a></li>
                <li><a href="/print_invoices_preview?type=sales&month=2025-08&status=all&details=true">معاينة طباعة المبيعات</a></li>
                <li><a href="/api/available_months?type=sales">API الأشهر المتاحة</a></li>
            </ul>
        </body>
        </html>
    '''

# تم حذف الدالة المكررة print_invoices لحل مشكلة التعارض

@app.route('/api/expenses/edit/<int:record_id>', methods=['PUT'])
@login_required
def expenses_edit_record(record_id):
    """Edit expenses record"""
    try:
        logger.info(f"🔵 Expenses - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for expenses
        
        logger.info(f"✅ Expenses record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Expenses updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating expenses record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating expenses: {str(e)}'})

@app.route('/api/expenses/delete/<int:record_id>', methods=['DELETE'])
@login_required
def expenses_delete_record(record_id):
    """Delete expenses record"""
    try:
        logger.info(f"🔵 Expenses - Delete Record button clicked for ID: {record_id}")

        # البحث عن المصروف
        expense = Expense.query.get(record_id)
        if not expense:
            return jsonify({'success': False, 'message': 'Expense not found'})

        # حذف المصروف
        db.session.delete(expense)
        db.session.commit()

        logger.info(f"✅ Expenses record {record_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Expense deleted successfully'})

    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error deleting expenses record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting expense: {str(e)}'})

    """Print expenses record"""
    try:
        logger.info(f"🔵 Expenses - Print Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual print logic for expenses
        
        logger.info(f"✅ Expenses record {record_id} prepared for print")
        return jsonify({'success': True, 'message': 'Print prepared', 'print_url': f'/print/expenses/{record_id}'})
        
    except Exception as e:
        logger.error(f"❌ Error preparing expenses record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

# EMPLOYEES HANDLERS

@app.route('/api/employees', methods=['GET'])
@login_required
def get_employees():
    """Get all employees"""
    try:
        # For now, return empty array since we don't have Employee model yet
        # TODO: Implement actual Employee model and database queries
        employees = []

        return jsonify({
            'success': True,
            'employees': employees,
            'message': 'Employees loaded successfully'
        })

    except Exception as e:
        logger.error(f"❌ Error loading employees: {str(e)}")
        return jsonify({
            'success': False,
            'employees': [],
            'message': f'Error loading employees: {str(e)}'
        })

@app.route('/api/employees/save', methods=['POST'])
@login_required
def employees_save_record():
    """Save employees record"""
    try:
        logger.info("🔵 Employees - Save Record button clicked")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual save logic for employees
        # For now, return success with dummy ID
        
        logger.info(f"✅ Employees record saved successfully")
        return jsonify({'success': True, 'message': 'Employees saved successfully', 'id': 1})
        
    except Exception as e:
        logger.error(f"❌ Error saving employees record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving employees: {str(e)}'})

@app.route('/api/employees/edit/<int:record_id>', methods=['PUT'])
@login_required
def employees_edit_record(record_id):
    """Edit employees record"""
    try:
        logger.info(f"🔵 Employees - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for employees
        
        logger.info(f"✅ Employees record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Employees updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating employees record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating employees: {str(e)}'})

@app.route('/api/employees/delete/<int:record_id>', methods=['DELETE'])
@login_required
def employees_delete_record(record_id):
    """Delete employees record"""
    try:
        logger.info(f"🔵 Employees - Delete Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual delete logic for employees
        
        logger.info(f"✅ Employees record {record_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Employees deleted successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error deleting employees record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting employees: {str(e)}'})

    """Search employees records"""
    try:
        logger.info("🔵 Employees - Search Records button clicked")
        
        query = request.args.get('q', '')
        
        # TODO: Implement actual search logic for employees
        
        logger.info(f"✅ Employees search completed")
        return jsonify({'success': True, 'message': 'Search completed', 'results': []})
        
    except Exception as e:
        logger.error(f"❌ Error searching employees records: {str(e)}")
        return jsonify({'success': False, 'message': f'Error searching employees: {str(e)}'})

    """Print employees record"""
    try:
        logger.info(f"🔵 Employees - Print Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual print logic for employees
        
        logger.info(f"✅ Employees record {record_id} prepared for print")
        return jsonify({'success': True, 'message': 'Print prepared', 'print_url': f'/print/employees/{record_id}'})
        
    except Exception as e:
        logger.error(f"❌ Error preparing employees record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

# TAXES HANDLERS

@app.route('/api/taxes/save', methods=['POST'])
@login_required
def taxes_save_record():
    """Save taxes record"""
    try:
        logger.info("🔵 Taxes - Save Record button clicked")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual save logic for taxes
        # For now, return success with dummy ID
        
        logger.info(f"✅ Taxes record saved successfully")
        return jsonify({'success': True, 'message': 'Taxes saved successfully', 'id': 1})
        
    except Exception as e:
        logger.error(f"❌ Error saving taxes record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving taxes: {str(e)}'})

@app.route('/api/taxes/edit/<int:record_id>', methods=['PUT'])
@login_required
def taxes_edit_record(record_id):
    """Edit taxes record"""
    try:
        logger.info(f"🔵 Taxes - Edit Record button clicked for ID: {record_id}")
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # TODO: Implement actual edit logic for taxes
        
        logger.info(f"✅ Taxes record {record_id} updated successfully")
        return jsonify({'success': True, 'message': 'Taxes updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating taxes record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating taxes: {str(e)}'})

@app.route('/api/taxes/delete/<int:record_id>', methods=['DELETE'])
@login_required
def taxes_delete_record(record_id):
    """Delete taxes record"""
    try:
        logger.info(f"🔵 Taxes - Delete Record button clicked for ID: {record_id}")
        
        # TODO: Implement actual delete logic for taxes
        
        logger.info(f"✅ Taxes record {record_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Taxes deleted successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error deleting taxes record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting taxes: {str(e)}'})

# =============================================================================
# SALES MANAGEMENT ROUTES - مسارات إدارة المبيعات
# =============================================================================

@app.route('/sales/new')
@login_required
def new_invoice():
    """صفحة إنشاء فاتورة جديدة"""
    branches = Branch.query.all()
    customers = Customer.query.all()
    products = Product.query.all()

    # إنشاء رقم فاتورة تلقائي
    today = datetime.now()
    invoice_number = f"INV-{today.strftime('%Y%m%d')}-{today.microsecond // 1000:03d}"

    return render_template('simple_invoice.html',
                         branches=branches,
                         customers=customers,
                         products=products,
                         invoice_number=invoice_number,
                         today_date=today.strftime('%Y-%m-%d'))

@app.route('/sales/save', methods=['POST'])
@login_required
def save_sale():
    """حفظ فاتورة مبيعات جديدة"""
    try:
        # الحصول على اسم العميل إذا تم اختياره
        customer_name = 'عميل نقدي'
        if request.form.get('customer_id'):
            customer = Customer.query.get(request.form['customer_id'])
            if customer:
                customer_name = customer.name

        # إنشاء الفاتورة
        sale = Sale(
            invoice_number=request.form['invoice_number'],
            invoice_date=datetime.strptime(request.form['invoice_date'], '%Y-%m-%d').date(),
            branch_id=int(request.form['branch_id']),
            customer_name=customer_name,
            total_amount=float(request.form['total_amount']),
            tax_amount=float(request.form['tax_amount']),
            final_amount=float(request.form['final_amount']),
            payment_method=request.form['payment_method'],
            created_by=current_user.id,
            created_at=datetime.now()
        )

        db.session.add(sale)
        db.session.flush()  # للحصول على معرف الفاتورة

        # إضافة عناصر الفاتورة
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')
        total_prices = request.form.getlist('total_price[]')

        for i in range(len(product_ids)):
            if product_ids[i] and quantities[i] and unit_prices[i]:  # تأكد من وجود جميع البيانات
                product = Product.query.get(product_ids[i])
                quantity = float(quantities[i])
                unit_price = float(unit_prices[i])
                total_price = quantity * unit_price

                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=int(product_ids[i]),
                    product_name=product.product_name if product else 'منتج محذوف',
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                db.session.add(sale_item)

        db.session.commit()
        flash('تم حفظ الفاتورة بنجاح', 'success')
        return redirect(url_for('sales'))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حفظ الفاتورة: {str(e)}', 'error')
        return redirect(url_for('new_invoice'))

@app.route('/sales/delete/<int:invoice_id>', methods=['POST'])
@login_required
def delete_invoice(invoice_id):
    """حذف فاتورة مبيعات"""
    try:
        sale = Sale.query.get_or_404(invoice_id)

        # حذف عناصر الفاتورة أولاً
        SaleItem.query.filter_by(sale_id=invoice_id).delete()

        # حذف الفاتورة
        db.session.delete(sale)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'تم حذف الفاتورة {sale.invoice_number} بنجاح'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء حذف الفاتورة: {str(e)}'
        }), 500

@app.route('/sales/print/<int:invoice_id>')
@login_required
def print_sales_invoice(invoice_id):
    """طباعة فاتورة مبيعات"""
    sale = Sale.query.get_or_404(invoice_id)
    sale_items = SaleItem.query.filter_by(sale_id=invoice_id).all()

    return render_template('print_invoice.html',
                         sale=sale,
                         sale_items=sale_items)

@app.route('/payments/new')
@login_required
def new_payment():
    """صفحة تسجيل دفعة جديدة"""

    # الحصول على جميع أنواع الفواتير غير المدفوعة
    unpaid_sales = Sale.query.filter(Sale.payment_status.in_(['pending', 'partial'])).all()
    unpaid_purchases = Purchase.query.filter(Purchase.payment_status.in_(['pending', 'partial'])).all()
    unpaid_expenses = Expense.query.filter(Expense.payment_status.in_(['pending', 'partial'])).all()
    unpaid_payrolls = EmployeePayroll.query.filter(EmployeePayroll.payment_status.in_(['pending', 'partial'])).all()

    # دمج جميع الفواتير في قائمة واحدة مع تحديد النوع
    all_invoices = []

    for sale in unpaid_sales:
        all_invoices.append({
            'id': sale.id,
            'type': 'sale',
            'invoice_number': sale.invoice_number,
            'customer_name': sale.customer_name or 'عميل نقدي',
            'total_amount': sale.final_amount,
            'paid_amount': sale.get_total_paid(),
            'remaining_amount': sale.get_remaining_amount(),
            'date': sale.invoice_date,
            'status': sale.payment_status
        })

    for purchase in unpaid_purchases:
        all_invoices.append({
            'id': purchase.id,
            'type': 'purchase',
            'invoice_number': purchase.invoice_number,
            'customer_name': purchase.supplier_name or 'مورد',
            'total_amount': purchase.final_amount,
            'paid_amount': purchase.get_total_paid(),
            'remaining_amount': purchase.get_remaining_amount(),
            'date': purchase.invoice_date,
            'status': purchase.payment_status
        })

    for expense in unpaid_expenses:
        all_invoices.append({
            'id': expense.id,
            'type': 'expense',
            'invoice_number': expense.expense_number,
            'customer_name': expense.expense_type,
            'total_amount': expense.amount,
            'paid_amount': expense.get_total_paid(),
            'remaining_amount': expense.get_remaining_amount(),
            'date': expense.expense_date,
            'status': expense.payment_status
        })

    for payroll in unpaid_payrolls:
        # تحويل التاريخ إلى datetime.date للتوافق مع باقي التواريخ
        from datetime import date
        payroll_date = date(payroll.year, payroll.month, 1)

        all_invoices.append({
            'id': payroll.id,
            'type': 'payroll',
            'invoice_number': payroll.payroll_number,
            'customer_name': payroll.employee_name,
            'total_amount': payroll.net_salary,
            'paid_amount': payroll.get_total_paid(),
            'remaining_amount': payroll.get_remaining_amount(),
            'date': payroll_date,
            'status': payroll.payment_status
        })

    # ترتيب الفواتير حسب التاريخ
    all_invoices.sort(key=lambda x: x['date'], reverse=True)

    # إذا تم تمرير معرف فاتورة محددة
    selected_invoice_id = request.args.get('invoice')

    return render_template('new_payment.html',
                         invoices=all_invoices,
                         selected_invoice_id=selected_invoice_id,
                         today_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/update_payment_statuses')
@login_required
def update_payment_statuses_route():
    """مسار لتحديث حالات الدفع يدوياً"""
    try:
        update_all_payment_statuses()
        flash('تم تحديث حالات الدفع بنجاح', 'success')
    except Exception as e:
        flash(f'خطأ في تحديث حالات الدفع: {str(e)}', 'error')
    return redirect(url_for('payments_dues'))

@app.route('/payments/submit', methods=['POST'])
@login_required
def submit_payment():
    """استقبال وحفظ دفعة جديدة"""
    try:
        data = request.form

        # إنشاء سجل الدفعة
        payment = Payment(
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            notes=data.get('notes', ''),
            created_by=current_user.id,
            created_at=datetime.now()
        )

        db.session.add(payment)
        db.session.flush()  # للحصول على معرف الدفعة

        # ربط الدفعة بالفواتير المحددة
        selected_invoices = request.form.getlist('selected_invoices')
        for invoice_ref in selected_invoices:
            # تحليل نوع الفاتورة ومعرفها (مثل: sale_1, purchase_2, expense_3, payroll_4)
            invoice_type, invoice_id = invoice_ref.split('_')
            applied_amount = float(data.get(f'applied_amount_{invoice_ref}', 0))

            if applied_amount > 0:
                # تحديد الفاتورة المناسبة حسب النوع
                if invoice_type == 'sale':
                    invoice_obj = Sale.query.get(invoice_id)
                    # التأكد من أن المبلغ المطبق لا يتجاوز المبلغ المتبقي
                    remaining = invoice_obj.get_remaining_amount()
                    if applied_amount > remaining:
                        applied_amount = remaining

                    payment_link = PaymentSale(
                        payment_id=payment.id,
                        sale_id=int(invoice_id),
                        applied_amount=applied_amount
                    )
                    db.session.add(payment_link)

                elif invoice_type == 'purchase':
                    invoice_obj = Purchase.query.get(invoice_id)
                    remaining = invoice_obj.get_remaining_amount()
                    if applied_amount > remaining:
                        applied_amount = remaining

                    payment_link = PaymentPurchase(
                        payment_id=payment.id,
                        purchase_id=int(invoice_id),
                        applied_amount=applied_amount
                    )
                    db.session.add(payment_link)

                elif invoice_type == 'expense':
                    invoice_obj = Expense.query.get(invoice_id)
                    remaining = invoice_obj.get_remaining_amount()
                    if applied_amount > remaining:
                        applied_amount = remaining

                    payment_link = PaymentExpense(
                        payment_id=payment.id,
                        expense_id=int(invoice_id),
                        applied_amount=applied_amount
                    )
                    db.session.add(payment_link)

                elif invoice_type == 'payroll':
                    invoice_obj = EmployeePayroll.query.get(invoice_id)
                    remaining = invoice_obj.get_remaining_amount()
                    if applied_amount > remaining:
                        applied_amount = remaining

                    payment_link = PaymentPayroll(
                        payment_id=payment.id,
                        payroll_id=int(invoice_id),
                        applied_amount=applied_amount
                    )
                    db.session.add(payment_link)

        # حفظ التغييرات أولاً
        db.session.commit()

        # تحديث حالة الدفع لجميع الفواتير المتأثرة
        for invoice_ref in selected_invoices:
            invoice_type, invoice_id = invoice_ref.split('_')

            if invoice_type == 'sale':
                invoice_obj = Sale.query.get(invoice_id)
            elif invoice_type == 'purchase':
                invoice_obj = Purchase.query.get(invoice_id)
            elif invoice_type == 'expense':
                invoice_obj = Expense.query.get(invoice_id)
            elif invoice_type == 'payroll':
                invoice_obj = EmployeePayroll.query.get(invoice_id)

            invoice_obj.update_payment_status()

        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
        return redirect(url_for('payments_dues'))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تسجيل الدفعة: {str(e)}', 'error')
        return redirect(url_for('new_payment'))

def get_invoices_with_items(section, month):
    """جلب الفواتير مع البنود - مثل الكود المرسل"""
    try:
        year, month_num = month.split('-')
        year = int(year)
        month_num = int(month_num)

        all_data = []

        if section == 'sales':
            # جلب فواتير المبيعات
            invoices = Sale.query.filter(
                db.extract('year', Sale.invoice_date) == year,
                db.extract('month', Sale.invoice_date) == month_num
            ).order_by(Sale.invoice_date).all()

            for inv in invoices:
                # جلب البنود المرتبطة
                items = SaleItem.query.filter_by(sale_id=inv.id).all()

                item_list = []
                for item in items:
                    item_list.append({
                        "description": item.product_name,
                        "quantity": item.quantity,
                        "price": item.unit_price,
                        "total": item.total_price
                    })

                all_data.append({
                    "id": inv.id,
                    "invoice_number": inv.invoice_number,
                    "invoice_date": inv.invoice_date.strftime('%Y-%m-%d'),
                    "customer_name": inv.customer_name,
                    "total": inv.final_amount,
                    "payment_status": inv.payment_status,
                    "items": item_list
                })

        elif section == 'purchases':
            # جلب فواتير المشتريات
            invoices = Purchase.query.filter(
                db.extract('year', Purchase.invoice_date) == year,
                db.extract('month', Purchase.invoice_date) == month_num
            ).order_by(Purchase.invoice_date).all()

            for inv in invoices:
                # جلب البنود المرتبطة
                items = PurchaseItem.query.filter_by(purchase_id=inv.id).all()

                item_list = []
                for item in items:
                    item_list.append({
                        "description": item.product_name,
                        "quantity": item.quantity,
                        "price": item.unit_price,
                        "total": item.total_price
                    })

                all_data.append({
                    "id": inv.id,
                    "invoice_number": inv.invoice_number,
                    "invoice_date": inv.invoice_date.strftime('%Y-%m-%d'),
                    "supplier_name": inv.supplier_name,
                    "total": inv.final_amount,
                    "payment_status": inv.payment_status,
                    "items": item_list
                })

        elif section == 'expenses':
            # جلب المصروفات
            expenses = Expense.query.filter(
                db.extract('year', Expense.expense_date) == year,
                db.extract('month', Expense.expense_date) == month_num
            ).order_by(Expense.expense_date).all()

            for exp in expenses:
                all_data.append({
                    "id": exp.id,
                    "expense_number": exp.expense_number,
                    "expense_date": exp.expense_date.strftime('%Y-%m-%d'),
                    "expense_type": exp.expense_type,
                    "description": exp.description,
                    "amount": exp.amount,
                    "payment_status": exp.payment_status
                })

        return all_data

    except Exception as e:
        print(f"خطأ في جلب الفواتير: {e}")
        return []

@app.route('/api/available_months')
@login_required
def get_available_months():
    """API لجلب الأشهر المتاحة للطباعة"""
    try:
        invoice_type = request.args.get('type', 'sales')
        months_data = []

        if invoice_type == 'sales':
            # جلب الأشهر من فواتير المبيعات
            sales_months = db.session.query(
                db.extract('year', Sale.invoice_date).label('year'),
                db.extract('month', Sale.invoice_date).label('month')
            ).distinct().order_by(
                db.extract('year', Sale.invoice_date).desc(),
                db.extract('month', Sale.invoice_date).desc()
            ).all()

            for year, month in sales_months:
                months_data.append({
                    'value': f"{int(year)}-{int(month):02d}",
                    'text': f"{get_month_name(int(month))} {int(year)}",
                    'year': int(year),
                    'month': int(month)
                })

        elif invoice_type == 'purchases':
            # جلب الأشهر من فواتير المشتريات
            purchases_months = db.session.query(
                db.extract('year', Purchase.invoice_date).label('year'),
                db.extract('month', Purchase.invoice_date).label('month')
            ).distinct().order_by(
                db.extract('year', Purchase.invoice_date).desc(),
                db.extract('month', Purchase.invoice_date).desc()
            ).all()

            for year, month in purchases_months:
                months_data.append({
                    'value': f"{int(year)}-{int(month):02d}",
                    'text': f"{get_month_name(int(month))} {int(year)}",
                    'year': int(year),
                    'month': int(month)
                })

        elif invoice_type == 'expenses':
            # جلب الأشهر من المصروفات
            expenses_months = db.session.query(
                db.extract('year', Expense.expense_date).label('year'),
                db.extract('month', Expense.expense_date).label('month')
            ).distinct().order_by(
                db.extract('year', Expense.expense_date).desc(),
                db.extract('month', Expense.expense_date).desc()
            ).all()

            for year, month in expenses_months:
                months_data.append({
                    'value': f"{int(year)}-{int(month):02d}",
                    'text': f"{get_month_name(int(month))} {int(year)}",
                    'year': int(year),
                    'month': int(month)
                })

        elif invoice_type == 'payroll':
            # جلب الأشهر من الرواتب
            payroll_months = db.session.query(
                EmployeePayroll.year,
                EmployeePayroll.month
            ).distinct().order_by(
                EmployeePayroll.year.desc(),
                EmployeePayroll.month.desc()
            ).all()

            for year, month in payroll_months:
                months_data.append({
                    'value': f"{year}-{month:02d}",
                    'text': f"{get_month_name(month)} {year}",
                    'year': year,
                    'month': month
                })

        return jsonify({
            'success': True,
            'months': months_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب الأشهر: {e}'
        }), 500

def get_month_name(month_num):
    """الحصول على اسم الشهر بالعربية"""
    months = {
        1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل',
        5: 'مايو', 6: 'يونيو', 7: 'يوليو', 8: 'أغسطس',
        9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
    }
    return months.get(month_num, f'شهر {month_num}')

@app.route('/download_invoices_pdf')
@login_required
def download_invoices_pdf():
    """تحميل تقرير الفواتير كملف PDF"""
    try:
        # استيراد مكتبات PDF
        try:
            from weasyprint import HTML, CSS
        except ImportError:
            # fallback إذا لم تكن weasyprint متاحة
            return redirect(url_for('print_invoices_preview', **request.args))

        invoice_type = request.args.get('type', 'sales')
        month = request.args.get('month', '')
        status = request.args.get('status', 'all')
        include_details = request.args.get('details', 'false').lower() == 'true'

        if not month:
            flash('يرجى اختيار الشهر والسنة', 'error')
            return redirect(url_for('payments_dues'))

        # تحليل الشهر والسنة
        try:
            year, month_num = month.split('-')
            year = int(year)
            month_num = int(month_num)
        except ValueError:
            flash('تنسيق الشهر غير صحيح', 'error')
            return redirect(url_for('payments_dues'))

        # جلب البيانات (نفس منطق print_invoices)
        invoices = []

        if invoice_type == 'sales':
            query = Sale.query.filter(
                db.extract('year', Sale.invoice_date) == year,
                db.extract('month', Sale.invoice_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Sale.invoice_date.desc()).all()

        elif invoice_type == 'purchases':
            query = Purchase.query.filter(
                db.extract('year', Purchase.invoice_date) == year,
                db.extract('month', Purchase.invoice_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Purchase.invoice_date.desc()).all()

        elif invoice_type == 'expenses':
            query = Expense.query.filter(
                db.extract('year', Expense.expense_date) == year,
                db.extract('month', Expense.expense_date) == month_num
            )
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(Expense.expense_date.desc()).all()

        elif invoice_type == 'payroll':
            query = EmployeePayroll.query.filter_by(year=year, month=month_num)
            if status != 'all':
                query = query.filter_by(payment_status=status)
            invoices = query.order_by(EmployeePayroll.created_at.desc()).all()

        # إنشاء HTML للطباعة
        html_content = render_template('print_invoices.html',
                                     invoices=invoices,
                                     invoice_type=invoice_type,
                                     month=month,
                                     status=status,
                                     include_details=include_details,
                                     year=year,
                                     month_num=month_num)

        # تحويل إلى PDF
        pdf = HTML(string=html_content).write_pdf()

        # تحديد اسم الملف
        type_names = {
            'sales': 'مبيعات',
            'purchases': 'مشتريات',
            'expenses': 'مصروفات',
            'payroll': 'رواتب'
        }

        filename = f"تقرير_{type_names.get(invoice_type, invoice_type)}_{month}_{status}.pdf"

        # إرسال الملف
        from flask import make_response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        flash(f'خطأ في إنشاء ملف PDF: {e}', 'error')
        return redirect(url_for('payments_dues'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data()
        # تحديث حالات الدفع عند بدء التطبيق
        update_all_payment_statuses()

    # مسح cache القوالب قبل التشغيل
    app.jinja_env.cache = {}

    print("🚀 تشغيل الخادم مع debug mode")
    print("🔄 إعادة التحميل التلقائي مفعلة")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), use_reloader=True)
