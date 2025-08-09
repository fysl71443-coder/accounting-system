#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
خادم بسيط يعمل مع أزرار الطباعة المدمجة
Simple Working Server with Integrated Print Buttons
"""

from flask import Flask, render_template_string, redirect, url_for, session, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
import webbrowser
import time
import threading

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'integrated-print-system-key'

# إعداد Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# مستخدم بسيط
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# بيانات تجريبية مع الخصم
sample_data = {
    'sales': [
        {'id': 'INV-2024-001', 'name': 'شركة الأمل التجارية', 'date': '2024-01-15', 'subtotal': 2700.00, 'discount': 200.00, 'amount': 2500.00},
        {'id': 'INV-2024-002', 'name': 'مؤسسة النور للتجارة', 'date': '2024-01-16', 'subtotal': 2000.00, 'discount': 200.00, 'amount': 1800.00},
        {'id': 'INV-2024-003', 'name': 'شركة الفجر الجديد', 'date': '2024-01-17', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00},
        {'id': 'INV-2024-004', 'name': 'مكتب الرياض للاستشارات', 'date': '2024-01-18', 'subtotal': 1650.00, 'discount': 150.00, 'amount': 1500.00},
        {'id': 'INV-2024-005', 'name': 'عميل نقدي', 'date': '2024-01-19', 'subtotal': 1000.00, 'discount': 50.00, 'amount': 950.00}
    ],
    'purchases': [
        {'id': 'PUR-2024-001', 'name': 'شركة التوريدات المتقدمة', 'date': '2024-01-15', 'subtotal': 6000.00, 'discount': 500.00, 'amount': 5500.00},
        {'id': 'PUR-2024-002', 'name': 'مؤسسة الإمداد الشامل', 'date': '2024-01-16', 'subtotal': 3500.00, 'discount': 300.00, 'amount': 3200.00},
        {'id': 'PUR-2024-003', 'name': 'شركة المواد الأساسية', 'date': '2024-01-17', 'subtotal': 4400.00, 'discount': 300.00, 'amount': 4100.00},
        {'id': 'PUR-2024-004', 'name': 'مورد المعدات الصناعية', 'date': '2024-01-18', 'subtotal': 3000.00, 'discount': 200.00, 'amount': 2800.00}
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
        <title>نظام المحاسبة المتكامل</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
            .card { background: white; color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            .btn-main { margin: 15px; padding: 20px 30px; font-size: 18px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="text-center text-success mb-4">
                    <i class="fas fa-calculator"></i>
                    نظام المحاسبة المتكامل
                </h1>
                
                <div class="text-center">
                    {% if current_user.is_authenticated %}
                        <h3>مرحباً {{ current_user.id }}!</h3>
                        
                        <a href="{{ url_for('payments_dues') }}" class="btn btn-primary btn-main">
                            <i class="fas fa-money-check-alt me-2"></i>
                            المدفوعات والمستحقات
                        </a>
                        
                        <br>
                        
                        <a href="{{ url_for('logout') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-sign-out-alt me-2"></i>
                            تسجيل الخروج
                        </a>
                    {% else %}
                        <a href="{{ url_for('login') }}" class="btn btn-primary btn-main">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            تسجيل الدخول للوصول للنظام
                        </a>
                    {% endif %}
                </div>
                
                <div class="alert alert-success mt-4">
                    <h4><i class="fas fa-check-circle"></i> النظام المتكامل يعمل!</h4>
                    <ul>
                        <li>✅ صفحة المدفوعات والمستحقات</li>
                        <li>✅ أزرار الطباعة مدمجة في النظام الأصلي</li>
                        <li>✅ طباعة جميع أنواع الفواتير</li>
                        <li>✅ طباعة فواتير محددة</li>
                        <li>✅ فتح الطباعة في نوافذ منفصلة</li>
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
            return redirect(url_for('payments_dues'))
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
            <h2 class="text-center mb-4">
                <i class="fas fa-sign-in-alt text-primary"></i>
                تسجيل الدخول
            </h2>
            
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
                <button type="submit" class="btn btn-primary w-100">
                    <i class="fas fa-sign-in-alt me-2"></i>
                    دخول
                </button>
            </form>
            
            <div class="text-center mt-3">
                <small class="text-muted">
                    المستخدم: admin | كلمة المرور: admin112233
                </small>
            </div>
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
    """صفحة المدفوعات والمستحقات - مدمجة في النظام الأصلي"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>المدفوعات والمستحقات - النظام المتكامل</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: #f8f9fa; padding: 20px; }
            .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; text-align: center; }
            .print-section { background: white; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; transition: all 0.3s ease; }
            .btn-print:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.2); }
            .tab-content { padding: 20px; background: white; border-radius: 10px; margin-top: 20px; }
            .integration-badge { background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="main-header">
                <h1><i class="fas fa-money-check-alt me-3"></i>المدفوعات والمستحقات</h1>
                <p class="mb-2">نظام إدارة المدفوعات مع أزرار الطباعة المدمجة</p>
                <span class="integration-badge">
                    <i class="fas fa-check-circle me-1"></i>
                    مدمج في النظام الأصلي
                </span>
            </div>
            
            <!-- أزرار الطباعة المدمجة -->
            <div class="print-section">
                <h3 class="text-center mb-4">
                    <i class="fas fa-print text-success me-2"></i>
                    أزرار الطباعة المدمجة في النظام الأصلي
                </h3>
                
                <div class="row text-center">
                    <div class="col-md-3 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary btn-print w-100" target="_blank">
                            <i class="fas fa-shopping-cart fa-2x mb-2"></i><br>
                            🖨️ طباعة جميع المبيعات
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success btn-print w-100" target="_blank">
                            <i class="fas fa-shopping-bag fa-2x mb-2"></i><br>
                            🖨️ طباعة جميع المشتريات
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='expenses') }}" class="btn btn-warning btn-print w-100" target="_blank">
                            <i class="fas fa-receipt fa-2x mb-2"></i><br>
                            🖨️ طباعة جميع المصروفات
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='payroll') }}" class="btn btn-info btn-print w-100" target="_blank">
                            <i class="fas fa-users fa-2x mb-2"></i><br>
                            🖨️ طباعة جميع الرواتب
                        </a>
                    </div>
                </div>
                
                <div class="alert alert-success mt-4">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>النظام المتكامل:</strong> أزرار الطباعة مدمجة في النظام الأصلي. تفتح في نوافذ منفصلة للطباعة مع الحفاظ على تجربة المستخدم في النظام الرئيسي.
                </div>
                
                <!-- طباعة فواتير محددة -->
                <div class="alert alert-info mt-3">
                    <h6><i class="fas fa-file-invoice me-1"></i> طباعة فواتير محددة:</h6>
                    <div class="row">
                        <div class="col-md-3">
                            <a href="{{ url_for('print_single_invoice', invoice_type='sales', invoice_id=1) }}" class="btn btn-outline-primary btn-sm" target="_blank">
                                <i class="fas fa-file-invoice me-1"></i> مبيعات #1
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="{{ url_for('print_single_invoice', invoice_type='purchases', invoice_id=1) }}" class="btn btn-outline-success btn-sm" target="_blank">
                                <i class="fas fa-file-invoice me-1"></i> مشتريات #1
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="{{ url_for('print_single_invoice', invoice_type='expenses', invoice_id=1) }}" class="btn btn-outline-warning btn-sm" target="_blank">
                                <i class="fas fa-file-invoice me-1"></i> مصروفات #1
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="{{ url_for('print_single_invoice', invoice_type='payroll', invoice_id=1) }}" class="btn btn-outline-info btn-sm" target="_blank">
                                <i class="fas fa-file-invoice me-1"></i> راتب #1
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- تبويبات النظام -->
            <div class="print-section">
                <h4><i class="fas fa-tabs text-primary me-2"></i>تبويبات النظام المتكامل:</h4>
                
                <ul class="nav nav-tabs" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" data-bs-toggle="tab" href="#sales">
                            <i class="fas fa-shopping-cart me-1"></i>المبيعات
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#purchases">
                            <i class="fas fa-shopping-bag me-1"></i>المشتريات
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#expenses">
                            <i class="fas fa-receipt me-1"></i>المصروفات
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#payroll">
                            <i class="fas fa-users me-1"></i>الرواتب
                        </a>
                    </li>
                </ul>
                
                <div class="tab-content">
                    <div class="tab-pane active" id="sales">
                        <h5><i class="fas fa-shopping-cart text-primary me-2"></i>فواتير المبيعات</h5>
                        <p>هنا تظهر فواتير المبيعات مع إمكانية البحث والفلترة...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المبيعات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="purchases">
                        <h5><i class="fas fa-shopping-bag text-success me-2"></i>فواتير المشتريات</h5>
                        <p>هنا تظهر فواتير المشتريات مع إمكانية البحث والفلترة...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المشتريات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="expenses">
                        <h5><i class="fas fa-receipt text-warning me-2"></i>فواتير المصروفات</h5>
                        <p>هنا تظهر فواتير المصروفات مع إمكانية البحث والفلترة...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='expenses') }}" class="btn btn-warning" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع المصروفات
                        </a>
                    </div>
                    
                    <div class="tab-pane" id="payroll">
                        <h5><i class="fas fa-users text-info me-2"></i>كشف الرواتب</h5>
                        <p>هنا يظهر كشف الرواتب مع إمكانية البحث والفلترة...</p>
                        <a href="{{ url_for('print_invoice', invoice_type='payroll') }}" class="btn btn-info" target="_blank">
                            <i class="fas fa-print me-1"></i> طباعة جميع الرواتب
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- أزرار التنقل -->
            <div class="text-center mt-4">
                <a href="{{ url_for('home') }}" class="btn btn-outline-primary btn-lg me-3">
                    <i class="fas fa-home me-2"></i> العودة للرئيسية
                </a>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-sign-out-alt me-2"></i> تسجيل الخروج
                </a>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

