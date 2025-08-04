#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام حساب التكاليف المتكامل للمطاعم
Integrated Restaurant Costing System

الملف الرئيسي لتشغيل النظام
Main launcher for the system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path

class RestaurantCostingLauncher:
    """واجهة تشغيل النظام الرئيسية"""
    
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("نظام حساب التكاليف المتكامل للمطاعم")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f8ff')
        
        # إعداد الخطوط
        try:
            self.title_font = ("Arial Unicode MS", 16, "bold")
            self.subtitle_font = ("Arial Unicode MS", 12)
            self.button_font = ("Arial Unicode MS", 11)
        except:
            self.title_font = ("Arial", 16, "bold")
            self.subtitle_font = ("Arial", 12)
            self.button_font = ("Arial", 11)
        
        self.create_header()
        self.create_main_menu()
        self.create_footer()
    
    def create_header(self):
        """إنشاء رأس الصفحة"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # العنوان الرئيسي
        title_label = tk.Label(header_frame, 
                              text="نظام حساب التكاليف المتكامل للمطاعم",
                              font=self.title_font,
                              fg='white',
                              bg='#2c3e50')
        title_label.pack(pady=15)
        
        # العنوان الفرعي
        subtitle_label = tk.Label(header_frame,
                                 text="Restaurant Integrated Costing System",
                                 font=self.subtitle_font,
                                 fg='#ecf0f1',
                                 bg='#2c3e50')
        subtitle_label.pack()
    
    def create_main_menu(self):
        """إنشاء القائمة الرئيسية"""
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # وصف النظام
        description_text = """
🍽️ نظام شامل لحساب تكاليف الوجبات في المطاعم

