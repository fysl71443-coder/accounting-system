# -*- coding: utf-8 -*-
"""
دعم اللغة العربية في واجهة المستخدم
Arabic Language Support for UI
"""

import tkinter as tk
from tkinter import font
import sys
import os

try:
    import arabic_reshaper
    import bidi.algorithm
    ARABIC_SUPPORT_AVAILABLE = True
except ImportError:
    ARABIC_SUPPORT_AVAILABLE = False
    print("تحذير: مكتبات الدعم العربي غير متوفرة. سيتم استخدام النص العادي.")

class ArabicSupport:
    """فئة دعم اللغة العربية"""
    
    @staticmethod
    def setup_arabic_support(root):
        """إعداد الدعم العربي للنافذة الرئيسية"""
        try:
            # تعيين الخط العربي الافتراضي
            arabic_font = font.nametofont("TkDefaultFont")
            arabic_font.configure(family="Arial Unicode MS", size=10)
            
            # تطبيق الخط على جميع العناصر
            root.option_add("*Font", arabic_font)
            
            # تعيين اتجاه النص من اليمين لليسار للعربية
            root.option_add("*Text.justify", "right")
            
        except Exception as e:
            print(f"خطأ في إعداد الدعم العربي: {e}")
    
    @staticmethod
    def reshape_arabic_text(text):
        """إعادة تشكيل النص العربي للعرض الصحيح"""
        if not ARABIC_SUPPORT_AVAILABLE or not text:
            return text
        
        try:
            # إعادة تشكيل النص العربي
            reshaped_text = arabic_reshaper.reshape(text)
            # تطبيق خوارزمية الاتجاه الثنائي
            bidi_text = bidi.algorithm.get_display(reshaped_text)
            return bidi_text
        except Exception as e:
            print(f"خطأ في إعادة تشكيل النص العربي: {e}")
            return text
    
    @staticmethod
    def get_arabic_font(size=10, weight="normal"):
        """الحصول على خط عربي مناسب"""
        try:
            # قائمة الخطوط العربية المفضلة
            arabic_fonts = [
                "Arial Unicode MS",
                "Tahoma",
                "Segoe UI",
                "Arial",
                "Times New Roman"
            ]
            
            # البحث عن خط متاح
            available_fonts = font.families()
            for font_name in arabic_fonts:
                if font_name in available_fonts:
                    return font.Font(family=font_name, size=size, weight=weight)
            
            # استخدام الخط الافتراضي إذا لم يتم العثور على خط عربي
            return font.Font(size=size, weight=weight)
            
        except Exception as e:
            print(f"خطأ في الحصول على الخط العربي: {e}")
            return font.Font(size=size, weight=weight)
    
    @staticmethod
    def configure_widget_for_arabic(widget, text=""):
        """تكوين عنصر واجهة للدعم العربي"""
        try:
            # تطبيق الخط العربي
            arabic_font = ArabicSupport.get_arabic_font()
            widget.configure(font=arabic_font)
            
            # تعيين النص المُعاد تشكيله
            if text:
                reshaped_text = ArabicSupport.reshape_arabic_text(text)
                if hasattr(widget, 'configure'):
                    if 'text' in widget.keys():
                        widget.configure(text=reshaped_text)
                    elif hasattr(widget, 'insert'):
                        widget.delete(0, tk.END)
                        widget.insert(0, reshaped_text)
            
        except Exception as e:
            print(f"خطأ في تكوين العنصر للدعم العربي: {e}")
    
    @staticmethod
    def create_arabic_label(parent, text, **kwargs):
        """إنشاء تسمية مع دعم عربي"""
        reshaped_text = ArabicSupport.reshape_arabic_text(text)
        arabic_font = ArabicSupport.get_arabic_font()
        
        label = tk.Label(parent, text=reshaped_text, font=arabic_font, **kwargs)
        return label
    
    @staticmethod
    def create_arabic_button(parent, text, command=None, **kwargs):
        """إنشاء زر مع دعم عربي"""
        reshaped_text = ArabicSupport.reshape_arabic_text(text)
        arabic_font = ArabicSupport.get_arabic_font()
        
        button = tk.Button(parent, text=reshaped_text, font=arabic_font, command=command, **kwargs)
        return button
    
    @staticmethod
    def create_arabic_entry(parent, **kwargs):
        """إنشاء حقل إدخال مع دعم عربي"""
        arabic_font = ArabicSupport.get_arabic_font()
        
        entry = tk.Entry(parent, font=arabic_font, justify='right', **kwargs)
        return entry
    
    @staticmethod
    def is_arabic_text(text):
        """التحقق من وجود نص عربي"""
        if not text:
            return False
        
        arabic_chars = set(range(0x0600, 0x06FF + 1))  # نطاق الأحرف العربية في Unicode
        
        for char in text:
            if ord(char) in arabic_chars:
                return True
        
        return False
    
    @staticmethod
    def get_text_direction(text):
        """تحديد اتجاه النص"""
        if ArabicSupport.is_arabic_text(text):
            return "rtl"  # من اليمين لليسار
        else:
            return "ltr"  # من اليسار لليمين
