#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء فاتورة مشتريات تجريبية لاختبار الطباعة
Create Test Purchase for Print Testing
"""

import requests
import time
import json

def create_test_purchase():
    """إنشاء فاتورة مشتريات تجريبية"""
    print("📦 إنشاء فاتورة مشتريات تجريبية")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return False
    
    # بيانات فاتورة تجريبية
    purchase_data = {
        'invoice_number': f'P-TEST-PRINT-{int(time.time())}',
        'supplier_id': '1',
        'supplier_name': 'مورد تجريبي للطباعة',
        'invoice_date': '2025-01-07',
        'payment_method': 'cash',
        'branch_id': '1',
        'notes': 'فاتورة تجريبية لاختبار الطباعة',
        'total_amount': '1000.00',
        'tax_amount': '150.00',
        'final_amount': '1150.00',
        'products': json.dumps([
            {
                'product_id': '1',
                'product_name': 'منتج تجريبي للطباعة',
                'quantity': '10',
                'unit_price': '100.00',
                'total_price': '1000.00'
            }
        ])
    }
    
    print(f"📝 إنشاء فاتورة: {purchase_data['invoice_number']}")
    
    try:
        response = session.post("http://localhost:5000/api/purchases/save/debug", data=purchase_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                purchase_id = result.get('purchase_id')
                print(f"✅ تم إنشاء الفاتورة بنجاح")
                print(f"   رقم الفاتورة: {purchase_data['invoice_number']}")
                print(f"   معرف الفاتورة: {purchase_id}")
                
                # اختبار الطباعة فوراً
                if purchase_id:
                    test_print_routes(session, purchase_id, purchase_data['invoice_number'])
                
                return True
            else:
                print(f"❌ فشل إنشاء الفاتورة: {result.get('message')}")
                return False
        else:
            print(f"❌ خطأ في الخادم: {response.status_code}")
            print(f"   المحتوى: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء الفاتورة: {e}")
        return False

def test_print_routes(session, purchase_id, invoice_number):
    """اختبار مسارات الطباعة"""
    print(f"\n🖨️ اختبار طباعة الفاتورة: {invoice_number}")
    print("-" * 30)
    
    routes = [
        f'/print_purchase/{purchase_id}',
        f'/purchases/print/{purchase_id}'
    ]
    
    for route in routes:
        try:
            response = session.get(f"http://localhost:5000{route}")
            if response.status_code == 200:
                print(f"   ✅ {route}: يعمل")
                
                # فحص محتوى الاستجابة
                content = response.text
                if 'فاتورة مشتريات' in content or invoice_number in content:
                    print(f"      📄 محتوى الطباعة صحيح")
                else:
                    print(f"      ⚠️ محتوى الطباعة قد يكون غير مكتمل")
                    
            elif response.status_code == 404:
                print(f"   ❌ {route}: غير موجود (404)")
            else:
                print(f"   ⚠️ {route}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {route}: خطأ - {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🧪 إنشاء واختبار فاتورة مشتريات للطباعة")
    print("=" * 60)
    
    if create_test_purchase():
        print("\n🎉 تم إنشاء الفاتورة التجريبية بنجاح!")
        print("\n📋 يمكنك الآن:")
        print("1. الذهاب إلى شاشة المشتريات")
        print("2. البحث عن الفاتورة التجريبية")
        print("3. اختبار زر الطباعة")
        
        print("\n🔗 الروابط:")
        print("   شاشة المشتريات: http://localhost:5000/purchases")
        print("   اختبار طباعة مباشر: http://localhost:5000/print_purchase/1")
        
    else:
        print("\n❌ فشل في إنشاء الفاتورة التجريبية")
        print("💡 تأكد من:")
        print("- تشغيل الخادم")
        print("- وجود موردين في قاعدة البيانات")
        print("- صحة بيانات تسجيل الدخول")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
