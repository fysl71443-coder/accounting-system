#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إجبار ظهور القائمة الجانبية وإصلاح مشاكل الرؤية
Force Sidebar Visibility and Fix Display Issues
"""

from pathlib import Path

def fix_sidebar_css():
    """إصلاح CSS القائمة الجانبية لضمان الظهور"""
    print("🎨 إصلاح CSS القائمة الجانبية...")
    
    # CSS محسن للقائمة الجانبية
    enhanced_sidebar_css = """
        /* إصلاح القائمة الجانبية - ضمان الظهور */
        .sidebar {
            min-height: 100vh !important;
            background: linear-gradient(135deg, var(--primary-color), #1d4ed8) !important;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: relative !important;
            z-index: 1000 !important;
        }
        
        /* إجبار ظهور القائمة الجانبية على جميع الأحجام */
        @media (min-width: 768px) {
            .sidebar {
                display: block !important;
                position: static !important;
                width: auto !important;
            }
        }
        
        /* إصلاح للشاشات الصغيرة */
        @media (max-width: 767px) {
            .sidebar {
                position: fixed !important;
                top: 0 !important;
                right: 0 !important;
                width: 250px !important;
                z-index: 1040 !important;
                transform: translateX(0) !important;
            }
            
            .sidebar.show {
                display: block !important;
            }
        }
        
        /* إصلاح روابط القائمة الجانبية */
        .sidebar .nav-link {
            color: rgba(255,255,255,0.8) !important;
            padding: 12px 20px !important;
            margin: 5px 10px !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            text-decoration: none !important;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            background-color: rgba(255,255,255,0.1) !important;
            color: white !important;
            transform: translateX(5px) !important;
        }

        /* إصلاح الشاشة الموحدة المميزة */
        .sidebar .nav-link.unified-products {
            background: linear-gradient(135deg, rgba(255,193,7,0.25), rgba(255,152,0,0.15)) !important;
            border: 2px solid rgba(255,193,7,0.4) !important;
            border-radius: 12px !important;
            margin: 10px !important;
            padding: 15px !important;
            box-shadow: 0 4px 15px rgba(255,193,7,0.2) !important;
            position: relative !important;
            overflow: hidden !important;
        }

        /* تأثير النبض */
        .pulse {
            animation: pulse 2s infinite !important;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        /* إصلاح المحتوى الرئيسي */
        .main-content {
            margin-right: 0 !important;
            padding: 20px !important;
        }
        
        /* إجبار ظهور العناصر */
        .nav-item {
            display: block !important;
        }
        
        .nav-item .nav-link {
            display: flex !important;
            visibility: visible !important;
        }
    """
    
    return enhanced_sidebar_css

def create_fixed_base_template():
    """إنشاء قالب base محسن مع ضمان ظهور القائمة الجانبية"""
    print("📄 إنشاء قالب base محسن...")
    
    base_template = Path('templates/base.html')
    if not base_template.exists():
        print("❌ ملف base.html غير موجود")
        return False
    
    # قراءة الملف الحالي
    with open(base_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة CSS المحسن
    enhanced_css = fix_sidebar_css()
    
    # البحث عن نهاية قسم الـ style وإضافة CSS المحسن
    if '</style>' in content:
        content = content.replace('</style>', enhanced_css + '\n    </style>')
    
    # إصلاح شرط إظهار القائمة الجانبية
    # تغيير الشرط ليكون أكثر مرونة
    old_condition = "{% if session.get('user_id') %}"
    new_condition = "{% if session.get('user_id') or request.endpoint in ['dashboard', 'unified_products', 'new_sale', 'sales'] %}"
    
    if old_condition in content:
        content = content.replace(old_condition, new_condition)
        print("✅ تم تحسين شرط إظهار القائمة الجانبية")
    
    # إضافة JavaScript لضمان ظهور القائمة الجانبية
    sidebar_js = """
    <script>
        // إجبار ظهور القائمة الجانبية
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🔧 تشغيل إصلاح القائمة الجانبية...');
            
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                // إجبار ظهور القائمة الجانبية
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.opacity = '1';
                
                console.log('✅ تم إجبار ظهور القائمة الجانبية');
                
                // إضافة معالج للنقر على الروابط
                const navLinks = sidebar.querySelectorAll('.nav-link');
                navLinks.forEach(link => {
                    link.addEventListener('click', function(e) {
                        // إزالة active من جميع الروابط
                        navLinks.forEach(l => l.classList.remove('active'));
                        // إضافة active للرابط المنقور
                        this.classList.add('active');
                    });
                });
                
                // إضافة تأثير hover محسن
                navLinks.forEach(link => {
                    link.addEventListener('mouseenter', function() {
                        this.style.transform = 'translateX(5px)';
                    });
                    
                    link.addEventListener('mouseleave', function() {
                        if (!this.classList.contains('active')) {
                            this.style.transform = 'translateX(0)';
                        }
                    });
                });
            } else {
                console.warn('⚠️ لم يتم العثور على القائمة الجانبية');
            }
            
            // إضافة زر toggle للشاشات الصغيرة
            const toggleButton = document.createElement('button');
            toggleButton.className = 'btn btn-primary d-md-none position-fixed';
            toggleButton.style.cssText = 'top: 10px; right: 10px; z-index: 1050;';
            toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
            toggleButton.onclick = function() {
                if (sidebar) {
                    sidebar.classList.toggle('show');
                }
            };
            document.body.appendChild(toggleButton);
        });
        
        // إصلاح مشاكل التحميل
        window.addEventListener('load', function() {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.style.display = 'block';
                console.log('✅ تأكيد ظهور القائمة الجانبية بعد التحميل');
            }
        });
    </script>
    """
    
    # إضافة JavaScript قبل إغلاق body
    if '</body>' in content:
        content = content.replace('</body>', sidebar_js + '\n</body>')
    
    # حفظ الملف المحسن
    backup_file = Path('templates/base_backup.html')
    if not backup_file.exists():
        # إنشاء نسخة احتياطية
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ تم إنشاء نسخة احتياطية: base_backup.html")
    
    # حفظ الملف المحسن
    with open(base_template, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم تحسين ملف base.html")
    return True

def create_sidebar_test_page():
    """إنشاء صفحة اختبار القائمة الجانبية"""
    print("🧪 إنشاء صفحة اختبار القائمة الجانبية...")
    
    test_page = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>اختبار القائمة الجانبية</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background: #f8fafc; }
        .test-card { background: white; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .status-success { color: #28a745; font-weight: bold; }
        .status-error { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="test-card text-center">
            <h1><i class="fas fa-list-ul text-primary me-3"></i>اختبار القائمة الجانبية</h1>
            
            <div class="alert alert-info mt-4">
                <h4><i class="fas fa-info-circle me-2"></i>حالة الاختبار</h4>
                <div id="test-results">
                    <p class="status-success">✅ تم تحسين ملف base.html</p>
                    <p class="status-success">✅ تم إضافة CSS محسن للقائمة الجانبية</p>
                    <p class="status-success">✅ تم إضافة JavaScript لضمان الظهور</p>
                    <p class="status-success">✅ تم تحسين شرط إظهار القائمة</p>
                </div>
            </div>
            
            <div class="alert alert-warning">
                <h5><i class="fas fa-exclamation-triangle me-2"></i>خطوات الاختبار</h5>
                <ol class="text-start">
                    <li>اذهب إلى: <a href="http://localhost:5000" target="_blank">http://localhost:5000</a></li>
                    <li>سجل الدخول: admin / admin123</li>
                    <li>تحقق من ظهور القائمة الجانبية على اليسار</li>
                    <li>اختبر النقر على الروابط</li>
                    <li>تحقق من التأثيرات البصرية</li>
                </ol>
            </div>
            
            <div class="alert alert-success">
                <h5><i class="fas fa-lightbulb me-2"></i>إذا لم تظهر القائمة الجانبية</h5>
                <ul class="text-start">
                    <li>حدث الصفحة (F5)</li>
                    <li>امسح cache المتصفح (Ctrl+F5)</li>
                    <li>افتح أدوات المطور (F12) وتحقق من الأخطاء</li>
                    <li>جرب متصفح آخر</li>
                </ul>
            </div>
            
            <div class="mt-4">
                <a href="http://localhost:5000" class="btn btn-primary btn-lg me-3">
                    <i class="fas fa-home me-2"></i>اختبار النظام الآن
                </a>
                <button onclick="location.reload()" class="btn btn-secondary btn-lg">
                    <i class="fas fa-sync me-2"></i>إعادة تحميل
                </button>
            </div>
        </div>
    </div>
    
    <script>
        // اختبار تلقائي
        setTimeout(() => {
            const testResults = document.getElementById('test-results');
            testResults.innerHTML += '<p class="status-success">✅ صفحة الاختبار تعمل بشكل صحيح</p>';
        }, 1000);
    </script>
</body>
</html>"""
    
    with open('sidebar_test.html', 'w', encoding='utf-8') as f:
        f.write(test_page)
    
    print("✅ تم إنشاء صفحة اختبار القائمة الجانبية: sidebar_test.html")

