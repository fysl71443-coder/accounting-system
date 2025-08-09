#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص شامل للنظام
Comprehensive System Diagnosis
"""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

def check_python_environment():
    """فحص بيئة Python"""
    print("🐍 فحص بيئة Python:")
    print("=" * 30)
    
    print(f"   ✅ إصدار Python: {sys.version.split()[0]}")
    
    # فحص المكتبات المطلوبة
    required_packages = [
        'flask', 'sqlalchemy', 'flask_sqlalchemy', 
        'flask_login', 'werkzeug', 'jinja2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: متوفر")
        except ImportError:
            print(f"   ❌ {package}: مفقود")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_files_structure():
    """فحص هيكل الملفات"""
    print("\n📁 فحص هيكل الملفات:")
    print("=" * 30)
    
    essential_files = [
        'app.py', 'run_local.py', 'requirements.txt',
        'templates/login.html', 'templates/dashboard.html',
        'templates/purchases.html', 'templates/simple_purchase.html',
        'static/css/unified-design.css'
    ]
    
    missing_files = []
    for file_path in essential_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}: مفقود")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_database():
    """فحص قاعدة البيانات"""
    print("\n🗃️ فحص قاعدة البيانات:")
    print("=" * 30)
    
    if not os.path.exists('accounting.db'):
        print("   ❌ قاعدة البيانات غير موجودة")
        return False
    
    try:
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        
        # فحص الجداول الأساسية
        essential_tables = [
            'users', 'branches', 'products', 'customers', 
            'purchases', 'purchase_items', 'sales', 'expenses'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        all_tables_exist = True
        for table in essential_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} سجل")
            else:
                print(f"   ❌ {table}: غير موجود")
                all_tables_exist = False
        
        conn.close()
        return all_tables_exist
        
    except Exception as e:
        print(f"   ❌ خطأ في قاعدة البيانات: {e}")
        return False

def test_app_import():
    """اختبار استيراد التطبيق"""
    print("\n🚀 اختبار استيراد التطبيق:")
    print("=" * 30)
    
    try:
        # محاولة استيراد التطبيق
        sys.path.insert(0, os.getcwd())
        from app import app
        print("   ✅ تم استيراد التطبيق بنجاح")
        
        # اختبار إنشاء context
        with app.app_context():
            print("   ✅ تم إنشاء application context")
            
            # اختبار قاعدة البيانات
            from app import db
            try:
                from sqlalchemy import text
                db.session.execute(text('SELECT 1'))
                print("   ✅ الاتصال بقاعدة البيانات يعمل")
            except Exception as e:
                print(f"   ❌ مشكلة في قاعدة البيانات: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في استيراد التطبيق: {e}")
        import traceback
        print(f"   📋 التفاصيل: {traceback.format_exc()}")
        return False

def check_routes():
    """فحص الروابط الأساسية"""
    print("\n🔗 فحص الروابط الأساسية:")
    print("=" * 30)
    
    try:
        from app import app
        
        essential_routes = [
            '/', '/login', '/dashboard', '/purchases', 
            '/purchases/simple', '/purchases/new', '/api/purchases/save'
        ]
        
        with app.app_context():
            all_routes_exist = True
            for route in essential_routes:
                try:
                    # محاولة العثور على الرابط
                    found = False
                    for rule in app.url_map.iter_rules():
                        if rule.rule == route:
                            print(f"   ✅ {route}: موجود")
                            found = True
                            break
                    
                    if not found:
                        print(f"   ❌ {route}: غير موجود")
                        all_routes_exist = False
                        
                except Exception as e:
                    print(f"   ❌ {route}: خطأ - {e}")
                    all_routes_exist = False
            
            return all_routes_exist
            
    except Exception as e:
        print(f"   ❌ خطأ في فحص الروابط: {e}")
        return False

def generate_diagnosis_report():
    """إنشاء تقرير التشخيص"""
    print("\n" + "=" * 60)
    print("📊 تقرير التشخيص الشامل")
    print("📊 Comprehensive Diagnosis Report")
    print("=" * 60)
    
    # تشغيل جميع الفحوصات
    python_ok = check_python_environment()
    files_ok = check_files_structure()
    db_ok = check_database()
    app_ok = test_app_import()
    routes_ok = check_routes()
    
    # حساب النتيجة الإجمالية
    total_checks = 5
    passed_checks = sum([python_ok, files_ok, db_ok, app_ok, routes_ok])
    score = (passed_checks / total_checks) * 100
    
    print(f"\n📈 النتيجة الإجمالية: {passed_checks}/{total_checks} ({score:.1f}%)")
    
    # التقييم
    if score >= 90:
        status = "🟢 ممتاز - النظام جاهز للاستخدام"
        recommendations = ["✅ النظام يعمل بشكل مثالي", "🚀 يمكن البدء في الاستخدام"]
    elif score >= 70:
        status = "🟡 جيد - يحتاج تحسينات طفيفة"
        recommendations = ["⚠️ إصلاح المشاكل البسيطة", "🔧 تحديث المكونات المفقودة"]
    elif score >= 50:
        status = "🟠 متوسط - يحتاج إصلاحات"
        recommendations = ["🔧 إصلاح المشاكل الأساسية", "📋 مراجعة الإعدادات"]
    else:
        status = "🔴 ضعيف - يحتاج عمل كبير"
        recommendations = ["🚨 إعادة تثبيت المتطلبات", "🗃️ إعادة إنشاء قاعدة البيانات"]
    
    print(f"🎯 الحالة: {status}")
    print(f"\n💡 التوصيات:")
    for rec in recommendations:
        print(f"   {rec}")
    
    # إضافة توصيات محددة
    if not python_ok:
        print("   📦 تثبيت المكتبات المفقودة: pip install -r requirements.txt")
    if not files_ok:
        print("   📁 التأكد من وجود جميع الملفات المطلوبة")
    if not db_ok:
        print("   🗃️ إعادة إنشاء قاعدة البيانات: python recreate_database.py")
    if not app_ok:
        print("   🚀 مراجعة أخطاء التطبيق في ملف app.py")
    if not routes_ok:
        print("   🔗 مراجعة تعريف الروابط في التطبيق")
    
    return score >= 70

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🔍 تشخيص شامل للنظام - System Comprehensive Diagnosis")
    print("=" * 60)
    
    success = generate_diagnosis_report()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ التشخيص مكتمل - النظام في حالة جيدة")
        print("✅ Diagnosis completed - System is in good condition")
    else:
        print("⚠️ التشخيص مكتمل - النظام يحتاج إصلاحات")
        print("⚠️ Diagnosis completed - System needs repairs")
    print("=" * 60)

if __name__ == "__main__":
    main()
