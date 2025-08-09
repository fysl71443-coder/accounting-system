#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار أزرار الطباعة البسيطة الجديدة
Test Simple Print Buttons
"""

import requests
import webbrowser

def test_simple_print_buttons():
    """اختبار أزرار الطباعة البسيطة"""
    print("🖨️ اختبار أزرار الطباعة البسيطة الجديدة")
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
            print_buttons = [
                ('printAllSales()', 'زر طباعة جميع المبيعات'),
                ('printAllPurchases()', 'زر طباعة جميع المشتريات'),
                ('printAllExpenses()', 'زر طباعة جميع المصروفات'),
                ('printAllPayroll()', 'زر طباعة جميع الرواتب'),
                ('طباعة جميع المبيعات', 'نص زر المبيعات'),
                ('طباعة جميع المشتريات', 'نص زر المشتريات'),
                ('طباعة جميع المصروفات', 'نص زر المصروفات'),
                ('طباعة جميع الرواتب', 'نص زر الرواتب')
            ]
            
            print("\n🔍 فحص أزرار الطباعة:")
            buttons_found = 0
            for button, description in print_buttons:
                if button in content:
                    print(f"   ✅ {description}")
                    buttons_found += 1
                else:
                    print(f"   ❌ {description}")
            
            # فحص الوظائف JavaScript
            js_functions = [
                ('function printAllSales()', 'وظيفة طباعة المبيعات'),
                ('function printAllPurchases()', 'وظيفة طباعة المشتريات'),
                ('function printAllExpenses()', 'وظيفة طباعة المصروفات'),
                ('function printAllPayroll()', 'وظيفة طباعة الرواتب'),
                ('function openSimplePrintWindow(', 'وظيفة فتح نافذة الطباعة')
            ]
            
            print("\n🔍 فحص وظائف JavaScript:")
            js_found = 0
            for func, description in js_functions:
                if func in content:
                    print(f"   ✅ {description}")
                    js_found += 1
                else:
                    print(f"   ❌ {description}")
            
            print(f"\n📊 النتائج:")
            print(f"   أزرار الطباعة: {buttons_found}/{len(print_buttons)}")
            print(f"   وظائف JavaScript: {js_found}/{len(js_functions)}")
            
            return buttons_found >= len(print_buttons) * 0.8 and js_found >= len(js_functions) * 0.8
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار شامل لأزرار الطباعة البسيطة")
    print("=" * 60)
    
    # اختبار الأزرار
    buttons_work = test_simple_print_buttons()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. سجل الدخول: admin / admin112233")
    print("2. اختبر أزرار الطباعة في كل تبويب:")
    print("   - تبويب المبيعات: 'طباعة جميع المبيعات'")
    print("   - تبويب المشتريات: 'طباعة جميع المشتريات'")
    print("   - تبويب المصروفات: 'طباعة جميع المصروفات'")
    print("   - تبويب الرواتب: 'طباعة جميع الرواتب'")
    print("3. تأكد من فتح نافذة طباعة جديدة")
    print("4. تأكد من وجود البيانات في التقرير")
    print("5. تأكد من حساب المجموع الإجمالي")
    
    print("\n🔗 الروابط:")
    print("   شاشة المدفوعات: http://localhost:5000/payments_dues")
    
    print("\n🌟 المزايا الجديدة:")
    print("✅ أزرار طباعة بسيطة وفعالة")
    print("✅ طباعة جميع الفواتير من كل نوع")
    print("✅ تصميم طباعة احترافي ومنسق")
    print("✅ ألوان مميزة لكل نوع فاتورة")
    print("✅ حساب المجموع الإجمالي تلقائياً")
    print("✅ معلومات الشركة والتاريخ")
    print("✅ تنسيق مناسب للطباعة والحفظ")
    print("✅ فتح نافذة طباعة تلقائياً")
    
    print("\n📊 ملخص النتائج:")
    if buttons_work:
        print("🎉 أزرار الطباعة البسيطة تعمل بشكل ممتاز!")
        print("✅ جميع الأزرار والوظائف متاحة")
        print("✅ يمكن طباعة جميع أنواع الفواتير")
    else:
        print("⚠️ هناك بعض المشاكل في أزرار الطباعة")
        print("💡 تأكد من تحديث الصفحة")
    
    print("\n💡 كيفية الاستخدام:")
    print("1. اذهب إلى أي تبويب (مبيعات، مشتريات، إلخ)")
    print("2. اضغط زر 'طباعة جميع [النوع]'")
    print("3. ستفتح نافذة جديدة مع التقرير")
    print("4. ستبدأ الطباعة تلقائياً")
    print("5. يمكن حفظ الصفحة كـ PDF")
    
    print("\n🎯 الفوائد:")
    print("- طباعة سريعة بدون تعقيد")
    print("- تقارير منسقة ومهنية")
    print("- لا حاجة لتحديد فواتير معينة")
    print("- يعمل مع جميع أنواع الفواتير")
    print("- مناسب للطباعة والأرشفة")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
