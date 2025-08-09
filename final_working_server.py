#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
خادم الطباعة النهائي العامل
Final Working Print Server
"""

from flask import Flask, render_template_string, redirect, url_for, session, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
import os

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'print-server-secret-key'

# إعداد Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# مستخدم بسيط للاختبار
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# بيانات تجريبية شاملة
sample_data = {
    'sales': [
        {'id': 'INV-2024-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'amount': 2500.00},
        {'id': 'INV-2024-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'amount': 1800.00},
        {'id': 'INV-2024-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'amount': 3200.00},
        {'id': 'INV-2024-004', 'name': 'مكتب الرياض للاستشارات', 'date': '2024-01-18', 'amount': 1500.00},
        {'id': 'INV-2024-005', 'name': 'عميل نقدي', 'date': '2024-01-19', 'amount': 950.00}
    ],
    'purchases': [
        {'id': 'PUR-2024-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'amount': 5500.00},
        {'id': 'PUR-2024-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'amount': 3200.00},
        {'id': 'PUR-2024-003', 'name': 'شركة المواد الأساسية', 'date': '2024-01-17', 'amount': 4100.00},
        {'id': 'PUR-2024-004', 'name': 'مورد المعدات الصناعية', 'date': '2024-01-18', 'amount': 2800.00}
    ],
    'expenses': [
        {'id': 'EXP-2024-001', 'name': 'مصروفات إدارية', 'date': '2024-01-15', 'amount': 800.00},
        {'id': 'EXP-2024-002', 'name': 'مصروفات تشغيلية', 'date': '2024-01-16', 'amount': 1200.00},
        {'id': 'EXP-2024-003', 'name': 'مصروفات صيانة', 'date': '2024-01-17', 'amount': 650.00},
        {'id': 'EXP-2024-004', 'name': 'مصروفات نقل', 'date': '2024-01-18', 'amount': 450.00}
    ],
    'payroll': [
        {'id': 'PAY-2024-001', 'name': 'أحمد محمد علي - مدير المبيعات', 'date': '2024-01-31', 'amount': 8500.00},
        {'id': 'PAY-2024-002', 'name': 'فاطمة أحمد سالم - محاسبة', 'date': '2024-01-31', 'amount': 6200.00},
        {'id': 'PAY-2024-003', 'name': 'محمد عبدالله حسن - موظف إداري', 'date': '2024-01-31', 'amount': 4800.00},
        {'id': 'PAY-2024-004', 'name': 'سارة علي محمد - سكرتيرة', 'date': '2024-01-31', 'amount': 4200.00}
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
        <title>نظام المحاسبة - الطباعة</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
            .card { background: white; color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="text-center text-success mb-4">🎉 نظام المحاسبة - خادم الطباعة</h1>
                
                <div class="text-center">
                    <h3>أزرار الطباعة العاملة:</h3>
                    
                    {% if current_user.is_authenticated %}
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" target="_blank" class="btn btn-primary btn-print">
                            <i class="fas fa-shopping-cart"></i> طباعة المبيعات
                        </a>
                        
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" target="_blank" class="btn btn-success btn-print">
                            <i class="fas fa-truck"></i> طباعة المشتريات
                        </a>
                        
                        <a href="{{ url_for('print_invoice', invoice_type='expenses') }}" target="_blank" class="btn btn-warning btn-print">
                            <i class="fas fa-receipt"></i> طباعة المصروفات
                        </a>
                        
                        <a href="{{ url_for('print_invoice', invoice_type='payroll') }}" target="_blank" class="btn btn-info btn-print">
                            <i class="fas fa-users"></i> طباعة الرواتب
                        </a>
                        
                        <br><br>
                        <a href="{{ url_for('payments_dues') }}" class="btn btn-outline-primary btn-lg">
                            <i class="fas fa-money-check-alt"></i> صفحة المدفوعات والمستحقات
                        </a>
                        
                        <a href="{{ url_for('logout') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-sign-out-alt"></i> تسجيل الخروج
                        </a>
                    {% else %}
                        <a href="{{ url_for('login') }}" class="btn btn-primary btn-lg">
                            <i class="fas fa-sign-in-alt"></i> تسجيل الدخول
                        </a>
                    {% endif %}
                </div>
                
                <div class="alert alert-success mt-4">
                    <h4>✅ المسارات المتاحة:</h4>
                    <ul>
                        <li>/print_invoices/sales - طباعة المبيعات</li>
                        <li>/print_invoices/purchases - طباعة المشتريات</li>
                        <li>/print_invoices/expenses - طباعة المصروفات</li>
                        <li>/print_invoices/payroll - طباعة الرواتب</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin112233':
            user = User('admin')
            login_user(user)
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('home'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px; }
            .card { background: white; border-radius: 15px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 class="text-center mb-4">تسجيل الدخول</h2>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">اسم المستخدم:</label>
                    <input type="text" name="username" class="form-control" value="admin" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">كلمة المرور:</label>
                    <input type="password" name="password" class="form-control" value="admin112233" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">دخول</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('home'))

@app.route('/payments_dues')
@login_required
def payments_dues():
    """صفحة المدفوعات والمستحقات مع أزرار الطباعة"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>المدفوعات والمستحقات</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: #f8f9fa; padding: 20px; }
            .print-section { background: white; border-radius: 10px; padding: 25px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center mb-4">
                <i class="fas fa-money-check-alt text-primary"></i>
                المدفوعات والمستحقات
            </h1>
            
            <!-- أزرار الطباعة الموحدة -->
            <div class="print-section">
                <h3 class="text-center mb-4">
                    <i class="fas fa-print text-success"></i>
                    أزرار الطباعة السريعة
                </h3>
                
                <div class="text-center">
                    <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary btn-print" target="_blank">
                        <i class="fas fa-shopping-cart me-2"></i>
                        🖨️ طباعة المبيعات
                    </a>
                    
                    <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success btn-print" target="_blank">
                        <i class="fas fa-shopping-bag me-2"></i>
                        🖨️ طباعة المشتريات
                    </a>
                    
                    <a href="{{ url_for('print_invoice', invoice_type='expenses') }}" class="btn btn-warning btn-print" target="_blank">
                        <i class="fas fa-receipt me-2"></i>
                        🖨️ طباعة المصروفات
                    </a>
                    
                    <a href="{{ url_for('print_invoice', invoice_type='payroll') }}" class="btn btn-info btn-print" target="_blank">
                        <i class="fas fa-users me-2"></i>
                        🖨️ طباعة الرواتب
                    </a>
                </div>
                
                <div class="alert alert-info mt-4">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>تعليمات:</strong> اضغط على أي زر لطباعة جميع الفواتير من النوع المحدد. ستفتح نافذة جديدة مع التقرير وستبدأ الطباعة تلقائياً.
                </div>
            </div>
            
            <!-- تبويبات المحاكاة -->
            <div class="print-section">
                <h4>تبويبات النظام:</h4>
                
                <ul class="nav nav-tabs" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" data-bs-toggle="tab" href="#sales">المبيعات</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#purchases">المشتريات</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#expenses">المصروفات</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#payroll">الرواتب</a>
                    </li>
                </ul>
                
                <div class="tab-content mt-3">
                    <div class="tab-pane active" id="sales">
                        <h5>فواتير المبيعات</h5>
                        <p>هنا تظهر فواتير المبيعات...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المبيعات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="purchases">
                        <h5>فواتير المشتريات</h5>
                        <p>هنا تظهر فواتير المشتريات...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المشتريات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="expenses">
                        <h5>فواتير المصروفات</h5>
                        <p>هنا تظهر فواتير المصروفات...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='expenses') }}" class="btn btn-warning" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المصروفات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="payroll">
                        <h5>كشف الرواتب</h5>
                        <p>هنا يظهر كشف الرواتب...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='payroll') }}" class="btn btn-info" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع الرواتب
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="text-center mt-4">
                <a href="{{ url_for('home') }}" class="btn btn-outline-primary">
                    <i class="fas fa-home me-2"></i> العودة للرئيسية
                </a>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

@app.route('/print_invoices/<invoice_type>')
@login_required
def print_invoice(invoice_type):
    """طباعة الفواتير حسب النوع - الدالة العاملة"""
    if invoice_type not in sample_data:
        flash(f'نوع الفاتورة غير صحيح: {invoice_type}', 'error')
        return redirect(url_for('payments_dues'))
    
    data = sample_data[invoice_type]
    title = titles[invoice_type]
    color = colors[invoice_type]
    total = sum(item['amount'] for item in data)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
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
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
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
    """
    
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
    print("🚀 تشغيل خادم الطباعة النهائي...")
    print("📍 الخادم سيعمل على: http://localhost:5000")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("🖨️ جميع أزرار الطباعة جاهزة")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
