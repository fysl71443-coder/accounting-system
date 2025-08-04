# -*- coding: utf-8 -*-
"""
مدير قاعدة البيانات
Database Manager
"""

import sqlite3
import os
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    """مدير قاعدة البيانات الرئيسي"""
    
    def __init__(self, db_path: str = "data/accounting.db"):
        """تهيئة مدير قاعدة البيانات"""
        self.db_path = db_path
        self.connection = None
        
        # إنشاء مجلد البيانات إذا لم يكن موجوداً
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # الاتصال بقاعدة البيانات
        self.connect()
    
    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
            return True
        except Exception as e:
            print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            return False
    
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Dict]]:
        """تنفيذ استعلام وإرجاع النتائج"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.connection.commit()
                return cursor.rowcount
                
        except Exception as e:
            print(f"خطأ في تنفيذ الاستعلام: {e}")
            self.connection.rollback()
            return None
    
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول المستخدمين
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """
        
        # جدول الأدوار والصلاحيات
        roles_table = """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL,
            permissions TEXT,
            description TEXT
        )
        """
        
        # جدول المنتجات
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE NOT NULL,
            product_name TEXT NOT NULL,
            description TEXT,
            unit_cost REAL DEFAULT 0,
            selling_price REAL DEFAULT 0,
            category TEXT,
            unit_type TEXT DEFAULT 'قطعة',
            min_stock_level INTEGER DEFAULT 0,
            current_stock INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # جدول الموردين
        suppliers_table = """
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            tax_number TEXT,
            payment_terms TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # جدول العملاء
        customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            tax_number TEXT,
            credit_limit REAL DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # جدول فواتير المشتريات
        purchases_table = """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            supplier_id INTEGER,
            invoice_date DATE NOT NULL,
            total_amount REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            final_amount REAL DEFAULT 0,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        """
        
        # جدول عناصر فواتير المشتريات
        purchase_items_table = """
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            product_id INTEGER,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            tax_rate REAL DEFAULT 15,
            tax_amount REAL DEFAULT 0,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """
        
        # جدول الفروع
        branches_table = """
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_code TEXT UNIQUE NOT NULL,
            branch_name TEXT NOT NULL,
            branch_name_en TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            manager_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # جدول فواتير المبيعات
        sales_table = """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            branch_id INTEGER,
            customer_id INTEGER,
            invoice_date DATE NOT NULL,
            total_amount REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            final_amount REAL DEFAULT 0,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (branch_id) REFERENCES branches (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        """
        
        # جدول عناصر فواتير المبيعات
        sale_items_table = """
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            tax_rate REAL DEFAULT 15,
            tax_amount REAL DEFAULT 0,
            FOREIGN KEY (sale_id) REFERENCES sales (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """
        
        # تنفيذ إنشاء الجداول
        tables = [
            users_table, roles_table, products_table, suppliers_table,
            customers_table, branches_table, purchases_table, purchase_items_table,
            sales_table, sale_items_table
        ]
        
        for table in tables:
            self.execute_query(table)
    
    def hash_password(self, password: str) -> str:
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_admin(self):
        """إنشاء مستخدم المدير الافتراضي"""
        # التحقق من وجود مستخدم مدير
        admin_exists = self.execute_query(
            "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
        )

        if not admin_exists:
            # إنشاء مستخدم المدير الافتراضي
            admin_password = self.hash_password("admin123")
            self.execute_query(
                """INSERT INTO users (username, password_hash, full_name, role)
                   VALUES (?, ?, ?, ?)""",
                ("admin", admin_password, "مدير النظام", "admin")
            )
            print("تم إنشاء مستخدم المدير الافتراضي: admin / admin123")

        # إنشاء الفروع الافتراضية
        self.create_default_branches()

        # إنشاء منتجات تجريبية
        self.create_sample_products()

    def create_default_branches(self):
        """إنشاء الفروع الافتراضية"""
        # التحقق من وجود فروع
        branches_exist = self.execute_query("SELECT id FROM branches LIMIT 1")

        if not branches_exist:
            # إنشاء الفروع الافتراضية
            branches = [
                ("PI", "PLACE INDIA", "PLACE INDIA", "", "", ""),
                ("CT", "CHINA TOWN", "CHINA TOWN", "", "", "")
            ]

            for branch_code, branch_name, branch_name_en, address, phone, manager in branches:
                self.execute_query(
                    """INSERT INTO branches (branch_code, branch_name, branch_name_en, address, phone, manager_name)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (branch_code, branch_name, branch_name_en, address, phone, manager)
                )

            print("تم إنشاء الفروع الافتراضية: PLACE INDIA, CHINA TOWN")

    def create_sample_products(self):
        """إنشاء منتجات تجريبية"""
        # التحقق من وجود منتجات
        products_exist = self.execute_query("SELECT id FROM products LIMIT 1")

        if not products_exist:
            # إنشاء منتجات تجريبية
            sample_products = [
                ("PHONE001", "iPhone 14", "هاتف ذكي من آبل", 3000.00, 3500.00, "إلكترونيات", "قطعة", 5, 20),
                ("PHONE002", "Samsung Galaxy S23", "هاتف ذكي من سامسونج", 2500.00, 3000.00, "إلكترونيات", "قطعة", 5, 15),
                ("LAPTOP001", "MacBook Air", "لابتوب من آبل", 4000.00, 4800.00, "إلكترونيات", "قطعة", 3, 10),
                ("LAPTOP002", "Dell XPS 13", "لابتوب من ديل", 3500.00, 4200.00, "إلكترونيات", "قطعة", 3, 8),
                ("SHIRT001", "قميص قطني", "قميص رجالي قطني", 50.00, 80.00, "ملابس", "قطعة", 10, 50),
                ("PANTS001", "بنطلون جينز", "بنطلون جينز رجالي", 80.00, 120.00, "ملابس", "قطعة", 10, 30),
                ("FOOD001", "أرز بسمتي", "أرز بسمتي فاخر", 15.00, 25.00, "أغذية", "كيلو", 20, 100),
                ("FOOD002", "زيت زيتون", "زيت زيتون بكر ممتاز", 30.00, 45.00, "أغذية", "لتر", 15, 50),
                ("COSM001", "كريم مرطب", "كريم مرطب للوجه", 25.00, 40.00, "مستحضرات تجميل", "قطعة", 8, 25),
                ("COSM002", "شامبو", "شامبو للشعر الجاف", 20.00, 35.00, "مستحضرات تجميل", "قطعة", 10, 40)
            ]

            for product_code, name, desc, cost, price, category, unit, min_stock, current_stock in sample_products:
                self.execute_query(
                    """INSERT INTO products (product_code, product_name, description, unit_cost,
                       selling_price, category, unit_type, min_stock_level, current_stock, is_active)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                    (product_code, name, desc, cost, price, category, unit, min_stock, current_stock)
                )

            print("تم إنشاء منتجات تجريبية")
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """التحقق من صحة بيانات المستخدم"""
        password_hash = self.hash_password(password)
        
        user = self.execute_query(
            """SELECT id, username, full_name, email, role, is_active 
               FROM users WHERE username = ? AND password_hash = ? AND is_active = 1""",
            (username, password_hash)
        )
        
        if user:
            # تحديث وقت آخر تسجيل دخول
            self.execute_query(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user[0]['id'],)
            )
            return user[0]
        
        return None
