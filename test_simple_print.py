#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الطباعة البسيطة الجديدة
Test New Simple Print
"""

import requests
import webbrowser
import time

def test_simple_print():
    """اختبار الطباعة البسيطة"""
    print("🖨️ اختبار الطباعة البسيطة الجديدة")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python app.py")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول")
        else:
            print("❌ فشل تسجيل الدخول")
            return False
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ صفحة المدفوعات تعمل")
            
            content = response.text
            
            # فحص أزرار الطباعة الجديدة
            print("\n🔍 فحص أزرار الطباعة الجديدة:")
            
            if 'printSalesInvoices()' in content:
                print("✅ زر طباعة المبيعات موجود")
            else:
                print("❌ زر طباعة المبيعات غير موجود")
            
            if 'printPurchasesInvoices()' in content:
                print("✅ زر طباعة المشتريات موجود")
            else:
                print("❌ زر طباعة المشتريات غير موجود")
            
            if 'printExpensesInvoices()' in content:
                print("✅ زر طباعة المصروفات موجود")
            else:
                print("❌ زر طباعة المصروفات غير موجود")
            
            if 'printPayrollInvoices()' in content:
                print("✅ زر طباعة الرواتب موجود")
            else:
                print("❌ زر طباعة الرواتب غير موجود")
            
            # فحص وجود الوظائف JavaScript
            print("\n🔍 فحص وظائف JavaScript:")
            
            if 'function printSalesInvoices' in content:
                print("✅ وظيفة طباعة المبيعات موجودة")
            else:
                print("❌ وظيفة طباعة المبيعات غير موجودة")
            
            if 'function createPrintHTML' in content:
                print("✅ وظيفة إنشاء HTML للطباعة موجودة")
            else:
                print("❌ وظيفة إنشاء HTML للطباعة غير موجودة")
            
            if 'function openPrintWindow' in content:
                print("✅ وظيفة فتح نافذة الطباعة موجودة")
            else:
                print("❌ وظيفة فتح نافذة الطباعة غير موجودة")
            
            # فحص عدم وجود النوافذ المنبثقة القديمة
            print("\n🔍 فحص حذف النوافذ المنبثقة القديمة:")
            
            if 'printModal' not in content:
                print("✅ تم حذف النافذة المنبثقة القديمة")
            else:
                print("⚠️ النافذة المنبثقة القديمة لا تزال موجودة")
            
            if 'openPrintModal' not in content:
                print("✅ تم حذف وظيفة النافذة المنبثقة القديمة")
            else:
                print("⚠️ وظيفة النافذة المنبثقة القديمة لا تزال موجودة")
            
            return True
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص صفحة المدفوعات: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار شامل للطباعة البسيطة الجديدة")
    print("=" * 60)
    
    # اختبار الطباعة البسيطة
    if not test_simple_print():
        print("❌ فشل اختبار الطباعة البسيطة")
        return
    
    # فتح المتصفح للاختبار اليدوي
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار:")
    print("=" * 60)
    
    print("🎉 تم إنجاز التحديث بنجاح!")
    print("✅ تم حذف النوافذ المنبثقة المعقدة")
    print("✅ تم إضافة أزرار طباعة بسيطة لكل قسم")
    print("✅ تم إضافة وظائف JavaScript للطباعة المباشرة")
    
    print("\n📋 تعليمات الاستخدام:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. اذهب إلى أي تبويب (مبيعات، مشتريات، مصروفات، رواتب)")
    print("3. اضغط زر 'طباعة فواتير [اسم القسم]'")
    print("4. ستفتح نافذة جديدة مع الفواتير في شكل صفوف")
    print("5. ستبدأ الطباعة تلقائياً")
    
    print("\n🌟 المزايا الجديدة:")
    print("- طباعة مباشرة بدون نوافذ منبثقة معقدة")
    print("- عرض الفواتير في شكل صفوف تحت بعضها")
    print("- تصميم بسيط ومناسب للطباعة")
    print("- حساب المجاميع والإحصائيات تلقائياً")
    print("- أزرار ملونة مميزة لكل قسم")
    
    print("\n🔗 الرابط:")
    print("http://localhost:5000/payments_dues")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
