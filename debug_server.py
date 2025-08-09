#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص مشاكل الخادم
Debug Server Issues
"""

import sys
import traceback

def test_import():
    """اختبار استيراد الملفات"""
    print("🔍 اختبار استيراد الملفات...")
    
    try:
        print("   - استيراد Flask...")
        from flask import Flask
        print("   ✅ Flask")
        
        print("   - استيراد app...")
        from app import app
        print("   ✅ app")
        
        print("   - فحص routes...")
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append(f"{rule.rule} -> {rule.endpoint}")
            
            print(f"   ✅ تم العثور على {len(routes)} route")
            
            # البحث عن routes الطباعة
            print_routes = [r for r in routes if 'print' in r.lower()]
            if print_routes:
                print("   📄 Routes الطباعة الموجودة:")
                for route in print_routes:
                    print(f"      - {route}")
            else:
                print("   ❌ لم يتم العثور على routes الطباعة")
        
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في الاستيراد: {e}")
        print(f"   📋 تفاصيل الخطأ:")
        traceback.print_exc()
        return False

def test_simple_server():
    """اختبار خادم بسيط"""
    print("\n🚀 اختبار خادم بسيط...")
    
    try:
        from flask import Flask
        
        # إنشاء تطبيق بسيط
        simple_app = Flask(__name__)
        
        @simple_app.route('/')
        def home():
            return "الخادم يعمل!"
        
        @simple_app.route('/test_print')
        def test_print():
            return "اختبار الطباعة يعمل!"
        
        print("   ✅ تم إنشاء التطبيق البسيط")
        
        # تشغيل الخادم
        print("   🌐 تشغيل الخادم البسيط...")
        simple_app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
        
    except Exception as e:
        print(f"   ❌ خطأ في الخادم البسيط: {e}")
        traceback.print_exc()

def create_working_server():
    """إنشاء خادم يعمل مع routes الطباعة"""
    print("\n🔧 إنشاء خادم يعمل مع routes الطباعة...")
    
    server_code = '''
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
'''
    
    with open("working_server.py", "w", encoding="utf-8") as f:
        f.write(server_code)
    
    print("✅ تم إنشاء working_server.py")
    return "working_server.py"

def main():
    """الوظيفة الرئيسية"""
    print("🔧 تشخيص مشاكل الخادم")
    print("=" * 50)
    
    # اختبار الاستيراد
    import_ok = test_import()
    
    if not import_ok:
        print("\n❌ مشكلة في استيراد الملفات")
        print("💡 سيتم إنشاء خادم بديل...")
        
        # إنشاء خادم بديل
        server_file = create_working_server()
        
        print(f"\n🚀 تشغيل الخادم البديل...")
        print(f"📄 الملف: {server_file}")
        print("💡 شغل الأمر: python working_server.py")
        
    else:
        print("\n✅ الاستيراد يعمل بشكل صحيح")
        print("💡 المشكلة قد تكون في التشغيل")
    
    print("\n📋 الحلول المقترحة:")
    print("1. شغل: python working_server.py")
    print("2. أو استخدم الصفحة المستقلة: working_print_solution.html")
    print("3. أو جرب: flask --app working_server.py run --debug")

if __name__ == "__main__":
    main()
