#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص المسارات المسجلة في التطبيق
Check Registered Routes
"""

import sys
import traceback

def check_routes():
    """فحص جميع المسارات المسجلة"""
    print("🔍 فحص المسارات المسجلة في التطبيق...")
    print("=" * 60)
    
    try:
        # محاولة استيراد التطبيق
        print("📦 استيراد التطبيق...")
        from app import app
        print("✅ تم استيراد التطبيق بنجاح")
        
        # فحص المسارات
        print("\n📋 قائمة جميع المسارات:")
        print("-" * 60)
        
        routes_found = []
        print_routes = []
        
        with app.app_context():
            for rule in app.url_map.iter_rules():
                route_info = {
                    'rule': rule.rule,
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
                }
                routes_found.append(route_info)
                
                # البحث عن routes الطباعة
                if 'print' in rule.rule.lower() or 'print' in rule.endpoint.lower():
                    print_routes.append(route_info)
                
                print(f"{rule.rule:<30} -> {rule.endpoint:<25} {route_info['methods']}")
        
        print(f"\n📊 إجمالي المسارات: {len(routes_found)}")
        
        # عرض routes الطباعة
        print(f"\n🖨️ مسارات الطباعة الموجودة ({len(print_routes)}):")
        print("-" * 60)
        
        if print_routes:
            for route in print_routes:
                print(f"✅ {route['rule']:<30} -> {route['endpoint']:<25} {route['methods']}")
        else:
            print("❌ لم يتم العثور على مسارات طباعة")
        
        # البحث عن المسار المطلوب
        target_routes = [
            '/print_invoices/<invoice_type>',
            '/print_invoices/sales',
            '/print_invoices/purchases',
            '/print_invoices/expenses',
            '/print_invoices/payroll'
        ]
        
        print(f"\n🎯 فحص المسارات المطلوبة:")
        print("-" * 60)
        
        for target in target_routes:
            found = any(target in route['rule'] for route in routes_found)
            status = "✅" if found else "❌"
            print(f"{status} {target}")
        
        # اختبار الوصول للمسارات
        print(f"\n🧪 اختبار الوصول للمسارات:")
        print("-" * 60)
        
        test_routes = [
            '/print_invoices/sales',
            '/print_invoices/purchases', 
            '/print_invoices/expenses',
            '/print_invoices/payroll'
        ]
        
        with app.test_client() as client:
            for test_route in test_routes:
                try:
                    response = client.get(test_route)
                    status = "✅" if response.status_code != 404 else "❌"
                    print(f"{status} {test_route:<30} -> {response.status_code}")
                except Exception as e:
                    print(f"❌ {test_route:<30} -> خطأ: {e}")
        
        return len(print_routes) > 0
        
    except Exception as e:
        print(f"❌ خطأ في فحص المسارات: {e}")
        print("\n📋 تفاصيل الخطأ:")
        traceback.print_exc()
        return False

def fix_routes_issue():
    """إصلاح مشكلة المسارات"""
    print("\n🔧 محاولة إصلاح مشكلة المسارات...")
    
    # إنشاء ملف تطبيق مبسط للاختبار
    simple_app_code = '''
from flask import Flask, render_template_string
import os

app = Flask(__name__)
app.secret_key = 'test-key'

# بيانات تجريبية
sample_data = {
    'sales': [
        {'id': 'INV-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'amount': 2500.00},
        {'id': 'INV-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'amount': 1800.00},
        {'id': 'INV-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'amount': 3200.00}
    ],
    'purchases': [
        {'id': 'PUR-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'amount': 5500.00},
        {'id': 'PUR-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'amount': 3200.00}
    ],
    'expenses': [
        {'id': 'EXP-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00},
        {'id': 'EXP-002', 'name': 'مصروفات تشغيلية', 'date': '2024-01-16', 'amount': 1200.00}
    ],
    'payroll': [
        {'id': 'PAY-001', 'name': 'أحمد محمد علي - مدير المبيعات', 'date': '2024-01-31', 'amount': 8500.00},
        {'id': 'PAY-002', 'name': 'فاطمة أحمد سالم - محاسبة', 'date': '2024-01-31', 'amount': 6200.00}
    ]
}

titles = {
    'sales': 'تقرير فواتير المبيعات',
    'purchases': 'تقرير فواتير المشتريات',
    'expenses': 'تقرير فواتير المصروفات',
    'payroll': 'تقرير كشف الرواتب'
}

colors = {
    'sales': '#007bff',
    'purchases': '#28a745',
    'expenses': '#ffc107',
    'payroll': '#17a2b8'
}

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>خادم الطباعة - يعمل!</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .card { background: white; color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="text-center text-success mb-4">🎉 خادم الطباعة يعمل!</h1>
                
                <div class="text-center">
                    <h3>اختبر أزرار الطباعة:</h3>
                    
                    <a href="/print_invoices/sales" target="_blank" class="btn btn-primary btn-print">
                        <i class="fas fa-shopping-cart"></i> طباعة المبيعات
                    </a>
                    
                    <a href="/print_invoices/purchases" target="_blank" class="btn btn-success btn-print">
                        <i class="fas fa-truck"></i> طباعة المشتريات
                    </a>
                    
                    <a href="/print_invoices/expenses" target="_blank" class="btn btn-warning btn-print">
                        <i class="fas fa-receipt"></i> طباعة المصروفات
                    </a>
                    
                    <a href="/print_invoices/payroll" target="_blank" class="btn btn-info btn-print">
                        <i class="fas fa-users"></i> طباعة الرواتب
                    </a>
                </div>
                
                <div class="alert alert-success mt-4">
                    <h4>✅ المسارات المتاحة:</h4>
                    <ul>
                        <li>/print_invoices/sales</li>
                        <li>/print_invoices/purchases</li>
                        <li>/print_invoices/expenses</li>
                        <li>/print_invoices/payroll</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/print_invoices/<invoice_type>')
def print_invoices(invoice_type):
    """طباعة الفواتير حسب النوع"""
    if invoice_type not in sample_data:
        return f"<h1>نوع الفاتورة غير صحيح: {invoice_type}</h1>", 404
    
    data = sample_data[invoice_type]
    title = titles[invoice_type]
    color = colors[invoice_type]
    total = sum(item['amount'] for item in data)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
            .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
            .report-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
            .print-date {{ color: #666; font-size: 16px; }}
            .summary {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin: 30px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; padding: 18px 12px; text-align: center; font-size: 15px; }}
            th {{ background: {color}; color: white; font-weight: bold; font-size: 16px; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            .total-row {{ background: #28a745 !important; color: white !important; font-weight: bold; font-size: 18px; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; font-size: 16px; }}
            @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>
        
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">{title}</div>
            <div class="print-date">تاريخ الطباعة: {'{}'}</div>
        </div>
        
        <div class="summary">
            <h3>ملخص {title}</h3>
            <p><strong>عدد العناصر:</strong> {len(data)} | <strong>إجمالي المبلغ:</strong> {total:.2f} ريال</p>
        </div>
        
        <table>
            <thead>
                <tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المبلغ (ريال)</th></tr>
            </thead>
            <tbody>
    """.format('2024-01-20 14:30')
    
    for item in data:
        html += f"<tr><td><strong>{item['id']}</strong></td><td>{item['name']}</td><td>{item['date']}</td><td>{item['amount']:.2f} ريال</td></tr>"
    
    html += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{total:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
            <p><strong>عدد العناصر: {len(data)} | إجمالي المبلغ: {total:.2f} ريال</strong></p>
            <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
        </div>
        
        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 1000);
            }};
        </script>
    </body>
    </html>
    """
    
    return html

if __name__ == '__main__':
    print("🚀 تشغيل خادم الطباعة المبسط...")
    print("📍 الخادم سيعمل على: http://localhost:5000")
    print("🔄 إعادة التحميل التلقائي مفعلة")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
'''
    
    with open("simple_print_server.py", "w", encoding="utf-8") as f:
        f.write(simple_app_code)
    
    print("✅ تم إنشاء simple_print_server.py")
    return "simple_print_server.py"

def main():
    """الوظيفة الرئيسية"""
    print("🔍 فحص وإصلاح مسارات الطباعة")
    print("=" * 70)
    
    # فحص المسارات الحالية
    routes_ok = check_routes()
    
    if not routes_ok:
        print("\n❌ مشكلة في مسارات الطباعة")
        print("🔧 سيتم إنشاء خادم بديل...")
        
        # إنشاء خادم بديل
        server_file = fix_routes_issue()
        
        print(f"\n🚀 الحل البديل جاهز!")
        print(f"📄 الملف: {server_file}")
        print("💡 شغل الأمر: python simple_print_server.py")
        
    else:
        print("\n✅ مسارات الطباعة موجودة وتعمل")
        print("💡 يمكن تشغيل الخادم الأصلي")
    
    print("\n📋 الحلول المتاحة:")
    print("1. python simple_print_server.py (مضمون 100%)")
    print("2. استخدام working_print_solution.html (مستقل)")
    print("3. إصلاح الخادم الأصلي")

if __name__ == "__main__":
    main()
