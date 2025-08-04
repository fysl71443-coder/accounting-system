#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام حساب التكاليف المتقدم للمطاعم
Advanced Restaurant Costing System

يدعم:
- حساب تكلفة الوجبات بدقة عالية
- إدارة المكونات والمواد الخام
- حساب النسب المئوية لكل مكون
- واجهة عربية/إنجليزية
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import os
import sys

# إعداد الترميز للعربية
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'Arabic_Saudi Arabia.1256')

class CostingDatabase:
    """إدارة قاعدة البيانات للنظام"""
    
    def __init__(self, db_path="restaurant_costing.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الوجبات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                name_en TEXT,
                description TEXT,
                servings INTEGER DEFAULT 1,
                total_cost REAL DEFAULT 0.0,
                cost_per_serving REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المواد الخام
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                name_en TEXT,
                unit TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                stock_quantity REAL DEFAULT 0.0,
                min_stock REAL DEFAULT 0.0,
                supplier TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول مكونات الوجبات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meal_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id INTEGER,
                ingredient_id INTEGER,
                quantity REAL NOT NULL,
                unit_cost REAL NOT NULL,
                total_cost REAL NOT NULL,
                percentage REAL DEFAULT 0.0,
                notes TEXT,
                FOREIGN KEY (meal_id) REFERENCES meals (id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
            )
        ''')
        
        # إدراج بيانات تجريبية
        self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        """إدراج بيانات تجريبية"""
        # التحقق من وجود بيانات
        cursor.execute("SELECT COUNT(*) FROM ingredients")
        if cursor.fetchone()[0] > 0:
            return
        
        # مواد خام تجريبية
        ingredients = [
            ("أرز بسمتي", "Basmati Rice", "كيلو", 12.50, 50.0, 10.0, "مورد الأرز"),
            ("دجاج طازج", "Fresh Chicken", "كيلو", 25.00, 30.0, 5.0, "مزرعة الدجاج"),
            ("بصل أحمر", "Red Onion", "كيلو", 3.50, 20.0, 5.0, "مورد الخضار"),
            ("طماطم", "Tomatoes", "كيلو", 4.00, 15.0, 3.0, "مورد الخضار"),
            ("لبن زبادي", "Yogurt", "كيلو", 8.00, 10.0, 2.0, "مصنع الألبان"),
            ("بهارات البرياني", "Biryani Spices", "كيلو", 45.00, 5.0, 1.0, "مورد البهارات"),
            ("زيت دوار الشمس", "Sunflower Oil", "لتر", 8.50, 20.0, 5.0, "مورد الزيوت"),
            ("ملح طعام", "Table Salt", "كيلو", 2.00, 10.0, 2.0, "مورد التوابل"),
            ("ثوم", "Garlic", "كيلو", 15.00, 8.0, 2.0, "مورد الخضار"),
            ("زنجبيل", "Ginger", "كيلو", 20.00, 5.0, 1.0, "مورد الخضار"),
            ("زعفران", "Saffron", "جرام", 0.50, 100.0, 20.0, "مورد البهارات الفاخرة"),
            ("لوز مقشر", "Peeled Almonds", "كيلو", 35.00, 3.0, 0.5, "مورد المكسرات"),
            ("زبيب ذهبي", "Golden Raisins", "كيلو", 18.00, 2.0, 0.5, "مورد المكسرات"),
            ("دقيق أبيض", "White Flour", "كيلو", 4.00, 25.0, 5.0, "مطحنة الدقيق"),
            ("سكر أبيض", "White Sugar", "كيلو", 5.00, 20.0, 5.0, "مصنع السكر"),
        ]
        
        cursor.executemany('''
            INSERT INTO ingredients (name, name_en, unit, purchase_price, stock_quantity, min_stock, supplier)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ingredients)
        
        # وجبات تجريبية
        meals = [
            ("برياني دجاج", "Chicken Biryani", "وجبة برياني دجاج بالبهارات الخاصة", 4),
            ("برياني لحم", "Mutton Biryani", "وجبة برياني لحم بالبهارات الفاخرة", 4),
            ("كبسة دجاج", "Chicken Kabsa", "كبسة دجاج سعودية أصيلة", 6),
        ]
        
        cursor.executemany('''
            INSERT INTO meals (name, name_en, description, servings)
            VALUES (?, ?, ?, ?)
        ''', meals)
    
    def get_connection(self):
        """الحصول على اتصال قاعدة البيانات"""
        return sqlite3.connect(self.db_path)
    
    def get_all_meals(self):
        """الحصول على جميع الوجبات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals ORDER BY name")
        meals = cursor.fetchall()
        conn.close()
        return meals
    
    def get_all_ingredients(self):
        """الحصول على جميع المواد الخام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ingredients ORDER BY name")
        ingredients = cursor.fetchall()
        conn.close()
        return ingredients
    
    def get_meal_ingredients(self, meal_id):
        """الحصول على مكونات وجبة معينة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT mi.*, i.name, i.name_en, i.unit, i.purchase_price
            FROM meal_ingredients mi
            JOIN ingredients i ON mi.ingredient_id = i.id
            WHERE mi.meal_id = ?
            ORDER BY mi.id
        ''', (meal_id,))
        ingredients = cursor.fetchall()
        conn.close()
        return ingredients
    
    def save_meal_cost(self, meal_id, ingredients_data, total_cost, cost_per_serving):
        """حفظ تكلفة الوجبة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # حذف المكونات القديمة
            cursor.execute("DELETE FROM meal_ingredients WHERE meal_id = ?", (meal_id,))
            
            # إضافة المكونات الجديدة
            for ingredient in ingredients_data:
                cursor.execute('''
                    INSERT INTO meal_ingredients 
                    (meal_id, ingredient_id, quantity, unit_cost, total_cost, percentage, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', ingredient)
            
            # تحديث تكلفة الوجبة
            cursor.execute('''
                UPDATE meals 
                SET total_cost = ?, cost_per_serving = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (total_cost, cost_per_serving, meal_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"خطأ في حفظ البيانات: {e}")
            return False
        finally:
            conn.close()

class CostingScreen:
    """شاشة حساب التكاليف الرئيسية"""
    
    def __init__(self, root):
        self.root = root
        self.db = CostingDatabase()
        self.language = "ar"  # اللغة الافتراضية
        self.current_meal_id = None
        self.ingredients_data = []
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("نظام حساب التكاليف - Restaurant Costing System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # إعداد الخطوط
        self.setup_fonts()
        
        # إنشاء الإطار الرئيسي
        self.create_main_frame()
        
        # إنشاء شريط الأدوات
        self.create_toolbar()
        
        # إنشاء قسم اختيار الوجبة
        self.create_meal_selection()
        
        # إنشاء جدول المكونات
        self.create_ingredients_table()
        
        # إنشاء قسم الحسابات
        self.create_calculations_section()
        
        # إنشاء أزرار التحكم
        self.create_control_buttons()
    
    def setup_fonts(self):
        """إعداد الخطوط للعربية"""
        try:
            self.arabic_font = ("Arial Unicode MS", 10)
            self.arabic_font_bold = ("Arial Unicode MS", 10, "bold")
            self.arabic_font_large = ("Arial Unicode MS", 12, "bold")
        except:
            self.arabic_font = ("Arial", 10)
            self.arabic_font_bold = ("Arial", 10, "bold")
            self.arabic_font_large = ("Arial", 12, "bold")
    
    def create_main_frame(self):
        """إنشاء الإطار الرئيسي"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # تكوين الشبكة
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar_frame = ttk.Frame(self.main_frame)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # عنوان النظام
        title_label = ttk.Label(toolbar_frame, text="نظام حساب التكاليف المتقدم", 
                               font=self.arabic_font_large)
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # أزرار شريط الأدوات
        buttons_frame = ttk.Frame(toolbar_frame)
        buttons_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(buttons_frame, text="وجبة جديدة", command=self.new_meal).grid(row=0, column=0, padx=2)
        ttk.Button(buttons_frame, text="تحديث الأسعار", command=self.update_prices).grid(row=0, column=1, padx=2)
        ttk.Button(buttons_frame, text="تصدير PDF", command=self.export_pdf).grid(row=0, column=2, padx=2)
        ttk.Button(buttons_frame, text="EN/AR", command=self.toggle_language).grid(row=0, column=3, padx=2)
        
        toolbar_frame.columnconfigure(1, weight=1)
    
    def create_meal_selection(self):
        """إنشاء قسم اختيار الوجبة"""
        meal_frame = ttk.LabelFrame(self.main_frame, text="اختيار الوجبة", padding="10")
        meal_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # اختيار الوجبة
        ttk.Label(meal_frame, text="اسم الوجبة:", font=self.arabic_font).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.meal_var = tk.StringVar()
        self.meal_combo = ttk.Combobox(meal_frame, textvariable=self.meal_var, 
                                      font=self.arabic_font, width=30, state="readonly")
        self.meal_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.meal_combo.bind('<<ComboboxSelected>>', self.on_meal_selected)
        
        # عدد الحصص
        ttk.Label(meal_frame, text="عدد الحصص:", font=self.arabic_font).grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        
        self.servings_var = tk.StringVar(value="1")
        servings_spinbox = ttk.Spinbox(meal_frame, from_=1, to=20, textvariable=self.servings_var, 
                                      width=10, command=self.calculate_totals)
        servings_spinbox.grid(row=0, column=3, sticky=tk.W)
        
        meal_frame.columnconfigure(1, weight=1)
    
    def create_ingredients_table(self):
        """إنشاء جدول المكونات"""
        table_frame = ttk.LabelFrame(self.main_frame, text="مكونات الوجبة", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # إنشاء Treeview
        columns = ("ingredient", "unit", "quantity", "unit_price", "total_cost", "percentage")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # تعريف العناوين
        headers = {
            "ingredient": "اسم المكون",
            "unit": "الوحدة", 
            "quantity": "الكمية",
            "unit_price": "سعر الوحدة",
            "total_cost": "التكلفة الجزئية",
            "percentage": "النسبة %"
        }
        
        for col, header in headers.items():
            self.tree.heading(col, text=header)
            if col == "ingredient":
                self.tree.column(col, width=200, anchor=tk.W)
            elif col in ["unit", "percentage"]:
                self.tree.column(col, width=80, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=120, anchor=tk.E)
        
        # إضافة scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # أزرار إدارة المكونات
        buttons_frame = ttk.Frame(table_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="إضافة مكون", command=self.add_ingredient).grid(row=0, column=0, padx=2)
        ttk.Button(buttons_frame, text="تعديل مكون", command=self.edit_ingredient).grid(row=0, column=1, padx=2)
        ttk.Button(buttons_frame, text="حذف مكون", command=self.delete_ingredient).grid(row=0, column=2, padx=2)
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
    
    def create_calculations_section(self):
        """إنشاء قسم الحسابات"""
        calc_frame = ttk.LabelFrame(self.main_frame, text="الحسابات النهائية", padding="10")
        calc_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # المتغيرات
        self.total_cost_var = tk.StringVar(value="0.00")
        self.cost_per_serving_var = tk.StringVar(value="0.00")
        
        # التكلفة الإجمالية
        ttk.Label(calc_frame, text="التكلفة الإجمالية:", font=self.arabic_font_bold).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(calc_frame, textvariable=self.total_cost_var, font=self.arabic_font_bold, 
                 foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(calc_frame, text="ريال", font=self.arabic_font).grid(row=0, column=2, sticky=tk.W)
        
        # تكلفة الحصة الواحدة
        ttk.Label(calc_frame, text="تكلفة الحصة الواحدة:", font=self.arabic_font_bold).grid(row=0, column=3, sticky=tk.W, padx=(20, 10))
        ttk.Label(calc_frame, textvariable=self.cost_per_serving_var, font=self.arabic_font_bold, 
                 foreground="green").grid(row=0, column=4, sticky=tk.W, padx=(0, 20))
        ttk.Label(calc_frame, text="ريال", font=self.arabic_font).grid(row=0, column=5, sticky=tk.W)
    
    def create_control_buttons(self):
        """إنشاء أزرار التحكم"""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(control_frame, text="حفظ التكاليف", command=self.save_costs, 
                  style="Accent.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="إعادة حساب", command=self.calculate_totals).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="مسح الكل", command=self.clear_all).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="خروج", command=self.root.quit).grid(row=0, column=3, padx=5)
    
    def load_data(self):
        """تحميل البيانات الأولية"""
        # تحميل الوجبات
        meals = self.db.get_all_meals()
        meal_names = [f"{meal[1]} ({meal[0]})" for meal in meals]
        self.meal_combo['values'] = meal_names
        
        if meal_names:
            self.meal_combo.current(0)
            self.on_meal_selected()
    
    def on_meal_selected(self, event=None):
        """عند اختيار وجبة"""
        if not self.meal_var.get():
            return
        
        # استخراج معرف الوجبة
        meal_text = self.meal_var.get()
        meal_id = int(meal_text.split('(')[1].split(')')[0])
        self.current_meal_id = meal_id
        
        # تحميل مكونات الوجبة
        self.load_meal_ingredients()
    
    def load_meal_ingredients(self):
        """تحميل مكونات الوجبة المختارة"""
        if not self.current_meal_id:
            return
        
        # مسح الجدول
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # تحميل المكونات
        ingredients = self.db.get_meal_ingredients(self.current_meal_id)
        
        for ingredient in ingredients:
            self.tree.insert("", "end", values=(
                ingredient[5],  # اسم المكون
                ingredient[7],  # الوحدة
                f"{ingredient[2]:.3f}",  # الكمية
                f"{ingredient[3]:.3f}",  # سعر الوحدة
                f"{ingredient[4]:.3f}",  # التكلفة الجزئية
                f"{ingredient[6]:.1f}%"  # النسبة المئوية
            ))
        
        self.calculate_totals()
    
    def calculate_totals(self):
        """حساب الإجماليات"""
        total_cost = Decimal('0.00')
        
        # حساب التكلفة الإجمالية
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            cost = Decimal(str(values[4]))
            total_cost += cost
        
        # حساب النسب المئوية
        for item in self.tree.get_children():
            values = list(self.tree.item(item)['values'])
            if total_cost > 0:
                cost = Decimal(str(values[4]))
                percentage = (cost / total_cost * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                values[5] = f"{percentage}%"
                self.tree.item(item, values=values)
        
        # تحديث المتغيرات
        servings = int(self.servings_var.get())
        cost_per_serving = (total_cost / servings).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        self.total_cost_var.set(f"{total_cost:.2f}")
        self.cost_per_serving_var.set(f"{cost_per_serving:.2f}")
    
    def add_ingredient(self):
        """إضافة مكون جديد"""
        self.open_ingredient_dialog()
    
    def edit_ingredient(self):
        """تعديل مكون موجود"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مكون للتعديل")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        self.open_ingredient_dialog(item, values)
    
    def delete_ingredient(self):
        """حذف مكون"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مكون للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذا المكون؟"):
            self.tree.delete(selected[0])
            self.calculate_totals()
    
    def open_ingredient_dialog(self, item=None, values=None):
        """فتح نافذة إضافة/تعديل مكون"""
        dialog = IngredientDialog(self.root, self.db, self.arabic_font)
        
        if values:
            dialog.set_values(values)
        
        result = dialog.show()
        
        if result:
            ingredient_name, unit, quantity, unit_price, total_cost = result
            
            if item:
                # تعديل موجود
                self.tree.item(item, values=(ingredient_name, unit, f"{quantity:.3f}", 
                                           f"{unit_price:.3f}", f"{total_cost:.3f}", "0.0%"))
            else:
                # إضافة جديد
                self.tree.insert("", "end", values=(ingredient_name, unit, f"{quantity:.3f}", 
                                                  f"{unit_price:.3f}", f"{total_cost:.3f}", "0.0%"))
            
            self.calculate_totals()
    
    def save_costs(self):
        """حفظ التكاليف"""
        if not self.current_meal_id:
            messagebox.showwarning("تحذير", "يرجى اختيار وجبة أولاً")
            return
        
        # جمع بيانات المكونات
        ingredients_data = []
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            
            # البحث عن معرف المكون
            ingredient_name = values[0]
            ingredients = self.db.get_all_ingredients()
            ingredient_id = None
            
            for ing in ingredients:
                if ing[1] == ingredient_name:
                    ingredient_id = ing[0]
                    break
            
            if ingredient_id:
                quantity = float(values[2])
                unit_cost = float(values[3])
                total_cost = float(values[4])
                percentage = float(values[5].replace('%', ''))
                
                ingredients_data.append((
                    self.current_meal_id, ingredient_id, quantity, 
                    unit_cost, total_cost, percentage, ""
                ))
        
        # حفظ في قاعدة البيانات
        total_cost = float(self.total_cost_var.get())
        cost_per_serving = float(self.cost_per_serving_var.get())
        
        if self.db.save_meal_cost(self.current_meal_id, ingredients_data, total_cost, cost_per_serving):
            messagebox.showinfo("نجح", "تم حفظ التكاليف بنجاح")
        else:
            messagebox.showerror("خطأ", "فشل في حفظ التكاليف")
    
    def clear_all(self):
        """مسح جميع المكونات"""
        if messagebox.askyesno("تأكيد", "هل تريد مسح جميع المكونات؟"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.calculate_totals()
    
    def new_meal(self):
        """إضافة وجبة جديدة"""
        messagebox.showinfo("قريباً", "هذه الميزة ستكون متاحة قريباً")
    
    def update_prices(self):
        """تحديث الأسعار"""
        messagebox.showinfo("تحديث", "تم تحديث الأسعار من قاعدة البيانات")
        self.load_meal_ingredients()
    
    def export_pdf(self):
        """تصدير تقرير PDF"""
        messagebox.showinfo("قريباً", "تصدير PDF سيكون متاح قريباً")
    
    def toggle_language(self):
        """تبديل اللغة"""
        self.language = "en" if self.language == "ar" else "ar"
        messagebox.showinfo("اللغة", f"تم التبديل إلى {'الإنجليزية' if self.language == 'en' else 'العربية'}")

class IngredientDialog:
    """نافذة إضافة/تعديل مكون"""
    
    def __init__(self, parent, db, font):
        self.parent = parent
        self.db = db
        self.font = font
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة/تعديل مكون")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """إعداد النافذة"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # اختيار المكون
        ttk.Label(main_frame, text="اسم المكون:", font=self.font).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.ingredient_var = tk.StringVar()
        self.ingredient_combo = ttk.Combobox(main_frame, textvariable=self.ingredient_var, 
                                           font=self.font, width=30)
        self.ingredient_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.ingredient_combo.bind('<<ComboboxSelected>>', self.on_ingredient_selected)
        
        # تحميل المكونات
        ingredients = self.db.get_all_ingredients()
        ingredient_names = [f"{ing[1]} - {ing[3]} {ing[2]}" for ing in ingredients]
        self.ingredient_combo['values'] = ingredient_names
        
        # الوحدة
        ttk.Label(main_frame, text="الوحدة:", font=self.font).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.unit_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.unit_var, font=self.font).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # الكمية
        ttk.Label(main_frame, text="الكمية المستخدمة:", font=self.font).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0.000")
        quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, font=self.font, width=15)
        quantity_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        quantity_entry.bind('<KeyRelease>', self.calculate_cost)
        
        # سعر الوحدة
        ttk.Label(main_frame, text="سعر الوحدة:", font=self.font).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.unit_price_var = tk.StringVar(value="0.000")
        price_entry = ttk.Entry(main_frame, textvariable=self.unit_price_var, font=self.font, width=15)
        price_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        price_entry.bind('<KeyRelease>', self.calculate_cost)
        
        # التكلفة الإجمالية
        ttk.Label(main_frame, text="التكلفة الإجمالية:", font=self.font).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.total_cost_var = tk.StringVar(value="0.000")
        ttk.Label(main_frame, textvariable=self.total_cost_var, font=self.font, 
                 foreground="blue").grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # أزرار التحكم
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="موافق", command=self.ok_clicked).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=self.cancel_clicked).grid(row=0, column=1, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
    
    def on_ingredient_selected(self, event=None):
        """عند اختيار مكون"""
        if not self.ingredient_var.get():
            return
        
        # استخراج معلومات المكون
        ingredient_text = self.ingredient_var.get()
        ingredient_name = ingredient_text.split(' - ')[0]
        
        # البحث عن المكون في قاعدة البيانات
        ingredients = self.db.get_all_ingredients()
        for ing in ingredients:
            if ing[1] == ingredient_name:
                self.unit_var.set(ing[3])
                self.unit_price_var.set(f"{ing[4]:.3f}")
                self.calculate_cost()
                break
    
    def calculate_cost(self, event=None):
        """حساب التكلفة"""
        try:
            quantity = float(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            total_cost = quantity * unit_price
            self.total_cost_var.set(f"{total_cost:.3f}")
        except ValueError:
            self.total_cost_var.set("0.000")
    
    def set_values(self, values):
        """تعيين القيم للتعديل"""
        self.ingredient_var.set(values[0])
        self.unit_var.set(values[1])
        self.quantity_var.set(values[2])
        self.unit_price_var.set(values[3])
        self.total_cost_var.set(values[4])
    
    def ok_clicked(self):
        """عند الضغط على موافق"""
        try:
            ingredient_name = self.ingredient_var.get().split(' - ')[0]
            unit = self.unit_var.get()
            quantity = float(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            total_cost = float(self.total_cost_var.get())
            
            if not ingredient_name or quantity <= 0 or unit_price <= 0:
                messagebox.showwarning("تحذير", "يرجى إدخال جميع البيانات بشكل صحيح")
                return
            
            self.result = (ingredient_name, unit, quantity, unit_price, total_cost)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة")
    
    def cancel_clicked(self):
        """عند الضغط على إلغاء"""
        self.dialog.destroy()
    
    def show(self):
        """عرض النافذة وإرجاع النتيجة"""
        self.dialog.wait_window()
        return self.result

def main():
    """الوظيفة الرئيسية"""
    root = tk.Tk()
    
    # إعداد النمط
    style = ttk.Style()
    style.theme_use('clam')
    
    # إنشاء التطبيق
    app = CostingScreen(root)
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    main()
