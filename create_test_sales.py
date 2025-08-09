#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, Sale, SaleItem, Customer, Product
from datetime import datetime, timedelta
import random

def create_test_sales():
    """إنشاء مبيعات تجريبية لاختبار الحذف"""
    with app.app_context():
        try:
            # التأكد من وجود عملاء ومنتجات
            customers = Customer.query.all()
            products = Product.query.all()
            
            if not customers:
                print("إنشاء عملاء تجريبيين...")
                test_customers = [
                    Customer(name='أحمد محمد', phone='0501234567', email='ahmed@example.com'),
                    Customer(name='فاطمة علي', phone='0507654321', email='fatima@example.com'),
                    Customer(name='محمد سالم', phone='0509876543', email='mohammed@example.com')
                ]
                for customer in test_customers:
                    db.session.add(customer)
                db.session.commit()
                customers = Customer.query.all()
            
            if not products:
                print("إنشاء منتجات تجريبية...")
                test_products = [
                    Product(name='لابتوب HP', description='لابتوب HP Pavilion', price=2500.00, cost=2000.00, quantity=10, category='إلكترونيات'),
                    Product(name='ماوس لاسلكي', description='ماوس لاسلكي لوجيتك', price=150.00, cost=100.00, quantity=50, category='إكسسوارات'),
                    Product(name='كيبورد ميكانيكي', description='كيبورد ميكانيكي RGB', price=300.00, cost=200.00, quantity=25, category='إكسسوارات')
                ]
                for product in test_products:
                    db.session.add(product)
                db.session.commit()
                products = Product.query.all()
            
            # إنشاء مبيعات تجريبية
            print("إنشاء مبيعات تجريبية...")
            
            for i in range(5):
                # اختيار عميل عشوائي
                customer = random.choice(customers)
                
                # إنشاء فاتورة مبيعات
                sale = Sale(
                    invoice_number=f'INV-{1000 + i:06d}',
                    customer_id=customer.id,
                    subtotal=0,
                    discount=0,
                    tax_rate=15.0,
                    tax_amount=0,
                    total=0,
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'فاتورة تجريبية رقم {i+1}',
                    payment_status='unpaid'
                )
                
                db.session.add(sale)
                db.session.flush()  # للحصول على ID
                
                # إضافة عناصر للفاتورة
                subtotal = 0
                num_items = random.randint(1, 3)
                
                for j in range(num_items):
                    product = random.choice(products)
                    quantity = random.randint(1, 5)
                    unit_price = product.price
                    item_total = quantity * unit_price
                    
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        product_id=product.id,
                        product_name=product.name,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=item_total,
                        discount=0
                    )
                    
                    db.session.add(sale_item)
                    subtotal += item_total
                
                # تحديث إجماليات الفاتورة
                discount = random.randint(0, int(subtotal * 0.1))  # خصم حتى 10%
                after_discount = subtotal - discount
                tax_amount = after_discount * 0.15  # ضريبة 15%
                total = after_discount + tax_amount
                
                sale.subtotal = subtotal
                sale.discount = discount
                sale.tax_amount = tax_amount
                sale.total = total
                
                print(f"✅ تم إنشاء فاتورة {sale.invoice_number} - العميل: {customer.name} - المبلغ: {total:.2f}")
            
            db.session.commit()
            
            # عرض ملخص
            total_sales = Sale.query.count()
            print(f"\n🎉 تم إنشاء المبيعات التجريبية بنجاح!")
            print(f"📊 إجمالي الفواتير في النظام: {total_sales}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    create_test_sales()
