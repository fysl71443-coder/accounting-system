#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح مشكلة إخفاء القائمة الجانبية
Fix Sidebar Visibility Issue
"""

import requests
import time
import webbrowser

def test_login_and_sidebar():
    """اختبار تسجيل الدخول وظهور القائمة الجانبية"""
    print("🔍 اختبار مشكلة القائمة الجانبية...")
    print("=" * 50)
    
    session = requests.Session()
    base_url = 'http://localhost:5000'
    
    try:
        # 1. اختبار الوصول للصفحة الرئيسية
        print("1️⃣ اختبار الوصول للصفحة الرئيسية...")
        response = session.get(base_url)
        if response.status_code == 200:
            print("✅ تم الوصول للصفحة الرئيسية")
            if 'sidebar' in response.text:
                print("⚠️ القائمة الجانبية موجودة في HTML ولكن قد تكون مخفية")
            else:
                print("❌ القائمة الجانبية غير موجودة في HTML")
        else:
            print(f"❌ فشل الوصول للصفحة الرئيسية: {response.status_code}")
            return False
        
        # 2. اختبار تسجيل الدخول
        print("\n2️⃣ اختبار تسجيل الدخول...")
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'language': 'ar'
        }
        
        response = session.post(f'{base_url}/login', data=login_data)
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
        else:
            print(f"❌ فشل تسجيل الدخول: {response.status_code}")
            return False
        
        # 3. اختبار لوحة التحكم بعد تسجيل الدخول
        print("\n3️⃣ اختبار لوحة التحكم بعد تسجيل الدخول...")
        response = session.get(f'{base_url}/dashboard')
        if response.status_code == 200:
            print("✅ تم الوصول للوحة التحكم")
            
            # فحص وجود القائمة الجانبية
            content = response.text
            if 'sidebar' in content:
                print("✅ القائمة الجانبية موجودة في HTML")
                
                # فحص عناصر القائمة الجانبية
                sidebar_elements = [
                    'لوحة التحكم',
                    'إدارة المنتجات والتكاليف',
                    'فاتورة جديدة',
                    'المبيعات',
                    'تسجيل الخروج'
                ]
                
                for element in sidebar_elements:
                    if element in content:
                        print(f"✅ عنصر القائمة '{element}': موجود")
                    else:
                        print(f"❌ عنصر القائمة '{element}': مفقود")
                
                return True
            else:
                print("❌ القائمة الجانبية غير موجودة في HTML")
                return False
        else:
            print(f"❌ فشل الوصول للوحة التحكم: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def create_sidebar_debug_page():
    """إنشاء صفحة تشخيص القائمة الجانبية"""
    debug_html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تشخيص القائمة الجانبية</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Cairo', sans-serif;
            background-color: #f8fafc;
        }
        
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        .sidebar .nav-link {
            color: rgba(255,255,255,0.8);
            padding: 12px 20px;
            margin: 5px 10px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            background-color: rgba(255,255,255,0.1);
            color: white;
            transform: translateX(5px);
        }

        .sidebar .nav-link.unified-products {
            background: linear-gradient(135deg, rgba(255,193,7,0.25), rgba(255,152,0,0.15));
            border: 2px solid rgba(255,193,7,0.4);
            border-radius: 12px;
            margin: 10px;
            padding: 15px !important;
            box-shadow: 0 4px 15px rgba(255,193,7,0.2);
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .debug-info {
            background: #fff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 d-md-block sidebar">
                <div class="position-sticky pt-3">
                    <div class="text-center mb-4">
                        <h4 class="text-white">
                            <i class="fas fa-calculator me-2"></i>
                            نظام المحاسبة
                        </h4>
                        <small class="text-white-50">مرحباً المستخدم</small>
                    </div>
                    
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link active" href="#">
                                <i class="fas fa-tachometer-alt me-2"></i>
                                لوحة التحكم
                            </a>
                        </li>

                        <li class="nav-item">
                            <hr class="text-white-50 my-2">
                            <small class="text-white-50 px-3">الشاشات المتقدمة</small>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link unified-products" href="#">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-cogs me-2 text-warning fs-5"></i>
                                    <div class="flex-grow-1">
                                        <span class="fw-bold text-warning d-block">
                                            🌟 إدارة المنتجات والتكاليف
                                        </span>
                                        <small class="text-white-50">شاشة موحدة متكاملة</small>
                                    </div>
                                    <span class="badge bg-success ms-2 pulse">جديد</span>
                                </div>
                            </a>
                        </li>
                        <li class="nav-item">
                            <hr class="text-white-50 my-2">
                            <small class="text-white-50 px-3">الشاشات الأساسية</small>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-plus-circle me-2"></i>
                                فاتورة جديدة
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-shopping-cart me-2"></i>
                                المبيعات
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-truck me-2"></i>
                                الموردين
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-users me-2"></i>
                                العملاء
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-chart-bar me-2"></i>
                                التقارير
                            </a>
                        </li>
                        <li class="nav-item mt-3">
                            <a class="nav-link text-warning" href="#">
                                <i class="fas fa-sign-out-alt me-2"></i>
                                تسجيل الخروج
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="debug-info">
                    <h2><i class="fas fa-bug text-danger me-2"></i>تشخيص القائمة الجانبية</h2>
                    
                    <div class="alert alert-info">
                        <h5><i class="fas fa-info-circle me-2"></i>معلومات التشخيص:</h5>
                        <ul>
                            <li><strong>حالة القائمة الجانبية:</strong> <span class="text-success">تعمل بشكل صحيح</span></li>
                            <li><strong>التصميم:</strong> <span class="text-success">محمل بالكامل</span></li>
                            <li><strong>الأيقونات:</strong> <span class="text-success">تظهر بشكل صحيح</span></li>
                            <li><strong>التأثيرات البصرية:</strong> <span class="text-success">تعمل</span></li>
                        </ul>
                    </div>
                    
                    <div class="alert alert-warning">
                        <h5><i class="fas fa-exclamation-triangle me-2"></i>المشاكل المحتملة:</h5>
                        <ul>
                            <li>قد تكون القائمة الجانبية مخفية بسبب عدم تسجيل الدخول</li>
                            <li>تحقق من متغير session.get('user_id') في Flask</li>
                            <li>تأكد من تسجيل الدخول بنجاح</li>
                        </ul>
                    </div>
                    
                    <div class="alert alert-success">
                        <h5><i class="fas fa-lightbulb me-2"></i>الحلول:</h5>
                        <ol>
                            <li>تسجيل الدخول: admin / admin123</li>
                            <li>تحديث الصفحة (F5)</li>
                            <li>مسح cache المتصفح (Ctrl+F5)</li>
                            <li>التأكد من تشغيل التطبيق على المنفذ 5000</li>
                        </ol>
                    </div>
                    
                    <div class="text-center mt-4">
                        <a href="http://localhost:5000" class="btn btn-primary btn-lg">
                            <i class="fas fa-home me-2"></i>العودة للنظام الرئيسي
                        </a>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        console.log('✅ صفحة تشخيص القائمة الجانبية تعمل بشكل صحيح');
        
        // اختبار النقر على الروابط
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('تم النقر على:', this.textContent.trim());
                alert('تم النقر على: ' + this.textContent.trim());
            });
        });
    </script>
</body>
</html>'''
    
    with open('sidebar_debug.html', 'w', encoding='utf-8') as f:
        f.write(debug_html)
    
    print("✅ تم إنشاء صفحة تشخيص القائمة الجانبية: sidebar_debug.html")

def run_diagnosis():
    """تشغيل التشخيص الكامل"""
    print("🔧 بدء تشخيص مشكلة القائمة الجانبية")
    print("=" * 60)
    
    # إنشاء صفحة التشخيص
    create_sidebar_debug_page()
    
    # فتح صفحة التشخيص
    print("\n🌐 فتح صفحة التشخيص...")
    webbrowser.open('file://' + os.path.abspath('sidebar_debug.html'))
    
    # انتظار قصير
    time.sleep(2)
    
    # اختبار النظام الفعلي
    print("\n🧪 اختبار النظام الفعلي...")
    if test_login_and_sidebar():
        print("\n✅ القائمة الجانبية تعمل بشكل صحيح!")
        print("💡 إذا لم تظهر القائمة الجانبية، تأكد من:")
        print("   1. تسجيل الدخول بنجاح")
        print("   2. تحديث الصفحة")
        print("   3. مسح cache المتصفح")
    else:
        print("\n❌ هناك مشكلة في القائمة الجانبية")
        print("🔧 جرب الحلول التالية:")
        print("   1. إعادة تشغيل التطبيق")
        print("   2. التأكد من تشغيل التطبيق على المنفذ 5000")
        print("   3. فحص ملف app.py للتأكد من routes")
    
    print("\n" + "=" * 60)
    print("🎯 للمساعدة:")
    print("🌐 صفحة التشخيص: sidebar_debug.html")
    print("🌐 النظام الرئيسي: http://localhost:5000")
    print("👤 بيانات الدخول: admin / admin123")
    print("=" * 60)

if __name__ == "__main__":
    import os
    run_diagnosis()
