#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل التطبيق بشكل مبسط
Simple App Runner
"""

if __name__ == "__main__":
    print("🚀 تشغيل نظام المحاسبة...")
    print("📍 الرابط: http://localhost:5000")
    print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
    print("👤 المستخدم: admin | كلمة المرور: admin123")
    print("=" * 50)
    
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
