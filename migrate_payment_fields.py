#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة حقول نظام المدفوعات لقاعدة البيانات
Migration script to add payment fields to database
"""

from app import app, db
import sqlite3

def add_payment_fields():
    """إضافة حقول المدفوعات لجميع الجداول"""
    
    with app.app_context():
        print("🔄 بدء إضافة حقول نظام المدفوعات...")
        
        # الحصول على مسار قاعدة البيانات
        db_path = 'accounting_system.db'
        
        try:
            # الاتصال بقاعدة البيانات مباشرة
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # فحص الجداول الموجودة أولاً
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [table[0] for table in cursor.fetchall()]
            print(f"📋 الجداول الموجودة: {existing_tables}")

            # إضافة حقول المدفوعات لجدول المبيعات
            if 'sale' in existing_tables:
                print("📊 إضافة حقول المدفوعات لجدول المبيعات...")
                try:
                    cursor.execute("ALTER TABLE sale ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid'")
                    cursor.execute("ALTER TABLE sale ADD COLUMN paid_amount FLOAT DEFAULT 0")
                    cursor.execute("ALTER TABLE sale ADD COLUMN payment_date DATETIME")
                    cursor.execute("ALTER TABLE sale ADD COLUMN payment_method VARCHAR(50)")
                    print("  ✅ تم إضافة حقول المدفوعات لجدول المبيعات")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print("  ⚠️ حقول المدفوعات موجودة بالفعل في جدول المبيعات")
                    else:
                        print(f"  ❌ خطأ في جدول المبيعات: {e}")
            else:
                print("  ⚠️ جدول المبيعات غير موجود")

            # إضافة حقول المدفوعات لجدول المشتريات
            if 'purchase' in existing_tables:
                print("📦 إضافة حقول المدفوعات لجدول المشتريات...")
                try:
                    cursor.execute("ALTER TABLE purchase ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid'")
                    cursor.execute("ALTER TABLE purchase ADD COLUMN paid_amount FLOAT DEFAULT 0")
                    cursor.execute("ALTER TABLE purchase ADD COLUMN payment_date DATETIME")
                    cursor.execute("ALTER TABLE purchase ADD COLUMN payment_method VARCHAR(50)")
                    print("  ✅ تم إضافة حقول المدفوعات لجدول المشتريات")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print("  ⚠️ حقول المدفوعات موجودة بالفعل في جدول المشتريات")
                    else:
                        print(f"  ❌ خطأ في جدول المشتريات: {e}")
            else:
                print("  ⚠️ جدول المشتريات غير موجود")

            # إضافة حقول المدفوعات لجدول المصروفات
            if 'expense' in existing_tables:
                print("💰 إضافة حقول المدفوعات لجدول المصروفات...")
                try:
                    cursor.execute("ALTER TABLE expense ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid'")
                    cursor.execute("ALTER TABLE expense ADD COLUMN paid_amount FLOAT DEFAULT 0")
                    cursor.execute("ALTER TABLE expense ADD COLUMN payment_date DATETIME")
                    cursor.execute("ALTER TABLE expense ADD COLUMN payment_method VARCHAR(50)")
                    print("  ✅ تم إضافة حقول المدفوعات لجدول المصروفات")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print("  ⚠️ حقول المدفوعات موجودة بالفعل في جدول المصروفات")
                    else:
                        print(f"  ❌ خطأ في جدول المصروفات: {e}")
            else:
                print("  ⚠️ جدول المصروفات غير موجود")

            # إضافة حقول المدفوعات لجدول الرواتب
            if 'payroll' in existing_tables:
                print("👥 إضافة حقول المدفوعات لجدول الرواتب...")
                try:
                    cursor.execute("ALTER TABLE payroll ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid'")
                    cursor.execute("ALTER TABLE payroll ADD COLUMN paid_amount FLOAT DEFAULT 0")
                    cursor.execute("ALTER TABLE payroll ADD COLUMN payment_date DATETIME")
                    cursor.execute("ALTER TABLE payroll ADD COLUMN payment_method VARCHAR(50)")
                    print("  ✅ تم إضافة حقول المدفوعات لجدول الرواتب")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print("  ⚠️ حقول المدفوعات موجودة بالفعل في جدول الرواتب")
                    else:
                        print(f"  ❌ خطأ في جدول الرواتب: {e}")
            else:
                print("  ⚠️ جدول الرواتب غير موجود")
            
            # حفظ التغييرات
            conn.commit()
            conn.close()
            
            print("💾 تم حفظ جميع التغييرات في قاعدة البيانات")
            print("🎉 تم إضافة حقول نظام المدفوعات بنجاح!")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ عام في إضافة الحقول: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False

def verify_payment_fields():
    """التحقق من وجود حقول المدفوعات"""
    
    with app.app_context():
        print("🔍 التحقق من حقول نظام المدفوعات...")
        
        try:
            conn = sqlite3.connect('accounting_system.db')
            cursor = conn.cursor()
            
            tables = ['sale', 'purchase', 'expense', 'payroll']
            payment_fields = ['payment_status', 'paid_amount', 'payment_date', 'payment_method']
            
            all_good = True
            
            for table in tables:
                print(f"📋 فحص جدول {table}:")
                
                # الحصول على معلومات الأعمدة
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [column[1] for column in cursor.fetchall()]
                
                for field in payment_fields:
                    if field in columns:
                        print(f"  ✅ {field} - موجود")
                    else:
                        print(f"  ❌ {field} - مفقود")
                        all_good = False
                
                print()
            
            conn.close()
            
            if all_good:
                print("🎉 جميع حقول المدفوعات موجودة ومُعدة بشكل صحيح!")
            else:
                print("⚠️ بعض حقول المدفوعات مفقودة - يرجى تشغيل add_payment_fields()")
            
            return all_good
            
        except Exception as e:
            print(f"❌ خطأ في التحقق من الحقول: {e}")
            return False

def update_existing_records():
    """تحديث السجلات الموجودة بحالات دفع افتراضية"""
    
    with app.app_context():
        print("🔄 تحديث السجلات الموجودة...")
        
        try:
            from app import Sale, Purchase, Expense, Payroll
            
            # تحديث المبيعات
            sales = Sale.query.filter(Sale.payment_status.is_(None)).all()
            for sale in sales:
                sale.payment_status = 'unpaid'
                sale.paid_amount = 0
            print(f"  ✅ تم تحديث {len(sales)} فاتورة مبيعات")
            
            # تحديث المشتريات
            purchases = Purchase.query.filter(Purchase.payment_status.is_(None)).all()
            for purchase in purchases:
                purchase.payment_status = 'unpaid'
                purchase.paid_amount = 0
            print(f"  ✅ تم تحديث {len(purchases)} فاتورة مشتريات")
            
            # تحديث المصروفات
            expenses = Expense.query.filter(Expense.payment_status.is_(None)).all()
            for expense in expenses:
                expense.payment_status = 'unpaid'
                expense.paid_amount = 0
            print(f"  ✅ تم تحديث {len(expenses)} مصروف")
            
            # تحديث الرواتب
            payrolls = Payroll.query.filter(Payroll.payment_status.is_(None)).all()
            for payroll in payrolls:
                payroll.payment_status = 'unpaid'
                payroll.paid_amount = 0
            print(f"  ✅ تم تحديث {len(payrolls)} راتب")
            
            db.session.commit()
            print("💾 تم حفظ جميع التحديثات")
            print("🎉 تم تحديث جميع السجلات الموجودة!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في تحديث السجلات: {e}")
            return False

def run_full_migration():
    """تشغيل migration كامل"""
    print("🚀 بدء migration نظام المدفوعات المتكامل")
    print("=" * 50)
    
    # إضافة الحقول
    if add_payment_fields():
        print("✅ تم إضافة الحقول بنجاح")
    else:
        print("❌ فشل في إضافة الحقول")
        return False
    
    print()
    
    # التحقق من الحقول
    if verify_payment_fields():
        print("✅ تم التحقق من الحقول بنجاح")
    else:
        print("❌ فشل في التحقق من الحقول")
        return False
    
    print()
    
    # تحديث السجلات الموجودة
    if update_existing_records():
        print("✅ تم تحديث السجلات الموجودة بنجاح")
    else:
        print("❌ فشل في تحديث السجلات")
        return False
    
    print()
    print("=" * 50)
    print("🎉 تم إكمال migration نظام المدفوعات بنجاح!")
    print("🔗 النظام الآن مربوط بالكامل مع شاشة المدفوعات والمستحقات")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--verify":
            verify_payment_fields()
        elif sys.argv[1] == "--update":
            update_existing_records()
        elif sys.argv[1] == "--full":
            run_full_migration()
    else:
        print("🔧 أدوات migration نظام المدفوعات:")
        print("  python migrate_payment_fields.py --full     # migration كامل")
        print("  python migrate_payment_fields.py --verify   # التحقق من الحقول")
        print("  python migrate_payment_fields.py --update   # تحديث السجلات")
        print()
        
        response = input("هل تريد تشغيل migration كامل؟ (y/n): ")
        if response.lower() == 'y':
            run_full_migration()
        else:
            print("تم إلغاء العملية")
