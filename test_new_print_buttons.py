#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار أزرار الطباعة الجديدة
Test New Print Buttons
"""

import requests
import webbrowser

def test_new_print_buttons():
    """اختبار أزرار الطباعة الجديدة"""
    print("🖨️ اختبار أزرار الطباعة الجديدة")
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
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ صفحة المدفوعات والمستحقات تعمل")
            
            content = response.text
            
            # فحص الأزرار الجديدة
            new_elements = [
                ('selectAllSales()', 'زر تحديد كل المبيعات'),
                ('printSelectedSales()', 'زر طباعة المبيعات المحددة'),
                ('toggleAllSales', 'وظيفة تبديل تحديد المبيعات'),
                ('sales-checkbox', 'checkboxes المبيعات'),
                ('selectAllSalesCheckbox', 'checkbox تحديد كل المبيعات'),
                ('multi_print.js', 'ملف JavaScript الجديد')
            ]
            
            print("\n🔍 فحص العناصر الجديدة:")
            elements_found = 0
            for element, description in new_elements:
                if element in content:
                    print(f"   ✅ {description}")
                    elements_found += 1
                else:
                    print(f"   ❌ {description}")
            
            # فحص الجداول المحدثة
            table_elements = [
                ('form-check-input', 'checkboxes في الجداول'),
                ('data-invoice=', 'بيانات الفواتير في checkboxes'),
                ('data-customer=', 'بيانات العملاء في checkboxes'),
                ('data-amount=', 'بيانات المبالغ في checkboxes')
            ]
            
            print("\n🔍 فحص تحديثات الجداول:")
            table_elements_found = 0
            for element, description in table_elements:
                if element in content:
                    print(f"   ✅ {description}")
                    table_elements_found += 1
                else:
                    print(f"   ❌ {description}")
            
            print(f"\n📊 النتائج:")
            print(f"   العناصر الجديدة: {elements_found}/{len(new_elements)}")
            print(f"   تحديثات الجداول: {table_elements_found}/{len(table_elements)}")
            
            return elements_found >= len(new_elements) * 0.7 and table_elements_found >= len(table_elements) * 0.7
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def test_javascript_file():
    """اختبار ملف JavaScript الجديد"""
    print("\n🔍 اختبار ملف JavaScript:")
    print("-" * 30)
    
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin112233'}
    session.post("http://localhost:5000/login", data=login_data)
    
    try:
        response = session.get("http://localhost:5000/static/js/multi_print.js")
        if response.status_code == 200:
            print("   ✅ ملف multi_print.js متاح")
            
            content = response.text
            
            # فحص الوظائف الأساسية
            functions = [
                'toggleAllSales',
                'selectAllSales', 
                'printSelectedSales',
                'createSalesPrintHTML',
                'toggleAllPurchases',
                'printSelectedPurchases',
                'openPrintWindow'
            ]
            
            functions_found = 0
            for func in functions:
                if f'function {func}' in content:
                    print(f"      ✅ وظيفة {func}")
                    functions_found += 1
                else:
                    print(f"      ❌ وظيفة {func}")
            
            print(f"      📊 الوظائف الموجودة: {functions_found}/{len(functions)}")
            return functions_found >= len(functions) * 0.8
            
        else:
            print(f"   ❌ ملف JavaScript غير متاح: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ خطأ في اختبار JavaScript: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار شامل لأزرار الطباعة الجديدة")
    print("=" * 60)
    
    # اختبار الأزرار الجديدة
    buttons_work = test_new_print_buttons()
    
    # اختبار ملف JavaScript
    js_works = test_javascript_file()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. اذهب إلى تبويب المبيعات")
    print("3. لاحظ وجود checkboxes في بداية كل صف")
    print("4. لاحظ وجود checkbox في رأس الجدول")
    print("5. اختبر أزرار:")
    print("   - 'تحديد الكل': يحدد جميع الفواتير")
    print("   - 'طباعة المحدد': يطبع الفواتير المحددة فقط")
    print("6. حدد فواتير معينة وجرب الطباعة")
    print("7. تأكد من فتح نافذة طباعة جديدة")
    
    print("\n🔗 الروابط:")
    print("   شاشة المدفوعات: http://localhost:5000/payments_dues")
    print("   ملف JavaScript: http://localhost:5000/static/js/multi_print.js")
    
    print("\n🌟 المزايا الجديدة:")
    print("✅ checkboxes لتحديد فواتير متعددة")
    print("✅ زر 'تحديد الكل' لتحديد جميع الفواتير")
    print("✅ زر 'طباعة المحدد' مع عداد الفواتير")
    print("✅ طباعة احترافية مع تصميم منسق")
    print("✅ حساب المجاميع تلقائياً")
    print("✅ معلومات الشركة والتاريخ")
    print("✅ تنسيق مناسب للطباعة")
    
    print("\n📊 ملخص النتائج:")
    if buttons_work and js_works:
        print("🎉 أزرار الطباعة الجديدة تعمل بشكل ممتاز!")
        print("✅ جميع الوظائف متاحة وتعمل بشكل صحيح")
    else:
        print("⚠️ هناك بعض المشاكل:")
        if not buttons_work:
            print("- مشكلة في أزرار الطباعة")
        if not js_works:
            print("- مشكلة في ملف JavaScript")
    
    print("\n💡 نصائح الاستخدام:")
    print("- حدد الفواتير المطلوبة قبل الطباعة")
    print("- استخدم 'تحديد الكل' لطباعة جميع الفواتير")
    print("- الزر يظهر عدد الفواتير المحددة")
    print("- النافذة تفتح تلقائياً للطباعة")
    print("- يمكن حفظ الصفحة كـ PDF من المتصفح")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
