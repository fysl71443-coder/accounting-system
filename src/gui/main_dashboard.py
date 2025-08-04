# -*- coding: utf-8 -*-
"""
الشاشة الرئيسية - لوحة التحكم
Main Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime, timedelta

from ..utils.language_manager import language_manager
from ..utils.arabic_support import ArabicSupport

class MainDashboard:
    """الشاشة الرئيسية للبرنامج"""
    
    def __init__(self, parent, db_manager, user_data):
        """تهيئة الشاشة الرئيسية"""
        self.parent = parent
        self.db_manager = db_manager
        self.user_data = user_data
        
        # إعداد النافذة الرئيسية
        self.setup_main_window()
        
        # إنشاء القوائم
        self.create_menu_bar()
        
        # إنشاء شريط الأدوات
        self.create_toolbar()
        
        # إنشاء المحتوى الرئيسي
        self.create_main_content()
        
        # تحديث البيانات
        self.refresh_dashboard()
    
    def setup_main_window(self):
        """إعداد النافذة الرئيسية"""
        self.parent.title(f"{language_manager.get_text('dashboard_title')} - {self.user_data['full_name']}")
        self.parent.geometry("1200x800")
        self.parent.state('zoomed')  # تكبير النافذة
        
        # تطبيق الدعم العربي
        ArabicSupport.setup_arabic_support(self.parent)
    
    def create_menu_bar(self):
        """إنشاء شريط القوائم"""
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # قائمة المبيعات
        sales_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_text("sales"),
            menu=sales_menu
        )
        sales_menu.add_command(
            label="فاتورة مبيعات جديدة",
            command=self.new_sales_invoice
        )
        sales_menu.add_command(
            label="عرض فواتير المبيعات",
            command=self.view_sales_invoices
        )
        sales_menu.add_separator()
        sales_menu.add_command(
            label=f"فرع {language_manager.get_text('place_india')}",
            command=lambda: self.switch_branch("PI")
        )
        sales_menu.add_command(
            label=f"فرع {language_manager.get_text('china_town')}",
            command=lambda: self.switch_branch("CT")
        )
        
        # قائمة المشتريات
        purchases_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_text("purchases"),
            menu=purchases_menu
        )
        purchases_menu.add_command(
            label="فاتورة مشتريات جديدة",
            command=self.new_purchase_invoice
        )
        purchases_menu.add_command(
            label="عرض فواتير المشتريات",
            command=self.view_purchase_invoices
        )
        
        # قائمة المخزون
        inventory_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_text("inventory"),
            menu=inventory_menu
        )
        inventory_menu.add_command(
            label=language_manager.get_text("products"),
            command=self.manage_products
        )
        inventory_menu.add_command(
            label="حركة المخزون",
            command=self.view_inventory_movement
        )
        
        # قائمة التقارير
        reports_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_text("reports"),
            menu=reports_menu
        )
        reports_menu.add_command(
            label=language_manager.get_text("sales_report"),
            command=self.sales_report
        )
        reports_menu.add_command(
            label=language_manager.get_text("purchase_report"),
            command=self.purchase_report
        )
        reports_menu.add_command(
            label=language_manager.get_text("financial_report"),
            command=self.financial_report
        )
        
        # قائمة الإعدادات
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label=language_manager.get_text("settings"),
            menu=settings_menu
        )
        settings_menu.add_command(
            label="إعدادات الشركة",
            command=self.company_settings
        )
        settings_menu.add_command(
            label="إدارة المستخدمين",
            command=self.manage_users
        )
        settings_menu.add_separator()
        settings_menu.add_command(
            label=language_manager.get_text("logout"),
            command=self.logout
        )
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        self.toolbar = ttk.Frame(self.parent)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # معلومات المستخدم والفرع
        user_frame = ttk.Frame(self.toolbar)
        user_frame.pack(side=tk.RIGHT if language_manager.is_rtl() else tk.LEFT)
        
        # اسم المستخدم
        user_label = ArabicSupport.create_arabic_label(
            user_frame,
            f"{language_manager.get_text('welcome')} {self.user_data['full_name']}",
            font=ArabicSupport.get_arabic_font(10, "bold")
        )
        user_label.pack(side=tk.TOP)
        
        # الفرع الحالي
        self.current_branch = "PI"  # الفرع الافتراضي
        self.branch_label = ArabicSupport.create_arabic_label(
            user_frame,
            f"{language_manager.get_text('branch')}: {language_manager.get_text('place_india')}",
            foreground="blue"
        )
        self.branch_label.pack(side=tk.TOP)
        
        # أزرار سريعة
        buttons_frame = ttk.Frame(self.toolbar)
        buttons_frame.pack(side=tk.LEFT if language_manager.is_rtl() else tk.RIGHT)
        
        # زر فاتورة مبيعات جديدة
        new_sale_btn = ArabicSupport.create_arabic_button(
            buttons_frame,
            "فاتورة مبيعات",
            command=self.new_sales_invoice
        )
        new_sale_btn.pack(side=tk.LEFT, padx=2)
        
        # زر فاتورة مشتريات جديدة
        new_purchase_btn = ArabicSupport.create_arabic_button(
            buttons_frame,
            "فاتورة مشتريات",
            command=self.new_purchase_invoice
        )
        new_purchase_btn.pack(side=tk.LEFT, padx=2)
        
        # زر تحديث
        refresh_btn = ArabicSupport.create_arabic_button(
            buttons_frame,
            language_manager.get_text("refresh"),
            command=self.refresh_dashboard
        )
        refresh_btn.pack(side=tk.LEFT, padx=2)
    
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        # إطار رئيسي مع تمرير
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # إطار الملخصات العلوي
        self.create_summary_cards(main_frame)
        
        # إطار المحتوى السفلي (رسومات بيانية + تنبيهات)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # الرسومات البيانية (يسار)
        self.create_charts_section(content_frame)
        
        # التنبيهات والإشعارات (يمين)
        self.create_alerts_section(content_frame)
    
    def create_summary_cards(self, parent):
        """إنشاء بطاقات الملخصات"""
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # بطاقة المبيعات اليومية
        self.daily_sales_card = self.create_summary_card(
            summary_frame,
            language_manager.get_text("daily_sales"),
            "0.00 ريال",
            "lightblue"
        )
        self.daily_sales_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # بطاقة المبيعات الشهرية
        self.monthly_sales_card = self.create_summary_card(
            summary_frame,
            language_manager.get_text("monthly_sales"),
            "0.00 ريال",
            "lightgreen"
        )
        self.monthly_sales_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # بطاقة إجمالي الإيرادات
        self.revenue_card = self.create_summary_card(
            summary_frame,
            language_manager.get_text("total_revenue"),
            "0.00 ريال",
            "lightyellow"
        )
        self.revenue_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # بطاقة صافي الربح
        self.profit_card = self.create_summary_card(
            summary_frame,
            language_manager.get_text("net_profit"),
            "0.00 ريال",
            "lightcoral"
        )
        self.profit_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    def create_summary_card(self, parent, title, value, color):
        """إنشاء بطاقة ملخص"""
        card = ttk.LabelFrame(parent, text=title, padding="10")
        
        value_label = ArabicSupport.create_arabic_label(
            card,
            value,
            font=ArabicSupport.get_arabic_font(14, "bold")
        )
        value_label.pack()
        
        return card
    
    def create_charts_section(self, parent):
        """إنشاء قسم الرسومات البيانية"""
        charts_frame = ttk.LabelFrame(
            parent,
            text="الرسومات البيانية",
            padding="10"
        )
        charts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # إنشاء رسم بياني للمبيعات
        self.create_sales_chart(charts_frame)
    
    def create_alerts_section(self, parent):
        """إنشاء قسم التنبيهات"""
        alerts_frame = ttk.LabelFrame(
            parent,
            text=language_manager.get_text("low_stock_alerts"),
            padding="10"
        )
        alerts_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        alerts_frame.configure(width=300)
        
        # قائمة التنبيهات
        self.alerts_listbox = tk.Listbox(alerts_frame, height=15)
        self.alerts_listbox.pack(fill=tk.BOTH, expand=True)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.alerts_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.alerts_listbox.yview)
    
    def create_sales_chart(self, parent):
        """إنشاء رسم بياني للمبيعات"""
        # إنشاء الرسم البياني
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # بيانات تجريبية
        dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
        sales = [1000, 1500, 1200, 1800, 2000, 1600, 2200]
        
        self.ax.plot(dates, sales, marker='o', linewidth=2, markersize=6)
        self.ax.set_title("مبيعات آخر 7 أيام", fontsize=12)
        self.ax.set_ylabel("المبلغ (ريال)")
        self.ax.grid(True, alpha=0.3)
        
        # تنسيق التواريخ
        self.fig.autofmt_xdate()
        
        # إضافة الرسم البياني إلى الواجهة
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def refresh_dashboard(self):
        """تحديث بيانات لوحة التحكم"""
        # تحديث الملخصات
        self.update_summary_cards()
        
        # تحديث التنبيهات
        self.update_alerts()
        
        # تحديث الرسومات البيانية
        self.update_charts()
    
    def update_summary_cards(self):
        """تحديث بطاقات الملخصات"""
        # هنا سيتم جلب البيانات الفعلية من قاعدة البيانات
        # مؤقتاً سنستخدم بيانات تجريبية
        pass
    
    def update_alerts(self):
        """تحديث التنبيهات"""
        # مسح التنبيهات الحالية
        self.alerts_listbox.delete(0, tk.END)
        
        # إضافة تنبيهات تجريبية
        alerts = [
            "منتج A - الكمية المتبقية: 5",
            "منتج B - الكمية المتبقية: 2",
            "منتج C - نفدت الكمية"
        ]
        
        for alert in alerts:
            self.alerts_listbox.insert(tk.END, alert)
    
    def update_charts(self):
        """تحديث الرسومات البيانية"""
        # سيتم تطوير هذه الوظيفة لاحقاً
        pass
    
    def switch_branch(self, branch_code):
        """تغيير الفرع"""
        self.current_branch = branch_code
        branch_name = language_manager.get_text("place_india") if branch_code == "PI" else language_manager.get_text("china_town")
        self.branch_label.config(text=f"{language_manager.get_text('branch')}: {branch_name}")
        
        # تحديث البيانات للفرع الجديد
        self.refresh_dashboard()
    
    # وظائف القوائم
    def new_sales_invoice(self):
        """فتح شاشة فاتورة مبيعات جديدة"""
        from .sales_invoice import SalesInvoiceWindow
        SalesInvoiceWindow(self.parent, self.db_manager, self.user_data, self.current_branch)
    
    def new_purchase_invoice(self):
        messagebox.showinfo("قريباً", "شاشة فاتورة المشتريات قيد التطوير")
    
    def view_sales_invoices(self):
        messagebox.showinfo("قريباً", "شاشة عرض فواتير المبيعات قيد التطوير")
    
    def view_purchase_invoices(self):
        messagebox.showinfo("قريباً", "شاشة عرض فواتير المشتريات قيد التطوير")
    
    def manage_products(self):
        """فتح شاشة إدارة المنتجات"""
        from .products_management import ProductsManagementWindow
        ProductsManagementWindow(self.parent, self.db_manager, self.user_data)
    
    def view_inventory_movement(self):
        messagebox.showinfo("قريباً", "شاشة حركة المخزون قيد التطوير")
    
    def sales_report(self):
        messagebox.showinfo("قريباً", "تقرير المبيعات قيد التطوير")
    
    def purchase_report(self):
        messagebox.showinfo("قريباً", "تقرير المشتريات قيد التطوير")
    
    def financial_report(self):
        messagebox.showinfo("قريباً", "التقرير المالي قيد التطوير")
    
    def company_settings(self):
        messagebox.showinfo("قريباً", "إعدادات الشركة قيد التطوير")
    
    def manage_users(self):
        messagebox.showinfo("قريباً", "إدارة المستخدمين قيد التطوير")
    
    def logout(self):
        """تسجيل الخروج"""
        result = messagebox.askyesno(
            "تسجيل الخروج",
            "هل أنت متأكد من تسجيل الخروج؟"
        )
        if result:
            self.parent.quit()
