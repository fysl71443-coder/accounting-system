#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
شاشة المصروفات المتقدمة - Advanced Expenses Screen
نظام محاسبي احترافي مع دعم اللغة العربية والإنجليزية
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
import sqlite3
import datetime
import json
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import arabic_reshaper
from bidi.algorithm import get_display

class AdvancedExpensesGUI:
    def __init__(self, root):
        self.root = root
        self.language = "ar"  # Default to Arabic
        self.setup_database()
        self.setup_ui()
        self.load_data()
        
    def setup_database(self):
        """إعداد قاعدة البيانات"""
        self.conn = sqlite3.connect('accounting_system.db')
        self.cursor = self.conn.cursor()
        
        # إنشاء الجداول المطلوبة
        self.create_tables()
        self.insert_sample_data()
        
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول فئات المصروفات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_ar TEXT NOT NULL,
                name_en TEXT NOT NULL,
                parent_id INTEGER,
                category_type TEXT DEFAULT 'operational',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموردين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المصروفات الرئيسي
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_number TEXT UNIQUE NOT NULL,
                expense_date DATE NOT NULL,
                category_id INTEGER,
                description TEXT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                currency TEXT DEFAULT 'SAR',
                vendor_id INTEGER,
                payment_method TEXT,
                payment_status TEXT DEFAULT 'unpaid',
                partial_amount DECIMAL(10,2) DEFAULT 0,
                attachment_path TEXT,
                notes TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES expense_categories (id),
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            )
        ''')
        
        # جدول المرفقات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER,
                file_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (expense_id) REFERENCES expenses (id)
            )
        ''')
        
        self.conn.commit()
        
    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        
        # فئات المصروفات
        categories = [
            ('رواتب', 'Salaries', None, 'operational'),
            ('إيجار', 'Rent', None, 'operational'),
            ('كهرباء', 'Electricity', None, 'operational'),
            ('صيانة', 'Maintenance', None, 'operational'),
            ('تسويق', 'Marketing', None, 'administrative'),
            ('مشتريات غير مخزنية', 'Non-inventory Purchases', None, 'operational'),
            ('مواصلات', 'Transportation', None, 'operational'),
            ('اتصالات', 'Communications', None, 'administrative'),
            ('قرطاسية', 'Stationery', None, 'administrative'),
            ('تأمين', 'Insurance', None, 'administrative')
        ]
        
        for cat in categories:
            self.cursor.execute('''
                INSERT OR IGNORE INTO expense_categories (name_ar, name_en, parent_id, category_type)
                VALUES (?, ?, ?, ?)
            ''', cat)
        
        # موردين تجريبيين
        vendors = [
            ('شركة الكهرباء السعودية',),
            ('شركة المياه الوطنية',),
            ('مؤسسة النقل والمواصلات',),
            ('شركة الصيانة المتخصصة',),
            ('مكتب الإعلان والتسويق',)
        ]
        
        for vendor in vendors:
            self.cursor.execute('''
                INSERT OR IGNORE INTO vendors (name) VALUES (?)
            ''', vendor)
        
        self.conn.commit()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("شاشة المصروفات المتقدمة - Advanced Expenses")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # إعداد الخطوط
        self.arabic_font = Font(family="Arial Unicode MS", size=10)
        self.english_font = Font(family="Arial", size=10)
        
        # إنشاء القوائم الرئيسية
        self.create_menu()
        self.create_main_frame()
        
    def create_menu(self):
        """إنشاء شريط القوائم"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة اللغة
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language / اللغة", menu=language_menu)
        language_menu.add_command(label="العربية", command=lambda: self.change_language("ar"))
        language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File / ملف", menu=file_menu)
        file_menu.add_command(label="Export to Excel / تصدير إلى Excel", command=self.export_to_excel)
        file_menu.add_command(label="Export to PDF / تصدير إلى PDF", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit / خروج", command=self.root.quit)
        
    def create_main_frame(self):
        """إنشاء الإطار الرئيسي"""
        # إطار رئيسي مع تمرير
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # إنشاء الأقسام
        self.create_input_section()
        self.create_filter_section()
        self.create_table_section()
        self.create_summary_section()
        self.create_charts_section()
        
    def create_input_section(self):
        """قسم إدخال المصروفات"""
        input_frame = ttk.LabelFrame(self.scrollable_frame, text="إدخال مصروف جديد - New Expense Entry", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # الصف الأول
        row1 = ttk.Frame(input_frame)
        row1.pack(fill="x", pady=2)
        
        # رقم العملية
        ttk.Label(row1, text="رقم العملية / Operation No:", font=self.arabic_font).pack(side="right", padx=5)
        self.expense_number_var = tk.StringVar(value=self.generate_expense_number())
        ttk.Entry(row1, textvariable=self.expense_number_var, state="readonly", width=15).pack(side="right", padx=5)
        
        # التاريخ
        ttk.Label(row1, text="التاريخ / Date:", font=self.arabic_font).pack(side="right", padx=5)
        self.date_var = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        ttk.Entry(row1, textvariable=self.date_var, width=12).pack(side="right", padx=5)
        
        # الصف الثاني
        row2 = ttk.Frame(input_frame)
        row2.pack(fill="x", pady=2)
        
        # نوع المصروف
        ttk.Label(row2, text="نوع المصروف / Expense Type:", font=self.arabic_font).pack(side="right", padx=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(row2, textvariable=self.category_var, width=20, state="readonly")
        self.category_combo.pack(side="right", padx=5)
        self.load_categories()
        
        # المبلغ
        ttk.Label(row2, text="المبلغ / Amount:", font=self.arabic_font).pack(side="right", padx=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.amount_var, width=15).pack(side="right", padx=5)
        
        # الصف الثالث
        row3 = ttk.Frame(input_frame)
        row3.pack(fill="x", pady=2)
        
        # الوصف
        ttk.Label(row3, text="الوصف / Description:", font=self.arabic_font).pack(side="right", padx=5)
        self.description_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.description_var, width=40).pack(side="right", padx=5)
        
        # الصف الرابع
        row4 = ttk.Frame(input_frame)
        row4.pack(fill="x", pady=2)
        
        # الجهة المستفيدة
        ttk.Label(row4, text="الجهة المستفيدة / Vendor:", font=self.arabic_font).pack(side="right", padx=5)
        self.vendor_var = tk.StringVar()
        self.vendor_combo = ttk.Combobox(row4, textvariable=self.vendor_var, width=20)
        self.vendor_combo.pack(side="right", padx=5)
        self.load_vendors()
        
        # طريقة الدفع
        ttk.Label(row4, text="طريقة الدفع / Payment Method:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_method_var = tk.StringVar()
        payment_methods = ["CASH", "MADA", "VISA", "MASTERCARD", "BANK", "GGC", "AKS"]
        self.payment_method_combo = ttk.Combobox(row4, textvariable=self.payment_method_var, values=payment_methods, width=12, state="readonly")
        self.payment_method_combo.pack(side="right", padx=5)
        
        # الصف الخامس
        row5 = ttk.Frame(input_frame)
        row5.pack(fill="x", pady=2)
        
        # حالة الدفع
        ttk.Label(row5, text="حالة الدفع / Payment Status:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_status_var = tk.StringVar()
        payment_statuses = ["unpaid", "paid", "partial"]
        status_labels = {"unpaid": "غير مدفوع", "paid": "مدفوع", "partial": "مدفوع جزئياً"}
        self.payment_status_combo = ttk.Combobox(row5, textvariable=self.payment_status_var, values=payment_statuses, width=12, state="readonly")
        self.payment_status_combo.pack(side="right", padx=5)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(buttons_frame, text="حفظ / Save", command=self.save_expense).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="مسح / Clear", command=self.clear_form).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="إرفاق ملف / Attach File", command=self.attach_file).pack(side="right", padx=5)
        
    def create_filter_section(self):
        """قسم الفلترة"""
        filter_frame = ttk.LabelFrame(self.scrollable_frame, text="فلترة المصروفات - Filter Expenses", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # فلاتر التاريخ
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(fill="x", pady=2)
        
        ttk.Label(date_frame, text="من تاريخ / From:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_date_from = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.filter_date_from, width=12).pack(side="right", padx=5)
        
        ttk.Label(date_frame, text="إلى تاريخ / To:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_date_to = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.filter_date_to, width=12).pack(side="right", padx=5)
        
        # فلاتر أخرى
        other_filters = ttk.Frame(filter_frame)
        other_filters.pack(fill="x", pady=2)
        
        ttk.Label(other_filters, text="نوع المصروف / Category:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(other_filters, textvariable=self.filter_category_var, width=20)
        self.filter_category_combo.pack(side="right", padx=5)
        
        ttk.Label(other_filters, text="حالة الدفع / Status:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_status_var = tk.StringVar()
        self.filter_status_combo = ttk.Combobox(other_filters, textvariable=self.filter_status_var, values=["all", "paid", "unpaid", "partial"], width=12)
        self.filter_status_combo.pack(side="right", padx=5)
        
        # زر التطبيق
        ttk.Button(filter_frame, text="تطبيق الفلتر / Apply Filter", command=self.apply_filter).pack(pady=5)
        
    def create_table_section(self):
        """قسم جدول المصروفات"""
        table_frame = ttk.LabelFrame(self.scrollable_frame, text="جدول المصروفات - Expenses Table", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # إنشاء Treeview
        columns = ("ID", "رقم العملية", "التاريخ", "النوع", "الوصف", "المبلغ", "طريقة الدفع", "الحالة", "الجهة")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # تعريف العناوين
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.tree.bind("<Double-1>", self.edit_expense)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
    def create_summary_section(self):
        """قسم الملخص"""
        summary_frame = ttk.LabelFrame(self.scrollable_frame, text="ملخص المصروفات - Expenses Summary", padding=10)
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        # متغيرات الملخص
        self.total_expenses_var = tk.StringVar(value="0.00")
        self.total_paid_var = tk.StringVar(value="0.00")
        self.total_unpaid_var = tk.StringVar(value="0.00")
        
        # عرض الملخص
        summary_row = ttk.Frame(summary_frame)
        summary_row.pack(fill="x")
        
        ttk.Label(summary_row, text="إجمالي المصروفات:", font=self.arabic_font).pack(side="right", padx=10)
        ttk.Label(summary_row, textvariable=self.total_expenses_var, font=self.arabic_font, foreground="blue").pack(side="right", padx=5)
        
        ttk.Label(summary_row, text="المدفوع:", font=self.arabic_font).pack(side="right", padx=10)
        ttk.Label(summary_row, textvariable=self.total_paid_var, font=self.arabic_font, foreground="green").pack(side="right", padx=5)
        
        ttk.Label(summary_row, text="المستحق:", font=self.arabic_font).pack(side="right", padx=10)
        ttk.Label(summary_row, textvariable=self.total_unpaid_var, font=self.arabic_font, foreground="red").pack(side="right", padx=5)
        
    def create_charts_section(self):
        """قسم الرسوم البيانية"""
        charts_frame = ttk.LabelFrame(self.scrollable_frame, text="التحليلات والرسوم البيانية - Analytics & Charts", padding=10)
        charts_frame.pack(fill="x", padx=10, pady=5)
        
        # أزرار الرسوم البيانية
        charts_buttons = ttk.Frame(charts_frame)
        charts_buttons.pack(fill="x", pady=5)
        
        ttk.Button(charts_buttons, text="رسم دائري للأنواع / Pie Chart by Type", command=self.show_pie_chart).pack(side="right", padx=5)
        ttk.Button(charts_buttons, text="رسم شريطي شهري / Monthly Bar Chart", command=self.show_bar_chart).pack(side="right", padx=5)
        ttk.Button(charts_buttons, text="أعلى 5 أنواع / Top 5 Categories", command=self.show_top_categories).pack(side="right", padx=5)

    # ==================== وظائف المساعدة ====================

    def generate_expense_number(self):
        """توليد رقم عملية تلقائي"""
        today = datetime.date.today()
        prefix = f"EXP-{today.strftime('%Y%m%d')}"

        # البحث عن آخر رقم في نفس اليوم
        self.cursor.execute('''
            SELECT expense_number FROM expenses
            WHERE expense_number LIKE ?
            ORDER BY expense_number DESC LIMIT 1
        ''', (f"{prefix}%",))

        result = self.cursor.fetchone()
        if result:
            last_number = int(result[0].split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:03d}"

    def load_categories(self):
        """تحميل فئات المصروفات"""
        self.cursor.execute('SELECT id, name_ar, name_en FROM expense_categories ORDER BY name_ar')
        categories = self.cursor.fetchall()

        category_values = []
        self.category_dict = {}

        for cat_id, name_ar, name_en in categories:
            if self.language == "ar":
                display_name = name_ar
            else:
                display_name = name_en
            category_values.append(display_name)
            self.category_dict[display_name] = cat_id

        self.category_combo['values'] = category_values
        if self.filter_category_combo:
            self.filter_category_combo['values'] = ["الكل / All"] + category_values

    def load_vendors(self):
        """تحميل الموردين"""
        self.cursor.execute('SELECT id, name FROM vendors ORDER BY name')
        vendors = self.cursor.fetchall()

        vendor_values = [vendor[1] for vendor in vendors]
        self.vendor_dict = {vendor[1]: vendor[0] for vendor in vendors}

        self.vendor_combo['values'] = vendor_values

    def save_expense(self):
        """حفظ المصروف"""
        try:
            # التحقق من البيانات المطلوبة
            if not self.description_var.get().strip():
                messagebox.showerror("خطأ / Error", "يرجى إدخال وصف المصروف / Please enter expense description")
                return

            if not self.amount_var.get().strip():
                messagebox.showerror("خطأ / Error", "يرجى إدخال المبلغ / Please enter amount")
                return

            try:
                amount = float(self.amount_var.get())
                if amount <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ / Error", "يرجى إدخال مبلغ صحيح / Please enter valid amount")
                return

            # الحصول على معرف الفئة
            category_name = self.category_var.get()
            category_id = self.category_dict.get(category_name)

            # الحصول على معرف المورد
            vendor_name = self.vendor_var.get()
            vendor_id = self.vendor_dict.get(vendor_name) if vendor_name else None

            # إدراج المصروف
            self.cursor.execute('''
                INSERT INTO expenses (
                    expense_number, expense_date, category_id, description,
                    amount, vendor_id, payment_method, payment_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.expense_number_var.get(),
                self.date_var.get(),
                category_id,
                self.description_var.get(),
                amount,
                vendor_id,
                self.payment_method_var.get(),
                self.payment_status_var.get() or 'unpaid'
            ))

            self.conn.commit()
            messagebox.showinfo("نجح / Success", "تم حفظ المصروف بنجاح / Expense saved successfully")

            # مسح النموذج وتحديث البيانات
            self.clear_form()
            self.load_data()
            self.update_summary()

        except Exception as e:
            messagebox.showerror("خطأ / Error", f"حدث خطأ أثناء الحفظ / Error saving: {str(e)}")

    def clear_form(self):
        """مسح النموذج"""
        self.expense_number_var.set(self.generate_expense_number())
        self.date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
        self.category_var.set("")
        self.description_var.set("")
        self.amount_var.set("")
        self.vendor_var.set("")
        self.payment_method_var.set("")
        self.payment_status_var.set("")

    def attach_file(self):
        """إرفاق ملف"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف / Select File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            messagebox.showinfo("نجح / Success", f"تم إرفاق الملف / File attached: {os.path.basename(file_path)}")

    def load_data(self):
        """تحميل البيانات في الجدول"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)

        # استعلام البيانات
        query = '''
            SELECT e.id, e.expense_number, e.expense_date,
                   COALESCE(c.name_ar, 'غير محدد') as category_name,
                   e.description, e.amount, e.payment_method, e.payment_status,
                   COALESCE(v.name, 'غير محدد') as vendor_name
            FROM expenses e
            LEFT JOIN expense_categories c ON e.category_id = c.id
            LEFT JOIN vendors v ON e.vendor_id = v.id
            ORDER BY e.expense_date DESC, e.id DESC
        '''

        self.cursor.execute(query)
        expenses = self.cursor.fetchall()

        # إدراج البيانات في الجدول
        for expense in expenses:
            # تنسيق حالة الدفع
            status_map = {
                'paid': 'مدفوع',
                'unpaid': 'غير مدفوع',
                'partial': 'مدفوع جزئياً'
            }
            status_display = status_map.get(expense[7], expense[7])

            # تنسيق المبلغ
            amount_display = f"{expense[5]:,.2f} ريال"

            self.tree.insert("", "end", values=(
                expense[0],  # ID
                expense[1],  # رقم العملية
                expense[2],  # التاريخ
                expense[3],  # النوع
                expense[4],  # الوصف
                amount_display,  # المبلغ
                expense[6] or 'غير محدد',  # طريقة الدفع
                status_display,  # الحالة
                expense[8]   # الجهة
            ))

    def apply_filter(self):
        """تطبيق الفلتر"""
        # بناء الاستعلام مع الفلاتر
        query = '''
            SELECT e.id, e.expense_number, e.expense_date,
                   COALESCE(c.name_ar, 'غير محدد') as category_name,
                   e.description, e.amount, e.payment_method, e.payment_status,
                   COALESCE(v.name, 'غير محدد') as vendor_name
            FROM expenses e
            LEFT JOIN expense_categories c ON e.category_id = c.id
            LEFT JOIN vendors v ON e.vendor_id = v.id
            WHERE 1=1
        '''

        params = []

        # فلتر التاريخ
        if self.filter_date_from.get():
            query += " AND e.expense_date >= ?"
            params.append(self.filter_date_from.get())

        if self.filter_date_to.get():
            query += " AND e.expense_date <= ?"
            params.append(self.filter_date_to.get())

        # فلتر الفئة
        filter_category = self.filter_category_var.get()
        if filter_category and filter_category != "الكل / All":
            category_id = self.category_dict.get(filter_category)
            if category_id:
                query += " AND e.category_id = ?"
                params.append(category_id)

        # فلتر الحالة
        filter_status = self.filter_status_var.get()
        if filter_status and filter_status != "all":
            query += " AND e.payment_status = ?"
            params.append(filter_status)

        query += " ORDER BY e.expense_date DESC, e.id DESC"

        # تنفيذ الاستعلام
        self.cursor.execute(query, params)
        expenses = self.cursor.fetchall()

        # مسح الجدول وإعادة تعبئته
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in expenses:
            status_map = {
                'paid': 'مدفوع',
                'unpaid': 'غير مدفوع',
                'partial': 'مدفوع جزئياً'
            }
            status_display = status_map.get(expense[7], expense[7])
            amount_display = f"{expense[5]:,.2f} ريال"

            self.tree.insert("", "end", values=(
                expense[0], expense[1], expense[2], expense[3],
                expense[4], amount_display, expense[6] or 'غير محدد',
                status_display, expense[8]
            ))

        self.update_summary()

    def update_summary(self):
        """تحديث ملخص المصروفات"""
        # حساب الإجماليات
        self.cursor.execute('SELECT SUM(amount) FROM expenses')
        total = self.cursor.fetchone()[0] or 0

        self.cursor.execute('SELECT SUM(amount) FROM expenses WHERE payment_status = "paid"')
        paid = self.cursor.fetchone()[0] or 0

        self.cursor.execute('SELECT SUM(amount) FROM expenses WHERE payment_status = "unpaid"')
        unpaid = self.cursor.fetchone()[0] or 0

        # تحديث المتغيرات
        self.total_expenses_var.set(f"{total:,.2f} ريال")
        self.total_paid_var.set(f"{paid:,.2f} ريال")
        self.total_unpaid_var.set(f"{unpaid:,.2f} ريال")

    def edit_expense(self, event):
        """تعديل المصروف"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        expense_id = item['values'][0]

        # استرجاع بيانات المصروف
        self.cursor.execute('''
            SELECT expense_number, expense_date, category_id, description,
                   amount, vendor_id, payment_method, payment_status
            FROM expenses WHERE id = ?
        ''', (expense_id,))

        expense = self.cursor.fetchone()
        if expense:
            # ملء النموذج بالبيانات
            self.expense_number_var.set(expense[0])
            self.date_var.set(expense[1])
            self.description_var.set(expense[3])
            self.amount_var.set(str(expense[4]))
            self.payment_method_var.set(expense[6] or "")
            self.payment_status_var.set(expense[7] or "unpaid")

            # تحديد الفئة
            if expense[2]:
                self.cursor.execute('SELECT name_ar FROM expense_categories WHERE id = ?', (expense[2],))
                cat_result = self.cursor.fetchone()
                if cat_result:
                    self.category_var.set(cat_result[0])

            # تحديد المورد
            if expense[5]:
                self.cursor.execute('SELECT name FROM vendors WHERE id = ?', (expense[5],))
                vendor_result = self.cursor.fetchone()
                if vendor_result:
                    self.vendor_var.set(vendor_result[0])

    def show_context_menu(self, event):
        """عرض قائمة السياق"""
        selection = self.tree.selection()
        if not selection:
            return

        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="تعديل / Edit", command=lambda: self.edit_expense(event))
        context_menu.add_command(label="حذف / Delete", command=self.delete_expense)
        context_menu.add_command(label="عرض المرفقات / View Attachments", command=self.view_attachments)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def delete_expense(self):
        """حذف المصروف"""
        selection = self.tree.selection()
        if not selection:
            return

        if messagebox.askyesno("تأكيد الحذف / Confirm Delete",
                              "هل أنت متأكد من حذف هذا المصروف؟ / Are you sure you want to delete this expense?"):
            item = self.tree.item(selection[0])
            expense_id = item['values'][0]

            self.cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            self.conn.commit()

            self.load_data()
            self.update_summary()
            messagebox.showinfo("نجح / Success", "تم حذف المصروف / Expense deleted")

    def view_attachments(self):
        """عرض المرفقات"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        expense_id = item['values'][0]

        # البحث عن المرفقات
        self.cursor.execute('SELECT file_path, file_name FROM attachments WHERE expense_id = ?', (expense_id,))
        attachments = self.cursor.fetchall()

        if attachments:
            attachment_window = tk.Toplevel(self.root)
            attachment_window.title("المرفقات / Attachments")
            attachment_window.geometry("400x300")

            for attachment in attachments:
                ttk.Label(attachment_window, text=attachment[1]).pack(pady=5)
        else:
            messagebox.showinfo("المرفقات / Attachments", "لا توجد مرفقات / No attachments found")

    def show_pie_chart(self):
        """عرض الرسم الدائري للأنواع"""
        # استعلام البيانات
        self.cursor.execute('''
            SELECT c.name_ar, SUM(e.amount) as total
            FROM expenses e
            LEFT JOIN expense_categories c ON e.category_id = c.id
            GROUP BY e.category_id, c.name_ar
            HAVING total > 0
            ORDER BY total DESC
        ''')

        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("تنبيه / Warning", "لا توجد بيانات لعرضها / No data to display")
            return

        # إنشاء الرسم البياني
        categories = [item[0] or 'غير محدد' for item in data]
        amounts = [item[1] for item in data]

        plt.figure(figsize=(10, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('توزيع المصروفات حسب النوع / Expenses Distribution by Type', fontsize=14)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def show_bar_chart(self):
        """عرض الرسم الشريطي الشهري"""
        # استعلام البيانات الشهرية
        self.cursor.execute('''
            SELECT strftime('%Y-%m', expense_date) as month, SUM(amount) as total
            FROM expenses
            GROUP BY strftime('%Y-%m', expense_date)
            ORDER BY month
        ''')

        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("تنبيه / Warning", "لا توجد بيانات لعرضها / No data to display")
            return

        months = [item[0] for item in data]
        amounts = [item[1] for item in data]

        plt.figure(figsize=(12, 6))
        plt.bar(months, amounts, color='skyblue', edgecolor='navy', alpha=0.7)
        plt.title('المصروفات الشهرية / Monthly Expenses', fontsize=14)
        plt.xlabel('الشهر / Month')
        plt.ylabel('المبلغ (ريال) / Amount (SAR)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def show_top_categories(self):
        """عرض أعلى 5 فئات"""
        self.cursor.execute('''
            SELECT c.name_ar, SUM(e.amount) as total, COUNT(e.id) as count
            FROM expenses e
            LEFT JOIN expense_categories c ON e.category_id = c.id
            GROUP BY e.category_id, c.name_ar
            ORDER BY total DESC
            LIMIT 5
        ''')

        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("تنبيه / Warning", "لا توجد بيانات لعرضها / No data to display")
            return

        # إنشاء نافذة جديدة
        top_window = tk.Toplevel(self.root)
        top_window.title("أعلى 5 فئات مصروفات / Top 5 Expense Categories")
        top_window.geometry("600x400")

        # إنشاء جدول
        columns = ("الترتيب", "الفئة", "المبلغ الإجمالي", "عدد العمليات")
        tree = ttk.Treeview(top_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # إدراج البيانات
        for i, (category, total, count) in enumerate(data, 1):
            tree.insert("", "end", values=(
                i,
                category or 'غير محدد',
                f"{total:,.2f} ريال",
                count
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def export_to_excel(self):
        """تصدير إلى Excel"""
        try:
            # استعلام البيانات
            self.cursor.execute('''
                SELECT e.expense_number, e.expense_date, c.name_ar as category,
                       e.description, e.amount, e.payment_method, e.payment_status,
                       v.name as vendor
                FROM expenses e
                LEFT JOIN expense_categories c ON e.category_id = c.id
                LEFT JOIN vendors v ON e.vendor_id = v.id
                ORDER BY e.expense_date DESC
            ''')

            data = self.cursor.fetchall()

            # إنشاء DataFrame
            df = pd.DataFrame(data, columns=[
                'رقم العملية', 'التاريخ', 'الفئة', 'الوصف',
                'المبلغ', 'طريقة الدفع', 'حالة الدفع', 'الجهة'
            ])

            # حفظ الملف
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )

            if filename:
                df.to_excel(filename, index=False, engine='openpyxl')
                messagebox.showinfo("نجح / Success", f"تم التصدير بنجاح / Exported successfully to: {filename}")

        except Exception as e:
            messagebox.showerror("خطأ / Error", f"خطأ في التصدير / Export error: {str(e)}")

    def export_to_pdf(self):
        """تصدير إلى PDF"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )

            if filename:
                # إنشاء ملف PDF
                c = canvas.Canvas(filename, pagesize=A4)
                width, height = A4

                # العنوان
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "Expenses Report - تقرير المصروفات")

                # التاريخ
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 80, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

                # البيانات
                y_position = height - 120
                c.setFont("Helvetica", 8)

                # العناوين
                headers = ["Date", "Category", "Description", "Amount", "Status"]
                x_positions = [50, 120, 200, 350, 450]

                for i, header in enumerate(headers):
                    c.drawString(x_positions[i], y_position, header)

                y_position -= 20

                # البيانات
                self.cursor.execute('''
                    SELECT e.expense_date, c.name_en, e.description, e.amount, e.payment_status
                    FROM expenses e
                    LEFT JOIN expense_categories c ON e.category_id = c.id
                    ORDER BY e.expense_date DESC
                    LIMIT 50
                ''')

                expenses = self.cursor.fetchall()

                for expense in expenses:
                    if y_position < 50:  # صفحة جديدة
                        c.showPage()
                        y_position = height - 50

                    for i, value in enumerate(expense):
                        text = str(value) if value else ""
                        if i == 3:  # المبلغ
                            text = f"{float(value):,.2f}" if value else "0.00"
                        c.drawString(x_positions[i], y_position, text[:20])  # تحديد طول النص

                    y_position -= 15

                c.save()
                messagebox.showinfo("نجح / Success", f"تم التصدير بنجاح / Exported successfully to: {filename}")

        except Exception as e:
            messagebox.showerror("خطأ / Error", f"خطأ في التصدير / Export error: {str(e)}")

    def change_language(self, lang):
        """تغيير اللغة"""
        self.language = lang
        messagebox.showinfo("اللغة / Language",
                           f"تم تغيير اللغة إلى {lang} / Language changed to {lang}\nيرجى إعادة تشغيل البرنامج / Please restart the application")


def main():
    """الوظيفة الرئيسية"""
    root = tk.Tk()
    app = AdvancedExpensesGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
