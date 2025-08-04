#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة المراجعة البسيطة للنظام المحاسبي
Simple Audit Tool for Accounting System
"""

import os
import re
import json
import datetime
from pathlib import Path
from typing import Dict, List

class SimpleAuditTool:
    """أداة المراجعة البسيطة للنظام المحاسبي"""
    
    def __init__(self):
        self.system_path = Path.cwd()
        self.templates_path = self.system_path / "templates"
        self.app_file = self.system_path / "app.py"
        
        # الشاشات المطلوب فحصها
        self.required_screens = {
            'login': {'name_ar': 'تسجيل الدخول', 'template': 'login.html', 'route': '/login'},
            'dashboard': {'name_ar': 'الشاشة الرئيسية', 'template': 'dashboard.html', 'route': '/dashboard'},
            'purchases': {'name_ar': 'المشتريات', 'template': 'purchases.html', 'route': '/purchases'},
            'inventory': {'name_ar': 'المخزون', 'template': 'inventory.html', 'route': '/inventory'},
            'products': {'name_ar': 'الأصناف والمنتجات', 'template': 'products.html', 'route': '/products'},
            'sales': {'name_ar': 'المبيعات', 'template': 'sales.html', 'route': '/sales'},
            'suppliers': {'name_ar': 'الموردين', 'template': 'suppliers.html', 'route': '/suppliers'},
            'employee_payroll': {'name_ar': 'الموظفين والرواتب', 'template': 'employee_payroll.html', 'route': '/employee_payroll'},
            'reports': {'name_ar': 'التقارير', 'template': 'reports.html', 'route': '/reports'},
            'payments_dues': {'name_ar': 'المدفوعات والمستحقات', 'template': 'payments_dues.html', 'route': '/payments_dues'},
            'advanced_expenses': {'name_ar': 'المصروفات المتقدمة', 'template': 'advanced_expenses.html', 'route': '/advanced_expenses'},
            'tax_management': {'name_ar': 'ضريبة القيمة المضافة', 'template': 'tax_management.html', 'route': '/tax_management'},
            'users': {'name_ar': 'المستخدمين والصلاحيات', 'template': 'users.html', 'route': '/users'},
            'settings': {'name_ar': 'الإعدادات العامة', 'template': 'settings.html', 'route': '/settings'},
            'financial_statements': {'name_ar': 'القوائم المالية', 'template': 'financial_statements.html', 'route': '/financial_statements'}
        }
        
        self.audit_results = {}
    
    def run_audit(self):
        """تشغيل الفحص الشامل"""
        print("🔍 بدء الفحص الشامل للنظام المحاسبي")
        print("🔍 Starting comprehensive audit of accounting system")
        print("=" * 80)
        
        for screen_id, screen_info in self.required_screens.items():
            print(f"\n📋 فحص شاشة: {screen_info['name_ar']}")
            result = self.audit_screen(screen_id, screen_info)
            self.audit_results[screen_id] = result
            self.print_screen_result(result)
        
        print("\n" + "=" * 80)
        self.print_summary()
        self.save_report()
    
    def audit_screen(self, screen_id: str, screen_info: Dict) -> Dict:
        """فحص شاشة واحدة"""
        result = {
            'screen_id': screen_id,
            'name_ar': screen_info['name_ar'],
            'template_exists': False,
            'route_exists': False,
            'has_buttons': False,
            'has_forms': False,
            'has_javascript': False,
            'has_arabic': False,
            'issues': [],
            'recommendations': [],
            'completion_percentage': 0,
            'status': 'غير مكتملة'
        }
        
        # فحص وجود القالب
        template_path = self.templates_path / screen_info['template']
        if template_path.exists():
            result['template_exists'] = True
            self.analyze_template(template_path, result)
        else:
            result['issues'].append(f"القالب غير موجود: {screen_info['template']}")
        
        # فحص وجود الرابط
        if self.app_file.exists():
            app_content = self.app_file.read_text(encoding='utf-8')
            if screen_info['route'] in app_content:
                result['route_exists'] = True
            else:
                result['issues'].append(f"الرابط غير موجود: {screen_info['route']}")
        
        # حساب نسبة الاكتمال
        checks = [
            result['template_exists'],
            result['route_exists'],
            result['has_buttons'],
            result['has_forms'],
            result['has_javascript']
        ]
        
        result['completion_percentage'] = int((sum(checks) / len(checks)) * 100)
        
        if result['completion_percentage'] >= 80:
            result['status'] = 'مكتملة ✅'
        elif result['completion_percentage'] >= 50:
            result['status'] = 'قيد التطوير 🔄'
        else:
            result['status'] = 'غير مكتملة ❌'
        
        return result
    
    def analyze_template(self, template_path: Path, result: Dict):
        """تحليل محتوى القالب"""
        try:
            content = template_path.read_text(encoding='utf-8')
            
            result['has_buttons'] = bool(re.search(r'<button|btn', content, re.IGNORECASE))
            result['has_forms'] = bool(re.search(r'<form', content, re.IGNORECASE))
            result['has_javascript'] = bool(re.search(r'<script|onclick=|function', content, re.IGNORECASE))
            result['has_arabic'] = bool(re.search(r'[\u0600-\u06FF]', content))
            
            if not result['has_buttons']:
                result['issues'].append("لا توجد أزرار تفاعلية")
            if not result['has_forms']:
                result['issues'].append("لا توجد نماذج إدخال")
            if not result['has_javascript']:
                result['issues'].append("لا توجد وظائف JavaScript")
            if not result['has_arabic']:
                result['issues'].append("لا يوجد دعم للغة العربية")
                
        except Exception as e:
            result['issues'].append(f"خطأ في قراءة القالب: {str(e)}")
    
    def print_screen_result(self, result: Dict):
        """طباعة نتيجة فحص الشاشة"""
        print(f"   الحالة: {result['status']}")
        print(f"   نسبة الاكتمال: {result['completion_percentage']}%")
        print(f"   القالب: {'✅' if result['template_exists'] else '❌'}")
        print(f"   الرابط: {'✅' if result['route_exists'] else '❌'}")
        print(f"   الأزرار: {'✅' if result['has_buttons'] else '❌'}")
        print(f"   النماذج: {'✅' if result['has_forms'] else '❌'}")
        print(f"   JavaScript: {'✅' if result['has_javascript'] else '❌'}")
        print(f"   العربية: {'✅' if result['has_arabic'] else '❌'}")
        
        if result['issues']:
            print(f"   المشاكل ({len(result['issues'])}):")
            for issue in result['issues'][:3]:  # أول 3 مشاكل فقط
                print(f"      - {issue}")
    
    def print_summary(self):
        """طباعة ملخص النتائج"""
        total_screens = len(self.audit_results)
        completed = sum(1 for r in self.audit_results.values() if r['completion_percentage'] >= 80)
        in_progress = sum(1 for r in self.audit_results.values() if 50 <= r['completion_percentage'] < 80)
        incomplete = sum(1 for r in self.audit_results.values() if r['completion_percentage'] < 50)
        
        print("📊 ملخص النتائج:")
        print(f"   إجمالي الشاشات: {total_screens}")
        print(f"   الشاشات المكتملة: {completed} ({completed/total_screens*100:.1f}%)")
        print(f"   الشاشات قيد التطوير: {in_progress} ({in_progress/total_screens*100:.1f}%)")
        print(f"   الشاشات غير المكتملة: {incomplete} ({incomplete/total_screens*100:.1f}%)")
        
        avg_completion = sum(r['completion_percentage'] for r in self.audit_results.values()) / total_screens
        print(f"   متوسط نسبة الاكتمال: {avg_completion:.1f}%")
    
    def save_report(self):
        """حفظ التقرير في ملف"""
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summary': {
                'total_screens': len(self.audit_results),
                'completed': sum(1 for r in self.audit_results.values() if r['completion_percentage'] >= 80),
                'in_progress': sum(1 for r in self.audit_results.values() if 50 <= r['completion_percentage'] < 80),
                'incomplete': sum(1 for r in self.audit_results.values() if r['completion_percentage'] < 50),
                'avg_completion': sum(r['completion_percentage'] for r in self.audit_results.values()) / len(self.audit_results)
            },
            'screens': self.audit_results
        }
        
        report_file = self.system_path / f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 تم حفظ التقرير في: {report_file}")
        except Exception as e:
            print(f"\n❌ خطأ في حفظ التقرير: {e}")
    
    def create_missing_files(self):
        """إنشاء الملفات المفقودة"""
        print("\n🔧 بدء الإصلاح التلقائي...")
        
        fixed_count = 0
        
        for screen_id, result in self.audit_results.items():
            screen_info = self.required_screens[screen_id]
            
            # إنشاء القالب المفقود
            if not result['template_exists']:
                self.create_basic_template(screen_id, screen_info)
                fixed_count += 1
                print(f"   ✅ تم إنشاء قالب: {screen_info['template']}")
            
            # إضافة الرابط المفقود
            if not result['route_exists']:
                self.add_route_to_app(screen_id, screen_info)
                fixed_count += 1
                print(f"   ✅ تم إضافة رابط: {screen_info['route']}")
        
        print(f"\n🎉 تم إصلاح {fixed_count} مشكلة")
    
    def create_basic_template(self, screen_id: str, screen_info: Dict):
        """إنشاء قالب أساسي"""
        template_content = f'''
{{% extends "base_simple.html" %}}

{{% block title %}}
    {{% if session.get('language', 'ar') == 'ar' %}}
        {screen_info['name_ar']}
    {{% else %}}
        {screen_info['name_ar']}
    {{% endif %}}
{{% endblock %}}

{{% block content %}}
<div class="container-fluid">
    <h1 class="h3 mb-4 text-gray-800">
        <i class="fas fa-cog"></i> {screen_info['name_ar']}
    </h1>
    
    <div class="card">
        <div class="card-header">
            <h6 class="m-0 font-weight-bold text-primary">{screen_info['name_ar']}</h6>
        </div>
        <div class="card-body">
            <p>هذه الشاشة تحت التطوير</p>
            <button type="button" class="btn btn-primary" onclick="alert('تحت التطوير')">
                إضافة جديد
            </button>
        </div>
    </div>
</div>
{{% endblock %}}
'''
        
        template_path = self.templates_path / screen_info['template']
        template_path.write_text(template_content, encoding='utf-8')
    
    def add_route_to_app(self, screen_id: str, screen_info: Dict):
        """إضافة رابط إلى app.py"""
        if not self.app_file.exists():
            return
        
        app_content = self.app_file.read_text(encoding='utf-8')
        
        route_code = f'''
@app.route('{screen_info['route']}')
@login_required
def {screen_id}():
    """{screen_info['name_ar']}"""
    return render_template('{screen_info['template']}')
'''
        
        # إضافة الرابط قبل if __name__ == '__main__':
        if "if __name__ == '__main__':" in app_content:
            app_content = app_content.replace(
                "if __name__ == '__main__':",
                route_code + "\nif __name__ == '__main__':"
            )
            self.app_file.write_text(app_content, encoding='utf-8')

def main():
    """الوظيفة الرئيسية"""
    print("🔍 أداة المراجعة البسيطة للنظام المحاسبي")
    print("🔍 Simple Audit Tool for Accounting System")
    print("=" * 60)
    
    audit_tool = SimpleAuditTool()
    
    # تشغيل الفحص
    audit_tool.run_audit()
    
    # سؤال عن الإصلاح التلقائي
    print("\n" + "=" * 60)
    response = input("هل تريد تشغيل الإصلاح التلقائي؟ (y/n): ").lower().strip()
    
    if response in ['y', 'yes', 'نعم', 'ن']:
        audit_tool.create_missing_files()
        print("\n🔄 إعادة تشغيل الفحص...")
        audit_tool.run_audit()
    
    print("\n✅ انتهى الفحص")

if __name__ == "__main__":
    main()
