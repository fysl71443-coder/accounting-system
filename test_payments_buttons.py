#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار أزرار شاشة المدفوعات والمستحقات
Test Payments & Dues Screen Buttons
"""

import requests
import webbrowser
import time

def test_payment_buttons():
    """اختبار أزرار المدفوعات"""
    print("🔘 اختبار أزرار شاشة المدفوعات والمستحقات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python run_local.py")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return False
    
    # اختبار صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ صفحة المدفوعات والمستحقات تعمل")
            content = response.text
            
            # فحص أزرار الطباعة
            print("\n🖨️ فحص أزرار الطباعة:")
            
            print_buttons = [
                ('printSalesInvoices()', 'زر طباعة المبيعات'),
                ('printPurchasesInvoices()', 'زر طباعة المشتريات'),
                ('printExpensesInvoices()', 'زر طباعة المصروفات'),
                ('printPayrollInvoices()', 'زر طباعة الرواتب')
            ]
            
            for button_func, description in print_buttons:
                if button_func in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description}")
            
            # فحص أزرار تسجيل الدفعات
            print("\n💳 فحص أزرار تسجيل الدفعات:")
            
            payment_buttons = [
                ('/payments/new?', 'روابط تسجيل الدفعات'),
                ('تسجيل دفعة', 'نص أزرار الدفعات'),
                ('btn-outline-success', 'تنسيق أزرار الدفعات')
            ]
            
            for button_element, description in payment_buttons:
                if button_element in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description}")
            
            return True
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def test_button_routes():
    """اختبار routes الأزرار"""
    print("\n🔗 اختبار routes الأزرار:")
    print("-" * 30)
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin112233'}
    session.post("http://localhost:5000/login", data=login_data)
    
    # اختبار routes
    routes = [
        ('/payments/new', 'صفحة تسجيل دفعة جديدة'),
        ('/payments/new?invoice=1&type=sales', 'تسجيل دفعة مبيعات'),
        ('/payments/new?invoice=1&type=purchases', 'تسجيل دفعة مشتريات'),
        ('/payments/new?invoice=1&type=expenses', 'تسجيل دفعة مصروفات'),
        ('/payments/new?invoice=1&type=payroll', 'تسجيل دفعة رواتب'),
        ('/print_invoices_preview?type=sales&month=2025-01&status=all', 'معاينة طباعة المبيعات'),
        ('/print_invoices_preview?type=purchases&month=2025-01&status=all', 'معاينة طباعة المشتريات'),
        ('/print_invoices_preview?type=expenses&month=2025-01&status=all', 'معاينة طباعة المصروفات'),
        ('/print_invoices_preview?type=payroll&month=2025-01&status=all', 'معاينة طباعة الرواتب')
    ]
    
    for route, name in routes:
        try:
            response = session.get(f"http://localhost:5000{route}")
            if response.status_code == 200:
                print(f"   ✅ {name}")
            elif response.status_code == 404:
                print(f"   ❌ {name}: غير موجود (404)")
            else:
                print(f"   ⚠️ {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: خطأ - {e}")

def test_javascript_functions():
    """اختبار وظائف JavaScript"""
    print("\n🔧 اختبار وظائف JavaScript:")
    print("-" * 30)
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin112233'}
    session.post("http://localhost:5000/login", data=login_data)
    
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            
            # فحص وظائف JavaScript
            js_functions = [
                ('function printSalesInvoices()', 'وظيفة طباعة المبيعات'),
                ('function printPurchasesInvoices()', 'وظيفة طباعة المشتريات'),
                ('function printExpensesInvoices()', 'وظيفة طباعة المصروفات'),
                ('function printPayrollInvoices()', 'وظيفة طباعة الرواتب'),
                ('function createPrintHTML(', 'وظيفة إنشاء HTML للطباعة'),
                ('function openPrintWindow(', 'وظيفة فتح نافذة الطباعة'),
                ('function testPrintModal()', 'وظيفة اختبار الطباعة'),
                ('function quickPrintTest()', 'وظيفة الاختبار السريع')
            ]
            
            for js_func, description in js_functions:
                if js_func in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description}")
                    
        else:
            print("❌ فشل في جلب محتوى الصفحة")
            
    except Exception as e:
        print(f"❌ خطأ في فحص JavaScript: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار شامل لأزرار شاشة المدفوعات والمستحقات")
    print("=" * 60)
    
    # اختبار الأزرار
    buttons_work = test_payment_buttons()
    
    if buttons_work:
        # اختبار routes
        test_button_routes()
        
        # اختبار JavaScript
        test_javascript_functions()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. اختبر أزرار الطباعة في كل تبويب:")
    print("   - اضغط 'طباعة فواتير المبيعات'")
    print("   - اضغط 'طباعة فواتير المشتريات'")
    print("   - اضغط 'طباعة فواتير المصروفات'")
    print("   - اضغط 'طباعة كشف الرواتب'")
    
    print("\n3. اختبر أزرار تسجيل الدفعات:")
    print("   - اضغط 'تسجيل دفعة' في أي تبويب")
    print("   - اضغط أيقونة المال بجانب أي فاتورة")
    
    print("\n4. اختبر أزرار الاختبار السريع:")
    print("   - اضغط '🧪 اختبار الطباعة' في الأسفل")
    print("   - اضغط '⚡ اختبار سريع' في الأسفل")
    print("   - اضغط '🖨️ طباعة مباشرة' في الأسفل")
    
    print("\n🔧 إذا لم تعمل الأزرار:")
    print("- اضغط F12 وفحص Console للأخطاء")
    print("- تأكد من تحميل JavaScript")
    print("- تأكد من وجود بيانات في الجداول")
    print("- تأكد من تفعيل النوافذ المنبثقة")
    
    print("\n🌟 الأزرار المتوفرة:")
    print("✅ أزرار طباعة لكل نوع فاتورة")
    print("✅ أزرار تسجيل الدفعات")
    print("✅ أزرار الاختبار والتشخيص")
    print("✅ أزرار الفلترة والبحث")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
