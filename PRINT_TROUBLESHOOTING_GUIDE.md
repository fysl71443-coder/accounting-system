# 🔧 دليل استكشاف أخطاء الطباعة
# Print Troubleshooting Guide

## 🚨 **المشاكل الشائعة وحلولها**

### 1. **مشكلة: الطباعة لا تعمل**

#### الأسباب المحتملة:
- ❌ الخادم لا يعمل
- ❌ JavaScript معطل في المتصفح
- ❌ النوافذ المنبثقة محظورة
- ❌ مشكلة في الشبكة

#### الحلول:

**أ) تشغيل الخادم:**
```bash
# الطريقة الأولى
python direct_start.py

# الطريقة الثانية
start_server.bat

# الطريقة الثالثة
python app.py
```

**ب) فحص الخادم:**
- افتح المتصفح واذهب إلى: http://localhost:5000
- يجب أن تظهر صفحة تسجيل الدخول
- إذا لم تظهر، الخادم لا يعمل

**ج) فحص JavaScript:**
- اضغط F12 في المتصفح
- اذهب إلى تبويب Console
- ابحث عن أخطاء JavaScript باللون الأحمر

**د) السماح بالنوافذ المنبثقة:**
- في Chrome: Settings > Privacy and security > Site Settings > Pop-ups and redirects
- في Firefox: Settings > Privacy & Security > Permissions > Block pop-up windows
- أضف http://localhost:5000 إلى المواقع المسموحة

---

### 2. **مشكلة: أزرار الطباعة لا تظهر**

#### الحلول:
```javascript
// فحص في Console المتصفح
console.log(document.getElementById('printModal'));
// يجب أن يعرض عنصر النافذة المنبثقة

// فحص Bootstrap
console.log(typeof bootstrap);
// يجب أن يعرض 'object'
```

#### إصلاح:
- تأكد من تحميل Bootstrap CSS و JS
- تأكد من وجود النافذة المنبثقة في HTML

---

### 3. **مشكلة: النافذة المنبثقة لا تفتح**

#### الحلول:
```javascript
// اختبار فتح النافذة يدوياً
openPrintModal('sales');

// فحص الأخطاء
try {
    openPrintModal('sales');
} catch(e) {
    console.error('خطأ:', e);
}
```

#### إصلاح:
- تأكد من وجود Bootstrap
- تأكد من صحة HTML للنافذة المنبثقة
- فحص Console للأخطاء

---

### 4. **مشكلة: قائمة الأشهر فارغة**

#### الحلول:
```javascript
// اختبار API الأشهر
fetch('/api/available_months?type=sales')
  .then(r => r.json())
  .then(d => console.log(d));
```

#### إصلاح:
- تأكد من وجود بيانات في قاعدة البيانات
- تشغيل: `python add_test_data_direct.py`
- فحص route في app.py

---

### 5. **مشكلة: معاينة الطباعة لا تعمل**

#### الحلول:
```bash
# اختبار مباشر
curl "http://localhost:5000/print_invoices_preview?type=sales&month=2025-08&status=all&details=true"
```

#### إصلاح:
- فحص route `/print_invoices_preview` في app.py
- تأكد من صحة template
- فحص logs الخادم

---

### 6. **مشكلة: تحميل PDF لا يعمل**

#### الحلول:
```bash
# اختبار تحميل PDF
curl -o test.pdf "http://localhost:5000/download_invoices_pdf?type=sales&month=2025-08&status=all&details=true"
```

#### إصلاح:
- تثبيت مكتبة weasyprint: `pip install weasyprint`
- إذا فشل، سيتم استخدام HTML fallback
- فحص route `/download_invoices_pdf`

---

## 🛠️ **خطوات التشخيص السريع**

### 1. **فحص الخادم:**
```bash
python -c "import requests; print(requests.get('http://localhost:5000').status_code)"
```

### 2. **فحص تسجيل الدخول:**
```bash
python simple_print_test.py
```

### 3. **فحص البيانات:**
```bash
python add_test_data_direct.py
```

### 4. **اختبار شامل:**
```bash
python test_print_complete.py
```

---

## 🔍 **فحص المتصفح**

### في Chrome/Edge:
1. اضغط F12
2. اذهب إلى Console
3. ابحث عن أخطاء باللون الأحمر
4. اذهب إلى Network لفحص طلبات الشبكة

### أخطاء شائعة في Console:
```
❌ Bootstrap is not defined
❌ openPrintModal is not defined  
❌ Failed to fetch
❌ Blocked by CORS policy
```

---

## 📋 **قائمة فحص سريعة**

- [ ] الخادم يعمل على http://localhost:5000
- [ ] تسجيل الدخول يعمل (admin/admin123)
- [ ] صفحة المدفوعات تفتح
- [ ] أزرار الطباعة ظاهرة (4 أزرار)
- [ ] النافذة المنبثقة تفتح
- [ ] قائمة الأشهر تحتوي على بيانات
- [ ] معاينة الطباعة تعمل
- [ ] تحميل PDF يعمل
- [ ] الطباعة المباشرة تعمل

---

## 🆘 **إذا لم تنجح الحلول**

### 1. **إعادة تشغيل كاملة:**
```bash
# إيقاف جميع العمليات
taskkill /f /im python.exe

# إعادة تشغيل
python direct_start.py
```

### 2. **مسح cache المتصفح:**
- Ctrl+Shift+Delete
- مسح Cached images and files

### 3. **اختبار متصفح آخر:**
- جرب Chrome, Firefox, Edge

### 4. **فحص Firewall/Antivirus:**
- تأكد من عدم حظر المنفذ 5000

---

## 📞 **معلومات الدعم**

- **المنفذ:** 5000
- **المستخدم:** admin
- **كلمة المرور:** admin123
- **الرابط:** http://localhost:5000/payments_dues

### ملفات مهمة:
- `app.py` - الخادم الرئيسي
- `templates/payments_dues.html` - صفحة المدفوعات
- `templates/print_invoices_preview.html` - معاينة الطباعة
- `direct_start.py` - تشغيل مباشر للخادم

---

**💡 نصيحة:** إذا استمرت المشاكل، شغل `python test_print_complete.py` وأرسل النتائج للدعم.
