#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل للنظام - الشاشات والقوالب والروابط
Comprehensive System Check - Screens, Templates, and Routes
"""

import os
import re
from pathlib import Path

def check_templates():
    """فحص القوالب الموجودة"""
    print("🎨 فحص القوالب (Templates):")
    print("=" * 40)
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ مجلد templates غير موجود")
        return []
    
    templates = []
    for template_file in templates_dir.glob("*.html"):
        templates.append(template_file.name)
        print(f"✅ {template_file.name}")
    
    print(f"📊 إجمالي القوالب: {len(templates)}")
    return templates

def check_routes():
    """فحص الروابط في app.py"""
    print("\n🔗 فحص الروابط (Routes):")
    print("=" * 40)
    
    if not os.path.exists("app.py"):
        print("❌ ملف app.py غير موجود")
        return []
    
    routes = []
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
        
        # البحث عن جميع الروابط
        route_pattern = r"@app\.route\(['\"]([^'\"]+)['\"](?:,\s*methods=\[([^\]]+)\])?\)"
        matches = re.findall(route_pattern, content)
        
        for match in matches:
            route_path = match[0]
            methods = match[1] if match[1] else "GET"
            routes.append((route_path, methods))
            print(f"✅ {route_path} [{methods}]")
    
    print(f"📊 إجمالي الروابط: {len(routes)}")
    return routes

def check_static_files():
    """فحص الملفات الثابتة"""
    print("\n📁 فحص الملفات الثابتة (Static Files):")
    print("=" * 40)
    
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ مجلد static غير موجود")
        return
    
    css_files = list(static_dir.glob("**/*.css"))
    js_files = list(static_dir.glob("**/*.js"))
    img_files = list(static_dir.glob("**/*.{png,jpg,jpeg,gif,svg,ico}"))
    
    print(f"🎨 ملفات CSS: {len(css_files)}")
    for css_file in css_files:
        print(f"   - {css_file}")
    
    print(f"⚡ ملفات JavaScript: {len(js_files)}")
    for js_file in js_files:
        print(f"   - {js_file}")
    
    print(f"🖼️ ملفات الصور: {len(img_files)}")
    for img_file in img_files:
        print(f"   - {img_file}")

def analyze_screen_completeness():
    """تحليل اكتمال الشاشات"""
    print("\n📋 تحليل اكتمال الشاشات:")
    print("=" * 40)
    
    # الشاشات المطلوبة
    required_screens = {
        "login.html": "شاشة تسجيل الدخول",
        "dashboard.html": "لوحة التحكم",
        "sales.html": "شاشة المبيعات",
        "purchases.html": "شاشة المشتريات", 
        "expenses.html": "شاشة المصروفات",
        "products.html": "شاشة المنتجات",
        "customers.html": "شاشة العملاء",
        "suppliers.html": "شاشة الموردين",
        "employee_payroll.html": "شاشة الرواتب",
        "financial_statements.html": "القوائم المالية",
        "advanced_reports.html": "التقارير المتقدمة",
        "advanced_expenses.html": "المصروفات المتقدمة",
        "new_purchase.html": "فاتورة مشتريات جديدة",
        "print_purchase.html": "طباعة فاتورة المشتريات"
    }
    
    templates_dir = Path("templates")
    existing_templates = set()
    if templates_dir.exists():
        existing_templates = {f.name for f in templates_dir.glob("*.html")}
    
    print("✅ الشاشات الموجودة:")
    for template in required_screens:
        if template in existing_templates:
            print(f"   ✅ {template} - {required_screens[template]}")
        else:
            print(f"   ❌ {template} - {required_screens[template]} (مفقود)")
    
    print(f"\n📊 الشاشات الموجودة: {len(existing_templates & set(required_screens.keys()))}/{len(required_screens)}")

def check_route_template_mapping():
    """فحص ربط الروابط بالقوالب"""
    print("\n🔄 فحص ربط الروابط بالقوالب:")
    print("=" * 40)
    
    if not os.path.exists("app.py"):
        print("❌ ملف app.py غير موجود")
        return
    
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # البحث عن render_template
    render_pattern = r"render_template\(['\"]([^'\"]+)['\"]"
    templates_used = re.findall(render_pattern, content)
    
    templates_dir = Path("templates")
    existing_templates = set()
    if templates_dir.exists():
        existing_templates = {f.name for f in templates_dir.glob("*.html")}
    
    print("🔗 القوالب المستخدمة في الكود:")
    for template in set(templates_used):
        if template in existing_templates:
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} (مفقود)")
    
    print("\n📁 القوالب الموجودة غير المستخدمة:")
    unused_templates = existing_templates - set(templates_used)
    for template in unused_templates:
        print(f"   ⚠️ {template}")

def check_database_models():
    """فحص نماذج قاعدة البيانات"""
    print("\n🗃️ فحص نماذج قاعدة البيانات:")
    print("=" * 40)
    
    if not os.path.exists("app.py"):
        print("❌ ملف app.py غير موجود")
        return
    
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # البحث عن النماذج
    model_pattern = r"class\s+(\w+)\(.*db\.Model\)"
    models = re.findall(model_pattern, content)
    
    print("📊 النماذج المعرفة في الكود:")
    for model in models:
        print(f"   ✅ {model}")
    
    print(f"\n📈 إجمالي النماذج: {len(models)}")

def generate_system_report():
    """إنشاء تقرير شامل لحالة النظام"""
    print("\n📊 تقرير حالة النظام:")
    print("=" * 40)

    # فحص الشاشات الأساسية
    core_screens = [
        ("login.html", "شاشة تسجيل الدخول"),
        ("dashboard.html", "لوحة التحكم"),
        ("sales.html", "شاشة المبيعات"),
        ("purchases.html", "شاشة المشتريات"),
        ("expenses.html", "شاشة المصروفات"),
        ("products.html", "شاشة المنتجات"),
        ("customers.html", "شاشة العملاء"),
        ("suppliers.html", "شاشة الموردين")
    ]

    templates_dir = Path("templates")
    existing_templates = set()
    if templates_dir.exists():
        existing_templates = {f.name for f in templates_dir.glob("*.html")}

    print("🎯 الشاشات الأساسية:")
    core_complete = 0
    for template, description in core_screens:
        if template in existing_templates:
            print(f"   ✅ {description}")
            core_complete += 1
        else:
            print(f"   ❌ {description}")

    print(f"\n📈 معدل اكتمال الشاشات الأساسية: {core_complete}/{len(core_screens)} ({core_complete/len(core_screens)*100:.1f}%)")

    # فحص قاعدة البيانات
    import sqlite3
    try:
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()

        required_tables = ['users', 'branches', 'products', 'customers', 'suppliers',
                          'sales', 'purchases', 'expenses', 'employee_payrolls']
        existing_tables = [table[0] for table in tables]

        print(f"\n🗃️ قاعدة البيانات: {len(existing_tables)} جدول")
        db_complete = sum(1 for table in required_tables if table in existing_tables)
        print(f"📊 الجداول الأساسية: {db_complete}/{len(required_tables)} ({db_complete/len(required_tables)*100:.1f}%)")

    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")

    # تقييم عام
    print(f"\n🎯 التقييم العام للنظام:")
    if core_complete == len(core_screens) and db_complete == len(required_tables):
        print("   🟢 النظام مكتمل وجاهز للاستخدام")
    elif core_complete >= len(core_screens) * 0.8:
        print("   🟡 النظام شبه مكتمل - يحتاج تحسينات طفيفة")
    else:
        print("   🔴 النظام يحتاج المزيد من العمل")

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔍 فحص شامل للنظام - System Comprehensive Check")
    print("=" * 60)

    # فحص القوالب
    templates = check_templates()

    # فحص الروابط
    routes = check_routes()

    # فحص الملفات الثابتة
    check_static_files()

    # تحليل اكتمال الشاشات
    analyze_screen_completeness()

    # فحص ربط الروابط بالقوالب
    check_route_template_mapping()

    # فحص نماذج قاعدة البيانات
    check_database_models()

    # إنشاء تقرير شامل
    generate_system_report()

    print("\n" + "=" * 60)
    print("✅ انتهى الفحص الشامل للنظام")
    print("✅ System comprehensive check completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
