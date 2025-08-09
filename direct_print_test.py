#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار مباشر لوظائف الطباعة
Direct Print Functions Test
"""

import requests
import webbrowser
import time

def test_direct_print():
    """اختبار مباشر لوظائف الطباعة"""
    print("🖨️ اختبار مباشر لوظائف الطباعة")
    print("=" * 50)
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل - تشغيل الخادم...")
        import subprocess
        subprocess.Popen(["python", "run_local.py"], cwd="D:/New folder/ACCOUNTS PROGRAM")
        time.sleep(5)
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return False
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            print("✅ تم الوصول لصفحة المدفوعات")
            
            # فحص مفصل للمحتوى
            print("\n🔍 فحص مفصل للمحتوى:")
            
            # البحث عن الأزرار
            if "printAllSales" in content:
                print("   ✅ وظيفة printAllSales موجودة")
            else:
                print("   ❌ وظيفة printAllSales غير موجودة")
            
            if "طباعة جميع المبيعات" in content:
                print("   ✅ نص زر المبيعات موجود")
            else:
                print("   ❌ نص زر المبيعات غير موجود")
            
            # البحث عن JavaScript
            if "function printAllSales()" in content:
                print("   ✅ تعريف وظيفة JavaScript موجود")
            else:
                print("   ❌ تعريف وظيفة JavaScript غير موجود")
            
            # فحص HTML للأزرار
            button_patterns = [
                'onclick="printAllSales()"',
                'onclick="printAllPurchases()"',
                'onclick="printAllExpenses()"',
                'onclick="printAllPayroll()"'
            ]
            
            print("\n🔍 فحص أزرار HTML:")
            for pattern in button_patterns:
                if pattern in content:
                    print(f"   ✅ {pattern}")
                else:
                    print(f"   ❌ {pattern}")
            
            # حفظ جزء من المحتوى للفحص
            with open("page_content_debug.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("\n💾 تم حفظ محتوى الصفحة في: page_content_debug.html")
            
            return True
        else:
            print(f"❌ فشل في الوصول للصفحة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def create_working_print_demo():
    """إنشاء عرض توضيحي للطباعة"""
    print("\n🎯 إنشاء عرض توضيحي للطباعة...")
    
    # بيانات تجريبية
    demo_sales = [
        {"invoice": "INV-2024-001", "customer": "شركة الأمل التجارية", "date": "2024-01-15", "amount": "2500.00"},
        {"invoice": "INV-2024-002", "customer": "مؤسسة النور للتجارة", "date": "2024-01-16", "amount": "1800.00"},
        {"invoice": "INV-2024-003", "customer": "شركة الفجر الجديد", "date": "2024-01-17", "amount": "3200.00"},
        {"invoice": "INV-2024-004", "customer": "مكتب الرياض للاستشارات", "date": "2024-01-18", "amount": "1500.00"},
        {"invoice": "INV-2024-005", "customer": "عميل نقدي", "date": "2024-01-19", "amount": "950.00"}
    ]
    
    total_amount = sum(float(sale["amount"]) for sale in demo_sales)
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # إنشاء HTML للطباعة
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تقرير فواتير المبيعات - عرض توضيحي</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                direction: rtl;
                margin: 20px;
                background: white;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 4px solid #007bff;
                padding-bottom: 25px;
            }}
            .company-name {{
                font-size: 32px;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 15px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }}
            .report-title {{
                font-size: 24px;
                color: #333;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            .print-date {{
                color: #666;
                font-size: 16px;
                font-style: italic;
            }}
            .summary-box {{
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                border: 2px solid #007bff;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }}
            .summary-title {{
                font-size: 20px;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 10px;
            }}
            .summary-stats {{
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }}
            .stat-item {{
                margin: 10px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}
            .stat-label {{
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 30px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 18px 12px;
                text-align: center;
                font-size: 15px;
            }}
            th {{
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                font-weight: bold;
                font-size: 16px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #e3f2fd;
                transition: background-color 0.3s ease;
            }}
            .total-row {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
                color: white !important;
                font-weight: bold;
                font-size: 18px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}
            .footer {{
                text-align: center;
                margin-top: 50px;
                padding-top: 30px;
                border-top: 3px solid #007bff;
                color: #666;
                font-size: 14px;
            }}
            .footer-logo {{
                font-size: 18px;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 10px;
            }}
            @media print {{
                body {{ margin: 0; }}
                .no-print {{ display: none !important; }}
            }}
            .print-button {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #007bff;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }}
            .print-button:hover {{
                background: #0056b3;
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            }}
        </style>
    </head>
    <body>
        <button class="print-button no-print" onclick="window.print()">
            🖨️ طباعة التقرير
        </button>
        
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">تقرير فواتير المبيعات</div>
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
        </div>
        
        <div class="summary-box">
            <div class="summary-title">ملخص المبيعات</div>
            <div class="summary-stats">
                <div class="stat-item">
                    <div class="stat-number">{len(demo_sales)}</div>
                    <div class="stat-label">عدد الفواتير</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_amount:,.2f}</div>
                    <div class="stat-label">إجمالي المبيعات (ريال)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_amount/len(demo_sales):,.2f}</div>
                    <div class="stat-label">متوسط الفاتورة (ريال)</div>
                </div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>رقم الفاتورة</th>
                    <th>اسم العميل</th>
                    <th>تاريخ الفاتورة</th>
                    <th>المبلغ (ريال)</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # إضافة صفوف البيانات
    for i, sale in enumerate(demo_sales, 1):
        html_content += f"""
                <tr>
                    <td><strong>{sale['invoice']}</strong></td>
                    <td>{sale['customer']}</td>
                    <td>{sale['date']}</td>
                    <td>{float(sale['amount']):,.2f} ريال</td>
                </tr>
        """
    
    # إضافة صف المجموع
    html_content += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{total_amount:,.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            <div class="footer-logo">نظام المحاسبة المتكامل</div>
            <p>تم إنشاء هذا التقرير تلقائياً بواسطة النظام</p>
            <p>للاستفسارات والدعم الفني: support@accounting-system.com</p>
            <p><strong>هذا عرض توضيحي لوظيفة طباعة فواتير المبيعات</strong></p>
        </div>
        
        <script>
            // طباعة تلقائية بعد التحميل
            window.onload = function() {{
                setTimeout(function() {{
                    if (confirm('هل تريد طباعة التقرير الآن؟')) {{
                        window.print();
                    }}
                }}, 1000);
            }};
        </script>
    </body>
    </html>
    """
    
    # حفظ الملف
    filename = "sales_print_demo.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ تم إنشاء العرض التوضيحي: {filename}")
    
    # فتح في المتصفح
    webbrowser.open(filename)
    
    return filename

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار مباشر ومحاكاة طباعة فواتير المبيعات")
    print("=" * 70)
    
    # اختبار مباشر
    test_result = test_direct_print()
    
    # إنشاء عرض توضيحي
    demo_file = create_working_print_demo()
    
    # فتح صفحة المدفوعات للمقارنة
    print("\n🌐 فتح صفحة المدفوعات للمقارنة...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 70)
    print("📊 ملخص النتائج:")
    print("=" * 70)
    
    if test_result:
        print("✅ تم الوصول لصفحة المدفوعات بنجاح")
    else:
        print("❌ مشكلة في الوصول لصفحة المدفوعات")
    
    print(f"✅ تم إنشاء عرض توضيحي للطباعة: {demo_file}")
    print("✅ تم فتح العرض التوضيحي في المتصفح")
    print("✅ تم فتح صفحة المدفوعات للمقارنة")
    
    print("\n📋 تعليمات المقارنة:")
    print("1. قارن بين العرض التوضيحي وصفحة المدفوعات")
    print("2. ابحث عن أزرار الطباعة في صفحة المدفوعات")
    print("3. اختبر وظيفة الطباعة إذا كانت متاحة")
    print("4. تحقق من ملف page_content_debug.html للتشخيص")
    
    print("\n🎯 هذا ما يجب أن تراه:")
    print("- أزرار طباعة في كل تبويب")
    print("- وظائف JavaScript للطباعة")
    print("- فتح نوافذ طباعة عند الضغط على الأزرار")
    print("- تقارير مشابهة للعرض التوضيحي")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
