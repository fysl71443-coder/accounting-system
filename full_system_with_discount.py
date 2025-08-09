#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
النظام الكامل مع خانات الخصم
Full System with Discount Fields
"""

from flask import Flask, render_template_string, redirect, url_for, session, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'full-system-with-discount-key'

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
    """الشاشة الرئيسية للنظام الكامل"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>نظام المحاسبة المتكامل - الشاشة الرئيسية</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
            .card { background: white; color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            .btn-main { margin: 15px; padding: 20px 30px; font-size: 18px; border-radius: 10px; }
            .feature-card { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 10px 0; }
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
                        
                        <div class="row">
                            <div class="col-md-4">
                                <a href="{{ url_for('dashboard') }}" class="btn btn-primary btn-main w-100">
                                    <i class="fas fa-tachometer-alt fa-2x mb-2"></i><br>
                                    لوحة التحكم
                                </a>
                            </div>
                            <div class="col-md-4">
                                <a href="{{ url_for('payments_dues') }}" class="btn btn-success btn-main w-100">
                                    <i class="fas fa-money-check-alt fa-2x mb-2"></i><br>
                                    المدفوعات والمستحقات
                                </a>
                            </div>
                            <div class="col-md-4">
                                <a href="{{ url_for('logout') }}" class="btn btn-outline-secondary btn-main w-100">
                                    <i class="fas fa-sign-out-alt fa-2x mb-2"></i><br>
                                    تسجيل الخروج
                                </a>
                            </div>
                        </div>
                    {% else %}
                        <a href="{{ url_for('login') }}" class="btn btn-primary btn-main">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            تسجيل الدخول للوصول للنظام الكامل
                        </a>
                    {% endif %}
                </div>
                
                <div class="feature-card mt-4">
                    <h4><i class="fas fa-star text-warning"></i> الميزات الجديدة:</h4>
                    <div class="row">
                        <div class="col-md-6">
                            <ul>
                                <li>✅ خانة المجموع الفرعي</li>
                                <li>✅ خانة الخصم</li>
                                <li>✅ المبلغ النهائي بعد الخصم</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <ul>
                                <li>✅ حساب إجمالي الخصومات</li>
                                <li>✅ عرض المبلغ الموفر</li>
                                <li>✅ تصميم محسن للطباعة</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="alert alert-info mt-4">
                    <h5><i class="fas fa-info-circle"></i> معلومات النظام:</h5>
                    <p><strong>النظام الكامل يتضمن:</strong></p>
                    <ul>
                        <li>🏠 الشاشة الرئيسية (هذه الصفحة)</li>
                        <li>📊 لوحة التحكم مع الإحصائيات</li>
                        <li>💳 صفحة المدفوعات والمستحقات</li>
                        <li>🖨️ أزرار الطباعة مع خانات الخصم</li>
                        <li>👤 نظام تسجيل الدخول</li>
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
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول - النظام الكامل</title>
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
                    دخول للنظام الكامل
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

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة التحكم - النظام الكامل</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: #f8f9fa; padding: 20px; }
            .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; text-align: center; }
            .dashboard-card { background: white; border-radius: 15px; padding: 25px; margin: 15px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
            .stat-card { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; border-radius: 10px; padding: 20px; text-align: center; }
            .btn-dashboard { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="main-header">
                <h1><i class="fas fa-tachometer-alt me-3"></i>لوحة التحكم الرئيسية</h1>
                <p class="mb-0">نظام المحاسبة المتكامل مع خانات الخصم</p>
            </div>
            
            <!-- إحصائيات سريعة -->
            <div class="row">
                <div class="col-md-3">
                    <div class="stat-card">
                        <i class="fas fa-shopping-cart fa-2x mb-2"></i>
                        <h4>المبيعات</h4>
                        <p class="mb-0">5 فواتير</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card" style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);">
                        <i class="fas fa-shopping-bag fa-2x mb-2"></i>
                        <h4>المشتريات</h4>
                        <p class="mb-0">4 فواتير</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card" style="background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);">
                        <i class="fas fa-receipt fa-2x mb-2"></i>
                        <h4>المصروفات</h4>
                        <p class="mb-0">4 فواتير</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card" style="background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);">
                        <i class="fas fa-users fa-2x mb-2"></i>
                        <h4>الرواتب</h4>
                        <p class="mb-0">4 موظفين</p>
                    </div>
                </div>
            </div>
            
            <!-- الوظائف الرئيسية -->
            <div class="dashboard-card">
                <h3><i class="fas fa-cogs text-primary me-2"></i>الوظائف الرئيسية</h3>
                
                <div class="row text-center">
                    <div class="col-md-4">
                        <a href="{{ url_for('payments_dues') }}" class="btn btn-primary btn-dashboard w-100">
                            <i class="fas fa-money-check-alt fa-2x mb-2"></i><br>
                            المدفوعات والمستحقات
                        </a>
                    </div>
                    <div class="col-md-4">
                        <a href="/sales" class="btn btn-success btn-dashboard w-100">
                            <i class="fas fa-shopping-cart fa-2x mb-2"></i><br>
                            إدارة المبيعات
                        </a>
                    </div>
                    <div class="col-md-4">
                        <a href="/purchases" class="btn btn-info btn-dashboard w-100">
                            <i class="fas fa-shopping-bag fa-2x mb-2"></i><br>
                            إدارة المشتريات
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- أزرار الطباعة مع الخصم -->
            <div class="dashboard-card">
                <h3><i class="fas fa-print text-success me-2"></i>طباعة الفواتير مع الخصم</h3>
                
                <div class="row text-center">
                    <div class="col-md-6">
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary btn-dashboard w-100" target="_blank">
                            <i class="fas fa-file-invoice-dollar fa-2x mb-2"></i><br>
                            💰 طباعة المبيعات مع الخصم
                        </a>
                    </div>
                    <div class="col-md-6">
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success btn-dashboard w-100" target="_blank">
                            <i class="fas fa-file-invoice-dollar fa-2x mb-2"></i><br>
                            💰 طباعة المشتريات مع الخصم
                        </a>
                    </div>
                </div>
                
                <div class="alert alert-success mt-3">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>الميزات الجديدة:</strong> خانات الخصم متاحة الآن في فواتير المبيعات والمشتريات!
                </div>
            </div>
            
            <!-- التنقل -->
            <div class="text-center mt-4">
                <a href="{{ url_for('home') }}" class="btn btn-outline-light btn-lg me-3">
                    <i class="fas fa-home me-2"></i> الرئيسية
                </a>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-sign-out-alt me-2"></i> تسجيل الخروج
                </a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/payments_dues')
