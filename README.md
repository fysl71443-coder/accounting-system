# نظام المحاسبة المتكامل - Integrated Accounting System

## 📋 وصف المشروع - Project Description

نظام محاسبي متكامل مطور بلغة Python باستخدام Flask، يدعم اللغتين العربية والإنجليزية مع نظام فروع للمبيعات. التطبيق مصمم للعمل على الويب ويمكن نشره على منصات مثل Render.

A comprehensive web-based accounting system developed in Python using Flask, supporting both Arabic and English languages with a branch system for sales. The application is designed for web deployment on platforms like Render.

## 🌟 المميزات الرئيسية - Key Features

### 🏢 نظام الفروع - Branch System
- **PLACE INDIA** - فرع الهند
- **CHINA TOWN** - فرع الصين

### 🌐 دعم اللغات - Language Support
- **العربية** - اتجاه من اليمين لليسار
- **English** - Left to right direction

### 💼 الوظائف المحاسبية - Accounting Functions
- ✅ فواتير المبيعات والمشتريات
- ✅ إدارة المخزون والأصناف
- ✅ إدارة الموردين والعملاء
- ✅ نظام الموظفين والرواتب
- ✅ التقارير المالية والضريبية
- ✅ نظام المدفوعات المتعددة

### 💳 طرق الدفع المدعومة - Supported Payment Methods
- نقدي (Cash)
- مدى (MADA)
- فيزا (VISA)
- ماستركارد (MasterCard)
- تحويل بنكي (Bank Transfer)
- GCC
- AKS
- آجل (Credit)

## 🛠️ التقنيات المستخدمة - Technologies Used

### Backend
- **Python 3.11+**
- **Flask** - إطار العمل الويب
- **SQLAlchemy** - ORM لقاعدة البيانات
- **PostgreSQL** - قاعدة البيانات (للإنتاج)
- **SQLite** - قاعدة البيانات (للتطوير)
- **Flask-Login** - إدارة المصادقة
- **Werkzeug** - الأمان وتشفير كلمات المرور

### Frontend
- **HTML5/CSS3** - هيكل وتصميم الصفحات
- **Bootstrap 5** - إطار العمل للتصميم
- **JavaScript** - التفاعل والديناميكية
- **Chart.js** - الرسومات البيانية
- **Font Awesome** - الأيقونات

### Additional Libraries
- **Gunicorn** - خادم WSGI للإنتاج
- **Matplotlib** - الرسومات البيانية
- **Pandas** - معالجة البيانات
- **ReportLab** - إنتاج ملفات PDF
- **Arabic-Reshaper** - دعم النصوص العربية

## 📁 هيكل المشروع - Project Structure

```
ACCOUNTS PROGRAM/
├── app.py                      # التطبيق الرئيسي Flask
├── requirements.txt            # المتطلبات
├── runtime.txt                # إصدار Python
├── Procfile                   # ملف Render/Heroku
├── render.yaml                # تكوين Render
├── README.md                  # ملف التوثيق
├── templates/                 # قوالب HTML
│   ├── base.html             # القالب الأساسي
│   ├── login.html            # صفحة تسجيل الدخول
│   ├── dashboard.html        # لوحة التحكم
│   ├── new_sale.html         # فاتورة مبيعات جديدة
│   ├── sales.html            # قائمة المبيعات
│   └── products.html         # إدارة المنتجات
├── static/                   # الملفات الثابتة
│   ├── css/                  # ملفات CSS
│   ├── js/                   # ملفات JavaScript
│   └── images/               # الصور والأيقونات
├── src/                      # مجلد المصدر (للمراجع)
└── assets/                   # الأصول
```

## 🚀 التثبيت والتشغيل - Installation & Running

### التطوير المحلي - Local Development

#### 1. تثبيت Python
تأكد من تثبيت Python 3.11 أو أحدث

#### 2. استنساخ المشروع
```bash
git clone <repository-url>
cd ACCOUNTS-PROGRAM
```

#### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

#### 4. إعداد متغيرات البيئة
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///accounting.db"  # للتطوير
```

#### 5. تشغيل التطبيق
```bash
python app.py
```

التطبيق سيعمل على: `http://localhost:5000`

### النشر على Render - Deploy to Render

#### 1. إنشاء حساب على Render
قم بزيارة [render.com](https://render.com) وأنشئ حساباً

#### 2. ربط المستودع
- اربط مستودع GitHub الخاص بك
- اختر هذا المشروع

#### 3. إعداد الخدمة
- اختر "Web Service"
- استخدم الإعدادات من ملف `render.yaml`
- أو قم بالإعداد يدوياً:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app:app`
  - **Environment:** Python 3.11

#### 4. إعداد قاعدة البيانات
- أنشئ خدمة PostgreSQL جديدة
- اربطها بالتطبيق عبر متغير `DATABASE_URL`

#### 5. النشر
- اضغط "Deploy" وانتظر اكتمال النشر
- التطبيق سيكون متاحاً على الرابط المُعطى

## 👤 بيانات تسجيل الدخول الافتراضية - Default Login

- **اسم المستخدم:** admin
- **كلمة المرور:** admin123

## 📊 الشاشات المتوفرة - Available Screens

### ✅ مكتملة - Completed
1. **شاشة تسجيل الدخول** - Login Screen
2. **الشاشة الرئيسية** - Main Dashboard
3. **نظام إدارة اللغات** - Language Management
4. **نظام الفروع** - Branch System

### 🔄 قيد التطوير - In Development
5. **شاشة المبيعات** - Sales Screen
6. **شاشة المشتريات** - Purchases Screen
7. **إدارة المنتجات** - Product Management
8. **إدارة المخزون** - Inventory Management
9. **إدارة الموردين** - Suppliers Management
10. **إدارة العملاء** - Customers Management
11. **نظام الموظفين** - Employee System
12. **التقارير المالية** - Financial Reports
13. **نظام الضرائب** - Tax System
14. **الإعدادات** - Settings

## 🗄️ قاعدة البيانات - Database

### الجداول المُنشأة - Created Tables
- `users` - المستخدمين
- `roles` - الأدوار والصلاحيات
- `branches` - الفروع
- `products` - المنتجات
- `suppliers` - الموردين
- `customers` - العملاء
- `purchases` - فواتير المشتريات
- `purchase_items` - عناصر فواتير المشتريات
- `sales` - فواتير المبيعات
- `sale_items` - عناصر فواتير المبيعات

## 🔧 الإعدادات - Configuration

يمكن تخصيص البرنامج من خلال ملف `config/settings.json` الذي يتم إنشاؤه تلقائياً.

## 📝 الترخيص - License

هذا المشروع مفتوح المصدر ومتاح للاستخدام والتطوير.

## 🤝 المساهمة - Contributing

نرحب بالمساهمات لتطوير وتحسين النظام.

## 📞 الدعم - Support

للدعم الفني أو الاستفسارات، يرجى إنشاء issue في المستودع.

---

**تم التطوير بـ ❤️ باستخدام Python**

**Developed with ❤️ using Python**
