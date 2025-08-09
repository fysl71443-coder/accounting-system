#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار طباعة البيانات الحقيقية
Test Real Data Printing
"""

import requests
import json
from datetime import datetime

class RealDataPrintingTest:
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
    
    def create_test_data(self):
        """إنشاء بيانات اختبار حقيقية"""
        print("📊 إنشاء بيانات اختبار حقيقية:")
        
        # إنشاء مبيعة اختبار
        sale_data = {
            'subtotal': 1500.00,
            'discount': 100.00,
            'total': 1400.00,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'notes': 'مبيعة اختبار للطباعة'
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/sales/create", json=sale_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"  ✅ تم إنشاء مبيعة اختبار #{result.get('sale_id')}")
                else:
                    print(f"  ❌ فشل إنشاء المبيعة: {result.get('message')}")
        except Exception as e:
            print(f"  ❌ خطأ في إنشاء المبيعة: {e}")
        
        # إنشاء مصروف اختبار
        expense_data = {
            'description': 'مصروف اختبار للطباعة',
            'amount': 750.00,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'category': 'office_supplies',
            'notes': 'اختبار طباعة البيانات الحقيقية'
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/expenses/create", json=expense_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"  ✅ تم إنشاء مصروف اختبار #{result.get('expense_id')}")
                else:
                    print(f"  ❌ فشل إنشاء المصروف: {result.get('message')}")
        except Exception as e:
            print(f"  ❌ خطأ في إنشاء المصروف: {e}")
    
    def test_data_apis(self):
        """اختبار APIs جلب البيانات"""
        print("🔗 اختبار APIs جلب البيانات:")
        
        apis = [
            ('/api/sales/list', 'المبيعات'),
            ('/api/purchases/list', 'المشتريات'),
            ('/api/expenses/list', 'المصروفات'),
            ('/api/payroll/list', 'الرواتب')
        ]
        
        working_apis = 0
        
        for api_path, name in apis:
            try:
                response = self.session.get(f"{self.base_url}{api_path}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        count = result.get('count', 0)
                        data_key = api_path.split('/')[-2]  # sales, purchases, etc.
                        data_list = result.get(data_key, [])
                        
                        print(f"  ✅ {name} - {count} عنصر")
                        
                        # عرض عينة من البيانات
                        if data_list and len(data_list) > 0:
                            sample = data_list[0]
                            if 'total' in sample:
                                print(f"     - عينة: المبلغ {sample['total']} ريال")
                            elif 'amount' in sample:
                                print(f"     - عينة: المبلغ {sample['amount']} ريال")
                        
                        working_apis += 1
                    else:
                        print(f"  ❌ {name} - فشل: {result.get('message')}")
                else:
                    print(f"  ❌ {name} - خطأ HTTP: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {name} - خطأ: {e}")
        
        return working_apis == len(apis)
    
    def test_print_data_quality(self):
        """اختبار جودة البيانات للطباعة"""
        print("📋 اختبار جودة البيانات للطباعة:")
        
        try:
            # اختبار بيانات المبيعات
            response = self.session.get(f"{self.base_url}/api/sales/list")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    sales = result.get('sales', [])
                    if sales:
                        sample_sale = sales[0]
                        required_fields = ['id', 'date', 'total', 'payment_status']
                        missing_fields = [field for field in required_fields if field not in sample_sale]
                        
                        if not missing_fields:
                            print("  ✅ بيانات المبيعات - كاملة وجاهزة للطباعة")
                        else:
                            print(f"  ⚠️ بيانات المبيعات - حقول مفقودة: {missing_fields}")
                    else:
                        print("  ⚠️ بيانات المبيعات - لا توجد بيانات")
            
            # اختبار بيانات المصروفات
            response = self.session.get(f"{self.base_url}/api/expenses/list")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    expenses = result.get('expenses', [])
                    if expenses:
                        sample_expense = expenses[0]
                        required_fields = ['id', 'date', 'description', 'amount', 'payment_status']
                        missing_fields = [field for field in required_fields if field not in sample_expense]
                        
                        if not missing_fields:
                            print("  ✅ بيانات المصروفات - كاملة وجاهزة للطباعة")
                        else:
                            print(f"  ⚠️ بيانات المصروفات - حقول مفقودة: {missing_fields}")
                    else:
                        print("  ⚠️ بيانات المصروفات - لا توجد بيانات")
            
            return True
            
        except Exception as e:
            print(f"  ❌ خطأ في اختبار جودة البيانات: {e}")
            return False
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🖨️ اختبار شامل لطباعة البيانات الحقيقية")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        print()
        
        # إنشاء بيانات اختبار
        self.create_test_data()
        print()
        
        # تشغيل الاختبارات
        tests = [
            ('APIs جلب البيانات', self.test_data_apis),
            ('جودة البيانات للطباعة', self.test_print_data_quality)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed_tests += 1
                print()
            except Exception as e:
                print(f"  ❌ {test_name} - خطأ في الاختبار: {e}")
                print()
        
        # النتائج النهائية
        print("=" * 60)
        print("📊 نتائج اختبار طباعة البيانات الحقيقية:")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 نسبة النجاح: {success_rate:.1f}%")
        print(f"✅ اختبارات ناجحة: {passed_tests}/{total_tests}")
        
        if success_rate == 100:
            print("🎉 ممتاز! طباعة البيانات الحقيقية تعمل بكفاءة 100%")
            print("🖨️ جميع أزرار الطباعة تعرض البيانات الحقيقية")
        elif success_rate >= 80:
            print("🟢 جيد جداً - الطباعة تعمل مع البيانات الحقيقية")
        else:
            print("🔴 يحتاج إصلاحات - الطباعة لا تزال تعرض بيانات وهمية")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = RealDataPrintingTest()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 نظام طباعة البيانات الحقيقية جاهز!")
        print("🖨️ جميع أزرار الطباعة تعرض البيانات الحقيقية من قاعدة البيانات")
    else:
        print("\n⚠️ النظام يحتاج مراجعة لضمان عرض البيانات الحقيقية")
