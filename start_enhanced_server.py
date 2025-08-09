#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل الخادم مع الطباعة المحسنة
Run Server with Enhanced Print
"""

import os
import sys

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'
os.environ['FLASK_ENV'] = 'development'

print("🚀 تشغيل خادم نظام المحاسبة مع الطباعة المحسنة")
print("📍 http://localhost:5000")
print("👤 admin / admin123")
print("🌟 الطباعة المحسنة متاحة الآن!")
print("=" * 50)

try:
    from app import app, db
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        print("✅ قاعدة البيانات جاهزة")
        
        # فحص routes المتاحة
        print("\n📋 Routes الطباعة المتاحة:")
        for rule in app.url_map.iter_rules():
            if 'print' in rule.rule:
                print(f"   🔗 {rule.rule}")
    
    print("\n🌐 بدء الخادم...")
    print("🔗 شاشة المدفوعات: http://localhost:5000/payments_dues")
    print("🌟 الطباعة المحسنة: http://localhost:5000/print_invoices_enhanced")
    print("📄 الطباعة العادية: http://localhost:5000/print_invoices_preview")
    
    # تشغيل الخادم
    app.run(
        debug=True,
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
