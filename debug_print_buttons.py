#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص مشكلة أزرار الطباعة
Debug Print Buttons Issue
"""

import requests
import webbrowser
import re

def debug_print_buttons():
    """تشخيص مشكلة أزرار الطباعة"""
    print("🔍 تشخيص مشكلة أزرار الطباعة")
    print("=" * 50)
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return
    
    # جلب محتوى الصفحة
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            print("✅ تم جلب محتوى الصفحة")
            
            # فحص أزرار الطباعة
            print("\n🔍 البحث عن أزرار الطباعة:")
            
            # البحث عن أزرار onclick
            onclick_buttons = re.findall(r'onclick="([^"]*print[^"]*)"', content, re.IGNORECASE)
            print(f"📊 أزرار onclick الموجودة: {len(onclick_buttons)}")
            for i, button in enumerate(onclick_buttons[:5]):  # أول 5 أزرار
                print(f"   {i+1}. {button}")
            
            # البحث عن نص "طباعة"
            print_text_count = content.count('طباعة')
            print(f"📊 عدد مرات ظهور كلمة 'طباعة': {print_text_count}")
            
            # البحث عن ملف JavaScript
            if 'payments_functions.js' in content:
                print("✅ ملف JavaScript محمل")
            else:
                print("❌ ملف JavaScript غير محمل")
            
            # البحث عن وظائف JavaScript
            js_functions = [
                'printSalesInvoices',
                'printPurchasesInvoices', 
                'printExpensesInvoices',
                'printPayrollInvoices'
            ]
            
            print("\n🔍 البحث عن وظائف JavaScript:")
            for func in js_functions:
                if func in content:
                    print(f"   ✅ {func}")
                else:
                    print(f"   ❌ {func}")
            
            # فحص التبويبات
            print("\n🔍 فحص التبويبات:")
            tabs = ['sales-tab', 'purchases-tab', 'expenses-tab', 'payroll-tab']
            for tab in tabs:
                if tab in content:
                    print(f"   ✅ {tab}")
                else:
                    print(f"   ❌ {tab}")
            
            # حفظ جزء من المحتوى للفحص
            with open('debug_page_content.html', 'w', encoding='utf-8') as f:
                f.write(content[:5000])  # أول 5000 حرف
            print("💾 تم حفظ جزء من المحتوى في debug_page_content.html")
            
        else:
            print(f"❌ فشل جلب الصفحة: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

def test_javascript_file():
    """اختبار ملف JavaScript"""
    print("\n🔍 اختبار ملف JavaScript:")
    print("-" * 30)
    
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin123'}
    session.post("http://localhost:5000/login", data=login_data)
    
    try:
        response = session.get("http://localhost:5000/static/js/payments_functions.js")
        if response.status_code == 200:
            print("✅ ملف JavaScript متاح")
            content = response.text
            
            # فحص الوظائف
            functions = ['printSalesInvoices', 'printPurchasesInvoices', 'printExpensesInvoices', 'printPayrollInvoices']
            for func in functions:
                if f'function {func}' in content:
                    print(f"   ✅ وظيفة {func} موجودة")
                else:
                    print(f"   ❌ وظيفة {func} مفقودة")
                    
        else:
            print(f"❌ ملف JavaScript غير متاح: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في اختبار JavaScript: {e}")

def create_simple_test_page():
    """إنشاء صفحة اختبار بسيطة"""
    print("\n🔧 إنشاء صفحة اختبار بسيطة...")
    
    test_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>اختبار أزرار الطباعة</title>
    <style>
        body { font-family: Arial, sans-serif; direction: rtl; margin: 20px; }
        button { margin: 10px; padding: 10px 20px; font-size: 16px; }
        .test-button { background: #007bff; color: white; border: none; cursor: pointer; }
        .test-button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>اختبار أزرار الطباعة</h1>
    
    <button class="test-button" onclick="testPrintSales()">🖨️ اختبار طباعة المبيعات</button>
    <button class="test-button" onclick="testPrintPurchases()">🖨️ اختبار طباعة المشتريات</button>
    <button class="test-button" onclick="testPrintExpenses()">🖨️ اختبار طباعة المصروفات</button>
    <button class="test-button" onclick="testPrintPayroll()">🖨️ اختبار طباعة الرواتب</button>
    
    <div id="test-results" style="margin-top: 20px; padding: 10px; background: #f8f9fa; border: 1px solid #dee2e6;"></div>
    
    <script>
        function testPrintSales() {
            console.log('🖨️ اختبار طباعة المبيعات');
            document.getElementById('test-results').innerHTML += '<p>✅ تم اختبار طباعة المبيعات</p>';
            
            // محاولة استدعاء الوظيفة الأصلية
            if (typeof printSalesInvoices === 'function') {
                printSalesInvoices();
            } else {
                alert('❌ وظيفة printSalesInvoices غير موجودة');
            }
        }
        
        function testPrintPurchases() {
            console.log('🖨️ اختبار طباعة المشتريات');
            document.getElementById('test-results').innerHTML += '<p>✅ تم اختبار طباعة المشتريات</p>';
            
            if (typeof printPurchasesInvoices === 'function') {
                printPurchasesInvoices();
            } else {
                alert('❌ وظيفة printPurchasesInvoices غير موجودة');
            }
        }
        
        function testPrintExpenses() {
            console.log('🖨️ اختبار طباعة المصروفات');
            document.getElementById('test-results').innerHTML += '<p>✅ تم اختبار طباعة المصروفات</p>';
            
            if (typeof printExpensesInvoices === 'function') {
                printExpensesInvoices();
            } else {
                alert('❌ وظيفة printExpensesInvoices غير موجودة');
            }
        }
        
        function testPrintPayroll() {
            console.log('🖨️ اختبار طباعة الرواتب');
            document.getElementById('test-results').innerHTML += '<p>✅ تم اختبار طباعة الرواتب</p>';
            
            if (typeof printPayrollInvoices === 'function') {
                printPayrollInvoices();
            } else {
                alert('❌ وظيفة printPayrollInvoices غير موجودة');
            }
        }
        
        // تحميل ملف JavaScript الخارجي
        const script = document.createElement('script');
        script.src = '/static/js/payments_functions.js';
        script.onload = function() {
            console.log('✅ تم تحميل ملف JavaScript');
            document.getElementById('test-results').innerHTML += '<p>✅ تم تحميل ملف JavaScript</p>';
        };
        script.onerror = function() {
            console.error('❌ فشل تحميل ملف JavaScript');
            document.getElementById('test-results').innerHTML += '<p>❌ فشل تحميل ملف JavaScript</p>';
        };
        document.head.appendChild(script);
    </script>
</body>
</html>
    """
    
    with open('test_print_buttons.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ تم إنشاء صفحة الاختبار: test_print_buttons.html")
    
    # فتح صفحة الاختبار
    webbrowser.open('file://' + os.path.abspath('test_print_buttons.html'))

def main():
    """الوظيفة الرئيسية"""
    print("🔍 تشخيص شامل لمشكلة أزرار الطباعة")
    print("=" * 60)
    
    # تشخيص المشكلة
    debug_print_buttons()
    
    # اختبار ملف JavaScript
    test_javascript_file()
    
    # إنشاء صفحة اختبار
    import os
    create_simple_test_page()
    
    # فتح الصفحة الأصلية
    print("\n🌐 فتح الصفحة الأصلية...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 خطوات التشخيص:")
    print("1. فحص صفحة الاختبار المنفصلة")
    print("2. فحص Console في المتصفح (F12)")
    print("3. البحث عن رسائل الأخطاء")
    print("4. التأكد من تحميل ملف JavaScript")
    
    print("\n💡 الحلول المحتملة:")
    print("- إعادة تشغيل الخادم")
    print("- مسح cache المتصفح")
    print("- فحص مسار ملف JavaScript")
    print("- التأكد من صحة HTML")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
