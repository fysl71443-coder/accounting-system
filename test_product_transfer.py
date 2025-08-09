#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار ترحيل المنتجات من حساب التكاليف إلى المبيعات
Test Product Transfer from Costing to Sales
"""

import requests
import json

def test_product_transfer():
    """اختبار ترحيل المنتجات"""
    
    # تسجيل الدخول أولاً
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'language': 'ar'
    }

    response = session.post('http://localhost:5000/login', data=login_data)
    if 'login' in response.url:
        print('❌ فشل في تسجيل الدخول')
        return

    print('✅ تم تسجيل الدخول بنجاح')

    # الحصول على الوجبات المحسوبة التكلفة
    response = session.get('http://localhost:5000/api/costing_meals')
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            meals = data['meals']
            print(f'\n📋 الوجبات المتاحة ({len(meals)}):')
            for meal in meals:
                meal_name = meal.get('name', 'غير محدد')
                cost_per_serving = meal.get('cost_per_serving', 0)
                print(f'- {meal_name}: {cost_per_serving:.2f} ريال للحصة')
            
            if meals:
                # ترحيل أول وجبة كمثال
                first_meal = meals[0]
                cost_per_serving = first_meal.get('cost_per_serving', 0)
                selling_price = cost_per_serving * 1.4  # هامش ربح 40%
                
                transfer_data = {
                    'meal_id': first_meal['id'],
                    'quantity': 2,  # إنتاج دفعتين
                    'selling_price': selling_price
                }
                
                meal_name = first_meal.get('name', 'غير محدد')
                print(f'\n🔄 ترحيل الوجبة: {meal_name}')
                print(f'   التكلفة: {cost_per_serving:.2f} ريال')
                print(f'   السعر المقترح: {selling_price:.2f} ريال')
                
                response = session.post('http://localhost:5000/api/transfer_meal_to_product', 
                                      json=transfer_data,
                                      headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    result = response.json()
                    if result['status'] == 'success':
                        print(f'✅ {result["message"]}')
                        print(f'   كود المنتج: {result["product_code"]}')
                        print(f'   المخزون المضاف: {result["stock_added"]} حصة')
                        
                        # عرض المنتجات الجاهزة
                        print('\n📦 المنتجات الجاهزة للبيع:')
                        products_response = session.get('http://localhost:5000/api/products')
                        if products_response.status_code == 200:
                            products = products_response.json()
                            for product in products[-3:]:  # آخر 3 منتجات
                                profit_margin = 0
                                if product['cost'] > 0:
                                    profit_margin = ((product['price'] - product['cost']) / product['cost']) * 100
                                
                                print(f'- {product["name"]} ({product["code"]})')
                                print(f'  التكلفة: {product["cost"]:.2f} ريال | السعر: {product["price"]:.2f} ريال')
                                print(f'  المخزون: {product["stock"]} | هامش الربح: {profit_margin:.1f}%')
                    else:
                        print(f'❌ خطأ: {result["message"]}')
                else:
                    print(f'❌ خطأ HTTP: {response.status_code}')
                    print(f'Response: {response.text}')
            else:
                print('⚠️ لا توجد وجبات محسوبة التكلفة')
        else:
            print(f'❌ خطأ: {data["message"]}')
    else:
        print(f'❌ خطأ في الاتصال: {response.status_code}')

if __name__ == "__main__":
    test_product_transfer()
