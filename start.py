#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل بسيط للتطبيق
Simple startup script
"""

import os
import sys

def main():
    """تشغيل التطبيق"""
    print("🚀 بدء تشغيل نظام المحاسبة...")
    print("🚀 Starting Accounting System...")
    print()
    print("📍 التطبيق سيعمل على: http://localhost:5000")
    print("📍 Application will run on: http://localhost:5000")
    print()
    print("👤 بيانات تسجيل الدخول:")
    print("👤 Login credentials:")
    print("   المستخدم / Username: admin")
    print("   كلمة المرور / Password: admin123")
    print()
    print("🛑 لإيقاف التطبيق اضغط Ctrl+C")
    print("🛑 To stop the application press Ctrl+C")
    print("=" * 50)
    
    try:
        # استيراد وتشغيل التطبيق
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف التطبيق")
        print("🛑 Application stopped")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل التطبيق: {e}")
        print(f"❌ Error running application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
