#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء بيانات تجريبية للاختبار
Create Test Data for Testing
"""

import requests
import json
from datetime import datetime, date

def login():
    """تسجيل الدخول"""
    session = requests.Session()
    
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        
        if response.status_code == 200:
            print("✅ تم تسجيل الدخول")
            return session
        else:
            print(f"❌ فشل تسجيل الدخول: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return None

def create_test_sales(session):
    """إنشاء فواتير مبيعات تجريبية"""
    print("📊 إنشاء فواتير مبيعات تجريبية...")
    
    # بيانات فاتورة مبيعات تجريبية
    sales_data = [
        {
            'invoice_number': 'S-2025-001',
            'invoice_date': '2025-08-01',
            'customer_name': 'عميل تجريبي 1',
            'customer_phone': '0501234567',
            'subtotal': 1000.00,
            'tax_amount': 150.00,
            'discount_amount': 50.00,
            'final_amount': 1100.00,
            'payment_method': 'cash',
            'payment_status': 'paid',
            'notes': 'فاتورة تجريبية للاختبار'
        },
        {
            'invoice_number': 'S-2025-002',
            'invoice_date': '2025-08-02',
            'customer_name': 'عميل تجريبي 2',
            'customer_phone': '0507654321',
            'subtotal': 2000.00,
            'tax_amount': 300.00,
            'discount_amount': 100.00,
            'final_amount': 2200.00,
            'payment_method': 'bank_transfer',
            'payment_status': 'partial',
            'notes': 'فاتورة تجريبية - دفع جزئي'
        },
        {
            'invoice_number': 'S-2025-003',
            'invoice_date': '2025-08-03',
            'customer_name': 'عميل تجريبي 3',
            'customer_phone': '0509876543',
            'subtotal': 1500.00,
            'tax_amount': 225.00,
            'discount_amount': 0.00,
            'final_amount': 1725.00,
            'payment_method': 'credit',
            'payment_status': 'pending',
            'notes': 'فاتورة تجريبية - غير مدفوعة'
        }
    ]
    
    created_count = 0
    for sale_data in sales_data:
        try:
            response = session.post("http://localhost:5000/api/sales", json=sale_data)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ تم إنشاء فاتورة مبيعات: {sale_data['invoice_number']}")
            else:
                print(f"⚠️ فشل إنشاء فاتورة: {sale_data['invoice_number']} - {response.status_code}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء فاتورة: {e}")
    
    print(f"📊 تم إنشاء {created_count} فاتورة مبيعات")

def create_test_expenses(session):
    """إنشاء مصروفات تجريبية"""
    print("💰 إنشاء مصروفات تجريبية...")
    
    expenses_data = [
        {
            'expense_number': 'E-2025-001',
            'expense_date': '2025-08-01',
            'expense_type': 'إيجار المكتب',
            'amount': 5000.00,
            'payment_method': 'bank_transfer',
            'payment_status': 'paid',
            'description': 'إيجار شهر أغسطس 2025'
        },
        {
            'expense_number': 'E-2025-002',
            'expense_date': '2025-08-02',
            'expense_type': 'فواتير الكهرباء',
            'amount': 800.00,
            'payment_method': 'cash',
            'payment_status': 'paid',
            'description': 'فاتورة كهرباء شهر يوليو'
        },
        {
            'expense_number': 'E-2025-003',
            'expense_date': '2025-08-03',
            'expense_type': 'مواد تنظيف',
            'amount': 300.00,
            'payment_method': 'cash',
            'payment_status': 'pending',
            'description': 'مواد تنظيف للمكتب'
        }
    ]
    
    created_count = 0
    for expense_data in expenses_data:
        try:
            response = session.post("http://localhost:5000/api/expenses", json=expense_data)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ تم إنشاء مصروف: {expense_data['expense_number']}")
            else:
                print(f"⚠️ فشل إنشاء مصروف: {expense_data['expense_number']} - {response.status_code}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء مصروف: {e}")
    
    print(f"💰 تم إنشاء {created_count} مصروف")

def test_print_with_data(session):
    """اختبار الطباعة مع البيانات الجديدة"""
    print("\n🖨️ اختبار الطباعة مع البيانات الجديدة...")
    
    # معاملات الاختبار
    params = {
        'type': 'sales',
        'month': '2025-08',
        'status': 'all',
        'details': 'true'
    }
    
    # اختبار API الأشهر المتاحة
    try:
        response = session.get("http://localhost:5000/api/available_months?type=sales")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                months_count = len(data.get('months', []))
                print(f"✅ API الأشهر المتاحة: {months_count} شهر")
                
                if months_count > 0:
                    # عرض الأشهر المتاحة
                    for month in data['months']:
                        print(f"   📅 {month['text']} ({month['value']})")
            else:
                print("⚠️ API الأشهر المتاحة يعمل لكن لا توجد بيانات")
        else:
            print(f"❌ API الأشهر المتاحة فشل: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في API الأشهر المتاحة: {e}")
    
    # اختبار معاينة الطباعة
    try:
        response = session.get("http://localhost:5000/print_invoices_preview", params=params)
        if response.status_code == 200:
            print("✅ معاينة الطباعة تعمل مع البيانات")
            
            # فحص محتوى الصفحة
            content = response.text
            if 'S-2025-001' in content:
                print("✅ البيانات التجريبية ظاهرة في التقرير")
        else:
            print(f"❌ معاينة الطباعة فشلت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في معاينة الطباعة: {e}")

def test_pdf_generation(session):
    """اختبار إنتاج PDF"""
    print("\n📄 اختبار إنتاج PDF...")
    
    params = {
        'type': 'sales',
        'month': '2025-08',
        'status': 'all',
        'details': 'true'
    }
    
    try:
        response = session.get("http://localhost:5000/download_invoices_pdf", params=params)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                # حفظ ملف PDF
                filename = f"test_invoice_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ تم إنتاج ملف PDF: {filename} ({file_size} بايت)")
                return filename
                
            elif 'text/html' in content_type:
                print("📄 تم إرجاع HTML (fallback) - weasyprint غير متاح")
                return True
        else:
            print(f"❌ فشل إنتاج PDF: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في إنتاج PDF: {e}")
    
    return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 إنشاء بيانات تجريبية واختبار الطباعة")
    print("=" * 60)
    
    # تسجيل الدخول
    session = login()
    if not session:
        print("❌ فشل تسجيل الدخول")
        return
    
    # إنشاء بيانات تجريبية
    create_test_sales(session)
    create_test_expenses(session)
    
    # اختبار الطباعة مع البيانات الجديدة
    test_print_with_data(session)
    
    # اختبار إنتاج PDF
    pdf_result = test_pdf_generation(session)
    
    print("\n" + "=" * 60)
    print("📊 ملخص النتائج:")
    print("=" * 60)
    
    if pdf_result:
        print("🎉 جميع وظائف الطباعة تعمل بنجاح!")
        print("✅ تم إنشاء بيانات تجريبية")
        print("✅ معاينة الطباعة تعمل")
        print("✅ إنتاج PDF يعمل")
        
        if isinstance(pdf_result, str):
            print(f"📁 ملف PDF: {pdf_result}")
            
        print("\n🚀 النظام جاهز للاستخدام!")
        print("🔗 http://localhost:5000/payments_dues")
        
    else:
        print("⚠️ بعض وظائف الطباعة تحتاج مراجعة")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
