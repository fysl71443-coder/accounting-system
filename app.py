#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المحاسبة المتكامل مع خانات الخصم
Complete Accounting System with Discount Fields
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import logging
import os
import json
import time

# إعداد التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = 'complete-accounting-system-with-discount'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد قاعدة البيانات
db = SQLAlchemy(app)

# إعداد نظام تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# إعداد نظام السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# نماذج قاعدة البيانات
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0)
    cost = db.Column(db.Float, default=0)
    quantity = db.Column(db.Integer, default=0)  # Changed from stock_quantity to quantity
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Product class already defined above - removing duplicate

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    subtotal = db.Column(db.Float, nullable=False, default=0)
    discount = db.Column(db.Float, nullable=False, default=0)
    tax_rate = db.Column(db.Float, default=15.0)  # Default VAT rate 15%
    tax_amount = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    # حقول نظام المدفوعات
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, partial, paid, overdue
    paid_amount = db.Column(db.Float, default=0)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    customer = db.relationship('Customer', backref='sales')

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(100), nullable=False)  # Store name in case product is deleted
    quantity = db.Column(db.Float, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    total_price = db.Column(db.Float, nullable=False, default=0)
    discount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)

    sale = db.relationship('Sale', backref='items')
    product = db.relationship('Product', backref='sale_items')

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    subtotal = db.Column(db.Float, nullable=False, default=0)
    discount = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    # حقول نظام المدفوعات
    payment_status = db.Column(db.String(20), default='unpaid')
    paid_amount = db.Column(db.Float, default=0)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    supplier = db.relationship('Supplier', backref='purchases')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_type = db.Column(db.String(100))  # نوع المصروف
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    reference = db.Column(db.String(100))  # رقم المرجع
    vendor = db.Column(db.String(200))  # المورد
    notes = db.Column(db.Text)
    # حقول نظام المدفوعات
    payment_status = db.Column(db.String(20), default='unpaid')
    paid_amount = db.Column(db.Float, default=0)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    salary = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    hire_date = db.Column(db.Date, default=date.today)

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7))  # YYYY-MM format
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    # حقول نظام المدفوعات
    payment_status = db.Column(db.String(20), default='unpaid')
    paid_amount = db.Column(db.Float, default=0)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    employee = db.relationship('Employee', backref='payrolls')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# إنشاء الجداول
with app.app_context():
    db.create_all()
    
    # إنشاء مستخدم افتراضي
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin112233'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logger.info("✅ تم إنشاء المستخدم الافتراضي")

# إنشاء الجداول فقط
with app.app_context():
    db.create_all()

    # إنشاء مستخدم افتراضي إذا لم يكن موجوداً
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin112233'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logger.info("✅ تم إنشاء المستخدم الافتراضي")

    # إنشاء منتجات تجريبية (معطل مؤقتاً لحل مشكلة قاعدة البيانات)
    # إنشاء منتجات تجريبية (معطل مؤقتاً لحل مشكلة قاعدة البيانات)
    # if Product.query.count() == 0:
    #     sample_products = [
    #         Product(name='لابتوب ديل', description='لابتوب ديل انسبايرون 15', price=2500.00, cost=2000.00, stock_quantity=10, category='إلكترونيات'),
    #         Product(name='ماوس لاسلكي', description='ماوس لاسلكي لوجيتك', price=150.00, cost=100.00, stock_quantity=50, category='إكسسوارات'),
    #         Product(name='كيبورد ميكانيكي', description='كيبورد ميكانيكي للألعاب', price=300.00, cost=200.00, stock_quantity=25, category='إكسسوارات'),
    #         Product(name='شاشة 24 بوصة', description='شاشة LED 24 بوصة', price=800.00, cost=600.00, stock_quantity=15, category='إلكترونيات'),
    #         Product(name='طابعة HP', description='طابعة HP ليزر', price=1200.00, cost=900.00, stock_quantity=8, category='مكتبية')
    #     ]
    #
    #     for product in sample_products:
    #         db.session.add(product)
    #
    #     db.session.commit()
    #     logger.info("✅ تم إنشاء المنتجات التجريبية")

# Routes الأساسية
@app.route('/')
def home():
    """الصفحة الرئيسية"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
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
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم"""
    # إحصائيات سريعة
    stats = {
        'sales_count': Sale.query.count(),
        'purchases_count': Purchase.query.count(),
        'expenses_count': Expense.query.count(),
        'employees_count': Employee.query.count(),
        'total_sales': db.session.query(db.func.sum(Sale.total)).scalar() or 0,
        'total_purchases': db.session.query(db.func.sum(Purchase.total)).scalar() or 0,
        'total_expenses': db.session.query(db.func.sum(Expense.amount)).scalar() or 0,
        'total_discount_sales': db.session.query(db.func.sum(Sale.discount)).scalar() or 0,
        'total_discount_purchases': db.session.query(db.func.sum(Purchase.discount)).scalar() or 0,
        'total_salaries': db.session.query(db.func.sum(Employee.salary)).scalar() or 0
    }

    return render_template('dashboard_new.html', stats=stats)

@app.route('/payments_dues')
@login_required
def payments_dues():
    """صفحة المدفوعات والمستحقات"""
    # جمع البيانات من جميع الجداول
    sales_list = Sale.query.all()
    purchases_list = Purchase.query.all()
    expenses_list = Expense.query.all()
    payrolls_list = Payroll.query.all()

    # حساب الإحصائيات
    total_sales = sum(s.total for s in sales_list)
    total_purchases = sum(p.total for p in purchases_list)
    total_expenses = sum(e.amount for e in expenses_list)
    total_payrolls = sum(p.amount for p in payrolls_list)

    summary_data = {
        'total_amount': total_sales + total_purchases + total_expenses + total_payrolls,
        'total_paid': total_sales + total_purchases + total_expenses + total_payrolls,  # افتراض أن كل شيء مدفوع
        'total_due': 0,  # يمكن حسابها لاحقاً
        'unpaid_count': 0,  # يمكن حسابها لاحقاً
        'sales_amount': total_sales,
        'purchases_amount': total_purchases,
        'expenses_amount': total_expenses,
        'payroll_amount': total_payrolls
    }

    return render_template('payments_dues.html',
                         summary_data=summary_data,
                         sales=sales_list,
                         purchases=purchases_list,
                         expenses=expenses_list,
                         payrolls=payrolls_list)

@app.route('/sales')
@login_required
def sales():
    """صفحة المبيعات"""
    sales_list = Sale.query.order_by(Sale.date.desc()).all()
    customers = Customer.query.all()

    # إضافة فروع وهمية للاختبار
    branches = [
        {'id': 1, 'name': 'PLACE INDIA'},
        {'id': 2, 'name': 'CHINA TOWN'}
    ]

    return render_template('sales.html',
                         sales=sales_list,
                         customers=customers,
                         branches=branches,
                         selected_branch=None)

@app.route('/purchases')
@login_required
def purchases():
    """صفحة المشتريات"""
    purchases_list = Purchase.query.order_by(Purchase.date.desc()).all()
    suppliers = Supplier.query.all()

    # حساب الإحصائيات
    summary_data = {
        'total_purchases': sum(p.total for p in purchases_list),
        'total_paid': sum(p.total for p in purchases_list),  # افتراض أن كل المشتريات مدفوعة
        'pending_purchases': 0,  # يمكن حسابها لاحقاً
        'invoices_count': len(purchases_list)
    }

    return render_template('purchases.html',
                         purchases=purchases_list,
                         suppliers=suppliers,
                         summary_data=summary_data)

