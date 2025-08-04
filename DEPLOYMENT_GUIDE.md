# دليل النشر على Render - Render Deployment Guide

## 🚀 نشر نظام المحاسبة على Render

هذا الدليل يوضح كيفية نشر نظام المحاسبة المتكامل على منصة Render.

---

## 📋 المتطلبات المسبقة - Prerequisites

1. **حساب GitHub** مع مستودع يحتوي على كود المشروع
2. **حساب Render** (مجاني) - [render.com](https://render.com)
3. **ملفات التكوين** الموجودة في المشروع:
   - `render.yaml`
   - `requirements.txt`
   - `runtime.txt`
   - `Procfile`

---

## 🔧 خطوات النشر - Deployment Steps

### 1. إعداد المستودع - Repository Setup

#### رفع الكود إلى GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Accounting System"
git branch -M main
git remote add origin https://github.com/yourusername/accounting-system.git
git push -u origin main
```

### 2. إنشاء خدمة قاعدة البيانات - Database Service

#### أ. تسجيل الدخول إلى Render
- اذهب إلى [render.com](https://render.com)
- سجل الدخول أو أنشئ حساباً جديداً

#### ب. إنشاء PostgreSQL Database
1. اضغط على **"New +"**
2. اختر **"PostgreSQL"**
3. املأ البيانات:
   - **Name:** `accounting-db`
   - **Database:** `accounting_system`
   - **User:** `accounting_user`
   - **Region:** اختر الأقرب لك
   - **Plan:** Free (مجاني)
4. اضغط **"Create Database"**

#### ج. نسخ رابط قاعدة البيانات
- بعد إنشاء قاعدة البيانات، انسخ **"External Database URL"**
- سنحتاجه لاحقاً

### 3. إنشاء خدمة الويب - Web Service

#### أ. إنشاء Web Service جديدة
1. اضغط على **"New +"**
2. اختر **"Web Service"**
3. اربط حساب GitHub إذا لم تفعل ذلك
4. اختر المستودع الذي يحتوي على المشروع

#### ب. إعداد الخدمة
املأ البيانات التالية:
- **Name:** `accounting-system`
- **Region:** نفس منطقة قاعدة البيانات
- **Branch:** `main`
- **Root Directory:** (اتركه فارغاً)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

#### ج. إعداد متغيرات البيئة
في قسم **"Environment Variables"**، أضف:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-super-secret-key-here-change-this` |
| `DATABASE_URL` | رابط قاعدة البيانات من الخطوة السابقة |
| `FLASK_ENV` | `production` |

#### د. إعدادات إضافية
- **Plan:** Free
- **Auto-Deploy:** Yes (للنشر التلقائي عند التحديث)

### 4. النشر - Deploy

1. اضغط **"Create Web Service"**
2. انتظر اكتمال عملية البناء والنشر (5-10 دقائق)
3. ستحصل على رابط التطبيق مثل: `https://accounting-system.onrender.com`

---

## 🔍 التحقق من النشر - Verify Deployment

### 1. فحص الحالة
- تأكد أن الخدمة تظهر **"Live"** في لوحة تحكم Render
- تحقق من عدم وجود أخطاء في السجلات (Logs)

### 2. اختبار التطبيق
1. افتح رابط التطبيق
2. يجب أن تظهر صفحة تسجيل الدخول
3. جرب تسجيل الدخول بالبيانات الافتراضية:
   - **المستخدم:** `admin`
   - **كلمة المرور:** `admin123`

### 3. اختبار الوظائف
- تصفح لوحة التحكم
- جرب إنشاء فاتورة مبيعات جديدة
- تحقق من عمل تبديل اللغة

---

## 🛠️ استكشاف الأخطاء - Troubleshooting

### مشاكل شائعة وحلولها:

#### 1. خطأ في قاعدة البيانات
**المشكلة:** `could not connect to server`
**الحل:**
- تأكد من صحة رابط قاعدة البيانات في متغيرات البيئة
- تحقق من أن قاعدة البيانات في حالة "Available"

#### 2. خطأ في البناء
**المشكلة:** `Build failed`
**الحل:**
- تحقق من ملف `requirements.txt`
- تأكد من وجود جميع الملفات المطلوبة
- راجع سجلات البناء للتفاصيل

#### 3. خطأ في التشغيل
**المشكلة:** `Application failed to start`
**الحل:**
- تحقق من أمر التشغيل: `gunicorn app:app`
- تأكد من وجود ملف `app.py` في الجذر
- راجع متغيرات البيئة

#### 4. مشاكل الأداء
**المشكلة:** التطبيق بطيء
**الحل:**
- الخطة المجانية لها قيود على الموارد
- فكر في الترقية للخطة المدفوعة
- تحسين الاستعلامات في قاعدة البيانات

---

## 📊 مراقبة التطبيق - Monitoring

### 1. السجلات - Logs
- اذهب إلى خدمة الويب في Render
- اضغط على تبويب **"Logs"**
- راقب الأخطاء والتحذيرات

### 2. المقاييس - Metrics
- تابع استخدام الذاكرة والمعالج
- راقب أوقات الاستجابة
- تحقق من حالة قاعدة البيانات

### 3. التنبيهات
- فعّل التنبيهات عبر البريد الإلكتروني
- اضبط تنبيهات للأخطاء الحرجة

---

## 🔄 التحديثات - Updates

### النشر التلقائي
عند تفعيل **Auto-Deploy**:
1. ادفع التحديثات إلى GitHub
2. Render سيقوم بالنشر تلقائياً
3. راقب عملية النشر في لوحة التحكم

### النشر اليدوي
1. اذهب إلى خدمة الويب
2. اضغط **"Manual Deploy"**
3. اختر الفرع المطلوب
4. اضغط **"Deploy"**

---

## 💰 التكاليف - Costs

### الخطة المجانية
- **Web Service:** مجاني مع قيود
- **PostgreSQL:** 90 يوم مجاني، ثم $7/شهر
- **قيود:** النوم بعد عدم النشاط، موارد محدودة

### الترقية
- **Starter Plan:** $7/شهر للويب سيرفس
- **موارد أكثر:** ذاكرة وسرعة أفضل
- **بدون نوم:** التطبيق يعمل 24/7

---

## 🔒 الأمان - Security

### أفضل الممارسات:
1. **غيّر SECRET_KEY** إلى قيمة قوية وفريدة
2. **استخدم HTTPS** (Render يوفره تلقائياً)
3. **راجع متغيرات البيئة** بانتظام
4. **فعّل النسخ الاحتياطي** لقاعدة البيانات
5. **راقب السجلات** للأنشطة المشبوهة

---

## 📞 الدعم - Support

### موارد مفيدة:
- [وثائق Render](https://render.com/docs)
- [مجتمع Render](https://community.render.com)
- [دعم Render](https://render.com/support)

### للمساعدة في المشروع:
- راجع ملف `README.md`
- أنشئ issue في GitHub
- تواصل مع فريق التطوير

---

**🎉 تهانينا! تطبيق المحاسبة الآن يعمل على الويب ومتاح للجميع!**

**🎉 Congratulations! Your accounting system is now live on the web!**
