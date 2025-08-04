#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل البرنامج المحاسبي
Accounting System Launcher
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_requirements():
    """التحقق من المتطلبات"""
    required_modules = [
        'tkinter',
        'sqlite3',
        'PIL',
        'matplotlib',
        'pandas'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'PIL':
                import PIL
            elif module == 'tkinter':
                import tkinter
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"""
المتطلبات التالية غير متوفرة:
Missing requirements:

{', '.join(missing_modules)}

يرجى تثبيتها باستخدام:
Please install them using:

pip install {' '.join(missing_modules)}
        """
        
        # إنشاء نافذة خطأ بسيطة
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("خطأ في المتطلبات - Requirements Error", error_msg)
        root.destroy()
        return False
    
    return True

def main():
    """الوظيفة الرئيسية"""
    try:
        # التحقق من المتطلبات
        if not check_requirements():
            sys.exit(1)
        
        # إضافة مسار المشروع
        project_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_path)
        
        # تشغيل التطبيق
        from main import main as run_app
        run_app()
        
    except Exception as e:
        # إنشاء نافذة خطأ
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "خطأ في التطبيق - Application Error",
            f"حدث خطأ غير متوقع:\nUnexpected error occurred:\n\n{str(e)}"
        )
        root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()
