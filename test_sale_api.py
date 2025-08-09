#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار API حفظ الفاتورة
Test Sale API
"""

import requests
import json
from datetime import datetime

def login_first():
    """تسجيل الدخول أولاً"""
    session = requests.Session()

    # الحصول على صفحة تسجيل الدخول للحصول على CSRF token إذا كان مطلوباً
    login_page = session.get('http://localhost:5000/login')

    # بيانات تسجيل الدخول
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'language': 'ar'
    }

    # تسجيل الدخول
    response = session.post('http://localhost:5000/login', data=login_data)

    if response.status_code == 200 and 'login' not in response.url:
        print("✅ تم تسجيل الدخول بنجاح")
        return session
    else:
        print("❌ فشل في تسجيل الدخول")
        return None

def test_save_sale_api():
    """اختبار API حفظ الفاتورة"""

    # تسجيل الدخول أولاً
    session = login_first()
    if not session:
        return

    # بيانات الفاتورة التجريبية
    sale_data = {
        "invoice_number": "TEST-API-001",
        "branch_id": 1,
        "customer_name": "عميل تجريبي API",
        "invoice_date": datetime.now().strftime('%Y-%m-%d'),
        "total_amount": 25.0,
        "tax_amount": 3.75,
        "final_amount": 28.75,
        "payment_method": "CASH",
        "items": [
            {
                "product_id": 1,
                "product_name": "برجر لحم",
                "quantity": 1.0,
                "unit_price": 25.0,
                "total_price": 25.0,
                "tax_rate": 15.0,
                "tax_amount": 3.75
            }
        ]
    }
    
    try:
        # إرسال الطلب باستخدام الجلسة المسجلة
        response = session.post(
            'http://localhost:5000/api/save_sale',
            json=sale_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print("✅ تم حفظ الفاتورة بنجاح!")
                print(f"معرف الفاتورة: {result['sale_id']}")
            else:
                print(f"❌ خطأ: {result['message']}")
        else:
            print(f"❌ خطأ HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم. تأكد من أن التطبيق يعمل على http://localhost:5000")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

if __name__ == "__main__":
    test_save_sale_api()
