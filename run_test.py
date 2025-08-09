#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل واختبار أزرار شاشة المبيعات
Run and Test Sales Screen Buttons
"""

import os
import sys
import time
import subprocess
import webbrowser

def start_server():
    """تشغيل الخادم"""
    print("🚀 تشغيل خادم المحاسبة...")
    
    # إعداد متغيرات البيئة
    os.environ['SECRET_KEY'] = 'test-key-for-development'
    
    try:
        # تشغيل الخادم في الخلفية
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd=os.getcwd())
        
        print("⏳ انتظار تشغيل الخادم...")
        time.sleep(5)
        
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def test_server():
    """اختبار الخادم"""
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار أزرار شاشة المبيعات")
    print("=" * 50)
    
    # تشغيل الخادم
    server_process = start_server()
    
    if not server_process:
        print("❌ فشل في تشغيل الخادم")
        return
    
    # اختبار الخادم
    if test_server():
        print("✅ الخادم يعمل بنجاح")
    else:
        print("⚠️ الخادم قد لا يعمل بشكل صحيح")
    
    # فتح المتصفح
    print("🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/sales")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. سجل الدخول: admin / admin123")
    print("2. اذهب إلى صفحة المبيعات")
    print("3. حدد فاتورة (radio button)")
    print("4. اختبر الأزرار:")
    print("   ✅ حفظ - ينقل لصفحة فاتورة جديدة")
    print("   ✅ تعديل - ينقل لصفحة التعديل")
    print("   ✅ حذف - يحذف الفاتورة المحددة")
    print("   ✅ معاينة - يفتح نافذة معاينة")
    print("   ✅ طباعة - يفتح نافذة طباعة")
    print("   ✅ اختيار فاتورة - يظهر معلومات الاختيار")
    print("   ✅ تسجيل دفعة - يفتح نافذة تسجيل الدفع")
    
    print("\n🔗 الروابط المهمة:")
    print("   الصفحة الرئيسية: http://localhost:5000")
    print("   صفحة المبيعات: http://localhost:5000/sales")
    print("   تسجيل الدخول: http://localhost:5000/login")
    
    print("\n🌟 المزايا الجديدة:")
    print("   - أزرار مُحدثة بمعرفات فريدة")
    print("   - إدارة حالة الأزرار (تفعيل/إلغاء)")
    print("   - نافذة تسجيل الدفع")
    print("   - اتصال بـ API الخلفي")
    print("   - تسجيل العمليات في Console")
    
    print("=" * 50)
    print("⚠️ اضغط Ctrl+C لإيقاف الخادم")
    
    try:
        input("\nاضغط Enter بعد انتهاء الاختبار...")
    except KeyboardInterrupt:
        pass
    
    # إيقاف الخادم
    if server_process:
        server_process.terminate()
        print("\n🛑 تم إيقاف الخادم")

if __name__ == "__main__":
    main()