✨ المميزات الرئيسية:
• حساب تكلفة الوجبات بدقة عالية
• إدارة المواد الخام والمكونات
• حساب النسب المئوية لكل مكون
• تتبع أسعار الشراء والمخزون
• واجهة عربية/إنجليزية سهلة الاستخدام
• تقارير مفصلة وتصدير PDF
        """
        
        desc_label = tk.Label(main_frame,
                             text=description_text,
                             font=self.subtitle_font,
                             bg='#f0f8ff',
                             fg='#2c3e50',
                             justify=tk.RIGHT)
        desc_label.pack(pady=20)
        
        # أزرار النظام
        buttons_frame = tk.Frame(main_frame, bg='#f0f8ff')
        buttons_frame.pack(pady=20)
        
        # زر حساب التكاليف
        costing_btn = tk.Button(buttons_frame,
                               text="🧮 شاشة حساب التكاليف\nCosting Screen",
                               font=self.button_font,
                               bg='#3498db',
                               fg='white',
                               width=25,
                               height=3,
                               command=self.open_costing_screen,
                               cursor='hand2')
        costing_btn.pack(pady=10)
        
        # زر إدارة المواد الخام
        ingredients_btn = tk.Button(buttons_frame,
                                   text="📦 إدارة المواد الخام والوجبات\nIngredients & Meals Management",
                                   font=self.button_font,
                                   bg='#27ae60',
                                   fg='white',
                                   width=25,
                                   height=3,
                                   command=self.open_ingredients_manager,
                                   cursor='hand2')
        ingredients_btn.pack(pady=10)
        
        # زر النظام الويب
        web_btn = tk.Button(buttons_frame,
                           text="🌐 النظام الويب المتكامل\nWeb-based System",
                           font=self.button_font,
                           bg='#e74c3c',
                           fg='white',
                           width=25,
                           height=3,
                           command=self.open_web_system,
                           cursor='hand2')
        web_btn.pack(pady=10)
        
        # زر المساعدة
        help_btn = tk.Button(buttons_frame,
                            text="❓ المساعدة والدليل\nHelp & Guide",
                            font=self.button_font,
                            bg='#9b59b6',
                            fg='white',
                            width=25,
                            height=3,
                            command=self.show_help,
                            cursor='hand2')
        help_btn.pack(pady=10)
    
    def create_footer(self):
        """إنشاء تذييل الصفحة"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_text = "© 2024 نظام حساب التكاليف المتكامل - تم التطوير بواسطة Python & Tkinter"
        footer_label = tk.Label(footer_frame,
                               text=footer_text,
                               font=("Arial", 9),
                               fg='#bdc3c7',
                               bg='#34495e')
        footer_label.pack(pady=20)
    
    def open_costing_screen(self):
        """فتح شاشة حساب التكاليف"""
        try:
            # التحقق من وجود الملف
            if not Path("costing_system.py").exists():
                messagebox.showerror("خطأ", "ملف نظام التكاليف غير موجود!")
                return
            
            # تشغيل النظام
            subprocess.Popen([sys.executable, "costing_system.py"])
            messagebox.showinfo("تم", "تم فتح شاشة حساب التكاليف")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح شاشة التكاليف:\n{str(e)}")
    
    def open_ingredients_manager(self):
        """فتح إدارة المواد الخام"""
        try:
            # التحقق من وجود الملف
            if not Path("ingredients_manager.py").exists():
                messagebox.showerror("خطأ", "ملف إدارة المواد الخام غير موجود!")
                return
            
            # تشغيل النظام
            subprocess.Popen([sys.executable, "ingredients_manager.py"])
            messagebox.showinfo("تم", "تم فتح إدارة المواد الخام والوجبات")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح إدارة المواد الخام:\n{str(e)}")
    
    def open_web_system(self):
        """فتح النظام الويب"""
        try:
            # التحقق من وجود الملف
            if not Path("main_app.py").exists():
                messagebox.showerror("خطأ", "ملف النظام الويب غير موجود!")
                return
            
            # تشغيل النظام الويب
            subprocess.Popen([sys.executable, "main_app.py"])
            messagebox.showinfo("تم", "تم تشغيل النظام الويب\nيمكنك الوصول إليه عبر: http://localhost:5000")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تشغيل النظام الويب:\n{str(e)}")
    
    def show_help(self):
        """عرض المساعدة"""
        help_window = tk.Toplevel(self.root)
        help_window.title("المساعدة والدليل")
        help_window.geometry("700x600")
        help_window.configure(bg='white')
        
        # إنشاء نص المساعدة
        help_text = """
🔹 دليل استخدام نظام حساب التكاليف المتكامل

📋 نظرة عامة:
هذا النظام مصمم لمساعدة المطاعم في حساب تكلفة الوجبات بدقة عالية
ويتكون من ثلاثة أجزاء رئيسية:

🧮 1. شاشة حساب التكاليف (Costing Screen):
• حساب تكلفة الوجبات بناءً على المكونات
• عرض النسبة المئوية لكل مكون
• حساب تكلفة الحصة الواحدة
• حفظ وتحديث التكاليف

📦 2. إدارة المواد الخام والوجبات:
• إضافة وتعديل المواد الخام
• إدارة أسعار الشراء والمخزون
• إنشاء وتعديل الوجبات
• تتبع الموردين

🌐 3. النظام الويب المتكامل:
• واجهة ويب حديثة
• إدارة شاملة للمطعم
• تقارير مفصلة
• دعم متعدد المستخدمين

🔧 كيفية الاستخدام:

1️⃣ ابدأ بإدارة المواد الخام:
   • أضف جميع المواد الخام المستخدمة
   • حدد أسعار الشراء والوحدات
   • أدخل كميات المخزون

2️⃣ أنشئ الوجبات:
   • أضف الوجبات المختلفة
   • حدد عدد الحصص لكل وجبة

3️⃣ احسب التكاليف:
   • اختر الوجبة المطلوبة
   • أضف المكونات والكميات
   • احفظ التكاليف المحسوبة

💡 نصائح مهمة:
• تأكد من تحديث أسعار المواد الخام دورياً
• راجع النسب المئوية للمكونات
• احفظ التكاليف بعد كل تعديل
• استخدم النظام الويب للتقارير المفصلة

🆘 الدعم الفني:
في حالة وجود مشاكل أو استفسارات، يرجى مراجعة:
• ملفات التوثيق المرفقة
• أمثلة الاستخدام
• دليل المستخدم التفصيلي

📞 للمساعدة الإضافية:
تواصل مع فريق التطوير عبر البريد الإلكتروني
أو من خلال نظام التذاكر المتاح
        """
        
        # إنشاء نص قابل للتمرير
        text_frame = tk.Frame(help_window, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, 
                             font=("Arial Unicode MS", 10),
                             bg='white',
                             fg='#2c3e50',
                             wrap=tk.WORD,
                             padx=10,
                             pady=10)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # إضافة شريط التمرير
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # إدراج النص
        text_widget.insert(tk.END, help_text)
        text_widget.configure(state=tk.DISABLED)
        
        # زر الإغلاق
        close_btn = tk.Button(help_window,
                             text="إغلاق",
                             font=self.button_font,
                             bg='#e74c3c',
                             fg='white',
                             command=help_window.destroy)
        close_btn.pack(pady=10)

def main():
    """الوظيفة الرئيسية"""
    root = tk.Tk()
    
    # إعداد النمط
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
    
    # إنشاء التطبيق
    app = RestaurantCostingLauncher(root)
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    main()
