#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل مبسط للخادم - بدون إعدادات معقدة
Simple Server Startup - No Complex Setup
"""

import os
import sys

# إعداد متغيرات البيئة الأساسية
os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

print("🚀 تشغيل خادم المحاسبة...")
print("🚀 Starting Accounting Server...")
print()
print("📍 http://localhost:5000")
print("👤 admin / admin123")
print("=" * 40)

try:
    # استيراد التطبيق مباشرة
    from app import app, db
    
    # إنشاء الجداول إذا لم تكن موجودة
    with app.app_context():
        try:
            db.create_all()
            print("✅ تم إنشاء قاعدة البيانات")
        except Exception as e:
            print(f"⚠️ تحذير قاعدة البيانات: {e}")
    
    # تشغيل الخادم
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False,  # تعطيل إعادة التحميل التلقائي
        threaded=True
    )
    
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("تأكد من وجود ملف app.py في نفس المجلد")
    
except Exception as e:
    print(f"❌ خطأ في التشغيل: {e}")
    import traceback
    traceback.print_exc()

input("\nاضغط Enter للخروج...")
