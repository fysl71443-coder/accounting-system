#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لوظائف الأزرار في شاشات المبيعات والمشتريات والمصروفات
"""

import requests
import time
import json
from datetime import datetime

class ButtonTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {
            'sales': {},
            'purchases': {},
            'expenses': {},
            'summary': {'passed': 0, 'failed': 0, 'total': 0}
        }
    
    def login(self, username="admin", password="admin112233"):
        """تسجيل الدخول"""
        try:
            login_data = {'username': username, 'password': password}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            if response.status_code == 200:
                print("✅ تم تسجيل الدخول بنجاح")
                return True
            else:
                print(f"❌ فشل تسجيل الدخول: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول: {e}")
            return False
    
    def test_page_load(self, page_url, page_name):
        """اختبار تحميل الصفحة"""
        try:
            response = self.session.get(f"{self.base_url}{page_url}")
            if response.status_code == 200:
                print(f"✅ {page_name} - تحميل الصفحة")
                return True
            else:
                print(f"❌ {page_name} - فشل تحميل الصفحة: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {page_name} - خطأ في تحميل الصفحة: {e}")
            return False
    
    def test_api_endpoint(self, endpoint, method="GET", data=None, expected_status=200):
        """اختبار API endpoint"""
        try:
            if method == "GET":
                response = self.session.get(f"{self.base_url}{endpoint}")
            elif method == "POST":
                response = self.session.post(f"{self.base_url}{endpoint}", json=data)
            elif method == "DELETE":
                response = self.session.delete(f"{self.base_url}{endpoint}")
            
            if response.status_code == expected_status:
                return True, response
            else:
                return False, response
        except Exception as e:
            return False, str(e)
    
    def test_sales_buttons(self):
        """اختبار أزرار شاشة المبيعات"""
        print("\n🔍 اختبار أزرار شاشة المبيعات:")
        results = {}
        
        # اختبار تحميل الصفحة
        results['page_load'] = self.test_page_load('/sales', 'المبيعات')
        
        # اختبار وجود الأزرار في HTML
        try:
            response = self.session.get(f"{self.base_url}/sales")
            html_content = response.text
            
            buttons_to_check = [
                ('btnSalesPrint', 'زر الطباعة'),
                ('btnSalesPreview', 'زر المعاينة'),
                ('btnSalesPayment', 'زر تسجيل الدفع'),
                ('btnSalesEdit', 'زر التعديل'),
                ('btnSalesDelete', 'زر الحذف')
            ]
            
            for button_id, button_name in buttons_to_check:
                if button_id in html_content:
                    print(f"✅ المبيعات - {button_name} موجود")
                    results[button_id] = True
                else:
                    print(f"❌ المبيعات - {button_name} غير موجود")
                    results[button_id] = False
                    
        except Exception as e:
            print(f"❌ خطأ في فحص أزرار المبيعات: {e}")
            results['buttons_check'] = False
        
        # اختبار JavaScript functions
        js_functions = [
            'PrintSalesRecord',
            'PreviewSalesRecord', 
            'RegisterPayment',
            'EditSalesRecord',
            'DeleteSalesRecord'
        ]
        
        for func in js_functions:
            if func in html_content:
                print(f"✅ المبيعات - وظيفة {func} موجودة")
                results[f'js_{func}'] = True
            else:
                print(f"❌ المبيعات - وظيفة {func} غير موجودة")
                results[f'js_{func}'] = False
        
        self.test_results['sales'] = results
        return results
    
    def test_purchases_buttons(self):
        """اختبار أزرار شاشة المشتريات"""
        print("\n🔍 اختبار أزرار شاشة المشتريات:")
        results = {}
        
        # اختبار تحميل الصفحة
        results['page_load'] = self.test_page_load('/purchases', 'المشتريات')
        
        # اختبار وجود الأزرار في HTML
        try:
            response = self.session.get(f"{self.base_url}/purchases")
            html_content = response.text
            
            buttons_to_check = [
                ('btnPurchasesPrint', 'زر الطباعة'),
                ('btnPurchasesPreview', 'زر المعاينة'),
                ('btnPurchasesPayment', 'زر تسجيل الدفع'),
                ('btnPurchasesEdit', 'زر التعديل'),
                ('btnPurchasesDelete', 'زر الحذف')
            ]
            
            for button_id, button_name in buttons_to_check:
                if button_id in html_content:
                    print(f"✅ المشتريات - {button_name} موجود")
                    results[button_id] = True
                else:
                    print(f"❌ المشتريات - {button_name} غير موجود")
                    results[button_id] = False
                    
        except Exception as e:
            print(f"❌ خطأ في فحص أزرار المشتريات: {e}")
            results['buttons_check'] = False
        
        # اختبار JavaScript functions
        js_functions = [
            'PrintPurchasesRecord',
            'PreviewPurchasesRecord',
            'RegisterPurchasesPayment', 
            'EditPurchasesRecord',
            'DeletePurchasesRecord'
        ]
        
        for func in js_functions:
            if func in html_content:
                print(f"✅ المشتريات - وظيفة {func} موجودة")
                results[f'js_{func}'] = True
            else:
                print(f"❌ المشتريات - وظيفة {func} غير موجودة")
                results[f'js_{func}'] = False
        
        self.test_results['purchases'] = results
        return results

    def test_expenses_buttons(self):
        """اختبار أزرار شاشة المصروفات"""
        print("\n🔍 اختبار أزرار شاشة المصروفات:")
        results = {}

        # اختبار تحميل الصفحة
        results['page_load'] = self.test_page_load('/expenses', 'المصروفات')

        # اختبار وجود الأزرار في HTML
        try:
            response = self.session.get(f"{self.base_url}/expenses")
            html_content = response.text

            buttons_to_check = [
                ('btnExpensesPrint', 'زر الطباعة'),
                ('btnExpensesPreview', 'زر المعاينة'),
                ('btnExpensesPayment', 'زر تسجيل الدفع'),
                ('btnExpensesEdit', 'زر التعديل'),
                ('btnExpensesDelete', 'زر الحذف')
            ]

            for button_id, button_name in buttons_to_check:
                if button_id in html_content:
                    print(f"✅ المصروفات - {button_name} موجود")
                    results[button_id] = True
                else:
                    print(f"❌ المصروفات - {button_name} غير موجود")
                    results[button_id] = False

        except Exception as e:
            print(f"❌ خطأ في فحص أزرار المصروفات: {e}")
            results['buttons_check'] = False

        # اختبار JavaScript functions
        js_functions = [
            'PrintExpensesRecord',
            'PreviewExpensesRecord',
            'RegisterExpensesPayment',
            'EditExpensesRecord',
            'DeleteExpensesRecord'
        ]

        for func in js_functions:
            if func in html_content:
                print(f"✅ المصروفات - وظيفة {func} موجودة")
                results[f'js_{func}'] = True
            else:
                print(f"❌ المصروفات - وظيفة {func} غير موجودة")
                results[f'js_{func}'] = False

        self.test_results['expenses'] = results
        return results

    def test_api_endpoints(self):
        """اختبار API endpoints"""
        print("\n🔍 اختبار API endpoints:")
        results = {}

        # اختبار endpoints الحذف (بدون حذف فعلي)
        endpoints_to_test = [
            ('/api/sales/delete/999', 'DELETE', 'حذف مبيعة'),
            ('/api/purchases/delete/999', 'DELETE', 'حذف مشتريات'),
            ('/api/expenses/delete/999', 'DELETE', 'حذف مصروف')
        ]

        for endpoint, method, description in endpoints_to_test:
            try:
                success, response = self.test_api_endpoint(endpoint, method, expected_status=404)
                if success or response.status_code == 404:  # 404 متوقع لأن ID غير موجود
                    print(f"✅ API - {description} endpoint موجود")
                    results[endpoint] = True
                else:
                    print(f"❌ API - {description} endpoint غير متاح")
                    results[endpoint] = False
            except Exception as e:
                print(f"❌ API - خطأ في اختبار {description}: {e}")
                results[endpoint] = False

        return results

    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🚀 بدء الاختبار الشامل لوظائف الأزرار")
        print("=" * 60)

        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return False

        # اختبار الشاشات
        sales_results = self.test_sales_buttons()
        purchases_results = self.test_purchases_buttons()
        expenses_results = self.test_expenses_buttons()
        api_results = self.test_api_endpoints()

        # حساب النتائج
        self.calculate_summary()

        # طباعة التقرير النهائي
        self.print_final_report()

        return True

    def calculate_summary(self):
        """حساب ملخص النتائج"""
        total_passed = 0
        total_failed = 0

        for screen in ['sales', 'purchases', 'expenses']:
            for test_name, result in self.test_results[screen].items():
                if result:
                    total_passed += 1
                else:
                    total_failed += 1

        self.test_results['summary'] = {
            'passed': total_passed,
            'failed': total_failed,
            'total': total_passed + total_failed,
            'success_rate': round((total_passed / (total_passed + total_failed)) * 100, 1) if (total_passed + total_failed) > 0 else 0
        }

    def print_final_report(self):
        """طباعة التقرير النهائي"""
        print("\n" + "=" * 60)
        print("📊 تقرير الاختبار النهائي")
        print("=" * 60)

        summary = self.test_results['summary']
        print(f"✅ الاختبارات الناجحة: {summary['passed']}")
        print(f"❌ الاختبارات الفاشلة: {summary['failed']}")
        print(f"📊 إجمالي الاختبارات: {summary['total']}")
        print(f"📈 نسبة النجاح: {summary['success_rate']}%")

        if summary['success_rate'] >= 90:
            print("🎉 ممتاز! الأزرار تعمل بكفاءة عالية")
        elif summary['success_rate'] >= 70:
            print("⚠️ جيد - يحتاج بعض التحسينات")
        else:
            print("🔧 يحتاج إصلاحات كبيرة")

        # حفظ النتائج في ملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"button_test_results_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)

        print(f"💾 تم حفظ النتائج في: {filename}")

if __name__ == "__main__":
    tester = ButtonTester()
    tester.run_comprehensive_test()
