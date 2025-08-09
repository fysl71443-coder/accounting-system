#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل مباشر للخادم - بدون مشاكل PowerShell
Direct Server Start - No PowerShell Issues
"""

import os
import sys

# إعداد المسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'
os.environ['FLASK_ENV'] = 'development'

print("🚀 تشغيل مباشر للخادم...")
print("📍 http://localhost:5000")
print("👤 admin / admin123")
print("=" * 40)

try:
    # استيراد مباشر
    from app import app, db
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        print("✅ قاعدة البيانات جاهزة")
    
    print("🌐 بدء الخادم...")
    
    # تشغيل الخادم
    app.run(
        debug=False,  # تعطيل debug لتجنب مشاكل reloader
        host='0.0.0.0', 
        port=5000, 
        use_reloader=False,
        threaded=True
    )
    
except KeyboardInterrupt:
    print("\n🛑 تم إيقاف الخادم")
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
    input("اضغط Enter للخروج...")
