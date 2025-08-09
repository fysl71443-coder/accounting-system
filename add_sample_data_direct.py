#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة بيانات عينة مباشرة لقاعدة البيانات
Add Sample Data Directly to Database
"""

import sqlite3
from datetime import datetime, timedelta

def add_sample_data():
    """إضافة بيانات عينة لقاعدة البيانات"""
    print("🏗️ إضافة بيانات عينة لقاعدة البيانات...")
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        # إضافة عملاء
        print("👥 إضافة عملاء:")
        customers = [
            ('شركة الأمل التجارية', '0501234567', 'amal@company.com'),
            ('مؤسسة النور للتجارة', '0507654321', 'noor@trade.com'),
            ('شركة الفجر الجديد', '0509876543', 'fajr@new.com'),
            ('مؤسسة الرياض التجارية', '0551234567', 'riyadh@trade.com')
        ]
        
        for name, phone, email in customers:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO customer (name, phone, email) 
                    VALUES (?, ?, ?)
                """, (name, phone, email))
                print(f"  ✅ {name}")
            except:
                pass
        
        # إضافة موردين
        print("\n🏭 إضافة موردين:")
        suppliers = [
            ('مورد المواد الأولية', '0551234567', 'materials@supplier.com'),
            ('شركة التوريدات المتقدمة', '0557654321', 'advanced@supply.com'),
            ('مؤسسة الإمدادات الشاملة', '0559876543', 'comprehensive@supply.com')
        ]
        
        for name, phone, email in suppliers:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO supplier (name, phone, email) 
                    VALUES (?, ?, ?)
                """, (name, phone, email))
                print(f"  ✅ {name}")
            except:
                pass
        
        # إضافة مبيعات
        print("\n💰 إضافة مبيعات:")
        sales_data = [
            (5000, 250, 4750, 'مبيعة كبيرة مع خصم', 'paid'),
            (2500, 100, 2400, 'مبيعة متوسطة', 'unpaid'),
            (1200, 0, 1200, 'مبيعة صغيرة بدون خصم', 'paid'),
            (8000, 500, 7500, 'مبيعة كبيرة جداً', 'partial'),
            (3200, 150, 3050, 'مبيعة عادية', 'unpaid')
        ]
        
        for i, (subtotal, discount, total, notes, status) in enumerate(sales_data):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            customer_id = (i % 4) + 1  # توزيع على العملاء
            
            try:
                cursor.execute("""
                    INSERT INTO sale (date, customer_id, subtotal, discount, total, notes, payment_status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (date, customer_id, subtotal, discount, total, notes, status))
                print(f"  ✅ مبيعة {total} ريال - {status}")
            except Exception as e:
                print(f"  ❌ خطأ في المبيعة: {e}")
        
        # إضافة مشتريات
        print("\n🛒 إضافة مشتريات:")
        purchases_data = [
            (3000, 150, 2850, 'شراء مواد أولية', 'paid'),
            (1800, 50, 1750, 'شراء معدات مكتبية', 'unpaid'),
            (4500, 200, 4300, 'شراء أجهزة كمبيوتر', 'partial'),
            (2200, 100, 2100, 'شراء أثاث مكتبي', 'paid')
        ]
        
        for i, (subtotal, discount, total, notes, status) in enumerate(purchases_data):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            supplier_id = (i % 3) + 1  # توزيع على الموردين
            
            try:
                cursor.execute("""
                    INSERT INTO purchase (date, supplier_id, subtotal, discount, total, notes, payment_status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (date, supplier_id, subtotal, discount, total, notes, status))
                print(f"  ✅ مشتريات {total} ريال - {status}")
            except Exception as e:
                print(f"  ❌ خطأ في المشتريات: {e}")
        
        # إضافة مصروفات
        print("\n📄 إضافة مصروفات:")
        expenses_data = [
            ('إيجار المكتب', 3000, 'rent', 'paid'),
            ('فواتير الكهرباء', 800, 'utilities', 'paid'),
            ('مواد مكتبية', 450, 'office_supplies', 'unpaid'),
            ('صيانة الأجهزة', 1200, 'maintenance', 'partial'),
            ('اشتراك الإنترنت', 300, 'utilities', 'paid')
        ]
        
        for i, (description, amount, category, status) in enumerate(expenses_data):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                cursor.execute("""
                    INSERT INTO expense (date, description, amount, category, payment_status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (date, description, amount, category, status))
                print(f"  ✅ {description} - {amount} ريال - {status}")
            except Exception as e:
                print(f"  ❌ خطأ في المصروف: {e}")
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print("\n🎉 تم إنشاء جميع البيانات العينة بنجاح!")
        print("📊 يمكنك الآن اختبار التقارير مع البيانات الحقيقية")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء البيانات: {e}")
        return False

if __name__ == "__main__":
    add_sample_data()
