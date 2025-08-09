#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل النظام المبسط
Simple App Starter
"""

import os
import sys

def start_application():
    """تشغيل التطبيق"""
    
    print("🚀 بدء تشغيل نظام المحاسبة الاحترافي")
    print("=" * 50)
    print("📍 الرابط الرئيسي: http://localhost:5000")
    print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
    print("👤 المستخدم: admin")
    print("🔑 كلمة المرور: admin123")
    print("=" * 50)
    
    try:
        # استيراد التطبيق
        print("📦 تحميل التطبيق...")
        from app import app, db
        
        # إنشاء قاعدة البيانات
        print("🗄️ إعداد قاعدة البيانات...")
        with app.app_context():
            db.create_all()
            print("✅ تم إعداد قاعدة البيانات")
        
        # تشغيل الخادم
        print("🌐 بدء تشغيل الخادم...")
        print("✅ النظام جاهز للاستخدام!")
        print("\n🔗 افتح المتصفح واذهب إلى: http://localhost:5000")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("💡 تأكد من تثبيت المتطلبات: pip install -r expenses_requirements.txt")
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        
        # محاولة إصلاح المشاكل الشائعة
        print("\n🔧 محاولة إصلاح المشاكل...")
        
        try:
            # التحقق من المنفذ
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 5000))
            sock.close()
            
            if result == 0:
                print("⚠️ المنفذ 5000 مستخدم. جاري المحاولة على منفذ آخر...")
                app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
            else:
                print("🔄 إعادة المحاولة...")
                app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
                
        except Exception as e2:
            print(f"❌ فشل الإصلاح: {e2}")
            print("\n📞 للمساعدة:")
            print("1. تأكد من تثبيت Python 3.7+")
            print("2. تأكد من تثبيت المتطلبات")
            print("3. تأكد من عدم وجود تطبيق آخر على المنفذ 5000")

if __name__ == "__main__":
    start_application()
