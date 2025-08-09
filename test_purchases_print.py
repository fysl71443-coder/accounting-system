#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار طباعة المشتريات
Test Purchases Print
"""

import requests
import webbrowser

def test_purchases_print():
    """اختبار طباعة المشتريات"""
    print("🖨️ اختبار طباعة المشتريات")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
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
    
    # فحص فواتير المشتريات
    try:
        response = session.get("http://localhost:5000/api/purchases/list")
        if response.status_code == 200:
            data = response.json()
            purchases = data.get('purchases', [])
            
            if purchases:
                print(f"✅ وجدت {len(purchases)} فاتورة مشتريات")
                
                # اختبار طباعة أول فاتورة
                first_purchase = purchases[0]
                purchase_id = first_purchase['id']
                invoice_number = first_purchase['invoice_number']
                
                print(f"\n🖨️ اختبار طباعة: {invoice_number} (ID: {purchase_id})")
                
                # اختبار المسارات
                routes = [
                    f'/print_purchase/{purchase_id}',
                    f'/purchases/print/{purchase_id}'
                ]
                
                for route in routes:
                    try:
                        response = session.get(f"http://localhost:5000{route}")
                        if response.status_code == 200:
                            print(f"   ✅ {route}: يعمل")
                        else:
                            print(f"   ❌ {route}: {response.status_code}")
                    except Exception as e:
                        print(f"   ❌ {route}: خطأ - {e}")
                
            else:
                print("⚠️ لا توجد فواتير مشتريات")
                
        else:
            print(f"❌ فشل جلب المشتريات: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    # فتح المتصفح
    print("\n🌐 فتح المتصفح...")
    webbrowser.open("http://localhost:5000/purchases")
    
    print("\n📋 تعليمات الاختبار:")
    print("1. سجل الدخول: admin / admin123")
    print("2. ابحث عن فاتورة في جدول المشتريات")
    print("3. اضغط زر الطباعة (أيقونة الطابعة)")
    print("4. يجب أن تفتح نافذة طباعة جديدة")
    
    print("\n🔧 إذا لم تعمل الطباعة:")
    print("- تأكد من وجود فواتير مشتريات")
    print("- اضغط F12 وفحص Console للأخطاء")
    print("- جرب الرابط المباشر: http://localhost:5000/print_purchase/1")
    
    print("=" * 50)

if __name__ == "__main__":
    test_purchases_print()
