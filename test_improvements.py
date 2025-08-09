#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test System Improvements - اختبار تحسينات النظام
اختبار الوظائف الجديدة والتحسينات المضافة
"""

import requests
import time

class ImprovementsTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {
                'username': 'admin',
                'password': 'admin123',
                'language': 'ar'
            }
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def test_screen_access(self, screen_name, url):
        """اختبار الوصول للشاشة"""
        try:
            response = self.session.get(f"{self.base_url}{url}")
            
            if response.status_code == 200:
                content = response.text
                
                # فحص وجود الأزرار
                buttons_found = []
                button_patterns = ['btnSave', 'btnEdit', 'btnDelete', 'btnPrint', 'btnSearch']
                
                for pattern in button_patterns:
                    if pattern in content:
                        buttons_found.append(pattern)
                
                print(f"✅ {screen_name}: متاح - أزرار: {len(buttons_found)}")
                return True, len(buttons_found)
            else:
                print(f"❌ {screen_name}: غير متاح - HTTP {response.status_code}")
                return False, 0
                
        except Exception as e:
            print(f"❌ {screen_name}: خطأ - {str(e)}")
            return False, 0
    
    def test_api_endpoint(self, endpoint, method='POST', data=None):
        """اختبار API endpoint"""
        try:
            if method == 'POST':
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json=data or {'test': 'data'},
                    headers={'Content-Type': 'application/json'}
                )
            else:
                response = self.session.get(f"{self.base_url}{endpoint}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return result.get('success', False), result.get('message', '')
                except:
                    return True, 'Success (non-JSON)'
            else:
                return False, f'HTTP {response.status_code}'
                
        except Exception as e:
            return False, str(e)
    
    def run_comprehensive_test(self):
        """تشغيل اختبار شامل"""
        print("🚀 بدء اختبار التحسينات الشاملة")
        print("🚀 Starting comprehensive improvements test")
        print("=" * 80)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return
        
        print("✅ تم تسجيل الدخول بنجاح\n")
        
        # اختبار الشاشات
        print("🔍 اختبار الوصول للشاشات...")
        print("-" * 50)
        
        screens = [
            ('لوحة التحكم', '/dashboard'),
            ('المبيعات', '/sales'),
            ('المشتريات', '/purchases'),
            ('المنتجات', '/products'),
            ('العملاء', '/customers'),
            ('الموردين', '/suppliers'),
            ('المصروفات', '/expenses'),
            ('المدفوعات والمستحقات', '/payments_dues'),
            ('ضريبة القيمة المضافة', '/tax_management'),
            ('الموظفين والرواتب', '/employee_payroll'),
            ('المخزون', '/inventory'),
            ('التقارير', '/reports'),
            ('التقارير المتقدمة', '/advanced_reports'),
            ('القوائم المالية', '/financial_statements')
        ]
        
        accessible_screens = 0
        total_buttons = 0
        
        for screen_name, url in screens:
            accessible, button_count = self.test_screen_access(screen_name, url)
            if accessible:
                accessible_screens += 1
                total_buttons += button_count
            time.sleep(0.5)
        
        print(f"\n📊 نتائج الشاشات:")
        print(f"• الشاشات المتاحة: {accessible_screens}/{len(screens)}")
        print(f"• إجمالي الأزرار: {total_buttons}")
        
        # اختبار API endpoints الجديدة
        print(f"\n🔗 اختبار API endpoints الجديدة...")
        print("-" * 50)
        
        new_endpoints = [
            ('المشتريات - حفظ', '/api/purchases/save'),
            ('المشتريات - تعديل', '/api/purchases/edit/1'),
            ('المشتريات - حذف', '/api/purchases/delete/1'),
            ('العملاء - حفظ', '/api/customers/save'),
            ('العملاء - بحث', '/api/customers/search'),
            ('الموردين - حفظ', '/api/suppliers/save'),
            ('الموردين - بحث', '/api/suppliers/search'),
            ('المصروفات - حفظ', '/api/expenses/save'),
            ('الموظفين - حفظ', '/api/employees/save'),
            ('الضرائب - حفظ', '/api/taxes/save')
        ]
        
        working_endpoints = 0
        
        for endpoint_name, endpoint_url in new_endpoints:
            method = 'PUT' if '/edit/' in endpoint_url else 'DELETE' if '/delete/' in endpoint_url else 'GET' if '/search' in endpoint_url else 'POST'
            success, message = self.test_api_endpoint(endpoint_url, method)
            
            if success:
                print(f"✅ {endpoint_name}: يعمل")
                working_endpoints += 1
            else:
                print(f"❌ {endpoint_name}: {message}")
            
            time.sleep(0.3)
        
        print(f"\n📊 نتائج API endpoints:")
        print(f"• Endpoints العاملة: {working_endpoints}/{len(new_endpoints)}")
        
        # اختبار مكونات الأزرار الجديدة
        print(f"\n🔘 اختبار مكونات الأزرار الجديدة...")
        print("-" * 50)
        
        button_components = [
            'payments_buttons.html',
            'taxes_buttons.html', 
            'employees_buttons.html',
            'inventory_buttons.html'
        ]
        
        existing_components = 0
        
        for component in button_components:
            component_path = f'templates/components/{component}'
            try:
                with open(component_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                button_count = content.count('<button')
                print(f"✅ {component}: موجود - {button_count} أزرار")
                existing_components += 1
                
            except FileNotFoundError:
                print(f"❌ {component}: غير موجود")
            except Exception as e:
                print(f"❌ {component}: خطأ - {str(e)}")
        
        print(f"\n📊 نتائج مكونات الأزرار:")
        print(f"• المكونات الموجودة: {existing_components}/{len(button_components)}")
        
        # النتيجة النهائية
        print(f"\n" + "=" * 80)
        print("🎯 النتيجة النهائية للتحسينات")
        print("🎯 Final Improvements Results")
        print("=" * 80)
        
        total_score = 0
        max_score = 0
        
        # نقاط الشاشات
        screen_score = (accessible_screens / len(screens)) * 30
        total_score += screen_score
        max_score += 30
        print(f"📱 الشاشات: {screen_score:.1f}/30 ({accessible_screens}/{len(screens)} متاح)")
        
        # نقاط API endpoints
        api_score = (working_endpoints / len(new_endpoints)) * 25
        total_score += api_score
        max_score += 25
        print(f"🔗 API Endpoints: {api_score:.1f}/25 ({working_endpoints}/{len(new_endpoints)} يعمل)")
        
        # نقاط مكونات الأزرار
        component_score = (existing_components / len(button_components)) * 20
        total_score += component_score
        max_score += 20
        print(f"🔘 مكونات الأزرار: {component_score:.1f}/20 ({existing_components}/{len(button_components)} موجود)")
        
        # نقاط الأزرار الإجمالية
        button_score = min(total_buttons / 50, 1) * 25  # افتراض 50 زر كحد أقصى
        total_score += button_score
        max_score += 25
        print(f"🎛️ الأزرار الإجمالية: {button_score:.1f}/25 ({total_buttons} زر)")
        
        # النسبة المئوية
        percentage = (total_score / max_score) * 100
        
        print(f"\n🏆 النتيجة الإجمالية: {total_score:.1f}/{max_score} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🌟 ممتاز! النظام محسّن بشكل كامل")
        elif percentage >= 75:
            print("✅ جيد جداً! معظم التحسينات مطبقة")
        elif percentage >= 60:
            print("👍 جيد! التحسينات الأساسية مطبقة")
        else:
            print("⚠️ يحتاج المزيد من التحسينات")
        
        # التوصيات
        print(f"\n💡 التوصيات:")
        if accessible_screens < len(screens):
            print("• إصلاح الشاشات غير المتاحة")
        if working_endpoints < len(new_endpoints):
            print("• إصلاح API endpoints غير العاملة")
        if existing_components < len(button_components):
            print("• إضافة مكونات الأزرار المفقودة")
        if total_buttons < 40:
            print("• إضافة المزيد من الأزرار للشاشات")
        
        print(f"\n🎉 انتهى اختبار التحسينات!")

def main():
    """تشغيل الاختبار"""
    tester = ImprovementsTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
