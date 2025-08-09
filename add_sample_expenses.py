#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة مصروفات تجريبية لقاعدة البيانات
Add Sample Expenses to Database
"""

import sys
import os
from datetime import datetime, date, timedelta

# إضافة المسار الحالي لـ Python path
sys.path.insert(0, os.getcwd())

def add_sample_expenses():
    """إضافة مصروفات تجريبية"""
    try:
        from app import app, db, Expense
        
        with app.app_context():
            print("🔍 فحص المصروفات الموجودة...")
            
            existing_expenses = Expense.query.count()
            print(f"📊 عدد المصروفات الحالية: {existing_expenses}")
            
            if existing_expenses == 0:
                print("➕ إضافة مصروفات تجريبية...")
                
                # قائمة المصروفات التجريبية
                sample_expenses = [
                    {
                        'expense_type': 'مصروفات إدارية',
                        'description': 'رواتب الموظفين الإداريين لشهر يناير',
                        'amount': 15000.00,
                        'expense_date': date.today() - timedelta(days=30),
                        'payment_method': 'تحويل بنكي',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات تشغيلية',
                        'description': 'فاتورة الكهرباء والماء',
                        'amount': 2500.00,
                        'expense_date': date.today() - timedelta(days=25),
                        'payment_method': 'تحويل بنكي',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات صيانة',
                        'description': 'صيانة أجهزة الكمبيوتر والطابعات',
                        'amount': 1200.00,
                        'expense_date': date.today() - timedelta(days=20),
                        'payment_method': 'نقدي',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات مكتبية',
                        'description': 'شراء أدوات مكتبية وقرطاسية',
                        'amount': 800.00,
                        'expense_date': date.today() - timedelta(days=15),
                        'payment_method': 'نقدي',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات تسويقية',
                        'description': 'حملة إعلانية على وسائل التواصل الاجتماعي',
                        'amount': 3500.00,
                        'expense_date': date.today() - timedelta(days=10),
                        'payment_method': 'بطاقة ائتمان',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات سفر',
                        'description': 'سفر لحضور مؤتمر تجاري',
                        'amount': 4200.00,
                        'expense_date': date.today() - timedelta(days=7),
                        'payment_method': 'تحويل بنكي',
                        'payment_status': 'pending'
                    },
                    {
                        'expense_type': 'مصروفات اتصالات',
                        'description': 'فواتير الهاتف والإنترنت',
                        'amount': 950.00,
                        'expense_date': date.today() - timedelta(days=5),
                        'payment_method': 'تحويل بنكي',
                        'payment_status': 'paid'
                    },
                    {
                        'expense_type': 'مصروفات إيجار',
                        'description': 'إيجار المكتب لشهر فبراير',
                        'amount': 8000.00,
                        'expense_date': date.today() - timedelta(days=3),
                        'payment_method': 'تحويل بنكي',
                        'payment_status': 'pending'
                    },
                    {
                        'expense_type': 'مصروفات أخرى',
                        'description': 'تأمين على المعدات والمكتب',
                        'amount': 1800.00,
                        'expense_date': date.today() - timedelta(days=1),
                        'payment_method': 'شيك',
                        'payment_status': 'partial'
                    },
                    {
                        'expense_type': 'مصروفات تشغيلية',
                        'description': 'وقود للمركبات والمولدات',
                        'amount': 2200.00,
                        'expense_date': date.today(),
                        'payment_method': 'نقدي',
                        'payment_status': 'pending'
                    }
                ]
                
                # إضافة المصروفات
                added_count = 0
                for i, expense_data in enumerate(sample_expenses, 1):
                    try:
                        expense_number = f"EXP-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
                        
                        expense = Expense(
                            expense_number=expense_number,
                            expense_type=expense_data['expense_type'],
                            description=expense_data['description'],
                            amount=expense_data['amount'],
                            expense_date=expense_data['expense_date'],
                            payment_method=expense_data['payment_method'],
                            payment_status=expense_data['payment_status'],
                            notes=f'مصروف تجريبي رقم {i}',
                            branch_id=1,
                            created_by=1,
                            created_at=datetime.now()
                        )
                        
                        db.session.add(expense)
                        added_count += 1
                        print(f"   ✅ تم إضافة: {expense_data['expense_type']} - {expense_data['amount']} ريال")
                        
                    except Exception as e:
                        print(f"   ❌ خطأ في إضافة المصروف {i}: {e}")
                
                # حفظ التغييرات
                try:
                    db.session.commit()
                    print(f"\n✅ تم إضافة {added_count} مصروف بنجاح!")
                    
                    # التحقق من الإضافة
                    total_expenses = Expense.query.count()
                    print(f"📊 إجمالي المصروفات الآن: {total_expenses}")
                    
                    # حساب الإجماليات
                    total_amount = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
                    paid_amount = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='paid').scalar() or 0
                    pending_amount = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='pending').scalar() or 0
                    
                    print(f"\n💰 الإحصائيات:")
                    print(f"   📊 إجمالي المبلغ: {total_amount:.2f} ريال")
                    print(f"   ✅ المدفوع: {paid_amount:.2f} ريال")
                    print(f"   ⏳ المعلق: {pending_amount:.2f} ريال")
                    
                    # عرض قائمة المصروفات
                    print(f"\n📋 قائمة المصروفات:")
                    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
                    for expense in expenses:
                        status_icon = "✅" if expense.payment_status == 'paid' else "⏳" if expense.payment_status == 'pending' else "🔄"
                        print(f"   {status_icon} {expense.expense_number}: {expense.expense_type} - {expense.amount:.2f} ريال")
                    
                except Exception as e:
                    print(f"❌ خطأ في حفظ البيانات: {e}")
                    db.session.rollback()
                    return False
                    
            else:
                print("✅ يوجد مصروفات في قاعدة البيانات بالفعل")
                
                # عرض المصروفات الموجودة
                print(f"\n📋 المصروفات الموجودة:")
                expenses = Expense.query.order_by(Expense.expense_date.desc()).limit(10).all()
                for expense in expenses:
                    status_icon = "✅" if expense.payment_status == 'paid' else "⏳" if expense.payment_status == 'pending' else "🔄"
                    print(f"   {status_icon} {expense.expense_number}: {expense.expense_type} - {expense.amount:.2f} ريال")
            
            return True
            
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        import traceback
        print(f"📋 التفاصيل: {traceback.format_exc()}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("💰 إضافة مصروفات تجريبية - Add Sample Expenses")
    print("=" * 60)
    
    success = add_sample_expenses()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ انتهت العملية بنجاح")
        print("✅ Operation completed successfully")
    else:
        print("❌ فشلت العملية")
        print("❌ Operation failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
