#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص قاعدة البيانات
Database Check Script
"""

import sqlite3
import os

def check_database():
    """فحص قاعدة البيانات الحالية"""
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 الجداول الموجودة في قاعدة البيانات:")
        print("=" * 50)
        
        for table in tables:
            table_name = table[0]
            print(f"\n🗂️ جدول: {table_name}")
            
            # الحصول على معلومات الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("   الأعمدة:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default_val}" if default_val else ""
                print(f"   - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
            
            # عدد الصفوف
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   📊 عدد الصفوف: {count}")
        
        print("\n" + "=" * 50)
        print(f"📈 إجمالي الجداول: {len(tables)}")
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database()
