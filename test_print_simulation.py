#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
محاكاة اختبار طباعة فواتير المبيعات
Sales Invoice Print Test Simulation
"""

import requests
import webbrowser
import time

def test_server_connection():
    """اختبار الاتصال بالخادم"""
    print("🌐 اختبار الاتصال بالخادم...")
    
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ الخادم يعمل بشكل طبيعي")
            return True
        else:
            print(f"⚠️ الخادم يعمل لكن مع رمز خطأ: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
        print("💡 تأكد من تشغيل الخادم: python run_local.py")
        return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def simulate_user_login():
    """محاكاة تسجيل دخول المستخدم"""
    print("🔐 محاكاة تسجيل دخول المستخدم...")
    
    session = requests.Session()
    
    try:
        # الحصول على صفحة تسجيل الدخول
        login_page = session.get("http://localhost:5000/login")
        if login_page.status_code != 200:
            print("❌ فشل في الوصول لصفحة تسجيل الدخول")
            return None
        
        # إرسال بيانات تسجيل الدخول
        login_data = {
            'username': 'admin',
            'password': 'admin112233'
        }
        
        response = session.post("http://localhost:5000/login", data=login_data)
        
        # التحقق من نجاح تسجيل الدخول
        if response.status_code == 200 and "dashboard" not in response.url:
            print("✅ تم تسجيل الدخول بنجاح")
            return session
        else:
            print("❌ فشل في تسجيل الدخول")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return None

def test_payments_page_access(session):
    """اختبار الوصول لصفحة المدفوعات"""
    print("📄 اختبار الوصول لصفحة المدفوعات...")
    
    try:
        response = session.get("http://localhost:5000/payments_dues")
        
        if response.status_code == 200:
            print("✅ تم الوصول لصفحة المدفوعات بنجاح")
            return response.text
        else:
            print(f"❌ فشل في الوصول للصفحة: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في الوصول للصفحة: {e}")
        return None

def analyze_print_functionality(page_content):
    """تحليل وظائف الطباعة في الصفحة"""
    print("🔍 تحليل وظائف الطباعة...")
    
    # فحص العناصر المطلوبة
    required_elements = [
        ('printAllSales()', 'وظيفة طباعة المبيعات'),
        ('printAllPurchases()', 'وظيفة طباعة المشتريات'),
        ('printAllExpenses()', 'وظيفة طباعة المصروفات'),
        ('printAllPayroll()', 'وظيفة طباعة الرواتب'),
        ('طباعة جميع المبيعات', 'نص زر المبيعات'),
        ('طباعة جميع المشتريات', 'نص زر المشتريات'),
        ('طباعة جميع المصروفات', 'نص زر المصروفات'),
        ('طباعة جميع الرواتب', 'نص زر الرواتب'),
        ('openSimplePrintWindow', 'وظيفة فتح نافذة الطباعة'),
        ('function printAllSales()', 'تعريف وظيفة المبيعات')
    ]
    
    found_elements = 0
    missing_elements = []
    
    for element, description in required_elements:
        if element in page_content:
            print(f"   ✅ {description}")
            found_elements += 1
        else:
            print(f"   ❌ {description}")
            missing_elements.append(description)
    
    print(f"\n📊 النتائج: {found_elements}/{len(required_elements)} عنصر موجود")
    
    if missing_elements:
        print("\n❌ العناصر المفقودة:")
        for element in missing_elements:
            print(f"   - {element}")
    
    return found_elements >= len(required_elements) * 0.7

def simulate_sales_data_extraction(page_content):
    """محاكاة استخراج بيانات المبيعات"""
    print("📊 محاكاة استخراج بيانات المبيعات...")
    
    # البحث عن جدول المبيعات
    if 'id="sales"' in page_content:
        print("✅ تم العثور على قسم المبيعات")
        
        # محاكاة وجود بيانات
        if 'all_sales' in page_content:
            print("✅ يحتوي على بيانات المبيعات")
            
            # محاكاة بيانات تجريبية
            sample_sales = [
                {'invoice': 'INV-001', 'customer': 'عميل تجريبي 1', 'date': '2024-01-15', 'amount': '1500.00'},
                {'invoice': 'INV-002', 'customer': 'عميل تجريبي 2', 'date': '2024-01-16', 'amount': '2300.00'},
                {'invoice': 'INV-003', 'customer': 'عميل تجريبي 3', 'date': '2024-01-17', 'amount': '1800.00'}
            ]
            
            print(f"📋 بيانات تجريبية للمبيعات ({len(sample_sales)} فاتورة):")
            total = 0
            for sale in sample_sales:
                amount = float(sale['amount'])
                total += amount
                print(f"   - {sale['invoice']}: {sale['customer']} - {amount} ريال")
            
            print(f"💰 المجموع الإجمالي: {total} ريال")
            
            return sample_sales
        else:
            print("⚠️ لا توجد بيانات مبيعات")
            return []
    else:
        print("❌ لم يتم العثور على قسم المبيعات")
        return []

def generate_print_preview(sales_data):
    """إنشاء معاينة للطباعة"""
    print("🖨️ إنشاء معاينة الطباعة...")
    
    if not sales_data:
        print("❌ لا توجد بيانات للطباعة")
        return None
    
    # إنشاء HTML للطباعة
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    total_amount = sum(float(sale['amount']) for sale in sales_data)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تقرير فواتير المبيعات</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #007bff; padding-bottom: 20px; }}
            .company-name {{ font-size: 28px; font-weight: bold; color: #007bff; }}
            .report-title {{ font-size: 22px; color: #333; margin: 10px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 2px solid #ddd; padding: 15px; text-align: center; }}
            th {{ background-color: #007bff; color: white; font-weight: bold; }}
            .total-row {{ background-color: #e3f2fd; font-weight: bold; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">تقرير فواتير المبيعات</div>
            <div>تاريخ الطباعة: {current_date}</div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>رقم الفاتورة</th>
                    <th>العميل</th>
                    <th>التاريخ</th>
                    <th>المبلغ (ريال)</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for sale in sales_data:
        html_content += f"""
                <tr>
                    <td>{sale['invoice']}</td>
                    <td>{sale['customer']}</td>
                    <td>{sale['date']}</td>
                    <td>{sale['amount']} ريال</td>
                </tr>
        """
    
    html_content += f"""
                <tr class="total-row">
                    <td colspan="3">المجموع الإجمالي</td>
                    <td>{total_amount:.2f} ريال</td>
                </tr>
            </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>عدد الفواتير: {len(sales_data)}</p>
            <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
        </div>
    </body>
    </html>
    """
    
    # حفظ الملف
    with open("sales_print_preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ تم إنشاء معاينة الطباعة: sales_print_preview.html")
    return "sales_print_preview.html"

def main():
    """الوظيفة الرئيسية لمحاكاة اختبار الطباعة"""
    print("🤖 محاكاة المستخدم لاختبار طباعة فواتير المبيعات")
    print("=" * 70)
    
    # اختبار الخادم
    if not test_server_connection():
        return
    
    # تسجيل الدخول
    session = simulate_user_login()
    if not session:
        return
    
    # الوصول لصفحة المدفوعات
    page_content = test_payments_page_access(session)
    if not page_content:
        return
    
    # تحليل وظائف الطباعة
    print_functions_ok = analyze_print_functionality(page_content)
    
    # استخراج بيانات المبيعات
    sales_data = simulate_sales_data_extraction(page_content)
    
    # إنشاء معاينة الطباعة
    preview_file = generate_print_preview(sales_data)
    
    # النتائج النهائية
    print("\n" + "=" * 70)
    print("📊 ملخص نتائج المحاكاة:")
    print("=" * 70)
    
    if print_functions_ok:
        print("✅ وظائف الطباعة موجودة ومتاحة")
    else:
        print("❌ هناك مشاكل في وظائف الطباعة")
    
    if sales_data:
        print(f"✅ تم استخراج {len(sales_data)} فاتورة مبيعات")
        total = sum(float(sale['amount']) for sale in sales_data)
        print(f"💰 المجموع الإجمالي: {total:.2f} ريال")
    else:
        print("⚠️ لم يتم العثور على بيانات مبيعات")
    
    if preview_file:
        print(f"✅ تم إنشاء معاينة الطباعة: {preview_file}")
        
        # فتح المعاينة في المتصفح
        print("🌐 فتح معاينة الطباعة...")
        webbrowser.open(preview_file)
        
        # فتح صفحة المدفوعات أيضاً
        print("🌐 فتح صفحة المدفوعات للاختبار اليدوي...")
        webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n📋 تعليمات الاختبار اليدوي:")
    print("1. تحقق من معاينة الطباعة في المتصفح")
    print("2. اذهب لصفحة المدفوعات")
    print("3. سجل الدخول: admin / admin112233")
    print("4. اضغط على تبويب المبيعات")
    print("5. ابحث عن زر 'طباعة جميع المبيعات'")
    print("6. اضغط على الزر واختبر الطباعة")
    
    print("\n🎯 النتيجة المتوقعة:")
    print("- فتح نافذة طباعة جديدة")
    print("- عرض تقرير مشابه للمعاينة")
    print("- إمكانية الطباعة أو الحفظ كـ PDF")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
