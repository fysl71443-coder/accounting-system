#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل للنظام
Comprehensive System Test
"""

import requests
import json

def test_system():
    """اختبار شامل للنظام"""
    
    print("🧪 اختبار شامل لنظام المحاسبة")
    print("=" * 50)

    # إنشاء جلسة
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'language': 'ar'
    }

    try:
        # 1. اختبار تسجيل الدخول
        print("1️⃣ اختبار تسجيل الدخول...")
        response = session.post('http://localhost:5000/login', data=login_data)
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
        else:
            print(f"❌ فشل تسجيل الدخول: {response.status_code}")
            return

        # 2. اختبار الصفحة الرئيسية
        print("\n2️⃣ اختبار الصفحة الرئيسية...")
        response = session.get('http://localhost:5000/dashboard')
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية تعمل")
            
            content = response.text
            # فحص العناصر المهمة
            checks = [
                ('sidebar', 'القائمة الجانبية'),
                ('إدارة المنتجات والتكاليف', 'الشاشة الموحدة'),
                ('bootstrap', 'Bootstrap CSS'),
                ('nav-link', 'روابط التنقل'),
                ('fas fa-', 'أيقونات FontAwesome')
            ]
            
            for check, desc in checks:
                if check in content:
                    print(f"✅ {desc}: موجود")
                else:
                    print(f"❌ {desc}: غير موجود")
        else:
            print(f"❌ خطأ في الصفحة الرئيسية: {response.status_code}")

        # 3. اختبار الشاشة الموحدة
        print("\n3️⃣ اختبار الشاشة الموحدة...")
        response = session.get('http://localhost:5000/unified_products')
        if response.status_code == 200:
            print("✅ الشاشة الموحدة تعمل")
            
            content = response.text
            unified_checks = [
                ('المواد الخام', 'تبويب المواد الخام'),
                ('حساب التكاليف', 'تبويب حساب التكاليف'),
                ('المنتجات الجاهزة', 'تبويب المنتجات الجاهزة'),
                ('nav-pills', 'التبويبات'),
                ('tab-content', 'محتوى التبويبات')
            ]
            
            for check, desc in unified_checks:
                if check in content:
                    print(f"✅ {desc}: موجود")
                else:
                    print(f"❌ {desc}: غير موجود")
        else:
            print(f"❌ خطأ في الشاشة الموحدة: {response.status_code}")

        # 4. اختبار APIs
        print("\n4️⃣ اختبار APIs...")
        
        # API المواد الخام
        response = session.get('http://localhost:5000/api/raw_materials')
        if response.status_code == 200:
            materials = response.json()
            print(f"✅ API المواد الخام: {len(materials)} مادة")
        else:
            print(f"❌ API المواد الخام: خطأ {response.status_code}")

        # API المنتجات
        response = session.get('http://localhost:5000/api/products')
        if response.status_code == 200:
            products = response.json()
            print(f"✅ API المنتجات: {len(products)} منتج")
        else:
            print(f"❌ API المنتجات: خطأ {response.status_code}")

        # 5. اختبار إضافة مادة خام
        print("\n5️⃣ اختبار إضافة مادة خام...")
        test_material = {
            'name': 'مادة اختبار',
            'unit': 'كيلو',
            'price': 10.50,
            'stock': 20.0,
            'min_stock': 5.0,
            'supplier': 'مورد اختبار'
        }
        
        response = session.post('http://localhost:5000/api/raw_materials',
                               json=test_material,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ إضافة مادة خام: نجح")
            else:
                print(f"⚠️ إضافة مادة خام: {result.get('message', 'موجود مسبقاً')}")
        else:
            print(f"❌ إضافة مادة خام: خطأ {response.status_code}")

        # 6. اختبار الروابط المهمة
        print("\n6️⃣ اختبار الروابط المهمة...")
        important_routes = [
            ('/new_sale', 'فاتورة جديدة'),
            ('/sales', 'المبيعات'),
            ('/logout', 'تسجيل الخروج')
        ]
        
        for route, desc in important_routes:
            response = session.get(f'http://localhost:5000{route}')
            if response.status_code == 200:
                print(f"✅ {desc}: يعمل")
            elif response.status_code == 302:
                print(f"✅ {desc}: إعادة توجيه (طبيعي)")
            else:
                print(f"❌ {desc}: خطأ {response.status_code}")

    except Exception as e:
        print(f"❌ خطأ عام: {e}")

    print("\n" + "=" * 50)
    print("🎯 ملخص النتائج:")
    print("📍 الرابط الرئيسي: http://localhost:5000")
    print("🌟 الشاشة الموحدة: http://localhost:5000/unified_products")
    print("👤 المستخدم: admin | كلمة المرور: admin123")
    print("=" * 50)

if __name__ == "__main__":
    test_system()
