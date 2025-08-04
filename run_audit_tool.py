#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت تشغيل أداة المراجعة الذكية
Quick Launch Script for Smart Audit Tool
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """فحص المتطلبات"""
    print("🔍 فحص المتطلبات...")
    print("🔍 Checking requirements...")
    
    required_packages = [
        'pandas',
        'openpyxl', 
        'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - متوفر")
        except ImportError:
            print(f"❌ {package} - غير متوفر")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 تثبيت الحزم المفقودة...")
        print(f"📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ تم تثبيت {package}")
            except subprocess.CalledProcessError:
                print(f"❌ فشل في تثبيت {package}")
                return False
    
    return True

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔍 أداة المراجعة الذكية للنظام المحاسبي")
    print("🔍 Smart Audit Tool for Accounting System")
    print("=" * 60)
    print()
    
    # فحص وجود ملف الأداة
    audit_tool_file = Path("system_audit_tool.py")
    if not audit_tool_file.exists():
        print("❌ ملف الأداة غير موجود: system_audit_tool.py")
        print("❌ Audit tool file not found: system_audit_tool.py")
        return
    
    # فحص المتطلبات
    if not check_requirements():
        print("❌ فشل في تثبيت المتطلبات")
        print("❌ Failed to install requirements")
        return
    
    print("\n🚀 تشغيل أداة المراجعة...")
    print("🚀 Launching audit tool...")
    
    try:
        # تشغيل الأداة
        import system_audit_tool
        system_audit_tool.main()
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الأداة: {e}")
        print(f"❌ Error running audit tool: {e}")

if __name__ == "__main__":
    main()
