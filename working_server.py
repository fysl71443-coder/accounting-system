
from flask import Flask, render_template_string
import datetime

app = Flask(__name__)
app.secret_key = 'test-key'

# بيانات تجريبية
sample_data = {
    'sales': [
        {'id': 'INV-001', 'name': 'شركة الأمل', 'date': '2024-01-15', 'amount': 2500.00},
        {'id': 'INV-002', 'name': 'مؤسسة النور', 'date': '2024-01-16', 'amount': 1800.00}
    ],
    'purchases': [
        {'id': 'PUR-001', 'name': 'شركة التوريدات', 'date': '2024-01-15', 'amount': 5500.00}
    ],
    'expenses': [
        {'id': 'EXP-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00}
    ],
    'payroll': [
        {'id': 'PAY-001', 'name': 'أحمد محمد - مدير', 'date': '2024-01-31', 'amount': 8500.00}
    ]
}

titles = {
    'sales': 'فواتير المبيعات',
    'purchases': 'فواتير المشتريات', 
    'expenses': 'فواتير المصروفات',
    'payroll': 'كشف الرواتب'
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
    <h1>خادم الطباعة يعمل!</h1>
    <ul>
        <li><a href="/print_invoices/sales">طباعة المبيعات</a></li>
        <li><a href="/print_invoices/purchases">طباعة المشتريات</a></li>
        <li><a href="/print_invoices/expenses">طباعة المصروفات</a></li>
        <li><a href="/print_invoices/payroll">طباعة الرواتب</a></li>
    </ul>
    """

@app.route('/print_invoices/<invoice_type>')
def print_invoices(invoice_type):
    if invoice_type not in sample_data:
        return f"نوع الفاتورة غير صحيح: {invoice_type}", 404
    
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
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid {color}; padding-bottom: 20px; }}
            .title {{ font-size: 28px; font-weight: bold; color: {color}; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 15px; text-align: center; }}
            th {{ background: {color}; color: white; }}
            .total {{ background: #f0f0f0; font-weight: bold; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ طباعة</button>
        <div class="header">
            <div class="title">نظام المحاسبة المتكامل</div>
            <div>{title}</div>
            <div>تاريخ الطباعة: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
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

if __name__ == '__main__':
    print("🚀 تشغيل خادم الطباعة...")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
