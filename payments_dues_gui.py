#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
شاشة المدفوعات والمستحقات - Payments & Dues Screen
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

class PaymentsDuesGUI:
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
        
        # جدول الموردين/العملاء/الموظفين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_type TEXT NOT NULL, -- supplier, customer, employee
                contact_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول فواتير الشراء
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                supplier_id INTEGER,
                invoice_date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                paid_amount DECIMAL(10,2) DEFAULT 0,
                payment_status TEXT DEFAULT 'unpaid', -- paid, unpaid, partial
                due_date DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES accounts (id)
            )
        ''')
        
        # جدول فواتير البيع الآجلة
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                invoice_date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                paid_amount DECIMAL(10,2) DEFAULT 0,
                payment_status TEXT DEFAULT 'unpaid',
                due_date DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES accounts (id)
            )
        ''')
        
        # جدول الرواتب
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payrolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                salary_month TEXT NOT NULL, -- YYYY-MM format
                basic_salary DECIMAL(10,2) NOT NULL,
                allowances DECIMAL(10,2) DEFAULT 0,
                deductions DECIMAL(10,2) DEFAULT 0,
                net_salary DECIMAL(10,2) NOT NULL,
                paid_amount DECIMAL(10,2) DEFAULT 0,
                payment_status TEXT DEFAULT 'unpaid',
                payment_date DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES accounts (id)
            )
        ''')
        
        # جدول المدفوعات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_number TEXT UNIQUE NOT NULL,
                transaction_type TEXT NOT NULL, -- purchase, sale, payroll, expense
                transaction_id INTEGER NOT NULL,
                payment_amount DECIMAL(10,2) NOT NULL,
                payment_method TEXT NOT NULL, -- MADA, VISA, BANK, CASH, etc.
                payment_date DATE NOT NULL,
                reference_number TEXT,
                notes TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        
        # حسابات تجريبية
        accounts = [
            ('شركة الأغذية المتحدة', 'supplier', '0501234567'),
            ('مؤسسة التوريدات الحديثة', 'supplier', '0509876543'),
            ('أحمد محمد السعيد', 'customer', '0551234567'),
            ('شركة الأطعمة المتميزة', 'customer', '0559876543'),
            ('محمد أحمد علي', 'employee', '0561234567'),
            ('فاطمة سعد الزهراني', 'employee', '0569876543'),
            ('خالد عبدالله النجار', 'employee', '0571234567')
        ]
        
        for account in accounts:
            self.cursor.execute('''
                INSERT OR IGNORE INTO accounts (name, account_type, contact_info)
                VALUES (?, ?, ?)
            ''', account)
        
        # فواتير شراء تجريبية
        purchases = [
            ('PUR-2025-001', 1, '2025-08-01', 15750.00, 10000.00, 'partial', '2025-08-15'),
            ('PUR-2025-002', 2, '2025-08-02', 22300.00, 0.00, 'unpaid', '2025-08-16'),
            ('PUR-2025-003', 1, '2025-08-03', 8900.00, 8900.00, 'paid', '2025-08-17')
        ]
        
        for purchase in purchases:
            self.cursor.execute('''
                INSERT OR IGNORE INTO purchases 
                (invoice_number, supplier_id, invoice_date, total_amount, paid_amount, payment_status, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', purchase)
        
        # فواتير بيع آجلة تجريبية
        sales = [
            ('SAL-2025-001', 3, '2025-08-01', 12500.00, 5000.00, 'partial', '2025-08-20'),
            ('SAL-2025-002', 4, '2025-08-02', 18750.00, 0.00, 'unpaid', '2025-08-22')
        ]
        
        for sale in sales:
            self.cursor.execute('''
                INSERT OR IGNORE INTO sales 
                (invoice_number, customer_id, invoice_date, total_amount, paid_amount, payment_status, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sale)
        
        # رواتب تجريبية
        payrolls = [
            (5, '2025-08', 8000.00, 1000.00, 500.00, 8500.00, 0.00, 'unpaid'),
            (6, '2025-08', 7500.00, 800.00, 300.00, 8000.00, 8000.00, 'paid'),
            (7, '2025-08', 9000.00, 1200.00, 600.00, 9600.00, 4800.00, 'partial')
        ]
        
        for payroll in payrolls:
            self.cursor.execute('''
                INSERT OR IGNORE INTO payrolls 
                (employee_id, salary_month, basic_salary, allowances, deductions, net_salary, paid_amount, payment_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', payroll)
        
        self.conn.commit()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("شاشة المدفوعات والمستحقات - Payments & Dues")
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
        self.create_filter_section()
        self.create_table_section()
        self.create_payment_section()
        self.create_summary_section()
        
    def create_filter_section(self):
        """قسم الفلترة"""
        filter_frame = ttk.LabelFrame(self.scrollable_frame, text="فلترة البيانات - Data Filters", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # الصف الأول - نوع الحساب
        row1 = ttk.Frame(filter_frame)
        row1.pack(fill="x", pady=2)
        
        ttk.Label(row1, text="نوع الحساب / Account Type:", font=self.arabic_font).pack(side="right", padx=5)
        self.account_type_var = tk.StringVar()
        account_types = ["all", "suppliers", "customers", "employees"]
        type_labels = {
            "all": "الكل / All",
            "suppliers": "الموردين / Suppliers", 
            "customers": "العملاء / Customers",
            "employees": "الموظفين / Employees"
        }
        self.account_type_combo = ttk.Combobox(row1, textvariable=self.account_type_var, 
                                             values=list(type_labels.values()), width=20, state="readonly")
        self.account_type_combo.pack(side="right", padx=5)
        self.account_type_combo.set("الكل / All")
        
        # حالة الدفع
        ttk.Label(row1, text="حالة الدفع / Payment Status:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_status_filter_var = tk.StringVar()
        status_options = ["all", "paid", "unpaid", "partial"]
        status_labels = {
            "all": "الكل / All",
            "paid": "مدفوع / Paid",
            "unpaid": "غير مدفوع / Unpaid", 
            "partial": "مدفوع جزئياً / Partial"
        }
        self.payment_status_filter_combo = ttk.Combobox(row1, textvariable=self.payment_status_filter_var,
                                                       values=list(status_labels.values()), width=15, state="readonly")
        self.payment_status_filter_combo.pack(side="right", padx=5)
        self.payment_status_filter_combo.set("الكل / All")
        
        # الصف الثاني - التواريخ
        row2 = ttk.Frame(filter_frame)
        row2.pack(fill="x", pady=2)
        
        ttk.Label(row2, text="من تاريخ / From Date:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_date_from = tk.StringVar()
        ttk.Entry(row2, textvariable=self.filter_date_from, width=12).pack(side="right", padx=5)
        
        ttk.Label(row2, text="إلى تاريخ / To Date:", font=self.arabic_font).pack(side="right", padx=5)
        self.filter_date_to = tk.StringVar()
        ttk.Entry(row2, textvariable=self.filter_date_to, width=12).pack(side="right", padx=5)
        
        # زر التطبيق
        ttk.Button(filter_frame, text="تطبيق الفلتر / Apply Filter", command=self.apply_filter).pack(pady=5)
        
    def create_table_section(self):
        """قسم جدول المعاملات"""
        table_frame = ttk.LabelFrame(self.scrollable_frame, text="جدول المعاملات - Transactions Table", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # إنشاء Treeview
        columns = ("ID", "رقم الفاتورة", "النوع", "الاسم", "التاريخ", "القيمة الإجمالية", "المدفوع", "المتبقي", "الحالة")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # تعريف العناوين
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor="center")
            elif col in ["القيمة الإجمالية", "المدفوع", "المتبقي"]:
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=120, anchor="center")
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.tree.bind("<Double-1>", self.record_payment)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_payment_section(self):
        """قسم تسجيل الدفعات"""
        payment_frame = ttk.LabelFrame(self.scrollable_frame, text="تسجيل دفعة - Record Payment", padding=10)
        payment_frame.pack(fill="x", padx=10, pady=5)

        # الصف الأول
        row1 = ttk.Frame(payment_frame)
        row1.pack(fill="x", pady=2)

        ttk.Label(row1, text="المبلغ المدفوع / Payment Amount:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_amount_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.payment_amount_var, width=15).pack(side="right", padx=5)

        ttk.Label(row1, text="طريقة الدفع / Payment Method:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_method_var = tk.StringVar()
        payment_methods = ["CASH", "MADA", "VISA", "MASTERCARD", "BANK", "GGC", "AKS"]
        self.payment_method_combo = ttk.Combobox(row1, textvariable=self.payment_method_var,
                                               values=payment_methods, width=12, state="readonly")
        self.payment_method_combo.pack(side="right", padx=5)

        # الصف الثاني
        row2 = ttk.Frame(payment_frame)
        row2.pack(fill="x", pady=2)

        ttk.Label(row2, text="تاريخ الدفع / Payment Date:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_date_var = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        ttk.Entry(row2, textvariable=self.payment_date_var, width=12).pack(side="right", padx=5)

        ttk.Label(row2, text="رقم المرجع / Reference:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_reference_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.payment_reference_var, width=20).pack(side="right", padx=5)

        # الصف الثالث - الملاحظات
        row3 = ttk.Frame(payment_frame)
        row3.pack(fill="x", pady=2)

        ttk.Label(row3, text="ملاحظات / Notes:", font=self.arabic_font).pack(side="right", padx=5)
        self.payment_notes_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.payment_notes_var, width=50).pack(side="right", padx=5)

        # أزرار العمليات
        buttons_frame = ttk.Frame(payment_frame)
        buttons_frame.pack(fill="x", pady=10)

        ttk.Button(buttons_frame, text="تسجيل الدفعة / Record Payment", command=self.save_payment).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="مسح / Clear", command=self.clear_payment_form).pack(side="right", padx=5)

    def create_summary_section(self):
        """قسم الملخص"""
        summary_frame = ttk.LabelFrame(self.scrollable_frame, text="ملخص المدفوعات والمستحقات - Summary", padding=10)
        summary_frame.pack(fill="x", padx=10, pady=5)

        # متغيرات الملخص
        self.total_amount_var = tk.StringVar(value="0.00")
        self.total_paid_var = tk.StringVar(value="0.00")
        self.total_due_var = tk.StringVar(value="0.00")
        self.unpaid_count_var = tk.StringVar(value="0")

        # عرض الملخص في شبكة
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(fill="x")

        # الصف الأول
        row1 = ttk.Frame(summary_grid)
        row1.pack(fill="x", pady=2)

        ttk.Label(row1, text="إجمالي المبالغ:", font=self.arabic_font, foreground="blue").pack(side="right", padx=10)
        ttk.Label(row1, textvariable=self.total_amount_var, font=self.arabic_font, foreground="blue").pack(side="right", padx=5)

        ttk.Label(row1, text="إجمالي المدفوع:", font=self.arabic_font, foreground="green").pack(side="right", padx=10)
        ttk.Label(row1, textvariable=self.total_paid_var, font=self.arabic_font, foreground="green").pack(side="right", padx=5)

        # الصف الثاني
        row2 = ttk.Frame(summary_grid)
        row2.pack(fill="x", pady=2)

        ttk.Label(row2, text="إجمالي المستحق:", font=self.arabic_font, foreground="red").pack(side="right", padx=10)
        ttk.Label(row2, textvariable=self.total_due_var, font=self.arabic_font, foreground="red").pack(side="right", padx=5)

        ttk.Label(row2, text="عدد العمليات غير المدفوعة:", font=self.arabic_font, foreground="orange").pack(side="right", padx=10)
        ttk.Label(row2, textvariable=self.unpaid_count_var, font=self.arabic_font, foreground="orange").pack(side="right", padx=5)

    # ==================== وظائف المساعدة ====================

    def load_data(self):
        """تحميل البيانات في الجدول"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)

        # تحميل فواتير الشراء
        self.cursor.execute('''
            SELECT p.id, p.invoice_number, 'شراء' as type, a.name, p.invoice_date,
                   p.total_amount, p.paid_amount, (p.total_amount - p.paid_amount) as remaining,
                   p.payment_status, 'purchase' as source_table
            FROM purchases p
            LEFT JOIN accounts a ON p.supplier_id = a.id
        ''')
        purchases = self.cursor.fetchall()

        # تحميل فواتير البيع الآجلة
        self.cursor.execute('''
            SELECT s.id, s.invoice_number, 'بيع آجل' as type, a.name, s.invoice_date,
                   s.total_amount, s.paid_amount, (s.total_amount - s.paid_amount) as remaining,
                   s.payment_status, 'sales' as source_table
            FROM sales s
            LEFT JOIN accounts a ON s.customer_id = a.id
        ''')
        sales = self.cursor.fetchall()

        # تحميل الرواتب
        self.cursor.execute('''
            SELECT pr.id, pr.salary_month as invoice_number, 'راتب' as type, a.name,
                   pr.salary_month || '-01' as invoice_date,
                   pr.net_salary, pr.paid_amount, (pr.net_salary - pr.paid_amount) as remaining,
                   pr.payment_status, 'payrolls' as source_table
            FROM payrolls pr
            LEFT JOIN accounts a ON pr.employee_id = a.id
        ''')
        payrolls = self.cursor.fetchall()

        # دمج جميع البيانات
        all_transactions = purchases + sales + payrolls

        # إدراج البيانات في الجدول
        for transaction in all_transactions:
            # تنسيق حالة الدفع
            status_map = {
                'paid': 'مدفوع',
                'unpaid': 'غير مدفوع',
                'partial': 'مدفوع جزئياً'
            }
            status_display = status_map.get(transaction[8], transaction[8])

            # تنسيق المبالغ
            total_display = f"{transaction[5]:,.2f} ريال"
            paid_display = f"{transaction[6]:,.2f} ريال"
            remaining_display = f"{transaction[7]:,.2f} ريال"

            # تحديد لون الصف حسب الحالة
            tags = []
            if transaction[8] == 'unpaid':
                tags = ['unpaid']
            elif transaction[8] == 'partial':
                tags = ['partial']
            elif transaction[8] == 'paid':
                tags = ['paid']

            self.tree.insert("", "end", values=(
                f"{transaction[9]}_{transaction[0]}",  # ID مع نوع الجدول
                transaction[1],  # رقم الفاتورة
                transaction[2],  # النوع
                transaction[3] or 'غير محدد',  # الاسم
                transaction[4],  # التاريخ
                total_display,   # القيمة الإجمالية
                paid_display,    # المدفوع
                remaining_display,  # المتبقي
                status_display   # الحالة
            ), tags=tags)

        # تطبيق الألوان
        self.tree.tag_configure('unpaid', background='#ffebee')
        self.tree.tag_configure('partial', background='#fff3e0')
        self.tree.tag_configure('paid', background='#e8f5e8')

        self.update_summary()

    def apply_filter(self):
        """تطبيق الفلتر"""
        # مسح الجدول
        for item in self.tree.get_children():
            self.tree.delete(item)

        # تحديد نوع الحساب
        account_type_display = self.account_type_var.get()
        account_type_map = {
            "الكل / All": "all",
            "الموردين / Suppliers": "suppliers",
            "العملاء / Customers": "customers",
            "الموظفين / Employees": "employees"
        }
        account_type = account_type_map.get(account_type_display, "all")

        # تحديد حالة الدفع
        status_display = self.payment_status_filter_var.get()
        status_map = {
            "الكل / All": "all",
            "مدفوع / Paid": "paid",
            "غير مدفوع / Unpaid": "unpaid",
            "مدفوع جزئياً / Partial": "partial"
        }
        payment_status = status_map.get(status_display, "all")

        transactions = []

        # تحميل البيانات حسب الفلتر
        if account_type in ["all", "suppliers"]:
            query = '''
                SELECT p.id, p.invoice_number, 'شراء' as type, a.name, p.invoice_date,
                       p.total_amount, p.paid_amount, (p.total_amount - p.paid_amount) as remaining,
                       p.payment_status, 'purchase' as source_table
                FROM purchases p
                LEFT JOIN accounts a ON p.supplier_id = a.id
                WHERE 1=1
            '''
            params = []

            if payment_status != "all":
                query += " AND p.payment_status = ?"
                params.append(payment_status)

            if self.filter_date_from.get():
                query += " AND p.invoice_date >= ?"
                params.append(self.filter_date_from.get())

            if self.filter_date_to.get():
                query += " AND p.invoice_date <= ?"
                params.append(self.filter_date_to.get())

            self.cursor.execute(query, params)
            transactions.extend(self.cursor.fetchall())

        if account_type in ["all", "customers"]:
            query = '''
                SELECT s.id, s.invoice_number, 'بيع آجل' as type, a.name, s.invoice_date,
                       s.total_amount, s.paid_amount, (s.total_amount - s.paid_amount) as remaining,
                       s.payment_status, 'sales' as source_table
                FROM sales s
                LEFT JOIN accounts a ON s.customer_id = a.id
                WHERE 1=1
            '''
            params = []

            if payment_status != "all":
                query += " AND s.payment_status = ?"
                params.append(payment_status)

            if self.filter_date_from.get():
                query += " AND s.invoice_date >= ?"
                params.append(self.filter_date_from.get())

            if self.filter_date_to.get():
                query += " AND s.invoice_date <= ?"
                params.append(self.filter_date_to.get())

            self.cursor.execute(query, params)
            transactions.extend(self.cursor.fetchall())

        if account_type in ["all", "employees"]:
            query = '''
                SELECT pr.id, pr.salary_month as invoice_number, 'راتب' as type, a.name,
                       pr.salary_month || '-01' as invoice_date,
                       pr.net_salary, pr.paid_amount, (pr.net_salary - pr.paid_amount) as remaining,
                       pr.payment_status, 'payrolls' as source_table
                FROM payrolls pr
                LEFT JOIN accounts a ON pr.employee_id = a.id
                WHERE 1=1
            '''
            params = []

            if payment_status != "all":
                query += " AND pr.payment_status = ?"
                params.append(payment_status)

            self.cursor.execute(query, params)
            transactions.extend(self.cursor.fetchall())

        # إدراج البيانات المفلترة
        for transaction in transactions:
            status_map = {
                'paid': 'مدفوع',
                'unpaid': 'غير مدفوع',
                'partial': 'مدفوع جزئياً'
            }
            status_display = status_map.get(transaction[8], transaction[8])

            total_display = f"{transaction[5]:,.2f} ريال"
            paid_display = f"{transaction[6]:,.2f} ريال"
            remaining_display = f"{transaction[7]:,.2f} ريال"

            tags = []
            if transaction[8] == 'unpaid':
                tags = ['unpaid']
            elif transaction[8] == 'partial':
                tags = ['partial']
            elif transaction[8] == 'paid':
                tags = ['paid']

            self.tree.insert("", "end", values=(
                f"{transaction[9]}_{transaction[0]}",
                transaction[1], transaction[2], transaction[3] or 'غير محدد',
                transaction[4], total_display, paid_display, remaining_display, status_display
            ), tags=tags)

        self.update_summary()

    def record_payment(self, event):
        """تسجيل دفعة (عند النقر المزدوج)"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        # استخراج معلومات المعاملة
        transaction_id_full = values[0]  # مثل "purchase_1"
        source_table, transaction_id = transaction_id_full.split('_')

        # ملء نموذج الدفع بالمعلومات
        remaining_text = values[7]  # "1000.00 ريال"
        remaining_amount = float(remaining_text.replace(' ريال', '').replace(',', ''))

        self.payment_amount_var.set(str(remaining_amount))

        messagebox.showinfo("تسجيل دفعة / Record Payment",
                           f"تم تحديد المعاملة: {values[1]}\nالمبلغ المتبقي: {remaining_text}")

    def save_payment(self):
        """حفظ الدفعة"""
        try:
            # التحقق من وجود معاملة محددة
            selection = self.tree.selection()
            if not selection:
                messagebox.showerror("خطأ / Error", "يرجى تحديد معاملة أولاً / Please select a transaction first")
                return

            # التحقق من البيانات المطلوبة
            if not self.payment_amount_var.get().strip():
                messagebox.showerror("خطأ / Error", "يرجى إدخال مبلغ الدفعة / Please enter payment amount")
                return

            if not self.payment_method_var.get():
                messagebox.showerror("خطأ / Error", "يرجى اختيار طريقة الدفع / Please select payment method")
                return

            try:
                payment_amount = float(self.payment_amount_var.get())
                if payment_amount <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ / Error", "يرجى إدخال مبلغ صحيح / Please enter valid amount")
                return

            # استخراج معلومات المعاملة المحددة
            item = self.tree.item(selection[0])
            values = item['values']
            transaction_id_full = values[0]
            source_table, transaction_id = transaction_id_full.split('_')

            # التحقق من أن المبلغ لا يتجاوز المتبقي
            remaining_text = values[7].replace(' ريال', '').replace(',', '')
            remaining_amount = float(remaining_text)

            if payment_amount > remaining_amount:
                messagebox.showerror("خطأ / Error",
                                   f"المبلغ المدخل أكبر من المتبقي\nالمتبقي: {remaining_amount:,.2f} ريال")
                return

            # توليد رقم دفعة
            payment_number = self.generate_payment_number()

            # حفظ الدفعة
            self.cursor.execute('''
                INSERT INTO payments (
                    payment_number, transaction_type, transaction_id, payment_amount,
                    payment_method, payment_date, reference_number, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment_number,
                source_table,
                int(transaction_id),
                payment_amount,
                self.payment_method_var.get(),
                self.payment_date_var.get(),
                self.payment_reference_var.get(),
                self.payment_notes_var.get()
            ))

            # تحديث المعاملة الأصلية
            self.update_transaction_payment(source_table, int(transaction_id), payment_amount)

            self.conn.commit()
            messagebox.showinfo("نجح / Success",
                               f"تم تسجيل الدفعة بنجاح\nرقم الدفعة: {payment_number}")

            # مسح النموذج وتحديث البيانات
            self.clear_payment_form()
            self.load_data()

        except Exception as e:
            messagebox.showerror("خطأ / Error", f"حدث خطأ أثناء حفظ الدفعة / Error saving payment: {str(e)}")

    def generate_payment_number(self):
        """توليد رقم دفعة تلقائي"""
        today = datetime.date.today()
        prefix = f"PAY-{today.strftime('%Y%m%d')}"

        self.cursor.execute('''
            SELECT payment_number FROM payments
            WHERE payment_number LIKE ?
            ORDER BY payment_number DESC LIMIT 1
        ''', (f"{prefix}%",))

        result = self.cursor.fetchone()
        if result:
            last_number = int(result[0].split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:03d}"

    def update_transaction_payment(self, source_table, transaction_id, payment_amount):
        """تحديث المعاملة بالدفعة الجديدة"""
        if source_table == "purchase":
            # تحديث فاتورة الشراء
            self.cursor.execute('''
                UPDATE purchases
                SET paid_amount = paid_amount + ?,
                    payment_status = CASE
                        WHEN (paid_amount + ?) >= total_amount THEN 'paid'
                        WHEN (paid_amount + ?) > 0 THEN 'partial'
                        ELSE 'unpaid'
                    END
                WHERE id = ?
            ''', (payment_amount, payment_amount, payment_amount, transaction_id))

        elif source_table == "sales":
            # تحديث فاتورة البيع
            self.cursor.execute('''
                UPDATE sales
                SET paid_amount = paid_amount + ?,
                    payment_status = CASE
                        WHEN (paid_amount + ?) >= total_amount THEN 'paid'
                        WHEN (paid_amount + ?) > 0 THEN 'partial'
                        ELSE 'unpaid'
                    END
                WHERE id = ?
            ''', (payment_amount, payment_amount, payment_amount, transaction_id))

        elif source_table == "payrolls":
            # تحديث الراتب
            self.cursor.execute('''
                UPDATE payrolls
                SET paid_amount = paid_amount + ?,
                    payment_status = CASE
                        WHEN (paid_amount + ?) >= net_salary THEN 'paid'
                        WHEN (paid_amount + ?) > 0 THEN 'partial'
                        ELSE 'unpaid'
                    END,
                    payment_date = ?
                WHERE id = ?
            ''', (payment_amount, payment_amount, payment_amount, self.payment_date_var.get(), transaction_id))

    def clear_payment_form(self):
        """مسح نموذج الدفع"""
        self.payment_amount_var.set("")
        self.payment_method_var.set("")
        self.payment_date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
        self.payment_reference_var.set("")
        self.payment_notes_var.set("")

    def update_summary(self):
        """تحديث ملخص المدفوعات والمستحقات"""
        # حساب الإجماليات من جميع المصادر

        # فواتير الشراء
        self.cursor.execute('SELECT SUM(total_amount), SUM(paid_amount) FROM purchases')
        purchase_totals = self.cursor.fetchone()
        purchase_total = purchase_totals[0] or 0
        purchase_paid = purchase_totals[1] or 0

        # فواتير البيع
        self.cursor.execute('SELECT SUM(total_amount), SUM(paid_amount) FROM sales')
        sales_totals = self.cursor.fetchone()
        sales_total = sales_totals[0] or 0
        sales_paid = sales_totals[1] or 0

        # الرواتب
        self.cursor.execute('SELECT SUM(net_salary), SUM(paid_amount) FROM payrolls')
        payroll_totals = self.cursor.fetchone()
        payroll_total = payroll_totals[0] or 0
        payroll_paid = payroll_totals[1] or 0

        # الإجماليات
        total_amount = purchase_total + sales_total + payroll_total
        total_paid = purchase_paid + sales_paid + payroll_paid
        total_due = total_amount - total_paid

        # عدد العمليات غير المدفوعة
        self.cursor.execute('''
            SELECT
                (SELECT COUNT(*) FROM purchases WHERE payment_status IN ('unpaid', 'partial')) +
                (SELECT COUNT(*) FROM sales WHERE payment_status IN ('unpaid', 'partial')) +
                (SELECT COUNT(*) FROM payrolls WHERE payment_status IN ('unpaid', 'partial'))
        ''')
        unpaid_count = self.cursor.fetchone()[0] or 0

        # تحديث المتغيرات
        self.total_amount_var.set(f"{total_amount:,.2f} ريال")
        self.total_paid_var.set(f"{total_paid:,.2f} ريال")
        self.total_due_var.set(f"{total_due:,.2f} ريال")
        self.unpaid_count_var.set(str(unpaid_count))

    def show_context_menu(self, event):
        """عرض قائمة السياق"""
        selection = self.tree.selection()
        if not selection:
            return

        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="تسجيل دفعة / Record Payment", command=lambda: self.record_payment(event))
        context_menu.add_command(label="عرض تفاصيل / View Details", command=self.view_transaction_details)
        context_menu.add_command(label="عرض سجل الدفعات / View Payment History", command=self.view_payment_history)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def view_transaction_details(self):
        """عرض تفاصيل المعاملة"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        details_window = tk.Toplevel(self.root)
        details_window.title("تفاصيل المعاملة / Transaction Details")
        details_window.geometry("500x400")

        # عرض التفاصيل
        details_text = tk.Text(details_window, wrap=tk.WORD, font=self.arabic_font)
        details_text.pack(fill="both", expand=True, padx=10, pady=10)

        details_content = f"""
تفاصيل المعاملة / Transaction Details
=====================================

رقم الفاتورة / Invoice Number: {values[1]}
النوع / Type: {values[2]}
الاسم / Name: {values[3]}
التاريخ / Date: {values[4]}
القيمة الإجمالية / Total Amount: {values[5]}
المدفوع / Paid Amount: {values[6]}
المتبقي / Remaining: {values[7]}
الحالة / Status: {values[8]}
        """

        details_text.insert(tk.END, details_content)
        details_text.config(state=tk.DISABLED)

    def view_payment_history(self):
        """عرض سجل الدفعات للمعاملة"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']
        transaction_id_full = values[0]
        source_table, transaction_id = transaction_id_full.split('_')

        # استعلام سجل الدفعات
        self.cursor.execute('''
            SELECT payment_number, payment_amount, payment_method, payment_date, reference_number, notes
            FROM payments
            WHERE transaction_type = ? AND transaction_id = ?
            ORDER BY payment_date DESC
        ''', (source_table, int(transaction_id)))

        payments = self.cursor.fetchall()

        # إنشاء نافذة السجل
        history_window = tk.Toplevel(self.root)
        history_window.title("سجل الدفعات / Payment History")
        history_window.geometry("800x400")

        if not payments:
            ttk.Label(history_window, text="لا توجد دفعات مسجلة / No payments recorded",
                     font=self.arabic_font).pack(pady=50)
            return

        # إنشاء جدول السجل
        columns = ("رقم الدفعة", "المبلغ", "طريقة الدفع", "التاريخ", "المرجع", "الملاحظات")
        history_tree = ttk.Treeview(history_window, columns=columns, show="headings")

        for col in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=120, anchor="center")

        # إدراج البيانات
        for payment in payments:
            history_tree.insert("", "end", values=(
                payment[0],  # رقم الدفعة
                f"{payment[1]:,.2f} ريال",  # المبلغ
                payment[2],  # طريقة الدفع
                payment[3],  # التاريخ
                payment[4] or '-',  # المرجع
                payment[5] or '-'   # الملاحظات
            ))

        history_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def export_to_excel(self):
        """تصدير إلى Excel"""
        try:
            # جمع البيانات من جميع المصادر
            all_data = []

            # فواتير الشراء
            self.cursor.execute('''
                SELECT p.invoice_number, 'شراء' as type, a.name, p.invoice_date,
                       p.total_amount, p.paid_amount, (p.total_amount - p.paid_amount) as remaining,
                       p.payment_status
                FROM purchases p
                LEFT JOIN accounts a ON p.supplier_id = a.id
            ''')
            all_data.extend(self.cursor.fetchall())

            # فواتير البيع
            self.cursor.execute('''
                SELECT s.invoice_number, 'بيع آجل' as type, a.name, s.invoice_date,
                       s.total_amount, s.paid_amount, (s.total_amount - s.paid_amount) as remaining,
                       s.payment_status
                FROM sales s
                LEFT JOIN accounts a ON s.customer_id = a.id
            ''')
            all_data.extend(self.cursor.fetchall())

            # الرواتب
            self.cursor.execute('''
                SELECT pr.salary_month, 'راتب' as type, a.name, pr.salary_month || '-01',
                       pr.net_salary, pr.paid_amount, (pr.net_salary - pr.paid_amount) as remaining,
                       pr.payment_status
                FROM payrolls pr
                LEFT JOIN accounts a ON pr.employee_id = a.id
            ''')
            all_data.extend(self.cursor.fetchall())

            # إنشاء DataFrame
            df = pd.DataFrame(all_data, columns=[
                'رقم الفاتورة', 'النوع', 'الاسم', 'التاريخ',
                'القيمة الإجمالية', 'المدفوع', 'المتبقي', 'الحالة'
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
                c.drawString(50, height - 50, "Payments & Dues Report - تقرير المدفوعات والمستحقات")

                # التاريخ
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 80, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

                # الملخص
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, height - 120, "Summary / الملخص:")

                c.setFont("Helvetica", 10)
                c.drawString(50, height - 140, f"Total Amount: {self.total_amount_var.get()}")
                c.drawString(50, height - 155, f"Total Paid: {self.total_paid_var.get()}")
                c.drawString(50, height - 170, f"Total Due: {self.total_due_var.get()}")
                c.drawString(50, height - 185, f"Unpaid Transactions: {self.unpaid_count_var.get()}")

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
    app = PaymentsDuesGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
