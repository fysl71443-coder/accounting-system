#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
قاذف التطبيقات الرئيسي - Main Application Launcher
نظام محاسبي احترافي مع دعم اللغة العربية والإنجليزية
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import subprocess
import sys
import os

class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.language = "ar"  # Default to Arabic
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("نظام المحاسبة الاحترافي - Professional Accounting System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # إعداد الخطوط
        self.arabic_font = Font(family="Arial Unicode MS", size=12)
        self.title_font = Font(family="Arial Unicode MS", size=16, weight="bold")
        
        # إنشاء الواجهة الرئيسية
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
    def create_header(self):
        """إنشاء رأس الصفحة"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # العنوان الرئيسي
        title_label = tk.Label(header_frame, 
                              text="نظام المحاسبة الاحترافي\nProfessional Accounting System",
                              font=self.title_font, 
                              fg='white', 
                              bg='#2c3e50',
                              justify=tk.CENTER)
        title_label.pack(expand=True)
        
        # زر تغيير اللغة
        lang_button = tk.Button(header_frame, 
                               text="English / العربية",
                               command=self.toggle_language,
                               bg='#3498db',
                               fg='white',
                               font=self.arabic_font,
                               relief=tk.FLAT,
                               padx=20)
        lang_button.place(relx=0.95, rely=0.5, anchor="center")
        
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عنوان القسم
        section_title = tk.Label(main_frame,
                                text="اختر التطبيق المطلوب - Choose Application",
                                font=self.title_font,
                                bg='#f0f0f0',
                                fg='#2c3e50')
        section_title.pack(pady=(0, 20))
        
        # إطار التطبيقات
        apps_frame = tk.Frame(main_frame, bg='#f0f0f0')
        apps_frame.pack(fill="both", expand=True)
        
        # تطبيق المصروفات المتقدمة
        self.create_app_card(apps_frame, 
                            "شاشة المصروفات المتقدمة\nAdvanced Expenses Screen",
                            "إدارة شاملة للمصروفات مع تصنيفات ذكية وتحليلات مفصلة\nComprehensive expense management with smart categorization",
                            "#e74c3c",
                            self.launch_expenses_app,
                            row=0, col=0)
        
        # تطبيق المدفوعات والمستحقات
        self.create_app_card(apps_frame,
                            "شاشة المدفوعات والمستحقات\nPayments & Dues Screen", 
                            "متابعة المدفوعات والمستحقات مع إمكانية تسجيل الدفعات\nTrack payments and dues with payment recording capabilities",
                            "#27ae60",
                            self.launch_payments_app,
                            row=0, col=1)
        
        # تطبيق حساب التكلفة
        self.create_app_card(apps_frame,
                            "شاشة حساب التكلفة للمطاعم\nRestaurant Costing Screen",
                            "حساب تكلفة الوجبات بناءً على المكونات والنسب\nCalculate meal costs based on ingredients and ratios",
                            "#3498db",
                            self.launch_costing_app,
                            row=1, col=0)
        
        # تطبيق إضافي (مستقبلي)
        self.create_app_card(apps_frame,
                            "تطبيقات إضافية\nAdditional Applications",
                            "المزيد من التطبيقات قريباً\nMore applications coming soon",
                            "#95a5a6",
                            self.show_coming_soon,
                            row=1, col=1)
        
    def create_app_card(self, parent, title, description, color, command, row, col):
        """إنشاء بطاقة تطبيق"""
        # إطار البطاقة
        card_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # تكوين الشبكة
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # محتوى البطاقة
        content_frame = tk.Frame(card_frame, bg=color, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # العنوان
        title_label = tk.Label(content_frame,
                              text=title,
                              font=self.arabic_font,
                              bg=color,
                              fg='white',
                              justify=tk.CENTER,
                              wraplength=250)
        title_label.pack(pady=(0, 10))
        
        # الوصف
        desc_label = tk.Label(content_frame,
                             text=description,
                             font=Font(family="Arial Unicode MS", size=10),
                             bg=color,
                             fg='white',
                             justify=tk.CENTER,
                             wraplength=250)
        desc_label.pack(pady=(0, 20))
        
        # زر التشغيل
        launch_button = tk.Button(content_frame,
                                 text="تشغيل التطبيق\nLaunch App",
                                 command=command,
                                 bg='white',
                                 fg=color,
                                 font=self.arabic_font,
                                 relief=tk.FLAT,
                                 padx=20,
                                 pady=10,
                                 cursor="hand2")
        launch_button.pack()
        
        # تأثير hover
        def on_enter(e):
            launch_button.config(bg='#ecf0f1')
            
        def on_leave(e):
            launch_button.config(bg='white')
            
        launch_button.bind("<Enter>", on_enter)
        launch_button.bind("<Leave>", on_leave)
        
    def create_footer(self):
        """إنشاء تذييل الصفحة"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=60)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        # معلومات التذييل
        footer_text = tk.Label(footer_frame,
                              text="نظام المحاسبة الاحترافي © 2025 - Professional Accounting System\nتم التطوير بواسطة فريق التطوير المتخصص",
                              font=Font(family="Arial Unicode MS", size=9),
                              bg='#34495e',
                              fg='white',
                              justify=tk.CENTER)
        footer_text.pack(expand=True)
        
    def launch_expenses_app(self):
        """تشغيل تطبيق المصروفات المتقدمة"""
        try:
            subprocess.Popen([sys.executable, "advanced_expenses_gui.py"])
            messagebox.showinfo("تشغيل التطبيق / Launch App", 
                               "تم تشغيل تطبيق المصروفات المتقدمة\nAdvanced Expenses app launched")
        except Exception as e:
            messagebox.showerror("خطأ / Error", 
                                f"خطأ في تشغيل التطبيق / Error launching app:\n{str(e)}")
    
    def launch_payments_app(self):
        """تشغيل تطبيق المدفوعات والمستحقات"""
        try:
            subprocess.Popen([sys.executable, "payments_dues_gui.py"])
            messagebox.showinfo("تشغيل التطبيق / Launch App",
                               "تم تشغيل تطبيق المدفوعات والمستحقات\nPayments & Dues app launched")
        except Exception as e:
            messagebox.showerror("خطأ / Error",
                                f"خطأ في تشغيل التطبيق / Error launching app:\n{str(e)}")
    
    def launch_costing_app(self):
        """تشغيل تطبيق حساب التكلفة"""
        try:
            subprocess.Popen([sys.executable, "costing_screen_gui.py"])
            messagebox.showinfo("تشغيل التطبيق / Launch App",
                               "تم تشغيل تطبيق حساب التكلفة\nCosting Screen app launched")
        except Exception as e:
            messagebox.showerror("خطأ / Error",
                                f"خطأ في تشغيل التطبيق / Error launching app:\n{str(e)}")
    
    def show_coming_soon(self):
        """عرض رسالة قريباً"""
        messagebox.showinfo("قريباً / Coming Soon",
                           "المزيد من التطبيقات قريباً\nMore applications coming soon")
    
    def toggle_language(self):
        """تبديل اللغة"""
        if self.language == "ar":
            self.language = "en"
            messagebox.showinfo("Language", "Language changed to English\nPlease restart the application")
        else:
            self.language = "ar"
            messagebox.showinfo("اللغة", "تم تغيير اللغة إلى العربية\nيرجى إعادة تشغيل التطبيق")


def check_requirements():
    """فحص المتطلبات"""
    required_files = [
        "advanced_expenses_gui.py",
        "payments_dues_gui.py", 
        "costing_screen_gui.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        messagebox.showerror("ملفات مفقودة / Missing Files",
                            f"الملفات التالية مفقودة / The following files are missing:\n" + 
                            "\n".join(missing_files))
        return False
    
    return True


def main():
    """الوظيفة الرئيسية"""
    # فحص المتطلبات
    if not check_requirements():
        return
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    
    # تعيين أيقونة النافذة (إذا كانت متوفرة)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    # إنشاء التطبيق
    app = MainLauncher(root)
    
    # تشغيل التطبيق
    root.mainloop()


if __name__ == "__main__":
    main()
