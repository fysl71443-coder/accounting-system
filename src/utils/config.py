# -*- coding: utf-8 -*-
"""
إعدادات التطبيق
Application Configuration
"""

import json
import os
from typing import Dict, Any

class Config:
    """فئة إدارة إعدادات التطبيق"""
    
    def __init__(self, config_file="config/settings.json"):
        """تهيئة إعدادات التطبيق"""
        self.config_file = config_file
        self.settings = {}
        self.load_default_settings()
        self.load_settings()
    
    def load_default_settings(self):
        """تحميل الإعدادات الافتراضية"""
        self.settings = {
            # إعدادات عامة
            "app_name": "نظام المحاسبة المتكامل",
            "app_name_en": "Integrated Accounting System",
            "version": "1.0.0",
            "language": "ar",  # اللغة الافتراضية
            
            # إعدادات قاعدة البيانات
            "database": {
                "path": "data/accounting.db",
                "backup_path": "backups/",
                "auto_backup": True,
                "backup_interval_days": 7
            },
            
            # إعدادات الشركة
            "company": {
                "name": "اسم الشركة",
                "name_en": "Company Name",
                "address": "عنوان الشركة",
                "phone": "+966-XX-XXX-XXXX",
                "email": "info@company.com",
                "tax_number": "123456789",
                "logo_path": "assets/logo.png"
            },
            
            # إعدادات الفواتير
            "invoice": {
                "auto_generate_number": True,
                "number_prefix": "INV-",
                "number_format": "{prefix}{year}{month:02d}{sequence:04d}",
                "default_tax_rate": 15.0,
                "print_after_save": False,
                "show_barcode": True,
                "barcode_type": "code128"
            },
            
            # إعدادات الفروع
            "branches": {
                "default_branch": "PI",  # PLACE INDIA
                "require_branch_selection": True,
                "branch_specific_numbering": True
            },
            
            # إعدادات طرق الدفع
            "payment_methods": [
                {"code": "CASH", "name_ar": "نقدي", "name_en": "Cash"},
                {"code": "MADA", "name_ar": "مدى", "name_en": "MADA"},
                {"code": "VISA", "name_ar": "فيزا", "name_en": "VISA"},
                {"code": "MASTERCARD", "name_ar": "ماستركارد", "name_en": "MasterCard"},
                {"code": "BANK", "name_ar": "تحويل بنكي", "name_en": "Bank Transfer"},
                {"code": "GCC", "name_ar": "GCC", "name_en": "GCC"},
                {"code": "AKS", "name_ar": "AKS", "name_en": "AKS"},
                {"code": "CREDIT", "name_ar": "آجل", "name_en": "Credit"}
            ],
            
            # إعدادات الواجهة
            "ui": {
                "theme": "default",
                "font_size": 10,
                "window_width": 1200,
                "window_height": 800,
                "show_splash_screen": True,
                "auto_save_interval": 300  # بالثواني
            },
            
            # إعدادات التقارير
            "reports": {
                "default_format": "pdf",
                "output_path": "reports/",
                "include_logo": True,
                "page_size": "A4",
                "orientation": "portrait"
            },
            
            # إعدادات الأمان
            "security": {
                "session_timeout": 3600,  # بالثواني
                "password_min_length": 6,
                "require_password_change": False,
                "max_login_attempts": 3,
                "lockout_duration": 300  # بالثواني
            },
            
            # إعدادات المخزون
            "inventory": {
                "low_stock_threshold": 10,
                "enable_negative_stock": False,
                "auto_update_cost": True,
                "cost_method": "FIFO"  # FIFO, LIFO, Average
            }
        }
    
    def load_settings(self):
        """تحميل الإعدادات من الملف"""
        try:
            # إنشاء مجلد الإعدادات إذا لم يكن موجوداً
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_settings = json.load(f)
                    # دمج الإعدادات المحملة مع الافتراضية
                    self._merge_settings(self.settings, file_settings)
        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
    
    def save_settings(self):
        """حفظ الإعدادات في الملف"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {e}")
            return False
    
    def get(self, key: str, default=None):
        """الحصول على قيمة إعداد"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """تعيين قيمة إعداد"""
        keys = key.split('.')
        setting = self.settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        setting[keys[-1]] = value
    
    def _merge_settings(self, default: Dict, loaded: Dict):
        """دمج الإعدادات المحملة مع الافتراضية"""
        for key, value in loaded.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_settings(default[key], value)
            else:
                default[key] = value
    
    def get_payment_methods(self):
        """الحصول على طرق الدفع"""
        return self.get("payment_methods", [])
    
    def get_company_info(self):
        """الحصول على معلومات الشركة"""
        return self.get("company", {})
    
    def get_invoice_settings(self):
        """الحصول على إعدادات الفواتير"""
        return self.get("invoice", {})
    
    def get_branch_settings(self):
        """الحصول على إعدادات الفروع"""
        return self.get("branches", {})
