#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
عرض توضيحي لنظام حساب التكاليف
Simple Costing System Demo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP

class SimpleCostingDemo:
    """عرض توضيحي مبسط لنظام حساب التكاليف"""
    
    def __init__(self, root):
        self.root = root
        self.ingredients_data = []
        self.setup_ui()
        self.load_sample_data()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.root.title("نظام حساب التكاليف - عرض توضيحي")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f8ff')
        
        # إعداد الخطوط
        try:
            self.arabic_font = ("Arial Unicode MS", 10)
            self.arabic_font_bold = ("Arial Unicode MS", 10, "bold")
            self.title_font = ("Arial Unicode MS", 14, "bold")
        except:
            self.arabic_font = ("Arial", 10)
            self.arabic_font_bold = ("Arial", 10, "bold")
            self.title_font = ("Arial", 14, "bold")
        
        self.create_header()
        self.create_meal_info()
        self.create_ingredients_table()
        self.create_calculations()
        self.create_buttons()
    
    def create_header(self):
        """إنشاء رأس الصفحة"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="🧮 نظام حساب التكاليف المتقدم للمطاعم",
                              font=self.title_font,
                              fg='white',
                              bg='#2c3e50')
        title_label.pack(pady=25)
    
    def create_meal_info(self):
        """إنشاء معلومات الوجبة"""
        info_frame = ttk.LabelFrame(self.root, text="معلومات الوجبة", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # اسم الوجبة
        tk.Label(info_frame, text="اسم الوجبة:", font=self.arabic_font_bold).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.meal_name_var = tk.StringVar(value="برياني دجاج")
        tk.Label(info_frame, textvariable=self.meal_name_var, font=self.arabic_font, fg='blue').grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # عدد الحصص
        tk.Label(info_frame, text="عدد الحصص:", font=self.arabic_font_bold).grid(row=0, column=2, sticky=tk.W, padx=20)
        self.servings_var = tk.StringVar(value="4")
        servings_spinbox = tk.Spinbox(info_frame, from_=1, to=20, textvariable=self.servings_var, 
                                     width=5, command=self.calculate_totals)
        servings_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
    
    def create_ingredients_table(self):
        """إنشاء جدول المكونات"""
        table_frame = ttk.LabelFrame(self.root, text="مكونات الوجبة وحساب التكاليف", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # إنشاء Treeview
        columns = ("ingredient", "quantity", "unit", "unit_price", "total_cost", "percentage")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # تعريف العناوين
        headers = {
            "ingredient": "اسم المكون",
            "quantity": "الكمية",
            "unit": "الوحدة",
            "unit_price": "سعر الوحدة (ريال)",
            "total_cost": "التكلفة الجزئية (ريال)",
            "percentage": "النسبة المئوية"
        }
        
        for col, header in headers.items():
            self.tree.heading(col, text=header)
            if col == "ingredient":
                self.tree.column(col, width=200, anchor=tk.W)
            elif col == "unit":
                self.tree.column(col, width=80, anchor=tk.CENTER)
            elif col == "percentage":
                self.tree.column(col, width=100, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=120, anchor=tk.E)
        
        # إضافة scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.tree.bind('<Double-1>', self.edit_ingredient)
    
    def create_calculations(self):
        """إنشاء قسم الحسابات"""
        calc_frame = ttk.LabelFrame(self.root, text="الحسابات النهائية", padding="15")
        calc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # المتغيرات
        self.total_cost_var = tk.StringVar(value="0.00")
        self.cost_per_serving_var = tk.StringVar(value="0.00")
        
        # التكلفة الإجمالية
        tk.Label(calc_frame, text="💰 التكلفة الإجمالية للوجبة:", 
                font=self.arabic_font_bold).grid(row=0, column=0, sticky=tk.W, padx=5)
        tk.Label(calc_frame, textvariable=self.total_cost_var, 
                font=("Arial", 14, "bold"), fg="blue").grid(row=0, column=1, sticky=tk.W, padx=10)
        tk.Label(calc_frame, text="ريال", font=self.arabic_font).grid(row=0, column=2, sticky=tk.W)
        
        # تكلفة الحصة الواحدة
        tk.Label(calc_frame, text="🍽️ تكلفة الحصة الواحدة:", 
                font=self.arabic_font_bold).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(calc_frame, textvariable=self.cost_per_serving_var, 
                font=("Arial", 14, "bold"), fg="green").grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(calc_frame, text="ريال", font=self.arabic_font).grid(row=1, column=2, sticky=tk.W, pady=5)
    
    def create_buttons(self):
        """إنشاء الأزرار"""
        buttons_frame = tk.Frame(self.root, bg='#f0f8ff')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # أزرار التحكم
        tk.Button(buttons_frame, text="🔄 إعادة حساب", font=self.arabic_font_bold,
                 bg='#3498db', fg='white', command=self.calculate_totals).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="➕ إضافة مكون", font=self.arabic_font_bold,
                 bg='#27ae60', fg='white', command=self.add_ingredient).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🗑️ حذف مكون", font=self.arabic_font_bold,
                 bg='#e74c3c', fg='white', command=self.delete_ingredient).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📊 تقرير مفصل", font=self.arabic_font_bold,
                 bg='#9b59b6', fg='white', command=self.show_detailed_report).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="❌ خروج", font=self.arabic_font_bold,
                 bg='#95a5a6', fg='white', command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def load_sample_data(self):
        """تحميل بيانات تجريبية لبرياني الدجاج"""
        sample_ingredients = [
            ("أرز بسمتي", 0.300, "كيلو", 12.50),
            ("دجاج طازج", 0.400, "كيلو", 25.00),
            ("بصل أحمر", 0.150, "كيلو", 3.50),
            ("طماطم", 0.100, "كيلو", 4.00),
            ("لبن زبادي", 0.100, "كيلو", 8.00),
            ("بهارات البرياني", 0.020, "كيلو", 45.00),
            ("زيت دوار الشمس", 0.050, "لتر", 8.50),
            ("ملح طعام", 0.010, "كيلو", 2.00),
            ("ثوم", 0.030, "كيلو", 15.00),
            ("زنجبيل", 0.020, "كيلو", 20.00),
            ("زعفران", 2.000, "جرام", 0.50),
            ("لوز مقشر", 0.020, "كيلو", 35.00),
            ("زبيب ذهبي", 0.015, "كيلو", 18.00),
        ]
        
        # إضافة البيانات للجدول
        for ingredient, quantity, unit, unit_price in sample_ingredients:
            total_cost = quantity * unit_price
            self.tree.insert("", "end", values=(
                ingredient,
                f"{quantity:.3f}",
                unit,
                f"{unit_price:.3f}",
                f"{total_cost:.3f}",
                "0.0%"
            ))
        
        self.calculate_totals()
    
    def calculate_totals(self):
        """حساب الإجماليات والنسب المئوية"""
        total_cost = Decimal('0.00')
        
        # حساب التكلفة الإجمالية
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            cost = Decimal(str(values[4]))
            total_cost += cost
        
        # حساب النسب المئوية وتحديث الجدول
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
        dialog = IngredientDialog(self.root, "إضافة مكون جديد")
        result = dialog.show()
        
        if result:
            ingredient_name, quantity, unit, unit_price = result
            total_cost = quantity * unit_price
            
            self.tree.insert("", "end", values=(
                ingredient_name,
                f"{quantity:.3f}",
                unit,
                f"{unit_price:.3f}",
                f"{total_cost:.3f}",
                "0.0%"
            ))
            
            self.calculate_totals()
    
    def edit_ingredient(self, event):
        """تعديل مكون موجود"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        
        dialog = IngredientDialog(self.root, "تعديل مكون", values)
        result = dialog.show()
        
        if result:
            ingredient_name, quantity, unit, unit_price = result
            total_cost = quantity * unit_price
            
            self.tree.item(item, values=(
                ingredient_name,
                f"{quantity:.3f}",
                unit,
                f"{unit_price:.3f}",
                f"{total_cost:.3f}",
                "0.0%"
            ))
            
            self.calculate_totals()
    
    def delete_ingredient(self):
        """حذف مكون"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مكون للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذا المكون؟"):
            self.tree.delete(selected[0])
            self.calculate_totals()
    
    def show_detailed_report(self):
        """عرض تقرير مفصل"""
        report_window = tk.Toplevel(self.root)
        report_window.title("تقرير تفصيلي لتكلفة الوجبة")
        report_window.geometry("600x500")
        
        # إنشاء النص
        text_widget = tk.Text(report_window, font=self.arabic_font, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء التقرير
        report = f"""
