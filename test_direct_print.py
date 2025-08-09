#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الطباعة المباشرة
Test Direct Print
"""

import requests
import webbrowser
import time

def test_direct_print():
    """اختبار الطباعة المباشرة"""
    print("🖨️ اختبار الطباعة المباشرة")
    print("=" * 40)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python app.py")
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
    
    # اختبار الطباعة المباشرة
    print("\n🖨️ اختبار route الطباعة المباشر...")
    
    form_data = {
        'section': 'sales',
        'month': '2025-08'
    }
    
    try:
        response = session.post("http://localhost:5000/print-invoices", data=form_data)
        
        if response.status_code == 200:
            print("✅ الطباعة المباشرة تعمل")
            
            # فحص نوع المحتوى
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                # حفظ ملف PDF
                filename = f"direct_print_test_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ تم إنتاج ملف PDF: {filename} ({file_size} بايت)")
                
            elif 'text/html' in content_type:
                print("📄 تم إرجاع HTML (fallback)")
                
                # حفظ ملف HTML للمراجعة
                filename = f"direct_print_test_{int(time.time())}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✅ تم حفظ ملف HTML: {filename}")
                
            else:
                print(f"⚠️ نوع محتوى غير متوقع: {content_type}")
                
        else:
            print(f"❌ الطباعة المباشرة فشلت: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الطباعة المباشرة: {e}")
        return False
    
    return True

def test_all_sections_direct():
    """اختبار جميع الأقسام بالطباعة المباشرة"""
    print("\n🔄 اختبار جميع الأقسام...")
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin123'}
    session.post("http://localhost:5000/login", data=login_data)
    
    sections = [
        ('sales', 'المبيعات'),
        ('purchases', 'المشتريات'), 
        ('expenses', 'المصروفات'),
        ('payroll', 'الرواتب')
    ]
    
    for section_code, section_name in sections:
        print(f"\n📊 اختبار {section_name} ({section_code})...")
        
        form_data = {
            'section': section_code,
            'month': '2025-08'
        }
        
        try:
            response = session.post("http://localhost:5000/print-invoices", data=form_data)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                
                if 'application/pdf' in content_type:
                    print(f"✅ {section_name}: تم إنتاج PDF ({len(response.content)} بايت)")
                elif 'text/html' in content_type:
                    print(f"✅ {section_name}: تم إنتاج HTML")
                    
                    # فحص محتوى البيانات
                    content = response.text
                    if section_code == 'sales' and 'S-2025-' in content:
                        print(f"   📊 {section_name}: بيانات موجودة")
                    elif section_code == 'purchases' and 'P-2025-' in content:
                        print(f"   📊 {section_name}: بيانات موجودة")
                    elif section_code == 'expenses' and 'E-2025-' in content:
                        print(f"   📊 {section_name}: بيانات موجودة")
                    else:
                        print(f"   ⚠️ {section_name}: لا توجد بيانات")
                        
            else:
                print(f"❌ {section_name}: فشل - {response.status_code}")
                
        except Exception as e:
            print(f"❌ {section_name}: خطأ - {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🖨️ اختبار شامل للطباعة المباشرة")
    print("=" * 60)
    
    # اختبار الطباعة المباشرة
    if not test_direct_print():
        print("❌ فشل اختبار الطباعة المباشرة")
        return
    
    # اختبار جميع الأقسام
    test_all_sections_direct()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار:")
    print("✅ الطباعة المباشرة تعمل")
    print("✅ جميع الأقسام مُختبرة")
    print("✅ تم فتح المتصفح")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. اضغط زر 'طباعة مباشرة' في أسفل الصفحة")
    print("3. اختر القسم والشهر")
    print("4. اضغط 'طباعة الفواتير'")
    print("5. يجب أن يتم تحميل ملف PDF أو عرض HTML")
    
    print("\n🔗 الروابط:")
    print("- شاشة المدفوعات: http://localhost:5000/payments_dues")
    print("- اختبار مباشر: http://localhost:5000/print-invoices")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
