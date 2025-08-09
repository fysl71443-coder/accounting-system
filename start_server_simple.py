#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل خادم بسيط للطباعة
Simple Print Server Startup
"""

from flask import Flask, render_template_string
import webbrowser
import time
import threading

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'simple-print-key'

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
    """الصفحة الرئيسية"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>نظام الطباعة - يعمل!</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
            .card { background: white; color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="text-center text-success mb-4">🎉 نظام الطباعة يعمل!</h1>
                
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
                    <h4>✅ الأزرار تعمل الآن!</h4>
                    <p>اضغط على أي زر لاختبار الطباعة</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/print_invoices/<invoice_type>')
def print_invoice(invoice_type):
    """طباعة الفواتير"""
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
            table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 15px; text-align: center; }}
            th {{ background: {color}; color: white; }}
            .total {{ background: #f0f0f0; font-weight: bold; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ طباعة</button>
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">{title}</div>
        </div>
        <table>
            <thead>
                <tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المبلغ</th></tr>
            </thead>
            <tbody>
    """
    
    for item in data:
        html += f"<tr><td>{item['id']}</td><td>{item['name']}</td><td>{item['date']}</td><td>{item['amount']:.2f} ريال</td></tr>"
    
    html += f"""
                <tr class="total"><td colspan="3">المجموع الإجمالي</td><td>{total:.2f} ريال</td></tr>
            </tbody>
        </table>
        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 1000);
            }};
        </script>
    </body>
    </html>
    """
    
    return html

def open_browser():
    """فتح المتصفح بعد تشغيل الخادم"""
    time.sleep(2)
    webbrowser.open("http://localhost:5000")

if __name__ == '__main__':
    print("🚀 تشغيل خادم الطباعة البسيط...")
    print("📍 الخادم سيعمل على: http://localhost:5000")
    print("🖨️ أزرار الطباعة جاهزة")
    print("=" * 50)
    
    # فتح المتصفح في thread منفصل
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # تشغيل الخادم
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