# دوال الطباعة المدمجة في النظام الأصلي
@app.route('/print_invoices/<invoice_type>')
@login_required
def print_invoice(invoice_type):
    """طباعة جميع الفواتير من نوع محدد - مدمجة في النظام الأصلي"""
    if invoice_type not in sample_data:
        flash(f'نوع الفاتورة غير صحيح: {invoice_type}', 'error')
        return redirect(url_for('payments_dues'))
    
    data = sample_data[invoice_type]
    title = titles[invoice_type]
    color = colors[invoice_type]

    # حساب المجاميع مع الخصم
    if invoice_type in ['sales', 'purchases']:
        subtotal = sum(item.get('subtotal', item['amount']) for item in data)
        total_discount = sum(item.get('discount', 0) for item in data)
        total = sum(item['amount'] for item in data)
    else:
        subtotal = sum(item['amount'] for item in data)
        total_discount = 0
        total = subtotal

    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} - النظام المتكامل</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
            .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
            .report-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
            .print-date {{ color: #666; font-size: 16px; }}
            .integration-note {{ background: #e8f5e8; border: 1px solid #28a745; border-radius: 5px; padding: 10px; margin: 10px 0; text-align: center; color: #155724; }}
            .summary {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin: 30px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; padding: 18px 12px; text-align: center; font-size: 15px; }}
            th {{ background: {color}; color: white; font-weight: bold; font-size: 16px; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            .total-row {{ background: #28a745 !important; color: white !important; font-weight: bold; font-size: 18px; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; font-size: 16px; }}
            @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} .integration-note {{ display: none; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>
        
        <div class="integration-note no-print">
            <strong>✅ مدمج في النظام الأصلي:</strong> هذا التقرير مدمج في نظام المحاسبة الرئيسي ويفتح في نافذة منفصلة للطباعة
        </div>
        
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="report-title">{title}</div>
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
        </div>
        
        <div class="summary">
            <h3>ملخص {title}</h3>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>عدد العناصر:</strong> {len(data)}</p>
                    {"<p><strong>المجموع الفرعي:</strong> " + f"{subtotal:.2f}" + " ريال</p>" if invoice_type in ['sales', 'purchases'] else ""}
                </div>
                <div class="col-md-6">
                    {"<p><strong>إجمالي الخصم:</strong> " + f"{total_discount:.2f}" + " ريال</p>" if invoice_type in ['sales', 'purchases'] and total_discount > 0 else ""}
                    <p><strong>المبلغ النهائي:</strong> {total:.2f} ريال</p>
                </div>
            </div>
        </div>
        
        <table>
            <thead>
                {"<tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المجموع الفرعي</th><th>الخصم</th><th>المبلغ النهائي</th></tr>" if invoice_type in ['sales', 'purchases'] else "<tr><th>الرقم</th><th>التفاصيل</th><th>التاريخ</th><th>المبلغ (ريال)</th></tr>"}
            </thead>
            <tbody>
    """

    for item in data:
        if invoice_type in ['sales', 'purchases']:
            subtotal_item = item.get('subtotal', item['amount'])
            discount_item = item.get('discount', 0)
            html += f"<tr><td><strong>{item['id']}</strong></td><td>{item['name']}</td><td>{item['date']}</td><td>{subtotal_item:.2f} ريال</td><td>{discount_item:.2f} ريال</td><td><strong>{item['amount']:.2f} ريال</strong></td></tr>"
        else:
            html += f"<tr><td><strong>{item['id']}</strong></td><td>{item['name']}</td><td>{item['date']}</td><td>{item['amount']:.2f} ريال</td></tr>"
    
    # إضافة صف المجموع الإجمالي
    if invoice_type in ['sales', 'purchases']:
        html += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{subtotal:.2f} ريال</strong></td>
                    <td><strong>{total_discount:.2f} ريال</strong></td>
                    <td><strong>{total:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>"""
    else:
        html += f"""
                <tr class="total-row">
                    <td colspan="3"><strong>المجموع الإجمالي</strong></td>
                    <td><strong>{total:.2f} ريال</strong></td>
                </tr>
            </tbody>
        </table>"""
        
        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
            {"<p><strong>عدد العناصر: " + str(len(data)) + " | المجموع الفرعي: " + f"{subtotal:.2f}" + " ريال | إجمالي الخصم: " + f"{total_discount:.2f}" + " ريال | المبلغ النهائي: " + f"{total:.2f}" + " ريال</strong></p>" if invoice_type in ['sales', 'purchases'] else "<p><strong>عدد العناصر: " + str(len(data)) + " | إجمالي المبلغ: " + f"{total:.2f}" + " ريال</strong></p>"}
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

@app.route('/print_invoice/<invoice_type>/<int:invoice_id>')
@login_required
def print_single_invoice(invoice_type, invoice_id):
    """طباعة فاتورة محددة - مدمجة في النظام الأصلي"""
    if invoice_type not in sample_data:
        flash(f'نوع الفاتورة غير صحيح: {invoice_type}', 'error')
        return redirect(url_for('payments_dues'))
    
    # البحث عن الفاتورة المحددة
    all_data = sample_data[invoice_type]
    if invoice_id <= len(all_data):
        invoice_data = all_data[invoice_id - 1]
    else:
        invoice_data = all_data[0] if all_data else None
    
    if not invoice_data:
        flash(f'لم يتم العثور على الفاتورة رقم {invoice_id}', 'error')
        return redirect(url_for('payments_dues'))
    
    title = f"فاتورة {titles[invoice_type].split()[-1]} رقم {invoice_id}"
    color = colors[invoice_type]
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} - النظام المتكامل</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; background: white; }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 4px solid {color}; padding-bottom: 25px; }}
            .company-name {{ font-size: 32px; font-weight: bold; color: {color}; margin-bottom: 15px; }}
            .invoice-title {{ font-size: 24px; color: #333; margin-bottom: 10px; }}
            .print-date {{ color: #666; font-size: 16px; }}
            .integration-note {{ background: #e8f5e8; border: 1px solid #28a745; border-radius: 5px; padding: 10px; margin: 10px 0; text-align: center; color: #155724; }}
            .invoice-details {{ background: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 25px; margin: 20px 0; }}
            .detail-row {{ display: flex; justify-content: space-between; margin: 15px 0; padding: 10px; background: white; border-radius: 5px; }}
            .detail-label {{ font-weight: bold; color: {color}; }}
            .detail-value {{ color: #333; }}
            .amount-box {{ text-align: center; background: {color}; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .amount-value {{ font-size: 28px; font-weight: bold; }}
            .print-btn {{ position: fixed; top: 20px; right: 20px; background: {color}; color: white; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; }}
            @media print {{ .no-print {{ display: none !important; }} body {{ margin: 0; }} .integration-note {{ display: none; }} }}
        </style>
    </head>
    <body>
        <button class="print-btn no-print" onclick="window.print()">🖨️ طباعة</button>
        
        <div class="integration-note no-print">
            <strong>✅ مدمج في النظام الأصلي:</strong> هذه الفاتورة مدمجة في نظام المحاسبة الرئيسي وتفتح في نافذة منفصلة للطباعة
        </div>
        
        <div class="header">
            <div class="company-name">نظام المحاسبة المتكامل</div>
            <div class="invoice-title">{title}</div>
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
        </div>
        
        <div class="invoice-details">
            <div class="detail-row">
                <span class="detail-label">رقم الفاتورة:</span>
                <span class="detail-value">{invoice_data['id']}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">التفاصيل:</span>
                <span class="detail-value">{invoice_data['name']}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">التاريخ:</span>
                <span class="detail-value">{invoice_data['date']}</span>
            </div>
            {"<div class='detail-row'><span class='detail-label'>المجموع الفرعي:</span><span class='detail-value'>" + f"{invoice_data.get('subtotal', invoice_data['amount']):.2f}" + " ريال</span></div>" if invoice_type in ['sales', 'purchases'] and 'subtotal' in invoice_data else ""}
            {"<div class='detail-row'><span class='detail-label'>الخصم:</span><span class='detail-value'>" + f"{invoice_data.get('discount', 0):.2f}" + " ريال</span></div>" if invoice_type in ['sales', 'purchases'] and invoice_data.get('discount', 0) > 0 else ""}
        </div>

        <div class="amount-box">
            <div>{"المبلغ النهائي بعد الخصم" if invoice_type in ['sales', 'purchases'] and invoice_data.get('discount', 0) > 0 else "المبلغ الإجمالي"}</div>
            <div class="amount-value">{invoice_data['amount']:.2f} ريال</div>
            {"<div style='font-size: 14px; margin-top: 10px;'>وفرت " + f"{invoice_data.get('discount', 0):.2f}" + " ريال</div>" if invoice_type in ['sales', 'purchases'] and invoice_data.get('discount', 0) > 0 else ""}
        </div>
        
        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px solid {color}; color: #666;">
            <p>تم إنشاء هذه الفاتورة بواسطة نظام المحاسبة المتكامل</p>
            <p><strong>فاتورة رقم: {invoice_id} | المبلغ: {invoice_data['amount']:.2f} ريال</strong></p>
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

def open_browser():
    """فتح المتصفح بعد تشغيل الخادم"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:5000")
        print("✅ تم فتح المتصفح")
    except:
        print("⚠️ لم يتم فتح المتصفح تلقائياً")

if __name__ == '__main__':
    print("🚀 تشغيل النظام المتكامل مع أزرار الطباعة المدمجة...")
    print("📍 الخادم: http://localhost:5000")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("💳 المدفوعات: http://localhost:5000/payments_dues")
    print("🖨️ أزرار الطباعة مدمجة في النظام الأصلي")
    print("🪟 الطباعة تفتح في نوافذ منفصلة")
    print("=" * 70)
    
    # فتح المتصفح في thread منفصل
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # تشغيل الخادم
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
