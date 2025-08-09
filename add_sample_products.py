#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, Product

def add_sample_products():
    """إضافة منتجات تجريبية"""
    with app.app_context():
        # التحقق من وجود منتجات
        if Product.query.count() > 0:
            print("✅ المنتجات موجودة بالفعل")
            return

        # إضافة منتجات تجريبية
        sample_products = [
            Product(
                name='لابتوب ديل', 
                description='لابتوب ديل انسبايرون 15', 
                price=2500.00, 
                cost=2000.00, 
                stock_quantity=10, 
                category='إلكترونيات', 
                is_active=True
            ),
            Product(
                name='ماوس لاسلكي', 
                description='ماوس لاسلكي لوجيتك', 
                price=150.00, 
                cost=100.00, 
                stock_quantity=50, 
                category='إكسسوارات', 
                is_active=True
            ),
            Product(
                name='كيبورد ميكانيكي', 
                description='كيبورد ميكانيكي للألعاب', 
                price=300.00, 
                cost=200.00, 
                stock_quantity=25, 
                category='إكسسوارات', 
                is_active=True
            ),
            Product(
                name='شاشة 24 بوصة', 
                description='شاشة LED 24 بوصة', 
                price=800.00, 
                cost=600.00, 
                stock_quantity=15, 
                category='إلكترونيات', 
                is_active=True
            ),
            Product(
                name='طابعة HP', 
                description='طابعة HP ليزر', 
                price=1200.00, 
                cost=900.00, 
                stock_quantity=8, 
                category='مكتبية', 
                is_active=True
            )
        ]

        for product in sample_products:
            db.session.add(product)

        db.session.commit()
        print(f'✅ تم إضافة {len(sample_products)} منتج تجريبي بنجاح')

if __name__ == '__main__':
    add_sample_products()