🍽️ تقرير تفصيلي لتكلفة الوجبة
{'='*50}

📋 معلومات الوجبة:
• اسم الوجبة: {self.meal_name_var.get()}
• عدد الحصص: {self.servings_var.get()} حصة
• التكلفة الإجمالية: {self.total_cost_var.get()} ريال
• تكلفة الحصة الواحدة: {self.cost_per_serving_var.get()} ريال

📊 تفصيل المكونات:
{'='*50}
"""
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            report += f"""
🔸 {values[0]}:
   الكمية: {values[1]} {values[2]}
   سعر الوحدة: {values[3]} ريال
   التكلفة الجزئية: {values[4]} ريال
   النسبة المئوية: {values[5]}
"""
        
        report += f"""
{'='*50}
💡 ملاحظات:
• جميع الأسعار بالريال السعودي
• النسب المئوية محسوبة من إجمالي تكلفة المكونات
• يمكن تعديل الكميات والأسعار حسب الحاجة
• لا تشمل التكاليف الإضافية (عمالة، كهرباء، إيجار)

📈 توصيات التسعير:
• التكلفة الحالية: {self.cost_per_serving_var.get()} ريال
• مع هامش ربح 30%: {float(self.cost_per_serving_var.get()) * 1.3:.2f} ريال
• مع هامش ربح 50%: {float(self.cost_per_serving_var.get()) * 1.5:.2f} ريال
"""
        
        text_widget.insert(tk.END, report)
        text_widget.configure(state=tk.DISABLED)
        
        # زر الإغلاق
        tk.Button(report_window, text="إغلاق", command=report_window.destroy).pack(pady=10)

class IngredientDialog:
    """نافذة إضافة/تعديل مكون"""
    
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
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # اسم المكون
        tk.Label(main_frame, text="اسم المكون:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ingredient_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.ingredient_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # الكمية
        tk.Label(main_frame, text="الكمية:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0.000")
        tk.Entry(main_frame, textvariable=self.quantity_var, width=30).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # الوحدة
        tk.Label(main_frame, text="الوحدة:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(main_frame, textvariable=self.unit_var, width=27)
        unit_combo['values'] = ('كيلو', 'جرام', 'لتر', 'مليلتر', 'قطعة', 'ملعقة', 'كوب')
        unit_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # سعر الوحدة
        tk.Label(main_frame, text="سعر الوحدة (ريال):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.unit_price_var = tk.StringVar(value="0.000")
        tk.Entry(main_frame, textvariable=self.unit_price_var, width=30).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # أزرار التحكم
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(buttons_frame, text="موافق", command=self.ok_clicked, bg='#27ae60', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="إلغاء", command=self.cancel_clicked, bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)
    
    def load_values(self):
        """تحميل القيم للتعديل"""
        if self.values:
            self.ingredient_var.set(self.values[0])
            self.quantity_var.set(self.values[1])
            self.unit_var.set(self.values[2])
            self.unit_price_var.set(self.values[3])
    
    def ok_clicked(self):
        """عند الضغط على موافق"""
        try:
            ingredient_name = self.ingredient_var.get().strip()
            quantity = float(self.quantity_var.get())
            unit = self.unit_var.get().strip()
            unit_price = float(self.unit_price_var.get())
            
            if not ingredient_name or not unit or quantity <= 0 or unit_price <= 0:
                messagebox.showwarning("تحذير", "يرجى إدخال جميع البيانات بشكل صحيح")
                return
            
            self.result = (ingredient_name, quantity, unit, unit_price)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للكمية والسعر")
    
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
    app = SimpleCostingDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
