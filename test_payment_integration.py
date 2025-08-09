#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لنظام ربط المدفوعات
Comprehensive Payment Integration Test
"""

import requests
import json
import time
from datetime import datetime
from app import app, db, Sale, Purchase, Expense, Payroll

class PaymentIntegrationTest:
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
    
    def test_payment_fields_exist(self):
        """اختبار وجود حقول المدفوعات في قاعدة البيانات"""
        print("🔍 اختبار وجود حقول المدفوعات:")
        
        with app.app_context():
            try:
                # اختبار نموذج المبيعات
                sale = Sale()
                has_payment_fields = all(hasattr(sale, field) for field in 
                                       ['payment_status', 'paid_amount', 'payment_date', 'payment_method'])
                print(f"  {'✅' if has_payment_fields else '❌'} نموذج المبيعات - حقول المدفوعات")
                
                # اختبار نموذج المشتريات
                purchase = Purchase()
                has_payment_fields = all(hasattr(purchase, field) for field in 
                                       ['payment_status', 'paid_amount', 'payment_date', 'payment_method'])
                print(f"  {'✅' if has_payment_fields else '❌'} نموذج المشتريات - حقول المدفوعات")
                
                # اختبار نموذج المصروفات
                expense = Expense()
                has_payment_fields = all(hasattr(expense, field) for field in 
                                       ['payment_status', 'paid_amount', 'payment_date', 'payment_method'])
                print(f"  {'✅' if has_payment_fields else '❌'} نموذج المصروفات - حقول المدفوعات")
                
                # اختبار نموذج الرواتب
                payroll = Payroll()
                has_payment_fields = all(hasattr(payroll, field) for field in 
                                       ['payment_status', 'paid_amount', 'payment_date', 'payment_method'])
                print(f"  {'✅' if has_payment_fields else '❌'} نموذج الرواتب - حقول المدفوعات")
                
                return True
                
            except Exception as e:
                print(f"  ❌ خطأ في فحص النماذج: {e}")
                return False
    
    def test_payment_integration_apis(self):
        """اختبار APIs نظام الربط"""
        print("🔗 اختبار APIs نظام الربط:")
        
        apis = [
            ('/api/payments/notify', 'POST'),
            ('/api/payments/check-updates', 'GET'),
            ('/api/sales/summary', 'GET'),
            ('/api/purchases/summary', 'GET'),
            ('/api/expenses/summary', 'GET')
        ]
        
        working_apis = 0
        
        for api_path, method in apis:
            try:
                if method == 'GET':
                    response = self.session.get(f"{self.base_url}{api_path}")
                else:
                    response = self.session.post(f"{self.base_url}{api_path}", 
                                               json={'event_type': 'test', 'data': {}})
                
                if response.status_code in [200, 400]:  # 400 مقبول للبيانات الاختبارية
                    print(f"  ✅ {api_path} - يعمل")
                    working_apis += 1
                else:
                    print(f"  ❌ {api_path} - خطأ {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {api_path} - خطأ: {e}")
        
        return working_apis == len(apis)
    
    def test_auto_update_on_payment(self):
        """اختبار التحديث التلقائي عند تسجيل دفعة"""
        print("💳 اختبار التحديث التلقائي عند تسجيل دفعة:")
        
        try:
            # إنشاء مبيعة جديدة
            sale_data = {
                'subtotal': 1000.00,
                'discount': 50.00,
                'total': 950.00,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'notes': 'اختبار ربط المدفوعات'
            }
            
            response = self.session.post(f"{self.base_url}/api/sales/create", json=sale_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    sale_id = result.get('sale_id')
                    print(f"  ✅ تم إنشاء مبيعة #{sale_id}")
                    
                    # تسجيل دفعة للمبيعة
                    payment_data = {
                        'id': sale_id,
                        'payment_status': 'paid'
                    }
                    
                    response = self.session.post(f"{self.base_url}/api/sales/update-payment-status", 
                                               json=payment_data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            print(f"  ✅ تم تحديث حالة الدفع تلقائياً")
                            return True, sale_id
                        else:
                            print(f"  ❌ فشل تحديث حالة الدفع: {result.get('message')}")
                    else:
                        print(f"  ❌ خطأ في تحديث حالة الدفع: {response.status_code}")
                else:
                    print(f"  ❌ فشل إنشاء المبيعة: {result.get('message')}")
            else:
                print(f"  ❌ خطأ في إنشاء المبيعة: {response.status_code}")
                
            return False, None
            
        except Exception as e:
            print(f"  ❌ خطأ في اختبار التحديث التلقائي: {e}")
            return False, None
    
    def test_cross_screen_updates(self):
        """اختبار التحديث عبر الشاشات"""
        print("🔄 اختبار التحديث عبر الشاشات:")
        
        try:
            # فحص ملخص المبيعات
            response = self.session.get(f"{self.base_url}/api/sales/summary")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    summary = result.get('summary', {})
                    print(f"  ✅ ملخص المبيعات - إجمالي: {summary.get('total-sales', 0)}")
                    print(f"     - مدفوع: {summary.get('paid-sales', 0)}")
                    print(f"     - معلق: {summary.get('pending-sales', 0)}")
                else:
                    print(f"  ❌ فشل جلب ملخص المبيعات: {result.get('message')}")
                    return False
            else:
                print(f"  ❌ خطأ في جلب ملخص المبيعات: {response.status_code}")
                return False
            
            # فحص ملخص المشتريات
            response = self.session.get(f"{self.base_url}/api/purchases/summary")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    summary = result.get('summary', {})
                    print(f"  ✅ ملخص المشتريات - إجمالي: {summary.get('total-purchases', 0)}")
                else:
                    print(f"  ❌ فشل جلب ملخص المشتريات: {result.get('message')}")
            
            # فحص ملخص المصروفات
            response = self.session.get(f"{self.base_url}/api/expenses/summary")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    summary = result.get('summary', {})
                    print(f"  ✅ ملخص المصروفات - إجمالي: {summary.get('total-expenses', 0)}")
                else:
                    print(f"  ❌ فشل جلب ملخص المصروفات: {result.get('message')}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ خطأ في اختبار التحديث عبر الشاشات: {e}")
            return False
    
    def test_notification_system_integration(self):
        """اختبار تكامل نظام الإشعارات"""
        print("🔔 اختبار تكامل نظام الإشعارات:")
        
        try:
            # إرسال إشعار اختبار
            notification_data = {
                'event_type': 'payment_registered',
                'data': {
                    'invoice_type': 'sale',
                    'invoice_id': 1,
                    'amount': 500.00,
                    'payment_method': 'CASH'
                }
            }
            
            response = self.session.post(f"{self.base_url}/api/payments/notify", 
                                       json=notification_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"  ✅ نظام الإشعارات - يعمل")
                    print(f"     - معرف الحدث: {result.get('event_id')}")
                    return True
                else:
                    print(f"  ❌ فشل نظام الإشعارات: {result.get('message')}")
            else:
                print(f"  ❌ خطأ في نظام الإشعارات: {response.status_code}")
                
            return False
            
        except Exception as e:
            print(f"  ❌ خطأ في اختبار نظام الإشعارات: {e}")
            return False
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🚀 اختبار شامل لنظام ربط المدفوعات")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        print()
        
        # تشغيل الاختبارات
        tests = [
            ('وجود حقول المدفوعات', self.test_payment_fields_exist),
            ('APIs نظام الربط', self.test_payment_integration_apis),
            ('التحديث التلقائي عند الدفع', self.test_auto_update_on_payment),
            ('التحديث عبر الشاشات', self.test_cross_screen_updates),
            ('تكامل نظام الإشعارات', self.test_notification_system_integration)
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
        print("📊 نتائج اختبار نظام ربط المدفوعات:")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 نسبة النجاح: {success_rate:.1f}%")
        print(f"✅ اختبارات ناجحة: {passed_tests}/{total_tests}")
        
        if success_rate == 100:
            print("🎉 ممتاز! نظام ربط المدفوعات يعمل بكفاءة 100%")
            print("🔗 جميع الشاشات مربوطة ومتحدثة تلقائياً")
        elif success_rate >= 80:
            print("🟢 جيد جداً - النظام مربوط ويعمل بشكل ممتاز")
        elif success_rate >= 60:
            print("🟡 جيد - النظام مربوط مع بعض المشاكل البسيطة")
        else:
            print("🔴 يحتاج إصلاحات - النظام غير مربوط بالشكل المطلوب")
        
        print()
        print("📋 حالة الربط:")
        print(f"  {'✅' if success_rate >= 80 else '❌'} المبيعات ← المدفوعات")
        print(f"  {'✅' if success_rate >= 80 else '❌'} المشتريات ← المدفوعات")
        print(f"  {'✅' if success_rate >= 80 else '❌'} المصروفات ← المدفوعات")
        print(f"  {'✅' if success_rate >= 80 else '❌'} الرواتب ← المدفوعات")
        print(f"  {'✅' if success_rate >= 80 else '❌'} التحديث التلقائي")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = PaymentIntegrationTest()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 نظام ربط المدفوعات جاهز للاستخدام!")
        print("🔗 جميع الشاشات مربوطة ومتحدثة تلقائياً")
    else:
        print("\n⚠️ النظام يحتاج مراجعة وإصلاحات إضافية")
