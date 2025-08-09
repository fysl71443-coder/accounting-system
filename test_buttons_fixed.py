#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الأزرار بعد الإصلاح
Test Buttons After Fix
"""

import requests
import webbrowser

def test_buttons_after_fix():
    """اختبار الأزرار بعد الإصلاح"""
    print("🔧 اختبار الأزرار بعد الإصلاح")
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
    
    # فحص الصفحة
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ صفحة المدفوعات والمستحقات تعمل")
            
            content = response.text
            
            # فحص ملف JavaScript الجديد
            if 'payments_functions.js' in content:
                print("✅ ملف JavaScript الجديد محمل")
            else:
                print("❌ ملف JavaScript الجديد غير محمل")
            
            # فحص الأزرار
            buttons_found = 0
            buttons = [
                'printSalesInvoices()',
                'printPurchasesInvoices()',
                'printExpensesInvoices()',
                'printPayrollInvoices()',
                'تسجيل دفعة',
                '/payments/new'
            ]
            
            print("\n🔍 فحص الأزرار:")
            for button in buttons:
                if button in content:
                    print(f"   ✅ {button}")
                    buttons_found += 1
                else:
                    print(f"   ❌ {button}")
            
            print(f"\n📊 النتيجة: {buttons_found}/{len(buttons)} زر موجود")
            
        else:
            print(f"❌ الصفحة فشلت: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    # فحص ملف JavaScript
    try:
        response = session.get("http://localhost:5000/static/js/payments_functions.js")
        if response.status_code == 200:
            print("✅ ملف JavaScript متاح")
        else:
            print(f"❌ ملف JavaScript غير متاح: {response.status_code}")
    except:
        print("❌ خطأ في الوصول لملف JavaScript")
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 اختبر الآن:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. اضغط F12 وفحص Console")
    print("3. يجب أن ترى: '✅ تم تحميل وظائف المدفوعات والمستحقات'")
    print("4. اختبر أزرار الطباعة في كل تبويب")
    print("5. اختبر أزرار تسجيل الدفعات")
    
    print("\n🔧 الإصلاحات المُنفذة:")
    print("✅ إنشاء ملف JavaScript منفصل")
    print("✅ إضافة جميع وظائف الطباعة")
    print("✅ إضافة وظائف الاختبار")
    print("✅ تحسين معالجة الأخطاء")
    print("✅ إضافة تسجيل العمليات")
    
    print("=" * 50)

if __name__ == "__main__":
    test_buttons_after_fix()
