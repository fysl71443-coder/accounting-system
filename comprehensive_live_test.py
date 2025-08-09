#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار عملي شامل لجميع الأزرار في جميع الشاشات
Comprehensive Live Testing for All Buttons in All Screens
"""

import requests
import json
import time
import webbrowser
from datetime import datetime

class ComprehensiveLiveTester:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'http://localhost:5000'
        self.test_results = []
        self.login_successful = False
        
    def log_test(self, screen, button, status, details="", response_time=0):
        """تسجيل نتيجة الاختبار"""
        result = {
            'screen': screen,
            'button': button,
            'status': status,
            'details': details,
            'response_time': response_time,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {screen} - {button}: {details} ({response_time:.2f}s)")
    
    def login(self):
        """تسجيل الدخول"""
        print("🔐 اختبار تسجيل الدخول...")
        
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'language': 'ar'
        }
        
        try:
            start_time = time.time()
            response = self.session.post(f'{self.base_url}/login', data=login_data)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.login_successful = True
                self.log_test("تسجيل الدخول", "زر تسجيل الدخول", "PASS", "تم بنجاح", response_time)
                return True
            else:
                self.log_test("تسجيل الدخول", "زر تسجيل الدخول", "FAIL", f"فشل - كود: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("تسجيل الدخول", "زر تسجيل الدخول", "FAIL", f"خطأ: {str(e)}", 0)
            return False
    
    def test_dashboard_buttons(self):
        """اختبار أزرار لوحة التحكم"""
        print("\n🏠 اختبار أزرار لوحة التحكم...")
        
        try:
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/dashboard')
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_test("لوحة التحكم", "تحميل الصفحة", "FAIL", f"كود: {response.status_code}", response_time)
                return
            
            self.log_test("لوحة التحكم", "تحميل الصفحة", "PASS", "تم التحميل بنجاح", response_time)
            
            # اختبار الروابط السريعة
            quick_links = [
                ('/new_sale', 'رابط فاتورة جديدة'),
                ('/unified_products', 'رابط الشاشة الموحدة'),
                ('/sales', 'رابط المبيعات'),
                ('/customers', 'رابط العملاء'),
                ('/suppliers', 'رابط الموردين')
            ]
            
            for url, button_name in quick_links:
                try:
                    start_time = time.time()
                    response = self.session.get(f'{self.base_url}{url}')
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        self.log_test("لوحة التحكم", button_name, "PASS", "يعمل بشكل صحيح", response_time)
                    elif response.status_code == 302:
                        self.log_test("لوحة التحكم", button_name, "PASS", "إعادة توجيه (طبيعي)", response_time)
                    else:
                        self.log_test("لوحة التحكم", button_name, "FAIL", f"كود: {response.status_code}", response_time)
                except Exception as e:
                    self.log_test("لوحة التحكم", button_name, "FAIL", f"خطأ: {str(e)}", 0)
                    
        except Exception as e:
            self.log_test("لوحة التحكم", "اختبار عام", "FAIL", f"خطأ عام: {str(e)}", 0)
    
    def test_unified_products_screen(self):
        """اختبار الشاشة الموحدة"""
        print("\n🌟 اختبار الشاشة الموحدة...")
        
        try:
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/unified_products')
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_test("الشاشة الموحدة", "تحميل الصفحة", "FAIL", f"كود: {response.status_code}", response_time)
                return
            
            self.log_test("الشاشة الموحدة", "تحميل الصفحة", "PASS", "تم التحميل بنجاح", response_time)
            
            # اختبار APIs المرتبطة بالأزرار
            api_tests = [
                ('/api/raw_materials', 'GET', 'API تحميل المواد الخام'),
                ('/api/products', 'GET', 'API تحميل المنتجات'),
            ]
            
            for url, method, test_name in api_tests:
                try:
                    start_time = time.time()
                    if method == 'GET':
                        response = self.session.get(f'{self.base_url}{url}')
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list):
                            self.log_test("الشاشة الموحدة", test_name, "PASS", f"تم تحميل {len(data)} عنصر", response_time)
                        else:
                            self.log_test("الشاشة الموحدة", test_name, "PASS", "استجابة صحيحة", response_time)
                    else:
                        self.log_test("الشاشة الموحدة", test_name, "FAIL", f"كود: {response.status_code}", response_time)
                except Exception as e:
                    self.log_test("الشاشة الموحدة", test_name, "FAIL", f"خطأ: {str(e)}", 0)
            
            # اختبار إضافة مادة خام
            self.test_add_raw_material_button()
            
            # اختبار حفظ منتج
            self.test_save_product_button()
            
        except Exception as e:
            self.log_test("الشاشة الموحدة", "اختبار عام", "FAIL", f"خطأ عام: {str(e)}", 0)
    
    def test_add_raw_material_button(self):
        """اختبار زر إضافة مادة خام"""
        print("📦 اختبار زر إضافة مادة خام...")
        
        test_material = {
            'name': f'مادة اختبار {int(time.time())}',
            'unit': 'كيلو',
            'price': 15.75,
            'stock': 25.0,
            'min_stock': 5.0,
            'supplier': 'مورد اختبار'
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f'{self.base_url}/api/raw_materials',
                json=test_material,
                headers={'Content-Type': 'application/json'}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test("الشاشة الموحدة", "زر إضافة مادة خام", "PASS", "تم الحفظ بنجاح", response_time)
                else:
                    self.log_test("الشاشة الموحدة", "زر إضافة مادة خام", "WARN", f"رسالة: {result.get('message')}", response_time)
            else:
                self.log_test("الشاشة الموحدة", "زر إضافة مادة خام", "FAIL", f"كود: {response.status_code}", response_time)
                
        except Exception as e:
            self.log_test("الشاشة الموحدة", "زر إضافة مادة خام", "FAIL", f"خطأ: {str(e)}", 0)
    
    def test_save_product_button(self):
        """اختبار زر حفظ منتج"""
        print("🍽️ اختبار زر حفظ منتج...")
        
        # الحصول على المواد الخام أولاً
        try:
            response = self.session.get(f'{self.base_url}/api/raw_materials')
            if response.status_code != 200:
                self.log_test("الشاشة الموحدة", "زر حفظ منتج", "FAIL", "لا يمكن تحميل المواد الخام", 0)
                return
            
            materials = response.json()
            if len(materials) < 2:
                self.log_test("الشاشة الموحدة", "زر حفظ منتج", "WARN", "عدد المواد الخام غير كافي للاختبار", 0)
                return
            
            # إنشاء منتج تجريبي
            test_product = {
                'name': f'منتج اختبار {int(time.time())}',
                'description': 'منتج تجريبي للاختبار',
                'servings': 4,
                'category': 'وجبات رئيسية',
                'ingredients': [
                    {
                        'material_id': materials[0]['id'],
                        'material_name': materials[0]['name'],
                        'quantity': 1.0,
                        'unit_price': materials[0]['price'],
                        'total_cost': materials[0]['price'],
                        'percentage': 60.0
                    },
                    {
                        'material_id': materials[1]['id'],
                        'material_name': materials[1]['name'],
                        'quantity': 0.5,
                        'unit_price': materials[1]['price'],
                        'total_cost': materials[1]['price'] * 0.5,
                        'percentage': 40.0
                    }
                ],
                'total_cost': materials[0]['price'] + (materials[1]['price'] * 0.5),
                'cost_per_serving': (materials[0]['price'] + (materials[1]['price'] * 0.5)) / 4,
                'suggested_price': ((materials[0]['price'] + (materials[1]['price'] * 0.5)) / 4) * 1.4
            }
            
            start_time = time.time()
            response = self.session.post(
                f'{self.base_url}/api/save_product_cost',
                json=test_product,
                headers={'Content-Type': 'application/json'}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test("الشاشة الموحدة", "زر حفظ منتج", "PASS", f"تم الحفظ - كود: {result.get('product_code')}", response_time)
                else:
                    self.log_test("الشاشة الموحدة", "زر حفظ منتج", "FAIL", f"فشل: {result.get('message')}", response_time)
            else:
                self.log_test("الشاشة الموحدة", "زر حفظ منتج", "FAIL", f"كود: {response.status_code}", response_time)
                
        except Exception as e:
            self.log_test("الشاشة الموحدة", "زر حفظ منتج", "FAIL", f"خطأ: {str(e)}", 0)
    
    def test_sales_screen(self):
        """اختبار شاشة المبيعات"""
        print("\n💰 اختبار شاشة المبيعات...")
        
        try:
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/new_sale')
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("شاشة المبيعات", "تحميل صفحة فاتورة جديدة", "PASS", "تم التحميل بنجاح", response_time)
            else:
                self.log_test("شاشة المبيعات", "تحميل صفحة فاتورة جديدة", "FAIL", f"كود: {response.status_code}", response_time)
            
            # اختبار صفحة المبيعات المحفوظة
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/sales')
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("شاشة المبيعات", "تحميل صفحة المبيعات", "PASS", "تم التحميل بنجاح", response_time)
            else:
                self.log_test("شاشة المبيعات", "تحميل صفحة المبيعات", "FAIL", f"كود: {response.status_code}", response_time)
            
        except Exception as e:
            self.log_test("شاشة المبيعات", "اختبار عام", "FAIL", f"خطأ عام: {str(e)}", 0)
    
    def test_language_buttons(self):
        """اختبار أزرار تغيير اللغة"""
        print("\n🌐 اختبار أزرار تغيير اللغة...")
        
        language_tests = [
            ('?lang=ar', 'زر اللغة العربية'),
            ('?lang=en', 'زر اللغة الإنجليزية')
        ]
        
        for lang_param, test_name in language_tests:
            try:
                start_time = time.time()
                response = self.session.get(f'{self.base_url}/dashboard{lang_param}')
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test("تغيير اللغة", test_name, "PASS", "يعمل بشكل صحيح", response_time)
                else:
                    self.log_test("تغيير اللغة", test_name, "FAIL", f"كود: {response.status_code}", response_time)
            except Exception as e:
                self.log_test("تغيير اللغة", test_name, "FAIL", f"خطأ: {str(e)}", 0)
    
    def test_logout_button(self):
        """اختبار زر تسجيل الخروج"""
        print("\n🚪 اختبار زر تسجيل الخروج...")
        
        try:
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/logout')
            response_time = time.time() - start_time
            
            if response.status_code == 200 or response.status_code == 302:
                self.log_test("تسجيل الخروج", "زر تسجيل الخروج", "PASS", "تم بنجاح", response_time)
            else:
                self.log_test("تسجيل الخروج", "زر تسجيل الخروج", "FAIL", f"كود: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("تسجيل الخروج", "زر تسجيل الخروج", "FAIL", f"خطأ: {str(e)}", 0)
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🧪 بدء الاختبار العملي الشامل لجميع الأزرار")
        print("=" * 70)
        print(f"🌐 الرابط: {self.base_url}")
        print("👤 المستخدم: admin | كلمة المرور: admin123")
        print("=" * 70)
        
        # تسجيل الدخول أولاً
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return
        
        # تشغيل جميع الاختبارات
        self.test_dashboard_buttons()
        self.test_unified_products_screen()
        self.test_sales_screen()
        self.test_language_buttons()
        self.test_logout_button()
        
        # عرض النتائج النهائية
        self.show_comprehensive_results()
    
    def show_comprehensive_results(self):
        """عرض النتائج الشاملة"""
        print("\n" + "=" * 70)
        print("📊 نتائج الاختبار العملي الشامل")
        print("=" * 70)
        
        # إحصائيات عامة
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.test_results if r['status'] == 'WARN'])
        
        print(f"📈 إجمالي الاختبارات: {total_tests}")
        print(f"✅ نجح: {passed_tests}")
        print(f"❌ فشل: {failed_tests}")
        print(f"⚠️ تحذيرات: {warnings}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"📊 نسبة النجاح: {success_rate:.1f}%")
        
        # متوسط زمن الاستجابة
        response_times = [r['response_time'] for r in self.test_results if r['response_time'] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"⏱️ متوسط زمن الاستجابة: {avg_response_time:.2f} ثانية")
        
        # تجميع النتائج حسب الشاشة
        by_screen = {}
        for result in self.test_results:
            screen = result['screen']
            if screen not in by_screen:
                by_screen[screen] = {'PASS': 0, 'FAIL': 0, 'WARN': 0}
            by_screen[screen][result['status']] += 1
        
        print(f"\n📋 النتائج حسب الشاشة:")
        for screen, counts in by_screen.items():
            total = counts['PASS'] + counts['FAIL'] + counts['WARN']
            success_rate = (counts['PASS'] / total * 100) if total > 0 else 0
            status_icon = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 70 else "🔴"
            print(f"   {status_icon} {screen}: {counts['PASS']}/{total} ({success_rate:.1f}%)")
        
        # عرض الاختبارات الفاشلة
        failed_tests_list = [r for r in self.test_results if r['status'] == 'FAIL']
        if failed_tests_list:
            print(f"\n❌ الاختبارات الفاشلة:")
            for result in failed_tests_list:
                print(f"   - {result['screen']} - {result['button']}: {result['details']}")
        
        # التوصيات النهائية
        print(f"\n🎯 التقييم النهائي:")
        if success_rate >= 95:
            print("🎉 ممتاز! جميع الأزرار تعمل بشكل مثالي")
        elif success_rate >= 85:
            print("✅ جيد جداً! معظم الأزرار تعمل بشكل صحيح")
        elif success_rate >= 70:
            print("⚠️ جيد! يحتاج بعض الإصلاحات")
        else:
            print("🔧 يحتاج إصلاحات شاملة")
        
        print(f"\n🌐 للاختبار اليدوي:")
        print("1. افتح المتصفح: http://localhost:5000")
        print("2. سجل الدخول: admin / admin123")
        print("3. اختبر كل زر يدوياً")
        print("=" * 70)

def main():
    """الوظيفة الرئيسية"""
    tester = ComprehensiveLiveTester()
    
    # فتح المتصفح
    print("🌐 فتح المتصفح...")
    webbrowser.open('http://localhost:5000')
    
    # انتظار قصير للتأكد من تشغيل الخادم
    print("⏳ انتظار تشغيل الخادم...")
    time.sleep(3)
    
    # تشغيل الاختبار
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
