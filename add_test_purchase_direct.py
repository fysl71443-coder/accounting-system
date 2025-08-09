#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة فاتورة مشتريات تجريبية مباشرة
Add Test Purchase Directly
"""

import os
from datetime import datetime, date

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'test-key-for-development'

def add_test_purchase():
    """إضافة فاتورة مشتريات تجريبية"""
    print("📦 إضافة فاتورة مشتريات تجريبية")
    print("=" * 50)
    
    try:
        from app import app, db, Purchase, PurchaseItem, Supplier, Product
        
        with app.app_context():
            # التأكد من وجود مورد
            supplier = Supplier.query.first()
            if not supplier:
                print("📦 إنشاء مورد تجريبي...")
                supplier = Supplier(
                    name='مورد تجريبي للطباعة',
                    contact_person='أحمد محمد',
                    phone='0501234567',
                    email='test@supplier.com',
                    address='الرياض، المملكة العربية السعودية'
                )
                db.session.add(supplier)
                db.session.commit()
                print("✅ تم إنشاء مورد تجريبي")
            
            # التأكد من وجود منتج
            product = Product.query.first()
            if not product:
                print("📦 إنشاء منتج تجريبي...")
                product = Product(
                    name='منتج تجريبي للطباعة',
                    price=100.0,
                    stock_quantity=100
                )
                db.session.add(product)
                db.session.commit()
                print("✅ تم إنشاء منتج تجريبي")
            
            # إنشاء فاتورة مشتريات تجريبية
            invoice_number = f'P-TEST-PRINT-{int(datetime.now().timestamp())}'
            
            test_purchase = Purchase(
                invoice_number=invoice_number,
                supplier_id=supplier.id,
                supplier_name=supplier.name,
                invoice_date=date.today(),
                total_amount=1000.0,
                tax_amount=150.0,
                final_amount=1150.0,
                payment_method='cash',
                payment_status='pending',
                notes='فاتورة تجريبية لاختبار الطباعة'
            )
            
            db.session.add(test_purchase)
            db.session.commit()
            
            print(f"✅ تم إنشاء فاتورة المشتريات: {invoice_number}")
            print(f"   معرف الفاتورة: {test_purchase.id}")
            print(f"   المورد: {supplier.name}")
            print(f"   المبلغ النهائي: {test_purchase.final_amount} ريال")
            
            # إضافة عناصر الفاتورة
            test_item = PurchaseItem(
                purchase_id=test_purchase.id,
                product_id=product.id,
                product_name=product.name,
                quantity=10.0,
                unit_price=100.0,
                total_price=1000.0
            )
            
            db.session.add(test_item)
            db.session.commit()
            
            print(f"✅ تم إضافة عنصر الفاتورة: {product.name}")
            
            # اختبار الطباعة
            test_print_functionality(test_purchase.id, invoice_number)
            
            return True
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء فاتورة المشتريات: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_print_functionality(purchase_id, invoice_number):
    """اختبار وظيفة الطباعة"""
    print(f"\n🖨️ اختبار وظيفة الطباعة للفاتورة: {invoice_number}")
    print("-" * 40)
    
    try:
        from app import app
        
        with app.app_context():
            # محاكاة طلب الطباعة
            with app.test_client() as client:
                # تسجيل الدخول
                login_response = client.post('/login', data={
                    'username': 'admin',
                    'password': 'admin123'
                })
                
                if login_response.status_code == 302:  # redirect after successful login
                    print("✅ تم تسجيل الدخول للاختبار")
                    
                    # اختبار مسار الطباعة الأساسي
                    print_response = client.get(f'/print_purchase/{purchase_id}')
                    
                    if print_response.status_code == 200:
                        print("✅ مسار الطباعة الأساسي يعمل")
                        
                        # فحص محتوى الاستجابة
                        content = print_response.get_data(as_text=True)
                        if invoice_number in content:
                            print("✅ محتوى الطباعة يحتوي على رقم الفاتورة")
                        else:
                            print("⚠️ محتوى الطباعة قد يكون غير مكتمل")
                            
                    else:
                        print(f"❌ مسار الطباعة الأساسي فشل: {print_response.status_code}")
                    
                    # اختبار المسار البديل
                    alt_response = client.get(f'/purchases/print/{purchase_id}')
                    
                    if alt_response.status_code == 200:
                        print("✅ المسار البديل للطباعة يعمل")
                    else:
                        print(f"❌ المسار البديل فشل: {alt_response.status_code}")
                        
                else:
                    print("❌ فشل تسجيل الدخول للاختبار")
                    
    except Exception as e:
        print(f"❌ خطأ في اختبار الطباعة: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🧪 إنشاء واختبار فاتورة مشتريات للطباعة")
    print("=" * 60)
    
    if add_test_purchase():
        print("\n🎉 تم إنشاء الفاتورة التجريبية بنجاح!")
        
        print("\n📋 الآن يمكنك:")
        print("1. الذهاب إلى: http://localhost:5000/purchases")
        print("2. البحث عن الفاتورة التجريبية")
        print("3. اضغط زر الطباعة (أيقونة الطابعة)")
        print("4. يجب أن تفتح نافذة طباعة جديدة")
        
        print("\n🔧 إذا لم تعمل الطباعة:")
        print("- اضغط F12 وفحص Console للأخطاء")
        print("- تأكد من تفعيل النوافذ المنبثقة")
        print("- جرب الرابط المباشر: http://localhost:5000/print_purchase/1")
        
        print("\n🌟 تم إصلاح:")
        print("✅ مسار الطباعة في JavaScript")
        print("✅ إضافة route بديل للطباعة")
        print("✅ حذف الدوال المكررة")
        print("✅ إضافة تسجيل العمليات")
        
    else:
        print("\n❌ فشل في إنشاء الفاتورة التجريبية")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
