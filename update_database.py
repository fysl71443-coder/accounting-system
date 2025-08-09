#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحديث قاعدة البيانات
Database Update Script
"""

import sqlite3
import os
from datetime import datetime

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    if os.path.exists('accounting.db'):
        backup_name = f'accounting_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        import shutil
        shutil.copy2('accounting.db', backup_name)
        print(f"✅ تم إنشاء نسخة احتياطية: {backup_name}")
        return backup_name
    return None

def update_database_schema():
    """تحديث مخطط قاعدة البيانات"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 بدء تحديث قاعدة البيانات...")
        
        # 1. إنشاء جدول الموردين إذا لم يكن موجوداً
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
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
        print("✅ جدول الموردين جاهز")
        
        # 2. إنشاء جدول عناصر المشتريات إذا لم يكن موجوداً
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_items (
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
        print("✅ جدول عناصر المشتريات جاهز")
        
        # 3. فحص وتحديث جدول المشتريات
        cursor.execute("PRAGMA table_info(purchases)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الأعمدة المفقودة
        if 'supplier_id' not in columns:
            cursor.execute('ALTER TABLE purchases ADD COLUMN supplier_id INTEGER')
            print("✅ تم إضافة عمود supplier_id")
            
        if 'subtotal' not in columns:
            cursor.execute('ALTER TABLE purchases ADD COLUMN subtotal FLOAT DEFAULT 0.0')
            print("✅ تم إضافة عمود subtotal")
            
        if 'discount_amount' not in columns:
            cursor.execute('ALTER TABLE purchases ADD COLUMN discount_amount FLOAT DEFAULT 0.0')
            print("✅ تم إضافة عمود discount_amount")
            
        # تحديث الأعمدة الموجودة إذا لزم الأمر
        if 'total_amount' in columns:
            # نقل البيانات من total_amount إلى subtotal إذا كان subtotal فارغاً
            cursor.execute('''
                UPDATE purchases 
                SET subtotal = total_amount 
                WHERE subtotal IS NULL OR subtotal = 0
            ''')
            print("✅ تم نقل البيانات من total_amount إلى subtotal")
        
        # 4. فحص وتحديث جدول المبيعات
        cursor.execute("PRAGMA table_info(sales)")
        sales_columns = [column[1] for column in cursor.fetchall()]
        
        if 'subtotal' not in sales_columns:
            cursor.execute('ALTER TABLE sales ADD COLUMN subtotal FLOAT DEFAULT 0.0')
            print("✅ تم إضافة عمود subtotal لجدول المبيعات")
            
        if 'discount_amount' not in sales_columns:
            cursor.execute('ALTER TABLE sales ADD COLUMN discount_amount FLOAT DEFAULT 0.0')
            print("✅ تم إضافة عمود discount_amount لجدول المبيعات")
        
        # 5. إنشاء جدول عناصر المبيعات إذا لم يكن موجوداً
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
        print("✅ جدول عناصر المبيعات جاهز")
        
        # 6. إنشاء جداول الدفعات إذا لم تكن موجودة
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
        print("✅ جدول الدفعات جاهز")
        
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
        print("✅ جدول ربط دفعات المبيعات جاهز")
        
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
        print("✅ جدول ربط دفعات المشتريات جاهز")
        
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
        print("✅ جدول ربط دفعات المصروفات جاهز")
        
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
        print("✅ جدول ربط دفعات الرواتب جاهز")
        
        # 7. إضافة بعض البيانات الأساسية
        # إضافة فرع افتراضي إذا لم يكن موجوداً
        cursor.execute("SELECT COUNT(*) FROM branches")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO branches (branch_code, branch_name, branch_name_en, is_active)
                VALUES ('MAIN', 'الفرع الرئيسي', 'Main Branch', 1)
            ''')
            print("✅ تم إضافة الفرع الرئيسي")
        
        # إضافة مورد افتراضي
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO suppliers (name, phone, email, is_active)
                VALUES ('مورد عام', '0500000000', 'supplier@example.com', 1)
            ''')
            print("✅ تم إضافة مورد افتراضي")
        
        conn.commit()
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
        raise
    finally:
        conn.close()

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🗃️ أداة تحديث قاعدة البيانات - Database Update Tool")
    print("=" * 60)
    
    # إنشاء نسخة احتياطية
    backup_file = backup_database()
    
    try:
        # تحديث قاعدة البيانات
        update_database_schema()
        
        print("\n" + "=" * 60)
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        print("✅ Database updated successfully!")
        if backup_file:
            print(f"📁 النسخة الاحتياطية: {backup_file}")
            print(f"📁 Backup file: {backup_file}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ فشل في تحديث قاعدة البيانات: {e}")
        print(f"❌ Failed to update database: {e}")
        if backup_file:
            print(f"💡 يمكنك استعادة النسخة الاحتياطية: {backup_file}")
            print(f"💡 You can restore from backup: {backup_file}")

if __name__ == "__main__":
    main()
