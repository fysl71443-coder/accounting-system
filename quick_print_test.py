#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للطباعة
Quick Print Test
"""

import requests
import webbrowser
import time

def main():
    print("🧪 اختبار سريع للطباعة")
    print("=" * 40)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل: python direct_start.py")
        return
    
    # فتح المتصفح
    print("🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. اضغط زر 'طباعة' في أي تبويب")
    print("3. اختر الشهر من القائمة")
    print("4. اضغط 'معاينة' أو 'تحميل PDF'")
    print("5. إذا لم تعمل، اضغط F12 وفحص Console")
    
    print("\n🔗 الرابط المباشر:")
    print("http://localhost:5000/payments_dues")

if __name__ == "__main__":
    main()
