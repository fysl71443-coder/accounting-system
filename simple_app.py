#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخة مبسطة من تطبيق المحاسبة للتشغيل السريع
Simplified version of accounting app for quick run
"""

try:
    from flask import Flask, render_template_string, request, redirect, url_for, flash, session
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Error importing Flask: {e}")
    print("Installing Flask...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template_string, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'dev-secret-key-for-testing'

# بيانات تجريبية للمنتجات
SAMPLE_PRODUCTS = [
    {"id": 1, "code": "PHONE001", "name": "iPhone 14", "category": "إلكترونيات", "cost": 3000.00, "price": 3500.00, "stock": 20},
    {"id": 2, "code": "PHONE002", "name": "Samsung Galaxy S23", "category": "إلكترونيات", "cost": 2500.00, "price": 3000.00, "stock": 15},
    {"id": 3, "code": "LAPTOP001", "name": "MacBook Air", "category": "إلكترونيات", "cost": 4000.00, "price": 4800.00, "stock": 10},
    {"id": 4, "code": "SHIRT001", "name": "قميص قطني", "category": "ملابس", "cost": 50.00, "price": 80.00, "stock": 50},
    {"id": 5, "code": "FOOD001", "name": "أرز بسمتي", "category": "أغذية", "cost": 15.00, "price": 25.00, "stock": 100},
]

# بيانات تجريبية للفواتير
SAMPLE_INVOICES = []

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ session.get('language', 'ar') }}" dir="{{ 'rtl' if session.get('language', 'ar') == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام المحاسبة - تسجيل الدخول</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% if session.get('language', 'ar') == 'ar' %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    {% endif %}
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: {{ "'Cairo', sans-serif" if session.get('language', 'ar') == 'ar' else "'Inter', sans-serif" }};
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .login-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .btn-primary {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            border: none;
        }
    </style>
</head>
<body>
    <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
        <div class="login-card p-5" style="width: 100%; max-width: 400px;">
            <div class="text-center mb-4">
                <div class="bg-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-calculator text-white fa-2x"></i>
                </div>
                <h3>{{ "نظام المحاسبة المتكامل" if session.get('language', 'ar') == 'ar' else "Integrated Accounting System" }}</h3>
                <p class="text-muted">{{ "يرجى تسجيل الدخول للمتابعة" if session.get('language', 'ar') == 'ar' else "Please login to continue" }}</p>
            </div>

            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-info">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">{{ "اسم المستخدم" if session.get('language', 'ar') == 'ar' else "Username" }}</label>
                    <input type="text" class="form-control" name="username" value="admin" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">{{ "كلمة المرور" if session.get('language', 'ar') == 'ar' else "Password" }}</label>
                    <input type="password" class="form-control" name="password" value="admin123" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">{{ "اللغة" if session.get('language', 'ar') == 'ar' else "Language" }}</label>
                    <select class="form-select" name="language">
                        <option value="ar" {{ 'selected' if session.get('language', 'ar') == 'ar' else '' }}>العربية</option>
                        <option value="en" {{ 'selected' if session.get('language', 'ar') == 'en' else '' }}>English</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">
                    {{ "تسجيل الدخول" if session.get('language', 'ar') == 'ar' else "Login" }}
                </button>
            </form>

            <div class="alert alert-info mt-3">
                <small>
                    <strong>{{ "بيانات تجريبية:" if session.get('language', 'ar') == 'ar' else "Demo Credentials:" }}</strong><br>
                    {{ "المستخدم:" if session.get('language', 'ar') == 'ar' else "Username:" }} admin<br>
                    {{ "كلمة المرور:" if session.get('language', 'ar') == 'ar' else "Password:" }} admin123
                </small>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ session.get('language', 'ar') }}" dir="{{ 'rtl' if session.get('language', 'ar') == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - نظام المحاسبة</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% if session.get('language', 'ar') == 'ar' %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    {% endif %}
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: {{ "'Cairo', sans-serif" if session.get('language', 'ar') == 'ar' else "'Inter', sans-serif" }};
            background-color: #f8fafc;
        }
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .stats-card.success { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .stats-card.warning { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .stats-card.info { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .card { border: none; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <i class="fas fa-calculator me-2"></i>
                {{ "نظام المحاسبة" if session.get('language', 'ar') == 'ar' else "Accounting System" }}
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('logout') }}">
                    <i class="fas fa-sign-out-alt me-1"></i>
                    {{ "تسجيل الخروج" if session.get('language', 'ar') == 'ar' else "Logout" }}
                </a>
            </div>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-12">
                <h1 class="h2 mb-4">
                    <i class="fas fa-tachometer-alt me-2"></i>
                    {{ "لوحة التحكم الرئيسية" if session.get('language', 'ar') == 'ar' else "Main Dashboard" }}
                </h1>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="row">
            <div class="col-xl-3 col-md-6">
                <div class="stats-card">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6>{{ "مبيعات اليوم" if session.get('language', 'ar') == 'ar' else "Today's Sales" }}</h6>
                            <h3>0.00 ريال</h3>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-calendar-day fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stats-card success">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6>{{ "مبيعات الشهر" if session.get('language', 'ar') == 'ar' else "Monthly Sales" }}</h6>
                            <h3>0.00 ريال</h3>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-chart-line fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stats-card warning">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6>{{ "إجمالي المنتجات" if session.get('language', 'ar') == 'ar' else "Total Products" }}</h6>
                            <h3>10</h3>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-box fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stats-card info">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6>{{ "الفروع النشطة" if session.get('language', 'ar') == 'ar' else "Active Branches" }}</h6>
                            <h3>2</h3>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-store fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-bolt me-2"></i>
                            {{ "إجراءات سريعة" if session.get('language', 'ar') == 'ar' else "Quick Actions" }}
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3 mb-3">
                                <a href="#" class="btn btn-primary w-100 h-100 d-flex flex-column justify-content-center align-items-center p-4">
                                    <i class="fas fa-plus-circle fa-2x mb-2"></i>
                                    {{ "فاتورة مبيعات جديدة" if session.get('language', 'ar') == 'ar' else "New Sales Invoice" }}
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="#" class="btn btn-success w-100 h-100 d-flex flex-column justify-content-center align-items-center p-4">
                                    <i class="fas fa-box fa-2x mb-2"></i>
                                    {{ "إدارة المنتجات" if session.get('language', 'ar') == 'ar' else "Manage Products" }}
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="#" class="btn btn-info w-100 h-100 d-flex flex-column justify-content-center align-items-center p-4">
                                    <i class="fas fa-chart-bar fa-2x mb-2"></i>
                                    {{ "تقارير المبيعات" if session.get('language', 'ar') == 'ar' else "Sales Reports" }}
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="#" class="btn btn-warning w-100 h-100 d-flex flex-column justify-content-center align-items-center p-4">
                                    <i class="fas fa-cog fa-2x mb-2"></i>
                                    {{ "الإعدادات" if session.get('language', 'ar') == 'ar' else "Settings" }}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Branches Info -->
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-store me-2"></i>
                            {{ "الفروع" if session.get('language', 'ar') == 'ar' else "Branches" }}
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">PLACE INDIA</h6>
                                    <small class="text-muted">{{ "فرع الهند" if session.get('language', 'ar') == 'ar' else "India Branch" }}</small>
                                </div>
                                <span class="badge bg-success">{{ "نشط" if session.get('language', 'ar') == 'ar' else "Active" }}</span>
                            </div>
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">CHINA TOWN</h6>
                                    <small class="text-muted">{{ "فرع الصين" if session.get('language', 'ar') == 'ar' else "China Branch" }}</small>
                                </div>
                                <span class="badge bg-success">{{ "نشط" if session.get('language', 'ar') == 'ar' else "Active" }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-info-circle me-2"></i>
                            {{ "معلومات النظام" if session.get('language', 'ar') == 'ar' else "System Info" }}
                        </h5>
                    </div>
                    <div class="card-body">
                        <p><strong>{{ "الإصدار:" if session.get('language', 'ar') == 'ar' else "Version:" }}</strong> 1.0.0</p>
                        <p><strong>{{ "نوع التطبيق:" if session.get('language', 'ar') == 'ar' else "App Type:" }}</strong> {{ "تطبيق ويب" if session.get('language', 'ar') == 'ar' else "Web Application" }}</p>
                        <p><strong>{{ "قاعدة البيانات:" if session.get('language', 'ar') == 'ar' else "Database:" }}</strong> SQLite/PostgreSQL</p>
                        <p><strong>{{ "الحالة:" if session.get('language', 'ar') == 'ar' else "Status:" }}</strong> <span class="badge bg-success">{{ "يعمل" if session.get('language', 'ar') == 'ar' else "Running" }}</span></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        language = request.form.get('language', 'ar')
        
        session['language'] = language
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            flash('تم تسجيل الدخول بنجاح!' if language == 'ar' else 'Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة' if language == 'ar' else 'Invalid username or password')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح' if session.get('language', 'ar') == 'ar' else 'Logged out successfully')
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 بدء تشغيل نظام المحاسبة...")
    print("🚀 Starting Accounting System...")
    print()
    print("📍 التطبيق يعمل على: http://localhost:5000")
    print("📍 Application running on: http://localhost:5000")
    print()
    print("👤 بيانات تسجيل الدخول:")
    print("👤 Login credentials:")
    print("   المستخدم / Username: admin")
    print("   كلمة المرور / Password: admin123")
    print()
    print("🛑 لإيقاف التطبيق اضغط Ctrl+C")
    print("🛑 To stop the application press Ctrl+C")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
