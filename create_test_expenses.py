#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, Expense
from datetime import datetime, timedelta
import random

def create_test_expenses():
    """إنشاء مصروفات تجريبية لاختبار الأزرار"""
    with app.app_context():
        try:
            print("إنشاء مصروفات تجريبية...")
            
            # قائمة مصروفات تجريبية
            test_expenses = [
                {
                    'description': 'فاتورة كهرباء',
                    'amount': 500.00,
                    'category': 'مرافق',
                    'expense_type': 'تشغيلي',
                    'vendor': 'شركة الكهرباء'
                },
                {
                    'description': 'إيجار المكتب',
                    'amount': 3000.00,
                    'category': 'إيجار',
                    'expense_type': 'ثابت',
                    'vendor': 'شركة العقارات'
                },
                {
                    'description': 'مواد مكتبية',
                    'amount': 150.00,
                    'category': 'مكتبية',
                    'expense_type': 'متغير',
                    'vendor': 'مكتبة الأعمال'
                },
                {
                    'description': 'صيانة أجهزة',
                    'amount': 800.00,
                    'category': 'صيانة',
                    'expense_type': 'طارئ',
                    'vendor': 'شركة الصيانة'
                },
                {
                    'description': 'وقود السيارات',
                    'amount': 400.00,
                    'category': 'مواصلات',
                    'expense_type': 'تشغيلي',
                    'vendor': 'محطة الوقود'
                }
            ]
            
            for i, expense_data in enumerate(test_expenses, 1):
                expense = Expense(
                    expense_number=f'EXP-{1000 + i:06d}',
                    description=expense_data['description'],
                    amount=expense_data['amount'],
                    category=expense_data['category'],
                    expense_type=expense_data['expense_type'],
                    vendor=expense_data['vendor'],
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'مصروف تجريبي رقم {i}',
                    payment_status='unpaid',
                    paid_amount=0
                )
                
                db.session.add(expense)
                print(f"✅ تم إنشاء مصروف: {expense.expense_number} - {expense.description} - {expense.amount:.2f} ريال")
            
            db.session.commit()
            
            # عرض ملخص
            total_expenses = Expense.query.count()
            print(f"\n🎉 تم إنشاء المصروفات التجريبية بنجاح!")
            print(f"📊 إجمالي المصروفات في النظام: {total_expenses}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    create_test_expenses()
