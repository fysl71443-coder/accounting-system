#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص تعارض المسارات
Diagnose Route Conflicts
"""

import re
import os
from pathlib import Path

def find_all_print_invoices_routes():
    """البحث عن جميع مسارات print_invoices"""
    print("🔍 البحث عن جميع مسارات print_invoices...")
    print("=" * 50)
    
    # قراءة app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن جميع @app.route
    route_pattern = r'@app\.route\([\'"]([^\'"]*print_invoices[^\'"]*)[\'"](?:,\s*methods=\[[^\]]+\])?\)\s*\n\s*@?\w*\s*\n\s*def\s+(\w+)\('
    
    matches = re.findall(route_pattern, content, re.MULTILINE)
    
    print("🔗 المسارات الموجودة:")
    for route, func_name in matches:
        print(f"   {route} → {func_name}()")
    
    # البحث عن دوال print_invoices
    func_pattern = r'def\s+(.*print_invoices.*)\('
    func_matches = re.findall(func_pattern, content)
    
    print("\n🔧 الدوال الموجودة:")
    for func in func_matches:
        print(f"   def {func}()")
    
    return matches, func_matches

def find_endpoint_conflicts():
    """البحث عن تعارضات endpoints"""
    print("\n🚨 البحث عن تعارضات endpoints...")
    print("=" * 50)
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن جميع أسماء الدوال
    func_pattern = r'def\s+(\w+)\('
    all_functions = re.findall(func_pattern, content)
    
    # البحث عن الدوال المكررة
    func_counts = {}
    for func in all_functions:
        func_counts[func] = func_counts.get(func, 0) + 1
    
    duplicates = {func: count for func, count in func_counts.items() if count > 1}
    
    if duplicates:
        print("❌ دوال مكررة موجودة:")
        for func, count in duplicates.items():
            print(f"   {func}: {count} مرات")
            
            # البحث عن مواقع الدوال المكررة
            pattern = rf'def\s+{func}\('
            matches = list(re.finditer(pattern, content))
            for i, match in enumerate(matches):
                line_num = content[:match.start()].count('\n') + 1
                print(f"      #{i+1}: السطر {line_num}")
    else:
        print("✅ لا توجد دوال مكررة")

def fix_route_conflict():
    """إصلاح تعارض المسارات"""
    print("\n🔧 محاولة إصلاح التعارض...")
    print("=" * 50)
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن أي دالة تحمل اسم print_invoices بدون لاحقة
    pattern = r'def\s+print_invoices\s*\('
    matches = list(re.finditer(pattern, content))
    
    if matches:
        print(f"❌ وجدت {len(matches)} دالة تحمل اسم print_invoices:")
        for i, match in enumerate(matches):
            line_num = content[:match.start()].count('\n') + 1
            print(f"   #{i+1}: السطر {line_num}")
            
            # عرض السياق
            lines = content.split('\n')
            start_line = max(0, line_num - 3)
            end_line = min(len(lines), line_num + 3)
            
            print(f"   السياق (السطور {start_line+1}-{end_line}):")
            for j in range(start_line, end_line):
                marker = ">>>" if j == line_num - 1 else "   "
                print(f"   {marker} {j+1:4d}: {lines[j]}")
            print()
    else:
        print("✅ لا توجد دالة تحمل اسم print_invoices بدون لاحقة")

def check_imports():
    """فحص الاستيرادات"""
    print("\n📦 فحص الاستيرادات...")
    print("=" * 50)
    
    # فحص جميع ملفات Python
    python_files = list(Path('.').glob('*.py'))
    
    for file_path in python_files:
        if file_path.name == 'app.py':
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن استيراد app أو print_invoices
            if 'from app import' in content or 'import app' in content:
                print(f"⚠️ {file_path.name} يستورد من app.py")
                
            if 'print_invoices' in content:
                print(f"⚠️ {file_path.name} يحتوي على print_invoices")
                
        except Exception as e:
            print(f"❌ خطأ في قراءة {file_path.name}: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🔍 تشخيص تعارض مسارات print_invoices")
    print("=" * 60)
    
    # البحث عن المسارات
    routes, functions = find_all_print_invoices_routes()
    
    # البحث عن التعارضات
    find_endpoint_conflicts()
    
    # محاولة الإصلاح
    fix_route_conflict()
    
    # فحص الاستيرادات
    check_imports()
    
    print("\n" + "=" * 60)
    print("📊 ملخص التشخيص:")
    print(f"   المسارات الموجودة: {len(routes)}")
    print(f"   الدوال الموجودة: {len(functions)}")
    
    print("\n💡 اقتراحات الحل:")
    print("1. تأكد من عدم وجود ملفات Python أخرى تستورد app")
    print("2. تأكد من عدم وجود دوال مكررة")
    print("3. أعد تشغيل الخادم بعد الإصلاح")
    print("4. استخدم أسماء دوال فريدة لكل endpoint")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
