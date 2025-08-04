#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج المحاسبة المتكامل
Integrated Accounting System

المطور: نظام محاسبي شامل باللغة العربية
Developer: Comprehensive Arabic Accounting System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# إضافة مسار المشروع إلى sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.db_manager import DatabaseManager
from src.gui.login_window import LoginWindow
from src.utils.config import Config
from src.utils.arabic_support import ArabicSupport

class AccountingApp:
    """الفئة الرئيسية للبرنامج المحاسبي"""
    
    def __init__(self):
        """تهيئة التطبيق"""
        self.root = None
        self.db_manager = None
        self.current_user = None
        self.config = Config()
        
    def initialize_database(self):
        """تهيئة قاعدة البيانات"""
        try:
            self.db_manager = DatabaseManager()
            self.db_manager.create_tables()
            self.db_manager.create_default_admin()
            return True
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"فشل في تهيئة قاعدة البيانات:\n{str(e)}")
            return False
    
    def show_login(self):
        """عرض شاشة تسجيل الدخول"""
        if self.root:
            self.root.destroy()
            
        self.root = tk.Tk()
        self.root.withdraw()  # إخفاء النافذة الرئيسية مؤقتاً
        
        # تطبيق الدعم العربي
        ArabicSupport.setup_arabic_support(self.root)
        
        # إنشاء نافذة تسجيل الدخول
        login_window = LoginWindow(self.root, self.db_manager, self.on_login_success)
        
        # تشغيل حلقة الأحداث
        self.root.mainloop()
    
    def on_login_success(self, user_data):
        """معالج نجاح تسجيل الدخول"""
        self.current_user = user_data
        self.show_main_dashboard()
    
    def show_main_dashboard(self):
        """عرض الشاشة الرئيسية"""
        # سيتم تطوير هذه الوظيفة لاحقاً
        from src.gui.main_dashboard import MainDashboard
        
        # إغلاق نافذة تسجيل الدخول
        for widget in self.root.winfo_children():
            if hasattr(widget, 'destroy'):
                widget.destroy()
        
        # إظهار النافذة الرئيسية
        self.root.deiconify()
        
        # إنشاء لوحة التحكم الرئيسية
        dashboard = MainDashboard(self.root, self.db_manager, self.current_user)
    
    def run(self):
        """تشغيل التطبيق"""
        try:
            # تهيئة قاعدة البيانات
            if not self.initialize_database():
                return
            
            # عرض شاشة تسجيل الدخول
            self.show_login()
            
        except Exception as e:
            messagebox.showerror("خطأ في التطبيق", f"حدث خطأ غير متوقع:\n{str(e)}")
        finally:
            # تنظيف الموارد
            if self.db_manager:
                self.db_manager.close()

def main():
    """النقطة الرئيسية لتشغيل التطبيق"""
    app = AccountingApp()
    app.run()

if __name__ == "__main__":
    main()
