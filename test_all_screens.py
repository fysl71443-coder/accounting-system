#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لجميع الشاشات والقوالب
Complete Test for All Screens and Templates
"""

import requests
import time
from datetime import datetime

# إعدادات الاختبار
BASE_URL = "http://localhost:5000"
TEST_USER = "admin"
TEST_PASS = "admin112233"

# قائمة جميع الشاشات للاختبار
SCREENS_TO_TEST = [
    "/",
    "/login",
    "/dashboard", 
    "/sales",
    "/purchases",
    "/expenses",
    "/products",
    "/inventory",
    "/customers",
    "/suppliers",
    "/payments_dues",
    "/reports",
    "/financial_statements",
    "/tax_management",
    "/employee_payroll",
    "/user_management",
    "/settings",
    "/advanced_reports",
    "/cost_calculation",
    "/meal_cost_calculator",

    "/raw_materials",
    "/product_transfer",
    "/advanced_expenses",
    "/role_management"
]

def test_screen(url):
    """اختبار شاشة واحدة"""
    try:
        response = requests.get(f"{BASE_URL}{url}", timeout=10)
        
        if response.status_code == 200:
            return {
                'url': url,
                'status': '✅ يعمل',
                'status_code': response.status_code,
                'size': len(response.content),
                'time': response.elapsed.total_seconds()
            }
        elif response.status_code == 302:
            return {
                'url': url,
                'status': '🔄 إعادة توجيه',
                'status_code': response.status_code,
                'redirect': response.headers.get('Location', ''),
                'time': response.elapsed.total_seconds()
            }
        else:
            return {
                'url': url,
                'status': '❌ خطأ',
                'status_code': response.status_code,
                'time': response.elapsed.total_seconds()
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status': '❌ فشل الاتصال',
            'error': str(e)
        }

def run_complete_test():
    """تشغيل اختبار شامل لجميع الشاشات"""
    print("🚀 بدء الاختبار الشامل لجميع الشاشات...")
    print("=" * 70)
    
    results = []
    working_screens = 0
    total_screens = len(SCREENS_TO_TEST)
    
    for screen in SCREENS_TO_TEST:
        print(f"🔍 اختبار: {screen}")
        result = test_screen(screen)
        results.append(result)
        
        if result['status'] in ['✅ يعمل', '🔄 إعادة توجيه']:
            working_screens += 1
            
        print(f"   النتيجة: {result['status']}")
        time.sleep(0.5)  # توقف قصير بين الاختبارات
    
    print("\n" + "=" * 70)
    print("📊 ملخص نتائج الاختبار:")
    print("=" * 70)
    
    for result in results:
        status_icon = "✅" if result['status'] == '✅ يعمل' else "🔄" if result['status'] == '🔄 إعادة توجيه' else "❌"
        print(f"{status_icon} {result['url']:<25} | {result['status']}")
    
    print("\n" + "=" * 70)
    print("🎯 النتيجة النهائية:")
    print("=" * 70)
    print(f"✅ الشاشات العاملة: {working_screens}/{total_screens}")
    print(f"📊 نسبة النجاح: {(working_screens/total_screens)*100:.1f}%")
    
    if working_screens == total_screens:
        print("🎉 تهانينا! جميع الشاشات تعمل بشكل مثالي!")
    elif working_screens >= total_screens * 0.9:
        print("👍 ممتاز! معظم الشاشات تعمل بشكل جيد")
    else:
        print("⚠️ يحتاج بعض الشاشات إلى مراجعة")
    
    print(f"⏰ وقت الاختبار: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return results

def test_specific_features():
    """اختبار مميزات محددة"""
    print("\n🔧 اختبار المميزات المتقدمة:")
    print("-" * 50)
    
    # اختبار تغيير اللغة
    try:
        response = requests.post(f"{BASE_URL}/change_language", 
                               json={'language': 'en'}, 
                               timeout=5)
        if response.status_code == 200:
            print("✅ تغيير اللغة: يعمل")
        else:
            print("❌ تغيير اللغة: لا يعمل")
    except:
        print("❌ تغيير اللغة: فشل الاتصال")
    
    # اختبار الطباعة
    print_urls = [
        "/print_invoices/sales",
        "/print_invoices/purchases", 
        "/print_invoices/expenses",
        "/print_invoices/payroll"
    ]
    
    for url in print_urls:
        try:
            response = requests.get(f"{BASE_URL}{url}", timeout=5)
            if response.status_code in [200, 302]:
                print(f"✅ طباعة {url.split('/')[-1]}: يعمل")
            else:
                print(f"❌ طباعة {url.split('/')[-1]}: لا يعمل")
        except:
            print(f"❌ طباعة {url.split('/')[-1]}: فشل الاتصال")

if __name__ == "__main__":
    print("🎯 اختبار شامل لنظام المحاسبة المتكامل")
    print("=" * 70)
    print(f"🌐 الخادم: {BASE_URL}")
    print(f"⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # تشغيل الاختبار الشامل
    results = run_complete_test()
    
    # اختبار المميزات المتقدمة
    test_specific_features()
    
    print("\n🏁 انتهى الاختبار الشامل")
    print("=" * 70)
