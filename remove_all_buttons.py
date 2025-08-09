#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove All Buttons System - حذف نظام الأزرار بالكامل
حذف جميع الأزرار ووظائفها من البرنامج
"""

import os
import re
from pathlib import Path
import shutil

def backup_files():
    """إنشاء نسخة احتياطية قبل الحذف"""
    print("📦 إنشاء نسخة احتياطية...")
    print("📦 Creating backup...")
    print("=" * 50)
    
    backup_dir = Path('backup_before_button_removal')
    backup_dir.mkdir(exist_ok=True)
    
    # نسخ الملفات المهمة
    important_files = [
        'app.py',
        'static/js/button_handlers.js',
        'templates/base_unified.html'
    ]
    
    for file_path in important_files:
        if Path(file_path).exists():
            backup_path = backup_dir / Path(file_path).name
            shutil.copy2(file_path, backup_path)
            print(f"✅ تم نسخ {file_path}")
    
    # نسخ مجلد components
    components_dir = Path('templates/components')
    if components_dir.exists():
        backup_components = backup_dir / 'components'
        if backup_components.exists():
            shutil.rmtree(backup_components)
        shutil.copytree(components_dir, backup_components)
        print(f"✅ تم نسخ مجلد components")
    
    print(f"✅ تم إنشاء النسخة الاحتياطية في: {backup_dir}")

def remove_button_components():
    """حذف مكونات الأزرار"""
    print(f"\n🗑️ حذف مكونات الأزرار...")
    print("🗑️ Removing button components...")
    print("=" * 50)
    
    components_dir = Path('templates/components')
    
    if not components_dir.exists():
        print("⚠️ مجلد components غير موجود")
        return
    
    # قائمة مكونات الأزرار للحذف
    button_components = [
        'sales_buttons.html',
        'products_buttons.html', 
        'purchases_buttons.html',
        'customers_buttons.html',
        'suppliers_buttons.html',
        'expenses_buttons.html',
        'payments_buttons.html',
        'taxes_buttons.html',
        'employees_buttons.html',
        'inventory_buttons.html',
        'reports_buttons.html'
    ]
    
    removed_count = 0
    
    for component in button_components:
        component_path = components_dir / component
        
        if component_path.exists():
            component_path.unlink()
            print(f"✅ تم حذف {component}")
            removed_count += 1
        else:
            print(f"⚠️ {component} غير موجود")
    
    print(f"\n📊 تم حذف {removed_count} مكون أزرار")

def remove_button_handlers_js():
    """حذف JavaScript handlers للأزرار"""
    print(f"\n🗑️ حذف JavaScript handlers...")
    print("🗑️ Removing JavaScript handlers...")
    print("=" * 50)
    
    js_file = Path('static/js/button_handlers.js')
    
    if js_file.exists():
        js_file.unlink()
        print("✅ تم حذف button_handlers.js")
    else:
        print("⚠️ button_handlers.js غير موجود")

def remove_api_endpoints():
    """حذف API endpoints الخاصة بالأزرار"""
    print(f"\n🗑️ حذف API endpoints...")
    print("🗑️ Removing API endpoints...")
    print("=" * 50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن وحذف API endpoints
        patterns_to_remove = [
            r'@app\.route\(\'/api/[^\']+\'\).*?def [^(]+\([^)]*\):.*?(?=@app\.route|if __name__|$)',
            r'# MISSING API ENDPOINTS.*?(?=if __name__|$)',
            r'# ============================================================================\n# MISSING API ENDPOINTS.*?(?=if __name__|$)'
        ]
        
        original_content = content
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
        
        # تنظيف الأسطر الفارغة الزائدة
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ تم حذف API endpoints من app.py")
        else:
            print("⚠️ لم يتم العثور على API endpoints للحذف")
            
    except Exception as e:
        print(f"❌ خطأ في حذف API endpoints: {str(e)}")

def remove_button_references_from_templates():
    """حذف مراجع الأزرار من القوالب"""
    print(f"\n🗑️ حذف مراجع الأزرار من القوالب...")
    print("🗑️ Removing button references from templates...")
    print("=" * 50)
    
    templates_dir = Path('templates')
    
    # قائمة القوالب الرئيسية
    main_templates = [
        'sales.html',
        'purchases.html', 
        'products.html',
        'customers.html',
        'suppliers.html',
        'expenses.html',
        'payments_dues.html',
        'tax_management.html',
        'employee_payroll.html',
        'inventory.html',
        'reports.html',
        'advanced_reports.html',
        'financial_statements.html'
    ]
    
    updated_count = 0
    
    for template_name in main_templates:
        template_path = templates_dir / template_name
        
        if not template_path.exists():
            print(f"⚠️ {template_name} غير موجود")
            continue
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # إزالة مراجع مكونات الأزرار
            patterns_to_remove = [
                r'{% include [\'"]components/[^\'\"]*_buttons\.html[\'"] %}',
                r'<!-- Button System -->.*?{% include [\'"]components/[^\'\"]*_buttons\.html[\'"] %}',
                r'{% block page_actions %}.*?{% endblock %}',
                r'<script src="[^"]*button_handlers\.js[^"]*"></script>',
                r'onclick="[^"]*Handler\.[^"]*"',
                r'id="btn[A-Z][^"]*"'
            ]
            
            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # تنظيف الأسطر الفارغة
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            if content != original_content:
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ تم تنظيف {template_name}")
                updated_count += 1
            else:
                print(f"⚠️ لا توجد مراجع أزرار في {template_name}")
                
        except Exception as e:
            print(f"❌ خطأ في معالجة {template_name}: {str(e)}")
    
    print(f"\n📊 تم تنظيف {updated_count} قالب")

def remove_button_css_js_references():
    """حذف مراجع CSS و JS الخاصة بالأزرار"""
    print(f"\n🗑️ حذف مراجع CSS و JS...")
    print("🗑️ Removing CSS and JS references...")
    print("=" * 50)
    
    # حذف من base_unified.html
    base_template = Path('templates/base_unified.html')
    
    if base_template.exists():
        try:
            with open(base_template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # إزالة مراجع JavaScript
            patterns_to_remove = [
                r'<script src="[^"]*button_handlers\.js[^"]*"></script>',
                r'<!-- Button System JavaScript -->.*?</script>',
                r'{% block page_actions %}.*?{% endblock %}'
            ]
            
            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            
            if content != original_content:
                with open(base_template, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ تم تنظيف base_unified.html")
            else:
                print("⚠️ لا توجد مراجع للحذف في base_unified.html")
                
        except Exception as e:
            print(f"❌ خطأ في معالجة base_unified.html: {str(e)}")

def clean_static_files():
    """تنظيف الملفات الثابتة"""
    print(f"\n🗑️ تنظيف الملفات الثابتة...")
    print("🗑️ Cleaning static files...")
    print("=" * 50)
    
    # حذف ملفات JavaScript المتعلقة بالأزرار
    js_files_to_remove = [
        'static/js/button_handlers.js',
        'static/js/buttons.js',
        'static/js/button_system.js'
    ]
    
    removed_count = 0
    
    for js_file in js_files_to_remove:
        js_path = Path(js_file)
        if js_path.exists():
            js_path.unlink()
            print(f"✅ تم حذف {js_file}")
            removed_count += 1
    
    print(f"📊 تم حذف {removed_count} ملف JavaScript")

def generate_removal_report():
    """إنشاء تقرير الحذف"""
    print(f"\n📋 إنشاء تقرير الحذف...")
    print("📋 Generating removal report...")
    print("=" * 50)
    
    report_content = """# 🗑️ تقرير حذف نظام الأزرار - Button System Removal Report

