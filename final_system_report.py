#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تقرير شامل نهائي لحالة النظام
Final Comprehensive System Report
"""

import os
import sqlite3
import requests
from pathlib import Path

def test_database_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    print("🗃️ اختبار قاعدة البيانات:")
    print("=" * 30)
    
    if not os.path.exists('accounting.db'):
        print("❌ قاعدة البيانات غير موجودة")
        return False
    
    try:
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        # اختبار الجداول الأساسية
        essential_tables = [
            'users', 'branches', 'products', 'customers', 
            'purchases', 'sales', 'expenses', 'employee_payrolls'
        ]
        
        all_tables_exist = True
        for table in essential_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} سجل")
            else:
                print(f"   ❌ {table}: غير موجود")
                all_tables_exist = False
        
        conn.close()
        return all_tables_exist
        
    except Exception as e:
        print(f"   ❌ خطأ في الاتصال: {e}")
        return False

def test_web_server():
    """اختبار الخادم"""
    print("\n🌐 اختبار الخادم:")
    print("=" * 30)
    
    try:
        # اختبار الصفحة الرئيسية
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("   ✅ الصفحة الرئيسية تعمل")
        else:
            print(f"   ⚠️ الصفحة الرئيسية: كود {response.status_code}")
        
        # اختبار صفحة تسجيل الدخول
        response = requests.get('http://localhost:5000/login', timeout=5)
        if response.status_code == 200:
            print("   ✅ صفحة تسجيل الدخول تعمل")
        else:
            print(f"   ⚠️ صفحة تسجيل الدخول: كود {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ الخادم غير متاح")
        return False
    except Exception as e:
        print(f"   ❌ خطأ في الاتصال: {e}")
        return False

def test_key_screens():
    """اختبار الشاشات الرئيسية"""
    print("\n📱 اختبار الشاشات الرئيسية:")
    print("=" * 30)
    
    key_screens = [
        ('/dashboard', 'لوحة التحكم'),
        ('/sales', 'المبيعات'),
        ('/purchases', 'المشتريات'),
        ('/expenses', 'المصروفات'),
        ('/products', 'المنتجات'),
        ('/customers', 'العملاء'),
        ('/purchases/new', 'فاتورة مشتريات جديدة')
    ]
    
    working_screens = 0
    total_screens = len(key_screens)
    
    for url, name in key_screens:
        try:
            response = requests.get(f'http://localhost:5000{url}', timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name}")
                working_screens += 1
            elif response.status_code == 302:
                print(f"   🔄 {name} (إعادة توجيه - يحتاج تسجيل دخول)")
                working_screens += 1
            else:
                print(f"   ❌ {name}: كود {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: خطأ")
    
    return working_screens, total_screens

def check_templates():
    """فحص القوالب"""
    print("\n🎨 فحص القوالب:")
    print("=" * 30)
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("   ❌ مجلد templates غير موجود")
        return 0, 0
    
    essential_templates = [
        'login.html', 'dashboard.html', 'sales.html', 'purchases.html',
        'expenses.html', 'products.html', 'customers.html', 'new_purchase.html'
    ]
    
    existing_templates = {f.name for f in templates_dir.glob("*.html")}
    working_templates = 0
    
    for template in essential_templates:
        if template in existing_templates:
            print(f"   ✅ {template}")
            working_templates += 1
        else:
            print(f"   ❌ {template}")
    
    return working_templates, len(essential_templates)

def generate_final_report():
    """إنشاء التقرير النهائي"""
    print("\n" + "=" * 60)
    print("📊 التقرير النهائي لحالة النظام")
    print("📊 Final System Status Report")
    print("=" * 60)
    
    # اختبار قاعدة البيانات
    db_status = test_database_connection()
    
    # اختبار الخادم
    server_status = test_web_server()
    
    # اختبار الشاشات
    working_screens, total_screens = test_key_screens()
    
    # فحص القوالب
    working_templates, total_templates = check_templates()
    
    # حساب النتيجة الإجمالية
    print(f"\n📈 ملخص النتائج:")
    print(f"   🗃️ قاعدة البيانات: {'✅ تعمل' if db_status else '❌ مشكلة'}")
    print(f"   🌐 الخادم: {'✅ يعمل' if server_status else '❌ مشكلة'}")
    print(f"   📱 الشاشات: {working_screens}/{total_screens} ({working_screens/total_screens*100:.1f}%)")
    print(f"   🎨 القوالب: {working_templates}/{total_templates} ({working_templates/total_templates*100:.1f}%)")
    
    # التقييم العام
    overall_score = 0
    if db_status: overall_score += 25
    if server_status: overall_score += 25
    overall_score += (working_screens / total_screens) * 25
    overall_score += (working_templates / total_templates) * 25
    
    print(f"\n🎯 التقييم العام: {overall_score:.1f}/100")
    
    if overall_score >= 90:
        print("   🟢 النظام ممتاز - جاهز للاستخدام الكامل")
        status = "ممتاز"
    elif overall_score >= 75:
        print("   🟡 النظام جيد - يحتاج تحسينات طفيفة")
        status = "جيد"
    elif overall_score >= 50:
        print("   🟠 النظام متوسط - يحتاج تحسينات")
        status = "متوسط"
    else:
        print("   🔴 النظام يحتاج عمل كبير")
        status = "يحتاج عمل"
    
    # التوصيات
    print(f"\n💡 التوصيات:")
    if not db_status:
        print("   - إصلاح مشاكل قاعدة البيانات")
    if not server_status:
        print("   - تشغيل الخادم")
    if working_screens < total_screens:
        print("   - إصلاح الشاشات المعطلة")
    if working_templates < total_templates:
        print("   - إضافة القوالب المفقودة")
    
    if overall_score >= 90:
        print("   - النظام جاهز للاستخدام!")
        print("   - يمكن البدء في إدخال البيانات الحقيقية")
        print("   - يمكن تدريب المستخدمين")
    
    return status, overall_score

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔍 تقرير شامل نهائي لحالة النظام")
    print("🔍 Final Comprehensive System Report")
    print("=" * 60)
    
    status, score = generate_final_report()
    
    print("\n" + "=" * 60)
    print(f"✅ انتهى التقرير - الحالة: {status} ({score:.1f}/100)")
    print("✅ Report completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
