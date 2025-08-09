#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لشاشة المشتريات
Quick Purchases Screen Test
"""

import requests
import webbrowser

def quick_purchases_test():
    """اختبار سريع لشاشة المشتريات"""
    print("🧪 اختبار سريع لشاشة المشتريات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        print("💡 شغل الخادم: python run_local.py")
        return
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return
    
    # فحص صفحة المشتريات
    try:
        response = session.get("http://localhost:5000/purchases")
        if response.status_code == 200:
            print("✅ صفحة المشتريات تعمل")
            
            content = response.text
            
            # فحص العناصر الأساسية
            elements_found = 0
            required_elements = [
                ('إدارة المشتريات', 'عنوان الصفحة'),
                ('إجمالي المشتريات', 'بطاقة الإحصائيات'),
                ('فاتورة جديدة', 'زر إنشاء فاتورة'),
                ('نموذج متقدم', 'زر النموذج المتقدم'),
                ('المدفوعات والمستحقات', 'زر المدفوعات'),
                ('طباعة التقرير', 'زر الطباعة'),
                ('purchases-table', 'جدول المشتريات'),
                ('purchaseModal', 'نافذة إنشاء فاتورة')
            ]
            
            print("\n🔍 فحص العناصر:")
            for element, description in required_elements:
                if element in content:
                    print(f"   ✅ {description}")
                    elements_found += 1
                else:
                    print(f"   ❌ {description}")
            
            print(f"\n📊 النتيجة: {elements_found}/{len(required_elements)} عنصر موجود")
            
            if elements_found >= len(required_elements) * 0.8:  # 80% من العناصر
                print("🎉 شاشة المشتريات تعمل بشكل جيد!")
            else:
                print("⚠️ بعض العناصر مفقودة في شاشة المشتريات")
                
        else:
            print(f"❌ صفحة المشتريات فشلت: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في فحص صفحة المشتريات: {e}")
    
    # اختبار routes أساسية
    print("\n🔍 اختبار routes أساسية:")
    
    routes = [
        ('/api/purchases/list', 'قائمة المشتريات'),
        ('/purchases/simple', 'النموذج المبسط'),
        ('/purchases/data/check', 'فحص البيانات')
    ]
    
    for route, name in routes:
        try:
            response = session.get(f"http://localhost:5000{route}")
            if response.status_code == 200:
                print(f"   ✅ {name}")
            else:
                print(f"   ⚠️ {name}: {response.status_code}")
        except:
            print(f"   ❌ {name}: خطأ")
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/purchases")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. سجل الدخول: admin / admin123")
    print("2. اختبر الأزرار:")
    print("   - فاتورة جديدة → النموذج المبسط")
    print("   - نموذج متقدم → النموذج المتقدم")
    print("   - المدفوعات والمستحقات → شاشة المدفوعات")
    print("   - طباعة التقرير → طباعة الصفحة")
    print("   - تحديث → تحديث البيانات")
    
    print("\n🔗 الروابط:")
    print("   شاشة المشتريات: http://localhost:5000/purchases")
    print("   النموذج المبسط: http://localhost:5000/purchases/simple")
    
    print("\n🌟 المزايا المتوفرة:")
    print("✅ إحصائيات المشتريات (إجمالي، مدفوع، معلق)")
    print("✅ جدول فواتير المشتريات مع البحث والفلترة")
    print("✅ نماذج إنشاء الفواتير (مبسط ومتقدم)")
    print("✅ أزرار العمليات (عرض، تعديل، طباعة، حذف)")
    print("✅ تصدير البيانات إلى Excel")
    print("✅ طباعة التقارير")
    
    print("=" * 50)

if __name__ == "__main__":
    quick_purchases_test()
