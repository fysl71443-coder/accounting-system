#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
شاشة حساب التكلفة للمطاعم - Restaurant Costing Screen
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
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

class CostingScreenGUI:
    def __init__(self, root):
        self.root = root
        self.language = "ar"  # Default to Arabic
        self.setup_database()
        self.setup_ui()
        self.load_data()
        
    def setup_database(self):
        """إعداد قاعدة البيانات"""
        self.conn = sqlite3.connect('restaurant_costing.db')
        self.cursor = self.conn.cursor()
        
        # إنشاء الجداول المطلوبة
        self.create_tables()
        self.insert_sample_data()
        
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول الوجبات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                servings INTEGER DEFAULT 1,
                total_cost DECIMAL(10,3) DEFAULT 0,
                cost_per_serving DECIMAL(10,3) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المواد الخام
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                unit TEXT NOT NULL, -- جم، لتر، قطعة، كيلو
                unit_price DECIMAL(10,3) NOT NULL,
                stock_quantity DECIMAL(10,3) DEFAULT 0,
                min_stock DECIMAL(10,3) DEFAULT 0,
                supplier TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول مكونات الوجبات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS meal_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id INTEGER,
                ingredient_id INTEGER,
                quantity_used DECIMAL(10,3) NOT NULL,
                unit_cost DECIMAL(10,3) NOT NULL,
                total_cost DECIMAL(10,3) NOT NULL,
                percentage DECIMAL(5,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (meal_id) REFERENCES meals (id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
            )
        ''')
        
        self.conn.commit()
        
    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        
        # مواد خام تجريبية
        ingredients = [
            ('دجاج', 'كيلو', 25.00, 50.0, 10.0, 'مؤسسة اللحوم'),
            ('أرز بسمتي', 'كيلو', 8.50, 100.0, 20.0, 'شركة الحبوب'),
            ('بصل', 'كيلو', 3.00, 30.0, 5.0, 'سوق الخضار'),
            ('طماطم', 'كيلو', 4.50, 25.0, 5.0, 'سوق الخضار'),
            ('زيت طبخ', 'لتر', 12.00, 20.0, 3.0, 'شركة الزيوت'),
            ('ملح', 'كيلو', 2.00, 10.0, 2.0, 'البقالة'),
            ('فلفل أسود', 'جم', 0.05, 500.0, 100.0, 'محل البهارات'),
            ('كمون', 'جم', 0.08, 300.0, 50.0, 'محل البهارات'),
            ('هيل', 'جم', 0.15, 200.0, 30.0, 'محل البهارات'),
            ('جزر', 'كيلو', 3.50, 20.0, 5.0, 'سوق الخضار'),
            ('بازلاء', 'كيلو', 6.00, 15.0, 3.0, 'سوق الخضار'),
            ('زبدة', 'كيلو', 18.00, 10.0, 2.0, 'منتجات الألبان')
        ]
        
        for ingredient in ingredients:
            self.cursor.execute('''
                INSERT OR IGNORE INTO ingredients (name, unit, unit_price, stock_quantity, min_stock, supplier)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ingredient)
        
        # وجبات تجريبية
        meals = [
            ('كبسة دجاج', 'كبسة دجاج بالخضار والبهارات', 4),
            ('مندي لحم', 'مندي لحم مع الأرز البسمتي', 6),
            ('برياني دجاج', 'برياني دجاج بالبهارات الهندية', 5)
        ]
        
        for meal in meals:
            self.cursor.execute('''
                INSERT OR IGNORE INTO meals (name, description, servings)
                VALUES (?, ?, ?)
            ''', meal)
        
        self.conn.commit()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("شاشة حساب التكلفة للمطاعم - Restaurant Costing Screen")
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
        
        # قائمة البيانات
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data / البيانات", menu=data_menu)
        data_menu.add_command(label="إدارة المواد الخام / Manage Ingredients", command=self.manage_ingredients)
        data_menu.add_command(label="تحديث الأسعار / Update Prices", command=self.update_prices)
        
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
        self.create_meal_selection_section()
        self.create_ingredients_section()
        self.create_cost_calculation_section()
        self.create_saved_meals_section()
        
    def create_meal_selection_section(self):
        """قسم اختيار الوجبة"""
        meal_frame = ttk.LabelFrame(self.scrollable_frame, text="اختيار الوجبة - Meal Selection", padding=10)
        meal_frame.pack(fill="x", padx=10, pady=5)
        
        # الصف الأول
        row1 = ttk.Frame(meal_frame)
        row1.pack(fill="x", pady=2)
        
        # اختيار الوجبة
        ttk.Label(row1, text="اختر الوجبة / Select Meal:", font=self.arabic_font).pack(side="right", padx=5)
        self.meal_var = tk.StringVar()
        self.meal_combo = ttk.Combobox(row1, textvariable=self.meal_var, width=30, state="readonly")
        self.meal_combo.pack(side="right", padx=5)
        self.meal_combo.bind('<<ComboboxSelected>>', self.on_meal_selected)
        
        # زر وجبة جديدة
        ttk.Button(row1, text="وجبة جديدة / New Meal", command=self.new_meal).pack(side="right", padx=5)
        
        # الصف الثاني
        row2 = ttk.Frame(meal_frame)
        row2.pack(fill="x", pady=2)
        
        # عدد الحصص
        ttk.Label(row2, text="عدد الحصص / Servings:", font=self.arabic_font).pack(side="right", padx=5)
        self.servings_var = tk.StringVar(value="1")
        servings_spinbox = tk.Spinbox(row2, from_=1, to=20, textvariable=self.servings_var, width=10)
        servings_spinbox.pack(side="right", padx=5)
        servings_spinbox.bind('<KeyRelease>', self.calculate_costs)
        servings_spinbox.bind('<ButtonRelease-1>', self.calculate_costs)
        
    def create_ingredients_section(self):
        """قسم المكونات"""
        ingredients_frame = ttk.LabelFrame(self.scrollable_frame, text="مكونات الوجبة - Meal Ingredients", padding=10)
        ingredients_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(ingredients_frame)
        buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(buttons_frame, text="إضافة مكون / Add Ingredient", command=self.add_ingredient).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="حذف المحدد / Remove Selected", command=self.remove_ingredient).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="تحديث الأسعار / Update Prices", command=self.update_ingredient_prices).pack(side="right", padx=5)
        
        # جدول المكونات
        columns = ("المكون", "الوحدة", "الكمية المستخدمة", "سعر الوحدة", "التكلفة الجزئية", "النسبة %")
        self.ingredients_tree = ttk.Treeview(ingredients_frame, columns=columns, show="headings", height=8)
        
        # تعريف العناوين
        for col in columns:
            self.ingredients_tree.heading(col, text=col)
            if col == "المكون":
                self.ingredients_tree.column(col, width=150, anchor="center")
            elif col == "النسبة %":
                self.ingredients_tree.column(col, width=80, anchor="center")
            else:
                self.ingredients_tree.column(col, width=120, anchor="center")
        
        # شريط التمرير للجدول
        ingredients_scroll = ttk.Scrollbar(ingredients_frame, orient="vertical", command=self.ingredients_tree.yview)
        self.ingredients_tree.configure(yscrollcommand=ingredients_scroll.set)
        
        self.ingredients_tree.pack(side="left", fill="both", expand=True)
        ingredients_scroll.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.ingredients_tree.bind("<Double-1>", self.edit_ingredient)
        
    def create_cost_calculation_section(self):
        """قسم حساب التكلفة"""
        cost_frame = ttk.LabelFrame(self.scrollable_frame, text="حساب التكلفة - Cost Calculation", padding=10)
        cost_frame.pack(fill="x", padx=10, pady=5)
        
        # متغيرات التكلفة
        self.total_cost_var = tk.StringVar(value="0.000")
        self.cost_per_serving_var = tk.StringVar(value="0.000")
        self.profit_margin_var = tk.StringVar(value="30")
        self.suggested_price_var = tk.StringVar(value="0.000")
        
        # الصف الأول - التكاليف
        row1 = ttk.Frame(cost_frame)
        row1.pack(fill="x", pady=5)
        
        # إجمالي التكلفة
        cost_label_frame = ttk.LabelFrame(row1, text="إجمالي التكلفة / Total Cost", padding=5)
        cost_label_frame.pack(side="right", padx=10, fill="x", expand=True)
        
        cost_display = ttk.Label(cost_label_frame, textvariable=self.total_cost_var, 
                                font=("Arial", 14, "bold"), foreground="blue")
        cost_display.pack()
        ttk.Label(cost_label_frame, text="ريال سعودي / SAR", font=self.arabic_font).pack()
        
        # تكلفة الحصة الواحدة
        serving_label_frame = ttk.LabelFrame(row1, text="تكلفة الحصة / Cost per Serving", padding=5)
        serving_label_frame.pack(side="right", padx=10, fill="x", expand=True)
        
        serving_display = ttk.Label(serving_label_frame, textvariable=self.cost_per_serving_var,
                                   font=("Arial", 14, "bold"), foreground="green")
        serving_display.pack()
        ttk.Label(serving_label_frame, text="ريال سعودي / SAR", font=self.arabic_font).pack()
        
        # الصف الثاني - هامش الربح والسعر المقترح
        row2 = ttk.Frame(cost_frame)
        row2.pack(fill="x", pady=5)
        
        # هامش الربح
        profit_frame = ttk.LabelFrame(row2, text="هامش الربح / Profit Margin", padding=5)
        profit_frame.pack(side="right", padx=10, fill="x", expand=True)
        
        profit_spinbox = tk.Spinbox(profit_frame, from_=0, to=200, textvariable=self.profit_margin_var, 
                                   width=10, font=("Arial", 12))
        profit_spinbox.pack()
        profit_spinbox.bind('<KeyRelease>', self.calculate_suggested_price)
        profit_spinbox.bind('<ButtonRelease-1>', self.calculate_suggested_price)
        ttk.Label(profit_frame, text="% نسبة مئوية", font=self.arabic_font).pack()
        
        # السعر المقترح
        price_label_frame = ttk.LabelFrame(row2, text="السعر المقترح / Suggested Price", padding=5)
        price_label_frame.pack(side="right", padx=10, fill="x", expand=True)
        
        price_display = ttk.Label(price_label_frame, textvariable=self.suggested_price_var,
                                 font=("Arial", 14, "bold"), foreground="red")
        price_display.pack()
        ttk.Label(price_label_frame, text="ريال سعودي / SAR", font=self.arabic_font).pack()
        
        # أزرار العمليات
        buttons_row = ttk.Frame(cost_frame)
        buttons_row.pack(fill="x", pady=10)
        
        ttk.Button(buttons_row, text="حفظ التكاليف / Save Costs", command=self.save_meal_costs).pack(side="right", padx=5)
        ttk.Button(buttons_row, text="إعادة حساب / Recalculate", command=self.calculate_costs).pack(side="right", padx=5)
        ttk.Button(buttons_row, text="مسح / Clear", command=self.clear_meal).pack(side="right", padx=5)
        
    def create_saved_meals_section(self):
        """قسم الوجبات المحفوظة"""
        saved_frame = ttk.LabelFrame(self.scrollable_frame, text="الوجبات المحفوظة - Saved Meals", padding=10)
        saved_frame.pack(fill="x", padx=10, pady=5)
        
        # جدول الوجبات المحفوظة
        columns = ("اسم الوجبة", "عدد الحصص", "إجمالي التكلفة", "تكلفة الحصة", "آخر تحديث")
        self.saved_meals_tree = ttk.Treeview(saved_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.saved_meals_tree.heading(col, text=col)
            self.saved_meals_tree.column(col, width=150, anchor="center")
        
        # شريط التمرير
        saved_scroll = ttk.Scrollbar(saved_frame, orient="vertical", command=self.saved_meals_tree.yview)
        self.saved_meals_tree.configure(yscrollcommand=saved_scroll.set)
        
        self.saved_meals_tree.pack(side="left", fill="both", expand=True)
        saved_scroll.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.saved_meals_tree.bind("<Double-1>", self.load_saved_meal)

    # ==================== وظائف المساعدة ====================

    def load_data(self):
        """تحميل البيانات الأولية"""
        self.load_meals()
        self.load_saved_meals()

    def load_meals(self):
        """تحميل قائمة الوجبات"""
        self.cursor.execute('SELECT id, name FROM meals ORDER BY name')
        meals = self.cursor.fetchall()

        meal_values = ["وجبة جديدة / New Meal"]
        self.meal_dict = {"وجبة جديدة / New Meal": None}

        for meal_id, name in meals:
            meal_values.append(name)
            self.meal_dict[name] = meal_id

        self.meal_combo['values'] = meal_values
        self.meal_combo.set("وجبة جديدة / New Meal")

    def load_saved_meals(self):
        """تحميل الوجبات المحفوظة"""
        # مسح البيانات الحالية
        for item in self.saved_meals_tree.get_children():
            self.saved_meals_tree.delete(item)

        # استعلام الوجبات
        self.cursor.execute('''
            SELECT name, servings, total_cost, cost_per_serving, updated_at
            FROM meals
            WHERE total_cost > 0
            ORDER BY updated_at DESC
        ''')

        meals = self.cursor.fetchall()

        for meal in meals:
            self.saved_meals_tree.insert("", "end", values=(
                meal[0],  # اسم الوجبة
                meal[1],  # عدد الحصص
                f"{meal[2]:.3f} ريال",  # إجمالي التكلفة
                f"{meal[3]:.3f} ريال",  # تكلفة الحصة
                meal[4][:10] if meal[4] else ""  # آخر تحديث (التاريخ فقط)
            ))

    def on_meal_selected(self, event):
        """عند اختيار وجبة"""
        meal_name = self.meal_var.get()
        meal_id = self.meal_dict.get(meal_name)

        if meal_id:
            self.load_meal_ingredients(meal_id)
        else:
            # وجبة جديدة - مسح المكونات
            for item in self.ingredients_tree.get_children():
                self.ingredients_tree.delete(item)
            self.calculate_costs()

    def load_meal_ingredients(self, meal_id):
        """تحميل مكونات الوجبة"""
        # مسح المكونات الحالية
        for item in self.ingredients_tree.get_children():
            self.ingredients_tree.delete(item)

        # استعلام مكونات الوجبة
        self.cursor.execute('''
            SELECT mi.id, i.name, i.unit, mi.quantity_used, mi.unit_cost, mi.total_cost, mi.percentage
            FROM meal_ingredients mi
            JOIN ingredients i ON mi.ingredient_id = i.id
            WHERE mi.meal_id = ?
            ORDER BY i.name
        ''', (meal_id,))

        ingredients = self.cursor.fetchall()

        for ingredient in ingredients:
            self.ingredients_tree.insert("", "end", values=(
                ingredient[1],  # اسم المكون
                ingredient[2],  # الوحدة
                f"{ingredient[3]:.3f}",  # الكمية المستخدمة
                f"{ingredient[4]:.3f}",  # سعر الوحدة
                f"{ingredient[5]:.3f}",  # التكلفة الجزئية
                f"{ingredient[6]:.1f}%"  # النسبة
            ))

        # تحميل عدد الحصص
        self.cursor.execute('SELECT servings FROM meals WHERE id = ?', (meal_id,))
        servings = self.cursor.fetchone()
        if servings:
            self.servings_var.set(str(servings[0]))

        self.calculate_costs()

    def new_meal(self):
        """إنشاء وجبة جديدة"""
        # نافذة إدخال اسم الوجبة
        dialog = tk.Toplevel(self.root)
        dialog.title("وجبة جديدة / New Meal")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # متغيرات الإدخال
        meal_name_var = tk.StringVar()
        meal_desc_var = tk.StringVar()

        # عناصر النافذة
        ttk.Label(dialog, text="اسم الوجبة / Meal Name:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=meal_name_var, width=40, font=self.arabic_font).pack(pady=5)

        ttk.Label(dialog, text="الوصف / Description:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=meal_desc_var, width=40, font=self.arabic_font).pack(pady=5)

        def save_new_meal():
            name = meal_name_var.get().strip()
            if not name:
                messagebox.showerror("خطأ / Error", "يرجى إدخال اسم الوجبة / Please enter meal name")
                return

            # إدراج الوجبة الجديدة
            self.cursor.execute('''
                INSERT INTO meals (name, description, servings)
                VALUES (?, ?, ?)
            ''', (name, meal_desc_var.get().strip(), 1))

            self.conn.commit()

            # تحديث قائمة الوجبات
            self.load_meals()
            self.meal_combo.set(name)

            dialog.destroy()
            messagebox.showinfo("نجح / Success", "تم إنشاء الوجبة الجديدة / New meal created successfully")

        # أزرار النافذة
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="حفظ / Save", command=save_new_meal).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="إلغاء / Cancel", command=dialog.destroy).pack(side="right", padx=5)

    def add_ingredient(self):
        """إضافة مكون جديد"""
        # نافذة اختيار المكون
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة مكون / Add Ingredient")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # متغيرات الإدخال
        ingredient_var = tk.StringVar()
        quantity_var = tk.StringVar()

        # تحميل المكونات المتاحة
        self.cursor.execute('SELECT id, name, unit, unit_price FROM ingredients ORDER BY name')
        available_ingredients = self.cursor.fetchall()

        ingredient_dict = {}
        ingredient_values = []

        for ing_id, name, unit, price in available_ingredients:
            display_name = f"{name} ({unit}) - {price:.3f} ريال"
            ingredient_values.append(display_name)
            ingredient_dict[display_name] = (ing_id, name, unit, price)

        # عناصر النافذة
        ttk.Label(dialog, text="اختر المكون / Select Ingredient:", font=self.arabic_font).pack(pady=5)
        ingredient_combo = ttk.Combobox(dialog, textvariable=ingredient_var, values=ingredient_values,
                                       width=50, state="readonly")
        ingredient_combo.pack(pady=5)

        ttk.Label(dialog, text="الكمية المستخدمة / Quantity Used:", font=self.arabic_font).pack(pady=5)
        quantity_entry = ttk.Entry(dialog, textvariable=quantity_var, width=20)
        quantity_entry.pack(pady=5)

        def add_selected_ingredient():
            if not ingredient_var.get():
                messagebox.showerror("خطأ / Error", "يرجى اختيار مكون / Please select an ingredient")
                return

            try:
                quantity = float(quantity_var.get())
                if quantity <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ / Error", "يرجى إدخال كمية صحيحة / Please enter valid quantity")
                return

            # الحصول على معلومات المكون
            ing_id, name, unit, unit_price = ingredient_dict[ingredient_var.get()]

            # حساب التكلفة
            total_cost = quantity * unit_price

            # إضافة المكون للجدول
            self.ingredients_tree.insert("", "end", values=(
                name,
                unit,
                f"{quantity:.3f}",
                f"{unit_price:.3f}",
                f"{total_cost:.3f}",
                "0.0%"  # سيتم حساب النسبة لاحقاً
            ))

            dialog.destroy()
            self.calculate_costs()

        # أزرار النافذة
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="إضافة / Add", command=add_selected_ingredient).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="إلغاء / Cancel", command=dialog.destroy).pack(side="right", padx=5)

    def remove_ingredient(self):
        """حذف المكون المحدد"""
        selection = self.ingredients_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير / Warning", "يرجى تحديد مكون للحذف / Please select an ingredient to remove")
            return

        if messagebox.askyesno("تأكيد الحذف / Confirm Delete",
                              "هل أنت متأكد من حذف هذا المكون؟ / Are you sure you want to remove this ingredient?"):
            for item in selection:
                self.ingredients_tree.delete(item)
            self.calculate_costs()

    def edit_ingredient(self, event):
        """تعديل المكون (عند النقر المزدوج)"""
        selection = self.ingredients_tree.selection()
        if not selection:
            return

        item = self.ingredients_tree.item(selection[0])
        values = item['values']

        # نافذة التعديل
        dialog = tk.Toplevel(self.root)
        dialog.title("تعديل المكون / Edit Ingredient")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # متغيرات التعديل
        quantity_var = tk.StringVar(value=values[2])
        unit_price_var = tk.StringVar(value=values[3])

        # عناصر النافذة
        ttk.Label(dialog, text=f"المكون: {values[0]}", font=self.arabic_font).pack(pady=5)
        ttk.Label(dialog, text=f"الوحدة: {values[1]}", font=self.arabic_font).pack(pady=5)

        ttk.Label(dialog, text="الكمية المستخدمة / Quantity:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=quantity_var, width=20).pack(pady=5)

        ttk.Label(dialog, text="سعر الوحدة / Unit Price:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=unit_price_var, width=20).pack(pady=5)

        def save_changes():
            try:
                quantity = float(quantity_var.get())
                unit_price = float(unit_price_var.get())
                if quantity <= 0 or unit_price <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("خطأ / Error", "يرجى إدخال قيم صحيحة / Please enter valid values")
                return

            # تحديث القيم
            total_cost = quantity * unit_price

            self.ingredients_tree.item(selection[0], values=(
                values[0],  # اسم المكون
                values[1],  # الوحدة
                f"{quantity:.3f}",
                f"{unit_price:.3f}",
                f"{total_cost:.3f}",
                "0.0%"  # سيتم حساب النسبة لاحقاً
            ))

            dialog.destroy()
            self.calculate_costs()

        # أزرار النافذة
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="حفظ / Save", command=save_changes).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="إلغاء / Cancel", command=dialog.destroy).pack(side="right", padx=5)

    def calculate_costs(self, event=None):
        """حساب التكاليف"""
        total_cost = 0.0

        # حساب إجمالي التكلفة
        for item in self.ingredients_tree.get_children():
            values = self.ingredients_tree.item(item)['values']
            if len(values) >= 5:
                try:
                    cost = float(values[4])
                    total_cost += cost
                except ValueError:
                    continue

        # حساب النسب المئوية وتحديث الجدول
        for item in self.ingredients_tree.get_children():
            values = self.ingredients_tree.item(item)['values']
            if len(values) >= 5:
                try:
                    cost = float(values[4])
                    percentage = (cost / total_cost * 100) if total_cost > 0 else 0

                    # تحديث النسبة في الجدول
                    updated_values = list(values)
                    updated_values[5] = f"{percentage:.1f}%"
                    self.ingredients_tree.item(item, values=updated_values)
                except ValueError:
                    continue

        # حساب تكلفة الحصة الواحدة
        try:
            servings = int(self.servings_var.get())
            cost_per_serving = total_cost / servings if servings > 0 else 0
        except ValueError:
            servings = 1
            cost_per_serving = total_cost

        # تحديث المتغيرات
        self.total_cost_var.set(f"{total_cost:.3f}")
        self.cost_per_serving_var.set(f"{cost_per_serving:.3f}")

        # حساب السعر المقترح
        self.calculate_suggested_price()

    def calculate_suggested_price(self, event=None):
        """حساب السعر المقترح"""
        try:
            cost_per_serving = float(self.cost_per_serving_var.get())
            profit_margin = float(self.profit_margin_var.get())

            suggested_price = cost_per_serving * (1 + profit_margin / 100)
            self.suggested_price_var.set(f"{suggested_price:.3f}")
        except ValueError:
            self.suggested_price_var.set("0.000")

    def save_meal_costs(self):
        """حفظ تكاليف الوجبة"""
        meal_name = self.meal_var.get()

        if meal_name == "وجبة جديدة / New Meal":
            messagebox.showerror("خطأ / Error", "يرجى اختيار وجبة أو إنشاء وجبة جديدة / Please select a meal or create a new one")
            return

        # التحقق من وجود مكونات
        if not self.ingredients_tree.get_children():
            messagebox.showerror("خطأ / Error", "يرجى إضافة مكونات للوجبة / Please add ingredients to the meal")
            return

        try:
            meal_id = self.meal_dict[meal_name]
            total_cost = float(self.total_cost_var.get())
            cost_per_serving = float(self.cost_per_serving_var.get())
            servings = int(self.servings_var.get())

            # تحديث الوجبة
            self.cursor.execute('''
                UPDATE meals
                SET servings = ?, total_cost = ?, cost_per_serving = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (servings, total_cost, cost_per_serving, meal_id))

            # حذف المكونات القديمة
            self.cursor.execute('DELETE FROM meal_ingredients WHERE meal_id = ?', (meal_id,))

            # إدراج المكونات الجديدة
            for item in self.ingredients_tree.get_children():
                values = self.ingredients_tree.item(item)['values']

                # البحث عن معرف المكون
                self.cursor.execute('SELECT id, unit_price FROM ingredients WHERE name = ?', (values[0],))
                ingredient_data = self.cursor.fetchone()

                if ingredient_data:
                    ingredient_id = ingredient_data[0]
                    quantity = float(values[2])
                    unit_cost = float(values[3])
                    total_ingredient_cost = float(values[4])
                    percentage = float(values[5].replace('%', ''))

                    self.cursor.execute('''
                        INSERT INTO meal_ingredients
                        (meal_id, ingredient_id, quantity_used, unit_cost, total_cost, percentage)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (meal_id, ingredient_id, quantity, unit_cost, total_ingredient_cost, percentage))

            self.conn.commit()
            messagebox.showinfo("نجح / Success", "تم حفظ تكاليف الوجبة بنجاح / Meal costs saved successfully")

            # تحديث قائمة الوجبات المحفوظة
            self.load_saved_meals()

        except Exception as e:
            messagebox.showerror("خطأ / Error", f"حدث خطأ أثناء الحفظ / Error saving: {str(e)}")

    def clear_meal(self):
        """مسح الوجبة الحالية"""
        if messagebox.askyesno("تأكيد المسح / Confirm Clear",
                              "هل أنت متأكد من مسح جميع البيانات؟ / Are you sure you want to clear all data?"):
            # مسح المكونات
            for item in self.ingredients_tree.get_children():
                self.ingredients_tree.delete(item)

            # إعادة تعيين القيم
            self.meal_combo.set("وجبة جديدة / New Meal")
            self.servings_var.set("1")
            self.profit_margin_var.set("30")

            # إعادة حساب التكاليف
            self.calculate_costs()

    def load_saved_meal(self, event):
        """تحميل وجبة محفوظة (عند النقر المزدوج)"""
        selection = self.saved_meals_tree.selection()
        if not selection:
            return

        item = self.saved_meals_tree.item(selection[0])
        meal_name = item['values'][0]

        # تحديد الوجبة في القائمة المنسدلة
        self.meal_combo.set(meal_name)

        # تحميل مكونات الوجبة
        meal_id = self.meal_dict.get(meal_name)
        if meal_id:
            self.load_meal_ingredients(meal_id)

    def update_ingredient_prices(self):
        """تحديث أسعار المكونات"""
        updated_count = 0

        for item in self.ingredients_tree.get_children():
            values = self.ingredients_tree.item(item)['values']
            ingredient_name = values[0]

            # الحصول على السعر الحالي من قاعدة البيانات
            self.cursor.execute('SELECT unit_price FROM ingredients WHERE name = ?', (ingredient_name,))
            result = self.cursor.fetchone()

            if result:
                current_price = result[0]
                old_price = float(values[3])

                if current_price != old_price:
                    # تحديث السعر والتكلفة
                    quantity = float(values[2])
                    new_total_cost = quantity * current_price

                    updated_values = list(values)
                    updated_values[3] = f"{current_price:.3f}"
                    updated_values[4] = f"{new_total_cost:.3f}"

                    self.ingredients_tree.item(item, values=updated_values)
                    updated_count += 1

        if updated_count > 0:
            self.calculate_costs()
            messagebox.showinfo("تحديث الأسعار / Price Update",
                               f"تم تحديث {updated_count} مكون / {updated_count} ingredients updated")
        else:
            messagebox.showinfo("تحديث الأسعار / Price Update",
                               "جميع الأسعار محدثة / All prices are up to date")

    def manage_ingredients(self):
        """إدارة المواد الخام"""
        # نافذة إدارة المواد الخام
        ingredients_window = tk.Toplevel(self.root)
        ingredients_window.title("إدارة المواد الخام / Manage Ingredients")
        ingredients_window.geometry("800x600")

        # جدول المواد الخام
        columns = ("الاسم", "الوحدة", "سعر الوحدة", "الكمية المتاحة", "الحد الأدنى", "المورد")
        ingredients_tree = ttk.Treeview(ingredients_window, columns=columns, show="headings")

        for col in columns:
            ingredients_tree.heading(col, text=col)
            ingredients_tree.column(col, width=120, anchor="center")

        # تحميل البيانات
        self.cursor.execute('''
            SELECT name, unit, unit_price, stock_quantity, min_stock, supplier
            FROM ingredients
            ORDER BY name
        ''')

        ingredients = self.cursor.fetchall()

        for ingredient in ingredients:
            ingredients_tree.insert("", "end", values=ingredient)

        ingredients_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # أزرار الإدارة
        buttons_frame = ttk.Frame(ingredients_window)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(buttons_frame, text="إضافة مادة خام / Add Ingredient",
                  command=lambda: self.add_new_ingredient(ingredients_tree)).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="تعديل / Edit",
                  command=lambda: self.edit_ingredient_data(ingredients_tree)).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="حذف / Delete",
                  command=lambda: self.delete_ingredient_data(ingredients_tree)).pack(side="left", padx=5)

    def add_new_ingredient(self, tree):
        """إضافة مادة خام جديدة"""
        # نافذة إضافة مادة خام
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة مادة خام / Add Ingredient")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # متغيرات الإدخال
        name_var = tk.StringVar()
        unit_var = tk.StringVar()
        price_var = tk.StringVar()
        stock_var = tk.StringVar()
        min_stock_var = tk.StringVar()
        supplier_var = tk.StringVar()

        # عناصر النافذة
        ttk.Label(dialog, text="اسم المادة / Name:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=name_var, width=30).pack(pady=2)

        ttk.Label(dialog, text="الوحدة / Unit:", font=self.arabic_font).pack(pady=5)
        unit_combo = ttk.Combobox(dialog, textvariable=unit_var, values=["كيلو", "جم", "لتر", "قطعة"], width=27)
        unit_combo.pack(pady=2)

        ttk.Label(dialog, text="سعر الوحدة / Unit Price:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=price_var, width=30).pack(pady=2)

        ttk.Label(dialog, text="الكمية المتاحة / Stock Quantity:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=stock_var, width=30).pack(pady=2)

        ttk.Label(dialog, text="الحد الأدنى / Min Stock:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=min_stock_var, width=30).pack(pady=2)

        ttk.Label(dialog, text="المورد / Supplier:", font=self.arabic_font).pack(pady=5)
        ttk.Entry(dialog, textvariable=supplier_var, width=30).pack(pady=2)

        def save_ingredient():
            try:
                name = name_var.get().strip()
                unit = unit_var.get().strip()
                price = float(price_var.get())
                stock = float(stock_var.get())
                min_stock = float(min_stock_var.get())
                supplier = supplier_var.get().strip()

                if not name or not unit:
                    messagebox.showerror("خطأ / Error", "يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")
                    return

                self.cursor.execute('''
                    INSERT INTO ingredients (name, unit, unit_price, stock_quantity, min_stock, supplier)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, unit, price, stock, min_stock, supplier))

                self.conn.commit()

                # تحديث الجدول
                tree.insert("", "end", values=(name, unit, price, stock, min_stock, supplier))

                dialog.destroy()
                messagebox.showinfo("نجح / Success", "تم إضافة المادة الخام بنجاح / Ingredient added successfully")

            except ValueError:
                messagebox.showerror("خطأ / Error", "يرجى إدخال قيم صحيحة / Please enter valid values")
            except Exception as e:
                messagebox.showerror("خطأ / Error", f"حدث خطأ / Error: {str(e)}")

        # أزرار النافذة
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="حفظ / Save", command=save_ingredient).pack(side="right", padx=5)
        ttk.Button(buttons_frame, text="إلغاء / Cancel", command=dialog.destroy).pack(side="right", padx=5)

    def update_prices(self):
        """تحديث أسعار المواد الخام"""
        messagebox.showinfo("تحديث الأسعار / Update Prices",
                           "سيتم تحديث الأسعار من المورد / Prices will be updated from supplier")

    def export_to_excel(self):
        """تصدير إلى Excel"""
        try:
            # جمع بيانات الوجبات والتكاليف
            self.cursor.execute('''
                SELECT m.name, m.servings, m.total_cost, m.cost_per_serving,
                       GROUP_CONCAT(i.name || ' (' || mi.quantity_used || ' ' || i.unit || ')') as ingredients
                FROM meals m
                LEFT JOIN meal_ingredients mi ON m.id = mi.meal_id
                LEFT JOIN ingredients i ON mi.ingredient_id = i.id
                WHERE m.total_cost > 0
                GROUP BY m.id, m.name, m.servings, m.total_cost, m.cost_per_serving
            ''')

            data = self.cursor.fetchall()

            # إنشاء DataFrame
            df = pd.DataFrame(data, columns=[
                'اسم الوجبة', 'عدد الحصص', 'إجمالي التكلفة', 'تكلفة الحصة', 'المكونات'
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
                c.drawString(50, height - 50, "Restaurant Costing Report - تقرير تكاليف المطعم")

                # التاريخ
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 80, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

                # بيانات الوجبة الحالية
                meal_name = self.meal_var.get()
                if meal_name != "وجبة جديدة / New Meal":
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, height - 120, f"Meal: {meal_name}")
                    c.drawString(50, height - 140, f"Total Cost: {self.total_cost_var.get()} SAR")
                    c.drawString(50, height - 160, f"Cost per Serving: {self.cost_per_serving_var.get()} SAR")
                    c.drawString(50, height - 180, f"Suggested Price: {self.suggested_price_var.get()} SAR")

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
    app = CostingScreenGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
