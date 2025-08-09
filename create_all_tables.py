#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء جميع جداول قاعدة البيانات
Create All Database Tables Script
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_all_tables():
    """إنشاء جميع الجداول المطلوبة"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 بدء إنشاء جميع الجداول...")
        
        # 1. جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
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
        print("✅ جدول المستخدمين")
        
        # 2. جدول الفروع
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS branches (
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
        print("✅ جدول الفروع")
        
        # 3. جدول المنتجات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
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
        print("✅ جدول المنتجات")
        
        # 4. جدول العملاء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
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
        print("✅ جدول العملاء")
        
        # 5. جدول المبيعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
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
        print("✅ جدول المبيعات")
        
        # 6. جدول عناصر المبيعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
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
        print("✅ جدول عناصر المبيعات")
        
        # 7. جدول المواد الخام
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raw_materials (
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
        print("✅ جدول المواد الخام")
        
        # 8. جدول تكلفة المنتجات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_costs (
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
        print("✅ جدول تكلفة المنتجات")
        
        # 9. جدول الدفعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
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
        print("✅ جدول الدفعات")
        
        # 10. جداول ربط الدفعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_sales (
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
            CREATE TABLE IF NOT EXISTS payment_purchases (
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
            CREATE TABLE IF NOT EXISTS payment_expenses (
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
            CREATE TABLE IF NOT EXISTS payment_payrolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER NOT NULL,
                payroll_id INTEGER NOT NULL,
                applied_amount FLOAT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments (id),
                FOREIGN KEY (payroll_id) REFERENCES employee_payrolls (id)
            )
        ''')
        print("✅ جداول ربط الدفعات")
        
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
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            password_hash = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES ('admin', ?, 'مدير النظام', 'admin@example.com', 'admin')
            ''', (password_hash,))
            print("✅ تم إنشاء المستخدم الافتراضي: admin / admin123")
        
        # 2. إنشاء الفرع الرئيسي
        cursor.execute("SELECT COUNT(*) FROM branches")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO branches (branch_code, branch_name, branch_name_en, is_active)
                VALUES ('MAIN', 'الفرع الرئيسي', 'Main Branch', 1)
            ''')
            print("✅ تم إضافة الفرع الرئيسي")
        
        # 3. إضافة مورد افتراضي
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
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
    print("🗃️ إنشاء جميع جداول قاعدة البيانات")
    print("🗃️ Create All Database Tables")
    print("=" * 60)
    
    try:
        # إنشاء الجداول
        create_all_tables()
        
        # إدراج البيانات الافتراضية
        insert_default_data()
        
        print("\n" + "=" * 60)
        print("✅ تم إنشاء قاعدة البيانات بنجاح!")
        print("✅ Database created successfully!")
        print("👤 بيانات تسجيل الدخول:")
        print("   المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ فشل في إنشاء قاعدة البيانات: {e}")
        print(f"❌ Failed to create database: {e}")

if __name__ == "__main__":
    main()
