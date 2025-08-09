#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء بيانات بسيطة للاختبار
Simple Data Creator for Testing
"""

import sqlite3
from datetime import datetime, timedelta

def create_simple_data():
    """إنشاء بيانات بسيطة"""
    print("🏗️ إنشاء بيانات اختبار بسيطة...")
    
    try:
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        # إضافة عملاء
        print("👥 إضافة عملاء:")
        customers = [
            ('شركة الأمل التجارية', '0501234567', 'amal@company.com'),
            ('مؤسسة النور للتجارة', '0507654321', 'noor@trade.com'),
            ('شركة الفجر الجديد', '0509876543', 'fajr@new.com')
        ]
        
        for name, phone, email in customers:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO customer (name, phone, email) 
                    VALUES (?, ?, ?)
                """, (name, phone, email))
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ خطأ في العميل {name}: {e}")
        
        # إضافة موردين
        print("\n🏭 إضافة موردين:")
        suppliers = [
            ('مورد المواد الأولية', '0551234567', 'materials@supplier.com'),
            ('شركة التوريدات المتقدمة', '0557654321', 'advanced@supply.com')
        ]
        
        for name, phone, email in suppliers:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO supplier (name, phone, email) 
                    VALUES (?, ?, ?)
                """, (name, phone, email))
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ خطأ في المورد {name}: {e}")
        
        # إضافة مبيعات
        print("\n💰 إضافة مبيعات:")
        for i in range(5):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            customer_id = (i % 3) + 1
            subtotal = 1000 + (i * 500)
            discount = subtotal * 0.05  # خصم 5%
            total = subtotal - discount
            
            try:
                cursor.execute("""
                    INSERT INTO sale (customer_id, subtotal, discount, total, date, payment_status) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (customer_id, subtotal, discount, total, date, 'paid' if i % 2 == 0 else 'unpaid'))
                print(f"  ✅ مبيعة {total:.0f} ريال")
            except Exception as e:
                print(f"  ❌ خطأ في المبيعة: {e}")
        
        # إضافة مشتريات
        print("\n🛒 إضافة مشتريات:")
        for i in range(4):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            supplier_id = (i % 2) + 1
            subtotal = 800 + (i * 300)
            discount = subtotal * 0.03  # خصم 3%
            total = subtotal - discount
            
            try:
                cursor.execute("""
                    INSERT INTO purchase (supplier_id, subtotal, discount, total, date, payment_status) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (supplier_id, subtotal, discount, total, date, 'paid' if i % 3 == 0 else 'unpaid'))
                print(f"  ✅ مشتريات {total:.0f} ريال")
            except Exception as e:
                print(f"  ❌ خطأ في المشتريات: {e}")
        
        # إضافة مصروفات
        print("\n📄 إضافة مصروفات:")
        expenses = [
            ('إيجار المكتب', 3000, 'rent'),
            ('فواتير الكهرباء', 800, 'utilities'),
            ('مواد مكتبية', 450, 'office_supplies'),
            ('صيانة الأجهزة', 1200, 'maintenance')
        ]
        
        for i, (description, amount, category) in enumerate(expenses):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                cursor.execute("""
                    INSERT INTO expense (description, amount, category, date, payment_status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (description, amount, category, date, 'paid' if i % 2 == 0 else 'unpaid'))
                print(f"  ✅ {description} - {amount} ريال")
            except Exception as e:
                print(f"  ❌ خطأ في المصروف: {e}")
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print("\n🎉 تم إنشاء جميع البيانات بنجاح!")
        print("📊 يمكنك الآن اختبار التقارير")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

if __name__ == "__main__":
    create_simple_data()
