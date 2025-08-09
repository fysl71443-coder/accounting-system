#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test for Sales Screen Buttons
"""

import requests
import webbrowser

def quick_test():
    """اختبار سريع لأزرار شاشة المبيعات"""
    print("🧪 اختبار سريع لأزرار شاشة المبيعات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python start_server.py")
        return
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return
    
    # فحص صفحة المبيعات
    try:
        response = session.get("http://localhost:5000/sales")
        if response.status_code == 200:
            print("✅ صفحة المبيعات تعمل")
            
            content = response.text
            
            # فحص الأزرار المطلوبة
            buttons_found = 0
            required_buttons = [
                'btnSalesSave',
                'btnSalesEdit', 
                'btnSalesDelete',
                'btnSalesPreview',
                'btnSalesPrint',
                'btnSalesSelectInvoice',
                'btnSalesRegisterPayment'
            ]
            
            print("\n🔍 فحص الأزرار:")
            for button in required_buttons:
                if button in content:
                    print(f"   ✅ {button}")
                    buttons_found += 1
                else:
                    print(f"   ❌ {button}")
            
            # فحص الوظائف JavaScript
            functions_found = 0
            required_functions = [
                'SaveSalesRecord',
                'EditSalesRecord',
                'DeleteSalesRecord', 
                'PreviewSalesRecord',
                'PrintSalesRecord',
                'SelectSalesInvoice',
                'RegisterSalesPayment'
            ]
            
            print("\n🔍 فحص وظائف JavaScript:")
            for func in required_functions:
                if f'function {func}' in content:
                    print(f"   ✅ {func}")
                    functions_found += 1
                else:
                    print(f"   ❌ {func}")
            
            # فحص النافذة المنبثقة للدفع
            if 'paymentModal' in content:
                print("   ✅ نافذة تسجيل الدفع")
            else:
                print("   ❌ نافذة تسجيل الدفع")
            
            print(f"\n📊 النتيجة:")
            print(f"   الأزرار: {buttons_found}/{len(required_buttons)}")
            print(f"   الوظائف: {functions_found}/{len(required_functions)}")
            
            if buttons_found == len(required_buttons) and functions_found == len(required_functions):
                print("🎉 جميع الأزرار والوظائف موجودة!")
            else:
                print("⚠️ بعض الأزرار أو الوظائف مفقودة")
                
        else:
            print(f"❌ صفحة المبيعات فشلت: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في فحص صفحة المبيعات: {e}")
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/sales")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. سجل الدخول: admin / admin123")
    print("2. اذهب إلى صفحة المبيعات")
    print("3. حدد فاتورة (radio button)")
    print("4. اختبر كل زر:")
    print("   - حفظ: ينقل لصفحة فاتورة جديدة")
    print("   - تعديل: ينقل لصفحة التعديل")
    print("   - حذف: يحذف الفاتورة المحددة")
    print("   - معاينة: يفتح نافذة معاينة")
    print("   - طباعة: يفتح نافذة طباعة")
    print("   - اختيار فاتورة: يظهر معلومات الاختيار")
    print("   - تسجيل دفعة: يفتح نافذة تسجيل الدفع")
    
    print("\n🔗 الروابط:")
    print("   الصفحة الرئيسية: http://localhost:5000")
    print("   صفحة المبيعات: http://localhost:5000/sales")
    
    print("=" * 50)

if __name__ == "__main__":
    quick_test()
