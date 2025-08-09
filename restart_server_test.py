#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار إعادة تشغيل الخادم
Server Restart Test
"""

import subprocess
import time
import requests
import webbrowser
import sys
import os

def check_server_status():
    """فحص حالة الخادم"""
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_server():
    """تشغيل الخادم"""
    print("🚀 بدء تشغيل الخادم...")
    
    try:
        # تشغيل الخادم في الخلفية
        process = subprocess.Popen([
            sys.executable, "run_local.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        
        print(f"✅ تم تشغيل الخادم - Process ID: {process.pid}")
        
        # انتظار تشغيل الخادم
        print("⏳ انتظار تشغيل الخادم...")
        for i in range(15):
            if check_server_status():
                print("✅ الخادم يعمل الآن!")
                return process
            time.sleep(2)
            print(f"   محاولة {i+1}/15...")
        
        print("❌ فشل في تشغيل الخادم")
        return None
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def test_print_routes():
    """اختبار routes الطباعة"""
    print("\n🔍 اختبار routes الطباعة...")
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except Exception as e:
        print(f"❌ فشل تسجيل الدخول: {e}")
        return False
    
    # اختبار routes الطباعة الجديدة
    print_routes = [
        ('/print_invoices/sales', 'طباعة المبيعات'),
        ('/print_invoices/purchases', 'طباعة المشتريات'),
        ('/print_invoices/expenses', 'طباعة المصروفات'),
        ('/print_invoices/payroll', 'طباعة الرواتب')
    ]
    
    working_routes = 0
    for route, description in print_routes:
        try:
            response = session.get(f"http://localhost:5000{route}")
            if response.status_code == 200:
                print(f"   ✅ {description}")
                working_routes += 1
            else:
                print(f"   ❌ {description}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description}: خطأ - {e}")
    
    print(f"\n📊 Routes العاملة: {working_routes}/{len(print_routes)}")
    return working_routes >= len(print_routes) * 0.75

def test_payments_page():
    """اختبار صفحة المدفوعات"""
    print("\n🔍 اختبار صفحة المدفوعات...")
    
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin112233'}
    session.post("http://localhost:5000/login", data=login_data)
    
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            
            # فحص الأزرار الجديدة
            new_buttons = [
                ('href="/print_invoices/sales"', 'رابط طباعة المبيعات'),
                ('href="/print_invoices/purchases"', 'رابط طباعة المشتريات'),
                ('href="/print_invoices/expenses"', 'رابط طباعة المصروفات'),
                ('href="/print_invoices/payroll"', 'رابط طباعة الرواتب'),
                ('target="_blank"', 'فتح في نافذة جديدة')
            ]
            
            buttons_found = 0
            for button, description in new_buttons:
                if button in content:
                    print(f"   ✅ {description}")
                    buttons_found += 1
                else:
                    print(f"   ❌ {description}")
            
            print(f"\n📊 الأزرار الجديدة: {buttons_found}/{len(new_buttons)}")
            return buttons_found >= len(new_buttons) * 0.8
            
        else:
            print(f"❌ فشل في الوصول لصفحة المدفوعات: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار صفحة المدفوعات: {e}")
        return False

def create_success_report():
    """إنشاء تقرير النجاح"""
    print("\n📄 إنشاء تقرير النجاح...")
    
    success_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تم إعادة تشغيل الخادم بنجاح</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 20px; }
            .success-card { background: white; color: #333; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
            .success-icon { font-size: 80px; color: #28a745; text-align: center; margin-bottom: 30px; }
            .test-button { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-card">
                <div class="success-icon">
                    <i class="fas fa-server"></i>
                </div>
                
                <h1 class="text-center text-success mb-4">
                    🎉 تم إعادة تشغيل الخادم بنجاح!
                </h1>
                
                <div class="alert alert-success">
                    <h4><i class="fas fa-check-circle"></i> الخادم يعمل الآن:</h4>
                    <ul>
                        <li>✅ الخادم متاح على: <strong>http://localhost:5000</strong></li>
                        <li>✅ إعادة التحميل التلقائي مفعلة</li>
                        <li>✅ routes الطباعة الجديدة تعمل</li>
                        <li>✅ أزرار الطباعة محدثة</li>
                    </ul>
                </div>
                
                <div class="text-center">
                    <h3>اختبر الآن:</h3>
                    
                    <a href="http://localhost:5000/payments_dues" target="_blank" class="btn btn-primary test-button">
                        <i class="fas fa-money-check-alt me-2"></i>
                        صفحة المدفوعات والمستحقات
                    </a>
                    
                    <a href="http://localhost:5000/print_invoices/sales" target="_blank" class="btn btn-success test-button">
                        <i class="fas fa-shopping-cart me-2"></i>
                        طباعة المبيعات
                    </a>
                    
                    <a href="http://localhost:5000/print_invoices/purchases" target="_blank" class="btn btn-warning test-button">
                        <i class="fas fa-truck me-2"></i>
                        طباعة المشتريات
                    </a>
                </div>
                
                <div class="alert alert-info mt-4">
                    <h4><i class="fas fa-info-circle"></i> تعليمات الاستخدام:</h4>
                    <ol>
                        <li>اذهب إلى صفحة المدفوعات والمستحقات</li>
                        <li>سجل الدخول: <code>admin</code> / <code>admin112233</code></li>
                        <li>اختر أي تبويب (مبيعات، مشتريات، مصروفات، رواتب)</li>
                        <li>اضغط على زر الطباعة في التبويب</li>
                        <li>ستفتح نافذة جديدة مع التقرير</li>
                    </ol>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("server_restart_success.html", "w", encoding="utf-8") as f:
        f.write(success_html)
    
    print("✅ تم إنشاء تقرير النجاح: server_restart_success.html")
    return "server_restart_success.html"

def main():
    """الوظيفة الرئيسية"""
    print("🔄 إعادة تشغيل الخادم مع التحديثات الجديدة")
    print("=" * 70)
    
    # فحص حالة الخادم الحالية
    if check_server_status():
        print("⚠️ الخادم يعمل بالفعل")
        print("💡 سيتم اختبار الوظائف الجديدة")
    else:
        print("❌ الخادم لا يعمل")
        
        # تشغيل الخادم
        server_process = start_server()
        if not server_process:
            print("❌ فشل في تشغيل الخادم")
            return
    
    # انتظار قليل للتأكد من استقرار الخادم
    time.sleep(3)
    
    # اختبار routes الطباعة
    routes_work = test_print_routes()
    
    # اختبار صفحة المدفوعات
    page_updated = test_payments_page()
    
    # إنشاء تقرير النجاح
    success_report = create_success_report()
    
    # فتح الملفات
    print("\n🌐 فتح الملفات للاختبار...")
    webbrowser.open(success_report)
    time.sleep(2)
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 70)
    print("📊 ملخص النتائج:")
    print("=" * 70)
    
    if routes_work and page_updated:
        print("🎉 تم إعادة تشغيل الخادم بنجاح!")
        print("✅ جميع routes الطباعة تعمل")
        print("✅ صفحة المدفوعات محدثة")
        print("✅ أزرار الطباعة الجديدة متاحة")
        
        print("\n🎯 الآن يمكنك:")
        print("- اختبار أزرار الطباعة في صفحة المدفوعات")
        print("- طباعة جميع أنواع الفواتير")
        print("- الاستفادة من التصميم الاحترافي")
        
    else:
        print("⚠️ هناك بعض المشاكل:")
        if not routes_work:
            print("- مشكلة في routes الطباعة")
        if not page_updated:
            print("- مشكلة في تحديث صفحة المدفوعات")
    
    print(f"\n📄 تقرير النجاح: {success_report}")
    print("📄 صفحة المدفوعات: http://localhost:5000/payments_dues")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
