#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إدارة المواد الخام والوجبات
Ingredients and Meals Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class IngredientsManager:
    """نظام إدارة المواد الخام"""
    
    def __init__(self, root, db_path="restaurant_costing.db"):
        self.root = root
        self.db_path = db_path
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("إدارة المواد الخام - Ingredients Management")
        self.root.geometry("1000x600")
        
        # إنشاء النوت بوك للتبويبات
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # تبويب المواد الخام
        self.create_ingredients_tab()
        
        # تبويب الوجبات
        self.create_meals_tab()
    
    def create_ingredients_tab(self):
        """إنشاء تبويب المواد الخام"""
        ingredients_frame = ttk.Frame(self.notebook)
        self.notebook.add(ingredients_frame, text="المواد الخام")
        
        # شريط الأدوات
        toolbar = ttk.Frame(ingredients_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="إضافة مادة خام", command=self.add_ingredient).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="تعديل", command=self.edit_ingredient).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="حذف", command=self.delete_ingredient).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="تحديث", command=self.refresh_ingredients).pack(side=tk.LEFT, padx=2)
        
        # جدول المواد الخام
        columns = ("id", "name", "name_en", "unit", "price", "stock", "min_stock", "supplier")
        self.ingredients_tree = ttk.Treeview(ingredients_frame, columns=columns, show="headings")
        
        headers = {
            "id": "المعرف",
            "name": "الاسم بالعربية",
            "name_en": "الاسم بالإنجليزية", 
            "unit": "الوحدة",
            "price": "السعر",
            "stock": "المخزون",
            "min_stock": "الحد الأدنى",
            "supplier": "المورد"
        }
        
        for col, header in headers.items():
            self.ingredients_tree.heading(col, text=header)
            if col == "id":
                self.ingredients_tree.column(col, width=50)
            elif col in ["name", "name_en", "supplier"]:
                self.ingredients_tree.column(col, width=150)
            else:
                self.ingredients_tree.column(col, width=100)
        
        # إضافة scrollbar
        ing_scrollbar = ttk.Scrollbar(ingredients_frame, orient=tk.VERTICAL, command=self.ingredients_tree.yview)
        self.ingredients_tree.configure(yscrollcommand=ing_scrollbar.set)
        
        self.ingredients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        ing_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
    
    def create_meals_tab(self):
        """إنشاء تبويب الوجبات"""
        meals_frame = ttk.Frame(self.notebook)
        self.notebook.add(meals_frame, text="الوجبات")
        
        # شريط الأدوات
        toolbar = ttk.Frame(meals_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="إضافة وجبة", command=self.add_meal).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="تعديل", command=self.edit_meal).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="حذف", command=self.delete_meal).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="تحديث", command=self.refresh_meals).pack(side=tk.LEFT, padx=2)
        
        # جدول الوجبات
        columns = ("id", "name", "name_en", "description", "servings", "total_cost", "cost_per_serving")
        self.meals_tree = ttk.Treeview(meals_frame, columns=columns, show="headings")
        
        headers = {
            "id": "المعرف",
            "name": "اسم الوجبة",
            "name_en": "الاسم بالإنجليزية",
            "description": "الوصف",
            "servings": "عدد الحصص",
            "total_cost": "التكلفة الإجمالية",
            "cost_per_serving": "تكلفة الحصة"
        }
        
        for col, header in headers.items():
            self.meals_tree.heading(col, text=header)
            if col == "id":
                self.meals_tree.column(col, width=50)
            elif col == "description":
                self.meals_tree.column(col, width=200)
            elif col in ["name", "name_en"]:
                self.meals_tree.column(col, width=150)
            else:
                self.meals_tree.column(col, width=100)
        
        # إضافة scrollbar
        meals_scrollbar = ttk.Scrollbar(meals_frame, orient=tk.VERTICAL, command=self.meals_tree.yview)
        self.meals_tree.configure(yscrollcommand=meals_scrollbar.set)
        
        self.meals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        meals_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
    
    def load_data(self):
        """تحميل البيانات"""
        self.refresh_ingredients()
        self.refresh_meals()
    
    def refresh_ingredients(self):
        """تحديث جدول المواد الخام"""
        # مسح البيانات الحالية
        for item in self.ingredients_tree.get_children():
            self.ingredients_tree.delete(item)
        
        # تحميل البيانات من قاعدة البيانات
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ingredients ORDER BY name")
        ingredients = cursor.fetchall()
        conn.close()
        
        # إضافة البيانات للجدول
        for ingredient in ingredients:
            self.ingredients_tree.insert("", "end", values=ingredient)
    
    def refresh_meals(self):
        """تحديث جدول الوجبات"""
        # مسح البيانات الحالية
        for item in self.meals_tree.get_children():
            self.meals_tree.delete(item)
        
        # تحميل البيانات من قاعدة البيانات
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals ORDER BY name")
        meals = cursor.fetchall()
        conn.close()
        
        # إضافة البيانات للجدول
        for meal in meals:
            self.meals_tree.insert("", "end", values=meal)
    
    def add_ingredient(self):
        """إضافة مادة خام جديدة"""
        dialog = IngredientEditDialog(self.root, "إضافة مادة خام جديدة")
        result = dialog.show()
        
        if result:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO ingredients (name, name_en, unit, purchase_price, stock_quantity, min_stock, supplier)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', result)
                conn.commit()
                messagebox.showinfo("نجح", "تم إضافة المادة الخام بنجاح")
                self.refresh_ingredients()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "اسم المادة الخام موجود مسبقاً")
            finally:
                conn.close()
    
    def edit_ingredient(self):
        """تعديل مادة خام"""
        selected = self.ingredients_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مادة خام للتعديل")
            return
        
        item = selected[0]
        values = self.ingredients_tree.item(item)['values']
        
        dialog = IngredientEditDialog(self.root, "تعديل مادة خام", values)
        result = dialog.show()
        
        if result:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE ingredients 
                    SET name=?, name_en=?, unit=?, purchase_price=?, stock_quantity=?, min_stock=?, supplier=?
                    WHERE id=?
                ''', result + (values[0],))
                conn.commit()
                messagebox.showinfo("نجح", "تم تحديث المادة الخام بنجاح")
                self.refresh_ingredients()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "اسم المادة الخام موجود مسبقاً")
            finally:
                conn.close()
    
    def delete_ingredient(self):
        """حذف مادة خام"""
        selected = self.ingredients_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مادة خام للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذه المادة الخام؟"):
            item = selected[0]
            values = self.ingredients_tree.item(item)['values']
            ingredient_id = values[0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ingredients WHERE id=?", (ingredient_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجح", "تم حذف المادة الخام بنجاح")
            self.refresh_ingredients()
    
    def add_meal(self):
        """إضافة وجبة جديدة"""
        dialog = MealEditDialog(self.root, "إضافة وجبة جديدة")
        result = dialog.show()
        
        if result:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO meals (name, name_en, description, servings)
                    VALUES (?, ?, ?, ?)
                ''', result)
                conn.commit()
                messagebox.showinfo("نجح", "تم إضافة الوجبة بنجاح")
                self.refresh_meals()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "اسم الوجبة موجود مسبقاً")
            finally:
                conn.close()
    
    def edit_meal(self):
        """تعديل وجبة"""
        selected = self.meals_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار وجبة للتعديل")
            return
        
        item = selected[0]
        values = self.meals_tree.item(item)['values']
        
        dialog = MealEditDialog(self.root, "تعديل وجبة", values)
        result = dialog.show()
        
        if result:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE meals 
                    SET name=?, name_en=?, description=?, servings=?
                    WHERE id=?
                ''', result + (values[0],))
                conn.commit()
                messagebox.showinfo("نجح", "تم تحديث الوجبة بنجاح")
                self.refresh_meals()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "اسم الوجبة موجود مسبقاً")
            finally:
                conn.close()
    
    def delete_meal(self):
        """حذف وجبة"""
        selected = self.meals_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار وجبة للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذه الوجبة؟"):
            item = selected[0]
            values = self.meals_tree.item(item)['values']
            meal_id = values[0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meals WHERE id=?", (meal_id,))
            cursor.execute("DELETE FROM meal_ingredients WHERE meal_id=?", (meal_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجح", "تم حذف الوجبة بنجاح")
            self.refresh_meals()

class IngredientEditDialog:
    """نافذة تعديل مادة خام"""
    
    def __init__(self, parent, title, values=None):
        self.parent = parent
        self.values = values
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
        
        if values:
            self.load_values()
    
    def setup_dialog(self):
        """إعداد النافذة"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # الحقول
        fields = [
            ("الاسم بالعربية:", "name"),
            ("الاسم بالإنجليزية:", "name_en"),
            ("الوحدة:", "unit"),
            ("سعر الشراء:", "price"),
            ("كمية المخزون:", "stock"),
            ("الحد الأدنى:", "min_stock"),
            ("المورد:", "supplier")
        ]
        
        self.vars = {}
        
        for i, (label, var_name) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            self.vars[var_name] = tk.StringVar()
            entry = ttk.Entry(main_frame, textvariable=self.vars[var_name], width=30)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # أزرار التحكم
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="موافق", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
    
    def load_values(self):
        """تحميل القيم للتعديل"""
        if self.values:
            self.vars["name"].set(self.values[1])
            self.vars["name_en"].set(self.values[2] or "")
            self.vars["unit"].set(self.values[3])
            self.vars["price"].set(str(self.values[4]))
            self.vars["stock"].set(str(self.values[5]))
            self.vars["min_stock"].set(str(self.values[6]))
            self.vars["supplier"].set(self.values[7] or "")
    
    def ok_clicked(self):
        """عند الضغط على موافق"""
        try:
            name = self.vars["name"].get().strip()
            name_en = self.vars["name_en"].get().strip()
            unit = self.vars["unit"].get().strip()
            price = float(self.vars["price"].get())
            stock = float(self.vars["stock"].get())
            min_stock = float(self.vars["min_stock"].get())
            supplier = self.vars["supplier"].get().strip()
            
            if not name or not unit or price < 0 or stock < 0 or min_stock < 0:
                messagebox.showwarning("تحذير", "يرجى إدخال جميع البيانات بشكل صحيح")
                return
            
            self.result = (name, name_en, unit, price, stock, min_stock, supplier)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للسعر والكميات")
    
    def cancel_clicked(self):
        """عند الضغط على إلغاء"""
        self.dialog.destroy()
    
    def show(self):
        """عرض النافذة وإرجاع النتيجة"""
        self.dialog.wait_window()
        return self.result

class MealEditDialog:
    """نافذة تعديل وجبة"""
    
    def __init__(self, parent, title, values=None):
        self.parent = parent
        self.values = values
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
        
        if values:
            self.load_values()
    
    def setup_dialog(self):
        """إعداد النافذة"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # الحقول
        ttk.Label(main_frame, text="اسم الوجبة:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="الاسم بالإنجليزية:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_en_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_en_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="الوصف:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.description_var, width=30).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="عدد الحصص:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.servings_var = tk.StringVar(value="1")
        ttk.Spinbox(main_frame, from_=1, to=20, textvariable=self.servings_var, width=28).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # أزرار التحكم
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="موافق", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
    
    def load_values(self):
        """تحميل القيم للتعديل"""
        if self.values:
            self.name_var.set(self.values[1])
            self.name_en_var.set(self.values[2] or "")
            self.description_var.set(self.values[3] or "")
            self.servings_var.set(str(self.values[4]))
    
    def ok_clicked(self):
        """عند الضغط على موافق"""
        try:
            name = self.name_var.get().strip()
            name_en = self.name_en_var.get().strip()
            description = self.description_var.get().strip()
            servings = int(self.servings_var.get())
            
            if not name or servings < 1:
                messagebox.showwarning("تحذير", "يرجى إدخال اسم الوجبة وعدد حصص صحيح")
                return
            
            self.result = (name, name_en, description, servings)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال رقم صحيح لعدد الحصص")
    
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
    app = IngredientsManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
