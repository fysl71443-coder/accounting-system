# -*- coding: utf-8 -*-
"""
شاشة تسجيل الدخول
Login Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from ..utils.language_manager import language_manager
from ..utils.arabic_support import ArabicSupport

class LoginWindow:
    """شاشة تسجيل الدخول"""
    
    def __init__(self, parent, db_manager, success_callback):
        """تهيئة شاشة تسجيل الدخول"""
        self.parent = parent
        self.db_manager = db_manager
        self.success_callback = success_callback
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # متغيرات الإدخال
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # ربط الأحداث
        self.bind_events()
        
        # تركيز على حقل اسم المستخدم
        self.username_entry.focus()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.window.title(language_manager.get_text("login_title"))
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        
        # توسيط النافذة
        self.center_window()
        
        # تطبيق الدعم العربي
        ArabicSupport.setup_arabic_support(self.window)
        
        # تعيين أيقونة النافذة (إذا كانت متوفرة)
        try:
            if os.path.exists("assets/icon.ico"):
                self.window.iconbitmap("assets/icon.ico")
        except:
            pass
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # شعار التطبيق
        self.create_logo(main_frame)
        
        # عنوان التطبيق
        title_label = ArabicSupport.create_arabic_label(
            main_frame,
            language_manager.get_text("login_title"),
            font=ArabicSupport.get_arabic_font(16, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # إطار تسجيل الدخول
        login_frame = ttk.LabelFrame(
            main_frame,
            text=language_manager.get_text("login"),
            padding="20"
        )
        login_frame.pack(fill=tk.X, pady=(0, 20))
        
        # حقل اسم المستخدم
        username_label = ArabicSupport.create_arabic_label(
            login_frame,
            language_manager.get_text("username")
        )
        username_label.pack(anchor=tk.W if language_manager.is_rtl() else tk.W)
        
        self.username_entry = ArabicSupport.create_arabic_entry(
            login_frame,
            textvariable=self.username_var,
            width=30
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 15))
        
        # حقل كلمة المرور
        password_label = ArabicSupport.create_arabic_label(
            login_frame,
            language_manager.get_text("password")
        )
        password_label.pack(anchor=tk.W if language_manager.is_rtl() else tk.W)
        
        self.password_entry = ArabicSupport.create_arabic_entry(
            login_frame,
            textvariable=self.password_var,
            show="*",
            width=30
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 15))
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(login_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # زر تسجيل الدخول
        self.login_button = ArabicSupport.create_arabic_button(
            buttons_frame,
            language_manager.get_text("login"),
            command=self.login,
            width=15
        )
        self.login_button.pack(side=tk.RIGHT if language_manager.is_rtl() else tk.LEFT, padx=(0, 10))
        
        # رابط نسيت كلمة المرور
        forgot_label = ArabicSupport.create_arabic_label(
            buttons_frame,
            language_manager.get_text("forgot_password"),
            foreground="blue",
            cursor="hand2"
        )
        forgot_label.pack(side=tk.LEFT if language_manager.is_rtl() else tk.RIGHT)
        forgot_label.bind("<Button-1>", self.forgot_password)
        
        # إطار اختيار اللغة
        language_frame = ttk.LabelFrame(
            main_frame,
            text=language_manager.get_text("language"),
            padding="10"
        )
        language_frame.pack(fill=tk.X)
        
        # أزرار اللغة
        lang_buttons_frame = ttk.Frame(language_frame)
        lang_buttons_frame.pack()
        
        # زر العربية
        arabic_button = ArabicSupport.create_arabic_button(
            lang_buttons_frame,
            "العربية",
            command=lambda: self.change_language("ar"),
            width=10
        )
        arabic_button.pack(side=tk.LEFT, padx=5)
        
        # زر الإنجليزية
        english_button = ArabicSupport.create_arabic_button(
            lang_buttons_frame,
            "English",
            command=lambda: self.change_language("en"),
            width=10
        )
        english_button.pack(side=tk.LEFT, padx=5)
    
    def create_logo(self, parent):
        """إنشاء شعار التطبيق"""
        try:
            # محاولة تحميل الشعار
            logo_path = "assets/logo.png"
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(parent, image=self.logo_image)
                logo_label.pack(pady=(0, 20))
            else:
                # شعار نصي إذا لم تكن الصورة متوفرة
                logo_label = ArabicSupport.create_arabic_label(
                    parent,
                    "💼",
                    font=ArabicSupport.get_arabic_font(48)
                )
                logo_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"خطأ في تحميل الشعار: {e}")
            # شعار نصي بديل
            logo_label = ArabicSupport.create_arabic_label(
                parent,
                "💼",
                font=ArabicSupport.get_arabic_font(48)
            )
            logo_label.pack(pady=(0, 20))
    
    def bind_events(self):
        """ربط الأحداث"""
        # تسجيل الدخول بالضغط على Enter
        self.window.bind('<Return>', lambda e: self.login())
        
        # إغلاق النافذة
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def login(self):
        """تسجيل الدخول"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # التحقق من صحة البيانات
        if not username or not password:
            messagebox.showerror(
                language_manager.get_text("error"),
                "يرجى إدخال اسم المستخدم وكلمة المرور"
            )
            return
        
        # محاولة تسجيل الدخول
        user_data = self.db_manager.authenticate_user(username, password)
        
        if user_data:
            messagebox.showinfo(
                language_manager.get_text("success"),
                language_manager.get_text("login_success")
            )
            
            # إغلاق نافذة تسجيل الدخول
            self.window.destroy()
            
            # استدعاء دالة النجاح
            self.success_callback(user_data)
        else:
            messagebox.showerror(
                language_manager.get_text("error"),
                language_manager.get_text("invalid_credentials")
            )
            
            # مسح كلمة المرور
            self.password_var.set("")
            self.password_entry.focus()
    
    def forgot_password(self, event=None):
        """نسيت كلمة المرور"""
        messagebox.showinfo(
            language_manager.get_text("info"),
            "يرجى الاتصال بمدير النظام لإعادة تعيين كلمة المرور"
        )
    
    def change_language(self, language_code):
        """تغيير اللغة"""
        if language_manager.set_language(language_code):
            # إعادة إنشاء الواجهة باللغة الجديدة
            self.window.destroy()
            self.__init__(self.parent, self.db_manager, self.success_callback)
    
    def on_closing(self):
        """معالج إغلاق النافذة"""
        self.parent.quit()
