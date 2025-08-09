#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive System Audit - فحص شامل للنظام
تفقد تنسيق الشاشات وإضافة الوظائف غير المكتملة
"""

import os
import re
import requests
from pathlib import Path
import json
import time

class SystemAuditor:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.audit_results = {
            'screens': {},
            'missing_functions': [],
            'ui_issues': [],
            'incomplete_features': [],
            'recommendations': []
        }
        
    def login(self):
        """تسجيل الدخول للنظام"""
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
    
    def audit_screen_layout(self, screen_name, url):
        """فحص تنسيق شاشة معينة"""
        print(f"\n🔍 فحص شاشة: {screen_name}")
        print(f"🔍 Auditing screen: {screen_name}")
        print("-" * 50)
        
        try:
            response = self.session.get(f"{self.base_url}{url}")
            
            if response.status_code != 200:
                print(f"❌ الشاشة غير متاحة - HTTP {response.status_code}")
                return False
            
            content = response.text
            screen_audit = {
                'accessible': True,
                'has_buttons': False,
                'has_form': False,
                'has_table': False,
                'has_modals': False,
                'button_count': 0,
                'missing_elements': [],
                'ui_issues': []
            }
            
            # فحص الأزرار
            button_patterns = [
                r'btnSave', r'btnEdit', r'btnDelete', r'btnPreview', 
                r'btnPrint', r'btnSearch', r'btnSelectInvoice', r'btnRegisterPayment'
            ]
            
            buttons_found = []
            for pattern in button_patterns:
                if re.search(pattern, content):
                    buttons_found.append(pattern)
            
            screen_audit['button_count'] = len(buttons_found)
            screen_audit['has_buttons'] = len(buttons_found) > 0
            
            if buttons_found:
                print(f"✅ الأزرار الموجودة: {', '.join(buttons_found)}")
            else:
                print("❌ لا توجد أزرار")
                screen_audit['missing_elements'].append('buttons')
            
            # فحص النماذج
            if re.search(r'<form', content):
                screen_audit['has_form'] = True
                print("✅ يحتوي على نماذج")
            else:
                print("⚠️ لا يحتوي على نماذج")
                screen_audit['missing_elements'].append('forms')
            
            # فحص الجداول
            if re.search(r'<table', content):
                screen_audit['has_table'] = True
                print("✅ يحتوي على جداول")
            else:
                print("⚠️ لا يحتوي على جداول")
            
            # فحص النوافذ المنبثقة
            if re.search(r'modal', content):
                screen_audit['has_modals'] = True
                print("✅ يحتوي على نوافذ منبثقة")
            else:
                print("⚠️ لا يحتوي على نوافذ منبثقة")
            
            # فحص التنسيق
            ui_checks = [
                ('Bootstrap CSS', r'bootstrap'),
                ('Font Awesome', r'font-awesome|fas fa-'),
                ('RTL Support', r'rtl|text-right'),
                ('Responsive Design', r'col-md|col-lg|col-sm')
            ]
            
            for check_name, pattern in ui_checks:
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"✅ {check_name} موجود")
                else:
                    print(f"⚠️ {check_name} مفقود")
                    screen_audit['ui_issues'].append(f"Missing {check_name}")
            
            self.audit_results['screens'][screen_name] = screen_audit
            return True
            
        except Exception as e:
            print(f"❌ خطأ في فحص الشاشة: {str(e)}")
            return False
    
    def audit_api_endpoints(self, screen_name):
        """فحص نقاط النهاية للـ API"""
        print(f"\n🔗 فحص API endpoints لشاشة: {screen_name}")
        
        # قائمة endpoints المتوقعة لكل شاشة
        expected_endpoints = {
            'sales': ['/api/sales/save', '/api/sales/edit', '/api/sales/delete', 
                     '/api/sales/preview', '/api/sales/print', '/api/sales/select_invoice', 
                     '/api/sales/register_payment'],
            'products': ['/api/products/save', '/api/products/edit', '/api/products/delete',
                        '/api/products/search', '/api/products/print'],
            'purchases': ['/api/purchases/save', '/api/purchases/edit', '/api/purchases/delete',
                         '/api/purchases/preview', '/api/purchases/print'],
            'customers': ['/api/customers/save', '/api/customers/edit', '/api/customers/delete',
                         '/api/customers/search', '/api/customers/print'],
            'suppliers': ['/api/suppliers/save', '/api/suppliers/edit', '/api/suppliers/delete',
                         '/api/suppliers/search', '/api/suppliers/print']
        }
        
        if screen_name not in expected_endpoints:
            print(f"⚠️ لا توجد endpoints متوقعة لشاشة {screen_name}")
            return
        
        working_endpoints = []
        missing_endpoints = []
        
        for endpoint in expected_endpoints[screen_name]:
            try:
                if 'save' in endpoint or 'edit' in endpoint or 'register_payment' in endpoint:
                    # POST/PUT endpoints - test with dummy data
                    response = self.session.post(f"{self.base_url}{endpoint}", 
                                               json={'test': 'data'})
                else:
                    # GET endpoints
                    response = self.session.get(f"{self.base_url}{endpoint}")
                
                if response.status_code in [200, 400, 422]:  # 400/422 for validation errors is OK
                    working_endpoints.append(endpoint)
                    print(f"✅ {endpoint}")
                else:
                    missing_endpoints.append(endpoint)
                    print(f"❌ {endpoint} - HTTP {response.status_code}")
                    
            except Exception as e:
                missing_endpoints.append(endpoint)
                print(f"❌ {endpoint} - Error: {str(e)}")
        
        if missing_endpoints:
            self.audit_results['missing_functions'].extend(
                [(screen_name, endpoint) for endpoint in missing_endpoints]
            )
    
    def check_incomplete_features(self):
        """فحص الميزات غير المكتملة"""
        print(f"\n🔍 فحص الميزات غير المكتملة...")
        print("🔍 Checking incomplete features...")
        print("=" * 60)
        
        incomplete_features = []
        
        # فحص ملفات القوالب للميزات غير المكتملة
        templates_dir = Path('templates')
        
        for template_file in templates_dir.glob('*.html'):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن تعليقات TODO أو FIXME
                todos = re.findall(r'<!--.*?TODO.*?-->', content, re.IGNORECASE | re.DOTALL)
                fixmes = re.findall(r'<!--.*?FIXME.*?-->', content, re.IGNORECASE | re.DOTALL)
                
                if todos or fixmes:
                    incomplete_features.append({
                        'file': str(template_file),
                        'todos': todos,
                        'fixmes': fixmes
                    })
                
                # البحث عن نماذج فارغة أو غير مكتملة
                if 'TODO' in content or 'FIXME' in content or 'placeholder' in content.lower():
                    print(f"⚠️ {template_file.name} قد يحتوي على ميزات غير مكتملة")
                
            except Exception as e:
                print(f"❌ خطأ في فحص {template_file}: {str(e)}")
        
        self.audit_results['incomplete_features'] = incomplete_features
    
    def generate_recommendations(self):
        """إنشاء توصيات للتحسين"""
        print(f"\n💡 إنشاء توصيات للتحسين...")
        print("💡 Generating improvement recommendations...")
        print("=" * 60)
        
        recommendations = []
        
        # توصيات بناءً على فحص الشاشات
        for screen_name, audit in self.audit_results['screens'].items():
            if not audit['has_buttons']:
                recommendations.append(f"إضافة نظام أزرار لشاشة {screen_name}")
            
            if not audit['has_form'] and screen_name in ['customers', 'suppliers', 'employees']:
                recommendations.append(f"إضافة نماذج إدخال لشاشة {screen_name}")
            
            if audit['ui_issues']:
                recommendations.append(f"إصلاح مشاكل التنسيق في شاشة {screen_name}: {', '.join(audit['ui_issues'])}")
        
        # توصيات بناءً على الوظائف المفقودة
        if self.audit_results['missing_functions']:
            recommendations.append("إضافة API endpoints المفقودة")
        
        # توصيات عامة
        recommendations.extend([
            "توحيد تصميم جميع الشاشات",
            "إضافة نظام إشعارات موحد",
            "تحسين الاستجابة للأجهزة المحمولة",
            "إضافة نظام مساعدة للمستخدمين",
            "تحسين أداء التحميل"
        ])
        
        self.audit_results['recommendations'] = recommendations
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    
    def run_comprehensive_audit(self):
        """تشغيل فحص شامل للنظام"""
        print("🚀 بدء الفحص الشامل للنظام")
        print("🚀 Starting comprehensive system audit")
        print("=" * 80)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول - لا يمكن متابعة الفحص")
            return
        
        print("✅ تم تسجيل الدخول بنجاح")
        
        # قائمة الشاشات للفحص
        screens_to_audit = [
            ('لوحة التحكم', '/dashboard'),
            ('المبيعات', '/sales'),
            ('المشتريات', '/purchases'),
            ('المنتجات', '/products'),
            ('العملاء', '/customers'),
            ('الموردين', '/suppliers'),
            ('التقارير', '/reports'),
            ('التقارير المتقدمة', '/advanced_reports'),
            ('المصروفات', '/expenses'),
            ('القوائم المالية', '/financial_statements'),
            ('المدفوعات والمستحقات', '/payments_dues'),
            ('ضريبة القيمة المضافة', '/tax_management'),
            ('الموظفين والرواتب', '/employee_payroll'),
            ('المخزون', '/inventory')
        ]
        
        # فحص كل شاشة
        for screen_name, url in screens_to_audit:
            self.audit_screen_layout(screen_name, url)
            time.sleep(1)  # تجنب الضغط على الخادم
        
        # فحص API endpoints
        api_screens = ['sales', 'products', 'purchases', 'customers', 'suppliers']
        for screen in api_screens:
            self.audit_api_endpoints(screen)
            time.sleep(1)
        
        # فحص الميزات غير المكتملة
        self.check_incomplete_features()
        
        # إنشاء التوصيات
        self.generate_recommendations()
        
        return self.audit_results
    
    def save_audit_report(self, results):
        """حفظ تقرير الفحص"""
        report_file = 'COMPREHENSIVE_AUDIT_REPORT.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 تم حفظ تقرير الفحص في: {report_file}")

def main():
    """تشغيل الفحص الشامل"""
    auditor = SystemAuditor()
    results = auditor.run_comprehensive_audit()
    auditor.save_audit_report(results)
    
    print(f"\n" + "=" * 80)
    print("🎉 انتهى الفحص الشامل للنظام!")
    print("🎉 Comprehensive system audit completed!")
    print("=" * 80)
    
    # ملخص النتائج
    total_screens = len(results['screens'])
    screens_with_buttons = sum(1 for s in results['screens'].values() if s['has_buttons'])
    missing_functions = len(results['missing_functions'])
    
    print(f"\n📊 ملخص النتائج:")
    print(f"📊 Results Summary:")
    print(f"• إجمالي الشاشات المفحوصة: {total_screens}")
    print(f"• الشاشات التي تحتوي على أزرار: {screens_with_buttons}")
    print(f"• الوظائف المفقودة: {missing_functions}")
    print(f"• التوصيات: {len(results['recommendations'])}")

if __name__ == "__main__":
    main()
