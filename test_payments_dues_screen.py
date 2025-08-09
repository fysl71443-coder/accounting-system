#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شاشة المدفوعات والمستحقات - اختبار شامل 100%
Comprehensive Payments and Dues Screen Testing Script
"""

import requests
import json
import time
import sys
import os
from datetime import datetime, date
from urllib.parse import urljoin

class PaymentsDuesScreenTester:
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
            login_page = self.session.get(urljoin(self.base_url, "/login"))
            if login_page.status_code != 200:
                self.log_test("تسجيل الدخول", "FAIL", f"لا يمكن الوصول لصفحة تسجيل الدخول: {login_page.status_code}")
                return False
            
            login_data = {
                'username': username,
                'password': password
            }
            
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data)
            
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
    
    def test_payments_dues_page_access(self):
        """فحص الوصول لشاشة المدفوعات والمستحقات"""
        print("\n📄 فحص الوصول لشاشة المدفوعات والمستحقات...")
        
        try:
            response = self.session.get(urljoin(self.base_url, "/payments_dues"))
            
            if response.status_code == 200:
                content = response.text
                
                # فحص العنوان
                if "المدفوعات والمستحقات" in content or "Payments" in content:
                    self.log_test("عنوان الصفحة", "PASS", "عنوان المدفوعات والمستحقات موجود")
                else:
                    self.log_test("عنوان الصفحة", "FAIL", "عنوان المدفوعات والمستحقات غير موجود")
                
                # فحص التبويبات
                tabs = ["sales", "purchases", "expenses", "payroll"]
                for tab in tabs:
                    if f'id="{tab}"' in content:
                        self.log_test(f"تبويب {tab}", "PASS", f"تبويب {tab} موجود")
                    else:
                        self.log_test(f"تبويب {tab}", "FAIL", f"تبويب {tab} غير موجود")
                
                # فحص أزرار الطباعة
                print_buttons = content.count('openPrintModal')
                if print_buttons >= 4:
                    self.log_test("أزرار الطباعة", "PASS", f"تم العثور على {print_buttons} زر طباعة")
                else:
                    self.log_test("أزرار الطباعة", "FAIL", f"عدد أزرار الطباعة غير كافي: {print_buttons}")
                
                # فحص الفلاتر
                filters = ["sales-status-filter", "purchases-status-filter", "expenses-status-filter"]
                for filter_id in filters:
                    if filter_id in content:
                        self.log_test(f"فلتر {filter_id}", "PASS", f"فلتر {filter_id} موجود")
                    else:
                        self.log_test(f"فلتر {filter_id}", "FAIL", f"فلتر {filter_id} غير موجود")
                
                # فحص النافذة المنبثقة للطباعة
                if "printModal" in content:
                    self.log_test("نافذة الطباعة", "PASS", "نافذة الطباعة موجودة")
                else:
                    self.log_test("نافذة الطباعة", "FAIL", "نافذة الطباعة غير موجودة")
                
                return True
                
            else:
                self.log_test("الوصول للصفحة", "FAIL", f"لا يمكن الوصول لشاشة المدفوعات: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("الوصول للصفحة", "FAIL", f"خطأ في الوصول للصفحة: {e}")
            return False
    
    def test_print_routes(self):
        """فحص routes الطباعة"""
        print("\n🖨️ فحص routes الطباعة...")
        
        # معاملات اختبار
        test_params = {
            'type': 'sales',
            'month': '2025-08',
            'status': 'all',
            'details': 'true'
        }
        
        # فحص route المعاينة
        try:
            preview_url = f"/print_invoices_preview?type={test_params['type']}&month={test_params['month']}&status={test_params['status']}&details={test_params['details']}"
            response = self.session.get(urljoin(self.base_url, preview_url))
            
            if response.status_code == 200:
                self.log_test("route معاينة الطباعة", "PASS", "route المعاينة يعمل")
            else:
                self.log_test("route معاينة الطباعة", "FAIL", f"route المعاينة لا يعمل: {response.status_code}")
                
        except Exception as e:
            self.log_test("route معاينة الطباعة", "FAIL", f"خطأ في route المعاينة: {e}")
        
        # فحص route الطباعة
        try:
            print_url = f"/print_invoices?type={test_params['type']}&month={test_params['month']}&status={test_params['status']}&details={test_params['details']}"
            response = self.session.get(urljoin(self.base_url, print_url))
            
            if response.status_code == 200:
                self.log_test("route الطباعة", "PASS", "route الطباعة يعمل")
            else:
                self.log_test("route الطباعة", "FAIL", f"route الطباعة لا يعمل: {response.status_code}")
                
        except Exception as e:
            self.log_test("route الطباعة", "FAIL", f"خطأ في route الطباعة: {e}")
    
    def test_data_availability(self):
        """فحص توفر البيانات"""
        print("\n📊 فحص توفر البيانات...")
        
        # فحص المبيعات
        try:
            response = self.session.get(urljoin(self.base_url, "/api/sales/list"))
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        sales_count = len(data.get('data', []))
                        self.log_test("بيانات المبيعات", "PASS", f"تم جلب {sales_count} فاتورة مبيعات")
                    else:
                        self.log_test("بيانات المبيعات", "WARN", "API المبيعات يعمل لكن لا توجد بيانات")
                except:
                    self.log_test("بيانات المبيعات", "WARN", "API المبيعات يعمل لكن البيانات غير صحيحة")
            else:
                self.log_test("بيانات المبيعات", "FAIL", f"API المبيعات لا يعمل: {response.status_code}")
        except Exception as e:
            self.log_test("بيانات المبيعات", "FAIL", f"خطأ في API المبيعات: {e}")
        
        # فحص المشتريات
        try:
            response = self.session.get(urljoin(self.base_url, "/api/purchases/list"))
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        purchases_count = len(data.get('data', []))
                        self.log_test("بيانات المشتريات", "PASS", f"تم جلب {purchases_count} فاتورة مشتريات")
                    else:
                        self.log_test("بيانات المشتريات", "WARN", "API المشتريات يعمل لكن لا توجد بيانات")
                except:
                    self.log_test("بيانات المشتريات", "WARN", "API المشتريات يعمل لكن البيانات غير صحيحة")
            else:
                self.log_test("بيانات المشتريات", "FAIL", f"API المشتريات لا يعمل: {response.status_code}")
        except Exception as e:
            self.log_test("بيانات المشتريات", "FAIL", f"خطأ في API المشتريات: {e}")
        
        # فحص المصروفات
        try:
            response = self.session.get(urljoin(self.base_url, "/api/expenses/list"))
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        expenses_count = len(data.get('data', []))
                        self.log_test("بيانات المصروفات", "PASS", f"تم جلب {expenses_count} مصروف")
                    else:
                        self.log_test("بيانات المصروفات", "WARN", "API المصروفات يعمل لكن لا توجد بيانات")
                except:
                    self.log_test("بيانات المصروفات", "WARN", "API المصروفات يعمل لكن البيانات غير صحيحة")
            else:
                self.log_test("بيانات المصروفات", "FAIL", f"API المصروفات لا يعمل: {response.status_code}")
        except Exception as e:
            self.log_test("بيانات المصروفات", "FAIL", f"خطأ في API المصروفات: {e}")
    
    def test_javascript_functions(self):
        """فحص وجود وظائف JavaScript"""
        print("\n🔧 فحص وظائف JavaScript...")
        
        try:
            response = self.session.get(urljoin(self.base_url, "/payments_dues"))
            if response.status_code == 200:
                content = response.text
                
                # فحص وظائف الطباعة
                js_functions = [
                    "openPrintModal",
                    "generatePrintReport", 
                    "printReport",
                    "filterSalesTable",
                    "filterPurchasesTable",
                    "filterExpensesTable",
                    "updateFilterCount"
                ]
                
                for func in js_functions:
                    if f"function {func}" in content:
                        self.log_test(f"وظيفة {func}", "PASS", f"وظيفة {func} موجودة")
                    else:
                        self.log_test(f"وظيفة {func}", "FAIL", f"وظيفة {func} غير موجودة")
                
                # فحص Bootstrap
                if "bootstrap" in content.lower():
                    self.log_test("Bootstrap", "PASS", "Bootstrap محمل")
                else:
                    self.log_test("Bootstrap", "WARN", "Bootstrap قد لا يكون محمل")
                
                # فحص jQuery (إذا كان مطلوب)
                if "jquery" in content.lower():
                    self.log_test("jQuery", "PASS", "jQuery محمل")
                else:
                    self.log_test("jQuery", "WARN", "jQuery غير محمل")
                
        except Exception as e:
            self.log_test("فحص JavaScript", "FAIL", f"خطأ في فحص JavaScript: {e}")
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n" + "="*80)
        print("📊 تقرير فحص شاشة المدفوعات والمستحقات الشامل")
        print("📊 Comprehensive Payments and Dues Screen Test Report")
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
            print("   🚀 شاشة المدفوعات والمستحقات جاهزة للاستخدام")
        else:
            print("   🔧 يحتاج إصلاح الاختبارات الفاشلة")
            print("   📋 مراجعة الأخطاء المذكورة أعلاه")
        
        if warning_tests > 0:
            print("   ⚠️ مراجعة التحذيرات لتحسين الأداء")
        
        # حفظ التقرير في ملف
        try:
            report_filename = f"payments_dues_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        
        return passed_tests/total_tests >= 0.8  # نجاح إذا كان 80% أو أكثر
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء فحص شاشة المدفوعات والمستحقات الشامل...")
        print("🚀 Starting comprehensive payments and dues screen testing...")
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return False
        
        # تشغيل الاختبارات
        self.test_payments_dues_page_access()
        self.test_print_routes()
        self.test_data_availability()
        self.test_javascript_functions()
        
        # إنشاء التقرير
        return self.generate_report()

def main():
    """الوظيفة الرئيسية"""
    print("="*80)
    print("🔍 فاحص شاشة المدفوعات والمستحقات الشامل")
    print("🔍 Comprehensive Payments and Dues Screen Tester")
    print("="*80)
    
    # إنشاء الفاحص
    tester = PaymentsDuesScreenTester()
    
    # تشغيل الاختبارات
    success = tester.run_all_tests()
    
    print("\n" + "="*80)
    if success:
        print("✅ اكتمل الفحص بنجاح - شاشة المدفوعات تعمل بشكل جيد")
        print("✅ Testing completed successfully - Payments screen is working well")
    else:
        print("⚠️ اكتمل الفحص مع وجود مشاكل - يحتاج مراجعة")
        print("⚠️ Testing completed with issues - needs review")
    print("="*80)

if __name__ == "__main__":
    main()
