#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الشاشة الموحدة للمنتجات والتكاليف
Test Unified Products & Costing Screen
"""

import requests
import json

def test_unified_products():
    """اختبار الشاشة الموحدة"""
    
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

    # 1. اختبار إضافة مادة خام
    print('\n🧪 اختبار إضافة مادة خام...')
    raw_material_data = {
        'name': 'لحم بقري طازج',
        'unit': 'كيلو',
        'price': 45.00,
        'stock': 20.0,
        'min_stock': 5.0,
        'supplier': 'مجزرة اللحوم الطازجة'
    }
    
    response = session.post('http://localhost:5000/api/raw_materials', 
                           json=raw_material_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f'✅ تم إضافة المادة الخام: {raw_material_data["name"]}')
        else:
            print(f'❌ خطأ في إضافة المادة الخام: {result.get("message")}')
    else:
        print(f'❌ خطأ HTTP في إضافة المادة الخام: {response.status_code}')

    # 2. اختبار الحصول على المواد الخام
    print('\n📋 اختبار تحميل المواد الخام...')
    response = session.get('http://localhost:5000/api/raw_materials')
    
    if response.status_code == 200:
        materials = response.json()
        print(f'✅ تم تحميل {len(materials)} مادة خام')
        
        # عرض أول 5 مواد
        print('📦 أول 5 مواد خام:')
        for material in materials[:5]:
            stock_status = '⚠️' if material['stock'] <= material['min_stock'] else '✅'
            print(f'   {stock_status} {material["name"]}: {material["price"]:.2f} ريال/{material["unit"]} (المخزون: {material["stock"]})')
    else:
        print(f'❌ خطأ في تحميل المواد الخام: {response.status_code}')

    # 3. اختبار إنشاء منتج مع تكلفة تفصيلية
    print('\n🍽️ اختبار إنشاء منتج مع تكلفة تفصيلية...')
    
    # الحصول على معرفات المواد الخام للاختبار
    if response.status_code == 200:
        materials = response.json()
        
        # البحث عن مواد محددة
        chicken = next((m for m in materials if 'دجاج' in m['name']), None)
        rice = next((m for m in materials if 'أرز' in m['name']), None)
        onion = next((m for m in materials if 'بصل' in m['name']), None)
        
        if chicken and rice and onion:
            product_data = {
                'name': 'كبسة دجاج مميزة',
                'description': 'كبسة دجاج بالخضار والبهارات الطبيعية',
                'servings': 4,
                'category': 'وجبات رئيسية',
                'ingredients': [
                    {
                        'material_id': chicken['id'],
                        'material_name': chicken['name'],
                        'quantity': 1.5,
                        'unit_price': chicken['price'],
                        'total_cost': 1.5 * chicken['price'],
                        'percentage': 0  # سيتم حسابها
                    },
                    {
                        'material_id': rice['id'],
                        'material_name': rice['name'],
                        'quantity': 0.8,
                        'unit_price': rice['price'],
                        'total_cost': 0.8 * rice['price'],
                        'percentage': 0
                    },
                    {
                        'material_id': onion['id'],
                        'material_name': onion['name'],
                        'quantity': 0.3,
                        'unit_price': onion['price'],
                        'total_cost': 0.3 * onion['price'],
                        'percentage': 0
                    }
                ],
                'total_cost': 0,  # سيتم حسابها
                'cost_per_serving': 0,  # سيتم حسابها
                'suggested_price': 0  # سيتم حسابها
            }
            
            # حساب التكاليف
            total_cost = sum(ing['total_cost'] for ing in product_data['ingredients'])
            cost_per_serving = total_cost / product_data['servings']
            suggested_price = cost_per_serving * 1.4  # هامش ربح 40%
            
            # تحديث النسب المئوية
            for ingredient in product_data['ingredients']:
                ingredient['percentage'] = (ingredient['total_cost'] / total_cost * 100) if total_cost > 0 else 0
            
            product_data['total_cost'] = total_cost
            product_data['cost_per_serving'] = cost_per_serving
            product_data['suggested_price'] = suggested_price
            
            print(f'📊 تفاصيل المنتج:')
            print(f'   الاسم: {product_data["name"]}')
            print(f'   إجمالي التكلفة: {total_cost:.2f} ريال')
            print(f'   تكلفة الحصة: {cost_per_serving:.2f} ريال')
            print(f'   السعر المقترح: {suggested_price:.2f} ريال')
            print(f'   المكونات:')
            for ing in product_data['ingredients']:
                print(f'     - {ing["material_name"]}: {ing["quantity"]} × {ing["unit_price"]:.2f} = {ing["total_cost"]:.2f} ريال ({ing["percentage"]:.1f}%)')
            
            # إرسال البيانات
            response = session.post('http://localhost:5000/api/save_product_cost',
                                   json=product_data,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f'✅ تم حفظ المنتج بنجاح!')
                    print(f'   كود المنتج: {result["product_code"]}')
                    print(f'   معرف المنتج: {result["product_id"]}')
                else:
                    print(f'❌ خطأ في حفظ المنتج: {result.get("message")}')
            else:
                print(f'❌ خطأ HTTP في حفظ المنتج: {response.status_code}')
                print(f'Response: {response.text}')
        else:
            print('❌ لم يتم العثور على المواد الخام المطلوبة للاختبار')

    # 4. اختبار تحميل المنتجات الجاهزة
    print('\n📦 اختبار تحميل المنتجات الجاهزة...')
    response = session.get('http://localhost:5000/api/products')
    
    if response.status_code == 200:
        products = response.json()
        print(f'✅ تم تحميل {len(products)} منتج جاهز')
        
        # عرض آخر 3 منتجات
        print('🍽️ آخر المنتجات المضافة:')
        for product in products[-3:]:
            profit_margin = 0
            if product['cost'] > 0:
                profit_margin = ((product['price'] - product['cost']) / product['cost']) * 100
            
            print(f'   📋 {product["name"]} ({product["code"]})')
            print(f'      التكلفة: {product["cost"]:.2f} ريال | السعر: {product["price"]:.2f} ريال')
            print(f'      المخزون: {product["stock"]} | هامش الربح: {profit_margin:.1f}%')
    else:
        print(f'❌ خطأ في تحميل المنتجات: {response.status_code}')

    print('\n🎉 انتهى الاختبار!')
    print('🌐 يمكنك الآن الوصول للشاشة الموحدة على: http://localhost:5000/unified_products')

if __name__ == "__main__":
    test_unified_products()
