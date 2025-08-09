# دليل استخدام المكونات المشتركة
## Shared Components Usage Guide

## 1. الأزرار الأساسية (Basic Actions)
```html
{% include "components/basic_actions.html" %}
```

### مع معاملات مخصصة:
```html
{% set save_function = "saveProduct()" %}
{% set refresh_function = "loadProducts()" %}
{% include "components/basic_actions.html" %}
```

## 2. إدارة البيانات (Data Management)
```html
{% include "components/data_management.html" %}
```

### مع معاملات مخصصة:
```html
{% set add_function = "addCustomer()" %}
{% set edit_function = "editCustomer()" %}
{% set delete_function = "deleteCustomer()" %}
{% include "components/data_management.html" %}
```

## 3. أزرار النماذج (Form Actions)
```html
{% include "components/form_actions.html" %}
```

### مع نص مخصص:
```html
{% set save_text = "حفظ المنتج" %}
{% include "components/form_actions.html" %}
```

## 4. استخدام الماكرو
```html
{% from "components/button_macros.html" import save_button, edit_button, delete_button %}

{{ save_button("saveProduct()") }}
{{ edit_button("editProduct(1)") }}
{{ delete_button("deleteProduct(1)") }}
```

## 5. أزرار اللغة
```html
{% include "components/language_switcher.html" %}
```

## فوائد استخدام المكونات المشتركة:
- ✅ تقليل التكرار
- ✅ سهولة الصيانة
- ✅ توحيد التصميم
- ✅ تحسين الأداء
- ✅ تقليل حجم الملفات
