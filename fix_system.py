#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح شامل للنظام
Comprehensive System Fix
"""

import os
import shutil
from pathlib import Path

def fix_system():
    """إصلاح المشاكل المحتملة في النظام"""
    
    print("🔧 بدء إصلاح النظام...")
    print("=" * 50)
    
    # 1. إصلاح ملف requirements.txt
    print("1️⃣ إصلاح ملف requirements.txt...")
    requirements_content = """Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Werkzeug==2.3.7
Jinja2==3.1.2
requests==2.31.0
python-dateutil==2.8.2
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print("✅ تم إصلاح ملف requirements.txt")
    
    # 2. إنشاء ملف تشغيل محسن
    print("\n2️⃣ إنشاء ملف تشغيل محسن...")
    run_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

def main():
    print("🚀 تشغيل نظام المحاسبة المتكامل")
    print("=" * 50)
    print("📍 الرابط: http://localhost:5000")
    print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
    print("👤 المستخدم: admin | كلمة المرور: admin123")
    print("=" * 50)
    
    try:
        from app import app, db
        
        # إنشاء قاعدة البيانات
        with app.app_context():
            db.create_all()
            print("✅ تم إعداد قاعدة البيانات")
        
        # تشغيل التطبيق
        print("🌐 بدء تشغيل الخادم...")
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
"""
    
    with open('run_fixed.py', 'w', encoding='utf-8') as f:
        f.write(run_content)
    print("✅ تم إنشاء ملف run_fixed.py")
    
    # 3. إنشاء ملف batch للتشغيل السريع
    print("\n3️⃣ إنشاء ملف batch للتشغيل السريع...")
    batch_content = """@echo off
chcp 65001 > nul
echo 🚀 تشغيل نظام المحاسبة...
echo ================================
echo 📍 الرابط: http://localhost:5000
echo 🌟 الشاشة الموحدة: http://localhost:5000/unified_products
echo 👤 المستخدم: admin ^| كلمة المرور: admin123
echo ================================
echo.
python run_fixed.py
pause
"""
    
    with open('start_system.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print("✅ تم إنشاء ملف start_system.bat")
    
    # 4. إنشاء ملف تعليمات
    print("\n4️⃣ إنشاء ملف التعليمات...")
    instructions = """# نظام المحاسبة المتكامل - دليل الاستخدام

## طرق تشغيل النظام:

### الطريقة الأولى (الأسهل):
1. انقر نقراً مزدوجاً على ملف `start_system.bat`
2. انتظر حتى يبدأ النظام
3. افتح المتصفح واذهب إلى: http://localhost:5000

### الطريقة الثانية:
1. افتح Command Prompt أو PowerShell
2. انتقل إلى مجلد المشروع
3. شغل الأمر: `python run_fixed.py`

### الطريقة الثالثة:
1. شغل الأمر: `python run_local.py`
2. اختر 'n' عند السؤال عن تثبيت المتطلبات

## بيانات تسجيل الدخول:
- المستخدم: admin
- كلمة المرور: admin123

## الروابط المهمة:
- الصفحة الرئيسية: http://localhost:5000
- الشاشة الموحدة: http://localhost:5000/unified_products
- فاتورة جديدة: http://localhost:5000/new_sale

## حل المشاكل الشائعة:

### إذا لم تظهر القائمة الجانبية:
1. حدث الصفحة (F5)
2. امسح cache المتصفح (Ctrl+F5)
3. جرب متصفح آخر
4. تأكد من تسجيل الدخول

### إذا ظهرت أخطاء:
1. تأكد من تثبيت Python 3.8+
2. شغل: `pip install -r requirements.txt`
3. تأكد من عدم وجود تطبيق آخر على المنفذ 5000

## المميزات الجديدة:
- 🌟 الشاشة الموحدة لإدارة المنتجات والتكاليف
- 📊 حساب التكاليف التفصيلي
- 📦 إدارة المواد الخام
- 💰 حساب هامش الربح التلقائي
- 🎨 واجهة محسنة مع تأثيرات بصرية

## الدعم:
إذا واجهت أي مشاكل، تأكد من:
1. تشغيل النظام كمدير (Run as Administrator)
2. إغلاق برامج مكافحة الفيروسات مؤقتاً
3. التأكد من اتصال الإنترنت لتحميل CSS/JS
"""
    
    with open('README_AR.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    print("✅ تم إنشاء ملف README_AR.md")
    
    # 5. إنشاء ملف اختبار سريع
    print("\n5️⃣ إنشاء ملف اختبار سريع...")
    quick_test = """#!/usr/bin/env python3
import requests
import webbrowser
import time

def quick_test():
    print("🧪 اختبار سريع للنظام...")
    
    try:
        # اختبار الاتصال
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ النظام يعمل!")
            print("🌐 فتح المتصفح...")
            webbrowser.open('http://localhost:5000')
        else:
            print("❌ النظام لا يعمل")
    except:
        print("❌ لا يمكن الوصول للنظام")
        print("💡 تأكد من تشغيل النظام أولاً")

if __name__ == "__main__":
    quick_test()
"""
    
    with open('quick_test.py', 'w', encoding='utf-8') as f:
        f.write(quick_test)
    print("✅ تم إنشاء ملف quick_test.py")
    
    print("\n" + "=" * 50)
    print("🎉 تم إصلاح النظام بنجاح!")
    print("\n📋 الملفات الجديدة:")
    print("- run_fixed.py (ملف تشغيل محسن)")
    print("- start_system.bat (تشغيل سريع)")
    print("- README_AR.md (دليل الاستخدام)")
    print("- quick_test.py (اختبار سريع)")
    print("\n🚀 لتشغيل النظام:")
    print("1. انقر على start_system.bat")
    print("2. أو شغل: python run_fixed.py")
    print("=" * 50)

if __name__ == "__main__":
    fix_system()
