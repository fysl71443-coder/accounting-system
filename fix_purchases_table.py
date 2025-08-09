#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح جدول المشتريات
Fix Purchases Table Script
"""

import sqlite3
import os
from datetime import datetime

def check_purchases_table():
    """فحص جدول المشتريات الحالي"""
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("🔍 فحص جدول المشتريات الحالي:")
        print("=" * 40)
        
        # فحص الأعمدة الموجودة
        cursor.execute("PRAGMA table_info(purchases)")
        columns = cursor.fetchall()
        
        print("الأعمدة الموجودة:")
        existing_columns = []
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            existing_columns.append(col_name)
            pk_str = " (PRIMARY KEY)" if pk else ""
            not_null_str = " NOT NULL" if not_null else ""
            default_str = f" DEFAULT {default_val}" if default_val else ""
            print(f"   - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
        
        # فحص الأعمدة المطلوبة
        required_columns = ['supplier_id', 'subtotal', 'discount_amount']
        missing_columns = []
        
        print(f"\nالأعمدة المطلوبة:")
        for col in required_columns:
            if col in existing_columns:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ {col} (مفقود)")
                missing_columns.append(col)
        
        return missing_columns
        
    except Exception as e:
        print(f"❌ خطأ في فحص الجدول: {e}")
        return []
    finally:
        conn.close()

def fix_purchases_table():
    """إصلاح جدول المشتريات"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("\n🔧 إصلاح جدول المشتريات:")
        print("=" * 40)
        
        # فحص الأعمدة الموجودة
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
        
        # تحديث البيانات الموجودة
        if 'total_amount' in columns:
            # نقل البيانات من total_amount إلى subtotal إذا كان subtotal فارغاً
            cursor.execute('''
                UPDATE purchases 
                SET subtotal = COALESCE(total_amount, 0.0)
                WHERE subtotal IS NULL OR subtotal = 0
            ''')
            print("✅ تم نقل البيانات من total_amount إلى subtotal")
            
            # تحديث final_amount ليكون subtotal + tax_amount - discount_amount
            cursor.execute('''
                UPDATE purchases 
                SET final_amount = COALESCE(subtotal, 0.0) + COALESCE(tax_amount, 0.0) - COALESCE(discount_amount, 0.0)
            ''')
            print("✅ تم تحديث final_amount")
        
        conn.commit()
        print("✅ تم إصلاح جدول المشتريات بنجاح!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ خطأ في إصلاح الجدول: {e}")
        raise
    finally:
        conn.close()

def verify_fix():
    """التحقق من الإصلاح"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("\n✅ التحقق من الإصلاح:")
        print("=" * 40)
        
        # فحص الأعمدة بعد الإصلاح
        cursor.execute("PRAGMA table_info(purchases)")
        columns = cursor.fetchall()
        
        required_columns = ['supplier_id', 'subtotal', 'discount_amount']
        all_present = True
        
        for req_col in required_columns:
            found = any(col[1] == req_col for col in columns)
            if found:
                print(f"   ✅ {req_col}")
            else:
                print(f"   ❌ {req_col}")
                all_present = False
        
        if all_present:
            print("\n🎉 جميع الأعمدة المطلوبة موجودة!")
            
            # اختبار استعلام بسيط
            cursor.execute("SELECT COUNT(*) FROM purchases")
            count = cursor.fetchone()[0]
            print(f"📊 عدد السجلات في الجدول: {count}")
            
            return True
        else:
            print("\n❌ بعض الأعمدة ما زالت مفقودة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في التحقق: {e}")
        return False
    finally:
        conn.close()

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔧 إصلاح جدول المشتريات - Fix Purchases Table")
    print("=" * 60)
    
    # فحص الجدول الحالي
    missing_columns = check_purchases_table()
    
    if not missing_columns:
        print("\n✅ جدول المشتريات سليم - لا يحتاج إصلاح")
        return
    
    print(f"\n⚠️ الأعمدة المفقودة: {', '.join(missing_columns)}")
    
    # إصلاح الجدول
    try:
        fix_purchases_table()
        
        # التحقق من الإصلاح
        if verify_fix():
            print("\n" + "=" * 60)
            print("✅ تم إصلاح جدول المشتريات بنجاح!")
            print("✅ Purchases table fixed successfully!")
            print("🚀 يمكن الآن تشغيل النظام بدون أخطاء")
            print("=" * 60)
        else:
            print("\n❌ فشل في التحقق من الإصلاح")
            
    except Exception as e:
        print(f"\n❌ فشل في إصلاح الجدول: {e}")

if __name__ == "__main__":
    main()
