# -*- coding: utf-8 -*-
"""
شاشة إدارة المنتجات
Products Management Screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from ..utils.language_manager import language_manager
from ..utils.arabic_support import ArabicSupport

class ProductsManagementWindow:
    """شاشة إدارة المنتجات"""
    
    def __init__(self, parent, db_manager, user_data):
        """تهيئة شاشة إدارة المنتجات"""
        self.parent = parent
        self.db_manager = db_manager
        self.user_data = user_data
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        
        # متغيرات البيانات
        self.selected_product_id = None
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحميل البيانات
        self.load_products()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.window.title("إدارة المنتجات - Products Management")
        self.window.geometry("1000x600")
        self.window.resizable(True, True)
        
        # تطبيق الدعم العربي
        ArabicSupport.setup_arabic_support(self.window)
        
        # توسيط النافذة
        self.center_window()
    
    def center_window(self):
        """توسيط النافذة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء أقسام الواجهة
        self.create_toolbar(main_frame)
        self.create_form_section(main_frame)
        self.create_products_list(main_frame)
    
    def create_toolbar(self, parent):
        """إنشاء شريط الأدوات"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # عنوان الشاشة
        title_label = ArabicSupport.create_arabic_label(
            toolbar_frame,
            "إدارة المنتجات",
            font=ArabicSupport.get_arabic_font(16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(toolbar_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("add"),
            command=self.add_product
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("edit"),
            command=self.edit_product
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("delete"),
            command=self.delete_product
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("refresh"),
            command=self.load_products
        ).pack(side=tk.LEFT, padx=2)
    
    def create_form_section(self, parent):
        """إنشاء قسم النموذج"""
        form_frame = ttk.LabelFrame(
            parent,
            text="بيانات المنتج",
            padding="10"
        )
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول
        row1_frame = ttk.Frame(form_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 10))
        
        # رمز المنتج
        ttk.Label(row1_frame, text="رمز المنتج:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.product_code_var = tk.StringVar()
        ttk.Entry(row1_frame, textvariable=self.product_code_var, width=15).grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # اسم المنتج
        ttk.Label(row1_frame, text="اسم المنتج:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.product_name_var = tk.StringVar()
        ttk.Entry(row1_frame, textvariable=self.product_name_var, width=25).grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # الفئة
        ttk.Label(row1_frame, text="الفئة:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            row1_frame,
            textvariable=self.category_var,
            values=["إلكترونيات", "ملابس", "أغذية", "مستحضرات تجميل", "أخرى"],
            width=15
        )
        category_combo.grid(row=0, column=5, padx=5, sticky=tk.W)
        
        # الصف الثاني
        row2_frame = ttk.Frame(form_frame)
        row2_frame.pack(fill=tk.X, pady=(0, 10))
        
        # تكلفة الوحدة
        ttk.Label(row2_frame, text="تكلفة الوحدة:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.unit_cost_var = tk.StringVar(value="0.00")
        ttk.Entry(row2_frame, textvariable=self.unit_cost_var, width=15).grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # سعر البيع
        ttk.Label(row2_frame, text="سعر البيع:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.selling_price_var = tk.StringVar(value="0.00")
        ttk.Entry(row2_frame, textvariable=self.selling_price_var, width=15).grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # وحدة القياس
        ttk.Label(row2_frame, text="وحدة القياس:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.unit_type_var = tk.StringVar(value="قطعة")
        unit_combo = ttk.Combobox(
            row2_frame,
            textvariable=self.unit_type_var,
            values=["قطعة", "كيلو", "لتر", "متر", "علبة", "كرتون"],
            width=10
        )
        unit_combo.grid(row=0, column=5, padx=5, sticky=tk.W)
        
        # الصف الثالث
        row3_frame = ttk.Frame(form_frame)
        row3_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الحد الأدنى للمخزون
        ttk.Label(row3_frame, text="الحد الأدنى للمخزون:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.min_stock_var = tk.StringVar(value="0")
        ttk.Entry(row3_frame, textvariable=self.min_stock_var, width=15).grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # الكمية الحالية
        ttk.Label(row3_frame, text="الكمية الحالية:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.current_stock_var = tk.StringVar(value="0")
        ttk.Entry(row3_frame, textvariable=self.current_stock_var, width=15).grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # حالة المنتج
        self.is_active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row3_frame, text="منتج نشط", variable=self.is_active_var).grid(row=0, column=4, padx=5, sticky=tk.W)
        
        # الوصف
        ttk.Label(form_frame, text="الوصف:").pack(anchor=tk.W, pady=(5, 0))
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(form_frame, textvariable=self.description_var, width=80)
        description_entry.pack(fill=tk.X, pady=(5, 10))
        
        # أزرار النموذج
        form_buttons_frame = ttk.Frame(form_frame)
        form_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(
            form_buttons_frame,
            text=language_manager.get_text("save"),
            command=self.save_product
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            form_buttons_frame,
            text="مسح الحقول",
            command=self.clear_form
        ).pack(side=tk.LEFT, padx=5)
    
    def create_products_list(self, parent):
        """إنشاء قائمة المنتجات"""
        list_frame = ttk.LabelFrame(
            parent,
            text="قائمة المنتجات",
            padding="10"
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار البحث
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text=language_manager.get_text("search")).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        search_entry.bind('<KeyRelease>', self.search_products)
        
        ttk.Button(
            search_frame,
            text="بحث",
            command=self.search_products
        ).pack(side=tk.LEFT)
        
        # جدول المنتجات
        columns = ("الرمز", "الاسم", "الفئة", "التكلفة", "سعر البيع", "المخزون", "الحالة")
        self.products_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar_v = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        scrollbar_h = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # تخطيط الجدول
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # ربط الأحداث
        self.products_tree.bind("<Double-1>", self.on_product_select)
        self.products_tree.bind("<<TreeviewSelect>>", self.on_product_select)
    
    def load_products(self):
        """تحميل قائمة المنتجات"""
        # مسح البيانات الحالية
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # جلب المنتجات من قاعدة البيانات
        products = self.db_manager.execute_query("""
            SELECT id, product_code, product_name, category, unit_cost, 
                   selling_price, current_stock, is_active
            FROM products
            ORDER BY product_name
        """)
        
        if products:
            for product in products:
                status = "نشط" if product['is_active'] else "غير نشط"
                values = (
                    product['product_code'],
                    product['product_name'],
                    product['category'] or "",
                    f"{product['unit_cost']:.2f}",
                    f"{product['selling_price']:.2f}",
                    product['current_stock'],
                    status
                )
                item = self.products_tree.insert("", tk.END, values=values)
                # حفظ معرف المنتج مع العنصر
                self.products_tree.set(item, "#0", product['id'])
    
    def search_products(self, event=None):
        """البحث في المنتجات"""
        search_term = self.search_var.get().strip()
        
        # مسح البيانات الحالية
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # تحديد استعلام البحث
        if search_term:
            query = """
                SELECT id, product_code, product_name, category, unit_cost, 
                       selling_price, current_stock, is_active
                FROM products
                WHERE product_name LIKE ? OR product_code LIKE ? OR category LIKE ?
                ORDER BY product_name
            """
            search_pattern = f"%{search_term}%"
            products = self.db_manager.execute_query(query, (search_pattern, search_pattern, search_pattern))
        else:
            # إذا كان البحث فارغاً، عرض جميع المنتجات
            self.load_products()
            return
        
        # عرض نتائج البحث
        if products:
            for product in products:
                status = "نشط" if product['is_active'] else "غير نشط"
                values = (
                    product['product_code'],
                    product['product_name'],
                    product['category'] or "",
                    f"{product['unit_cost']:.2f}",
                    f"{product['selling_price']:.2f}",
                    product['current_stock'],
                    status
                )
                item = self.products_tree.insert("", tk.END, values=values)
                self.products_tree.set(item, "#0", product['id'])
    
    def on_product_select(self, event=None):
        """معالج اختيار منتج"""
        selected = self.products_tree.selection()
        if selected:
            item = selected[0]
            product_id = self.products_tree.set(item, "#0")
            
            # جلب بيانات المنتج
            product = self.db_manager.execute_query(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )
            
            if product:
                product = product[0]
                self.selected_product_id = product['id']
                
                # ملء النموذج
                self.product_code_var.set(product['product_code'])
                self.product_name_var.set(product['product_name'])
                self.category_var.set(product['category'] or "")
                self.unit_cost_var.set(str(product['unit_cost']))
                self.selling_price_var.set(str(product['selling_price']))
                self.unit_type_var.set(product['unit_type'])
                self.min_stock_var.set(str(product['min_stock_level']))
                self.current_stock_var.set(str(product['current_stock']))
                self.is_active_var.set(bool(product['is_active']))
                self.description_var.set(product['description'] or "")
    
    def clear_form(self):
        """مسح النموذج"""
        self.selected_product_id = None
        self.product_code_var.set("")
        self.product_name_var.set("")
        self.category_var.set("")
        self.unit_cost_var.set("0.00")
        self.selling_price_var.set("0.00")
        self.unit_type_var.set("قطعة")
        self.min_stock_var.set("0")
        self.current_stock_var.set("0")
        self.is_active_var.set(True)
        self.description_var.set("")
    
    def save_product(self):
        """حفظ المنتج"""
        # التحقق من صحة البيانات
        if not self.product_code_var.get().strip() or not self.product_name_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال رمز واسم المنتج")
            return
        
        try:
            unit_cost = float(self.unit_cost_var.get())
            selling_price = float(self.selling_price_var.get())
            min_stock = int(self.min_stock_var.get())
            current_stock = int(self.current_stock_var.get())
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم رقمية صحيحة")
            return
        
        # بيانات المنتج
        product_data = (
            self.product_code_var.get().strip(),
            self.product_name_var.get().strip(),
            self.description_var.get().strip(),
            unit_cost,
            selling_price,
            self.category_var.get().strip(),
            self.unit_type_var.get(),
            min_stock,
            current_stock,
            self.is_active_var.get()
        )
        
        try:
            if self.selected_product_id:
                # تحديث منتج موجود
                query = """
                    UPDATE products SET
                        product_code = ?, product_name = ?, description = ?,
                        unit_cost = ?, selling_price = ?, category = ?,
                        unit_type = ?, min_stock_level = ?, current_stock = ?,
                        is_active = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                self.db_manager.execute_query(query, product_data + (self.selected_product_id,))
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح")
            else:
                # إضافة منتج جديد
                query = """
                    INSERT INTO products (
                        product_code, product_name, description, unit_cost,
                        selling_price, category, unit_type, min_stock_level,
                        current_stock, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                self.db_manager.execute_query(query, product_data)
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح")
            
            # تحديث القائمة ومسح النموذج
            self.load_products()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ المنتج: {str(e)}")
    
    def add_product(self):
        """إضافة منتج جديد"""
        self.clear_form()
    
    def edit_product(self):
        """تعديل المنتج المحدد"""
        if not self.selected_product_id:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
    
    def delete_product(self):
        """حذف المنتج المحدد"""
        if not self.selected_product_id:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        result = messagebox.askyesno(
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا المنتج؟"
        )
        
        if result:
            try:
                self.db_manager.execute_query(
                    "DELETE FROM products WHERE id = ?",
                    (self.selected_product_id,)
                )
                messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
                self.load_products()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في حذف المنتج: {str(e)}")