@app.route('/expenses')
@login_required
def expenses():
    """صفحة المصروفات - تم إعادة توجيهها للصفحة الجديدة التي تعمل"""
    expenses_list = Expense.query.order_by(Expense.date.desc()).all()

    # حساب الإحصائيات
    summary_data = {
        'total_expenses': sum(e.amount for e in expenses_list),
        'expenses_count': len(expenses_list),
        'pending_expenses': sum(e.amount for e in expenses_list if e.payment_status != 'paid'),
        'avg_expense': sum(e.amount for e in expenses_list) / len(expenses_list) if expenses_list else 0
    }

    # استخدام الصفحة الجديدة التي تعمل
    return render_template('expenses_new.html', expenses=expenses_list, summary_data=summary_data)

# مسارات إنشاء الفواتير الجديدة
@app.route('/sales/new')
@login_required
def new_sale():
    """صفحة إنشاء فاتورة مبيعات جديدة"""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('sale_form.html', today=today)

@app.route('/purchases/new')
@login_required
def new_purchase():
    """صفحة إنشاء فاتورة مشتريات جديدة"""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('purchase_form.html', today=today)

@app.route('/purchases/simple')
@login_required
def simple_purchase():
    """صفحة إنشاء فاتورة مشتريات بسيطة"""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('purchase_form.html', today=today)

# مسارات التعديل والطباعة
@app.route('/sales/edit/<int:sale_id>')
@login_required
def edit_sale(sale_id):
    """صفحة تعديل فاتورة مبيعات"""
    flash(f'🚧 صفحة تعديل فاتورة المبيعات رقم {sale_id} قيد التطوير', 'info')
    return redirect(url_for('sales'))

@app.route('/purchases/edit/<int:purchase_id>')
@login_required
def edit_purchase(purchase_id):
    """صفحة تعديل فاتورة مشتريات"""
    flash(f'🚧 صفحة تعديل فاتورة المشتريات رقم {purchase_id} قيد التطوير', 'info')
    return redirect(url_for('purchases'))

@app.route('/sales/print/<int:sale_id>')
@login_required
def print_sale_page(sale_id):
    """طباعة فاتورة مبيعات"""
    flash(f'🚧 طباعة فاتورة المبيعات رقم {sale_id} قيد التطوير', 'info')
    return redirect(url_for('sales'))

@app.route('/purchases/print/<int:purchase_id>')
@login_required
def print_purchase_page(purchase_id):
    """طباعة فاتورة مشتريات"""
    flash(f'🚧 طباعة فاتورة المشتريات رقم {purchase_id} قيد التطوير', 'info')
    return redirect(url_for('purchases'))

@app.route('/sales/preview/<int:sale_id>')
@login_required
def preview_sale_page(sale_id):
    """معاينة فاتورة مبيعات"""
    flash(f'🚧 معاينة فاتورة المبيعات رقم {sale_id} قيد التطوير', 'info')
    return redirect(url_for('sales'))

@app.route('/purchases/preview/<int:purchase_id>')
@login_required
def preview_purchase_page(purchase_id):
    """معاينة فاتورة مشتريات"""
    flash(f'🚧 معاينة فاتورة المشتريات رقم {purchase_id} قيد التطوير', 'info')
    return redirect(url_for('purchases'))

# مسارات API للتصدير
@app.route('/api/sales/export')
@login_required
def export_sales_api():
    """تصدير المبيعات"""
    try:
        # يمكن إضافة منطق التصدير الفعلي هنا
        flash('🚧 تصدير المبيعات قيد التطوير', 'info')
        return redirect(url_for('sales'))
    except Exception as e:
        flash(f'❌ خطأ في تصدير المبيعات: {str(e)}', 'error')
        return redirect(url_for('sales'))

@app.route('/api/purchases/export')
@login_required
def export_purchases_api():
    """تصدير المشتريات"""
    try:
        # يمكن إضافة منطق التصدير الفعلي هنا
        flash('🚧 تصدير المشتريات قيد التطوير', 'info')
        return redirect(url_for('purchases'))
    except Exception as e:
        flash(f'❌ خطأ في تصدير المشتريات: {str(e)}', 'error')
        return redirect(url_for('purchases'))

@app.route('/expenses_test')
@login_required
def expenses_test():
    """صفحة اختبار المصروفات البسيطة"""
    expenses_list = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('expenses_simple.html', expenses=expenses_list)

@app.route('/test_buttons')
@login_required
def test_buttons():
    """صفحة اختبار الأزرار فقط"""
    expenses_list = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('test_buttons.html', expenses=expenses_list)

@app.route('/expenses_new')
@login_required
def expenses_new():
    """صفحة المصروفات الجديدة - تعمل بشكل صحيح"""
    expenses_list = Expense.query.order_by(Expense.date.desc()).all()

    # حساب الإحصائيات
    summary_data = {
        'total_expenses': sum(e.amount for e in expenses_list),
        'expenses_count': len(expenses_list),
        'pending_expenses': sum(e.amount for e in expenses_list if e.payment_status != 'paid'),
        'avg_expense': sum(e.amount for e in expenses_list) / len(expenses_list) if expenses_list else 0
    }

    return render_template('expenses_new.html', expenses=expenses_list, summary_data=summary_data)

@app.route('/expenses/new')
@login_required
def new_expense():
    """صفحة إضافة مصروف جديد"""
    return render_template('expense_form.html', action='add')

@app.route('/expenses/edit/<int:expense_id>')
@login_required
def edit_expense_page(expense_id):
    """صفحة تعديل مصروف"""
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense_form.html', expense=expense, action='edit')

@app.route('/employees')
@login_required
def employees():
    """صفحة الموظفين"""
    employees_list = Employee.query.all()
    return render_template('employees.html', employees=employees_list)

@app.route('/employee_payroll')
@login_required
def employee_payroll():
    """صفحة الموظفين والرواتب"""
    payrolls_list = Payroll.query.order_by(Payroll.date.desc()).all()
    employees_list = Employee.query.all()

    # حساب الإحصائيات
    summary_data = {
        'total_employees': len(employees_list),
        'total_payrolls': len(payrolls_list),
        'total_paid': sum(p.amount for p in payrolls_list),
        'pending_amount': 0  # يمكن حسابها لاحقاً
    }

    return render_template('employee_payroll.html',
                         payrolls=payrolls_list,
                         employees=employees_list,
                         summary_data=summary_data)

@app.route('/payroll')
@login_required
def payroll():
    """إعادة توجيه إلى صفحة الموظفين والرواتب"""
    return redirect(url_for('employee_payroll'))

@app.route('/customers')
@login_required
def customers():
    """صفحة العملاء"""
    customers_list = Customer.query.all()
    return render_template('customers.html', customers=customers_list)

@app.route('/suppliers')
@login_required
def suppliers():
    """صفحة الموردين"""
    suppliers_list = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers_list)

@app.route('/products')
@login_required
def products():
    """صفحة المنتجات الموحدة مع التكاليف"""
    products_list = Product.query.all()
    return render_template('unified_products.html', products=products_list)

@app.route('/inventory')
@login_required
def inventory():
    """صفحة المخزون"""
    products_list = Product.query.all()
    return render_template('inventory.html', products=products_list)

