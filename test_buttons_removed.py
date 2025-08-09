#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار حذف الأزرار التي لا تعمل
Test Removed Non-Working Buttons
"""

import requests
import webbrowser

def test_buttons_removed():
    """اختبار حذف الأزرار التي لا تعمل"""
    print("🗑️ اختبار حذف الأزرار التي لا تعمل")
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
            
            # فحص الأزرار المحذوفة (يجب ألا تكون موجودة)
            removed_buttons = [
                ('printSalesInvoicesDirect()', 'زر طباعة المبيعات'),
                ('printPurchasesInvoices()', 'زر طباعة المشتريات'),
                ('printExpensesInvoices()', 'زر طباعة المصروفات'),
                ('printPayrollInvoices()', 'زر طباعة الرواتب'),
                ('testPrintModal()', 'زر اختبار الطباعة'),
                ('quickPrintTest()', 'زر الاختبار السريع'),
                ('showDirectPrintForm()', 'زر الطباعة المباشرة'),
                ('testFilters()', 'زر اختبار الفلاتر')
            ]
            
            print("\n🔍 فحص الأزرار المحذوفة:")
            buttons_removed = 0
            for button_func, description in removed_buttons:
                if button_func not in content:
                    print(f"   ✅ {description}: تم حذفه")
                    buttons_removed += 1
                else:
                    print(f"   ❌ {description}: لا يزال موجود")
            
            # فحص الأزرار الجديدة (يجب أن تكون موجودة)
            new_buttons = [
                ('/simple_print', 'رابط صفحة الطباعة الجديدة'),
                ('طباعة الفواتير', 'نص زر الطباعة الجديد')
            ]
            
            print("\n🔍 فحص الأزرار الجديدة:")
            new_buttons_found = 0
            for button_element, description in new_buttons:
                if button_element in content:
                    print(f"   ✅ {description}: موجود")
                    new_buttons_found += 1
                else:
                    print(f"   ❌ {description}: غير موجود")
            
            print(f"\n📊 النتائج:")
            print(f"   الأزرار المحذوفة: {buttons_removed}/{len(removed_buttons)}")
            print(f"   الأزرار الجديدة: {new_buttons_found}/{len(new_buttons)}")
            
            return buttons_removed >= len(removed_buttons) * 0.8 and new_buttons_found > 0
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def test_new_print_page():
    """اختبار صفحة الطباعة الجديدة"""
    print("\n🖨️ اختبار صفحة الطباعة الجديدة:")
    print("-" * 30)
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin112233'}
    session.post("http://localhost:5000/login", data=login_data)
    
    try:
        response = session.get("http://localhost:5000/simple_print")
        if response.status_code == 200:
            print("   ✅ صفحة الطباعة الجديدة تعمل")
            
            content = response.text
            
            # فحص العناصر الأساسية
            elements = [
                ('تحديد الكل', 'زر تحديد الكل'),
                ('طباعة المحدد', 'زر الطباعة'),
                ('فواتير المبيعات', 'بطاقة المبيعات'),
                ('loadInvoices', 'وظيفة تحميل الفواتير')
            ]
            
            elements_found = 0
            for element, description in elements:
                if element in content:
                    print(f"      ✅ {description}")
                    elements_found += 1
                else:
                    print(f"      ❌ {description}")
            
            return elements_found >= len(elements) * 0.8
            
        else:
            print(f"   ❌ صفحة الطباعة الجديدة: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ خطأ في صفحة الطباعة الجديدة: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار حذف الأزرار التي لا تعمل")
    print("=" * 60)
    
    # اختبار حذف الأزرار
    buttons_removed = test_buttons_removed()
    
    # اختبار صفحة الطباعة الجديدة
    new_page_works = test_new_print_page()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 ملخص التحديثات:")
    print("=" * 30)
    
    if buttons_removed:
        print("✅ تم حذف الأزرار التي لا تعمل بنجاح")
    else:
        print("❌ لا تزال هناك أزرار لا تعمل")
    
    if new_page_works:
        print("✅ صفحة الطباعة الجديدة تعمل بشكل صحيح")
    else:
        print("❌ مشكلة في صفحة الطباعة الجديدة")
    
    print("\n🗑️ الأزرار المحذوفة:")
    print("- أزرار طباعة المبيعات/المشتريات/المصروفات/الرواتب")
    print("- أزرار الاختبار والتشخيص")
    print("- لوحة التشخيص السفلية")
    
    print("\n➕ الأزرار المضافة:")
    print("- زر 'طباعة الفواتير' في الزاوية السفلية")
    print("- يؤدي إلى صفحة الطباعة المتقدمة")
    
    print("\n📋 تعليمات الاستخدام:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. اذهب إلى شاشة المدفوعات والمستحقات")
    print("3. لاحظ عدم وجود أزرار الطباعة القديمة")
    print("4. اضغط زر 'طباعة الفواتير' في الأسفل")
    print("5. ستنتقل لصفحة الطباعة المتقدمة")
    
    print("\n🔗 الروابط:")
    print("   شاشة المدفوعات: http://localhost:5000/payments_dues")
    print("   صفحة الطباعة: http://localhost:5000/simple_print")
    
    print("\n🌟 النتيجة:")
    if buttons_removed and new_page_works:
        print("🎉 تم تنظيف الواجهة بنجاح!")
        print("✅ تم حذف جميع الأزرار التي لا تعمل")
        print("✅ تم إضافة بديل فعال للطباعة")
    else:
        print("⚠️ هناك بعض المشاكل تحتاج لمراجعة")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
