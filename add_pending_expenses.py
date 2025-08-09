#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة مصروفات بحالة pending لاختبار المدفوعات والمستحقات
Add Pending Expenses for Testing Payments and Dues
"""

import sys
import os
from datetime import datetime, date, timedelta

# إضافة المسار الحالي لـ Python path
sys.path.insert(0, os.getcwd())

def add_pending_expenses():
    """إضافة مصروفات بحالة pending"""
    try:
        from app import app, db, Expense
        
        with app.app_context():
            print("💰 إضافة مصروفات بحالة pending...")
            
            # قائمة المصروفات بحالة pending
            pending_expenses = [
                {
                    'expense_type': 'مصروفات إدارية',
                    'description': 'رواتب الموظفين الإداريين - معلق',
                    'amount': 12000.00,
                    'expense_date': date.today() - timedelta(days=5),
                    'payment_method': 'تحويل بنكي',
                    'payment_status': 'pending'
                },
                {
                    'expense_type': 'مصروفات تشغيلية',
                    'description': 'فاتورة الكهرباء والماء - غير مدفوعة',
                    'amount': 3500.00,
                    'expense_date': date.today() - timedelta(days=3),
                    'payment_method': 'تحويل بنكي',
                    'payment_status': 'pending'
                },
                {
                    'expense_type': 'مصروفات صيانة',
                    'description': 'صيانة المعدات - مدفوع جزئياً',
                    'amount': 2800.00,
                    'expense_date': date.today() - timedelta(days=2),
                    'payment_method': 'نقدي',
                    'payment_status': 'partial'
                },
                {
                    'expense_type': 'مصروفات إيجار',
                    'description': 'إيجار المكتب - معلق',
                    'amount': 8500.00,
                    'expense_date': date.today() - timedelta(days=1),
                    'payment_method': 'تحويل بنكي',
                    'payment_status': 'pending'
                },
                {
                    'expense_type': 'مصروفات تسويقية',
                    'description': 'حملة إعلانية - غير مدفوعة',
                    'amount': 4200.00,
                    'expense_date': date.today(),
                    'payment_method': 'بطاقة ائتمان',
                    'payment_status': 'pending'
                }
            ]
            
            # إضافة المصروفات
            added_count = 0
            for i, expense_data in enumerate(pending_expenses, 1):
                try:
                    expense_number = f"EXP-PENDING-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
                    
                    expense = Expense(
                        expense_number=expense_number,
                        expense_type=expense_data['expense_type'],
                        description=expense_data['description'],
                        amount=expense_data['amount'],
                        expense_date=expense_data['expense_date'],
                        payment_method=expense_data['payment_method'],
                        payment_status=expense_data['payment_status'],
                        notes=f'مصروف اختبار - حالة {expense_data["payment_status"]}',
                        branch_id=1,
                        created_by=1,
                        created_at=datetime.now()
                    )
                    
                    db.session.add(expense)
                    added_count += 1
                    
                    status_icon = "⏳" if expense_data['payment_status'] == 'pending' else "🔄"
                    print(f"   {status_icon} تم إضافة: {expense_data['expense_type']} - {expense_data['amount']} ريال - {expense_data['payment_status']}")
                    
                except Exception as e:
                    print(f"   ❌ خطأ في إضافة المصروف {i}: {e}")
            
            # حفظ التغييرات
            try:
                db.session.commit()
                print(f"\n✅ تم إضافة {added_count} مصروف بحالة pending/partial!")
                
                # التحقق من النتائج
                pending_count = Expense.query.filter_by(payment_status='pending').count()
                partial_count = Expense.query.filter_by(payment_status='partial').count()
                paid_count = Expense.query.filter_by(payment_status='paid').count()
                total_count = Expense.query.count()
                
                print(f"\n📊 إحصائيات المصروفات:")
                print(f"   ⏳ معلقة: {pending_count}")
                print(f"   🔄 مدفوعة جزئياً: {partial_count}")
                print(f"   ✅ مدفوعة: {paid_count}")
                print(f"   📊 الإجمالي: {total_count}")
                
                # حساب المبالغ
                pending_amount = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='pending').scalar() or 0
                partial_amount = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='partial').scalar() or 0
                paid_amount = db.session.query(db.func.sum(Expense.amount)).filter_by(payment_status='paid').scalar() or 0
                
                print(f"\n💰 المبالغ:")
                print(f"   ⏳ معلقة: {pending_amount:.2f} ريال")
                print(f"   🔄 مدفوعة جزئياً: {partial_amount:.2f} ريال")
                print(f"   ✅ مدفوعة: {paid_amount:.2f} ريال")
                print(f"   📊 الإجمالي: {(pending_amount + partial_amount + paid_amount):.2f} ريال")
                
                # عرض المصروفات غير المدفوعة
                print(f"\n📋 المصروفات غير المدفوعة:")
                unpaid_expenses = Expense.query.filter(Expense.payment_status.in_(['pending', 'partial'])).all()
                for expense in unpaid_expenses:
                    status_icon = "⏳" if expense.payment_status == 'pending' else "🔄"
                    print(f"   {status_icon} {expense.expense_number}: {expense.expense_type} - {expense.amount:.2f} ريال")
                
                return True
                
            except Exception as e:
                print(f"❌ خطأ في حفظ البيانات: {e}")
                db.session.rollback()
                return False
                
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        import traceback
        print(f"📋 التفاصيل: {traceback.format_exc()}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("⏳ إضافة مصروفات بحالة pending - Add Pending Expenses")
    print("=" * 60)
    
    success = add_pending_expenses()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ انتهت العملية بنجاح")
        print("✅ Operation completed successfully")
        print("🔗 يمكنك الآن زيارة /payments_dues لرؤية المصروفات")
        print("🔗 You can now visit /payments_dues to see the expenses")
    else:
        print("❌ فشلت العملية")
        print("❌ Operation failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
