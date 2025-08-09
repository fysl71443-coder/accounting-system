#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>نظام الفواتير مع الخصم</title>
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
                <h1 class="text-center text-success mb-4">🎉 نظام الفواتير مع خانات الخصم يعمل!</h1>
                
                <div class="text-center">
                    <h3>اختبر الفواتير مع الخصم:</h3>
                    
                    <a href="/print_invoices/sales" target="_blank" class="btn btn-primary btn-print">
                        💰 طباعة المبيعات مع الخصم
                    </a>
                    
                    <a href="/print_invoices/purchases" target="_blank" class="btn btn-success btn-print">
                        💰 طباعة المشتريات مع الخصم
                    </a>
                    
                    <a href="/payments_dues" class="btn btn-info btn-print">
                        💳 صفحة المدفوعات والمستحقات
                    </a>
                </div>
                
                <div class="alert alert-success mt-4">
                    <h4>✅ الميزات الجديدة:</h4>
                    <ul>
                        <li>✅ خانة المجموع الفرعي</li>
                        <li>✅ خانة الخصم</li>
                        <li>✅ المبلغ النهائي بعد الخصم</li>
                        <li>✅ حساب إجمالي الخصومات</li>
                        <li>✅ عرض المبلغ الموفر</li>
                        <li>✅ تصميم محسن للطباعة</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/payments_dues')
def payments_dues():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>المدفوعات والمستحقات</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: #f8f9fa; padding: 20px; }
            .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; text-align: center; }
            .print-section { background: white; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-header">
                <h1>💳 المدفوعات والمستحقات</h1>
                <p>نظام إدارة المدفوعات مع خانات الخصم</p>
            </div>
            
            <div class="print-section">
                <h3 class="text-center mb-4">🖨️ أزرار الطباعة مع الخصم</h3>
                
                <div class="row text-center">
                    <div class="col-md-6 mb-3">
                        <a href="/print_invoices/sales" class="btn btn-primary btn-print w-100" target="_blank">
                            💰 طباعة المبيعات مع الخصم
                        </a>
                    </div>
                    <div class="col-md-6 mb-3">
                        <a href="/print_invoices/purchases" class="btn btn-success btn-print w-100" target="_blank">
                            💰 طباعة المشتريات مع الخصم
                        </a>
                    </div>
                </div>
                
                <div class="alert alert-info">
                    <strong>✅ الميزات الجديدة:</strong> خانات الخصم متاحة الآن في فواتير المبيعات والمشتريات مع حساب المبلغ الموفر!
                </div>
            </div>
            
            <div class="text-center">
                <a href="/" class="btn btn-outline-primary">🏠 العودة للرئيسية</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/print_invoices/<invoice_type>')
def print_invoice(invoice_type):
    data = {
        'sales': [
            {'id': 'INV-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'subtotal': 2700.00, 'discount': 200.00, 'amount': 2500.00},
            {'id': 'INV-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'subtotal': 2000.00, 'discount': 200.00, 'amount': 1800.00},
            {'id': 'INV-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00}
        ],
        'purchases': [
            {'id': 'PUR-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'subtotal': 6000.00, 'discount': 500.00, 'amount': 5500.00},
            {'id': 'PUR-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00}
        ]
    }
    
    if invoice_type not in data:
        return f"<h1>نوع الفاتورة غير صحيح: {invoice_type}</h1>", 404
    
    items = data[invoice_type]
    title = f"تقرير فواتير {invoice_type}"
    color = '#007bff' if invoice_type == 'sales' else '#28a745'
    
    subtotal = sum(item['subtotal'] for item in items)
    total_discount = sum(item['discount'] for item in items)
    total = sum(item['amount'] for item in items)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} مع الخصم</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
            .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
            .report-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
            .print-date {{ color: #666; font-size: 16px; }}
            .summary {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 20px; margin: 20px 0; }}
            .summary-row {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background: white; border-radius: 5px; }}
            .summary-label {{ font-weight: bold; color: {color}; }}
            .summary-value {{ color: #333; }}
            .discount-highlight {{ color: #dc3545; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 30px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; padding: 15px 10px; text-align: center; font-size: 14px; }}
            th {{ background: {color}; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            .total-row {{ background: #28a745 !important; color: white !important; font-weight: bold; }}
            .discount-col {{ color: #dc3545; font-weight: bold; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
            @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>
        
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">{title} مع تفاصيل الخصم</div>
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
        </div>
        
        <div class="summary">
            <h3 style="text-align: center; margin-bottom: 20px;">ملخص {title}</h3>
            <div class="summary-row">
                <span class="summary-label">عدد العناصر:</span>
                <span class="summary-value">{len(items)} فاتورة</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">المجموع الفرعي:</span>
                <span class="summary-value">{subtotal:.2f} ريال</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">إجمالي الخصم:</span>
                <span class="summary-value discount-highlight">-{total_discount:.2f} ريال</span>
            </div>
            <div class="summary-row" style="background: #28a745; color: white; font-weight: bold;">
                <span>المبلغ النهائي:</span>
                <span>{total:.2f} ريال</span>
            </div>
            <div class="summary-row" style="background: #17a2b8; color: white;">
                <span>المبلغ الموفر:</span>
                <span>{total_discount:.2f} ريال</span>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>الرقم</th>
                    <th>التفاصيل</th>
                    <th>التاريخ</th>
                    <th>المجموع الفرعي</th>
                    <th>الخصم</th>
                    <th>المبلغ النهائي</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for item in items:
        html += f"""
                <tr>
                    <td><strong>{item['id']}</strong></td>
                    <td>{item['name']}</td>
                    <td>{item['date']}</td>
                    <td>{item['subtotal']:.2f} ريال</td>
                    <td class="discount-col">-{item['discount']:.2f} ريال</td>
                    <td><strong>{item['amount']:.2f} ريال</strong></td>
                </tr>"""
    
    html += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{subtotal:.2f} ريال</strong></td>
                    <td><strong>-{total_discount:.2f} ريال</strong></td>
                    <td><strong>{total:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 50px; padding: 20px; background: #f8f9fa; border-radius: 10px; border: 2px solid {color};">
            <h4 style="color: {color}; margin-bottom: 15px;">ملخص الخصومات</h4>
            <p><strong>عدد الفواتير:</strong> {len(items)} | <strong>المجموع الفرعي:</strong> {subtotal:.2f} ريال</p>
            <p><strong>إجمالي الخصم:</strong> <span style="color: #dc3545;">{total_discount:.2f} ريال</span> | <strong>المبلغ النهائي:</strong> <span style="color: #28a745;">{total:.2f} ريال</span></p>
            <p style="color: #17a2b8; font-weight: bold;">🎉 وفرت {total_discount:.2f} ريال من خلال الخصومات!</p>
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
    print("🚀 تشغيل خادم الفواتير مع الخصم...")
    print("📍 الخادم: http://localhost:5000")
    print("💰 الميزات: خانات الخصم في المبيعات والمشتريات")
    print("=" * 60)
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
