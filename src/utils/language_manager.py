# -*- coding: utf-8 -*-
"""
مدير اللغات - دعم العربية والإنجليزية
Language Manager - Arabic and English Support
"""

import json
import os
from typing import Dict, Any

class LanguageManager:
    """مدير اللغات للبرنامج"""
    
    def __init__(self):
        """تهيئة مدير اللغات"""
        self.current_language = "ar"  # اللغة الافتراضية العربية
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """تحميل ترجمات اللغات"""
        self.translations = {
            "ar": {
                # شاشة تسجيل الدخول
                "login_title": "تسجيل الدخول - نظام المحاسبة",
                "username": "اسم المستخدم",
                "password": "كلمة المرور",
                "login": "دخول",
                "forgot_password": "نسيت كلمة المرور؟",
                "invalid_credentials": "اسم المستخدم أو كلمة المرور غير صحيحة",
                "login_success": "تم تسجيل الدخول بنجاح",
                
                # الشاشة الرئيسية
                "dashboard_title": "لوحة التحكم الرئيسية",
                "welcome": "مرحباً",
                "daily_sales": "المبيعات اليومية",
                "monthly_sales": "المبيعات الشهرية",
                "total_revenue": "إجمالي الإيرادات",
                "total_expenses": "إجمالي المصروفات",
                "net_profit": "صافي الربح",
                "low_stock_alerts": "تنبيهات المخزون المنخفض",
                
                # القوائم الرئيسية
                "sales": "المبيعات",
                "purchases": "المشتريات",
                "products": "الأصناف",
                "inventory": "المخزون",
                "suppliers": "الموردين",
                "customers": "العملاء",
                "employees": "الموظفين",
                "reports": "التقارير",
                "settings": "الإعدادات",
                "logout": "تسجيل الخروج",
                
                # الفروع
                "branches": "الفروع",
                "place_india": "PLACE INDIA",
                "china_town": "CHINA TOWN",
                "select_branch": "اختر الفرع",
                "branch": "الفرع",
                
                # فواتير المبيعات
                "sales_invoice": "فاتورة مبيعات",
                "invoice_number": "رقم الفاتورة",
                "invoice_date": "تاريخ الفاتورة",
                "customer_name": "اسم العميل",
                "product_name": "اسم المنتج",
                "quantity": "الكمية",
                "unit_price": "سعر الوحدة",
                "total_price": "المجموع",
                "tax_rate": "معدل الضريبة",
                "tax_amount": "مبلغ الضريبة",
                "final_total": "المجموع النهائي",
                "payment_method": "طريقة الدفع",
                
                # طرق الدفع
                "cash": "نقدي",
                "mada": "مدى",
                "visa": "فيزا",
                "mastercard": "ماستركارد",
                "bank": "تحويل بنكي",
                "gcc": "GCC",
                "aks": "AKS",
                "credit": "آجل",
                
                # الأزرار
                "add": "إضافة",
                "edit": "تعديل",
                "delete": "حذف",
                "save": "حفظ",
                "cancel": "إلغاء",
                "print": "طباعة",
                "search": "بحث",
                "refresh": "تحديث",
                "export": "تصدير",
                "import": "استيراد",
                
                # الرسائل
                "success": "نجح",
                "error": "خطأ",
                "warning": "تحذير",
                "info": "معلومات",
                "confirm_delete": "هل أنت متأكد من الحذف؟",
                "operation_success": "تمت العملية بنجاح",
                "operation_failed": "فشلت العملية",
                
                # التقارير
                "sales_report": "تقرير المبيعات",
                "purchase_report": "تقرير المشتريات",
                "inventory_report": "تقرير المخزون",
                "financial_report": "التقرير المالي",
                "tax_report": "تقرير الضرائب",
                "employee_report": "تقرير الموظفين",
                
                # اللغة
                "language": "اللغة",
                "arabic": "العربية",
                "english": "English"
            },
            
            "en": {
                # Login Screen
                "login_title": "Login - Accounting System",
                "username": "Username",
                "password": "Password",
                "login": "Login",
                "forgot_password": "Forgot Password?",
                "invalid_credentials": "Invalid username or password",
                "login_success": "Login successful",
                
                # Dashboard
                "dashboard_title": "Main Dashboard",
                "welcome": "Welcome",
                "daily_sales": "Daily Sales",
                "monthly_sales": "Monthly Sales",
                "total_revenue": "Total Revenue",
                "total_expenses": "Total Expenses",
                "net_profit": "Net Profit",
                "low_stock_alerts": "Low Stock Alerts",
                
                # Main Menus
                "sales": "Sales",
                "purchases": "Purchases",
                "products": "Products",
                "inventory": "Inventory",
                "suppliers": "Suppliers",
                "customers": "Customers",
                "employees": "Employees",
                "reports": "Reports",
                "settings": "Settings",
                "logout": "Logout",
                
                # Branches
                "branches": "Branches",
                "place_india": "PLACE INDIA",
                "china_town": "CHINA TOWN",
                "select_branch": "Select Branch",
                "branch": "Branch",
                
                # Sales Invoice
                "sales_invoice": "Sales Invoice",
                "invoice_number": "Invoice Number",
                "invoice_date": "Invoice Date",
                "customer_name": "Customer Name",
                "product_name": "Product Name",
                "quantity": "Quantity",
                "unit_price": "Unit Price",
                "total_price": "Total Price",
                "tax_rate": "Tax Rate",
                "tax_amount": "Tax Amount",
                "final_total": "Final Total",
                "payment_method": "Payment Method",
                
                # Payment Methods
                "cash": "Cash",
                "mada": "MADA",
                "visa": "VISA",
                "mastercard": "MasterCard",
                "bank": "Bank Transfer",
                "gcc": "GCC",
                "aks": "AKS",
                "credit": "Credit",
                
                # Buttons
                "add": "Add",
                "edit": "Edit",
                "delete": "Delete",
                "save": "Save",
                "cancel": "Cancel",
                "print": "Print",
                "search": "Search",
                "refresh": "Refresh",
                "export": "Export",
                "import": "Import",
                
                # Messages
                "success": "Success",
                "error": "Error",
                "warning": "Warning",
                "info": "Information",
                "confirm_delete": "Are you sure you want to delete?",
                "operation_success": "Operation completed successfully",
                "operation_failed": "Operation failed",
                
                # Reports
                "sales_report": "Sales Report",
                "purchase_report": "Purchase Report",
                "inventory_report": "Inventory Report",
                "financial_report": "Financial Report",
                "tax_report": "Tax Report",
                "employee_report": "Employee Report",
                
                # Language
                "language": "Language",
                "arabic": "العربية",
                "english": "English"
            }
        }
    
    def set_language(self, language_code: str):
        """تغيير اللغة الحالية"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key: str, default: str = None) -> str:
        """الحصول على النص المترجم"""
        if default is None:
            default = key
            
        return self.translations.get(self.current_language, {}).get(key, default)
    
    def get_current_language(self) -> str:
        """الحصول على اللغة الحالية"""
        return self.current_language
    
    def is_rtl(self) -> bool:
        """التحقق من اتجاه الكتابة (من اليمين لليسار)"""
        return self.current_language == "ar"
    
    def get_available_languages(self) -> Dict[str, str]:
        """الحصول على قائمة اللغات المتاحة"""
        return {
            "ar": "العربية",
            "en": "English"
        }

# إنشاء مثيل عام لمدير اللغات
language_manager = LanguageManager()
