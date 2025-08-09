#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة أعمدة المدفوعات مباشرة لقاعدة البيانات
Direct migration to add payment columns
"""

import sqlite3
import os

def add_payment_columns():
    """إضافة أعمدة المدفوعات مباشرة"""

    # البحث عن قاعدة البيانات في المواقع المختلفة
    db_paths = [
        'accounting_system.db',
        'instance/accounting.db',
        'instance/accounting_system.db',
        'accounting.db'
    ]

    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        print("❌ قاعدة البيانات غير موجودة في أي من المواقع المتوقعة")
        print(f"🔍 المواقع المفحوصة: {db_paths}")
        return False

    print(f"📍 تم العثور على قاعدة البيانات في: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 إضافة أعمدة المدفوعات...")
        
        # قائمة الجداول والأعمدة المطلوبة
        tables_to_update = ['sale', 'purchase', 'expense', 'payroll']
        payment_columns = [
            "payment_status VARCHAR(20) DEFAULT 'unpaid'",
            "paid_amount FLOAT DEFAULT 0",
            "payment_date DATETIME",
            "payment_method VARCHAR(50)"
        ]
        
        for table in tables_to_update:
            print(f"📋 تحديث جدول {table}:")
            
            # فحص وجود الجدول
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                print(f"  ⚠️ جدول {table} غير موجود")
                continue
            
            # إضافة كل عمود
            for column_def in payment_columns:
                column_name = column_def.split()[0]
                try:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
                    print(f"  ✅ تم إضافة عمود {column_name}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"  ⚠️ عمود {column_name} موجود بالفعل")
                    else:
                        print(f"  ❌ خطأ في إضافة {column_name}: {e}")
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print("💾 تم حفظ جميع التغييرات")
        return True
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def verify_columns():
    """التحقق من الأعمدة المضافة"""

    # البحث عن قاعدة البيانات
    db_paths = ['accounting_system.db', 'instance/accounting.db', 'instance/accounting_system.db', 'accounting.db']
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        print("❌ قاعدة البيانات غير موجودة")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        tables = ['sale', 'purchase', 'expense', 'payroll']
        payment_fields = ['payment_status', 'paid_amount', 'payment_date', 'payment_method']
        
        print("🔍 التحقق من الأعمدة المضافة:")
        
        all_good = True
        
        for table in tables:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                print(f"  ⚠️ جدول {table} غير موجود")
                continue
                
            print(f"📋 جدول {table}:")
            
            # الحصول على معلومات الأعمدة
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [column[1] for column in cursor.fetchall()]
            
            for field in payment_fields:
                if field in columns:
                    print(f"  ✅ {field}")
                else:
                    print(f"  ❌ {field} - مفقود")
                    all_good = False
        
        conn.close()
        
        if all_good:
            print("🎉 جميع أعمدة المدفوعات موجودة!")
        else:
            print("⚠️ بعض الأعمدة مفقودة")
            
        return all_good
        
    except Exception as e:
        print(f"❌ خطأ في التحقق: {e}")
        return False

if __name__ == "__main__":
    print("🚀 إضافة أعمدة نظام المدفوعات")
    print("=" * 40)
    
    if add_payment_columns():
        print()
        verify_columns()
        print()
        print("🎉 تم إكمال العملية بنجاح!")
        print("🔗 النظام الآن جاهز للربط مع شاشة المدفوعات")
    else:
        print("❌ فشل في إضافة الأعمدة")
