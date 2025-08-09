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
        # محاولة تثبيت المتطلبات مع إخفاء الإخراج المفصل
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ], capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            print("✅ تم تثبيت المتطلبات بنجاح")
            print("✅ Requirements installed successfully")
            return True
        else:
            print(f"⚠️ تحذير في تثبيت المتطلبات: {result.stderr}")
            print(f"⚠️ Warning installing requirements: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ انتهت مهلة تثبيت المتطلبات - المتابعة")
        print("⚠️ Requirements installation timeout - continuing")
        return False
    except FileNotFoundError:
        print("⚠️ ملف requirements.txt غير موجود - المتابعة")
        print("⚠️ requirements.txt not found - continuing")
        return False
    except Exception as e:
        print(f"⚠️ خطأ في تثبيت المتطلبات: {e}")
        print(f"⚠️ Error installing requirements: {e}")
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
    print("   كلمة المرور / Password: admin112233")
    print()
    print("🛑 لإيقاف التطبيق اضغط Ctrl+C")
    print("🛑 To stop the application press Ctrl+C")
    print("=" * 50)

    try:
        # استيراد وتشغيل التطبيق
        print("📦 تحميل التطبيق...")
        from app import app, db

        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        print("🗄️ إعداد قاعدة البيانات...")
        with app.app_context():
            try:
                db.create_all()
                print("✅ تم إعداد قاعدة البيانات")
            except Exception as e:
                print(f"⚠️ تحذير قاعدة البيانات: {e}")

        print("🌐 بدء الخادم...")
        print("🔄 إعادة التحميل التلقائي مفعلة")
        print("💡 استخدام Flask debug mode")

        # مسح cache القوالب
        app.jinja_env.cache = {}

        # تشغيل الخادم مع debug mode
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True, use_debugger=True)

    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف التطبيق بواسطة المستخدم")
        print("🛑 Application stopped by user")
    except ImportError as e:
        print(f"\n❌ خطأ في استيراد التطبيق: {e}")
        print("❌ Error importing application")
        print("💡 تأكد من وجود ملف app.py في نفس المجلد")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل التطبيق: {e}")
        print(f"❌ Error running application: {e}")
        import traceback
        traceback.print_exc()

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
    
    # تثبيت المتطلبات تلقائياً (بدون سؤال)
    print("📦 تثبيت المتطلبات تلقائياً...")
    print("📦 Installing requirements automatically...")

    if not install_requirements():
        print("⚠️ فشل تثبيت المتطلبات - المتابعة بدونها")
        print("⚠️ Failed to install requirements - continuing without them")
    
    # إعداد البيئة
    setup_environment()
    
    # تشغيل التطبيق
    run_app()

if __name__ == "__main__":
    main()
