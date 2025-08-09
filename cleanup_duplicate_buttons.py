#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تنظيف الأزرار المكررة وإنشاء مكونات مشتركة
Cleanup Duplicate Buttons and Create Shared Components
"""

import os
import re
from pathlib import Path

class ButtonCleanup:
    def __init__(self):
        self.templates_dir = Path('templates')
        self.components_dir = Path('templates/components')
        self.components_dir.mkdir(exist_ok=True)
        
    def create_shared_components(self):
        """إنشاء مكونات مشتركة للأزرار المكررة"""
        print("🔧 إنشاء مكونات مشتركة...")
        
        # مكون أزرار الإجراءات الأساسية
        basic_actions_component = '''<!-- مكون الأزرار الأساسية المشتركة -->
<div class="btn-group" role="group">
    <!-- زر الحفظ -->
    <button type="button" class="btn btn-success btn-sm" onclick="{{ save_function|default('saveData()') }}">
        <i class="fas fa-save me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}حفظ{% else %}Save{% endif %}
    </button>
    
    <!-- زر التحديث -->
    <button type="button" class="btn btn-info btn-sm" onclick="{{ refresh_function|default('refreshData()') }}">
        <i class="fas fa-sync-alt me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}تحديث{% else %}Refresh{% endif %}
    </button>
    
    <!-- زر التصدير -->
    <button type="button" class="btn btn-secondary btn-sm" onclick="{{ export_function|default('exportData()') }}">
        <i class="fas fa-download me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}تصدير{% else %}Export{% endif %}
    </button>
    
    <!-- زر الطباعة -->
    <button type="button" class="btn btn-primary btn-sm" onclick="{{ print_function|default('printReport()') }}">
        <i class="fas fa-print me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}طباعة{% else %}Print{% endif %}
    </button>
</div>'''
        
        with open(self.components_dir / 'basic_actions.html', 'w', encoding='utf-8') as f:
            f.write(basic_actions_component)
        
        # مكون أزرار إدارة البيانات
        data_management_component = '''<!-- مكون أزرار إدارة البيانات -->
<div class="btn-toolbar" role="toolbar">
    <div class="btn-group me-2" role="group">
        <!-- زر إضافة -->
        <button type="button" class="btn btn-success btn-sm" onclick="{{ add_function|default('addNew()') }}">
            <i class="fas fa-plus me-1"></i>
            {% if session.get('language', 'ar') == 'ar' %}إضافة{% else %}Add{% endif %}
        </button>
        
        <!-- زر تعديل -->
        <button type="button" class="btn btn-warning btn-sm" onclick="{{ edit_function|default('editSelected()') }}">
            <i class="fas fa-edit me-1"></i>
            {% if session.get('language', 'ar') == 'ar' %}تعديل{% else %}Edit{% endif %}
        </button>
        
        <!-- زر حذف -->
        <button type="button" class="btn btn-danger btn-sm" onclick="{{ delete_function|default('deleteSelected()') }}">
            <i class="fas fa-trash me-1"></i>
            {% if session.get('language', 'ar') == 'ar' %}حذف{% else %}Delete{% endif %}
        </button>
    </div>
    
    <div class="btn-group" role="group">
        <!-- زر مسح الفلاتر -->
        <button type="button" class="btn btn-outline-secondary btn-sm" onclick="{{ clear_function|default('clearFilters()') }}">
            <i class="fas fa-times me-1"></i>
            {% if session.get('language', 'ar') == 'ar' %}مسح الفلاتر{% else %}Clear Filters{% endif %}
        </button>
    </div>
</div>'''
        
        with open(self.components_dir / 'data_management.html', 'w', encoding='utf-8') as f:
            f.write(data_management_component)
        
        # مكون أزرار اللغة
        language_component = '''<!-- مكون أزرار تغيير اللغة -->
<div class="btn-group btn-group-sm" role="group">
    <a href="?lang=ar" class="btn btn-outline-primary {{ 'active' if session.get('language', 'ar') == 'ar' else '' }}">
        العربية
    </a>
    <a href="?lang=en" class="btn btn-outline-primary {{ 'active' if session.get('language', 'ar') == 'en' else '' }}">
        English
    </a>
</div>'''
        
        with open(self.components_dir / 'language_switcher.html', 'w', encoding='utf-8') as f:
            f.write(language_component)
        
        # مكون أزرار النماذج
        form_actions_component = '''<!-- مكون أزرار النماذج -->
<div class="d-flex justify-content-end gap-2">
    <!-- زر الحفظ -->
    <button type="submit" class="btn btn-success">
        <i class="fas fa-save me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}{{ save_text|default('حفظ') }}{% else %}{{ save_text|default('Save') }}{% endif %}
    </button>
    
    <!-- زر الإلغاء -->
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
        <i class="fas fa-times me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}إلغاء{% else %}Cancel{% endif %}
    </button>
    
    <!-- زر إعادة التعيين -->
    <button type="reset" class="btn btn-outline-warning">
        <i class="fas fa-undo me-1"></i>
        {% if session.get('language', 'ar') == 'ar' %}إعادة تعيين{% else %}Reset{% endif %}
    </button>
</div>'''
        
        with open(self.components_dir / 'form_actions.html', 'w', encoding='utf-8') as f:
            f.write(form_actions_component)
        
        print("✅ تم إنشاء 4 مكونات مشتركة")
    
    def create_macro_file(self):
        """إنشاء ملف الماكرو للأزرار المشتركة"""
        macro_content = '''<!-- ماكرو الأزرار المشتركة -->
{% macro action_button(type, text, icon, onclick, class="btn-sm") %}
<button type="button" class="btn btn-{{ type }} {{ class }}" onclick="{{ onclick }}">
    <i class="fas fa-{{ icon }} me-1"></i>
    {% if session.get('language', 'ar') == 'ar' %}{{ text.ar }}{% else %}{{ text.en }}{% endif %}
</button>
{% endmacro %}

{% macro save_button(onclick="saveData()", class="btn-sm") %}
{{ action_button('success', {'ar': 'حفظ', 'en': 'Save'}, 'save', onclick, class) }}
{% endmacro %}

{% macro edit_button(onclick="editData()", class="btn-sm") %}
{{ action_button('warning', {'ar': 'تعديل', 'en': 'Edit'}, 'edit', onclick, class) }}
{% endmacro %}

{% macro delete_button(onclick="deleteData()", class="btn-sm") %}
{{ action_button('danger', {'ar': 'حذف', 'en': 'Delete'}, 'trash', onclick, class) }}
{% endmacro %}

{% macro refresh_button(onclick="refreshData()", class="btn-sm") %}
{{ action_button('info', {'ar': 'تحديث', 'en': 'Refresh'}, 'sync-alt', onclick, class) }}
{% endmacro %}

{% macro export_button(onclick="exportData()", class="btn-sm") %}
{{ action_button('secondary', {'ar': 'تصدير', 'en': 'Export'}, 'download', onclick, class) }}
{% endmacro %}

{% macro print_button(onclick="printReport()", class="btn-sm") %}
{{ action_button('primary', {'ar': 'طباعة', 'en': 'Print'}, 'print', onclick, class) }}
{% endmacro %}

{% macro add_button(onclick="addNew()", class="btn-sm") %}
{{ action_button('success', {'ar': 'إضافة', 'en': 'Add'}, 'plus', onclick, class) }}
{% endmacro %}

{% macro close_button(onclick="", class="btn-sm") %}
<button type="button" class="btn btn-secondary {{ class }}" data-bs-dismiss="modal" onclick="{{ onclick }}">
    <i class="fas fa-times me-1"></i>
    {% if session.get('language', 'ar') == 'ar' %}إغلاق{% else %}Close{% endif %}
</button>
{% endmacro %}

{% macro reset_button(onclick="", class="btn-sm") %}
<button type="reset" class="btn btn-outline-warning {{ class }}" onclick="{{ onclick }}">
    <i class="fas fa-undo me-1"></i>
    {% if session.get('language', 'ar') == 'ar' %}إعادة تعيين{% else %}Reset{% endif %}
</button>
{% endmacro %}'''
        
        with open(self.components_dir / 'button_macros.html', 'w', encoding='utf-8') as f:
            f.write(macro_content)
        
        print("✅ تم إنشاء ملف الماكرو للأزرار")
    
    def remove_duplicate_language_buttons(self):
        """إزالة أزرار اللغة المكررة من الملفات الأساسية"""
        print("🧹 إزالة أزرار اللغة المكررة...")
        
        base_files = ['base_fixed.html', 'base_simple.html', 'base_unified.html']
        
        for file_name in base_files:
            file_path = self.templates_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # إزالة أزرار اللغة المكررة واستبدالها بالمكون المشترك
                    language_pattern = r'<div class="language-switcher">.*?</div>'
                    replacement = '{% include "components/language_switcher.html" %}'
                    
                    new_content = re.sub(language_pattern, replacement, content, flags=re.DOTALL)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ تم تنظيف {file_name}")
                    
                except Exception as e:
                    print(f"❌ خطأ في تنظيف {file_name}: {e}")
    
    def create_usage_guide(self):
        """إنشاء دليل استخدام المكونات المشتركة"""
        guide_content = '''# دليل استخدام المكونات المشتركة
## Shared Components Usage Guide

## 1. الأزرار الأساسية (Basic Actions)
```html
{% include "components/basic_actions.html" %}
```

### مع معاملات مخصصة:
```html
{% set save_function = "saveProduct()" %}
{% set refresh_function = "loadProducts()" %}
{% include "components/basic_actions.html" %}
```

## 2. إدارة البيانات (Data Management)
```html
{% include "components/data_management.html" %}
```

### مع معاملات مخصصة:
```html
{% set add_function = "addCustomer()" %}
{% set edit_function = "editCustomer()" %}
{% set delete_function = "deleteCustomer()" %}
{% include "components/data_management.html" %}
```

## 3. أزرار النماذج (Form Actions)
```html
{% include "components/form_actions.html" %}
```

### مع نص مخصص:
```html
{% set save_text = "حفظ المنتج" %}
{% include "components/form_actions.html" %}
```

## 4. استخدام الماكرو
```html
{% from "components/button_macros.html" import save_button, edit_button, delete_button %}

{{ save_button("saveProduct()") }}
{{ edit_button("editProduct(1)") }}
{{ delete_button("deleteProduct(1)") }}
```

## 5. أزرار اللغة
```html
{% include "components/language_switcher.html" %}
```

## فوائد استخدام المكونات المشتركة:
- ✅ تقليل التكرار
- ✅ سهولة الصيانة
- ✅ توحيد التصميم
- ✅ تحسين الأداء
- ✅ تقليل حجم الملفات
'''
        
        with open('SHARED_COMPONENTS_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ تم إنشاء دليل استخدام المكونات المشتركة")
    
    def run_cleanup(self):
        """تشغيل عملية التنظيف الكاملة"""
        print("🧹 بدء تنظيف الأزرار المكررة")
        print("=" * 50)
        
        self.create_shared_components()
        self.create_macro_file()
        self.remove_duplicate_language_buttons()
        self.create_usage_guide()
        
        print("\n" + "=" * 50)
        print("✅ تم إنجاز التنظيف بنجاح!")
        print("📁 المكونات المشتركة في: templates/components/")
        print("📄 دليل الاستخدام: SHARED_COMPONENTS_GUIDE.md")
        print("=" * 50)

def main():
    """الوظيفة الرئيسية"""
    cleanup = ButtonCleanup()
    cleanup.run_cleanup()

if __name__ == "__main__":
    main()
