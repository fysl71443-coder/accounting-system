#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل ومنهجي لجميع شاشات النظام
Comprehensive and Systematic Test for All System Screens
"""

import requests
import time
import json
from datetime import datetime
from urllib.parse import urljoin

class SystemTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, status, details=""):
        """تسجيل نتيجة الاختبار"""
        self.total_tests += 1
        if status:
            self.passed_tests += 1
            print(f"✅ {test_name}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name} - {details}")
        
        self.test_results[test_name] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_login(self):
        """اختبار تسجيل الدخول"""
        print("\n🔐 اختبار تسجيل الدخول...")
        
        try:
            # اختبار صفحة تسجيل الدخول
            response = self.session.get(urljoin(self.base_url, "/login"))
            self.log_test("صفحة تسجيل الدخول تحميل", response.status_code == 200)
            
            # اختبار تسجيل الدخول
            login_data = {
                'username': 'admin',
                'password': 'admin112233'
            }
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data)
            success = response.status_code == 302 or 'dashboard' in response.url
            self.log_test("تسجيل الدخول بنجاح", success)
            
            return success
            
        except Exception as e:
            self.log_test("تسجيل الدخول", False, str(e))
            return False
    
    def test_screen(self, url, screen_name, expected_elements=None):
        """اختبار شاشة واحدة"""
        try:
            response = self.session.get(urljoin(self.base_url, url))
            
            # اختبار تحميل الصفحة
            page_loads = response.status_code == 200
            self.log_test(f"{screen_name} - تحميل الصفحة", page_loads)
            
            if page_loads and expected_elements:
                content = response.text
                for element in expected_elements:
                    element_exists = element in content
                    self.log_test(f"{screen_name} - عنصر '{element}'", element_exists)
            
            return page_loads
            
        except Exception as e:
            self.log_test(f"{screen_name} - تحميل", False, str(e))
            return False
    
    def test_dashboard(self):
        """اختبار الشاشة الرئيسية"""
        print("\n🏠 اختبار الشاشة الرئيسية...")
        
        expected_elements = [
            'لوحة التحكم',
            'إدارة المبيعات',
            'إدارة المنتجات',
            'المشتريات',
            'المصروفات',
            'طباعة جميع الفواتير',
            'طباعة فواتير المبيعات',
            'طباعة فواتير المشتريات',
            'طباعة فواتير المصروفات',
            'طباعة كشوف الرواتب'
        ]
        
        return self.test_screen("/dashboard", "الشاشة الرئيسية", expected_elements)
    
    def test_sales_screen(self):
        """اختبار شاشة المبيعات"""
        print("\n💰 اختبار شاشة المبيعات...")
        
        expected_elements = [
            'المبيعات',
            'إضافة مبيعة جديدة',
            'البحث',
            'فلترة',
            'المجموع'
        ]
        
        return self.test_screen("/sales", "شاشة المبيعات", expected_elements)
    
    def test_purchases_screen(self):
        """اختبار شاشة المشتريات"""
        print("\n🛒 اختبار شاشة المشتريات...")
        
        expected_elements = [
            'المشتريات',
            'إضافة مشترى جديد',
            'البحث',
            'المورد'
        ]
        
        return self.test_screen("/purchases", "شاشة المشتريات", expected_elements)
    
    def test_expenses_screen(self):
        """اختبار شاشة المصروفات"""
        print("\n💸 اختبار شاشة المصروفات...")
        
        expected_elements = [
            'المصروفات',
            'إضافة مصروف جديد',
            'الوصف',
            'المبلغ'
        ]
        
        return self.test_screen("/expenses", "شاشة المصروفات", expected_elements)
    
    def test_products_screen(self):
        """اختبار شاشة المنتجات"""
        print("\n📦 اختبار شاشة المنتجات...")
        
        expected_elements = [
            'المنتجات',
            'إضافة منتج',
            'المواد الخام',
            'حساب التكلفة'
        ]
        
        return self.test_screen("/products", "شاشة المنتجات", expected_elements)
    
    def test_customers_screen(self):
        """اختبار شاشة العملاء"""
        print("\n👥 اختبار شاشة العملاء...")
        
        expected_elements = [
            'العملاء',
            'إضافة عميل',
            'الاسم',
            'الهاتف'
        ]
        
        return self.test_screen("/customers", "شاشة العملاء", expected_elements)
    
    def test_suppliers_screen(self):
        """اختبار شاشة الموردين"""
        print("\n🚚 اختبار شاشة الموردين...")
        
        expected_elements = [
            'الموردين',
            'إضافة مورد',
            'الاسم',
            'الهاتف'
        ]
        
        return self.test_screen("/suppliers", "شاشة الموردين", expected_elements)
    
    def test_inventory_screen(self):
        """اختبار شاشة المخزون"""
        print("\n📦 اختبار شاشة المخزون...")
        
        expected_elements = [
            'المخزون',
            'المنتج',
            'الكمية',
            'السعر'
        ]
        
        return self.test_screen("/inventory", "شاشة المخزون", expected_elements)
    
    def test_reports_screen(self):
        """اختبار شاشة التقارير"""
        print("\n📊 اختبار شاشة التقارير...")
        
        expected_elements = [
            'التقارير',
            'تقرير المبيعات',
            'تقرير المشتريات',
            'من تاريخ',
            'إلى تاريخ'
        ]
        
        return self.test_screen("/reports", "شاشة التقارير", expected_elements)
    
    def test_financial_statements_screen(self):
        """اختبار شاشة القوائم المالية"""
        print("\n📈 اختبار شاشة القوائم المالية...")
        
        expected_elements = [
            'القوائم المالية',
            'قائمة الدخل',
            'الميزانية العمومية'
        ]
        
        return self.test_screen("/financial_statements", "شاشة القوائم المالية", expected_elements)
    
    def test_payments_dues_screen(self):
        """اختبار شاشة المدفوعات والمستحقات"""
        print("\n💳 اختبار شاشة المدفوعات والمستحقات...")
        
        expected_elements = [
            'المدفوعات والمستحقات',
            'المبلغ الإجمالي',
            'المبلغ المدفوع'
        ]
        
        return self.test_screen("/payments_dues", "شاشة المدفوعات والمستحقات", expected_elements)
    
    def test_employee_payroll_screen(self):
        """اختبار شاشة الموظفين والرواتب"""
        print("\n👨‍💼 اختبار شاشة الموظفين والرواتب...")
        
        expected_elements = [
            'الموظفين والرواتب',
            'إضافة موظف',
            'الراتب'
        ]
        
        return self.test_screen("/employee_payroll", "شاشة الموظفين والرواتب", expected_elements)
    
    def test_settings_screen(self):
        """اختبار شاشة الإعدادات"""
        print("\n⚙️ اختبار شاشة الإعدادات...")
        
        expected_elements = [
            'الإعدادات',
            'إعدادات النظام',
            'اللغة'
        ]
        
        return self.test_screen("/settings", "شاشة الإعدادات", expected_elements)
    
    def test_print_functionality(self):
        """اختبار وظائف الطباعة"""
        print("\n🖨️ اختبار وظائف الطباعة...")
        
        print_urls = [
            "/print_all_invoices/sales",
            "/print_all_invoices/purchases", 
            "/print_all_invoices/expenses",
            "/print_all_invoices/payroll"
        ]
        
        for url in print_urls:
            try:
                response = self.session.get(urljoin(self.base_url, url))
                success = response.status_code == 200
                invoice_type = url.split('/')[-1]
                self.log_test(f"طباعة فواتير {invoice_type}", success)
            except Exception as e:
                self.log_test(f"طباعة فواتير {url}", False, str(e))
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🚀 بدء الاختبار الشامل لنظام المحاسبة")
        print("=" * 70)
        
        start_time = time.time()
        
        # اختبار تسجيل الدخول
        if not self.test_login():
            print("❌ فشل في تسجيل الدخول - توقف الاختبار")
            return
        
        # اختبار جميع الشاشات
        self.test_dashboard()
        self.test_sales_screen()
        self.test_purchases_screen()
        self.test_expenses_screen()
        self.test_products_screen()
        self.test_customers_screen()
        self.test_suppliers_screen()
        self.test_inventory_screen()
        self.test_reports_screen()
        self.test_financial_statements_screen()
        self.test_payments_dues_screen()
        self.test_employee_payroll_screen()
        self.test_settings_screen()
        
        # اختبار وظائف الطباعة
        self.test_print_functionality()
        
        # النتائج النهائية
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 70)
        print("📊 نتائج الاختبار الشامل:")
        print("=" * 70)
        print(f"✅ الاختبارات الناجحة: {self.passed_tests}")
        print(f"❌ الاختبارات الفاشلة: {self.failed_tests}")
        print(f"📊 إجمالي الاختبارات: {self.total_tests}")
        print(f"📈 نسبة النجاح: {(self.passed_tests/self.total_tests)*100:.1f}%")
        print(f"⏱️ وقت الاختبار: {duration:.2f} ثانية")
        
        if self.failed_tests == 0:
            print("🎉 جميع الاختبارات نجحت! النظام يعمل بشكل مثالي!")
        else:
            print("⚠️ بعض الاختبارات فشلت - يحتاج النظام إلى مراجعة")
        
        # حفظ النتائج
        self.save_results()
        
        return self.failed_tests == 0
    
    def save_results(self):
        """حفظ نتائج الاختبار"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.total_tests,
                'passed_tests': self.passed_tests,
                'failed_tests': self.failed_tests,
                'success_rate': (self.passed_tests/self.total_tests)*100 if self.total_tests > 0 else 0
            },
            'detailed_results': self.test_results
        }
        
        filename = f"comprehensive_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ النتائج في: {filename}")

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_comprehensive_test()
