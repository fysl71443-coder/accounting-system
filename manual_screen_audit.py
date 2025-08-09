#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Screen Audit - فحص يدوي للشاشات
فحص تنسيق الشاشات والوظائف المفقودة
"""

import os
import re
from pathlib import Path

def audit_template_files():
    """فحص ملفات القوالب"""
    print("🔍 فحص ملفات القوالب...")
    print("🔍 Auditing template files...")
    print("=" * 60)
    
    templates_dir = Path('templates')
    screen_analysis = {}
    
    # قائمة الشاشات الرئيسية
    main_screens = [
        'dashboard_unified.html',
        'sales.html', 
        'purchases.html',
        'products.html',
        'customers.html',
        'suppliers.html',
        'reports.html',
        'advanced_reports.html',
        'expenses.html',
        'financial_statements.html',
        'payments_dues.html',
        'tax_management.html',
        'employee_payroll.html',
        'inventory.html'
    ]
    
    for screen_file in main_screens:
        screen_path = templates_dir / screen_file
        
        if not screen_path.exists():
            print(f"❌ {screen_file} - الملف غير موجود")
            continue
        
        print(f"\n📄 فحص: {screen_file}")
        print("-" * 40)
        
        try:
            with open(screen_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'file_size': len(content),
                'has_buttons': False,
                'button_count': 0,
                'has_form': False,
                'has_table': False,
                'has_modals': False,
                'extends_unified': False,
                'missing_elements': [],
                'issues': []
            }
            
            # فحص الوراثة
            if 'extends "base_unified.html"' in content:
                analysis['extends_unified'] = True
                print("✅ يستخدم base_unified.html")
            else:
                print("❌ لا يستخدم base_unified.html")
                analysis['issues'].append('Not using base_unified.html')
            
            # فحص الأزرار
            button_patterns = [
                'btnSave', 'btnEdit', 'btnDelete', 'btnPreview', 
                'btnPrint', 'btnSearch', 'btnSelectInvoice', 'btnRegisterPayment'
            ]
            
            buttons_found = []
            for pattern in button_patterns:
                if pattern in content:
                    buttons_found.append(pattern)
            
            analysis['button_count'] = len(buttons_found)
            analysis['has_buttons'] = len(buttons_found) > 0
            
            if buttons_found:
                print(f"✅ الأزرار: {', '.join(buttons_found)} ({len(buttons_found)})")
            else:
                print("❌ لا توجد أزرار")
                analysis['missing_elements'].append('buttons')
            
            # فحص النماذج
            form_count = len(re.findall(r'<form', content))
            if form_count > 0:
                analysis['has_form'] = True
                print(f"✅ النماذج: {form_count}")
            else:
                print("⚠️ لا توجد نماذج")
            
            # فحص الجداول
            table_count = len(re.findall(r'<table', content))
            if table_count > 0:
                analysis['has_table'] = True
                print(f"✅ الجداول: {table_count}")
            else:
                print("⚠️ لا توجد جداول")
            
            # فحص النوافذ المنبثقة
            modal_count = len(re.findall(r'modal', content))
            if modal_count > 0:
                analysis['has_modals'] = True
                print(f"✅ النوافذ المنبثقة: {modal_count}")
            else:
                print("⚠️ لا توجد نوافذ منبثقة")
            
            # فحص مكونات الأزرار
            if 'components/' in content and '_buttons.html' in content:
                print("✅ يستخدم مكونات الأزرار")
            else:
                print("⚠️ لا يستخدم مكونات الأزرار")
                analysis['missing_elements'].append('button_components')
            
            # فحص JavaScript
            if 'Handler' in content or 'onclick' in content:
                print("✅ يحتوي على JavaScript handlers")
            else:
                print("⚠️ لا يحتوي على JavaScript handlers")
                analysis['missing_elements'].append('javascript_handlers')
            
            screen_analysis[screen_file] = analysis
            
        except Exception as e:
            print(f"❌ خطأ في فحص {screen_file}: {str(e)}")
    
    return screen_analysis

def audit_button_components():
    """فحص مكونات الأزرار"""
    print(f"\n🔍 فحص مكونات الأزرار...")
    print("🔍 Auditing button components...")
    print("=" * 60)
    
    components_dir = Path('templates/components')
    
    if not components_dir.exists():
        print("❌ مجلد components غير موجود")
        return {}
    
    button_components = {}
    
    for component_file in components_dir.glob('*_buttons.html'):
        print(f"\n📄 فحص: {component_file.name}")
        print("-" * 40)
        
        try:
            with open(component_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # عد الأزرار
            button_count = len(re.findall(r'<button', content))
            
            # فحص أنواع الأزرار
            button_types = []
            if 'btnSave' in content: button_types.append('Save')
            if 'btnEdit' in content: button_types.append('Edit')
            if 'btnDelete' in content: button_types.append('Delete')
            if 'btnPreview' in content: button_types.append('Preview')
            if 'btnPrint' in content: button_types.append('Print')
            if 'btnSearch' in content: button_types.append('Search')
            if 'btnSelectInvoice' in content: button_types.append('SelectInvoice')
            if 'btnRegisterPayment' in content: button_types.append('RegisterPayment')
            
            print(f"✅ عدد الأزرار: {button_count}")
            print(f"✅ أنواع الأزرار: {', '.join(button_types)}")
            
            # فحص JavaScript handlers
            if 'Handler' in content:
                print("✅ يحتوي على JavaScript handlers")
            else:
                print("⚠️ لا يحتوي على JavaScript handlers")
            
            button_components[component_file.name] = {
                'button_count': button_count,
                'button_types': button_types,
                'has_handlers': 'Handler' in content
            }
            
        except Exception as e:
            print(f"❌ خطأ في فحص {component_file.name}: {str(e)}")
    
    return button_components

def audit_api_routes():
    """فحص routes في app.py"""
    print(f"\n🔍 فحص API routes...")
    print("🔍 Auditing API routes...")
    print("=" * 60)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # البحث عن جميع routes
        routes = re.findall(r"@app\.route\('([^']+)'", app_content)
        
        print(f"📊 إجمالي Routes: {len(routes)}")
        
        # تصنيف Routes
        screen_routes = []
        api_routes = []
        other_routes = []
        
        for route in routes:
            if route.startswith('/api/'):
                api_routes.append(route)
            elif route in ['/', '/login', '/logout', '/dashboard']:
                other_routes.append(route)
            else:
                screen_routes.append(route)
        
        print(f"\n📄 Screen Routes ({len(screen_routes)}):")
        for route in sorted(screen_routes):
            print(f"  • {route}")
        
        print(f"\n🔗 API Routes ({len(api_routes)}):")
        for route in sorted(api_routes):
            print(f"  • {route}")
        
        # فحص API routes لكل شاشة
        expected_apis = {
            'sales': ['save', 'edit', 'delete', 'preview', 'print', 'select_invoice', 'register_payment'],
            'products': ['save', 'edit', 'delete', 'search', 'print'],
            'purchases': ['save', 'edit', 'delete', 'preview', 'print', 'select_invoice', 'register_payment'],
            'customers': ['save', 'edit', 'delete', 'search', 'print'],
            'suppliers': ['save', 'edit', 'delete', 'search', 'print']
        }
        
        print(f"\n🔍 فحص API completeness:")
        for screen, expected in expected_apis.items():
            print(f"\n{screen.upper()}:")
            for action in expected:
                api_route = f"/api/{screen}/{action}"
                if api_route in api_routes or any(action in route for route in api_routes if screen in route):
                    print(f"  ✅ {action}")
                else:
                    print(f"  ❌ {action} - مفقود")
        
        return {
            'total_routes': len(routes),
            'screen_routes': screen_routes,
            'api_routes': api_routes,
            'other_routes': other_routes
        }
        
    except Exception as e:
        print(f"❌ خطأ في فحص app.py: {str(e)}")
        return {}

def generate_improvement_plan(screen_analysis, button_components, routes_analysis):
    """إنشاء خطة التحسين"""
    print(f"\n💡 خطة التحسين والتطوير...")
    print("💡 Improvement and Development Plan...")
    print("=" * 80)
    
    improvements = []
    
    # تحليل الشاشات
    screens_without_buttons = []
    screens_without_forms = []
    screens_with_issues = []
    
    for screen, analysis in screen_analysis.items():
        if not analysis['has_buttons']:
            screens_without_buttons.append(screen)
        
        if not analysis['has_form'] and screen not in ['dashboard_unified.html', 'reports.html']:
            screens_without_forms.append(screen)
        
        if analysis['issues']:
            screens_with_issues.append((screen, analysis['issues']))
    
    # إنشاء التوصيات
    if screens_without_buttons:
        improvements.append({
            'priority': 'HIGH',
            'category': 'Button System',
            'description': 'إضافة نظام الأزرار للشاشات التالية',
            'screens': screens_without_buttons,
            'action': 'Add button components and handlers'
        })
    
    if screens_without_forms:
        improvements.append({
            'priority': 'MEDIUM',
            'category': 'Forms',
            'description': 'إضافة نماذج الإدخال للشاشات التالية',
            'screens': screens_without_forms,
            'action': 'Add input forms with validation'
        })
    
    if screens_with_issues:
        improvements.append({
            'priority': 'HIGH',
            'category': 'Template Issues',
            'description': 'إصلاح مشاكل القوالب',
            'screens': [s[0] for s in screens_with_issues],
            'action': 'Fix template inheritance and structure'
        })
    
    # طباعة الخطة
    for i, improvement in enumerate(improvements, 1):
        print(f"\n{i}. {improvement['description']}")
        print(f"   الأولوية: {improvement['priority']}")
        print(f"   الفئة: {improvement['category']}")
        print(f"   الشاشات المتأثرة: {len(improvement['screens'])}")
        for screen in improvement['screens']:
            print(f"     • {screen}")
        print(f"   الإجراء المطلوب: {improvement['action']}")
    
    return improvements

def main():
    """تشغيل الفحص اليدوي"""
    print("🚀 بدء الفحص اليدوي للنظام")
    print("🚀 Starting manual system audit")
    print("=" * 80)
    
    # فحص القوالب
    screen_analysis = audit_template_files()
    
    # فحص مكونات الأزرار
    button_components = audit_button_components()
    
    # فحص API routes
    routes_analysis = audit_api_routes()
    
    # إنشاء خطة التحسين
    improvements = generate_improvement_plan(screen_analysis, button_components, routes_analysis)
    
    # ملخص النتائج
    print(f"\n" + "=" * 80)
    print("📊 ملخص نتائج الفحص")
    print("📊 Audit Results Summary")
    print("=" * 80)
    
    total_screens = len(screen_analysis)
    screens_with_buttons = sum(1 for s in screen_analysis.values() if s['has_buttons'])
    screens_with_forms = sum(1 for s in screen_analysis.values() if s['has_form'])
    
    print(f"• إجمالي الشاشات: {total_screens}")
    print(f"• الشاشات مع أزرار: {screens_with_buttons}/{total_screens}")
    print(f"• الشاشات مع نماذج: {screens_with_forms}/{total_screens}")
    print(f"• مكونات الأزرار: {len(button_components)}")
    print(f"• إجمالي Routes: {routes_analysis.get('total_routes', 0)}")
    print(f"• توصيات التحسين: {len(improvements)}")
    
    print(f"\n🎯 الخطوة التالية:")
    print("🎯 Next Step:")
    print("تنفيذ خطة التحسين بدءاً من الأولوية العالية")
    print("Implement improvement plan starting with HIGH priority items")

if __name__ == "__main__":
    main()
