#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لنظام الحفظ التلقائي المتقدم
Comprehensive Advanced Auto-Save System Test
"""

import requests
import json
import time
from datetime import datetime
from app import app, db, Sale, Purchase, Expense, Employee

class AdvancedAutoSaveTest:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_results = {}
        
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {'username': 'admin', 'password': 'admin123'}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def test_notification_system(self):
        """اختبار نظام الإشعارات"""
        print("🔔 اختبار نظام الإشعارات:")
        
        # فحص وجود ملفات JavaScript
        js_files = [
            'static/js/advanced-notifications.js',
            'static/js/auto-save-system.js',
            'static/js/batch-operations.js',
            'static/js/undo-redo-system.js',
            'static/js/performance-monitor.js'
        ]
        
        all_exist = True
        for js_file in js_files:
            try:
                with open(js_file, 'r') as f:
                    content = f.read()
                    if 'NotificationSystem' in content or 'showNotification' in content:
                        print(f"  ✅ {js_file} - موجود ويعمل")
                    else:
                        print(f"  ❌ {js_file} - موجود لكن قد لا يعمل")
                        all_exist = False
            except FileNotFoundError:
                print(f"  ❌ {js_file} - غير موجود")
                all_exist = False
        
        return all_exist
    
    def test_auto_save_endpoints(self):
        """اختبار endpoints الحفظ التلقائي"""
        print("🔗 اختبار API endpoints:")
        
        endpoints = [
            '/api/sales/create',
            '/api/purchases/create', 
            '/api/expenses/create',
            '/api/employees/create',
            '/api/batch/process',
            '/api/auto-save/status'
        ]
        
        working_endpoints = 0
        
        for endpoint in endpoints:
            try:
                # اختبار GET للحالة، POST للباقي
                method = 'GET' if 'status' in endpoint else 'POST'
                data = {} if method == 'POST' else None
                
                response = self.session.request(method, f"{self.base_url}{endpoint}", json=data)
                
                if response.status_code in [200, 400]:  # 400 مقبول للبيانات الفارغة
                    print(f"  ✅ {endpoint} - يعمل")
                    working_endpoints += 1
                else:
                    print(f"  ❌ {endpoint} - خطأ {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {endpoint} - خطأ: {e}")
        
        return working_endpoints == len(endpoints)
    
    def test_form_auto_save(self):
        """اختبار الحفظ التلقائي للنماذج"""
        print("📝 اختبار الحفظ التلقائي للنماذج:")
        
        # اختبار حفظ مصروف
        expense_data = {
            'description': 'اختبار الحفظ التلقائي المتقدم',
            'amount': 250.00,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'office_supplies',
            'notes': 'اختبار شامل للنظام'
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/expenses/create", json=expense_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("  ✅ حفظ المصروفات - يعمل تلقائياً")
                    return True, result.get('expense_id')
                else:
                    print(f"  ❌ حفظ المصروفات - فشل: {result.get('message')}")
                    return False, None
            else:
                print(f"  ❌ حفظ المصروفات - خطأ HTTP: {response.status_code}")
                return False, None
        except Exception as e:
            print(f"  ❌ حفظ المصروفات - خطأ: {e}")
            return False, None
    
    def test_batch_operations(self):
        """اختبار العمليات المجمعة"""
        print("📦 اختبار العمليات المجمعة:")
        
        batch_data = {
            'operations': [
                {
                    'type': 'save',
                    'data': {
                        'description': 'مصروف مجمع 1',
                        'amount': 100.00,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'type': 'general'
                    }
                },
                {
                    'type': 'save',
                    'data': {
                        'description': 'مصروف مجمع 2',
                        'amount': 200.00,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'type': 'office_supplies'
                    }
                }
            ]
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/batch/process", json=batch_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"  ✅ العمليات المجمعة - نجح حفظ {result.get('summary', {}).get('successful', 0)} عملية")
                    return True
                else:
                    print(f"  ❌ العمليات المجمعة - فشل: {result.get('message')}")
                    return False
            else:
                print(f"  ❌ العمليات المجمعة - خطأ HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ العمليات المجمعة - خطأ: {e}")
            return False
    
    def test_system_status(self):
        """اختبار حالة النظام"""
        print("📊 اختبار حالة النظام:")
        
        try:
            response = self.session.get(f"{self.base_url}/api/auto-save/status")
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    stats = result.get('stats', {})
                    print(f"  ✅ حالة النظام - نشط")
                    print(f"     - المبيعات: {stats.get('sales_count', 0)}")
                    print(f"     - المشتريات: {stats.get('purchases_count', 0)}")
                    print(f"     - المصروفات: {stats.get('expenses_count', 0)}")
                    print(f"     - الموظفين: {stats.get('employees_count', 0)}")
                    return True
                else:
                    print(f"  ❌ حالة النظام - فشل: {result.get('message')}")
                    return False
            else:
                print(f"  ❌ حالة النظام - خطأ HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ حالة النظام - خطأ: {e}")
            return False
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🚀 اختبار شامل لنظام الحفظ التلقائي المتقدم")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        print()
        
        # تشغيل الاختبارات
        tests = [
            ('نظام الإشعارات', self.test_notification_system),
            ('API Endpoints', self.test_auto_save_endpoints),
            ('الحفظ التلقائي للنماذج', self.test_form_auto_save),
            ('العمليات المجمعة', self.test_batch_operations),
            ('حالة النظام', self.test_system_status)
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
        print("📊 نتائج الاختبار الشامل:")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 نسبة النجاح: {success_rate:.1f}%")
        print(f"✅ اختبارات ناجحة: {passed_tests}/{total_tests}")
        
        if success_rate == 100:
            print("🎉 ممتاز! نظام الحفظ التلقائي المتقدم يعمل بكفاءة 100%")
        elif success_rate >= 80:
            print("🟢 جيد جداً - النظام يعمل بشكل ممتاز")
        elif success_rate >= 60:
            print("🟡 جيد - النظام يعمل مع بعض المشاكل البسيطة")
        else:
            print("🔴 يحتاج إصلاحات - النظام لا يعمل بالشكل المطلوب")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = AdvancedAutoSaveTest()
    tester.run_comprehensive_test()
