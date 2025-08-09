#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار التطبيقات - Applications Test Runner
اختبار سريع لجميع التطبيقات المطورة
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import sqlite3

def test_database_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    try:
        # اختبار قاعدة بيانات المحاسبة
        conn1 = sqlite3.connect('accounting_system.db')
        cursor1 = conn1.cursor()
        cursor1.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table"')
        tables_count1 = cursor1.fetchone()[0]
        conn1.close()
        
        # اختبار قاعدة بيانات المطاعم
        conn2 = sqlite3.connect('restaurant_costing.db')
        cursor2 = conn2.cursor()
        cursor2.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table"')
        tables_count2 = cursor2.fetchone()[0]
        conn2.close()
        
        return True, f"قواعد البيانات متصلة بنجاح\nجداول المحاسبة: {tables_count1}\nجداول المطاعم: {tables_count2}"
    except Exception as e:
        return False, f"خطأ في الاتصال بقاعدة البيانات: {str(e)}"

def test_imports():
    """اختبار استيراد المكتبات المطلوبة"""
    required_modules = [
        'tkinter',
        'sqlite3',
        'datetime',
        'json',
        'os',
        'PIL',
        'matplotlib',
        'pandas',
        'reportlab'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        return False, f"المكتبات المفقودة: {', '.join(missing_modules)}"
    else:
        return True, "جميع المكتبات متوفرة"

def test_files_exist():
    """اختبار وجود الملفات المطلوبة"""
    required_files = [
        'advanced_expenses_gui.py',
        'payments_dues_gui.py',
        'costing_screen_gui.py',
        'main_launcher.py',
        'expenses_requirements.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        return False, f"الملفات المفقودة: {', '.join(missing_files)}"
    else:
        return True, "جميع الملفات موجودة"

def run_quick_test():
    """تشغيل اختبار سريع"""
    results = []
    
    # اختبار الملفات
    files_ok, files_msg = test_files_exist()
    results.append(("وجود الملفات", files_ok, files_msg))
    
    # اختبار المكتبات
    imports_ok, imports_msg = test_imports()
    results.append(("المكتبات المطلوبة", imports_ok, imports_msg))
    
    # اختبار قاعدة البيانات
    db_ok, db_msg = test_database_connection()
    results.append(("قاعدة البيانات", db_ok, db_msg))
    
    return results

class TestRunner:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة الاختبار"""
        self.root.title("اختبار التطبيقات - Applications Test Runner")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # العنوان
        title_label = tk.Label(self.root, 
                              text="اختبار نظام المحاسبة الاحترافي\nProfessional Accounting System Test",
                              font=("Arial Unicode MS", 14, "bold"),
                              bg='#f0f0f0',
                              fg='#2c3e50')
        title_label.pack(pady=20)
        
        # إطار النتائج
        results_frame = ttk.LabelFrame(self.root, text="نتائج الاختبار - Test Results", padding=10)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # منطقة النص
        self.results_text = tk.Text(results_frame, 
                                   font=("Arial Unicode MS", 10),
                                   wrap=tk.WORD,
                                   height=15)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # أزرار العمليات
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(buttons_frame, 
                 text="تشغيل الاختبار السريع\nRun Quick Test",
                 command=self.run_tests,
                 bg='#3498db',
                 fg='white',
                 font=("Arial Unicode MS", 10),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        tk.Button(buttons_frame,
                 text="اختبار المصروفات\nTest Expenses App",
                 command=self.test_expenses_app,
                 bg='#e74c3c',
                 fg='white',
                 font=("Arial Unicode MS", 10),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        tk.Button(buttons_frame,
                 text="اختبار المدفوعات\nTest Payments App",
                 command=self.test_payments_app,
                 bg='#27ae60',
                 fg='white',
                 font=("Arial Unicode MS", 10),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        tk.Button(buttons_frame,
                 text="اختبار التكلفة\nTest Costing App",
                 command=self.test_costing_app,
                 bg='#f39c12',
                 fg='white',
                 font=("Arial Unicode MS", 10),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        # تشغيل الاختبار تلقائياً
        self.root.after(1000, self.run_tests)
        
    def run_tests(self):
        """تشغيل جميع الاختبارات"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "بدء الاختبارات...\nStarting tests...\n\n")
        self.root.update()
        
        results = run_quick_test()
        
        for test_name, success, message in results:
            status = "✅ نجح" if success else "❌ فشل"
            self.results_text.insert(tk.END, f"{status} {test_name}:\n{message}\n\n")
            self.root.update()
        
        # ملخص النتائج
        passed = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        if passed == total:
            summary = f"🎉 جميع الاختبارات نجحت ({passed}/{total})\n✅ النظام جاهز للاستخدام"
            self.results_text.insert(tk.END, f"\n{summary}\n")
        else:
            summary = f"⚠️ بعض الاختبارات فشلت ({passed}/{total})\n❌ يرجى إصلاح المشاكل قبل الاستخدام"
            self.results_text.insert(tk.END, f"\n{summary}\n")
    
    def test_expenses_app(self):
        """اختبار تطبيق المصروفات"""
        try:
            self.results_text.insert(tk.END, "\n🔄 اختبار تطبيق المصروفات...\n")
            self.root.update()
            
            # محاولة استيراد التطبيق
            import advanced_expenses_gui
            self.results_text.insert(tk.END, "✅ تم استيراد تطبيق المصروفات بنجاح\n")
            
            # اختبار إنشاء النافذة
            test_root = tk.Toplevel()
            test_root.withdraw()  # إخفاء النافذة
            app = advanced_expenses_gui.AdvancedExpensesGUI(test_root)
            test_root.destroy()
            
            self.results_text.insert(tk.END, "✅ تم إنشاء واجهة المصروفات بنجاح\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ خطأ في اختبار المصروفات: {str(e)}\n")
    
    def test_payments_app(self):
        """اختبار تطبيق المدفوعات"""
        try:
            self.results_text.insert(tk.END, "\n🔄 اختبار تطبيق المدفوعات...\n")
            self.root.update()
            
            # محاولة استيراد التطبيق
            import payments_dues_gui
            self.results_text.insert(tk.END, "✅ تم استيراد تطبيق المدفوعات بنجاح\n")
            
            # اختبار إنشاء النافذة
            test_root = tk.Toplevel()
            test_root.withdraw()  # إخفاء النافذة
            app = payments_dues_gui.PaymentsDuesGUI(test_root)
            test_root.destroy()
            
            self.results_text.insert(tk.END, "✅ تم إنشاء واجهة المدفوعات بنجاح\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ خطأ في اختبار المدفوعات: {str(e)}\n")
    
    def test_costing_app(self):
        """اختبار تطبيق التكلفة"""
        try:
            self.results_text.insert(tk.END, "\n🔄 اختبار تطبيق التكلفة...\n")
            self.root.update()
            
            # محاولة استيراد التطبيق
            import costing_screen_gui
            self.results_text.insert(tk.END, "✅ تم استيراد تطبيق التكلفة بنجاح\n")
            
            # اختبار إنشاء النافذة
            test_root = tk.Toplevel()
            test_root.withdraw()  # إخفاء النافذة
            app = costing_screen_gui.CostingScreenGUI(test_root)
            test_root.destroy()
            
            self.results_text.insert(tk.END, "✅ تم إنشاء واجهة التكلفة بنجاح\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ خطأ في اختبار التكلفة: {str(e)}\n")

def main():
    """الوظيفة الرئيسية"""
    root = tk.Tk()
    app = TestRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
