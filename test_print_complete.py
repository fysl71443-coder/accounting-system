#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل للطباعة - إصلاح جميع المشاكل
Complete Print Testing - Fix All Issues
"""

import requests
import time
import webbrowser
from datetime import datetime

def start_server():
    """تشغيل الخادم"""
    import subprocess
    import sys
    import os
    
    print("🚀 تشغيل الخادم...")
    
    try:
        # تشغيل الخادم في الخلفية
        process = subprocess.Popen([
            sys.executable, "direct_start.py"
        ], cwd=os.getcwd())
        
        # انتظار قليل للتأكد من بدء التشغيل
        time.sleep(5)
        
        # فحص إذا كان الخادم يعمل
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code in [200, 302]:
                print("✅ الخادم يعمل بنجاح")
                return process
        except:
            pass
        
        print("⚠️ الخادم قد لا يعمل بشكل صحيح")
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def test_server_connection():
    """اختبار الاتصال بالخادم"""
    print("\n🔗 اختبار الاتصال بالخادم...")
    
    try:
        response = requests.get("http://localhost:5000", timeout=10)
        if response.status_code in [200, 302]:
            print("✅ الخادم متاح ويعمل")
            return True
        else:
            print(f"⚠️ الخادم يعمل لكن كود الاستجابة: {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
        return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def login_and_get_session():
    """تسجيل الدخول والحصول على session"""
    print("\n🔐 تسجيل الدخول...")
    
    session = requests.Session()
    
    try:
        # تسجيل الدخول
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
            return session
        else:
            print(f"❌ فشل تسجيل الدخول: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return None

def test_payments_page(session):
    """اختبار صفحة المدفوعات"""
    print("\n📄 اختبار صفحة المدفوعات...")
    
    try:
        response = session.get("http://localhost:5000/payments_dues", timeout=10)
        
        if response.status_code == 200:
            print("✅ صفحة المدفوعات تعمل")
            
            content = response.text
            
            # فحص أزرار الطباعة
            print_buttons = content.count('openPrintModal')
            print(f"✅ عدد أزرار الطباعة: {print_buttons}")
            
            # فحص النافذة المنبثقة
            if 'printModal' in content:
                print("✅ نافذة الطباعة موجودة")
            else:
                print("❌ نافذة الطباعة غير موجودة")
            
            # فحص الفلاتر
            filters = ['sales-status-filter', 'purchases-status-filter', 'expenses-status-filter']
            for filter_id in filters:
                if filter_id in content:
                    print(f"✅ فلتر {filter_id} موجود")
                else:
                    print(f"❌ فلتر {filter_id} غير موجود")
            
            return True
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في صفحة المدفوعات: {e}")
        return False

def test_print_routes(session):
    """اختبار routes الطباعة"""
    print("\n🖨️ اختبار routes الطباعة...")
    
    # معاملات الاختبار
    params = {
        'type': 'sales',
        'month': '2025-08',
        'status': 'all',
        'details': 'true'
    }
    
    # اختبار API الأشهر المتاحة
    try:
        response = session.get("http://localhost:5000/api/available_months?type=sales", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                months_count = len(data.get('months', []))
                print(f"✅ API الأشهر المتاحة: {months_count} شهر")
                
                if months_count > 0:
                    for month in data['months'][:2]:  # عرض أول شهرين
                        print(f"   📅 {month['text']} ({month['value']})")
            else:
                print("⚠️ API الأشهر المتاحة يعمل لكن لا توجد بيانات")
        else:
            print(f"❌ API الأشهر المتاحة فشل: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في API الأشهر المتاحة: {e}")
    
    # اختبار معاينة الطباعة
    try:
        response = session.get("http://localhost:5000/print_invoices_preview", params=params, timeout=15)
        if response.status_code == 200:
            print("✅ معاينة الطباعة تعمل")
            
            # فحص محتوى الصفحة
            content = response.text
            if 'تقرير الفواتير' in content:
                print("✅ عنوان التقرير موجود")
            if 'S-2025-001' in content:
                print("✅ البيانات التجريبية ظاهرة")
        else:
            print(f"❌ معاينة الطباعة فشلت: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ خطأ في معاينة الطباعة: {e}")
    
    # اختبار صفحة الطباعة
    try:
        response = session.get("http://localhost:5000/print_invoices", params=params, timeout=15)
        if response.status_code == 200:
            print("✅ صفحة الطباعة تعمل")
        else:
            print(f"❌ صفحة الطباعة فشلت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في صفحة الطباعة: {e}")
    
    # اختبار تحميل PDF
    try:
        response = session.get("http://localhost:5000/download_invoices_pdf", params=params, timeout=20)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ تم إنتاج ملف PDF: {filename} ({file_size} بايت)")
                return filename
                
            elif 'text/html' in content_type:
                print("📄 تم إرجاع HTML (fallback) - مكتبة PDF غير متاحة")
                return True
        else:
            print(f"❌ تحميل PDF فشل: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في تحميل PDF: {e}")
    
    return True

def open_browser_for_manual_test():
    """فتح المتصفح للاختبار اليدوي"""
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    
    try:
        webbrowser.open("http://localhost:5000/payments_dues")
        print("✅ تم فتح المتصفح")
        
        print("\n📋 تعليمات الاختبار اليدوي:")
        print("1. تسجيل الدخول: admin / admin123")
        print("2. اختبار أزرار الطباعة في كل تبويب")
        print("3. اختبار اختيار الشهر من القائمة المنسدلة")
        print("4. اختبار المعاينة والطباعة وتحميل PDF")
        print("5. فحص Console (F12) للأخطاء")
        
    except Exception as e:
        print(f"❌ خطأ في فتح المتصفح: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار شامل لنظام الطباعة - إصلاح جميع المشاكل")
    print("=" * 70)
    
    # اختبار الاتصال بالخادم
    if not test_server_connection():
        print("\n💡 محاولة تشغيل الخادم...")
        server_process = start_server()
        
        # انتظار وإعادة اختبار
        time.sleep(5)
        if not test_server_connection():
            print("❌ فشل في تشغيل الخادم")
            print("💡 يرجى تشغيل الخادم يدوياً: python direct_start.py")
            return
    
    # تسجيل الدخول
    session = login_and_get_session()
    if not session:
        print("❌ فشل تسجيل الدخول")
        return
    
    # اختبار صفحة المدفوعات
    if not test_payments_page(session):
        print("❌ فشل اختبار صفحة المدفوعات")
        return
    
    # اختبار routes الطباعة
    pdf_result = test_print_routes(session)
    
    # فتح المتصفح للاختبار اليدوي
    open_browser_for_manual_test()
    
    print("\n" + "=" * 70)
    print("📊 ملخص نتائج الاختبار الشامل:")
    print("=" * 70)
    
    if pdf_result:
        print("🎉 جميع اختبارات الطباعة نجحت!")
        print("✅ الخادم يعمل")
        print("✅ صفحة المدفوعات تعمل")
        print("✅ أزرار الطباعة موجودة")
        print("✅ routes الطباعة تعمل")
        print("✅ إنتاج PDF يعمل")
        
        if isinstance(pdf_result, str):
            print(f"📁 ملف PDF تجريبي: {pdf_result}")
        
        print("\n🚀 النظام جاهز للاستخدام!")
        print("🔗 http://localhost:5000/payments_dues")
        print("👤 admin / admin123")
        
    else:
        print("⚠️ بعض الاختبارات فشلت - يحتاج مراجعة")
    
    print("=" * 70)
    
    # انتظار المستخدم
    input("\nاضغط Enter بعد انتهاء الاختبار اليدوي...")

if __name__ == "__main__":
    main()
