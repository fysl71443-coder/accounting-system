#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة موردين تجريبيين لقاعدة البيانات
Add Sample Suppliers to Database
"""

import sys
import os
from datetime import datetime

# إضافة المسار الحالي لـ Python path
sys.path.insert(0, os.getcwd())

def add_sample_suppliers():
    """إضافة موردين تجريبيين"""
    try:
        from app import app, db, Supplier
        
        with app.app_context():
            print("🔍 فحص الموردين الموجودين...")
            
            existing_suppliers = Supplier.query.count()
            print(f"📊 عدد الموردين الحاليين: {existing_suppliers}")
            
            if existing_suppliers == 0:
                print("➕ إضافة موردين تجريبيين...")
                
                # قائمة الموردين التجريبيين
                sample_suppliers = [
                    {
                        'name': 'شركة المواد الغذائية المتحدة',
                        'phone': '0112345678',
                        'email': 'info@foodunited.com',
                        'address': 'الرياض، المملكة العربية السعودية',
                        'tax_number': '300123456789003',
                        'contact_person': 'أحمد محمد',
                        'credit_limit': 50000.0
                    },
                    {
                        'name': 'مؤسسة الخضار والفواكه',
                        'phone': '0113456789',
                        'email': 'sales@freshveggies.com',
                        'address': 'جدة، المملكة العربية السعودية',
                        'tax_number': '300234567890003',
                        'contact_person': 'فاطمة أحمد',
                        'credit_limit': 25000.0
                    },
                    {
                        'name': 'شركة اللحوم الطازجة',
                        'phone': '0114567890',
                        'email': 'orders@freshmeat.com',
                        'address': 'الدمام، المملكة العربية السعودية',
                        'tax_number': '300345678901003',
                        'contact_person': 'محمد علي',
                        'credit_limit': 75000.0
                    },
                    {
                        'name': 'مصنع الألبان الذهبية',
                        'phone': '0115678901',
                        'email': 'info@goldendairy.com',
                        'address': 'الطائف، المملكة العربية السعودية',
                        'tax_number': '300456789012003',
                        'contact_person': 'سارة خالد',
                        'credit_limit': 40000.0
                    },
                    {
                        'name': 'شركة التوابل والبهارات',
                        'phone': '0116789012',
                        'email': 'sales@spicescompany.com',
                        'address': 'مكة المكرمة، المملكة العربية السعودية',
                        'tax_number': '300567890123003',
                        'contact_person': 'عبدالله حسن',
                        'credit_limit': 30000.0
                    },
                    {
                        'name': 'مؤسسة المواد التنظيف',
                        'phone': '0117890123',
                        'email': 'info@cleaningsupplies.com',
                        'address': 'المدينة المنورة، المملكة العربية السعودية',
                        'tax_number': '300678901234003',
                        'contact_person': 'نورا عبدالرحمن',
                        'credit_limit': 20000.0
                    }
                ]
                
                # إضافة الموردين
                added_count = 0
                for supplier_data in sample_suppliers:
                    try:
                        supplier = Supplier(
                            name=supplier_data['name'],
                            phone=supplier_data['phone'],
                            email=supplier_data['email'],
                            address=supplier_data['address'],
                            tax_number=supplier_data['tax_number'],
                            contact_person=supplier_data['contact_person'],
                            credit_limit=supplier_data['credit_limit'],
                            is_active=True,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        
                        db.session.add(supplier)
                        added_count += 1
                        print(f"   ✅ تم إضافة: {supplier_data['name']}")
                        
                    except Exception as e:
                        print(f"   ❌ خطأ في إضافة {supplier_data['name']}: {e}")
                
                # حفظ التغييرات
                try:
                    db.session.commit()
                    print(f"\n✅ تم إضافة {added_count} مورد بنجاح!")
                    
                    # التحقق من الإضافة
                    total_suppliers = Supplier.query.count()
                    print(f"📊 إجمالي الموردين الآن: {total_suppliers}")
                    
                    # عرض قائمة الموردين
                    print(f"\n📋 قائمة الموردين:")
                    suppliers = Supplier.query.all()
                    for supplier in suppliers:
                        print(f"   🏢 {supplier.name} - {supplier.phone}")
                    
                except Exception as e:
                    print(f"❌ خطأ في حفظ البيانات: {e}")
                    db.session.rollback()
                    return False
                    
            else:
                print("✅ يوجد موردين في قاعدة البيانات بالفعل")
                
                # عرض الموردين الموجودين
                print(f"\n📋 الموردين الموجودين:")
                suppliers = Supplier.query.all()
                for supplier in suppliers:
                    status = "نشط" if supplier.is_active else "غير نشط"
                    print(f"   🏢 {supplier.name} - {supplier.phone} ({status})")
            
            return True
            
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        import traceback
        print(f"📋 التفاصيل: {traceback.format_exc()}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🏢 إضافة موردين تجريبيين - Add Sample Suppliers")
    print("=" * 60)
    
    success = add_sample_suppliers()
    
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
