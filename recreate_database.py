#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعادة إنشاء قاعدة البيانات بالكامل
Recreate Database Completely
"""

import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def backup_existing_data():
    """نسخ احتياطي للبيانات الموجودة"""
    if not os.path.exists('accounting.db'):
        return {}
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    backup_data = {}
    
    try:
        # نسخ بيانات المستخدمين
        cursor.execute("SELECT * FROM users")
        backup_data['users'] = cursor.fetchall()
        
        # نسخ بيانات الفروع
        cursor.execute("SELECT * FROM branches")
        backup_data['branches'] = cursor.fetchall()
        
        # نسخ بيانات المنتجات
        cursor.execute("SELECT * FROM products")
        backup_data['products'] = cursor.fetchall()
        
        # نسخ بيانات العملاء
        cursor.execute("SELECT * FROM customers")
        backup_data['customers'] = cursor.fetchall()
        
        # نسخ بيانات الموردين
        cursor.execute("SELECT * FROM suppliers")
        backup_data['suppliers'] = cursor.fetchall()
        
        # نسخ بيانات المبيعات
        cursor.execute("SELECT * FROM sales")
        backup_data['sales'] = cursor.fetchall()
        
        # نسخ بيانات المشتريات
        cursor.execute("SELECT * FROM purchases")
        backup_data['purchases'] = cursor.fetchall()
        
        # نسخ بيانات المصروفات
        cursor.execute("SELECT * FROM expenses")
        backup_data['expenses'] = cursor.fetchall()
        
        # نسخ بيانات الرواتب
        cursor.execute("SELECT * FROM employee_payrolls")
        backup_data['payrolls'] = cursor.fetchall()
        
        print(f"✅ تم نسخ البيانات احتياطياً:")
        for table, data in backup_data.items():
            print(f"   - {table}: {len(data)} سجل")
            
    except Exception as e:
        print(f"⚠️ تحذير: لم يتم نسخ بعض البيانات: {e}")
    finally:
        conn.close()
    
    return backup_data

def create_fresh_database():
    """إنشاء قاعدة بيانات جديدة"""
    # حذف قاعدة البيانات القديمة
    if os.path.exists('accounting.db'):
        backup_name = f'accounting_old_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('accounting.db', backup_name)
        print(f"📁 تم نقل قاعدة البيانات القديمة إلى: {backup_name}")
    
    # إنشاء قاعدة بيانات جديدة
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 إنشاء قاعدة بيانات جديدة...")
        
        # 1. جدول المستخدمين
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(200),
                email VARCHAR(120),
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        ''')
        
        # 2. جدول الفروع
        cursor.execute('''
            CREATE TABLE branches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                branch_code VARCHAR(10) UNIQUE NOT NULL,
                branch_name VARCHAR(200) NOT NULL,
                branch_name_en VARCHAR(200),
                address TEXT,
                phone VARCHAR(20),
                manager_name VARCHAR(100),
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. جدول المنتجات
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code VARCHAR(50) UNIQUE NOT NULL,
                product_name VARCHAR(200) NOT NULL,
                description TEXT,
                selling_price FLOAT DEFAULT 0.0,
                unit_cost FLOAT DEFAULT 0.0,
                unit_type VARCHAR(20) DEFAULT 'قطعة',
                min_stock_level INTEGER DEFAULT 0,
                current_stock INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 4. جدول العملاء
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                tax_number VARCHAR(50),
                credit_limit FLOAT DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 5. جدول الموردين
        cursor.execute('''
            CREATE TABLE suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                tax_number VARCHAR(50),
                contact_person VARCHAR(100),
                credit_limit FLOAT DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 6. جدول المبيعات
        cursor.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number VARCHAR(50) UNIQUE NOT NULL,
                branch_id INTEGER,
                customer_id INTEGER,
                customer_name VARCHAR(200),
                invoice_date DATE NOT NULL,
                subtotal FLOAT DEFAULT 0.0,
                discount_amount FLOAT DEFAULT 0.0,
                tax_amount FLOAT DEFAULT 0.0,
                final_amount FLOAT DEFAULT 0.0,
                payment_method VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'pending',
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (branch_id) REFERENCES branches (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # 7. جدول المشتريات - مع جميع الأعمدة المطلوبة
        cursor.execute('''
            CREATE TABLE purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number VARCHAR(50) UNIQUE NOT NULL,
                branch_id INTEGER,
                supplier_id INTEGER,
                supplier_name VARCHAR(200),
                invoice_date DATE NOT NULL,
                subtotal FLOAT DEFAULT 0.0,
                discount_amount FLOAT DEFAULT 0.0,
                tax_amount FLOAT DEFAULT 0.0,
                final_amount FLOAT DEFAULT 0.0,
                payment_method VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'pending',
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (branch_id) REFERENCES branches (id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # 8. جدول عناصر المشتريات
        cursor.execute('''
            CREATE TABLE purchase_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name VARCHAR(200) NOT NULL,
                quantity FLOAT NOT NULL,
                unit_price FLOAT NOT NULL,
                total_price FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (purchase_id) REFERENCES purchases (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # 9. جدول عناصر المبيعات
        cursor.execute('''
            CREATE TABLE sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name VARCHAR(200) NOT NULL,
                quantity FLOAT NOT NULL,
                unit_price FLOAT NOT NULL,
                total_price FLOAT NOT NULL,
                tax_rate FLOAT DEFAULT 15.0,
                tax_amount FLOAT DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sale_id) REFERENCES sales (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # 10. جدول المصروفات
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_number VARCHAR(50) UNIQUE NOT NULL,
                branch_id INTEGER,
                expense_type VARCHAR(100),
                description TEXT,
                expense_date DATE NOT NULL,
                amount FLOAT NOT NULL,
                payment_method VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'pending',
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (branch_id) REFERENCES branches (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # 11. جدول الرواتب
        cursor.execute('''
            CREATE TABLE employee_payrolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payroll_number VARCHAR(50) UNIQUE NOT NULL,
                employee_name VARCHAR(200) NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                basic_salary FLOAT DEFAULT 0.0,
                allowances FLOAT DEFAULT 0.0,
                deductions FLOAT DEFAULT 0.0,
                net_salary FLOAT DEFAULT 0.0,
                payment_method VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'pending',
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # 12. جدول المواد الخام
        cursor.execute('''
            CREATE TABLE raw_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_code VARCHAR(50) UNIQUE NOT NULL,
                material_name VARCHAR(200) NOT NULL,
                description TEXT,
                unit_type VARCHAR(20) DEFAULT 'كيلو',
                unit_cost FLOAT DEFAULT 0.0,
                current_stock FLOAT DEFAULT 0.0,
                min_stock_level FLOAT DEFAULT 0.0,
                supplier VARCHAR(100),
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 13. جدول تكلفة المنتجات
        cursor.execute('''
            CREATE TABLE product_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                raw_material_id INTEGER NOT NULL,
                quantity_used DECIMAL(10, 3) NOT NULL,
                unit_cost DECIMAL(10, 3) NOT NULL,
                total_cost DECIMAL(10, 3) NOT NULL,
                percentage DECIMAL(5, 2) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (raw_material_id) REFERENCES raw_materials (id)
            )
        ''')
        
        # 14. جدول الدفعات
        cursor.execute('''
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_number VARCHAR(50) UNIQUE NOT NULL,
                payment_date DATE NOT NULL,
                amount FLOAT NOT NULL,
                payment_method VARCHAR(20),
                reference_number VARCHAR(100),
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # 15-18. جداول ربط الدفعات
        cursor.execute('''
            CREATE TABLE payment_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER NOT NULL,
                sale_id INTEGER NOT NULL,
                applied_amount FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments (id),
                FOREIGN KEY (sale_id) REFERENCES sales (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE payment_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER NOT NULL,
                purchase_id INTEGER NOT NULL,
                applied_amount FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments (id),
                FOREIGN KEY (purchase_id) REFERENCES purchases (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE payment_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER NOT NULL,
                expense_id INTEGER NOT NULL,
                applied_amount FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments (id),
                FOREIGN KEY (expense_id) REFERENCES expenses (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE payment_payrolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER NOT NULL,
                payroll_id INTEGER NOT NULL,
                applied_amount FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments (id),
                FOREIGN KEY (payroll_id) REFERENCES employee_payrolls (id)
            )
        ''')
        
        conn.commit()
        print("✅ تم إنشاء جميع الجداول بنجاح!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        raise
    finally:
        conn.close()

def insert_default_data():
    """إدراج البيانات الافتراضية"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("📝 إدراج البيانات الافتراضية...")
        
        # 1. إنشاء مستخدم المدير
        password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, password_hash, full_name, email, role)
            VALUES ('admin', ?, 'مدير النظام', 'admin@example.com', 'admin')
        ''', (password_hash,))
        print("✅ تم إنشاء المستخدم الافتراضي: admin / admin123")
        
        # 2. إنشاء الفرع الرئيسي
        cursor.execute('''
            INSERT INTO branches (branch_code, branch_name, branch_name_en, is_active)
            VALUES ('MAIN', 'الفرع الرئيسي', 'Main Branch', 1)
        ''')
        print("✅ تم إضافة الفرع الرئيسي")
        
        # 3. إضافة مورد افتراضي
        cursor.execute('''
            INSERT INTO suppliers (name, phone, email, is_active)
            VALUES ('مورد عام', '0500000000', 'supplier@example.com', 1)
        ''')
        print("✅ تم إضافة مورد افتراضي")
        
        conn.commit()
        print("✅ تم إدراج البيانات الافتراضية بنجاح!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ خطأ في إدراج البيانات الافتراضية: {e}")
        raise
    finally:
        conn.close()

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔄 إعادة إنشاء قاعدة البيانات بالكامل")
    print("🔄 Recreate Database Completely")
    print("=" * 60)
    
    try:
        # نسخ احتياطي للبيانات الموجودة
        backup_data = backup_existing_data()
        
        # إنشاء قاعدة بيانات جديدة
        create_fresh_database()
        
        # إدراج البيانات الافتراضية
        insert_default_data()
        
        print("\n" + "=" * 60)
        print("✅ تم إعادة إنشاء قاعدة البيانات بنجاح!")
        print("✅ Database recreated successfully!")
        print("👤 بيانات تسجيل الدخول:")
        print("   المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("🚀 يمكن الآن تشغيل النظام بدون أخطاء")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ فشل في إعادة إنشاء قاعدة البيانات: {e}")
        print(f"❌ Failed to recreate database: {e}")

if __name__ == "__main__":
    main()
