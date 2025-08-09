#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار إصلاح زر الطباعة
Test Print Button Fix
"""

import requests
import webbrowser
import time

def test_print_fix():
    """اختبار إصلاح الطباعة"""
    print("🔧 اختبار إصلاح زر الطباعة")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python app.py")
        return False
    
    # اختبار صفحة الاختبار المباشرة
    print("\n📄 اختبار صفحة الاختبار المباشرة...")
    try:
        response = requests.get("http://localhost:5000/print-test")
        if response.status_code == 200:
            print("✅ صفحة اختبار الطباعة تعمل")
            print("🔗 http://localhost:5000/print-test")
        else:
            print(f"❌ صفحة اختبار الطباعة فشلت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في صفحة الاختبار: {e}")
    
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
    
    # اختبار route الطباعة المباشر
    print("\n🖨️ اختبار route الطباعة المباشر...")
    
    form_data = {
        'section': 'sales',
        'month': '2025-08'
    }
    
    try:
        print("📤 إرسال طلب الطباعة...")
        response = session.post("http://localhost:5000/print-invoices", data=form_data)
        
        print(f"📥 استجابة الخادم: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ route الطباعة يعمل")
            
            content_type = response.headers.get('content-type', '')
            print(f"📋 نوع المحتوى: {content_type}")
            
            if 'application/pdf' in content_type:
                print("✅ تم إنتاج ملف PDF")
                
                # حفظ ملف PDF
                filename = f"print_test_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ تم حفظ ملف PDF: {filename} ({file_size} بايت)")
                
            elif 'text/html' in content_type:
                print("✅ تم إنتاج HTML (fallback)")
                
                # فحص محتوى HTML
                content = response.text
                if 'فواتير شهر 2025-08' in content:
                    print("✅ محتوى التقرير صحيح")
                if 'table' in content:
                    print("✅ جدول الفواتير موجود")
                    
                # حفظ ملف HTML للمراجعة
                filename = f"print_test_{int(time.time())}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ تم حفظ ملف HTML: {filename}")
                
            return True
            
        else:
            print(f"❌ route الطباعة فشل: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار route الطباعة: {e}")
        return False

def test_all_sections():
    """اختبار جميع الأقسام"""
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
    
    success_count = 0
    
    for section_code, section_name in sections:
        print(f"\n📊 اختبار {section_name} ({section_code})...")
        
        form_data = {
            'section': section_code,
            'month': '2025-08'
        }
        
        try:
            response = session.post("http://localhost:5000/print-invoices", data=form_data)
            
            if response.status_code == 200:
                print(f"✅ {section_name}: نجح")
                success_count += 1
                
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    print(f"   📄 PDF ({len(response.content)} بايت)")
                elif 'text/html' in content_type:
                    print(f"   📄 HTML ({len(response.text)} حرف)")
                    
            else:
                print(f"❌ {section_name}: فشل - {response.status_code}")
                
        except Exception as e:
            print(f"❌ {section_name}: خطأ - {e}")
    
    print(f"\n📊 النتيجة: {success_count}/{len(sections)} أقسام تعمل")
    return success_count == len(sections)

def main():
    """الوظيفة الرئيسية"""
    print("🔧 اختبار شامل لإصلاح زر الطباعة")
    print("=" * 60)
    
    # اختبار الطباعة
    if not test_print_fix():
        print("❌ فشل اختبار الطباعة الأساسي")
        return
    
    # اختبار جميع الأقسام
    all_sections_work = test_all_sections()
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/print-test")
    
    print("\n" + "=" * 60)
    print("📊 ملخص النتائج:")
    print("=" * 60)
    
    if all_sections_work:
        print("🎉 جميع اختبارات الطباعة نجحت!")
        print("✅ route الطباعة المباشر يعمل")
        print("✅ جميع الأقسام تعمل")
        print("✅ إنتاج PDF/HTML يعمل")
        
        print("\n🚀 النظام جاهز للاستخدام!")
        print("🔗 صفحة الاختبار: http://localhost:5000/print-test")
        print("🔗 شاشة المدفوعات: http://localhost:5000/payments_dues")
        
    else:
        print("⚠️ بعض الاختبارات فشلت")
        print("🔧 يرجى مراجعة الأخطاء أعلاه")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. استخدم صفحة الاختبار المباشرة")
    print("2. اختر القسم والشهر")
    print("3. اضغط 'طباعة'")
    print("4. يجب أن يتم تحميل PDF أو عرض HTML")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