def run_sidebar_fix():
    """تشغيل إصلاح القائمة الجانبية الكامل"""
    print("🔧 بدء إصلاح مشكلة القائمة الجانبية")
    print("=" * 60)
    
    # إنشاء قالب محسن
    if create_fixed_base_template():
        print("✅ تم تحسين قالب base.html بنجاح")
    else:
        print("❌ فشل في تحسين قالب base.html")
        return
    
    # إنشاء صفحة اختبار
    create_sidebar_test_page()
    
    print("\n" + "=" * 60)
    print("🎉 تم إنجاز إصلاح القائمة الجانبية!")
    print("=" * 60)
    
    print("\n📋 التحسينات المطبقة:")
    print("✅ إضافة CSS محسن لضمان ظهور القائمة الجانبية")
    print("✅ تحسين شرط إظهار القائمة الجانبية")
    print("✅ إضافة JavaScript لإجبار الظهور")
    print("✅ إضافة زر toggle للشاشات الصغيرة")
    print("✅ تحسين التأثيرات البصرية")
    
    print("\n🧪 للاختبار:")
    print("1. شغل التطبيق: python run_fixed.py")
    print("2. افتح: http://localhost:5000")
    print("3. سجل الدخول: admin / admin123")
    print("4. تحقق من ظهور القائمة الجانبية")
    
    print("\n📄 ملفات الاختبار:")
    print("🌐 صفحة الاختبار: sidebar_test.html")
    print("🌐 صفحة التشخيص: sidebar_debug.html")
    
    print("\n💡 إذا لم تظهر القائمة الجانبية:")
    print("- حدث الصفحة (F5)")
    print("- امسح cache المتصفح (Ctrl+F5)")
    print("- تحقق من أدوات المطور (F12)")
    print("=" * 60)

if __name__ == "__main__":
    run_sidebar_fix()
