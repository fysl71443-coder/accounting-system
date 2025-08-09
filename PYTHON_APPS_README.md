# نظام المحاسبة الاحترافي - Professional Accounting System

## 🌟 نظرة عامة / Overview

نظام محاسبي احترافي مطور بلغة Python مع واجهات رسومية متقدمة، يدعم اللغة العربية والإنجليزية بشكل كامل. يتضمن النظام عدة تطبيقات متخصصة لإدارة مختلف جوانب المحاسبة.

A professional accounting system developed in Python with advanced graphical interfaces, fully supporting Arabic and English languages. The system includes several specialized applications for managing various aspects of accounting.

## 🎯 التطبيقات المتضمنة / Included Applications

### 1. شاشة المصروفات المتقدمة / Advanced Expenses Screen
- **الملف**: `advanced_expenses_gui.py`
- **الوصف**: إدارة شاملة للمصروفات مع تصنيفات ذكية وتحليلات مفصلة
- **المميزات**:
  - تسجيل المصروفات مع تصنيفات متعددة المستويات
  - دعم طرق دفع متنوعة (MADA, VISA, BANK, CASH, etc.)
  - إرفاق الملفات والإيصالات
  - رسوم بيانية تحليلية (دائرية وشريطية)
  - تصدير إلى Excel و PDF
  - فلترة متقدمة حسب التاريخ والنوع والحالة

### 2. شاشة المدفوعات والمستحقات / Payments & Dues Screen
- **الملف**: `payments_dues_gui.py`
- **الوصف**: متابعة المدفوعات والمستحقات مع إمكانية تسجيل الدفعات
- **المميزات**:
  - عرض فواتير الشراء والبيع الآجلة والرواتب
  - تسجيل دفعات جزئية أو كاملة
  - تتبع حالات الدفع (مدفوع/غير مدفوع/جزئي)
  - ملخص مالي شامل
  - سجل تفصيلي لكل دفعة
  - تقارير مالية قابلة للطباعة

### 3. شاشة حساب التكلفة للمطاعم / Restaurant Costing Screen
- **الملف**: `costing_screen_gui.py`
- **الوصف**: حساب تكلفة الوجبات بناءً على المكونات والنسب
- **المميزات**:
  - إدارة المواد الخام وأسعارها
  - حساب تكلفة الوجبة بناءً على المكونات
  - حساب النسب المئوية لكل مكون
  - تحديد هامش الربح والسعر المقترح
  - حفظ وصفات الوجبات
  - تحديث الأسعار تلقائياً

## 🚀 التشغيل / Installation & Running

### المتطلبات / Requirements

```bash
pip install -r expenses_requirements.txt
```

المكتبات المطلوبة:
- Pillow==10.0.1
- matplotlib==3.7.2
- pandas==2.1.1
- openpyxl==3.1.2
- reportlab==4.0.4
- arabic-reshaper==3.0.0
- python-bidi==0.4.2

### التشغيل / Running

#### الطريقة الأولى: القاذف الرئيسي
```bash
python main_launcher.py
```

#### الطريقة الثانية: تشغيل التطبيقات منفردة
```bash
# شاشة المصروفات المتقدمة
python advanced_expenses_gui.py

# شاشة المدفوعات والمستحقات
python payments_dues_gui.py

# شاشة حساب التكلفة
python costing_screen_gui.py
```

## 🗄️ قواعد البيانات / Databases

### قاعدة بيانات المحاسبة العامة
**الملف**: `accounting_system.db`

**الجداول**:
- `expense_categories` - فئات المصروفات
- `vendors` - الموردين
- `expenses` - المصروفات
- `attachments` - المرفقات
- `accounts` - الحسابات (موردين/عملاء/موظفين)
- `purchases` - فواتير الشراء
- `sales` - فواتير البيع
- `payrolls` - الرواتب
- `payments` - المدفوعات

### قاعدة بيانات المطاعم
**الملف**: `restaurant_costing.db`

**الجداول**:
- `meals` - الوجبات
- `ingredients` - المواد الخام
- `meal_ingredients` - مكونات الوجبات

## 🎨 المميزات التقنية / Technical Features

### دعم اللغات / Language Support
- **العربية**: دعم كامل مع اتجاه RTL
- **الإنجليزية**: دعم كامل مع اتجاه LTR
- تبديل اللغة ديناميكي

