#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق المحاسبة الويب - Flask Web Accounting Application
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import json

# إنشاء التطبيق
app = Flask(__name__)

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
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)
    
    # العلاقات
    product = db.relationship('Product', backref='sale_items')

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
    
    return render_template('dashboard.html',
                         daily_sales=daily_sales,
                         monthly_sales=monthly_sales,
                         total_products=total_products,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales)

@app.route('/products')
@login_required
def products():
    """صفحة إدارة المنتجات"""
    search = request.args.get('search', '')
    
    query = Product.query
    if search:
        query = query.filter(
            db.or_(
                Product.product_name.contains(search),
                Product.product_code.contains(search),
                Product.category.contains(search)
            )
        )
    
    products = query.order_by(Product.product_name).all()
    return render_template('products.html', products=products, search=search)

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

@app.route('/new_sale')
@login_required
def new_sale():
    """صفحة فاتورة مبيعات جديدة"""
    branches = Branch.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True).all()
    
    return render_template('new_sale.html', branches=branches, products=products)

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

        # إضافة عناصر الفاتورة
        for item in data['items']:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item.get('product_id'),
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
def api_generate_invoice_number():
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

# الصفحات الإضافية
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

    # بيانات تجريبية للتقارير
    report_data = {
        'total_sales': 45000.00,
        'total_purchases': 20000.00,
        'total_expenses': 8000.00,
        'total_salaries': 12000.00,
        'total_vat': 6750.00,
        'net_profit': 5000.00
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

@app.route('/payments_dues')
@login_required
def payments_dues():
    """صفحة المدفوعات والمستحقات"""

    # بيانات تجريبية للمدفوعات والمستحقات
    summary_data = {
        'total_amount': 41200.00,
        'total_paid': 20200.00,
        'total_due': 21000.00,
        'unpaid_count': 4
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

    return render_template('payments_dues.html',
                         summary_data=summary_data,
                         account_types=account_types,
                         payment_statuses=payment_statuses,
                         payment_methods=payment_methods)

@app.route('/tax_management')
@login_required
def tax_management():
    """صفحة إدارة الضرائب"""

    # بيانات تجريبية للضرائب
    tax_statistics = {
        'total_collected': 15750.00,
        'vat_collected': 13500.00,
        'other_taxes': 2250.00,
        'invoices_count': 1250
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

def create_default_data():
    """إنشاء البيانات الافتراضية"""

    # إنشاء مستخدم المدير
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
        print("تم إنشاء المستخدم الافتراضي: admin / admin123")
    
    # إنشاء الفروع
    branches_data = [
        ('PI', 'PLACE INDIA', 'PLACE INDIA'),
        ('CT', 'CHINA TOWN', 'CHINA TOWN')
    ]
    
    for code, name_ar, name_en in branches_data:
        branch = Branch.query.filter_by(branch_code=code).first()
        if not branch:
            branch = Branch(
                branch_code=code,
                branch_name=name_ar,
                branch_name_en=name_en
            )
            db.session.add(branch)
    
    db.session.commit()

@app.route('/advanced_expenses')
@login_required
def advanced_expenses():
    """صفحة المصروفات المتقدمة"""

    # بيانات تجريبية للمصروفات
    summary_data = {
        'total_expenses': 30500.00,
        'paid_expenses': 24300.00,
        'pending_expenses': 6200.00,
        'expenses_count': 6
    }

    return render_template('advanced_expenses.html', summary_data=summary_data)

@app.route('/employee_payroll')
@login_required
def employee_payroll():
    """صفحة إدارة الموظفين والرواتب"""

    # بيانات تجريبية للملخص
    summary_data = {
        'total_employees': 5,
        'paid_salaries': 45000.00,
        'outstanding_salaries': 15000.00,
        'overdue_count': 2
    }

    return render_template('employee_payroll.html', summary_data=summary_data)

@app.route('/purchases')
@login_required
def purchases():
    """صفحة إدارة المشتريات"""

    # بيانات تجريبية للملخص
    summary_data = {
        'total_purchases': 6225.50,
        'paid_purchases': 3852.50,
        'pending_purchases': 2373.00,
        'invoices_count': 3
    }

    # الموردين
    suppliers = [
        {'id': 1, 'name_ar': 'شركة المواد الغذائية المتحدة', 'name_en': 'United Food Materials Company'},
        {'id': 2, 'name_ar': 'مؤسسة الخضار والفواكه', 'name_en': 'Vegetables & Fruits Est.'},
        {'id': 3, 'name_ar': 'شركة اللحوم الطازجة', 'name_en': 'Fresh Meat Company'},
        {'id': 4, 'name_ar': 'مصنع الألبان الذهبية', 'name_en': 'Golden Dairy Factory'},
        {'id': 5, 'name_ar': 'شركة التوابل والبهارات', 'name_en': 'Spices & Seasonings Co.'}
    ]

    # المنتجات
    products = [
        {'id': 1, 'name_ar': 'أرز بسمتي', 'name_en': 'Basmati Rice', 'unit_ar': 'كيس 25 كيلو', 'unit_en': '25kg Bag', 'cost_price': 85.00},
        {'id': 2, 'name_ar': 'زيت الطبخ', 'name_en': 'Cooking Oil', 'unit_ar': 'جالون 4 لتر', 'unit_en': '4L Gallon', 'cost_price': 32.50},
        {'id': 3, 'name_ar': 'دجاج طازج', 'name_en': 'Fresh Chicken', 'unit_ar': 'كيلو', 'unit_en': 'Kg', 'cost_price': 18.00},
        {'id': 4, 'name_ar': 'طماطم', 'name_en': 'Tomatoes', 'unit_ar': 'كيلو', 'unit_en': 'Kg', 'cost_price': 4.50},
        {'id': 5, 'name_ar': 'بصل', 'name_en': 'Onions', 'unit_ar': 'كيلو', 'unit_en': 'Kg', 'cost_price': 3.20},
        {'id': 6, 'name_ar': 'لحم بقري', 'name_en': 'Beef', 'unit_ar': 'كيلو', 'unit_en': 'Kg', 'cost_price': 45.00},
        {'id': 7, 'name_ar': 'حليب طازج', 'name_en': 'Fresh Milk', 'unit_ar': 'لتر', 'unit_en': 'Liter', 'cost_price': 6.50},
        {'id': 8, 'name_ar': 'دقيق أبيض', 'name_en': 'White Flour', 'unit_ar': 'كيس 50 كيلو', 'unit_en': '50kg Bag', 'cost_price': 95.00}
    ]

    return render_template('purchases.html',
                         summary_data=summary_data,
                         suppliers=suppliers,
                         products=products)

@app.route('/financial_statements')
@login_required
def financial_statements():
    """صفحة القوائم المالية"""

    # بيانات تجريبية للحسابات
    accounts_data = {
        'assets': {
            'cash': {'name_ar': 'النقدية', 'name_en': 'Cash', 'balance': 45000.00},
            'bank': {'name_ar': 'البنك', 'name_en': 'Bank', 'balance': 125000.00},
            'accounts_receivable': {'name_ar': 'حسابات العملاء', 'name_en': 'Accounts Receivable', 'balance': 35000.00},
            'inventory': {'name_ar': 'المخزون', 'name_en': 'Inventory', 'balance': 85000.00},
            'equipment': {'name_ar': 'المعدات', 'name_en': 'Equipment', 'balance': 150000.00},
            'furniture': {'name_ar': 'الأثاث', 'name_en': 'Furniture', 'balance': 25000.00}
        },
        'liabilities': {
            'accounts_payable': {'name_ar': 'حسابات الموردين', 'name_en': 'Accounts Payable', 'balance': 28000.00},
            'salaries_payable': {'name_ar': 'الرواتب المستحقة', 'name_en': 'Salaries Payable', 'balance': 15000.00},
            'vat_payable': {'name_ar': 'ضريبة القيمة المضافة المستحقة', 'name_en': 'VAT Payable', 'balance': 8500.00},
            'loans': {'name_ar': 'القروض', 'name_en': 'Loans', 'balance': 75000.00}
        },
        'equity': {
            'capital': {'name_ar': 'رأس المال', 'name_en': 'Capital', 'balance': 200000.00},
            'retained_earnings': {'name_ar': 'الأرباح المرحلة', 'name_en': 'Retained Earnings', 'balance': 89500.00}
        },
        'revenue': {
            'sales_revenue': {'name_ar': 'إيرادات المبيعات', 'name_en': 'Sales Revenue', 'balance': 180000.00},
            'other_income': {'name_ar': 'إيرادات أخرى', 'name_en': 'Other Income', 'balance': 5000.00}
        },
        'expenses': {
            'cost_of_goods': {'name_ar': 'تكلفة البضاعة المباعة', 'name_en': 'Cost of Goods Sold', 'balance': 95000.00},
            'salaries_expense': {'name_ar': 'مصروف الرواتب', 'name_en': 'Salaries Expense', 'balance': 45000.00},
            'rent_expense': {'name_ar': 'مصروف الإيجار', 'name_en': 'Rent Expense', 'balance': 18000.00},
            'utilities_expense': {'name_ar': 'مصروف الكهرباء والماء', 'name_en': 'Utilities Expense', 'balance': 8500.00},
            'marketing_expense': {'name_ar': 'مصروف التسويق', 'name_en': 'Marketing Expense', 'balance': 6000.00},
            'depreciation_expense': {'name_ar': 'مصروف الإهلاك', 'name_en': 'Depreciation Expense', 'balance': 12000.00}
        }
    }

    # حساب الإجماليات
    totals = {
        'total_assets': sum(account['balance'] for account in accounts_data['assets'].values()),
        'total_liabilities': sum(account['balance'] for account in accounts_data['liabilities'].values()),
        'total_equity': sum(account['balance'] for account in accounts_data['equity'].values()),
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

# API routes معطلة مؤقتاً - سيتم تفعيلها بعد تحديث قاعدة البيانات

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data()

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