@login_required
def payments_dues():
    """صفحة المدفوعات والمستحقات مع خانات الخصم"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>المدفوعات والمستحقات - النظام الكامل</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; background: #f8f9fa; padding: 20px; }
            .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; text-align: center; }
            .print-section { background: white; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
            .btn-print { margin: 10px; padding: 15px 25px; font-size: 16px; border-radius: 8px; }
            .discount-badge { background: #dc3545; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="main-header">
                <h1><i class="fas fa-money-check-alt me-3"></i>المدفوعات والمستحقات</h1>
                <p class="mb-2">نظام إدارة المدفوعات مع خانات الخصم المتقدمة</p>
                <span class="discount-badge">
                    <i class="fas fa-percentage me-1"></i>
                    خانات الخصم متاحة
                </span>
            </div>
            
            <!-- أزرار الطباعة مع الخصم -->
            <div class="print-section">
                <h3 class="text-center mb-4">
                    <i class="fas fa-print text-success me-2"></i>
                    طباعة الفواتير مع خانات الخصم
                </h3>
                
                <div class="row text-center">
                    <div class="col-md-6 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='sales') }}" class="btn btn-primary btn-print w-100" target="_blank">
                            <i class="fas fa-file-invoice-dollar fa-2x mb-2"></i><br>
                            💰 طباعة المبيعات مع الخصم
                            <br><small>يشمل: المجموع الفرعي + الخصم + المبلغ النهائي</small>
                        </a>
                    </div>
                    <div class="col-md-6 mb-3">
                        <a href="{{ url_for('print_invoice', invoice_type='purchases') }}" class="btn btn-success btn-print w-100" target="_blank">
                            <i class="fas fa-file-invoice-dollar fa-2x mb-2"></i><br>
                            💰 طباعة المشتريات مع الخصم
                            <br><small>يشمل: المجموع الفرعي + الخصم + المبلغ النهائي</small>
                        </a>
                    </div>
                </div>
                
                <div class="alert alert-success">
                    <h6><i class="fas fa-star text-warning"></i> الميزات الجديدة في الطباعة:</h6>
                    <div class="row">
                        <div class="col-md-6">
                            <ul class="mb-0">
                                <li>✅ عمود المجموع الفرعي</li>
                                <li>✅ عمود الخصم (بلون أحمر)</li>
                                <li>✅ عمود المبلغ النهائي</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <ul class="mb-0">
                                <li>✅ حساب إجمالي الخصومات</li>
                                <li>✅ عرض المبلغ الموفر</li>
                                <li>✅ ملخص تفصيلي للخصومات</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- التنقل -->
            <div class="text-center mt-4">
                <a href="{{ url_for('home') }}" class="btn btn-outline-primary btn-lg me-3">
                    <i class="fas fa-home me-2"></i> الشاشة الرئيسية
                </a>
                <a href="{{ url_for('dashboard') }}" class="btn btn-outline-success btn-lg me-3">
                    <i class="fas fa-tachometer-alt me-2"></i> لوحة التحكم
                </a>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-sign-out-alt me-2"></i> تسجيل الخروج
                </a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/print_invoices/<invoice_type>')
@login_required
def print_invoice(invoice_type):
    """طباعة الفواتير مع خانات الخصم"""
    if invoice_type not in sample_data:
        flash(f'نوع الفاتورة غير صحيح: {invoice_type}', 'error')
        return redirect(url_for('payments_dues'))
    
    data = sample_data[invoice_type]
    title = titles[invoice_type]
    color = colors[invoice_type]
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # حساب المجاميع
    if invoice_type in ['sales', 'purchases']:
        subtotal = sum(item['subtotal'] for item in data)
        total_discount = sum(item['discount'] for item in data)
        total = sum(item['amount'] for item in data)
        has_discount = True
    else:
        subtotal = sum(item['amount'] for item in data)
        total_discount = 0
        total = subtotal
        has_discount = False
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} مع الخصم - النظام الكامل</title>
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
            th, td {{ border: 1px solid #ddd; padding: 15px 8px; text-align: center; font-size: 14px; }}
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
            <div class="report-title">{title}{"" if not has_discount else " مع تفاصيل الخصم"}</div>
            <div class="print-date">تاريخ الطباعة: {current_date}</div>
        </div>
    """
    
    if has_discount:
        html += f"""
        <div class="summary">
            <h3 style="text-align: center; margin-bottom: 20px;">ملخص {title}</h3>
            <div class="summary-row">
                <span class="summary-label">عدد العناصر:</span>
                <span class="summary-value">{len(data)} فاتورة</span>
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
        
        for item in data:
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
            <p><strong>عدد الفواتير:</strong> {len(data)} | <strong>المجموع الفرعي:</strong> {subtotal:.2f} ريال</p>
            <p><strong>إجمالي الخصم:</strong> <span style="color: #dc3545;">{total_discount:.2f} ريال</span> | <strong>المبلغ النهائي:</strong> <span style="color: #28a745;">{total:.2f} ريال</span></p>
            <p style="color: #17a2b8; font-weight: bold;">🎉 وفرت {total_discount:.2f} ريال من خلال الخصومات!</p>
        </div>
        """
    else:
        html += f"""
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
        """
    
    html += f"""
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
    print("🚀 تشغيل النظام الكامل مع خانات الخصم...")
    print("🏠 الشاشة الرئيسية: http://localhost:5000")
    print("📊 لوحة التحكم: http://localhost:5000/dashboard")
    print("💳 المدفوعات: http://localhost:5000/payments_dues")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("💰 خانات الخصم متاحة في المبيعات والمشتريات")
    print("=" * 70)
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
