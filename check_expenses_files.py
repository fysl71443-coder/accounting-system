#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص ملفات شاشة المصروفات
Check Expenses Screen Files
"""

import os
import sys
from pathlib import Path

def check_expenses_files():
    """فحص وجود ملفات شاشة المصروفات"""
    print("📁 فحص ملفات شاشة المصروفات:")
    print("=" * 50)
    
    # الملفات المطلوبة
    required_files = [
        ('templates/expenses.html', 'قالب شاشة المصروفات'),
        ('templates/new_expense.html', 'قالب إضافة مصروف جديد'),
        ('static/css/unified-design.css', 'ملف التصميم'),
        ('static/js/expenses.js', 'ملف JavaScript للمصروفات')
    ]
    
    existing_files = 0
    missing_files = []
    
    for file_path, description in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {description}: {file_path}")
            existing_files += 1
        else:
            print(f"   ❌ {description}: {file_path} - مفقود")
            missing_files.append((file_path, description))
    
    print(f"\n📊 النتيجة: {existing_files}/{len(required_files)} ملف موجود")
    
    return existing_files, missing_files

def check_expenses_routes():
    """فحص routes المصروفات في app.py"""
    print("\n🔗 فحص routes المصروفات في app.py:")
    print("=" * 50)
    
    if not Path('app.py').exists():
        print("❌ ملف app.py غير موجود")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Routes المطلوبة
    required_routes = [
        ('@app.route(\'/expenses\')', 'شاشة المصروفات الرئيسية'),
        ('@app.route(\'/expenses/new\')', 'صفحة إضافة مصروف جديد'),
        ('@app.route(\'/api/expenses/save\')', 'API حفظ المصروف'),
        ('@app.route(\'/api/expenses/list\')', 'API جلب قائمة المصروفات'),
        ('def expenses()', 'وظيفة شاشة المصروفات'),
        ('class Expense(', 'نموذج المصروف')
    ]
    
    found_routes = 0
    missing_routes = []
    
    for route_pattern, description in required_routes:
        if route_pattern in content:
            print(f"   ✅ {description}: موجود")
            found_routes += 1
        else:
            print(f"   ❌ {description}: مفقود")
            missing_routes.append((route_pattern, description))
    
    print(f"\n📊 النتيجة: {found_routes}/{len(required_routes)} route موجود")
    
    return found_routes, missing_routes

def check_expenses_database():
    """فحص جدول المصروفات في قاعدة البيانات"""
    print("\n🗃️ فحص جدول المصروفات:")
    print("=" * 50)
    
    if not Path('accounting.db').exists():
        print("❌ قاعدة البيانات غير موجودة")
        return False
    
    try:
        import sqlite3
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        # فحص وجود جدول expenses
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
        if cursor.fetchone():
            print("   ✅ جدول expenses موجود")
            
            # فحص هيكل الجدول
            cursor.execute("PRAGMA table_info(expenses)")
            columns = cursor.fetchall()
            
            print("   📋 أعمدة الجدول:")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                print(f"      - {col_name}: {col_type}")
            
            # فحص عدد السجلات
            cursor.execute("SELECT COUNT(*) FROM expenses")
            count = cursor.fetchone()[0]
            print(f"   📊 عدد المصروفات: {count}")
            
        else:
            print("   ❌ جدول expenses غير موجود")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في فحص قاعدة البيانات: {e}")
        return False

def analyze_expenses_template():
    """تحليل قالب المصروفات"""
    print("\n🎨 تحليل قالب المصروفات:")
    print("=" * 50)
    
    template_path = Path('templates/expenses.html')
    if not template_path.exists():
        print("❌ قالب expenses.html غير موجود")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # العناصر المطلوبة في القالب
    required_elements = [
        ('table', 'جدول المصروفات'),
        ('btn-success', 'زر إضافة جديد'),
        ('btn-primary', 'زر البحث'),
        ('modal', 'نافذة منبثقة'),
        ('form', 'نموذج'),
        ('expenses-table', 'معرف جدول المصروفات'),
        ('loadExpensesData', 'وظيفة تحميل البيانات'),
        ('saveExpense', 'وظيفة حفظ المصروف')
    ]
    
    found_elements = 0
    for element, description in required_elements:
        if element in content:
            print(f"   ✅ {description}: موجود")
            found_elements += 1
        else:
            print(f"   ❌ {description}: مفقود")
    
    print(f"\n📊 النتيجة: {found_elements}/{len(required_elements)} عنصر موجود")
    
    return found_elements >= len(required_elements) * 0.7

def generate_expenses_fix_recommendations():
    """إنشاء توصيات لإصلاح المشاكل"""
    print("\n💡 توصيات الإصلاح:")
    print("=" * 50)
    
    recommendations = [
        "🔧 إنشاء API endpoints المفقودة:",
        "   - /api/expenses/list لجلب قائمة المصروفات",
        "   - /api/expenses/categories لجلب فئات المصروفات",
        "   - /expenses/new لصفحة إضافة مصروف جديد",
        "",
        "📄 إنشاء القوالب المفقودة:",
        "   - templates/new_expense.html لإضافة مصروف جديد",
        "",
        "🔄 إصلاح مشاكل API:",
        "   - إصلاح Content-Type في API حفظ المصروف",
        "   - إضافة معالجة JSON في الطلبات",
        "",
        "🎨 تحسين الواجهة:",
        "   - إضافة زر التصدير",
        "   - ربط الأزرار بالوظائف الصحيحة",
        "",
        "🗃️ فحص قاعدة البيانات:",
        "   - التأكد من وجود جدول expenses",
        "   - إضافة البيانات التجريبية إذا لزم الأمر"
    ]
    
    for recommendation in recommendations:
        print(recommendation)

def main():
    """الوظيفة الرئيسية"""
    print("=" * 80)
    print("🔍 فحص ملفات ومكونات شاشة المصروفات")
    print("🔍 Check Expenses Screen Files and Components")
    print("=" * 80)
    
    # فحص الملفات
    existing_files, missing_files = check_expenses_files()
    
    # فحص Routes
    found_routes, missing_routes = check_expenses_routes()
    
    # فحص قاعدة البيانات
    db_status = check_expenses_database()
    
    # تحليل القالب
    template_status = analyze_expenses_template()
    
    # النتيجة الإجمالية
    print("\n" + "=" * 80)
    print("📊 النتيجة الإجمالية:")
    print("=" * 80)
    
    total_score = 0
    max_score = 4
    
    if existing_files >= 2:
        total_score += 1
        print("✅ الملفات: مقبول")
    else:
        print("❌ الملفات: يحتاج عمل")
    
    if found_routes >= 3:
        total_score += 1
        print("✅ Routes: مقبول")
    else:
        print("❌ Routes: يحتاج عمل")
    
    if db_status:
        total_score += 1
        print("✅ قاعدة البيانات: تعمل")
    else:
        print("❌ قاعدة البيانات: مشكلة")
    
    if template_status:
        total_score += 1
        print("✅ القالب: مقبول")
    else:
        print("❌ القالب: يحتاج تحسين")
    
    success_rate = (total_score / max_score) * 100
    print(f"\n🎯 معدل النجاح: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🟢 شاشة المصروفات في حالة جيدة")
    elif success_rate >= 50:
        print("🟡 شاشة المصروفات تحتاج تحسينات")
    else:
        print("🔴 شاشة المصروفات تحتاج عمل كبير")
    
    # التوصيات
    generate_expenses_fix_recommendations()
    
    print("\n" + "=" * 80)
    print("✅ انتهى فحص ملفات شاشة المصروفات")
    print("✅ Expenses screen files check completed")
    print("=" * 80)

if __name__ == "__main__":
    main()