# الشاشات المفقودة
@app.route('/reports')
@login_required
def reports():
    """صفحة التقارير"""
    return render_template('reports.html')

@app.route('/financial_statements')
@login_required
def financial_statements():
    """صفحة القوائم المالية"""
    return render_template('financial_statements.html')

@app.route('/tax_management')
@login_required
def tax_management():
    """صفحة إدارة الضرائب"""
    return render_template('tax_management.html')

@app.route('/settings')
@login_required
def settings():
    """صفحة الإعدادات"""
    return render_template('settings.html')

@app.route('/user_management')
@login_required
def user_management():
    """صفحة إدارة المستخدمين"""
    users_list = User.query.all()
    return render_template('user_management.html', users=users_list)

@app.route('/cost_calculation')
@login_required
def cost_calculation():
    """صفحة حساب التكاليف"""
    return render_template('cost_calculation.html')

@app.route('/meal_cost_calculator')
@login_required
def meal_cost_calculator():
    """صفحة حاسبة تكلفة الوجبات"""
    return render_template('meal_cost_calculator.html')

@app.route('/advanced_reports')
@login_required
def advanced_reports():
    """صفحة التقارير المتقدمة"""
    return render_template('advanced_reports.html')



@app.route('/raw_materials')
@login_required
def raw_materials():
    """صفحة المواد الخام"""
    return render_template('raw_materials.html')

@app.route('/product_transfer')
@login_required
def product_transfer():
    """صفحة نقل المنتجات"""
    return render_template('product_transfer.html')

@app.route('/advanced_expenses')
@login_required
def advanced_expenses():
    """صفحة المصروفات المتقدمة"""
    return render_template('advanced_expenses.html')

@app.route('/role_management')
@login_required
def role_management():
    """صفحة إدارة الأدوار"""
    return render_template('role_management.html')

@app.route('/change_language', methods=['POST'])
def change_language():
    """تغيير اللغة"""
    try:
        data = request.get_json()
        language = data.get('language', 'ar')
        session['language'] = language
        return jsonify({'status': 'success', 'language': language})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/print_all_invoices/<invoice_type>')
@login_required
def print_all_invoices(invoice_type):
    """طباعة جميع الفواتير لنوع معين"""
    try:
        if invoice_type == 'sales':
            invoices = Sale.query.order_by(Sale.date.desc()).all()
            title = 'جميع فواتير المبيعات'
            headers = ['رقم الفاتورة', 'التاريخ', 'العميل', 'المبلغ الفرعي', 'الخصم', 'المجموع', 'ملاحظات']

        elif invoice_type == 'purchases':
            invoices = Purchase.query.order_by(Purchase.date.desc()).all()
            title = 'جميع فواتير المشتريات'
            headers = ['رقم الفاتورة', 'التاريخ', 'المورد', 'المبلغ الفرعي', 'الخصم', 'المجموع', 'ملاحظات']

        elif invoice_type == 'expenses':
            invoices = Expense.query.order_by(Expense.date.desc()).all()
            title = 'جميع فواتير المصروفات'
            headers = ['رقم المصروف', 'التاريخ', 'الوصف', 'الفئة', 'المبلغ', 'ملاحظات']

        elif invoice_type == 'payroll':
            invoices = Payroll.query.order_by(Payroll.date.desc()).all()
            title = 'جميع كشوف الرواتب'
            headers = ['رقم الكشف', 'التاريخ', 'الموظف', 'المنصب', 'المبلغ', 'ملاحظات']

        else:
            return "نوع فاتورة غير صحيح", 400

        # حساب الإجماليات
        if invoice_type in ['sales', 'purchases']:
            total_amount = sum(inv.total for inv in invoices)
            total_discount = sum(inv.discount for inv in invoices)
            subtotal_amount = sum(inv.subtotal for inv in invoices)
        elif invoice_type in ['expenses', 'payroll']:
            total_amount = sum(inv.amount for inv in invoices)
            total_discount = 0
            subtotal_amount = total_amount

        return render_template('print_all_invoices.html',
                             invoices=invoices,
                             invoice_type=invoice_type,
                             title=title,
                             headers=headers,
                             total_amount=total_amount,
                             total_discount=total_discount,
                             subtotal_amount=subtotal_amount,
                             count=len(invoices))

    except Exception as e:
        return f"خطأ في طباعة الفواتير: {str(e)}", 500

