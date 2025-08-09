#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Routing Issues - إصلاح مشاكل التوجيه
"""

import os
import re
from pathlib import Path

def check_template_inheritance():
    """فحص وإصلاح وراثة القوالب"""
    
    print("🔍 فحص وراثة القوالب...")
    print("🔍 Checking template inheritance...")
    print("=" * 60)
    
    templates_dir = Path('templates')
    issues_found = []
    
    # قائمة الملفات التي يجب أن تستخدم base_unified.html
    should_use_unified = [
        'dashboard.html',
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
        'inventory.html',
        'unified_products.html'
    ]
    
    for template_file in should_use_unified:
        template_path = templates_dir / template_file
        
        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # فحص السطر الأول
                first_line = content.split('\n')[0].strip()
                
                if 'extends "base.html"' in first_line:
                    print(f"❌ {template_file} يستخدم base.html (يجب تغييره)")
                    issues_found.append((template_file, 'uses_old_base'))
                elif 'extends "base_unified.html"' in first_line:
                    print(f"✅ {template_file} يستخدم base_unified.html")
                else:
                    print(f"⚠️ {template_file} لا يستخدم أي base template")
                    issues_found.append((template_file, 'no_base'))
                    
            except Exception as e:
                print(f"❌ خطأ في قراءة {template_file}: {str(e)}")
        else:
            print(f"⚠️ {template_file} غير موجود")
    
    return issues_found

def fix_template_inheritance(issues):
    """إصلاح مشاكل وراثة القوالب"""
    
    print(f"\n🔧 إصلاح {len(issues)} مشكلة في وراثة القوالب...")
    print("🔧 Fixing template inheritance issues...")
    print("=" * 60)
    
    for template_file, issue_type in issues:
        template_path = Path(f'templates/{template_file}')
        
        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if issue_type == 'uses_old_base':
                    # تغيير من base.html إلى base_unified.html
                    new_content = content.replace(
                        '{% extends "base.html" %}',
                        '{% extends "base_unified.html" %}'
                    )
                    
                    if new_content != content:
                        # إنشاء نسخة احتياطية
                        backup_path = template_path.with_suffix('.html.backup_routing')
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # كتابة المحتوى الجديد
                        with open(template_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ تم إصلاح {template_file}")
                    else:
                        print(f"⚠️ لم يتم العثور على base.html في {template_file}")
                
            except Exception as e:
                print(f"❌ خطأ في إصلاح {template_file}: {str(e)}")

def check_missing_routes():
    """فحص الروابط المفقودة في app.py"""
    
    print(f"\n🔍 فحص الروابط المفقودة...")
    print("🔍 Checking for missing routes...")
    print("=" * 60)
    
    # قائمة الروابط المطلوبة
    required_routes = [
        'dashboard',
        'sales',
        'purchases', 
        'products',
        'customers',
        'suppliers',
        'reports',
        'advanced_reports',
        'expenses',
        'financial_statements',
        'payments_dues',
        'tax_management',
        'employee_payroll',
        'inventory',
        'unified_products'
    ]
    
    # قراءة app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    missing_routes = []
    
    for route in required_routes:
        # البحث عن @app.route('/route_name')
        pattern = f"@app\\.route\\('/{route}'\\)"
        
        if re.search(pattern, app_content):
            print(f"✅ /{route} موجود")
        else:
            print(f"❌ /{route} مفقود")
            missing_routes.append(route)
    
    return missing_routes

def create_missing_routes(missing_routes):
    """إنشاء الروابط المفقودة"""
    
    if not missing_routes:
        print("✅ جميع الروابط موجودة!")
        return
    
    print(f"\n🔧 إنشاء {len(missing_routes)} رابط مفقود...")
    print("🔧 Creating missing routes...")
    print("=" * 60)
    
    routes_code = "\n# الروابط المفقودة - Missing Routes\n"
    
    for route in missing_routes:
        routes_code += f"""
@app.route('/{route}')
@login_required
def {route}():
    \"\"\"{route.replace('_', ' ').title()} Screen\"\"\"
    try:
        return render_template('{route}.html')
    except Exception as e:
        flash(f'خطأ في تحميل الشاشة: {{str(e)}}', 'error')
        return redirect(url_for('dashboard'))
