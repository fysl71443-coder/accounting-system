#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار زر الطباعة مباشرة
Direct Print Button Test
"""

import requests
import webbrowser
import time

def test_print_button():
    """اختبار زر الطباعة"""
    print("🧪 اختبار زر الطباعة في شاشة المدفوعات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم أولاً:")
        print("   python app.py")
        print("   أو")
        print("   python direct_start.py")
        return False
    
    # فتح المتصفح
    print("🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 خطوات الاختبار:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. ابحث عن أزرار 'طباعة' في كل تبويب")
    print("3. اضغط على أي زر طباعة")
    print("4. يجب أن تفتح نافذة منبثقة")
    print("5. إذا لم تفتح، اضغط F12 وفحص Console")
    
    print("\n🔧 إذا لم تعمل الطباعة:")
    print("- تأكد من تفعيل JavaScript")
    print("- تأكد من السماح بالنوافذ المنبثقة")
    print("- اضغط على زر 'اختبار سريع' في أسفل الصفحة")
    
    print("\n🔗 الرابط المباشر:")
    print("http://localhost:5000/payments_dues")
    
    return True

def test_api_endpoints():
    """اختبار API endpoints للطباعة"""
    print("\n🔌 اختبار API endpoints...")
    
    session = requests.Session()
    
    # تسجيل الدخول
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        if response.status_code == 200:
            print("✅ تسجيل الدخول نجح")
        else:
            print("❌ فشل تسجيل الدخول")
            return False
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False
    
    # اختبار API الأشهر المتاحة
    try:
        response = session.get("http://localhost:5000/api/available_months?type=sales")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ API الأشهر المتاحة: {len(data.get('months', []))} شهر")
            else:
                print("⚠️ API يعمل لكن لا توجد بيانات")
        else:
            print(f"❌ API الأشهر المتاحة فشل: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في API الأشهر: {e}")
    
    # اختبار معاينة الطباعة
    try:
        params = {'type': 'sales', 'month': '2025-08', 'status': 'all', 'details': 'true'}
        response = session.get("http://localhost:5000/print_invoices_preview", params=params)
        if response.status_code == 200:
            print("✅ معاينة الطباعة تعمل")
        else:
            print(f"❌ معاينة الطباعة فشلت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في معاينة الطباعة: {e}")
    
    return True

def main():
    """الوظيفة الرئيسية"""
    print("🖨️ اختبار زر الطباعة - شاشة المدفوعات والمستحقات")
    print("=" * 60)
    
    # اختبار زر الطباعة
    if not test_print_button():
        return
    
    # اختبار API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار:")
    print("✅ تم فتح المتصفح")
    print("✅ تم اختبار API endpoints")
    print("🔗 الرابط: http://localhost:5000/payments_dues")
    print("👤 المستخدم: admin / admin123")
    
    print("\n💡 نصائح:")
    print("- إذا لم تعمل الطباعة، اضغط F12 وفحص Console")
    print("- استخدم زر 'اختبار سريع' في أسفل الصفحة")
    print("- تأكد من السماح بالنوافذ المنبثقة")
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
