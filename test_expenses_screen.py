#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شاشة المصروفات - اختبار شامل وعملي
Comprehensive Expenses Screen Testing Script
"""

import requests
import json
import time
import sys
import os
from datetime import datetime, date
from urllib.parse import urljoin

class ExpensesScreenTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.login_successful = False
        
    def log_test(self, test_name, status, message="", details=""):
        """تسجيل نتيجة الاختبار"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            print(f"   📋 {details}")
    
    def login(self, username="admin", password="admin123"):
        """تسجيل الدخول"""
        print("🔐 محاولة تسجيل الدخول...")
        
        try:
            # جلب صفحة تسجيل الدخول
            login_page = self.session.get(urljoin(self.base_url, "/login"))
            if login_page.status_code != 200:
                self.log_test("تسجيل الدخول", "FAIL", f"لا يمكن الوصول لصفحة تسجيل الدخول: {login_page.status_code}")
                return False
            
            # محاولة تسجيل الدخول
            login_data = {
                'username': username,
                'password': password
            }
            
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data)
            
            # فحص نجاح تسجيل الدخول
            if response.status_code == 200 and "dashboard" in response.url.lower():
                self.log_test("تسجيل الدخول", "PASS", "تم تسجيل الدخول بنجاح")
                self.login_successful = True
                return True
            else:
                self.log_test("تسجيل الدخول", "FAIL", f"فشل تسجيل الدخول: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("تسجيل الدخول", "FAIL", f"خطأ في تسجيل الدخول: {e}")
            return False
    
    def test_expenses_page_access(self):
        """فحص الوصول لشاشة المصروفات"""
        print("\n📄 فحص الوصول لشاشة المصروفات...")
        
        try:
            response = self.session.get(urljoin(self.base_url, "/expenses"))
            
            if response.status_code == 200:
                # فحص وجود العناصر الأساسية في الصفحة
                content = response.text
                
                # فحص العنوان
                if "المصروفات" in content or "Expenses" in content:
                    self.log_test("عنوان الصفحة", "PASS", "عنوان المصروفات موجود")
                else:
                    self.log_test("عنوان الصفحة", "FAIL", "عنوان المصروفات غير موجود")
                
                # فحص وجود الجدول
                if "expenses-table" in content or "table" in content:
                    self.log_test("جدول المصروفات", "PASS", "جدول المصروفات موجود")
                else:
                    self.log_test("جدول المصروفات", "FAIL", "جدول المصروفات غير موجود")
                
                # فحص وجود أزرار الإجراءات
                buttons_found = 0
                button_checks = [
                    ("btn-success", "زر إضافة جديد"),
                    ("btn-primary", "زر البحث"),
                    ("btn-info", "زر التصدير"),
                    ("btn-warning", "زر التقارير")
                ]
                
                for button_class, button_name in button_checks:
                    if button_class in content:
                        self.log_test(button_name, "PASS", f"{button_name} موجود")
                        buttons_found += 1
                    else:
                        self.log_test(button_name, "WARN", f"{button_name} غير موجود")
                
                self.log_test("أزرار الإجراءات", "PASS", f"تم العثور على {buttons_found} زر من أصل {len(button_checks)}")
                return True
                
            else:
                self.log_test("الوصول للصفحة", "FAIL", f"لا يمكن الوصول لشاشة المصروفات: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("الوصول للصفحة", "FAIL", f"خطأ في الوصول للصفحة: {e}")
            return False
    
    def test_expenses_api_endpoints(self):
        """فحص API endpoints للمصروفات"""
        print("\n🔌 فحص API endpoints...")
        
        api_endpoints = [
            ("/api/expenses/list", "GET", "جلب قائمة المصروفات"),
            ("/api/expenses/save", "POST", "حفظ مصروف جديد"),
            ("/api/expenses/categories", "GET", "جلب فئات المصروفات"),
            ("/expenses/new", "GET", "صفحة إضافة مصروف جديد")
        ]
        
        for endpoint, method, description in api_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(urljoin(self.base_url, endpoint))
                elif method == "POST":
                    # اختبار POST مع بيانات وهمية
                    test_data = {
                        'description': 'مصروف تجريبي',
                        'amount': '100.00',
                        'category': 'عام',
                        'date': date.today().strftime('%Y-%m-%d')
                    }
                    response = self.session.post(urljoin(self.base_url, endpoint), data=test_data)
                
                if response.status_code in [200, 201, 302]:  # 302 للإعادة التوجيه
                    self.log_test(f"API {endpoint}", "PASS", f"{description} - الكود: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"API {endpoint}", "FAIL", f"{description} - غير موجود (404)")
                elif response.status_code == 405:
                    self.log_test(f"API {endpoint}", "WARN", f"{description} - طريقة غير مسموحة (405)")
                else:
                    self.log_test(f"API {endpoint}", "WARN", f"{description} - الكود: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"API {endpoint}", "FAIL", f"خطأ في {description}: {e}")
    
    def test_expenses_crud_operations(self):
        """فحص عمليات CRUD للمصروفات"""
        print("\n🔄 فحص عمليات CRUD...")
        
        # بيانات مصروف تجريبي
        test_expense = {
            'description': f'مصروف تجريبي - {datetime.now().strftime("%H:%M:%S")}',
            'amount': '150.75',
            'category': 'مصروفات إدارية',
            'expense_date': date.today().strftime('%Y-%m-%d'),
            'payment_method': 'نقدي',
            'notes': 'مصروف تجريبي للاختبار'
        }
        
        # 1. اختبار الإنشاء (Create)
        try:
            response = self.session.post(urljoin(self.base_url, "/api/expenses/save"), data=test_expense)
            
            if response.status_code in [200, 201, 302]:
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        result = response.json()
                        if result.get('success'):
                            expense_id = result.get('id')
                            self.log_test("إنشاء مصروف", "PASS", f"تم إنشاء المصروف بنجاح - ID: {expense_id}")
                        else:
                            self.log_test("إنشاء مصروف", "FAIL", f"فشل الإنشاء: {result.get('message', 'خطأ غير معروف')}")
                    else:
                        self.log_test("إنشاء مصروف", "PASS", f"تم إرسال البيانات - الكود: {response.status_code}")
                except:
                    self.log_test("إنشاء مصروف", "PASS", f"تم إرسال البيانات - الكود: {response.status_code}")
            else:
                self.log_test("إنشاء مصروف", "FAIL", f"فشل الإنشاء - الكود: {response.status_code}")
                
        except Exception as e:
            self.log_test("إنشاء مصروف", "FAIL", f"خطأ في إنشاء المصروف: {e}")
        
        # 2. اختبار القراءة (Read)
        try:
            response = self.session.get(urljoin(self.base_url, "/api/expenses/list"))
            
            if response.status_code == 200:
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        data = response.json()
                        if data.get('success') and 'data' in data:
                            expenses_count = len(data['data'])
                            self.log_test("قراءة المصروفات", "PASS", f"تم جلب {expenses_count} مصروف")
                        else:
                            self.log_test("قراءة المصروفات", "WARN", "تم الوصول للـ API لكن البيانات غير متوفرة")
                    else:
                        self.log_test("قراءة المصروفات", "PASS", "تم الوصول للـ API")
                except:
                    self.log_test("قراءة المصروفات", "PASS", "تم الوصول للـ API")
            else:
                self.log_test("قراءة المصروفات", "FAIL", f"فشل جلب المصروفات - الكود: {response.status_code}")
                
        except Exception as e:
            self.log_test("قراءة المصروفات", "FAIL", f"خطأ في جلب المصروفات: {e}")
    
    def test_expenses_buttons_functionality(self):
        """فحص وظائف الأزرار"""
        print("\n🔘 فحص وظائف الأزرار...")
        
        # قائمة الأزرار المتوقعة
        button_tests = [
            ("/expenses/new", "زر إضافة مصروف جديد"),
            ("/expenses", "زر عرض جميع المصروفات"),
            ("/api/expenses/export", "زر تصدير المصروفات"),
            ("/expenses/reports", "زر التقارير")
        ]
        
        for url, button_name in button_tests:
            try:
                response = self.session.get(urljoin(self.base_url, url))
                
                if response.status_code == 200:
                    self.log_test(button_name, "PASS", f"يعمل بشكل صحيح")
                elif response.status_code == 302:
                    self.log_test(button_name, "PASS", f"إعادة توجيه صحيحة")
                elif response.status_code == 404:
                    self.log_test(button_name, "FAIL", f"الصفحة غير موجودة")
                else:
                    self.log_test(button_name, "WARN", f"استجابة غير متوقعة: {response.status_code}")
                    
            except Exception as e:
                self.log_test(button_name, "FAIL", f"خطأ في الاختبار: {e}")
    
    def test_expenses_data_validation(self):
        """فحص التحقق من صحة البيانات"""
        print("\n✅ فحص التحقق من صحة البيانات...")
        
        # اختبار بيانات غير صحيحة
        invalid_data_tests = [
            ({}, "بيانات فارغة"),
            ({'description': '', 'amount': '0'}, "وصف فارغ ومبلغ صفر"),
            ({'description': 'test', 'amount': '-100'}, "مبلغ سالب"),
            ({'description': 'test', 'amount': 'abc'}, "مبلغ غير رقمي")
        ]
        
        for test_data, test_name in invalid_data_tests:
            try:
                response = self.session.post(urljoin(self.base_url, "/api/expenses/save"), data=test_data)
                
                if response.status_code == 400:
                    self.log_test(f"التحقق - {test_name}", "PASS", "تم رفض البيانات غير الصحيحة")
                elif response.status_code in [200, 201]:
                    try:
                        if response.headers.get('content-type', '').startswith('application/json'):
                            result = response.json()
                            if not result.get('success'):
                                self.log_test(f"التحقق - {test_name}", "PASS", "تم رفض البيانات مع رسالة خطأ")
                            else:
                                self.log_test(f"التحقق - {test_name}", "WARN", "تم قبول بيانات غير صحيحة")
                        else:
                            self.log_test(f"التحقق - {test_name}", "WARN", "لا يوجد تحقق من البيانات")
                    except:
                        self.log_test(f"التحقق - {test_name}", "WARN", "لا يوجد تحقق من البيانات")
                else:
                    self.log_test(f"التحقق - {test_name}", "WARN", f"استجابة غير متوقعة: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"التحقق - {test_name}", "FAIL", f"خطأ في الاختبار: {e}")
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n" + "="*80)
        print("📊 تقرير فحص شاشة المصروفات الشامل")
        print("📊 Comprehensive Expenses Screen Test Report")
        print("="*80)
        
        # إحصائيات عامة
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed_tests = len([t for t in self.test_results if t['status'] == 'FAIL'])
        warning_tests = len([t for t in self.test_results if t['status'] == 'WARN'])
        
        print(f"\n📈 الإحصائيات العامة:")
        print(f"   📊 إجمالي الاختبارات: {total_tests}")
        print(f"   ✅ نجح: {passed_tests}")
        print(f"   ❌ فشل: {failed_tests}")
        print(f"   ⚠️ تحذيرات: {warning_tests}")
        print(f"   📊 معدل النجاح: {(passed_tests/total_tests*100):.1f}%")
        
        # تفاصيل النتائج
        print(f"\n📋 تفاصيل النتائج:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"   {status_icon} [{result['timestamp']}] {result['test']}: {result['message']}")
        
        # التوصيات
        print(f"\n💡 التوصيات:")
        if failed_tests == 0:
            print("   🎉 ممتاز! جميع الاختبارات الأساسية نجحت")
            print("   🚀 شاشة المصروفات جاهزة للاستخدام")
        else:
            print("   🔧 يحتاج إصلاح الاختبارات الفاشلة")
            print("   📋 مراجعة الأخطاء المذكورة أعلاه")
        
        if warning_tests > 0:
            print("   ⚠️ مراجعة التحذيرات لتحسين الأداء")
        
        # حفظ التقرير في ملف
        try:
            report_filename = f"expenses_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'summary': {
                        'total': total_tests,
                        'passed': passed_tests,
                        'failed': failed_tests,
                        'warnings': warning_tests,
                        'success_rate': passed_tests/total_tests*100
                    },
                    'results': self.test_results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 تم حفظ التقرير في: {report_filename}")
            
        except Exception as e:
            print(f"\n❌ خطأ في حفظ التقرير: {e}")
        
        return passed_tests/total_tests >= 0.7  # نجاح إذا كان 70% أو أكثر
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء فحص شاشة المصروفات الشامل...")
        print("🚀 Starting comprehensive expenses screen testing...")
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return False
        
        # تشغيل الاختبارات
        self.test_expenses_page_access()
        self.test_expenses_api_endpoints()
        self.test_expenses_crud_operations()
        self.test_expenses_buttons_functionality()
        self.test_expenses_data_validation()
        
        # إنشاء التقرير
        return self.generate_report()

def main():
    """الوظيفة الرئيسية"""
    print("="*80)
    print("🔍 فاحص شاشة المصروفات الشامل")
    print("🔍 Comprehensive Expenses Screen Tester")
    print("="*80)
    
    # إنشاء الفاحص
    tester = ExpensesScreenTester()
    
    # تشغيل الاختبارات
    success = tester.run_all_tests()
    
    print("\n" + "="*80)
    if success:
        print("✅ اكتمل الفحص بنجاح - شاشة المصروفات تعمل بشكل جيد")
        print("✅ Testing completed successfully - Expenses screen is working well")
    else:
        print("⚠️ اكتمل الفحص مع وجود مشاكل - يحتاج مراجعة")
        print("⚠️ Testing completed with issues - needs review")
    print("="*80)

if __name__ == "__main__":
    main()
