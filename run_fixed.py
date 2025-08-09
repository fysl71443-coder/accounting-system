#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

def main():
    print("🚀 تشغيل نظام المحاسبة المتكامل")
    print("=" * 50)
    print("📍 الرابط: http://localhost:5000")
    print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
    print("👤 المستخدم: admin | كلمة المرور: admin123")
    print("=" * 50)
    
    try:
        from app import app, db
        
        # إنشاء قاعدة البيانات
        with app.app_context():
            db.create_all()
            print("✅ تم إعداد قاعدة البيانات")
        
        # تشغيل التطبيق
        print("🌐 بدء تشغيل الخادم...")
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