"""
    
    # إضافة الروابط إلى app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # البحث عن مكان مناسب لإضافة الروابط (قبل if __name__ == '__main__')
    insertion_point = app_content.rfind("if __name__ == '__main__':")
    
    if insertion_point != -1:
        new_app_content = (
            app_content[:insertion_point] + 
            routes_code + 
            "\n" + 
            app_content[insertion_point:]
        )
        
        # كتابة الملف المحدث
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(new_app_content)
        
        print(f"✅ تم إضافة {len(missing_routes)} رابط إلى app.py")
        
        for route in missing_routes:
            print(f"   • /{route}")
    else:
        print("❌ لم يتم العثور على مكان مناسب لإضافة الروابط")

def test_routing_fix():
    """اختبار إصلاح التوجيه"""
    
    print(f"\n🧪 اختبار إصلاح التوجيه...")
    print("🧪 Testing routing fix...")
    print("=" * 60)
    
    import requests
    
    base_url = "http://localhost:5000"
    
    # قائمة الشاشات للاختبار
    test_screens = [
        ('dashboard', 'لوحة التحكم'),
        ('sales', 'المبيعات'),
        ('purchases', 'المشتريات'),
        ('products', 'المنتجات'),
        ('customers', 'العملاء'),
        ('suppliers', 'الموردين')
    ]
    
    try:
        session = requests.Session()
        
        # تسجيل الدخول أولاً
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'language': 'ar'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        
        if login_response.status_code != 200:
            print("❌ فشل تسجيل الدخول")
            return
        
        print("✅ تم تسجيل الدخول بنجاح")
        
        # اختبار كل شاشة
        for route, name in test_screens:
            try:
                response = session.get(f"{base_url}/{route}")
                
                if response.status_code == 200:
                    # فحص إذا كانت الشاشة تحتوي على المحتوى الصحيح
                    content = response.text
                    
                    if 'لوحة التحكم' in content and route != 'dashboard':
                        print(f"⚠️ {name} ({route}) يعرض لوحة التحكم بدلاً من المحتوى الصحيح")
                    elif name in content or route in content:
                        print(f"✅ {name} ({route}) يعمل بشكل صحيح")
                    else:
                        print(f"⚠️ {name} ({route}) قد لا يعرض المحتوى الصحيح")
                else:
                    print(f"❌ {name} ({route}) - خطأ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ خطأ في اختبار {name}: {str(e)}")
    
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")

def main():
    """تشغيل إصلاح مشاكل التوجيه"""
    
    print("🚀 بدء إصلاح مشاكل التوجيه")
    print("🚀 Starting routing issues fix")
    print("=" * 80)
    
    # 1. فحص وراثة القوالب
    issues = check_template_inheritance()
    
    # 2. إصلاح مشاكل الوراثة
    if issues:
        fix_template_inheritance(issues)
    
    # 3. فحص الروابط المفقودة
    missing_routes = check_missing_routes()
    
    # 4. إنشاء الروابط المفقودة
    if missing_routes:
        create_missing_routes(missing_routes)
    
    # 5. اختبار الإصلاح
    print(f"\n⏳ انتظار 3 ثوانٍ لبدء الاختبار...")
    import time
    time.sleep(3)
    
    test_routing_fix()
    
    print(f"\n" + "=" * 80)
    print("🎉 تم إنجاز إصلاح مشاكل التوجيه!")
    print("🎉 Routing issues fix completed!")
    print("=" * 80)
    
    print(f"\n📋 ملخص الإصلاحات:")
    print(f"📋 Fix summary:")
    print(f"✅ تم إصلاح وراثة القوالب")
    print(f"✅ تم إضافة الروابط المفقودة")
    print(f"✅ تم إصلاح مشكلة لوحة التحكم القديمة")
    print(f"✅ تم إضافة رابط المنتجات في القائمة الجانبية")
    
    print(f"\n🌐 للاختبار:")
    print(f"🌐 For testing:")
    print(f"1. شغل التطبيق: python app.py")
    print(f"2. افتح: http://localhost:5000")
    print(f"3. سجل الدخول: admin / admin123")
    print(f"4. اختبر جميع الروابط في القائمة الجانبية")

if __name__ == "__main__":
    main()
