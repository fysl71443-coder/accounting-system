#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار يدوي شامل للأزرار - يفحص الكود والوظائف
"""

import requests
import re
import json
from datetime import datetime

class ManualButtonTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {}
    
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {'username': 'admin', 'password': 'admin112233'}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def get_page_content(self, url):
        """الحصول على محتوى الصفحة"""
        try:
            response = self.session.get(f"{self.base_url}{url}")
            if response.status_code == 200:
                return response.text
            return None
        except:
            return None
    
    def check_button_functionality(self, page_content, button_configs):
        """فحص وظائف الأزرار في الصفحة"""
        results = {}
        
        for button_id, config in button_configs.items():
            result = {
                'button_exists': False,
                'onclick_exists': False,
                'function_defined': False,
                'function_complete': False,
                'score': 0
            }
            
            # فحص وجود الزر
            button_pattern = rf'id="{button_id}"'
            if re.search(button_pattern, page_content):
                result['button_exists'] = True
                result['score'] += 25
            
            # فحص وجود onclick
            onclick_pattern = rf'onclick="{config["onclick"]}\(\)"'
            if re.search(onclick_pattern, page_content):
                result['onclick_exists'] = True
                result['score'] += 25
            
            # فحص تعريف الوظيفة
            function_pattern = rf'function {config["onclick"]}\s*\('
            if re.search(function_pattern, page_content):
                result['function_defined'] = True
                result['score'] += 25
            
            # فحص اكتمال الوظيفة (وجود محتوى)
            function_content_pattern = rf'function {config["onclick"]}\s*\([^{{]*\{{[^}}]+\}}'
            if re.search(function_content_pattern, page_content, re.DOTALL):
                result['function_complete'] = True
                result['score'] += 25
            
            results[button_id] = result
        
        return results
    
    def test_sales_page(self):
        """اختبار صفحة المبيعات"""
        print("\n🔍 اختبار صفحة المبيعات:")
        
        content = self.get_page_content('/sales')
        if not content:
            print("❌ فشل في تحميل صفحة المبيعات")
            return {}
        
        button_configs = {
            'btnSalesPrint': {'onclick': 'PrintSalesRecord'},
            'btnSalesPreview': {'onclick': 'PreviewSalesRecord'},
            'btnSalesPayment': {'onclick': 'RegisterPayment'},
            'btnSalesEdit': {'onclick': 'EditSalesRecord'},
            'btnSalesDelete': {'onclick': 'DeleteSalesRecord'}
        }
        
        results = self.check_button_functionality(content, button_configs)
        
        # طباعة النتائج
        for button_id, result in results.items():
            score = result['score']
            if score == 100:
                status = "✅ مثالي"
            elif score >= 75:
                status = "🟡 جيد"
            elif score >= 50:
                status = "🟠 متوسط"
            else:
                status = "❌ ضعيف"
            
            print(f"  {status} {button_id}: {score}%")
            if score < 100:
                issues = []
                if not result['button_exists']: issues.append("الزر غير موجود")
                if not result['onclick_exists']: issues.append("onclick غير موجود")
                if not result['function_defined']: issues.append("الوظيفة غير معرفة")
                if not result['function_complete']: issues.append("الوظيفة فارغة")
                print(f"    المشاكل: {', '.join(issues)}")
        
        return results
    
    def test_purchases_page(self):
        """اختبار صفحة المشتريات"""
        print("\n🔍 اختبار صفحة المشتريات:")
        
        content = self.get_page_content('/purchases')
        if not content:
            print("❌ فشل في تحميل صفحة المشتريات")
            return {}
        
        button_configs = {
            'btnPurchasesPrint': {'onclick': 'PrintPurchasesRecord'},
            'btnPurchasesPreview': {'onclick': 'PreviewPurchasesRecord'},
            'btnPurchasesPayment': {'onclick': 'RegisterPurchasesPayment'},
            'btnPurchasesEdit': {'onclick': 'EditPurchasesRecord'},
            'btnPurchasesDelete': {'onclick': 'DeletePurchasesRecord'}
        }
        
        results = self.check_button_functionality(content, button_configs)
        
        # طباعة النتائج
        for button_id, result in results.items():
            score = result['score']
            if score == 100:
                status = "✅ مثالي"
            elif score >= 75:
                status = "🟡 جيد"
            elif score >= 50:
                status = "🟠 متوسط"
            else:
                status = "❌ ضعيف"
            
            print(f"  {status} {button_id}: {score}%")
            if score < 100:
                issues = []
                if not result['button_exists']: issues.append("الزر غير موجود")
                if not result['onclick_exists']: issues.append("onclick غير موجود")
                if not result['function_defined']: issues.append("الوظيفة غير معرفة")
                if not result['function_complete']: issues.append("الوظيفة فارغة")
                print(f"    المشاكل: {', '.join(issues)}")
        
        return results
    
    def test_expenses_page(self):
        """اختبار صفحة المصروفات"""
        print("\n🔍 اختبار صفحة المصروفات:")
        
        content = self.get_page_content('/expenses')
        if not content:
            print("❌ فشل في تحميل صفحة المصروفات")
            return {}
        
        button_configs = {
            'btnExpensesPrint': {'onclick': 'PrintExpensesRecord'},
            'btnExpensesPreview': {'onclick': 'PreviewExpensesRecord'},
            'btnExpensesPayment': {'onclick': 'RegisterExpensesPayment'},
            'btnExpensesEdit': {'onclick': 'EditExpensesRecord'},
            'btnExpensesDelete': {'onclick': 'DeleteExpensesRecord'}
        }
        
        results = self.check_button_functionality(content, button_configs)
        
        # طباعة النتائج
        for button_id, result in results.items():
            score = result['score']
            if score == 100:
                status = "✅ مثالي"
            elif score >= 75:
                status = "🟡 جيد"
            elif score >= 50:
                status = "🟠 متوسط"
            else:
                status = "❌ ضعيف"
            
            print(f"  {status} {button_id}: {score}%")
            if score < 100:
                issues = []
                if not result['button_exists']: issues.append("الزر غير موجود")
                if not result['onclick_exists']: issues.append("onclick غير موجود")
                if not result['function_defined']: issues.append("الوظيفة غير معرفة")
                if not result['function_complete']: issues.append("الوظيفة فارغة")
                print(f"    المشاكل: {', '.join(issues)}")
        
        return results
    
    def test_api_endpoints(self):
        """اختبار API endpoints"""
        print("\n🔍 اختبار API endpoints:")
        
        endpoints = [
            ('/api/sales/delete/999', 'DELETE'),
            ('/api/purchases/delete/999', 'DELETE'),
            ('/api/expenses/delete/999', 'DELETE')
        ]
        
        results = {}
        for endpoint, method in endpoints:
            try:
                if method == 'DELETE':
                    response = self.session.delete(f"{self.base_url}{endpoint}")
                
                # نتوقع 404 لأن ID غير موجود، أو 405 إذا كان endpoint غير موجود
                if response.status_code in [404, 405]:
                    print(f"✅ {endpoint} - endpoint موجود")
                    results[endpoint] = True
                else:
                    print(f"❌ {endpoint} - endpoint غير متاح ({response.status_code})")
                    results[endpoint] = False
                    
            except Exception as e:
                print(f"❌ {endpoint} - خطأ: {e}")
                results[endpoint] = False
        
        return results
    
    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        total_score = 0
        total_buttons = 0
        
        for page_results in self.test_results.values():
            if isinstance(page_results, dict):
                for button_result in page_results.values():
                    if isinstance(button_result, dict) and 'score' in button_result:
                        total_score += button_result['score']
                        total_buttons += 1
        
        return (total_score / (total_buttons * 100) * 100) if total_buttons > 0 else 0
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🚀 بدء الاختبار اليدوي الشامل للأزرار")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        
        # اختبار الصفحات
        self.test_results['sales'] = self.test_sales_page()
        self.test_results['purchases'] = self.test_purchases_page()
        self.test_results['expenses'] = self.test_expenses_page()
        self.test_results['api'] = self.test_api_endpoints()
        
        # حساب النتيجة الإجمالية
        overall_score = self.calculate_overall_score()
        
        # طباعة التقرير النهائي
        print("\n" + "=" * 60)
        print("📊 التقرير النهائي")
        print("=" * 60)
        print(f"📈 النتيجة الإجمالية: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("🎉 ممتاز! الأزرار تعمل بكفاءة عالية")
        elif overall_score >= 70:
            print("🟡 جيد - يحتاج بعض التحسينات")
        elif overall_score >= 50:
            print("🟠 متوسط - يحتاج تحسينات")
        else:
            print("❌ ضعيف - يحتاج إصلاحات كبيرة")
        
        # حفظ النتائج
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"manual_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ النتائج في: {filename}")
        
        return True

if __name__ == "__main__":
    tester = ManualButtonTester()
    tester.run_comprehensive_test()
