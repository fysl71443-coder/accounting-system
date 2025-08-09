#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعادة تعيين قاعدة البيانات مع خانات الخصم
Reset Database with Discount Fields
"""

import os
import sys
from app import app, db, User, Customer, Supplier, Product, Sale, Purchase, Expense, Employee, Payroll
from werkzeug.security import generate_password_hash

def reset_database():
    """إعادة تعيين قاعدة البيانات"""
    print("🔄 إعادة تعيين قاعدة البيانات...")
    
    with app.app_context():
        # حذف جميع الجداول
        db.drop_all()
        print("✅ تم حذف الجداول القديمة")
        
        # إنشاء جداول جديدة
        db.create_all()
        print("✅ تم إنشاء الجداول الجديدة")
        
        # إنشاء مستخدم افتراضي
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin112233'),
            is_admin=True
        )
        db.session.add(admin_user)
        print("✅ تم إنشاء المستخدم الافتراضي")
        
        # إنشاء عملاء تجريبيين
        customers = [
            Customer(name='شركة الأمل التجارية', phone='0501234567', email='amal@example.com'),
            Customer(name='مؤسسة النور للتجارة', phone='0507654321', email='noor@example.com'),
            Customer(name='شركة الفجر الجديد', phone='0509876543', email='fajr@example.com'),
            Customer(name='مكتب الرياض للاستشارات', phone='0502468135', email='riyadh@example.com'),
            Customer(name='عميل نقدي', phone='0500000000', email='cash@example.com')
        ]
        for customer in customers:
            db.session.add(customer)
        print("✅ تم إنشاء العملاء التجريبيين")
        
        # إنشاء موردين تجريبيين
        suppliers = [
            Supplier(name='شركة التوريدات المتقدمة', phone='0111234567', email='advanced@example.com'),
            Supplier(name='مؤسسة الإمداد الشامل', phone='0117654321', email='supply@example.com'),
            Supplier(name='شركة المواد الأساسية', phone='0119876543', email='materials@example.com'),
            Supplier(name='مورد المعدات الصناعية', phone='0112468135', email='equipment@example.com')
        ]
        for supplier in suppliers:
            db.session.add(supplier)
        print("✅ تم إنشاء الموردين التجريبيين")
        
        # إنشاء منتجات تجريبية
        products = [
            Product(name='منتج أ', price=100, cost=70, quantity=50, category='فئة 1'),
            Product(name='منتج ب', price=200, cost=140, quantity=30, category='فئة 2'),
            Product(name='منتج ج', price=150, cost=100, quantity=40, category='فئة 1'),
            Product(name='منتج د', price=300, cost=200, quantity=20, category='فئة 3')
        ]
        for product in products:
            db.session.add(product)
        print("✅ تم إنشاء المنتجات التجريبية")
        
        # إنشاء مبيعات تجريبية مع خصم
        sales = [
            Sale(customer_id=1, subtotal=2700, discount=200, total=2500),
            Sale(customer_id=2, subtotal=2000, discount=200, total=1800),
            Sale(customer_id=3, subtotal=3500, discount=300, total=3200),
            Sale(customer_id=4, subtotal=1650, discount=150, total=1500),
            Sale(customer_id=5, subtotal=1000, discount=50, total=950)
        ]
        for sale in sales:
            db.session.add(sale)
        print("✅ تم إنشاء المبيعات التجريبية مع الخصم")
        
        # إنشاء مشتريات تجريبية مع خصم
        purchases = [
            Purchase(supplier_id=1, subtotal=6000, discount=500, total=5500),
            Purchase(supplier_id=2, subtotal=3500, discount=300, total=3200),
            Purchase(supplier_id=3, subtotal=4400, discount=300, total=4100),
            Purchase(supplier_id=4, subtotal=3000, discount=200, total=2800)
        ]
        for purchase in purchases:
            db.session.add(purchase)
        print("✅ تم إنشاء المشتريات التجريبية مع الخصم")
        
        # إنشاء مصروفات تجريبية
        expenses = [
            Expense(description='مصروفات إدارية', amount=800, category='إدارية'),
            Expense(description='مصروفات تشغيلية', amount=1200, category='تشغيلية'),
            Expense(description='مصروفات صيانة', amount=650, category='صيانة'),
            Expense(description='مصروفات نقل', amount=450, category='نقل')
        ]
        for expense in expenses:
            db.session.add(expense)
        print("✅ تم إنشاء المصروفات التجريبية")
        
        # إنشاء موظفين تجريبيين
        employees = [
            Employee(name='أحمد محمد علي', position='مدير المبيعات', salary=8500, phone='0501111111'),
            Employee(name='فاطمة أحمد سالم', position='محاسبة', salary=6200, phone='0502222222'),
            Employee(name='محمد عبدالله حسن', position='موظف إداري', salary=4800, phone='0503333333'),
            Employee(name='سارة علي محمد', position='سكرتيرة', salary=4200, phone='0504444444')
        ]
        for employee in employees:
            db.session.add(employee)
        print("✅ تم إنشاء الموظفين التجريبيين")
        
        # إنشاء رواتب تجريبية
        payrolls = [
            Payroll(employee_id=1, amount=8500, month='2024-01'),
            Payroll(employee_id=2, amount=6200, month='2024-01'),
            Payroll(employee_id=3, amount=4800, month='2024-01'),
            Payroll(employee_id=4, amount=4200, month='2024-01')
        ]
        for payroll in payrolls:
            db.session.add(payroll)
        print("✅ تم إنشاء الرواتب التجريبية")
        
        # حفظ جميع التغييرات
        db.session.commit()
        print("✅ تم حفظ جميع البيانات")
        
        print("\n🎉 تم إعادة تعيين قاعدة البيانات بنجاح!")
        print("📊 البيانات التجريبية:")
        print(f"   - العملاء: {len(customers)}")
        print(f"   - الموردين: {len(suppliers)}")
        print(f"   - المنتجات: {len(products)}")
        print(f"   - المبيعات: {len(sales)} (مع خصم)")
        print(f"   - المشتريات: {len(purchases)} (مع خصم)")
        print(f"   - المصروفات: {len(expenses)}")
        print(f"   - الموظفين: {len(employees)}")
        print(f"   - الرواتب: {len(payrolls)}")
        print("\n🔑 بيانات تسجيل الدخول:")
        print("   - المستخدم: admin")
        print("   - كلمة المرور: admin112233")

if __name__ == '__main__':
    reset_database()
