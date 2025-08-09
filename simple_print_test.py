#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار مبسط لوظائف الطباعة
Simple Print Functions Test
"""

import requests
import time

def test_server():
    """اختبار الخادم"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print(f"✅ الخادم يعمل - كود الاستجابة: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ الخادم لا يعمل: {e}")
        return False

def test_login():
    """اختبار تسجيل الدخول"""
    session = requests.Session()
    
    try:
        # تسجيل الدخول
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        
        if response.status_code == 200:
            print("✅ تسجيل الدخول نجح")
            return session
        else:
            print(f"❌ تسجيل الدخول فشل: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return None

def test_payments_page(session):
    """اختبار صفحة المدفوعات"""
    try:
        response = session.get("http://localhost:5000/payments_dues")
        
        if response.status_code == 200:
            print("✅ صفحة المدفوعات تعمل")
            
            # فحص محتوى الصفحة
            content = response.text
            if 'openPrintModal' in content:
                print("✅ أزرار الطباعة موجودة")
            if 'printModal' in content:
                print("✅ نافذة الطباعة موجودة")
                
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
    
    # اختبار معاينة الطباعة
    try:
        response = session.get("http://localhost:5000/print_invoices_preview", params=params)
        if response.status_code == 200:
            print("✅ معاينة الطباعة تعمل")
        else:
            print(f"❌ معاينة الطباعة فشلت: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ خطأ في معاينة الطباعة: {e}")
    
    # اختبار صفحة الطباعة
    try:
        response = session.get("http://localhost:5000/print_invoices", params=params)
        if response.status_code == 200:
            print("✅ صفحة الطباعة تعمل")
        else:
            print(f"❌ صفحة الطباعة فشلت: {response.status_code}")
            print(f"📋 محتوى الخطأ: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ خطأ في صفحة الطباعة: {e}")
    
    # اختبار API الأشهر المتاحة
    try:
        response = session.get("http://localhost:5000/api/available_months?type=sales")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ API الأشهر المتاحة يعمل - {len(data.get('months', []))} شهر")
            else:
                print("⚠️ API الأشهر المتاحة يعمل لكن لا توجد بيانات")
        else:
            print(f"❌ API الأشهر المتاحة فشل: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في API الأشهر المتاحة: {e}")

def create_test_data(session):
    """إنشاء بيانات تجريبية للاختبار"""
    print("\n📊 إنشاء بيانات تجريبية...")
    
    # يمكن إضافة كود لإنشاء فواتير تجريبية هنا
    # لكن الآن سنتجاهل هذا ونختبر بالبيانات الموجودة
    print("⚠️ تم تجاهل إنشاء البيانات التجريبية")

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار مبسط لوظائف الطباعة")
    print("=" * 50)
    
    # اختبار الخادم
    if not test_server():
        print("💡 يرجى تشغيل الخادم أولاً: python quick_start.py")
        return
    
    # انتظار قليل للتأكد من تشغيل الخادم
    time.sleep(2)
    
    # تسجيل الدخول
    session = test_login()
    if not session:
        print("❌ فشل تسجيل الدخول")
        return
    
    # اختبار صفحة المدفوعات
    if not test_payments_page(session):
        print("❌ فشل اختبار صفحة المدفوعات")
        return
    
    # إنشاء بيانات تجريبية
    create_test_data(session)
    
    # اختبار routes الطباعة
    test_print_routes(session)
    
    print("\n" + "=" * 50)
    print("🎉 اكتمل الاختبار المبسط!")
    print("💡 يمكنك الآن فتح المتصفح واختبار الطباعة يدوياً")
    print("🔗 http://localhost:5000/payments_dues")
    print("=" * 50)

if __name__ == "__main__":
    main()
