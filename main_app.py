#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المحاسبة المتكامل - النسخة الرئيسية
Integrated Accounting System - Main Version
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# جعل بيانات الجلسة متاحة في جميع القوالب
@app.context_processor
def inject_user():
    return dict(
        current_user_authenticated=bool(session.get('user_id')),
        current_user_name=session.get('full_name', ''),
        current_user_role=session.get('role', '')
    )

# إعداد قاعدة البيانات
DATABASE = 'accounting.db'

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """تهيئة قاعدة البيانات"""
    conn = get_db_connection()
    
    # جدول المستخدمين
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # جدول الفروع
    conn.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_code TEXT UNIQUE NOT NULL,
            branch_name TEXT NOT NULL,
            branch_name_en TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            manager_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المنتجات
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE NOT NULL,
            product_name TEXT NOT NULL,
            description TEXT,
            unit_cost REAL DEFAULT 0.0,
            selling_price REAL DEFAULT 0.0,
            category TEXT,
            unit_type TEXT DEFAULT 'قطعة',
            min_stock_level INTEGER DEFAULT 0,
            current_stock INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المبيعات
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            branch_id INTEGER,
            customer_name TEXT,
            invoice_date DATE NOT NULL,
            total_amount REAL DEFAULT 0.0,
            tax_amount REAL DEFAULT 0.0,
            final_amount REAL DEFAULT 0.0,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'completed',
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (branch_id) REFERENCES branches (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # جدول عناصر المبيعات
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            tax_rate REAL DEFAULT 15.0,
            tax_amount REAL DEFAULT 0.0,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # جدول المكونات الخام
    conn.execute('''
        CREATE TABLE IF NOT EXISTS raw_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_code TEXT UNIQUE NOT NULL,
            material_name TEXT NOT NULL,
            description TEXT,
            unit_type TEXT DEFAULT 'كيلو',
            cost_per_unit REAL DEFAULT 0.0,
            current_stock REAL DEFAULT 0.0,
            min_stock_level REAL DEFAULT 0.0,
            supplier_name TEXT,
            last_purchase_price REAL DEFAULT 0.0,
            last_purchase_date DATE,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول وصفات المنتجات (المكونات)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS product_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantity_needed REAL NOT NULL,
            unit_type TEXT NOT NULL,
            cost_per_unit REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (material_id) REFERENCES raw_materials (id)
        )
    ''')

    # جدول تحديث التكاليف
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cost_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            old_cost REAL DEFAULT 0.0,
            new_cost REAL DEFAULT 0.0,
            material_costs REAL DEFAULT 0.0,
            labor_cost REAL DEFAULT 0.0,
            overhead_cost REAL DEFAULT 0.0,
            profit_margin REAL DEFAULT 0.0,
            updated_by INTEGER,
            update_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (updated_by) REFERENCES users (id)
        )
    ''')
    
    # إنشاء المستخدم الافتراضي
    admin_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exists:
        password_hash = generate_password_hash('admin123')
        conn.execute('''
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', password_hash, 'مدير النظام', 'admin'))
    
    # إنشاء الفروع الافتراضية
    branches_exist = conn.execute('SELECT id FROM branches LIMIT 1').fetchone()
    if not branches_exist:
        branches = [
            ('PI', 'PLACE INDIA', 'PLACE INDIA', '', '', ''),
            ('CT', 'CHINA TOWN', 'CHINA TOWN', '', '', '')
        ]
        for branch_code, branch_name, branch_name_en, address, phone, manager in branches:
            conn.execute('''
                INSERT INTO branches (branch_code, branch_name, branch_name_en, address, phone, manager_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (branch_code, branch_name, branch_name_en, address, phone, manager))
    
    # إنشاء المكونات الخام التجريبية
    materials_exist = conn.execute('SELECT id FROM raw_materials LIMIT 1').fetchone()
    if not materials_exist:
        raw_materials = [
            # مكونات البرياني
            ("RICE001", "أرز بسمتي", "أرز بسمتي فاخر للبرياني", "كيلو", 12.00, 50.0, 10.0, "مورد الأرز المحلي", 12.00),
            ("CHICKEN001", "دجاج طازج", "دجاج طازج مقطع قطع", "كيلو", 25.00, 30.0, 5.0, "مزرعة الدجاج الطازج", 25.00),
            ("ONION001", "بصل", "بصل أحمر طازج", "كيلو", 3.00, 20.0, 5.0, "مورد الخضار", 3.00),
            ("TOMATO001", "طماطم", "طماطم طازجة", "كيلو", 4.00, 15.0, 3.0, "مورد الخضار", 4.00),
            ("YOGURT001", "لبن زبادي", "لبن زبادي طبيعي", "كيلو", 8.00, 10.0, 2.0, "مصنع الألبان", 8.00),
            ("SPICE001", "بهارات البرياني", "خلطة بهارات البرياني الخاصة", "كيلو", 45.00, 5.0, 1.0, "مورد البهارات", 45.00),
            ("OIL001", "زيت طبخ", "زيت دوار الشمس للطبخ", "لتر", 8.00, 20.0, 5.0, "مورد الزيوت", 8.00),
            ("SALT001", "ملح", "ملح طعام نقي", "كيلو", 2.00, 10.0, 2.0, "مورد التوابل", 2.00),
            ("GARLIC001", "ثوم", "ثوم طازج", "كيلو", 15.00, 8.0, 2.0, "مورد الخضار", 15.00),
            ("GINGER001", "زنجبيل", "زنجبيل طازج", "كيلو", 20.00, 5.0, 1.0, "مورد الخضار", 20.00),
            ("SAFFRON001", "زعفران", "زعفران أصلي", "جرام", 0.50, 100.0, 20.0, "مورد البهارات الفاخرة", 0.50),
            ("ALMONDS001", "لوز", "لوز مقشر", "كيلو", 35.00, 3.0, 0.5, "مورد المكسرات", 35.00),
            ("RAISINS001", "زبيب", "زبيب ذهبي", "كيلو", 18.00, 2.0, 0.5, "مورد المكسرات", 18.00),

            # مكونات أخرى
            ("BREAD001", "دقيق", "دقيق أبيض فاخر", "كيلو", 4.00, 25.0, 5.0, "مطحنة الدقيق", 4.00),
            ("SUGAR001", "سكر", "سكر أبيض نقي", "كيلو", 5.00, 20.0, 5.0, "مصنع السكر", 5.00),
        ]

        for material_code, name, desc, unit, cost, stock, min_stock, supplier, last_price in raw_materials:
            conn.execute('''
                INSERT INTO raw_materials (material_code, material_name, description, unit_type,
                cost_per_unit, current_stock, min_stock_level, supplier_name, last_purchase_price, last_purchase_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, DATE('now'))
            ''', (material_code, name, desc, unit, cost, stock, min_stock, supplier, last_price))

    # إنشاء منتجات تجريبية
    products_exist = conn.execute('SELECT id FROM products LIMIT 1').fetchone()
    if not products_exist:
        sample_products = [
            # منتجات مركبة (وجبات)
            ("BIRYANI001", "برياني دجاج", "وجبة برياني دجاج بالبهارات الخاصة", 0.00, 45.00, "وجبات", "طبق", 5, 20),
            ("BIRYANI002", "برياني لحم", "وجبة برياني لحم بالبهارات الخاصة", 0.00, 55.00, "وجبات", "طبق", 5, 15),

            # منتجات بسيطة
            ("PHONE001", "iPhone 14", "هاتف ذكي من آبل", 3000.00, 3500.00, "إلكترونيات", "قطعة", 5, 20),
            ("PHONE002", "Samsung Galaxy S23", "هاتف ذكي من سامسونج", 2500.00, 3000.00, "إلكترونيات", "قطعة", 5, 15),
            ("LAPTOP001", "MacBook Air", "لابتوب من آبل", 4000.00, 4800.00, "إلكترونيات", "قطعة", 3, 10),
            ("SHIRT001", "قميص قطني", "قميص رجالي قطني", 50.00, 80.00, "ملابس", "قطعة", 10, 50),
            ("FOOD001", "أرز بسمتي", "أرز بسمتي فاخر", 15.00, 25.00, "أغذية", "كيلو", 20, 100),
            ("FOOD002", "زيت زيتون", "زيت زيتون بكر ممتاز", 30.00, 45.00, "أغذية", "لتر", 15, 50),
        ]

        for product_code, name, desc, cost, price, category, unit, min_stock, current_stock in sample_products:
            cursor = conn.execute('''
                INSERT INTO products (product_code, product_name, description, unit_cost,
                selling_price, category, unit_type, min_stock_level, current_stock, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (product_code, name, desc, cost, price, category, unit, min_stock, current_stock))

            # إضافة وصفة البرياني دجاج
            if product_code == "BIRYANI001":
                product_id = cursor.lastrowid
                biryani_recipe = [
                    # (material_code, quantity, unit, notes)
                    ("RICE001", 0.3, "كيلو", "أرز بسمتي منقوع ومسلوق"),
                    ("CHICKEN001", 0.4, "كيلو", "دجاج مقطع ومتبل"),
                    ("ONION001", 0.15, "كيلو", "بصل مقلي ذهبي"),
                    ("TOMATO001", 0.1, "كيلو", "طماطم مقطعة"),
                    ("YOGURT001", 0.1, "كيلو", "لبن زبادي للتتبيل"),
                    ("SPICE001", 0.02, "كيلو", "بهارات البرياني"),
                    ("OIL001", 0.05, "لتر", "زيت للطبخ"),
                    ("SALT001", 0.01, "كيلو", "ملح حسب الذوق"),
                    ("GARLIC001", 0.03, "كيلو", "ثوم مفروم"),
                    ("GINGER001", 0.02, "كيلو", "زنجبيل مفروم"),
                    ("SAFFRON001", 2.0, "جرام", "زعفران للون والطعم"),
                    ("ALMONDS001", 0.02, "كيلو", "لوز مقلي للتزيين"),
                    ("RAISINS001", 0.015, "كيلو", "زبيب للتزيين"),
                ]

                for material_code, quantity, unit, notes in biryani_recipe:
                    # الحصول على معرف المكون
                    material = conn.execute(
                        'SELECT id, cost_per_unit FROM raw_materials WHERE material_code = ?',
                        (material_code,)
                    ).fetchone()

                    if material:
                        material_id = material['id']
                        cost_per_unit = material['cost_per_unit']
                        total_cost = quantity * cost_per_unit

                        conn.execute('''
                            INSERT INTO product_recipes (product_id, material_id, quantity_needed,
                            unit_type, cost_per_unit, total_cost, notes)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (product_id, material_id, quantity, unit, cost_per_unit, total_cost, notes))
    
    conn.commit()
    conn.close()

def calculate_product_cost(product_id):
    """حساب تكلفة المنتج بناءً على مكوناته"""
    conn = get_db_connection()

    # الحصول على وصفة المنتج
    recipe = conn.execute('''
        SELECT pr.*, rm.material_name, rm.cost_per_unit as current_cost_per_unit
        FROM product_recipes pr
        JOIN raw_materials rm ON pr.material_id = rm.id
        WHERE pr.product_id = ? AND rm.is_active = 1
    ''', (product_id,)).fetchall()

    if not recipe:
        conn.close()
        return 0.0, []

    total_material_cost = 0.0
    cost_breakdown = []

    for item in recipe:
        # حساب التكلفة الحالية
        current_total_cost = item['quantity_needed'] * item['current_cost_per_unit']
        total_material_cost += current_total_cost

        cost_breakdown.append({
            'material_name': item['material_name'],
            'quantity': item['quantity_needed'],
            'unit': item['unit_type'],
            'cost_per_unit': item['current_cost_per_unit'],
            'total_cost': current_total_cost,
            'notes': item['notes']
        })

        # تحديث تكلفة المكون في جدول الوصفة إذا تغيرت
        if item['cost_per_unit'] != item['current_cost_per_unit']:
            conn.execute('''
                UPDATE product_recipes
                SET cost_per_unit = ?, total_cost = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (item['current_cost_per_unit'], current_total_cost, item['id']))

    conn.commit()
    conn.close()

    return total_material_cost, cost_breakdown

def update_product_cost(product_id, material_cost, labor_cost=0.0, overhead_cost=0.0, profit_margin=0.0):
    """تحديث تكلفة المنتج وحفظ سجل التحديث"""
    conn = get_db_connection()

    # الحصول على التكلفة الحالية
    current_product = conn.execute(
        'SELECT unit_cost FROM products WHERE id = ?', (product_id,)
    ).fetchone()

    old_cost = current_product['unit_cost'] if current_product else 0.0

    # حساب التكلفة الجديدة
    total_cost = material_cost + labor_cost + overhead_cost
    new_cost = total_cost * (1 + profit_margin / 100)

    # تحديث تكلفة المنتج
    conn.execute('''
        UPDATE products
        SET unit_cost = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_cost, product_id))

    # حفظ سجل التحديث
    conn.execute('''
        INSERT INTO cost_updates (product_id, old_cost, new_cost, material_costs,
        labor_cost, overhead_cost, profit_margin, updated_by, update_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, old_cost, new_cost, material_cost, labor_cost, overhead_cost,
          profit_margin, session.get('user_id'), 'تحديث تلقائي للتكلفة'))

    conn.commit()
    conn.close()

    return new_cost

def login_required(f):
    """ديكوريتر للتحقق من تسجيل الدخول"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# الصفحات الرئيسية
@app.route('/')
def index():
    """الصفحة الرئيسية"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        language = request.form.get('language', 'ar')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND is_active = 1',
            (username,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            session['language'] = language
            
            # تحديث آخر تسجيل دخول
            conn = get_db_connection()
            conn.execute(
                'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                (user['id'],)
            )
            conn.commit()
            conn.close()
            
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية"""
    conn = get_db_connection()
    
    # إحصائيات سريعة
    today = datetime.now().date()
    
    # مبيعات اليوم
    daily_sales = conn.execute(
        'SELECT COALESCE(SUM(final_amount), 0) as total FROM sales WHERE DATE(invoice_date) = ?',
        (today,)
    ).fetchone()['total']
    
    # مبيعات الشهر
    month_start = today.replace(day=1)
    monthly_sales = conn.execute(
        'SELECT COALESCE(SUM(final_amount), 0) as total FROM sales WHERE invoice_date >= ?',
        (month_start,)
    ).fetchone()['total']
    
    # عدد المنتجات
    total_products = conn.execute(
        'SELECT COUNT(*) as count FROM products WHERE is_active = 1'
    ).fetchone()['count']
    
    # تنبيهات المخزون المنخفض
    low_stock_products = conn.execute(
        'SELECT * FROM products WHERE current_stock <= min_stock_level AND is_active = 1'
    ).fetchall()
    
    # آخر المبيعات
    recent_sales = conn.execute('''
        SELECT s.*, b.branch_name 
        FROM sales s 
        LEFT JOIN branches b ON s.branch_id = b.id 
        ORDER BY s.created_at DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
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

    conn = get_db_connection()

    if search:
        products = conn.execute('''
            SELECT * FROM products
            WHERE (product_name LIKE ? OR product_code LIKE ? OR category LIKE ?)
            ORDER BY product_name
        ''', (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        products = conn.execute('SELECT * FROM products ORDER BY product_name').fetchall()

    conn.close()

    return render_template('products.html', products=products, search=search)

@app.route('/raw_materials')
@login_required
def raw_materials():
    """صفحة إدارة المكونات الخام"""
    search = request.args.get('search', '')

    conn = get_db_connection()

    if search:
        materials = conn.execute('''
            SELECT * FROM raw_materials
            WHERE (material_name LIKE ? OR material_code LIKE ? OR supplier_name LIKE ?)
            ORDER BY material_name
        ''', (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        materials = conn.execute('SELECT * FROM raw_materials ORDER BY material_name').fetchall()

    conn.close()

    return render_template('raw_materials.html', materials=materials, search=search)

@app.route('/product_cost/<int:product_id>')
@login_required
def product_cost(product_id):
    """صفحة حساب تكلفة المنتج"""
    conn = get_db_connection()

    # الحصول على بيانات المنتج
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        flash('المنتج غير موجود', 'error')
        return redirect(url_for('products'))

    # حساب تكلفة المكونات
    material_cost, cost_breakdown = calculate_product_cost(product_id)

    # الحصول على سجل تحديثات التكلفة
    cost_history = conn.execute('''
        SELECT cu.*, u.full_name as updated_by_name
        FROM cost_updates cu
        LEFT JOIN users u ON cu.updated_by = u.id
        WHERE cu.product_id = ?
        ORDER BY cu.created_at DESC
        LIMIT 10
    ''', (product_id,)).fetchall()

    conn.close()

    return render_template('product_cost.html',
                         product=product,
                         material_cost=material_cost,
                         cost_breakdown=cost_breakdown,
                         cost_history=cost_history)

@app.route('/sales')
@login_required
def sales():
    """صفحة المبيعات"""
    branch_id = request.args.get('branch_id')
    
    conn = get_db_connection()
    
    if branch_id:
        sales = conn.execute('''
            SELECT s.*, b.branch_name 
            FROM sales s 
            LEFT JOIN branches b ON s.branch_id = b.id 
            WHERE s.branch_id = ?
            ORDER BY s.created_at DESC
        ''', (branch_id,)).fetchall()
    else:
        sales = conn.execute('''
            SELECT s.*, b.branch_name 
            FROM sales s 
            LEFT JOIN branches b ON s.branch_id = b.id 
            ORDER BY s.created_at DESC
        ''').fetchall()
    
    branches = conn.execute('SELECT * FROM branches WHERE is_active = 1').fetchall()
    conn.close()
    
    return render_template('sales.html', sales=sales, branches=branches, selected_branch=branch_id)

@app.route('/new_sale')
@login_required
def new_sale():
    """صفحة فاتورة مبيعات جديدة"""
    conn = get_db_connection()
    branches = conn.execute('SELECT * FROM branches WHERE is_active = 1').fetchall()
    products = conn.execute('SELECT * FROM products WHERE is_active = 1').fetchall()
    conn.close()
    
    return render_template('new_sale.html', branches=branches, products=products)

# API endpoints
@app.route('/api/products')
@login_required
def api_products():
    """API للحصول على المنتجات"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE is_active = 1').fetchall()
    conn.close()
    
    return jsonify([{
        'id': p['id'],
        'code': p['product_code'],
        'name': p['product_name'],
        'price': p['selling_price'],
        'stock': p['current_stock']
    } for p in products])

@app.route('/api/generate_invoice_number')
@login_required
def api_generate_invoice_number():
    """API لتوليد رقم فاتورة جديد"""
    branch_id = request.args.get('branch_id', 1)
    today = datetime.now()
    
    conn = get_db_connection()
    
    # البحث عن آخر رقم فاتورة لهذا اليوم والفرع
    last_sale = conn.execute('''
        SELECT invoice_number FROM sales 
        WHERE branch_id = ? AND DATE(invoice_date) = DATE(?)
        ORDER BY id DESC LIMIT 1
    ''', (branch_id, today.strftime('%Y-%m-%d'))).fetchone()
    
    sequence = 1
    if last_sale:
        try:
            last_sequence = int(last_sale['invoice_number'].split('-')[-1])
            sequence = last_sequence + 1
        except:
            sequence = 1
    
    # الحصول على رمز الفرع
    branch = conn.execute('SELECT branch_code FROM branches WHERE id = ?', (branch_id,)).fetchone()
    branch_code = branch['branch_code'] if branch else 'XX'
    
    conn.close()
    
    # تنسيق رقم الفاتورة: BRANCH-YYYYMMDD-XXXX
    invoice_number = f"{branch_code}-{today.strftime('%Y%m%d')}-{sequence:04d}"
    
    return jsonify({'invoice_number': invoice_number})

@app.route('/api/save_sale', methods=['POST'])
@login_required
def api_save_sale():
    """API لحفظ فاتورة مبيعات"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        
        # إنشاء فاتورة جديدة
        cursor = conn.execute('''
            INSERT INTO sales (invoice_number, branch_id, customer_name, invoice_date,
                             total_amount, tax_amount, final_amount, payment_method, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['invoice_number'],
            data['branch_id'],
            data.get('customer_name'),
            data['invoice_date'],
            data['total_amount'],
            data['tax_amount'],
            data['final_amount'],
            data['payment_method'],
            session['user_id']
        ))
        
        sale_id = cursor.lastrowid
        
        # إضافة عناصر الفاتورة
        for item in data['items']:
            conn.execute('''
                INSERT INTO sale_items (sale_id, product_id, product_name, quantity,
                                      unit_price, total_price, tax_rate, tax_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_id,
                item.get('product_id'),
                item['product_name'],
                item['quantity'],
                item['unit_price'],
                item['total_price'],
                item.get('tax_rate', 15.0),
                item.get('tax_amount', 0.0)
            ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'تم حفظ الفاتورة بنجاح',
            'sale_id': sale_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'خطأ في حفظ الفاتورة: {str(e)}'
        }), 400

@app.route('/api/update_product_cost', methods=['POST'])
@login_required
def api_update_product_cost():
    """API لتحديث تكلفة المنتج"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        labor_cost = float(data.get('labor_cost', 0))
        overhead_cost = float(data.get('overhead_cost', 0))
        profit_margin = float(data.get('profit_margin', 0))

        # حساب تكلفة المكونات
        material_cost, _ = calculate_product_cost(product_id)

        # تحديث التكلفة
        new_cost = update_product_cost(product_id, material_cost, labor_cost, overhead_cost, profit_margin)

        return jsonify({
            'status': 'success',
            'message': 'تم تحديث التكلفة بنجاح',
            'new_cost': new_cost,
            'material_cost': material_cost,
            'total_additional_cost': labor_cost + overhead_cost
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'خطأ في تحديث التكلفة: {str(e)}'
        }), 400

@app.route('/api/recalculate_cost/<int:product_id>')
@login_required
def api_recalculate_cost(product_id):
    """API لإعادة حساب تكلفة المنتج"""
    try:
        material_cost, cost_breakdown = calculate_product_cost(product_id)

        return jsonify({
            'status': 'success',
            'material_cost': material_cost,
            'cost_breakdown': cost_breakdown
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'خطأ في حساب التكلفة: {str(e)}'
        }), 400

@app.route('/api/update_material_cost', methods=['POST'])
@login_required
def api_update_material_cost():
    """API لتحديث تكلفة مكون خام"""
    try:
        data = request.get_json()
        material_id = data.get('material_id')
        new_cost = float(data.get('new_cost'))

        conn = get_db_connection()

        # تحديث تكلفة المكون
        conn.execute('''
            UPDATE raw_materials
            SET cost_per_unit = ?, last_purchase_price = ?, last_purchase_date = DATE('now'), updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_cost, new_cost, material_id))

        # البحث عن جميع المنتجات التي تستخدم هذا المكون
        affected_products = conn.execute('''
            SELECT DISTINCT pr.product_id, p.product_name
            FROM product_recipes pr
            JOIN products p ON pr.product_id = p.id
            WHERE pr.material_id = ?
        ''', (material_id,)).fetchall()

        conn.commit()
        conn.close()

        # إعادة حساب تكلفة المنتجات المتأثرة
        updated_products = []
        for product in affected_products:
            material_cost, _ = calculate_product_cost(product['product_id'])
            updated_products.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'new_material_cost': material_cost
            })

        return jsonify({
            'status': 'success',
            'message': 'تم تحديث تكلفة المكون بنجاح',
            'affected_products': updated_products
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'خطأ في تحديث تكلفة المكون: {str(e)}'
        }), 400

@app.route('/change_language', methods=['POST'])
def change_language():
    """تغيير اللغة"""
    data = request.get_json()
    language = data.get('language', 'ar')
    session['language'] = language
    return jsonify({'status': 'success'})

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

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    # تهيئة قاعدة البيانات
    init_database()
    
    print("🚀 بدء تشغيل نظام المحاسبة المتكامل...")
    print("🚀 Starting Integrated Accounting System...")
    print()
    print("📍 التطبيق يعمل على: http://localhost:5000")
    print("📍 Application running on: http://localhost:5000")
    print()
    print("👤 بيانات تسجيل الدخول:")
    print("👤 Login credentials:")
    print("   المستخدم / Username: admin")
    print("   كلمة المرور / Password: admin123")
    print()
    print("🛑 لإيقاف التطبيق اضغط Ctrl+C")
    print("🛑 To stop the application press Ctrl+C")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
