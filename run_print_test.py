#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل خادم اختبار الطباعة
Run Print Test Server
"""

import os
import sys

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'

print("🚀 تشغيل خادم اختبار الطباعة")
print("📍 http://localhost:5000")
print("🔗 صفحة الاختبار: http://localhost:5000/print-test")
print("=" * 50)

try:
    from app import app, db
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        print("✅ قاعدة البيانات جاهزة")
        
        # فحص routes المتاحة
        print("\n📋 Routes الطباعة:")
        for rule in app.url_map.iter_rules():
            if 'print' in rule.rule.lower():
                print(f"   🔗 {rule.rule} - {list(rule.methods)}")
    
    print("\n🌐 بدء الخادم...")
    
    # تشغيل الخادم
    app.run(
        debug=True,
        host='0.0.0.0', 
        port=5000, 
        use_reloader=False
    )
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
    input("اضغط Enter للخروج...")
