#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل سريع للتطبيق المحلي
Quick Local Run Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """التحقق من إصدار Python"""
    if sys.version_info < (3, 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - متوافق")
    return True

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 جاري تثبيت المتطلبات...")
    print("📦 Installing requirements...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ تم تثبيت المتطلبات بنجاح")
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تثبيت المتطلبات: {e}")
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_environment():
    """إعداد متغيرات البيئة"""
    print("⚙️ إعداد متغيرات البيئة...")
    print("⚙️ Setting up environment variables...")
    
    # إعداد متغيرات البيئة الافتراضية
    os.environ.setdefault('SECRET_KEY', 'dev-secret-key-change-in-production')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///accounting.db')
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    print("✅ تم إعداد متغيرات البيئة")
    print("✅ Environment variables set")

def run_app():
    """تشغيل التطبيق"""
    print("🚀 بدء تشغيل التطبيق...")
    print("🚀 Starting application...")
    print()
    print("📍 التطبيق سيعمل على: http://localhost:5000")
    print("📍 Application will run on: http://localhost:5000")
    print()
    print("👤 بيانات تسجيل الدخول الافتراضية:")
    print("👤 Default login credentials:")
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

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🏢 نظام المحاسبة المتكامل - Integrated Accounting System")
    print("🚀 أداة التشغيل السريع - Quick Launch Tool")
    print("=" * 60)
    print()
    
    # التحقق من إصدار Python
    if not check_python_version():
        return
    
    # التحقق من وجود ملف المتطلبات
    if not Path("requirements.txt").exists():
        print("❌ ملف requirements.txt غير موجود")
        print("❌ requirements.txt file not found")
        return
    
    # التحقق من وجود ملف التطبيق
    if not Path("app.py").exists():
        print("❌ ملف app.py غير موجود")
        print("❌ app.py file not found")
        return
    
    # سؤال المستخدم عن تثبيت المتطلبات
    install_deps = input("هل تريد تثبيت/تحديث المتطلبات؟ (y/n) / Install/update requirements? (y/n): ").lower().strip()
    
    if install_deps in ['y', 'yes', 'نعم', 'ن']:
        if not install_requirements():
            return
    
    # إعداد البيئة
    setup_environment()
    
    # تشغيل التطبيق
    run_app()

if __name__ == "__main__":
    main()