@app.route('/print_invoices/<invoice_type>')
@login_required
def print_invoices(invoice_type):
    """طباعة الفواتير مع خانات الخصم"""
    try:
        logger.info(f"🖨️ طباعة فواتير {invoice_type}")

        # تحديد البيانات حسب نوع الفاتورة
        if invoice_type == 'sales':
            data = Sale.query.order_by(Sale.date.desc()).all()
            title = 'تقرير فواتير المبيعات مع الخصم'
            color = '#007bff'
        elif invoice_type == 'purchases':
            data = Purchase.query.order_by(Purchase.date.desc()).all()
            title = 'تقرير فواتير المشتريات مع الخصم'
            color = '#28a745'
        elif invoice_type == 'expenses':
            data = Expense.query.order_by(Expense.date.desc()).all()
            title = 'تقرير فواتير المصروفات'
            color = '#ffc107'
        elif invoice_type == 'payroll':
            data = Payroll.query.order_by(Payroll.date.desc()).all()
            title = 'تقرير كشف الرواتب'
            color = '#17a2b8'
        else:
            flash('نوع الفاتورة غير صحيح', 'error')
            return redirect(url_for('payments_dues'))

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        # حساب المجاميع
        if invoice_type in ['sales', 'purchases']:
            subtotal_amount = sum(item.subtotal for item in data)
            total_discount = sum(item.discount for item in data)
            total_amount = sum(item.total for item in data)
            has_discount = True
        else:
            subtotal_amount = sum(item.amount for item in data)
            total_discount = 0
            total_amount = subtotal_amount
            has_discount = False

        # إنشاء HTML للطباعة
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; margin: 20px; background: white; line-height: 1.5; }}
                .header {{ text-align: center; margin-bottom: 25px; border-bottom: 2px solid {color}; padding-bottom: 15px; }}
                .company-name {{ font-size: 24px; font-weight: bold; color: {color}; margin-bottom: 8px; }}
                .report-title {{ font-size: 18px; color: #333; margin-bottom: 5px; }}
                .print-date {{ color: #666; font-size: 13px; }}
                .summary {{ background: {color}10; border: 1px solid {color}; border-radius: 6px; padding: 12px; margin: 15px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                th, td {{ border: 1px solid #e0e0e0; padding: 10px 6px; text-align: center; font-size: 13px; }}
                th {{ background: {color}; color: white; font-weight: bold; font-size: 14px; }}
                tr:nth-child(even) {{ background-color: #fafafa; }}
                .total-row {{ background: #2c3e50 !important; color: white !important; font-weight: bold; font-size: 15px; }}
                .print-btn {{ position: fixed; top: 10px; right: 10px; background: {color}; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 13px; }}
                @media print {{ .no-print {{ display: none !important; }} body {{ margin: 5px; }} }}
            </style>
        </head>
        <body>
            <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>

            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="report-title">{title}</div>
                <div class="print-date">تاريخ الطباعة: {current_date}</div>
            </div>
        """

        # حساب إحصائيات الدفع
        paid_count = 0
        unpaid_count = 0
        paid_amount = 0
        unpaid_amount = 0

        for item in data:
            payment_status = getattr(item, 'payment_status', 'unpaid')
            item_amount = item.total if hasattr(item, 'total') else item.amount

            if payment_status == 'paid':
                paid_count += 1
                paid_amount += item_amount
            else:
                unpaid_count += 1
                unpaid_amount += item_amount

        # ملخص مبسط ومركز
        html_content += f"""
        <div class="summary">
            <h3 style="color: {color}; margin-bottom: 20px;">📊 ملخص {title}</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0;">
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid {color};">
                    <h4 style="color: {color}; margin: 0 0 10px 0;">📋 العدد الكلي</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0; color: #333;">{len(data)}</p>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid {color};">
                    <h4 style="color: {color}; margin: 0 0 10px 0;">💰 المبلغ الكلي</h4>
                    <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{total_amount:.0f} ريال</p>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid {color};">
                    <h4 style="color: {color}; margin: 0 0 10px 0;">📅 التاريخ</h4>
                    <p style="font-size: 16px; font-weight: bold; margin: 0; color: #333;">{current_date.split()[0]}</p>
                </div>
            </div>
        </div>
        """

        # جدول مبسط ومركز على المعلومات المهمة فقط
        if has_discount:
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th style="width: 15%;">الرقم</th>
                        <th style="width: 35%;">التفاصيل</th>
                        <th style="width: 20%;">التاريخ</th>
                        <th style="width: 20%;">المبلغ النهائي</th>
                        <th style="width: 10%;">الحالة</th>
                    </tr>
                </thead>
                <tbody>
            """

            for item in data:
                if invoice_type == 'sales':
                    details = item.customer.name if item.customer else 'عميل نقدي'
                else:  # purchases
                    details = item.supplier.name if item.supplier else 'مورد نقدي'

                # تحديد حالة الدفع مع رموز بصرية
                payment_status = getattr(item, 'payment_status', 'unpaid')
                status_info = {
                    'paid': ('✅', 'مدفوع', '#28a745'),
                    'partial': ('🟡', 'جزئي', '#ffc107'),
                    'unpaid': ('❌', 'غير مدفوع', '#dc3545'),
                    'overdue': ('⏰', 'متأخر', '#6c757d')
                }.get(payment_status, ('❓', 'غير محدد', '#6c757d'))

                icon, status_text, status_color = status_info

                # تنسيق التاريخ
                date_formatted = item.date.strftime('%d/%m/%Y') if item.date else 'غير محدد'

                html_content += f"""
                    <tr>
                        <td><strong>#{item.id:04d}</strong></td>
                        <td style="text-align: right; padding-right: 15px; font-weight: 500;">{details}</td>
                        <td style="font-weight: 500;">{date_formatted}</td>
                        <td><strong style="color: #2c3e50; font-size: 16px;">{item.total:.0f} ريال</strong></td>
                        <td style="font-size: 18px;">{icon}</td>
                    </tr>
                """

            html_content += f"""
                    <tr class="total-row">
                        <td colspan="3"><strong>🧮 المجموع الإجمالي</strong></td>
                        <td><strong>{total_amount:.0f} ريال</strong></td>
                        <td><strong>{len(data)}</strong></td>
                    </tr>
                </tbody>
            </table>
            """
        else:
            # جدول مبسط للمصروفات والرواتب - المعلومات الأساسية فقط
            if invoice_type == 'expenses':
                html_content += """
                <table>
                    <thead>
                        <tr>
                            <th style="width: 12%;">الرقم</th>
                            <th style="width: 45%;">وصف المصروف</th>
                            <th style="width: 18%;">التاريخ</th>
                            <th style="width: 20%;">المبلغ</th>
                            <th style="width: 5%;">الحالة</th>
                        </tr>
                    </thead>
                    <tbody>
                """
            else:  # payroll
                html_content += """
                <table>
                    <thead>
                        <tr>
                            <th style="width: 12%;">الرقم</th>
                            <th style="width: 40%;">اسم الموظف</th>
                            <th style="width: 18%;">الشهر</th>
                            <th style="width: 20%;">المبلغ</th>
                            <th style="width: 10%;">الحالة</th>
                        </tr>
                    </thead>
                    <tbody>
                """

            for item in data:
                # تحديد حالة الدفع مع رموز واضحة
                payment_status = getattr(item, 'payment_status', 'unpaid')
                status_info = {
                    'paid': '✅',
                    'partial': '🟡',
                    'unpaid': '❌',
                    'overdue': '⏰'
                }.get(payment_status, '❓')

                # تنسيق التاريخ
                date_formatted = item.date.strftime('%d/%m/%Y') if item.date else 'غير محدد'

                if invoice_type == 'expenses':
                    html_content += f"""
                        <tr>
                            <td><strong>#{item.id:04d}</strong></td>
                            <td style="text-align: right; padding-right: 15px; font-weight: 500;">{item.description}</td>
                            <td style="font-weight: 500;">{date_formatted}</td>
                            <td><strong style="color: #2c3e50; font-size: 16px;">{item.amount:.0f} ريال</strong></td>
                            <td style="font-size: 18px;">{status_info}</td>
                        </tr>
                    """
                else:  # payroll
                    employee_name = item.employee.name if item.employee else 'موظف غير محدد'
                    month = getattr(item, 'month', 'غير محدد')
                    html_content += f"""
                        <tr>
                            <td><strong>#{item.id:04d}</strong></td>
                            <td style="text-align: right; padding-right: 15px; font-weight: 500;">{employee_name}</td>
                            <td style="font-weight: 500;">{month}</td>
                            <td><strong style="color: #2c3e50; font-size: 16px;">{item.amount:.0f} ريال</strong></td>
                            <td style="font-size: 18px;">{status_info}</td>
                        </tr>
                    """

            html_content += f"""
                    <tr class="total-row">
                        <td colspan="3"><strong>🧮 المجموع الإجمالي</strong></td>
                        <td><strong>{total_amount:.0f} ريال</strong></td>
                        <td><strong>{len(data)}</strong></td>
                    </tr>
                </tbody>
            </table>
            """

        # خاتمة مختصرة ومهنية
        html_content += f"""
            <div style="text-align: center; margin-top: 30px; padding: 15px; border-top: 2px solid {color};">
                <p style="color: #666; margin: 0; font-size: 14px;">
                    <strong>نظام المحاسبة المتكامل</strong> |
                    {len(data)} عنصر |
                    {total_amount:.0f} ريال |
                    {current_date.split()[0]}
                </p>
            </div>

            <script>
                window.onload = function() {{
                    setTimeout(function() {{ window.print(); }}, 300);
                }};
            </script>
        </body>
        </html>
        """

        return html_content

    except Exception as e:
        logger.error(f"❌ خطأ في طباعة الفواتير: {e}")
        flash('حدث خطأ في الطباعة', 'error')
        return redirect(url_for('payments_dues'))

@app.route('/api/sales/create', methods=['POST'])
@login_required
def create_sale():
    """إنشاء مبيعة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('subtotal') or not data.get('total'):
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # Generate unique invoice number
        last_sale = Sale.query.order_by(Sale.id.desc()).first()
        next_number = (last_sale.id + 1) if last_sale else 1
        invoice_number = f"INV-{next_number:06d}"

        # إنشاء مبيعة جديدة
        new_sale = Sale(
            invoice_number=invoice_number,
            customer_id=data.get('customer_id') if data.get('customer_id') else None,
            subtotal=float(data.get('subtotal', 0)),
            discount=float(data.get('discount', 0)),
            tax_rate=float(data.get('tax_rate', 15.0)),
            tax_amount=float(data.get('tax_amount', 0)),
            total=float(data.get('total', 0)),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else datetime.utcnow(),
            notes=data.get('notes', '')
        )

        db.session.add(new_sale)
        db.session.flush()  # Get the sale ID

        # Handle sale items if provided
        items_data = data.get('items', [])
        total_calculated = 0

        for item_data in items_data:
            if not item_data.get('product_name') or not item_data.get('quantity'):
                continue

            quantity = float(item_data.get('quantity', 1))
            unit_price = float(item_data.get('unit_price', 0))
            item_discount = float(item_data.get('discount', 0))
            total_price = (quantity * unit_price) - item_discount

            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=item_data.get('product_id'),
                product_name=item_data.get('product_name'),
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount=item_discount,
                notes=item_data.get('notes', '')
            )

            db.session.add(sale_item)
            total_calculated += total_price

            # Update product stock if product_id is provided
            if item_data.get('product_id'):
                product = Product.query.get(item_data.get('product_id'))
                if product:
                    product.stock_quantity = max(0, product.stock_quantity - quantity)

        # If items were provided, update the sale total
        if items_data:
            new_sale.subtotal = total_calculated + new_sale.discount
            new_sale.total = total_calculated

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم حفظ المبيعة بنجاح',
            'sale_id': new_sale.id,
            'invoice_number': new_sale.invoice_number
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ المبيعة: {str(e)}'})

@app.route('/api/purchases/create', methods=['POST'])
@login_required
def create_purchase():
    """إنشاء مشتريات جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('subtotal') or not data.get('total'):
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # إنشاء مشتريات جديدة
        new_purchase = Purchase(
            supplier_id=data.get('supplier_id') if data.get('supplier_id') else None,
            subtotal=float(data.get('subtotal', 0)),
            discount=float(data.get('discount', 0)),
            total=float(data.get('total', 0)),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else datetime.utcnow(),
            notes=data.get('notes', '')
        )

        db.session.add(new_purchase)
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم حفظ المشتريات بنجاح', 'purchase_id': new_purchase.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ المشتريات: {str(e)}'})

@app.route('/api/expenses/create', methods=['POST'])
@login_required
def create_expense():
    """إنشاء مصروف جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('amount') or not data.get('description'):
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # Generate unique expense number
        last_expense = Expense.query.order_by(Expense.id.desc()).first()
        next_number = (last_expense.id + 1) if last_expense else 1
        expense_number = f"EXP-{next_number:06d}"

        # إنشاء مصروف جديد
        new_expense = Expense(
            expense_number=expense_number,
            description=data.get('description'),
            amount=float(data.get('amount', 0)),
            expense_type=data.get('expense_type', 'general'),
            category=data.get('category', 'general'),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else datetime.utcnow(),
            reference=data.get('reference', ''),
            vendor=data.get('vendor', ''),
            payment_method=data.get('payment_method', 'cash'),
            notes=data.get('notes', '')
        )

        db.session.add(new_expense)
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم حفظ المصروف بنجاح', 'expense_id': new_expense.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ المصروف: {str(e)}'})

@app.route('/print_expense/<int:expense_id>')
@login_required
def print_expense(expense_id):
    """طباعة مصروف"""
    try:
        expense = Expense.query.get_or_404(expense_id)

        # Generate expense number if not exists
        if not expense.expense_number:
            expense.expense_number = f"EXP-{expense.id:06d}"
            db.session.commit()

        # Company information
        company_info = {
            'name': 'شركة المحاسبة المتكاملة',
            'name_en': 'Integrated Accounting Company',
            'address': 'الرياض، المملكة العربية السعودية',
            'phone': '+966 11 123 4567',
            'email': 'info@accounting.com',
            'tax_number': '123456789012345'
        }

        return render_template('print_expense.html',
                             expense=expense,
                             company=company_info,
                             print_date=datetime.now())

    except Exception as e:
        flash(f'خطأ في طباعة المصروف: {str(e)}', 'error')
        return redirect(url_for('expenses'))

@app.route('/api/expenses/delete/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """حذف مصروف"""
    try:
        expense = Expense.query.get_or_404(expense_id)

        # Check if expense is paid - prevent deletion of paid expenses
        if expense.payment_status == 'paid' and expense.paid_amount > 0:
            return jsonify({
                'success': False,
                'message': 'لا يمكن حذف مصروف مدفوع. يرجى إلغاء الدفعة أولاً.'
            })

        # Store expense info for response
        expense_number = expense.expense_number or f"EXP-{expense.id:06d}"

        # Delete the expense
        db.session.delete(expense)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'تم حذف المصروف {expense_number} بنجاح'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حذف المصروف: {str(e)}'
        })

@app.route('/api/expenses/update/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    """تحديث مصروف"""
    try:
        expense = Expense.query.get_or_404(expense_id)
        data = request.get_json()

        # Check if expense is paid - prevent editing of paid expenses
        if expense.payment_status == 'paid' and expense.paid_amount > 0:
            return jsonify({
                'success': False,
                'message': 'لا يمكن تعديل مصروف مدفوع. يرجى إلغاء الدفعة أولاً.'
            })

        # Update expense fields
        if 'description' in data:
            expense.description = data.get('description')
        if 'amount' in data:
            expense.amount = float(data.get('amount', 0))
        if 'expense_type' in data:
            expense.expense_type = data.get('expense_type')
        if 'category' in data:
            expense.category = data.get('category')
        if 'date' in data:
            expense.date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else expense.date
        if 'reference' in data:
            expense.reference = data.get('reference', '')
        if 'vendor' in data:
            expense.vendor = data.get('vendor', '')
        if 'payment_method' in data:
            expense.payment_method = data.get('payment_method')
        if 'notes' in data:
            expense.notes = data.get('notes', '')

        db.session.commit()

        expense_number = expense.expense_number or f"EXP-{expense.id:06d}"
        return jsonify({
            'success': True,
            'message': f'تم تحديث المصروف {expense_number} بنجاح'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في تحديث المصروف: {str(e)}'
        })

@app.route('/api/expenses/search', methods=['GET'])
@login_required
def search_expenses():
    """البحث والتصفية في المصروفات"""
    try:
        # Get search parameters
        search_term = request.args.get('search', '').strip()
        expense_type = request.args.get('expense_type', '')
        payment_method = request.args.get('payment_method', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        min_amount = request.args.get('min_amount', '')
        max_amount = request.args.get('max_amount', '')

        # Start with base query
        query = Expense.query

        # Apply search term filter
        if search_term:
            query = query.filter(
                db.or_(
                    Expense.description.contains(search_term),
                    Expense.expense_number.contains(search_term),
                    Expense.vendor.contains(search_term),
                    Expense.reference.contains(search_term)
                )
            )

        # Apply expense type filter
        if expense_type:
            query = query.filter(Expense.expense_type == expense_type)

        # Apply payment method filter
        if payment_method:
            query = query.filter(Expense.payment_method == payment_method)

        # Apply date range filter
        if date_from:
            query = query.filter(Expense.date >= datetime.strptime(date_from, '%Y-%m-%d'))
        if date_to:
            query = query.filter(Expense.date <= datetime.strptime(date_to, '%Y-%m-%d'))

        # Apply amount range filter
        if min_amount:
            query = query.filter(Expense.amount >= float(min_amount))
        if max_amount:
            query = query.filter(Expense.amount <= float(max_amount))

        # Execute query
        expenses = query.order_by(Expense.date.desc()).all()

        # Format results
        results = []
        for expense in expenses:
            results.append({
                'id': expense.id,
                'expense_number': expense.expense_number or f"EXP-{expense.id:06d}",
                'description': expense.description,
                'amount': expense.amount,
                'expense_type': expense.expense_type or expense.category,
                'date': expense.date.strftime('%Y-%m-%d') if expense.date else '',
                'payment_method': expense.payment_method,
                'vendor': expense.vendor,
                'reference': expense.reference,
                'payment_status': expense.payment_status,
                'notes': expense.notes
            })

        return jsonify({
            'success': True,
            'expenses': results,
            'count': len(results)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في البحث: {str(e)}'
        })

@app.route('/api/expenses/export')
@login_required
def export_expenses():
    """تصدير المصروفات إلى Excel"""
    try:
        # Get filter parameters
        expense_type = request.args.get('expense_type', '')
        payment_method = request.args.get('payment_method', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')

        # Build query with filters
        query = Expense.query

        if expense_type:
            query = query.filter(Expense.expense_type == expense_type)
        if payment_method:
            query = query.filter(Expense.payment_method == payment_method)
        if date_from:
            query = query.filter(Expense.date >= datetime.strptime(date_from, '%Y-%m-%d'))
        if date_to:
            query = query.filter(Expense.date <= datetime.strptime(date_to, '%Y-%m-%d'))

        expenses = query.order_by(Expense.date.desc()).all()

        # Create CSV content
        import io
        import csv

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'رقم المصروف', 'التاريخ', 'نوع المصروف', 'الوصف',
            'المبلغ', 'طريقة الدفع', 'المورد', 'رقم المرجع',
            'حالة الدفع', 'ملاحظات'
        ])

        # Write data
        for expense in expenses:
            writer.writerow([
                expense.expense_number or f"EXP-{expense.id:06d}",
                expense.date.strftime('%Y-%m-%d') if expense.date else '',
                expense.expense_type or expense.category or '',
                expense.description or '',
                expense.amount or 0,
                expense.payment_method or '',
                expense.vendor or '',
                expense.reference or '',
                'مدفوع' if expense.payment_status == 'paid' else 'غير مدفوع',
                expense.notes or ''
            ])

        # Prepare response
        output.seek(0)

        from flask import make_response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=expenses_{datetime.now().strftime("%Y%m%d")}.csv'

        return response

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في التصدير: {str(e)}'
        })

@app.route('/api/save_expense', methods=['POST'])
@login_required
def save_expense():
    """حفظ مصروف جديد - endpoint للتوافق مع الواجهة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('amount') or not data.get('description'):
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # إنشاء مصروف جديد
        new_expense = Expense(
            description=data.get('description'),
            amount=float(data.get('amount', 0)),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else datetime.utcnow(),
            category=data.get('expense_type', 'general'),
            notes=data.get('reference', '')
        )

        db.session.add(new_expense)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم حفظ المصروف بنجاح',
            'expense_id': new_expense.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ المصروف: {str(e)}'})

@app.route('/api/employees/create', methods=['POST'])
@login_required
def create_employee():
    """إنشاء موظف جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get('name') or not data.get('salary'):
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # إنشاء موظف جديد
        new_employee = Employee(
            name=data.get('name'),
            position=data.get('position', ''),
            salary=float(data.get('salary', 0)),
            hire_date=datetime.strptime(data.get('hire_date'), '%Y-%m-%d') if data.get('hire_date') else datetime.utcnow(),
            phone=data.get('phone', ''),
            email=data.get('email', '')
        )

        db.session.add(new_employee)
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم حفظ الموظف بنجاح', 'employee_id': new_employee.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حفظ الموظف: {str(e)}'})

@app.route('/api/sales/delete/<int:sale_id>', methods=['DELETE'])
@login_required
def delete_sale(sale_id):
    """حذف مبيعة"""
    try:
        sale = Sale.query.get_or_404(sale_id)
        db.session.delete(sale)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف المبيعة بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حذف المبيعة: {str(e)}'})

@app.route('/api/purchases/delete/<int:purchase_id>', methods=['DELETE'])
@login_required
def delete_purchase(purchase_id):
    """حذف مشتريات"""
    try:
        purchase = Purchase.query.get_or_404(purchase_id)
        db.session.delete(purchase)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف فاتورة المشتريات بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حذف فاتورة المشتريات: {str(e)}'})

# delete_expense function already defined above - removing duplicate

# ============================================================================
# ADVANCED AUTO-SAVE SYSTEM API ENDPOINTS
# ============================================================================

@app.route('/api/batch/process', methods=['POST'])
@login_required
def process_batch_operations():
    """معالجة العمليات المجمعة"""
    try:
        data = request.get_json()
        operations = data.get('operations', [])

        if not operations:
            return jsonify({'success': False, 'message': 'لا توجد عمليات للمعالجة'})

        results = []

        for operation in operations:
            try:
                result = None
                op_type = operation.get('type')
                op_data = operation.get('data', {})
                target_id = operation.get('targetId')

                if op_type == 'save':
                    # تحديد نوع البيانات وحفظها
                    if 'customer_id' in op_data or 'subtotal' in op_data:
                        # مبيعة
                        sale = Sale(
                            customer_id=op_data.get('customer_id'),
                            subtotal=float(op_data.get('subtotal', 0)),
                            discount=float(op_data.get('discount', 0)),
                            total=float(op_data.get('total', 0)),
                            date=datetime.strptime(op_data.get('date'), '%Y-%m-%d') if op_data.get('date') else datetime.utcnow(),
                            notes=op_data.get('notes', '')
                        )
                        db.session.add(sale)
                        db.session.flush()
                        result = {'id': sale.id, 'type': 'sale'}

                    elif 'supplier_id' in op_data:
                        # مشتريات
                        purchase = Purchase(
                            supplier_id=op_data.get('supplier_id'),
                            subtotal=float(op_data.get('subtotal', 0)),
                            discount=float(op_data.get('discount', 0)),
                            total=float(op_data.get('total', 0)),
                            date=datetime.strptime(op_data.get('date'), '%Y-%m-%d') if op_data.get('date') else datetime.utcnow(),
                            notes=op_data.get('notes', '')
                        )
                        db.session.add(purchase)
                        db.session.flush()
                        result = {'id': purchase.id, 'type': 'purchase'}

                    elif 'description' in op_data and 'amount' in op_data:
                        # مصروف
                        expense = Expense(
                            description=op_data.get('description'),
                            amount=float(op_data.get('amount', 0)),
                            date=datetime.strptime(op_data.get('date'), '%Y-%m-%d') if op_data.get('date') else datetime.utcnow(),
                            category=op_data.get('type', 'general'),
                            notes=op_data.get('notes', '')
                        )
                        db.session.add(expense)
                        db.session.flush()
                        result = {'id': expense.id, 'type': 'expense'}

                    elif 'name' in op_data and 'salary' in op_data:
                        # موظف
                        employee = Employee(
                            name=op_data.get('name'),
                            position=op_data.get('position', ''),
                            salary=float(op_data.get('salary', 0)),
                            hire_date=datetime.strptime(op_data.get('hire_date'), '%Y-%m-%d') if op_data.get('hire_date') else datetime.utcnow(),
                            phone=op_data.get('phone', ''),
                            email=op_data.get('email', '')
                        )
                        db.session.add(employee)
                        db.session.flush()
                        result = {'id': employee.id, 'type': 'employee'}

                elif op_type == 'delete':
                    # حذف حسب النوع
                    if target_id:
                        # محاولة حذف من جميع الجداول
                        deleted = False
                        for model in [Sale, Purchase, Expense, Employee]:
                            try:
                                item = model.query.get(target_id)
                                if item:
                                    db.session.delete(item)
                                    deleted = True
                                    break
                            except:
                                continue

                        if not deleted:
                            raise Exception(f'لم يتم العثور على العنصر {target_id}')

                        result = {'deleted_id': target_id}

                results.append({
                    'success': True,
                    'operation_id': operation.get('id'),
                    'result': result
                })

            except Exception as op_error:
                results.append({
                    'success': False,
                    'operation_id': operation.get('id'),
                    'error': str(op_error)
                })

        # حفظ جميع التغييرات
        db.session.commit()

        successful_ops = len([r for r in results if r['success']])
        total_ops = len(results)

        return jsonify({
            'success': True,
            'message': f'تم معالجة {successful_ops}/{total_ops} عملية بنجاح',
            'results': results,
            'summary': {
                'total': total_ops,
                'successful': successful_ops,
                'failed': total_ops - successful_ops
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في معالجة العمليات المجمعة: {str(e)}'})

@app.route('/api/auto-save/status', methods=['GET'])
@login_required
def get_auto_save_status():
    """الحصول على حالة نظام الحفظ التلقائي"""
    try:
        # إحصائيات النظام
        stats = {
            'sales_count': Sale.query.count(),
            'purchases_count': Purchase.query.count(),
            'expenses_count': Expense.query.count(),
            'employees_count': Employee.query.count(),
            'last_activity': datetime.utcnow().isoformat(),
            'system_status': 'active'
        }

        return jsonify({'success': True, 'stats': stats})

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب الحالة: {str(e)}'})

@app.route('/api/forms/recover/<form_id>', methods=['GET'])
@login_required
def recover_form_data(form_id):
    """استعادة بيانات النموذج المحفوظة"""
    try:
        # هنا يمكن إضافة منطق استعادة البيانات من قاعدة البيانات
        # أو من ملفات مؤقتة حسب الحاجة

        return jsonify({
            'success': True,
            'message': 'تم استعادة البيانات',
            'data': {}  # البيانات المستعادة
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في استعادة البيانات: {str(e)}'})

# ============================================================================
# PAYMENT INTEGRATION SYSTEM API ENDPOINTS
# ============================================================================

@app.route('/api/payments/notify', methods=['POST'])
@login_required
def notify_payment_system():
    """إشعار نظام المدفوعات بالتغييرات"""
    try:
        data = request.get_json()
        event_type = data.get('event_type')
        event_data = data.get('data', {})

        # تسجيل الحدث في قاعدة البيانات أو ملف log
        print(f"📢 إشعار نظام المدفوعات: {event_type}")

        # يمكن إضافة منطق معالجة الأحداث هنا
        # مثل تحديث حالة الدفع، إرسال إشعارات، إلخ

        return jsonify({
            'success': True,
            'message': 'تم استلام الإشعار',
            'event_id': f"event_{int(time.time())}"
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في معالجة الإشعار: {str(e)}'})

@app.route('/api/payments/check-updates', methods=['GET'])
@login_required
def check_payment_updates():
    """فحص التحديثات في نظام المدفوعات"""
    try:
        last_update = request.headers.get('X-Last-Update', '0')
        current_time = int(time.time())

        # فحص التحديثات منذ آخر مرة
        # هنا يمكن إضافة منطق فحص التغييرات في قاعدة البيانات

        # مثال على التحديثات
        updates = []
        has_updates = False

        # يمكن إضافة منطق فحص التغييرات الفعلية هنا

        return jsonify({
            'success': True,
            'hasUpdates': has_updates,
            'updates': updates,
            'timestamp': str(current_time)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في فحص التحديثات: {str(e)}'})

@app.route('/api/<string:module>/update-payment-status', methods=['POST'])
@login_required
def update_payment_status(module):
    """تحديث حالة الدفع لفاتورة معينة"""
    try:
        data = request.get_json()
        item_id = data.get('id')
        payment_status = data.get('payment_status')

        if not item_id or not payment_status:
            return jsonify({'success': False, 'message': 'البيانات المطلوبة مفقودة'})

        # تحديد النموذج حسب النوع
        model_map = {
            'sales': Sale,
            'purchases': Purchase,
            'expenses': Expense,
            'payroll': Employee  # أو نموذج Payroll إذا كان موجود
        }

        model = model_map.get(module)
        if not model:
            return jsonify({'success': False, 'message': 'نوع الوحدة غير صحيح'})

        # العثور على العنصر وتحديثه
        item = model.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': 'العنصر غير موجود'})

        # تحديث حالة الدفع (إضافة الحقل إذا لم يكن موجود)
        if hasattr(item, 'payment_status'):
            item.payment_status = payment_status

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم تحديث حالة الدفع بنجاح',
            'item_id': item_id,
            'new_status': payment_status
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في تحديث حالة الدفع: {str(e)}'})

@app.route('/api/<string:module>/summary', methods=['GET'])
@login_required
def get_module_summary(module):
    """الحصول على ملخص الوحدة مع حالات الدفع"""
    try:
        model_map = {
            'sales': Sale,
            'purchases': Purchase,
            'expenses': Expense
        }

        model = model_map.get(module)
        if not model:
            return jsonify({'success': False, 'message': 'نوع الوحدة غير صحيح'})

        # حساب الإحصائيات حسب نوع النموذج
        if module == 'expenses':
            # للمصروفات نستخدم حقل amount بدلاً من total
            total_amount = db.session.query(db.func.sum(model.amount)).scalar() or 0
            if hasattr(model, 'payment_status'):
                paid_items = model.query.filter_by(payment_status='paid').all()
                paid_amount = sum(item.amount for item in paid_items)
            else:
                paid_amount = 0
        else:
            # للمبيعات والمشتريات نستخدم حقل total
            total_amount = db.session.query(db.func.sum(model.total)).scalar() or 0
            if hasattr(model, 'payment_status'):
                paid_items = model.query.filter_by(payment_status='paid').all()
                paid_amount = sum(item.total for item in paid_items)
            else:
                paid_amount = 0

        total_count = model.query.count()
        pending_amount = total_amount - paid_amount

        summary = {
            f'total-{module}': total_amount,
            f'paid-{module}': paid_amount,
            f'pending-{module}': pending_amount,
            'count': total_count
        }

        return jsonify({
            'success': True,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب الملخص: {str(e)}'})

@app.route('/api/sales/list', methods=['GET'])
@login_required
def get_sales_list():
    """جلب قائمة المبيعات للطباعة"""
    try:
        sales = Sale.query.all()
        sales_data = []

        for sale in sales:
            customer_name = sale.customer.name if sale.customer else 'عميل غير محدد'
            sales_data.append({
                'id': sale.id,
                'date': sale.date.isoformat() if sale.date else None,
                'customer': {'name': customer_name},
                'subtotal': sale.subtotal,
                'discount': sale.discount,
                'total': sale.total,
                'payment_status': getattr(sale, 'payment_status', 'unpaid'),
                'paid_amount': getattr(sale, 'paid_amount', 0),
                'payment_method': getattr(sale, 'payment_method', None)
            })

        return jsonify({
            'success': True,
            'sales': sales_data,
            'count': len(sales_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب المبيعات: {str(e)}'})

@app.route('/sales/print/<int:sale_id>')
@login_required
def print_sale(sale_id):
    """طباعة فاتورة مبيعات"""
    try:
        sale = Sale.query.get_or_404(sale_id)

        # Generate invoice number if not exists
        if not hasattr(sale, 'invoice_number') or not sale.invoice_number:
            sale.invoice_number = f"INV-{sale.id:06d}"
            db.session.commit()

        # Company information
        company_info = {
            'name': 'شركة المحاسبة المتكاملة',
            'name_en': 'Integrated Accounting Company',
            'address': 'الرياض، المملكة العربية السعودية',
            'phone': '+966 11 123 4567',
            'email': 'info@accounting.com',
            'tax_number': '123456789012345'
        }

        return render_template('print_sale.html',
                             sale=sale,
                             company=company_info,
                             print_date=datetime.now())

    except Exception as e:
        flash(f'خطأ في طباعة الفاتورة: {str(e)}', 'error')
        return redirect(url_for('sales'))

# delete_sale function already defined above - removing duplicate

@app.route('/api/sales/update/<int:sale_id>', methods=['PUT'])
@login_required
def update_sale(sale_id):
    """تحديث فاتورة مبيعات"""
    try:
        sale = Sale.query.get_or_404(sale_id)
        data = request.get_json()

        # Check if sale has payments
        if sale.paid_amount and sale.paid_amount > 0:
            return jsonify({
                'success': False,
                'message': 'لا يمكن تعديل فاتورة تحتوي على مدفوعات. يرجى إلغاء المدفوعات أولاً.'
            })

        # Update sale fields
        if 'customer_id' in data:
            sale.customer_id = data.get('customer_id') if data.get('customer_id') else None
        if 'subtotal' in data:
            sale.subtotal = float(data.get('subtotal', 0))
        if 'discount' in data:
            sale.discount = float(data.get('discount', 0))
        if 'tax_rate' in data:
            sale.tax_rate = float(data.get('tax_rate', 15.0))
        if 'tax_amount' in data:
            sale.tax_amount = float(data.get('tax_amount', 0))
        if 'total' in data:
            sale.total = float(data.get('total', 0))
        if 'date' in data:
            sale.date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else sale.date
        if 'notes' in data:
            sale.notes = data.get('notes', '')

        # Handle sale items update if provided
        if 'items' in data:
            # Delete existing items
            SaleItem.query.filter_by(sale_id=sale.id).delete()

            # Add new items
            items_data = data.get('items', [])
            total_calculated = 0

            for item_data in items_data:
                if not item_data.get('product_name') or not item_data.get('quantity'):
                    continue

                quantity = float(item_data.get('quantity', 1))
                unit_price = float(item_data.get('unit_price', 0))
                item_discount = float(item_data.get('discount', 0))
                total_price = (quantity * unit_price) - item_discount

                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item_data.get('product_id'),
                    product_name=item_data.get('product_name'),
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    discount=item_discount,
                    notes=item_data.get('notes', '')
                )

                db.session.add(sale_item)
                total_calculated += total_price

            # Update sale total if items were provided
            if items_data:
                sale.subtotal = total_calculated + sale.discount
                sale.total = total_calculated + sale.tax_amount

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'تم تحديث الفاتورة {sale.invoice_number} بنجاح'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في تحديث الفاتورة: {str(e)}'
        })

@app.route('/api/products/list', methods=['GET'])
@login_required
def get_products_list():
    """جلب قائمة المنتجات"""
    try:
        products = Product.query.filter_by(is_active=True).all()
        products_data = []

        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock_quantity': product.stock_quantity,
                'barcode': product.barcode,
                'category': product.category
            })

        return jsonify({
            'success': True,
            'products': products_data,
            'count': len(products_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب المنتجات: {str(e)}'})

@app.route('/api/purchases/list', methods=['GET'])
@login_required
def get_purchases_list():
    """جلب قائمة المشتريات للطباعة"""
    try:
        purchases = Purchase.query.all()
        purchases_data = []

        for purchase in purchases:
            supplier_name = purchase.supplier.name if purchase.supplier else 'مورد غير محدد'
            purchases_data.append({
                'id': purchase.id,
                'date': purchase.date.isoformat() if purchase.date else None,
                'supplier': {'name': supplier_name},
                'subtotal': purchase.subtotal,
                'discount': purchase.discount,
                'total': purchase.total,
                'payment_status': getattr(purchase, 'payment_status', 'unpaid'),
                'paid_amount': getattr(purchase, 'paid_amount', 0),
                'payment_method': getattr(purchase, 'payment_method', None)
            })

        return jsonify({
            'success': True,
            'purchases': purchases_data,
            'count': len(purchases_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب المشتريات: {str(e)}'})

@app.route('/api/expenses/list', methods=['GET'])
@login_required
def get_expenses_list():
    """جلب قائمة المصروفات للطباعة"""
    try:
        expenses = Expense.query.all()
        expenses_data = []

        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'date': expense.date.isoformat() if expense.date else None,
                'description': expense.description,
                'category': expense.category,
                'amount': expense.amount,
                'payment_status': getattr(expense, 'payment_status', 'unpaid'),
                'paid_amount': getattr(expense, 'paid_amount', 0),
                'payment_method': getattr(expense, 'payment_method', None)
            })

        return jsonify({
            'success': True,
            'expenses': expenses_data,
            'count': len(expenses_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب المصروفات: {str(e)}'})

@app.route('/api/payroll/list', methods=['GET'])
@login_required
def get_payroll_list():
    """جلب قائمة الرواتب للطباعة"""
    try:
        payrolls = Payroll.query.all()
        payrolls_data = []

        for payroll in payrolls:
            employee_name = payroll.employee.name if payroll.employee else 'موظف غير محدد'
            payrolls_data.append({
                'id': payroll.id,
                'date': payroll.date.isoformat() if payroll.date else None,
                'employee': {'name': employee_name},
                'month': payroll.month,
                'amount': payroll.amount,
                'payment_status': getattr(payroll, 'payment_status', 'unpaid'),
                'paid_amount': getattr(payroll, 'paid_amount', 0),
                'payment_method': getattr(payroll, 'payment_method', None)
            })

        return jsonify({
            'success': True,
            'payrolls': payrolls_data,
            'count': len(payrolls_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب الرواتب: {str(e)}'})

if __name__ == '__main__':
    print("🚀 تشغيل النظام المحاسبي المتكامل...")
    print("🏠 الشاشة الرئيسية: http://localhost:5000")
    print("📊 لوحة التحكم: http://localhost:5000/dashboard")
    print("💳 المدفوعات والمستحقات: http://localhost:5000/payments_dues")
    print("💰 النظام يدعم الحفظ التلقائي والربط المباشر")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