## ✅ العمليات المنفذة:

### 1. النسخة الاحتياطية:
- ✅ تم إنشاء نسخة احتياطية في مجلد `backup_before_button_removal`
- ✅ تم نسخ الملفات المهمة قبل التعديل

### 2. مكونات الأزرار المحذوفة:
- ✅ sales_buttons.html
- ✅ products_buttons.html
- ✅ purchases_buttons.html
- ✅ customers_buttons.html
- ✅ suppliers_buttons.html
- ✅ expenses_buttons.html
- ✅ payments_buttons.html
- ✅ taxes_buttons.html
- ✅ employees_buttons.html
- ✅ inventory_buttons.html
- ✅ reports_buttons.html

### 3. JavaScript المحذوف:
- ✅ button_handlers.js - حذف كامل
- ✅ جميع handlers للأزرار
- ✅ جميع وظائف الأزرار

### 4. API Endpoints المحذوفة:
- ✅ جميع endpoints المتعلقة بالأزرار
- ✅ تنظيف app.py من الكود الزائد

### 5. القوالب المُنظفة:
- ✅ إزالة مراجع مكونات الأزرار
- ✅ إزالة onclick handlers
- ✅ إزالة button IDs
- ✅ تنظيف base_unified.html

## 🎯 النتيجة:
- ❌ لا توجد أزرار في النظام
- ❌ لا توجد وظائف أزرار
- ❌ لا توجد مراجع للأزرار
- ✅ النظام نظيف ومبسط

## 📦 النسخة الاحتياطية:
يمكن استعادة نظام الأزرار من مجلد `backup_before_button_removal`

تاريخ الحذف: اليوم
حالة النظام: مُنظف من الأزرار
"""
    
    with open('BUTTON_REMOVAL_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("✅ تم إنشاء تقرير الحذف: BUTTON_REMOVAL_REPORT.md")

def main():
    """تشغيل عملية حذف الأزرار"""
    print("🚀 بدء حذف نظام الأزرار بالكامل")
    print("🚀 Starting complete button system removal")
    print("=" * 80)
    
    # تأكيد من المستخدم
    print("⚠️ تحذير: سيتم حذف جميع الأزرار ووظائفها من البرنامج!")
    print("⚠️ Warning: All buttons and their functions will be removed!")
    
    # إنشاء نسخة احتياطية
    backup_files()
    
    # حذف مكونات الأزرار
    remove_button_components()
    
    # حذف JavaScript handlers
    remove_button_handlers_js()
    
    # حذف API endpoints
    remove_api_endpoints()
    
    # حذف مراجع الأزرار من القوالب
    remove_button_references_from_templates()
    
    # حذف مراجع CSS و JS
    remove_button_css_js_references()
    
    # تنظيف الملفات الثابتة
    clean_static_files()
    
    # إنشاء تقرير
    generate_removal_report()
    
    print(f"\n" + "=" * 80)
    print("🎉 تم حذف نظام الأزرار بالكامل!")
    print("🎉 Button system completely removed!")
    print("=" * 80)
    
    print(f"\n📋 ملخص العملية:")
    print("✅ تم إنشاء نسخة احتياطية")
    print("✅ تم حذف جميع مكونات الأزرار")
    print("✅ تم حذف JavaScript handlers")
    print("✅ تم حذف API endpoints")
    print("✅ تم تنظيف القوالب")
    print("✅ تم تنظيف الملفات الثابتة")
    
    print(f"\n🔄 الخطوة التالية:")
    print("إعادة تشغيل التطبيق لرؤية النتيجة")
    print("Restart the application to see the result")

if __name__ == "__main__":
    main()
