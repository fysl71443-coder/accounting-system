#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تثبيت المتطلبات للبرنامج المحاسبي
Requirements Installation Script for Accounting System
"""

import subprocess
import sys
import os

def install_package(package):
    """تثبيت حزمة Python"""
    try:
        print(f"جاري تثبيت {package}...")
        print(f"Installing {package}...")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ تم تثبيت {package} بنجاح")
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تثبيت {package}: {e}")
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("مرحباً بك في برنامج تثبيت متطلبات النظام المحاسبي")
    print("Welcome to Accounting System Requirements Installer")
    print("=" * 60)
    
    # قائمة المتطلبات
    requirements = [
        "Pillow>=9.0.0",
        "reportlab>=3.6.0", 
        "matplotlib>=3.5.0",
        "pandas>=1.4.0",
        "openpyxl>=3.0.0",
        "python-barcode>=0.13.0",
        "qrcode>=7.3.0",
        "arabic-reshaper>=2.1.0",
        "python-bidi>=0.4.0",
        "tkcalendar>=1.6.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0"
    ]
    
    print(f"\nسيتم تثبيت {len(requirements)} حزمة...")
    print(f"\n{len(requirements)} packages will be installed...")
    
    # تحديث pip أولاً
    print("\nجاري تحديث pip...")
    print("\nUpdating pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ تم تحديث pip بنجاح")
        print("✅ pip updated successfully")
    except:
        print("⚠️ تعذر تحديث pip، سيتم المتابعة...")
        print("⚠️ Could not update pip, continuing...")
    
    # تثبيت المتطلبات
    successful = 0
    failed = 0
    
    for requirement in requirements:
        if install_package(requirement):
            successful += 1
        else:
            failed += 1
        print("-" * 40)
    
    # النتائج النهائية
    print("\n" + "=" * 60)
    print("نتائج التثبيت - Installation Results")
    print("=" * 60)
    print(f"✅ تم تثبيت بنجاح: {successful}")
    print(f"✅ Successfully installed: {successful}")
    print(f"❌ فشل في التثبيت: {failed}")
    print(f"❌ Failed to install: {failed}")
    
    if failed == 0:
        print("\n🎉 تم تثبيت جميع المتطلبات بنجاح!")
        print("🎉 All requirements installed successfully!")
        print("\nيمكنك الآن تشغيل البرنامج باستخدام:")
        print("You can now run the program using:")
        print("python run.py")
    else:
        print(f"\n⚠️ فشل في تثبيت {failed} حزمة")
        print(f"⚠️ Failed to install {failed} packages")
        print("\nيرجى المحاولة مرة أخرى أو تثبيت الحزم يدوياً")
        print("Please try again or install packages manually")
    
    print("\n" + "=" * 60)
    
    # انتظار إدخال المستخدم قبل الإغلاق
    input("\nاضغط Enter للخروج... / Press Enter to exit...")

if __name__ == "__main__":
    main()
