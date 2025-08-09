#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص البيانات المحفوظة في قاعدة البيانات
Check Saved Data in Database
"""

import sqlite3
import os
from datetime import datetime

def check_purchases_data():
    """فحص بيانات المشتريات المحفوظة"""
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("🔍 فحص بيانات المشتريات:")
        print("=" * 50)
        
        # فحص جدول المشتريات
        cursor.execute("SELECT COUNT(*) FROM purchases")
        purchases_count = cursor.fetchone()[0]
        print(f"📊 عدد فواتير المشتريات: {purchases_count}")
        
        if purchases_count > 0:
            print("\n📋 آخر 5 فواتير مشتريات:")
            cursor.execute("""
                SELECT id, invoice_number, supplier_name, invoice_date, 
                       total_amount, final_amount, payment_status, created_at
                FROM purchases 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            purchases = cursor.fetchall()
            for purchase in purchases:
                id, invoice_num, supplier, date, total, final, status, created = purchase
                print(f"   🧾 {invoice_num}: {supplier} - {final} ريال ({status}) - {created}")
        
        # فحص جدول عناصر المشتريات
        cursor.execute("SELECT COUNT(*) FROM purchase_items")
        items_count = cursor.fetchone()[0]
        print(f"\n📦 عدد عناصر المشتريات: {items_count}")
        
        if items_count > 0:
            print("\n📋 آخر 10 عناصر مشتريات:")
            cursor.execute("""
                SELECT pi.id, pi.purchase_id, pi.product_name, pi.quantity, 
                       pi.unit_price, pi.total_price, p.invoice_number
                FROM purchase_items pi
                LEFT JOIN purchases p ON pi.purchase_id = p.id
                ORDER BY pi.id DESC 
                LIMIT 10
            """)
            
            items = cursor.fetchall()
            for item in items:
                id, purchase_id, product, qty, price, total, invoice = item
                print(f"   📦 {product}: {qty} × {price} = {total} ريال (فاتورة: {invoice})")
        
        # إحصائيات إضافية
        print(f"\n📈 إحصائيات:")
        
        # إجمالي المبيعات
        cursor.execute("SELECT SUM(final_amount) FROM purchases WHERE payment_status != 'cancelled'")
        total_purchases = cursor.fetchone()[0] or 0
        print(f"   💰 إجمالي المشتريات: {total_purchases:.2f} ريال")
        
        # حسب حالة الدفع
        cursor.execute("""
            SELECT payment_status, COUNT(*), SUM(final_amount) 
            FROM purchases 
            GROUP BY payment_status
        """)
        status_stats = cursor.fetchall()
        for status, count, amount in status_stats:
            print(f"   📊 {status}: {count} فاتورة - {amount:.2f} ريال")
        
        # آخر فاتورة
        cursor.execute("""
            SELECT invoice_number, supplier_name, final_amount, created_at
            FROM purchases 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        last_purchase = cursor.fetchone()
        if last_purchase:
            invoice, supplier, amount, created = last_purchase
            print(f"\n🕒 آخر فاتورة: {invoice} - {supplier} - {amount} ريال - {created}")
        
    except Exception as e:
        print(f"❌ خطأ في فحص البيانات: {e}")
    finally:
        conn.close()

def check_database_structure():
    """فحص هيكل قاعدة البيانات"""
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("\n🏗️ فحص هيكل قاعدة البيانات:")
        print("=" * 50)
        
        # فحص جدول المشتريات
        print("📋 جدول المشتريات (purchases):")
        cursor.execute("PRAGMA table_info(purchases)")
        columns = cursor.fetchall()
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            pk_str = " (PRIMARY KEY)" if pk else ""
            not_null_str = " NOT NULL" if not_null else ""
            default_str = f" DEFAULT {default_val}" if default_val else ""
            print(f"   - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
        
        # فحص جدول عناصر المشتريات
        print(f"\n📦 جدول عناصر المشتريات (purchase_items):")
        cursor.execute("PRAGMA table_info(purchase_items)")
        columns = cursor.fetchall()
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            pk_str = " (PRIMARY KEY)" if pk else ""
            not_null_str = " NOT NULL" if not_null else ""
            default_str = f" DEFAULT {default_val}" if default_val else ""
            print(f"   - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
        
    except Exception as e:
        print(f"❌ خطأ في فحص الهيكل: {e}")
    finally:
        conn.close()

def test_insert_sample():
    """اختبار إدراج بيانات تجريبية"""
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return
    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        print("\n🧪 اختبار إدراج بيانات تجريبية:")
        print("=" * 50)
        
        # إدراج فاتورة تجريبية
        test_invoice = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cursor.execute("""
            INSERT INTO purchases (
                invoice_number, supplier_name, invoice_date, 
                total_amount, tax_amount, final_amount, 
                payment_method, payment_status, notes, 
                branch_id, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_invoice, 'مورد تجريبي', datetime.now().date(),
            100.0, 15.0, 115.0,
            'نقدي', 'pending', 'فاتورة تجريبية',
            1, 1, datetime.now()
        ))
        
        purchase_id = cursor.lastrowid
        print(f"✅ تم إدراج فاتورة تجريبية: {test_invoice} (ID: {purchase_id})")
        
        # إدراج عنصر تجريبي
        cursor.execute("""
            INSERT INTO purchase_items (
                purchase_id, product_name, quantity, 
                unit_price, total_price, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            purchase_id, 'منتج تجريبي', 2.0,
            50.0, 100.0, datetime.now()
        ))
        
        print(f"✅ تم إدراج عنصر تجريبي للفاتورة")
        
        conn.commit()
        print("✅ تم حفظ البيانات التجريبية بنجاح")
        
        # التحقق من الإدراج
        cursor.execute("SELECT COUNT(*) FROM purchases WHERE invoice_number = ?", (test_invoice,))
        if cursor.fetchone()[0] > 0:
            print("✅ تم التحقق من وجود الفاتورة في قاعدة البيانات")
        else:
            print("❌ لم يتم العثور على الفاتورة في قاعدة البيانات")
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الإدراج: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔍 فحص البيانات المحفوظة - Check Saved Data")
    print("=" * 60)
    
    # فحص البيانات الموجودة
    check_purchases_data()
    
    # فحص هيكل قاعدة البيانات
    check_database_structure()
    
    # اختبار إدراج بيانات
    test_insert_sample()
    
    print("\n" + "=" * 60)
    print("✅ انتهى فحص البيانات")
    print("✅ Data check completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
