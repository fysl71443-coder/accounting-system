#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الطباعة المحسنة مع البنود
Test Enhanced Print with Items
"""

import requests
import webbrowser
import time

def test_enhanced_print():
    """اختبار الطباعة المحسنة"""
    print("🌟 اختبار الطباعة المحسنة مع البنود")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم أولاً:")
        print("   python app.py")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول")
        else:
            print("❌ فشل تسجيل الدخول")
            return False
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False
    
    # اختبار الطباعة المحسنة
    print("\n🌟 اختبار الطباعة المحسنة...")
    
    params = {
        'type': 'sales',
        'month': '2025-08',
        'status': 'all'
    }
    
    try:
        response = session.get("http://localhost:5000/print_invoices_enhanced", params=params)
        
        if response.status_code == 200:
            print("✅ الطباعة المحسنة تعمل")
            
            # فحص محتوى الصفحة
            content = response.text
            if 'فواتير sales لشهر 2025-08' in content:
                print("✅ عنوان التقرير المحسن موجود")
            if 'items-table' in content:
                print("✅ جدول البنود موجود")
            if 'summary' in content:
                print("✅ ملخص التقرير موجود")
            if 'S-2025-001' in content:
                print("✅ البيانات التجريبية ظاهرة")
                
            # حفظ ملف HTML للمراجعة
            with open('enhanced_report_test.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ تم حفظ ملف HTML: enhanced_report_test.html")
            
        else:
            print(f"❌ الطباعة المحسنة فشلت: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الطباعة المحسنة: {e}")
        return False
    
    # فتح المتصفح للاختبار اليدوي
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. اضغط زر 'طباعة' في أي تبويب")
    print("3. اختر الشهر من القائمة")
    print("4. اضغط 'معاينة محسنة' (الزر الأصفر)")
    print("5. يجب أن تظهر صفحة بتصميم محسن مع البنود")
    
    return True

def test_all_sections():
    """اختبار جميع الأقسام"""
    print("\n🔄 اختبار جميع الأقسام...")
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin123'}
    session.post("http://localhost:5000/login", data=login_data)
    
    sections = ['sales', 'purchases', 'expenses']
    
    for section in sections:
        print(f"\n📊 اختبار قسم: {section}")
        
        params = {
            'type': section,
            'month': '2025-08',
            'status': 'all'
        }
        
        try:
            response = session.get("http://localhost:5000/print_invoices_enhanced", params=params)
            
            if response.status_code == 200:
                print(f"✅ {section}: الطباعة المحسنة تعمل")
                
                # فحص محتوى محدد لكل قسم
                content = response.text
                if section == 'sales' and 'S-2025-' in content:
                    print(f"✅ {section}: بيانات المبيعات موجودة")
                elif section == 'purchases' and 'P-2025-' in content:
                    print(f"✅ {section}: بيانات المشتريات موجودة")
                elif section == 'expenses' and 'E-2025-' in content:
                    print(f"✅ {section}: بيانات المصروفات موجودة")
                else:
                    print(f"⚠️ {section}: لا توجد بيانات")
                    
            else:
                print(f"❌ {section}: فشل - {response.status_code}")
                
        except Exception as e:
            print(f"❌ {section}: خطأ - {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🌟 اختبار شامل للطباعة المحسنة")
    print("=" * 60)
    
    # اختبار الطباعة المحسنة
    if not test_enhanced_print():
        return
    
    # اختبار جميع الأقسام
    test_all_sections()
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار:")
    print("✅ تم اختبار الطباعة المحسنة")
    print("✅ تم اختبار جميع الأقسام")
    print("✅ تم فتح المتصفح للاختبار اليدوي")
    
    print("\n🌟 المزايا الجديدة:")
    print("- عرض البنود التفصيلية لكل فاتورة")
    print("- تصميم محسن وأكثر جاذبية")
    print("- ملخص إحصائي شامل")
    print("- دعم جميع أنواع الفواتير")
    
    print("\n🔗 الروابط:")
    print("- الطباعة العادية: http://localhost:5000/print_invoices_preview")
    print("- الطباعة المحسنة: http://localhost:5000/print_invoices_enhanced")
    print("- شاشة المدفوعات: http://localhost:5000/payments_dues")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
