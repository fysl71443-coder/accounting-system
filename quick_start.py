#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل سريع للخادم - للاختبار
Quick Server Start - For Testing
"""

import os
import sys

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'
os.environ['FLASK_ENV'] = 'development'

print("🚀 تشغيل سريع للخادم...")
print("📍 http://localhost:5000")
print("👤 admin / admin123")
print("=" * 40)

try:
    from app import app, db
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        print("✅ قاعدة البيانات جاهزة")
    
    # تشغيل الخادم
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    input("اضغط Enter للخروج...")
