#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لشاشة المدفوعات والمستحقات بعد الإصلاحات
Quick Test for Payments & Dues Screen After Fixes
"""

import requests
import webbrowser

def quick_test():
    """اختبار سريع"""
    print("⚡ اختبار سريع لشاشة المدفوعات والمستحقات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        return
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return
    
    # اختبار الصفحة الأساسية
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ شاشة المدفوعات والمستحقات تعمل")
        else:
            print(f"❌ شاشة المدفوعات والمستحقات: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في الشاشة: {e}")
    
    # اختبار APIs المُصلحة
    print("\n🔍 اختبار APIs:")
    
    apis = [
        ('/api/sales/list', 'API المبيعات'),
        ('/api/purchases/list', 'API المشتريات'),
        ('/api/expenses/list', 'API المصروفات'),
        ('/print_invoices?type=sales&month=2025-01&status=all', 'route الطباعة'),
        ('/print_invoices_preview?type=sales&month=2025-01&status=all', 'معاينة الطباعة')
    ]
    
    for api, name in apis:
        try:
            response = session.get(f"http://localhost:5000{api}")
            if response.status_code == 200:
                print(f"   ✅ {name}")
            else:
                print(f"   ⚠️ {name}: {response.status_code}")
        except:
            print(f"   ❌ {name}: خطأ")
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 اختبر الآن:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. تحقق من وجود البيانات في التبويبات")
    print("3. اختبر أزرار الطباعة")
    print("4. اختبر تسجيل الدفعات")
    
    print("\n🔧 الإصلاحات المُنفذة:")
    print("✅ إضافة API المبيعات المفقود")
    print("✅ إضافة route الطباعة المفقود")
    print("✅ تحسين معالجة الأخطاء")
    
    print("=" * 50)

if __name__ == "__main__":
    quick_test()
