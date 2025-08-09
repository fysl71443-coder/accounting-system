#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء بيانات عينة للاختبار
Create Sample Data for Testing
"""

import requests
import json
from datetime import datetime, timedelta

class SampleDataCreator:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {'username': 'admin', 'password': 'admin123'}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def create_customers_and_suppliers(self):
        """إنشاء عملاء وموردين"""
        print("👥 إنشاء عملاء وموردين:")
        
        # عملاء
        customers = [
            {'name': 'شركة الأمل التجارية', 'phone': '0501234567', 'email': 'amal@company.com'},
            {'name': 'مؤسسة النور للتجارة', 'phone': '0507654321', 'email': 'noor@trade.com'},
            {'name': 'شركة الفجر الجديد', 'phone': '0509876543', 'email': 'fajr@new.com'}
        ]
        
        for customer in customers:
            try:
                response = self.session.post(f"{self.base_url}/api/customers/create", json=customer)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  ✅ عميل: {customer['name']}")
            except:
                pass
        
        # موردين
        suppliers = [
            {'name': 'مورد المواد الأولية', 'phone': '0551234567', 'email': 'materials@supplier.com'},
            {'name': 'شركة التوريدات المتقدمة', 'phone': '0557654321', 'email': 'advanced@supply.com'}
        ]
        
        for supplier in suppliers:
            try:
                response = self.session.post(f"{self.base_url}/api/suppliers/create", json=supplier)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  ✅ مورد: {supplier['name']}")
            except:
                pass
    
    def create_sample_sales(self):
        """إنشاء مبيعات عينة"""
        print("\n💰 إنشاء مبيعات عينة:")
        
        sales_data = [
            {'subtotal': 5000, 'discount': 250, 'total': 4750, 'notes': 'مبيعة كبيرة مع خصم'},
            {'subtotal': 2500, 'discount': 100, 'total': 2400, 'notes': 'مبيعة متوسطة'},
            {'subtotal': 1200, 'discount': 0, 'total': 1200, 'notes': 'مبيعة صغيرة بدون خصم'},
            {'subtotal': 8000, 'discount': 500, 'total': 7500, 'notes': 'مبيعة كبيرة جداً'}
        ]
        
        created_count = 0
        for i, sale in enumerate(sales_data):
            sale['date'] = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                response = self.session.post(f"{self.base_url}/api/sales/create", json=sale)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        created_count += 1
                        print(f"  ✅ مبيعة #{result.get('sale_id')} - {sale['total']} ريال")
            except Exception as e:
                print(f"  ❌ خطأ في إنشاء المبيعة: {e}")
        
        print(f"  📊 تم إنشاء {created_count} مبيعة")
    
    def create_sample_expenses(self):
        """إنشاء مصروفات عينة"""
        print("\n📄 إنشاء مصروفات عينة:")
        
        expenses_data = [
            {'description': 'إيجار المكتب', 'amount': 3000, 'category': 'rent'},
            {'description': 'فواتير الكهرباء', 'amount': 800, 'category': 'utilities'},
            {'description': 'مواد مكتبية', 'amount': 450, 'category': 'office_supplies'},
            {'description': 'صيانة الأجهزة', 'amount': 1200, 'category': 'maintenance'}
        ]
        
        created_count = 0
        for i, expense in enumerate(expenses_data):
            expense['date'] = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            try:
                response = self.session.post(f"{self.base_url}/api/expenses/create", json=expense)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        created_count += 1
                        print(f"  ✅ مصروف #{result.get('expense_id')} - {expense['amount']} ريال")
            except Exception as e:
                print(f"  ❌ خطأ في إنشاء المصروف: {e}")
        
        print(f"  📊 تم إنشاء {created_count} مصروف")
    
    def run_data_creation(self):
        """تشغيل إنشاء البيانات"""
        print("🏗️ إنشاء بيانات عينة للاختبار")
        print("=" * 50)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        
        # إنشاء البيانات
        self.create_customers_and_suppliers()
        self.create_sample_sales()
        self.create_sample_expenses()
        
        print("\n🎉 تم إنشاء البيانات العينة بنجاح!")
        print("📊 يمكنك الآن اختبار التقارير مع البيانات الحقيقية")
        
        return True

if __name__ == "__main__":
    creator = SampleDataCreator()
    creator.run_data_creation()