### واجهة المستخدم / User Interface
- تصميم احترافي باستخدام Tkinter
- ألوان متناسقة ومريحة للعين
- خطوط واضحة تدعم العربية
- تأثيرات بصرية تفاعلية

### إدارة البيانات / Data Management
- قواعد بيانات SQLite محلية
- نسخ احتياطي تلقائي
- تشفير البيانات الحساسة
- تتبع تغييرات البيانات

### التقارير والتصدير / Reports & Export
- تصدير إلى Excel مع تنسيق احترافي
- تصدير إلى PDF مع شعار الشركة
- رسوم بيانية تفاعلية
- طباعة مباشرة

## 📁 هيكل الملفات / File Structure

```
accounting-system/
├── main_launcher.py              # القاذف الرئيسي
├── advanced_expenses_gui.py      # شاشة المصروفات المتقدمة
├── payments_dues_gui.py          # شاشة المدفوعات والمستحقات
├── costing_screen_gui.py         # شاشة حساب التكلفة
├── expenses_requirements.txt     # متطلبات المشروع
├── PYTHON_APPS_README.md         # دليل المستخدم
├── accounting_system.db          # قاعدة بيانات المحاسبة
├── restaurant_costing.db         # قاعدة بيانات المطاعم
└── exports/                      # مجلد التصدير
    ├── excel/                    # ملفات Excel
    ├── pdf/                      # ملفات PDF
    └── backups/                  # النسخ الاحتياطية
```

## 🔧 التخصيص / Customization

### إضافة فئات مصروفات جديدة
```sql
INSERT INTO expense_categories (name_ar, name_en, category_type)
VALUES ('فئة جديدة', 'New Category', 'operational');
```

### إضافة طرق دفع جديدة
يمكن تعديل قائمة طرق الدفع في كل تطبيق:
```python
payment_methods = ["CASH", "MADA", "VISA", "MASTERCARD", "BANK", "GGC", "AKS", "NEW_METHOD"]
```

### تخصيص الألوان والخطوط
```python
# في كل ملف تطبيق
self.arabic_font = Font(family="Arial Unicode MS", size=10)
self.primary_color = "#3498db"
self.success_color = "#27ae60"
```

## 🛠️ الصيانة والدعم / Maintenance & Support

### النسخ الاحتياطي
- نسخ احتياطي يومي لقواعد البيانات
- تصدير البيانات بصيغ متعددة
- استعادة البيانات من النسخ الاحتياطية

### التحديثات
- تحديثات دورية للمميزات
- إصلاح الأخطاء والثغرات
- تحسين الأداء والسرعة

### الدعم الفني
- دليل المستخدم المفصل
- أمثلة عملية للاستخدام
- حلول للمشاكل الشائعة

## 🚨 استكشاف الأخطاء / Troubleshooting

### مشاكل شائعة وحلولها

#### 1. خطأ في تشغيل التطبيق
```bash
# تأكد من تثبيت المتطلبات
pip install -r expenses_requirements.txt

# تأكد من وجود Python 3.7+
python --version
```

#### 2. مشكلة في عرض النصوص العربية
```python
# تأكد من تثبيت الخطوط العربية
# Windows: Arial Unicode MS
# Linux: Install Arabic fonts
sudo apt-get install fonts-arabeyes
```

#### 3. خطأ في قاعدة البيانات
```python
# حذف قاعدة البيانات وإعادة إنشائها
import os
if os.path.exists('accounting_system.db'):
    os.remove('accounting_system.db')
# ثم تشغيل التطبيق مرة أخرى
```

## 📝 الترخيص / License

هذا المشروع مطور لأغراض تعليمية وتجارية. يمكن استخدامه وتعديله حسب الحاجة.

This project is developed for educational and commercial purposes. It can be used and modified as needed.

## 👥 فريق التطوير / Development Team

- **المطور الرئيسي**: فريق التطوير المتخصص
- **التصميم**: قسم تصميم واجهات المستخدم
- **الاختبار**: فريق ضمان الجودة
- **الدعم الفني**: قسم الدعم والصيانة

## 📞 التواصل / Contact

للاستفسارات والدعم الفني:
- البريد الإلكتروني: support@accounting-system.com
- الهاتف: +966-XX-XXX-XXXX
- الموقع الإلكتروني: www.accounting-system.com

---

**© 2025 نظام المحاسبة الاحترافي - Professional Accounting System**

**تم إنشاء هذا النظام باستخدام Python و Tkinter مع دعم كامل للغة العربية**
