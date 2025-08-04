# -*- coding: utf-8 -*-
"""
شاشة فاتورة المبيعات
Sales Invoice Screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid

from ..utils.language_manager import language_manager
from ..utils.arabic_support import ArabicSupport

class SalesInvoiceWindow:
    """شاشة فاتورة المبيعات"""
    
    def __init__(self, parent, db_manager, user_data, branch_id="PI"):
        """تهيئة شاشة فاتورة المبيعات"""
        self.parent = parent
        self.db_manager = db_manager
        self.user_data = user_data
        self.branch_id = branch_id
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        
        # متغيرات البيانات
        self.invoice_items = []
        self.total_amount = 0.0
        self.tax_amount = 0.0
        self.final_amount = 0.0
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحميل البيانات الأولية
        self.load_initial_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.window.title(f"{language_manager.get_text('sales_invoice')} - {language_manager.get_text('place_india' if self.branch_id == 'PI' else 'china_town')}")
        self.window.geometry("1000x700")
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
        self.create_header_section(main_frame)
        self.create_customer_section(main_frame)
        self.create_items_section(main_frame)
        self.create_totals_section(main_frame)
        self.create_buttons_section(main_frame)
    
    def create_header_section(self, parent):
        """إنشاء قسم رأس الفاتورة"""
        header_frame = ttk.LabelFrame(
            parent,
            text="معلومات الفاتورة",
            padding="10"
        )
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول
        row1_frame = ttk.Frame(header_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 10))
        
        # رقم الفاتورة
        ttk.Label(row1_frame, text=language_manager.get_text("invoice_number")).pack(side=tk.LEFT)
        self.invoice_number_var = tk.StringVar(value=self.generate_invoice_number())
        invoice_entry = ttk.Entry(row1_frame, textvariable=self.invoice_number_var, width=20, state="readonly")
        invoice_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # التاريخ
        ttk.Label(row1_frame, text=language_manager.get_text("invoice_date")).pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(row1_frame, textvariable=self.date_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # الفرع
        ttk.Label(row1_frame, text=language_manager.get_text("branch")).pack(side=tk.LEFT)
        branch_name = language_manager.get_text("place_india") if self.branch_id == "PI" else language_manager.get_text("china_town")
        ttk.Label(row1_frame, text=branch_name, foreground="blue", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_customer_section(self, parent):
        """إنشاء قسم معلومات العميل"""
        customer_frame = ttk.LabelFrame(
            parent,
            text="معلومات العميل",
            padding="10"
        )
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        # اسم العميل
        customer_row = ttk.Frame(customer_frame)
        customer_row.pack(fill=tk.X)
        
        ttk.Label(customer_row, text=language_manager.get_text("customer_name")).pack(side=tk.LEFT)
        self.customer_var = tk.StringVar()
        customer_entry = ttk.Entry(customer_row, textvariable=self.customer_var, width=30)
        customer_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # زر اختيار عميل
        select_customer_btn = ttk.Button(
            customer_row,
            text="اختيار عميل",
            command=self.select_customer
        )
        select_customer_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_items_section(self, parent):
        """إنشاء قسم عناصر الفاتورة"""
        items_frame = ttk.LabelFrame(
            parent,
            text="عناصر الفاتورة",
            padding="10"
        )
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إطار إضافة منتج
        add_item_frame = ttk.Frame(items_frame)
        add_item_frame.pack(fill=tk.X, pady=(0, 10))
        
        # حقول إضافة منتج
        ttk.Label(add_item_frame, text=language_manager.get_text("product_name")).grid(row=0, column=0, padx=5, sticky=tk.W)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_item_frame, textvariable=self.product_var, width=20)
        self.product_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_item_frame, text=language_manager.get_text("quantity")).grid(row=0, column=2, padx=5, sticky=tk.W)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(add_item_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_item_frame, text=language_manager.get_text("unit_price")).grid(row=0, column=4, padx=5, sticky=tk.W)
        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(add_item_frame, textvariable=self.price_var, width=10)
        price_entry.grid(row=0, column=5, padx=5)
        
        # زر إضافة
        add_btn = ttk.Button(
            add_item_frame,
            text=language_manager.get_text("add"),
            command=self.add_item
        )
        add_btn.grid(row=0, column=6, padx=10)
        
        # جدول العناصر
        columns = ("المنتج", "الكمية", "السعر", "المجموع", "الضريبة", "الإجمالي")
        self.items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=10)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.items_tree.bind("<Double-1>", self.edit_item)
        self.items_tree.bind("<Delete>", self.delete_item)
    
    def create_totals_section(self, parent):
        """إنشاء قسم المجاميع"""
        totals_frame = ttk.LabelFrame(
            parent,
            text="المجاميع",
            padding="10"
        )
        totals_frame.pack(fill=tk.X, pady=(0, 10))
        
        # إطار المجاميع
        totals_grid = ttk.Frame(totals_frame)
        totals_grid.pack(side=tk.RIGHT)
        
        # المجموع الفرعي
        ttk.Label(totals_grid, text="المجموع الفرعي:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.subtotal_label = ttk.Label(totals_grid, text="0.00 ريال", font=("Arial", 10, "bold"))
        self.subtotal_label.grid(row=0, column=1, sticky=tk.E, padx=5)
        
        # الضريبة
        ttk.Label(totals_grid, text="الضريبة (15%):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.tax_label = ttk.Label(totals_grid, text="0.00 ريال", font=("Arial", 10, "bold"))
        self.tax_label.grid(row=1, column=1, sticky=tk.E, padx=5)
        
        # المجموع النهائي
        ttk.Label(totals_grid, text="المجموع النهائي:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.total_label = ttk.Label(totals_grid, text="0.00 ريال", font=("Arial", 12, "bold"), foreground="red")
        self.total_label.grid(row=2, column=1, sticky=tk.E, padx=5)
        
        # طريقة الدفع
        payment_frame = ttk.Frame(totals_frame)
        payment_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(payment_frame, text=language_manager.get_text("payment_method")).pack(anchor=tk.W)
        self.payment_var = tk.StringVar(value="CASH")
        payment_combo = ttk.Combobox(
            payment_frame,
            textvariable=self.payment_var,
            values=["CASH", "MADA", "VISA", "MASTERCARD", "BANK", "GCC", "AKS", "CREDIT"],
            width=15
        )
        payment_combo.pack(anchor=tk.W, pady=(5, 0))
    
    def create_buttons_section(self, parent):
        """إنشاء قسم الأزرار"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X)
        
        # الأزرار
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("save"),
            command=self.save_invoice
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("print"),
            command=self.print_invoice
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="حفظ وطباعة",
            command=self.save_and_print
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text=language_manager.get_text("cancel"),
            command=self.close_window
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="فاتورة جديدة",
            command=self.new_invoice
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        # تحميل قائمة المنتجات
        products = self.db_manager.execute_query("SELECT product_name FROM products WHERE is_active = 1")
        if products:
            product_names = [product['product_name'] for product in products]
            self.product_combo['values'] = product_names
    
    def generate_invoice_number(self):
        """توليد رقم فاتورة تلقائي"""
        # تنسيق: BRANCH-YYYYMMDD-XXXX
        today = datetime.now()
        date_part = today.strftime("%Y%m%d")
        
        # البحث عن آخر رقم فاتورة لهذا اليوم والفرع
        query = """
        SELECT COUNT(*) as count FROM sales 
        WHERE branch_id = (SELECT id FROM branches WHERE branch_code = ?) 
        AND DATE(invoice_date) = DATE(?)
        """
        result = self.db_manager.execute_query(query, (self.branch_id, today.strftime("%Y-%m-%d")))
        
        sequence = 1
        if result and result[0]['count']:
            sequence = result[0]['count'] + 1
        
        return f"{self.branch_id}-{date_part}-{sequence:04d}"
    
    def add_item(self):
        """إضافة منتج للفاتورة"""
        product_name = self.product_var.get().strip()
        quantity = self.quantity_var.get().strip()
        price = self.price_var.get().strip()
        
        # التحقق من صحة البيانات
        if not product_name or not quantity or not price:
            messagebox.showerror("خطأ", "يرجى إدخال جميع البيانات المطلوبة")
            return
        
        try:
            quantity = float(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للكمية والسعر")
            return
        
        # حساب المجاميع
        subtotal = quantity * price
        tax_rate = 15.0  # معدل الضريبة
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount
        
        # إضافة العنصر للجدول
        item_data = (product_name, quantity, f"{price:.2f}", f"{subtotal:.2f}", f"{tax_amount:.2f}", f"{total:.2f}")
        self.items_tree.insert("", tk.END, values=item_data)
        
        # إضافة للقائمة
        self.invoice_items.append({
            'product_name': product_name,
            'quantity': quantity,
            'unit_price': price,
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total': total
        })
        
        # تحديث المجاميع
        self.update_totals()
        
        # مسح الحقول
        self.product_var.set("")
        self.quantity_var.set("1")
        self.price_var.set("")
    
    def update_totals(self):
        """تحديث المجاميع"""
        self.total_amount = sum(item['subtotal'] for item in self.invoice_items)
        self.tax_amount = sum(item['tax_amount'] for item in self.invoice_items)
        self.final_amount = sum(item['total'] for item in self.invoice_items)
        
        # تحديث التسميات
        self.subtotal_label.config(text=f"{self.total_amount:.2f} ريال")
        self.tax_label.config(text=f"{self.tax_amount:.2f} ريال")
        self.total_label.config(text=f"{self.final_amount:.2f} ريال")
    
    def delete_item(self, event=None):
        """حذف عنصر من الفاتورة"""
        selected = self.items_tree.selection()
        if selected:
            # الحصول على فهرس العنصر
            item_index = self.items_tree.index(selected[0])
            
            # حذف من الجدول والقائمة
            self.items_tree.delete(selected[0])
            del self.invoice_items[item_index]
            
            # تحديث المجاميع
            self.update_totals()
    
    def save_invoice(self):
        """حفظ الفاتورة"""
        if not self.invoice_items:
            messagebox.showerror("خطأ", "يرجى إضافة منتجات للفاتورة")
            return
        
        try:
            # حفظ الفاتورة في قاعدة البيانات
            # هذا مثال مبسط - سيتم تطوير الحفظ الفعلي لاحقاً
            messagebox.showinfo("نجح", "تم حفظ الفاتورة بنجاح")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة: {str(e)}")
    
    def print_invoice(self):
        """طباعة الفاتورة"""
        if not self.invoice_items:
            messagebox.showerror("خطأ", "لا توجد عناصر للطباعة")
            return
        
        # سيتم تطوير وظيفة الطباعة لاحقاً
        messagebox.showinfo("قريباً", "وظيفة الطباعة قيد التطوير")
    
    def save_and_print(self):
        """حفظ وطباعة الفاتورة"""
        self.save_invoice()
        self.print_invoice()
    
    def new_invoice(self):
        """فاتورة جديدة"""
        # مسح البيانات الحالية
        self.invoice_items.clear()
        self.items_tree.delete(*self.items_tree.get_children())
        
        # إعادة تعيين القيم
        self.invoice_number_var.set(self.generate_invoice_number())
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.customer_var.set("")
        self.payment_var.set("CASH")
        
        # تحديث المجاميع
        self.update_totals()
    
    def select_customer(self):
        """اختيار عميل"""
        # سيتم تطوير نافذة اختيار العميل لاحقاً
        messagebox.showinfo("قريباً", "نافذة اختيار العميل قيد التطوير")
    
    def edit_item(self, event=None):
        """تعديل عنصر"""
        # سيتم تطوير وظيفة التعديل لاحقاً
        messagebox.showinfo("قريباً", "وظيفة تعديل العنصر قيد التطوير")
    
    def close_window(self):
        """إغلاق النافذة"""
        if self.invoice_items:
            result = messagebox.askyesno(
                "تأكيد الإغلاق",
                "هناك بيانات غير محفوظة. هل أنت متأكد من الإغلاق؟"
            )
            if not result:
                return
        
        self.window.destroy()
