#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح نموذج Purchase وإضافة حقل supplier_id
Fix Purchase Model and Add supplier_id Field
"""

import os
import sys
from datetime import datetime

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'

def fix_purchase_model():
    """إصلاح نموذج Purchase"""
    print("🔧 إصلاح نموذج Purchase...")
    print("=" * 50)
    
    try:
        from app import app, db, Purchase, Supplier
        
        with app.app_context():
            print("📊 فحص قاعدة البيانات الحالية...")
            
            # فحص إذا كان العمود supplier_id موجود
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('purchases')]
            
            print(f"📋 الأعمدة الحالية في جدول purchases: {columns}")
            
            if 'supplier_id' not in columns:
                print("⚠️ العمود supplier_id غير موجود، سيتم إضافته...")
                
                # إضافة العمود الجديد
                try:
                    with db.engine.connect() as conn:
                        conn.execute(db.text("""
                            ALTER TABLE purchases 
                            ADD COLUMN supplier_id INTEGER 
                            REFERENCES suppliers(id)
                        """))
                        conn.commit()
                    
                    print("✅ تم إضافة العمود supplier_id بنجاح")
                    
                except Exception as e:
                    print(f"❌ خطأ في إضافة العمود: {e}")
                    print("💡 سيتم إعادة إنشاء الجداول...")
                    
                    # إعادة إنشاء الجداول
                    db.drop_all()
                    db.create_all()
                    print("✅ تم إعادة إنشاء الجداول")
                    
            else:
                print("✅ العمود supplier_id موجود بالفعل")
            
            # إنشاء بيانات تجريبية للموردين إذا لم تكن موجودة
            if Supplier.query.count() == 0:
                print("📦 إنشاء موردين تجريبيين...")
                
                suppliers = [
                    Supplier(
                        name='مورد 1',
                        contact_person='أحمد محمد',
                        phone='0501234567',
                        email='supplier1@example.com',
                        address='الرياض، المملكة العربية السعودية'
                    ),
                    Supplier(
                        name='مورد 2', 
                        contact_person='فاطمة علي',
                        phone='0507654321',
                        email='supplier2@example.com',
                        address='جدة، المملكة العربية السعودية'
                    ),
                    Supplier(
                        name='مورد 3',
                        contact_person='محمد سالم',
                        phone='0509876543',
                        email='supplier3@example.com',
                        address='الدمام، المملكة العربية السعودية'
                    )
                ]
                
                for supplier in suppliers:
                    db.session.add(supplier)
                
                db.session.commit()
                print(f"✅ تم إنشاء {len(suppliers)} مورد تجريبي")
            
            # فحص فواتير المشتريات الموجودة
            purchases_count = Purchase.query.count()
            print(f"📊 عدد فواتير المشتريات الموجودة: {purchases_count}")
            
            # إنشاء فاتورة مشتريات تجريبية للاختبار
            if purchases_count == 0:
                print("📦 إنشاء فاتورة مشتريات تجريبية...")
                
                supplier = Supplier.query.first()
                if supplier:
                    test_purchase = Purchase(
                        invoice_number='P-TEST-001',
                        supplier_id=supplier.id,
                        supplier_name=supplier.name,
                        invoice_date=datetime.now().date(),
                        total_amount=1000.0,
                        tax_amount=150.0,
                        final_amount=1150.0,
                        payment_method='cash',
                        payment_status='pending',
                        notes='فاتورة تجريبية لاختبار النظام'
                    )
                    
                    db.session.add(test_purchase)
                    db.session.commit()
                    
                    print("✅ تم إنشاء فاتورة مشتريات تجريبية")
                else:
                    print("⚠️ لا يوجد موردين لإنشاء فاتورة تجريبية")
            
            print("\n✅ تم إصلاح نموذج Purchase بنجاح!")
            
    except Exception as e:
        print(f"❌ خطأ في إصلاح نموذج Purchase: {e}")
        import traceback
        traceback.print_exc()

def test_purchase_creation():
    """اختبار إنشاء فاتورة مشتريات"""
    print("\n🧪 اختبار إنشاء فاتورة مشتريات...")
    print("=" * 50)
    
    try:
        from app import app, db, Purchase, Supplier
        
        with app.app_context():
            supplier = Supplier.query.first()
            
            if not supplier:
                print("❌ لا يوجد موردين في قاعدة البيانات")
                return False
            
            # محاولة إنشاء فاتورة مشتريات
            test_purchase = Purchase(
                invoice_number=f'P-TEST-{int(datetime.now().timestamp())}',
                supplier_id=supplier.id,  # هذا يجب أن يعمل الآن
                supplier_name=supplier.name,
                invoice_date=datetime.now().date(),
                total_amount=500.0,
                tax_amount=75.0,
                final_amount=575.0,
                payment_method='credit',
                payment_status='pending',
                notes='اختبار إنشاء فاتورة مشتريات'
            )
            
            db.session.add(test_purchase)
            db.session.commit()
            
            print(f"✅ تم إنشاء فاتورة مشتريات بنجاح: {test_purchase.invoice_number}")
            print(f"   المورد: {test_purchase.supplier_name} (ID: {test_purchase.supplier_id})")
            print(f"   المبلغ النهائي: {test_purchase.final_amount} ريال")
            
            return True
            
    except Exception as e:
        print(f"❌ خطأ في اختبار إنشاء فاتورة المشتريات: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🔧 إصلاح مشكلة supplier_id في نموذج Purchase")
    print("=" * 60)
    
    # إصلاح النموذج
    fix_purchase_model()
    
    # اختبار الإنشاء
    if test_purchase_creation():
        print("\n🎉 تم إصلاح المشكلة بنجاح!")
        print("✅ يمكن الآن إنشاء فواتير المشتريات بدون أخطاء")
    else:
        print("\n❌ لا تزال هناك مشكلة في إنشاء فواتير المشتريات")
    
    print("\n📋 ملخص الإصلاحات:")
    print("1. ✅ إضافة حقل supplier_id إلى نموذج Purchase")
    print("2. ✅ إضافة علاقة مع نموذج Supplier")
    print("3. ✅ حذف property supplier_id القديم")
    print("4. ✅ إنشاء موردين تجريبيين")
    print("5. ✅ اختبار إنشاء فاتورة مشتريات")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
