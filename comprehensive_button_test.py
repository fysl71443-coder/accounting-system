#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لجميع أزرار النظام
Comprehensive Button Testing System
"""

import requests
import json
import time
from datetime import datetime

class ButtonTester:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'http://localhost:5000'
        self.test_results = []
        self.login_successful = False
        
    def log_test(self, test_name, status, details=""):
        """تسجيل نتيجة الاختبار"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {details}")
    
    def login(self):
        """تسجيل الدخول"""
        print("🔐 اختبار تسجيل الدخول...")
        
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'language': 'ar'
        }
        
        try:
            response = self.session.post(f'{self.base_url}/login', data=login_data)
            if response.status_code == 200 and 'dashboard' in response.url:
                self.login_successful = True
                self.log_test("تسجيل الدخول", "PASS", "تم بنجاح")
                return True
            else:
                self.log_test("تسجيل الدخول", "FAIL", f"فشل - كود: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("تسجيل الدخول", "FAIL", f"خطأ: {str(e)}")
            return False
    
    def test_dashboard_buttons(self):
        """اختبار أزرار لوحة التحكم"""
        print("\n📊 اختبار أزرار لوحة التحكم...")
        
        try:
            response = self.session.get(f'{self.base_url}/dashboard')
            if response.status_code != 200:
                self.log_test("تحميل لوحة التحكم", "FAIL", f"كود: {response.status_code}")
                return
            
            self.log_test("تحميل لوحة التحكم", "PASS", "تم التحميل بنجاح")
            
            # اختبار أزرار الإحصائيات السريعة
            dashboard_buttons = [
                ('/new_sale', 'زر فاتورة جديدة'),
                ('/unified_products', 'زر إدارة المنتجات والتكاليف'),
                ('/sales', 'زر المبيعات'),
                ('/customers', 'زر العملاء'),
                ('/suppliers', 'زر الموردين'),
                ('/reports', 'زر التقارير')
            ]
            
            for url, button_name in dashboard_buttons:
                try:
                    response = self.session.get(f'{self.base_url}{url}')
                    if response.status_code == 200:
                        self.log_test(button_name, "PASS", "يعمل بشكل صحيح")
                    elif response.status_code == 302:
                        self.log_test(button_name, "PASS", "إعادة توجيه (طبيعي)")
                    else:
                        self.log_test(button_name, "FAIL", f"كود: {response.status_code}")
                except Exception as e:
                    self.log_test(button_name, "FAIL", f"خطأ: {str(e)}")
                    
        except Exception as e:
            self.log_test("اختبار لوحة التحكم", "FAIL", f"خطأ عام: {str(e)}")
    
    def test_sidebar_buttons(self):
        """اختبار أزرار القائمة الجانبية"""
        print("\n📋 اختبار أزرار القائمة الجانبية...")
        
        sidebar_buttons = [
            ('/dashboard', 'زر لوحة التحكم'),
            ('/unified_products', 'زر الشاشة الموحدة'),
            ('/new_sale', 'زر فاتورة جديدة'),
            ('/sales', 'زر المبيعات'),
            ('/logout', 'زر تسجيل الخروج')
        ]
        
        for url, button_name in sidebar_buttons:
            try:
                response = self.session.get(f'{self.base_url}{url}')
                if response.status_code == 200:
                    self.log_test(button_name, "PASS", "يعمل بشكل صحيح")
                elif response.status_code == 302:
                    self.log_test(button_name, "PASS", "إعادة توجيه (طبيعي)")
                else:
                    self.log_test(button_name, "FAIL", f"كود: {response.status_code}")
            except Exception as e:
                self.log_test(button_name, "FAIL", f"خطأ: {str(e)}")
    
    def test_unified_products_buttons(self):
        """اختبار أزرار الشاشة الموحدة"""
        print("\n🌟 اختبار أزرار الشاشة الموحدة...")
        
        try:
            response = self.session.get(f'{self.base_url}/unified_products')
            if response.status_code != 200:
                self.log_test("تحميل الشاشة الموحدة", "FAIL", f"كود: {response.status_code}")
                return
            
            self.log_test("تحميل الشاشة الموحدة", "PASS", "تم التحميل بنجاح")
            
            # اختبار APIs المرتبطة بالأزرار
            api_tests = [
                ('/api/raw_materials', 'GET', 'API تحميل المواد الخام'),
                ('/api/products', 'GET', 'API تحميل المنتجات'),
            ]
            
            for url, method, test_name in api_tests:
                try:
                    if method == 'GET':
                        response = self.session.get(f'{self.base_url}{url}')
                    
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list):
                            self.log_test(test_name, "PASS", f"تم تحميل {len(data)} عنصر")
                        else:
                            self.log_test(test_name, "PASS", "استجابة صحيحة")
                    else:
                        self.log_test(test_name, "FAIL", f"كود: {response.status_code}")
                except Exception as e:
                    self.log_test(test_name, "FAIL", f"خطأ: {str(e)}")
            
            # اختبار إضافة مادة خام
            self.test_add_raw_material_button()
            
            # اختبار حفظ منتج
            self.test_save_product_button()
            
        except Exception as e:
            self.log_test("اختبار الشاشة الموحدة", "FAIL", f"خطأ عام: {str(e)}")
    
    def test_add_raw_material_button(self):
        """اختبار زر إضافة مادة خام"""
        print("\n📦 اختبار زر إضافة مادة خام...")
        
        test_material = {
            'name': f'مادة اختبار {int(time.time())}',
            'unit': 'كيلو',
            'price': 15.75,
            'stock': 25.0,
            'min_stock': 5.0,
            'supplier': 'مورد اختبار'
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/raw_materials',
                json=test_material,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test("زر إضافة مادة خام", "PASS", "تم الحفظ بنجاح")
                else:
                    self.log_test("زر إضافة مادة خام", "WARN", f"رسالة: {result.get('message')}")
            else:
                self.log_test("زر إضافة مادة خام", "FAIL", f"كود: {response.status_code}")
                
        except Exception as e:
            self.log_test("زر إضافة مادة خام", "FAIL", f"خطأ: {str(e)}")
    
    def test_save_product_button(self):
        """اختبار زر حفظ منتج"""
        print("\n🍽️ اختبار زر حفظ منتج...")
        
        # الحصول على المواد الخام أولاً
        try:
            response = self.session.get(f'{self.base_url}/api/raw_materials')
            if response.status_code != 200:
                self.log_test("زر حفظ منتج", "FAIL", "لا يمكن تحميل المواد الخام")
                return
            
            materials = response.json()
            if len(materials) < 2:
                self.log_test("زر حفظ منتج", "WARN", "عدد المواد الخام غير كافي للاختبار")
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
            
            response = self.session.post(
                f'{self.base_url}/api/save_product_cost',
                json=test_product,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test("زر حفظ منتج", "PASS", f"تم الحفظ - كود: {result.get('product_code')}")
                else:
                    self.log_test("زر حفظ منتج", "FAIL", f"فشل: {result.get('message')}")
            else:
                self.log_test("زر حفظ منتج", "FAIL", f"كود: {response.status_code}")
                
        except Exception as e:
            self.log_test("زر حفظ منتج", "FAIL", f"خطأ: {str(e)}")
    
    def test_sales_buttons(self):
        """اختبار أزرار المبيعات"""
        print("\n💰 اختبار أزرار المبيعات...")
        
        sales_urls = [
            ('/new_sale', 'صفحة فاتورة جديدة'),
            ('/sales', 'صفحة المبيعات'),
            ('/api/customers', 'API العملاء'),
            ('/api/products_for_sale', 'API المنتجات للبيع')
        ]
        
        for url, test_name in sales_urls:
            try:
                response = self.session.get(f'{self.base_url}{url}')
                if response.status_code == 200:
                    self.log_test(test_name, "PASS", "يعمل بشكل صحيح")
                elif response.status_code == 302:
                    self.log_test(test_name, "PASS", "إعادة توجيه (طبيعي)")
                else:
                    self.log_test(test_name, "FAIL", f"كود: {response.status_code}")
            except Exception as e:
                self.log_test(test_name, "FAIL", f"خطأ: {str(e)}")
    
    def test_language_buttons(self):
        """اختبار أزرار تغيير اللغة"""
        print("\n🌐 اختبار أزرار تغيير اللغة...")
        
        language_tests = [
            ('?lang=ar', 'زر اللغة العربية'),
            ('?lang=en', 'زر اللغة الإنجليزية')
        ]
        
        for lang_param, test_name in language_tests:
            try:
                response = self.session.get(f'{self.base_url}/dashboard{lang_param}')
                if response.status_code == 200:
                    self.log_test(test_name, "PASS", "يعمل بشكل صحيح")
                else:
                    self.log_test(test_name, "FAIL", f"كود: {response.status_code}")
            except Exception as e:
                self.log_test(test_name, "FAIL", f"خطأ: {str(e)}")
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🧪 بدء الاختبار الشامل لجميع أزرار النظام")
        print("=" * 60)
        
        # تسجيل الدخول أولاً
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return
        
        # تشغيل جميع الاختبارات
        self.test_dashboard_buttons()
        self.test_sidebar_buttons()
        self.test_unified_products_buttons()
        self.test_sales_buttons()
        self.test_language_buttons()
        
        # عرض النتائج النهائية
        self.show_final_results()
    
    def show_final_results(self):
        """عرض النتائج النهائية"""
        print("\n" + "=" * 60)
        print("📊 ملخص نتائج الاختبار الشامل")
        print("=" * 60)
        
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.test_results if r['status'] == 'WARN'])
        total = len(self.test_results)
        
        print(f"✅ نجح: {passed}")
        print(f"❌ فشل: {failed}")
        print(f"⚠️ تحذيرات: {warnings}")
        print(f"📊 الإجمالي: {total}")
        print(f"📈 نسبة النجاح: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print(f"\n❌ الاختبارات الفاشلة:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"   - {result['test']}: {result['details']}")
        
        if warnings > 0:
            print(f"\n⚠️ التحذيرات:")
            for result in self.test_results:
                if result['status'] == 'WARN':
                    print(f"   - {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        print("🎯 توصيات:")
        if failed == 0:
            print("🎉 ممتاز! جميع الأزرار تعمل بشكل صحيح")
        else:
            print("🔧 يرجى مراجعة الأزرار الفاشلة وإصلاحها")
        
        print("📍 الرابط: http://localhost:5000")
        print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
        print("=" * 60)

def main():
    """الوظيفة الرئيسية"""
    tester = ButtonTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
