#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لإصلاح المشاكل
"""

import requests
import time

def test_screen(url, name):
    """اختبار شاشة واحدة"""
    try:
        print(f"🔍 اختبار {name}...")
        
        # تسجيل الدخول أولاً
        session = requests.Session()
        login_data = {'username': 'admin', 'password': 'admin112233'}
        login_response = session.post('http://localhost:5000/login', data=login_data)
        
        if login_response.status_code != 200 and login_response.status_code != 302:
            print(f"❌ فشل تسجيل الدخول")
            return False
        
        # اختبار الشاشة
        response = session.get(f'http://localhost:5000{url}')
        
        if response.status_code == 200:
            print(f"✅ {name} - تعمل بنجاح")
            return True
        else:
            print(f"❌ {name} - خطأ {response.status_code}")
            print(f"📝 المحتوى: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ {name} - خطأ: {str(e)}")
        return False

def main():
    print("🚀 اختبار سريع للشاشات المشكوك فيها...")
    print("=" * 50)
    
    # اختبار الشاشات المشكوك فيها
    screens = [
        ('/sales', 'شاشة المبيعات'),
        ('/payments_dues', 'شاشة المدفوعات والمستحقات'),
        ('/dashboard', 'الشاشة الرئيسية'),
        ('/purchases', 'شاشة المشتريات'),
        ('/expenses', 'شاشة المصروفات')
    ]
    
    results = []
    for url, name in screens:
        result = test_screen(url, name)
        results.append((name, result))
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("📊 النتائج النهائية:")
    print("=" * 50)
    
    working = 0
    total = len(results)
    
    for name, result in results:
        if result:
            print(f"✅ {name}")
            working += 1
        else:
            print(f"❌ {name}")
    
    print(f"\n📈 النسبة: {working}/{total} ({working/total*100:.1f}%)")
    
    if working == total:
        print("🎉 جميع الشاشات تعمل بنجاح!")
    else:
        print("⚠️ بعض الشاشات تحتاج إصلاح")

if __name__ == "__main__":
    main()
