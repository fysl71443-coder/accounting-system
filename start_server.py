#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل مبسط للخادم
Simple Server Startup Script
"""

import os
import sys

def main():
    """تشغيل الخادم مباشرة"""
    print("🚀 بدء تشغيل خادم المحاسبة...")
    print("🚀 Starting Accounting Server...")
    print()
    
    # إعداد متغيرات البيئة
    os.environ.setdefault('SECRET_KEY', 'dev-secret-key-change-in-production')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///accounting.db')
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    print("📍 الخادم سيعمل على: http://localhost:5000")
    print("📍 Server will run on: http://localhost:5000")
    print()
    print()
    print("🛑 لإيقاف الخادم اضغط Ctrl+C")
    print("🛑 To stop server press Ctrl+C")
    print("=" * 50)
    
    try:
        # استيراد وتشغيل التطبيق
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف الخادم")
        print("🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
