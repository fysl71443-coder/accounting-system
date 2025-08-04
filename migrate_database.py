#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحديث قاعدة البيانات لنظام الصلاحيات
Database Migration Script for Permissions System
"""

import os
import sqlite3
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

def migrate_database():
    """تحديث قاعدة البيانات لدعم نظام الصلاحيات"""
    
    # إنشاء نسخة احتياطية
    backup_file = backup_database()
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        print("🔄 بدء تحديث قاعدة البيانات...")
        
        # 1. إنشاء جدول الأدوار
        print("📝 إنشاء جدول الأدوار...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(80) UNIQUE NOT NULL,
                name_ar VARCHAR(80) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                -- صلاحيات الوصول للشاشات
                can_access_sales BOOLEAN DEFAULT 0,
                can_access_purchases BOOLEAN DEFAULT 0,
                can_access_inventory BOOLEAN DEFAULT 0,
                can_access_reports BOOLEAN DEFAULT 0,
                can_access_employees BOOLEAN DEFAULT 0,
                can_access_costs BOOLEAN DEFAULT 0,
                can_access_taxes BOOLEAN DEFAULT 0,
                can_access_settings BOOLEAN DEFAULT 0,
                can_access_financial_statements BOOLEAN DEFAULT 0,
                can_access_payments BOOLEAN DEFAULT 0,
                can_access_expenses BOOLEAN DEFAULT 0,
                can_access_suppliers BOOLEAN DEFAULT 0,
                
                -- صلاحيات العمليات CRUD
                can_create BOOLEAN DEFAULT 0,
                can_edit BOOLEAN DEFAULT 0,
                can_delete BOOLEAN DEFAULT 0,
                can_print BOOLEAN DEFAULT 0,
                can_export BOOLEAN DEFAULT 0
            )
        ''')
        
        # 2. التحقق من وجود الأعمدة الجديدة في جدول المستخدمين
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الأعمدة المفقودة
        new_columns = [
            ('role_id', 'INTEGER'),
            ('old_role', 'VARCHAR(20) DEFAULT "user"'),
            ('login_attempts', 'INTEGER DEFAULT 0'),
            ('locked_until', 'DATETIME')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"➕ إضافة عمود {column_name} لجدول المستخدمين...")
                cursor.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_type}')
        
        # 3. إدراج الأدوار الافتراضية
        print("👥 إضافة الأدوار الافتراضية...")
        
        # التحقق من وجود الأدوار
        cursor.execute("SELECT COUNT(*) FROM roles")
        roles_count = cursor.fetchone()[0]
        
        if roles_count == 0:
            default_roles = [
                # مشرف عام - جميع الصلاحيات
                ('admin', 'مشرف عام', 'صلاحيات كاملة لجميع أجزاء النظام', 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # صلاحيات الوصول
                 1, 1, 1, 1, 1),  # صلاحيات العمليات
                
                # محاسب - صلاحيات محاسبية
                ('accountant', 'محاسب', 'صلاحيات محاسبية ومالية', 1,
                 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1,  # صلاحيات الوصول
                 1, 1, 0, 1, 1),  # صلاحيات العمليات
                
                # موظف - صلاحيات محدودة
                ('employee', 'موظف', 'صلاحيات محدودة للعمليات الأساسية', 1,
                 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # صلاحيات الوصول
                 1, 0, 0, 1, 0),  # صلاحيات العمليات
                
                # مراقب - عرض فقط
                ('viewer', 'مراقب', 'صلاحيات عرض فقط', 1,
                 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1,  # صلاحيات الوصول
                 0, 0, 0, 1, 0),  # صلاحيات العمليات
                
                # مدير - صلاحيات إدارية
                ('manager', 'مدير', 'صلاحيات إدارية مع قيود محددة', 1,
                 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,  # صلاحيات الوصول
                 1, 1, 0, 1, 1)   # صلاحيات العمليات
            ]
            
            cursor.executemany('''
                INSERT INTO roles (
                    name, name_ar, description, is_active,
                    can_access_sales, can_access_purchases, can_access_inventory, 
                    can_access_reports, can_access_employees, can_access_costs,
                    can_access_taxes, can_access_settings, can_access_financial_statements,
                    can_access_payments, can_access_expenses, can_access_suppliers,
                    can_create, can_edit, can_delete, can_print, can_export
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', default_roles)
        
        # 4. تحديث المستخدمين الموجودين
        print("🔄 تحديث المستخدمين الموجودين...")
        
        # نسخ الدور القديم إلى old_role إذا لم يكن موجوداً
        cursor.execute("UPDATE users SET old_role = role WHERE old_role IS NULL")
        
        # ربط المستخدمين بالأدوار الجديدة
        cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
        admin_role_result = cursor.fetchone()
        if admin_role_result:
            admin_role_id = admin_role_result[0]
            cursor.execute("UPDATE users SET role_id = ? WHERE role = 'admin' OR old_role = 'admin'", (admin_role_id,))
        
        cursor.execute("SELECT id FROM roles WHERE name = 'employee'")
        employee_role_result = cursor.fetchone()
        if employee_role_result:
            employee_role_id = employee_role_result[0]
            cursor.execute("UPDATE users SET role_id = ? WHERE (role = 'user' OR old_role = 'user') AND role_id IS NULL", (employee_role_id,))
        
        # 5. إنشاء جدول جلسات المستخدمين (اختياري)
        print("🔐 إنشاء جدول جلسات المستخدمين...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token VARCHAR(255) UNIQUE NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # حفظ التغييرات
        conn.commit()
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        
        # عرض إحصائيات
        cursor.execute("SELECT COUNT(*) FROM roles")
        roles_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        print(f"📊 الإحصائيات:")
        print(f"   - عدد الأدوار: {roles_count}")
        print(f"   - عدد المستخدمين: {users_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
        
        # استعادة النسخة الاحتياطية
        if backup_file and os.path.exists(backup_file):
            import shutil
            shutil.copy2(backup_file, 'accounting.db')
            print(f"🔄 تم استعادة النسخة الاحتياطية: {backup_file}")
        
        return False
        
    finally:
        conn.close()

def verify_migration():
    """التحقق من نجاح التحديث"""
    try:
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        print("🔍 التحقق من التحديث...")
        
        # التحقق من جدول الأدوار
        cursor.execute("SELECT name, name_ar FROM roles")
        roles = cursor.fetchall()
        print(f"✅ الأدوار المتاحة: {len(roles)}")
        for role in roles:
            print(f"   - {role[1]} ({role[0]})")
        
        # التحقق من المستخدمين
        cursor.execute("""
            SELECT u.username, u.full_name, r.name_ar 
            FROM users u 
            LEFT JOIN roles r ON u.role_id = r.id
        """)
        users = cursor.fetchall()
        print(f"✅ المستخدمين: {len(users)}")
        for user in users:
            role_name = user[2] if user[2] else user[0]  # fallback to old role
            print(f"   - {user[1]} ({user[0]}) - {role_name}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في التحقق: {e}")
        return False

if __name__ == '__main__':
    print("🚀 بدء تحديث قاعدة البيانات لنظام الصلاحيات")
    print("=" * 50)

    # التحقق من وجود قاعدة البيانات
    if not os.path.exists('accounting.db'):
        print("❌ لم يتم العثور على قاعدة البيانات accounting.db")
        print("🔄 يرجى تشغيل التطبيق أولاً لإنشاء قاعدة البيانات")
        exit(1)

    if migrate_database():
        print("\n" + "=" * 50)
        verify_migration()
        print("\n✅ تم تحديث قاعدة البيانات بنجاح!")
        print("🔄 يمكنك الآن إعادة تشغيل التطبيق")
    else:
        print("\n❌ فشل في تحديث قاعدة البيانات")
        print("🔄 يرجى مراجعة الأخطاء أعلاه")
