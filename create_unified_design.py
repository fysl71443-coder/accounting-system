#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء تصميم موحد للنظام
Create Unified Design System
"""

from pathlib import Path

def create_unified_css():
    """إنشاء CSS موحد للنظام"""
    
    unified_css = """
/* نظام التصميم الموحد - Unified Design System */
:root {
    /* الألوان الأساسية */
    --primary-color: #2563eb;      /* أزرق أساسي */
    --primary-dark: #1d4ed8;       /* أزرق داكن */
    --primary-light: #3b82f6;      /* أزرق فاتح */
    
    --secondary-color: #6b7280;    /* رمادي متوسط */
    --secondary-dark: #374151;     /* رمادي داكن */
    --secondary-light: #9ca3af;    /* رمادي فاتح */
    
    --white: #ffffff;              /* أبيض */
    --black: #000000;              /* أسود */
    --gray-50: #f9fafb;           /* رمادي فاتح جداً */
    --gray-100: #f3f4f6;          /* رمادي فاتح */
    --gray-200: #e5e7eb;          /* رمادي فاتح متوسط */
    --gray-300: #d1d5db;          /* رمادي متوسط فاتح */
    --gray-400: #9ca3af;          /* رمادي متوسط */
    --gray-500: #6b7280;          /* رمادي متوسط */
    --gray-600: #4b5563;          /* رمادي متوسط داكن */
    --gray-700: #374151;          /* رمادي داكن */
    --gray-800: #1f2937;          /* رمادي داكن جداً */
    --gray-900: #111827;          /* رمادي أسود */
    
    /* الخطوط */
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-xs: 0.75rem;      /* 12px */
    --font-size-sm: 0.875rem;     /* 14px */
    --font-size-base: 1rem;       /* 16px */
    --font-size-lg: 1.125rem;     /* 18px */
    --font-size-xl: 1.25rem;      /* 20px */
    --font-size-2xl: 1.5rem;      /* 24px */
    --font-size-3xl: 1.875rem;    /* 30px */
    
    /* المسافات */
    --spacing-1: 0.25rem;         /* 4px */
    --spacing-2: 0.5rem;          /* 8px */
    --spacing-3: 0.75rem;         /* 12px */
    --spacing-4: 1rem;            /* 16px */
    --spacing-5: 1.25rem;         /* 20px */
    --spacing-6: 1.5rem;          /* 24px */
    --spacing-8: 2rem;            /* 32px */
    --spacing-10: 2.5rem;         /* 40px */
    --spacing-12: 3rem;           /* 48px */
    
    /* الظلال */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    
    /* الحدود */
    --border-radius-sm: 0.25rem;  /* 4px */
    --border-radius: 0.375rem;    /* 6px */
    --border-radius-md: 0.5rem;   /* 8px */
    --border-radius-lg: 0.75rem;  /* 12px */
    --border-radius-xl: 1rem;     /* 16px */
}

/* إعادة تعيين الأساسيات */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    line-height: 1.5;
    color: var(--gray-900);
    background-color: var(--gray-50);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* الحاويات */
.container-fluid {
    padding-left: var(--spacing-4);
    padding-right: var(--spacing-4);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: var(--spacing-4);
    padding-right: var(--spacing-4);
}

/* القائمة الجانبية الموحدة */
.sidebar {
    min-height: 100vh;
    background: linear-gradient(180deg, var(--white) 0%, var(--gray-50) 100%);
    border-right: 1px solid var(--gray-200);
    box-shadow: var(--shadow-lg);
    padding: 0;
    position: fixed;
    top: 0;
    right: 0;
    width: 280px;
    z-index: 1000;
    overflow-y: auto;
}

.sidebar-header {
    padding: var(--spacing-6);
    border-bottom: 1px solid var(--gray-200);
    background: var(--white);
}

.sidebar-title {
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: var(--spacing-2);
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
}

.sidebar-subtitle {
    font-size: var(--font-size-sm);
    color: var(--gray-600);
}

.sidebar-nav {
    padding: var(--spacing-4);
}

.nav-section {
    margin-bottom: var(--spacing-6);
}

.nav-section-title {
    font-size: var(--font-size-xs);
    font-weight: 600;
    color: var(--gray-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--spacing-3);
    padding: 0 var(--spacing-3);
}

.nav-link {
    display: flex;
    align-items: center;
    gap: var(--spacing-3);
    padding: var(--spacing-3) var(--spacing-4);
    margin-bottom: var(--spacing-1);
    border-radius: var(--border-radius-md);
    color: var(--gray-700);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.nav-link:hover {
    background-color: var(--gray-100);
    color: var(--gray-900);
    text-decoration: none;
    transform: translateX(-2px);
}

.nav-link.active {
    background-color: var(--primary-color);
    color: var(--white);
    box-shadow: var(--shadow-md);
}

.nav-link.featured {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: var(--white);
    border: 1px solid var(--primary-light);
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.nav-link.featured::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}

.nav-link.featured:hover::before {
    transform: translateX(100%);
}

.nav-icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.badge {
    font-size: var(--font-size-xs);
    padding: var(--spacing-1) var(--spacing-2);
    border-radius: var(--border-radius-sm);
    font-weight: 600;
}

.badge-new {
    background-color: var(--primary-color);
    color: var(--white);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* المحتوى الرئيسي */
.main-content {
    margin-right: 280px;
    min-height: 100vh;
    background-color: var(--gray-50);
}

.page-header {
    background: var(--white);
    border-bottom: 1px solid var(--gray-200);
    padding: var(--spacing-6) var(--spacing-8);
    margin-bottom: var(--spacing-8);
}

.page-title {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: var(--spacing-2);
}

.page-subtitle {
    font-size: var(--font-size-lg);
    color: var(--gray-600);
}

.page-content {
    padding: 0 var(--spacing-8) var(--spacing-8);
}

/* البطاقات */
.card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.card-header {
    padding: var(--spacing-6);
    border-bottom: 1px solid var(--gray-200);
    background: var(--gray-50);
}

.card-title {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--gray-900);
    margin-bottom: var(--spacing-1);
}

.card-subtitle {
    font-size: var(--font-size-sm);
    color: var(--gray-600);
}

.card-body {
    padding: var(--spacing-6);
}

.card-footer {
    padding: var(--spacing-4) var(--spacing-6);
    border-top: 1px solid var(--gray-200);
    background: var(--gray-50);
}

/* الأزرار */
.btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-2);
    padding: var(--spacing-3) var(--spacing-4);
    border: 1px solid transparent;
    border-radius: var(--border-radius);
    font-size: var(--font-size-sm);
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.btn-primary {
    background-color: var(--primary-color);
    color: var(--white);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--primary-dark);
    border-color: var(--primary-dark);
    color: var(--white);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-secondary {
    background-color: var(--gray-600);
    color: var(--white);
    border-color: var(--gray-600);
}

.btn-secondary:hover {
    background-color: var(--gray-700);
    border-color: var(--gray-700);
    color: var(--white);
}

.btn-outline {
    background-color: transparent;
    color: var(--gray-700);
    border-color: var(--gray-300);
}

.btn-outline:hover {
    background-color: var(--gray-100);
    color: var(--gray-900);
    border-color: var(--gray-400);
}

.btn-sm {
    padding: var(--spacing-2) var(--spacing-3);
    font-size: var(--font-size-xs);
}

.btn-lg {
    padding: var(--spacing-4) var(--spacing-6);
    font-size: var(--font-size-lg);
}

/* النماذج */
.form-group {
    margin-bottom: var(--spacing-5);
}

.form-label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--gray-700);
    margin-bottom: var(--spacing-2);
}

.form-control {
    width: 100%;
    padding: var(--spacing-3);
    border: 1px solid var(--gray-300);
    border-radius: var(--border-radius);
    font-size: var(--font-size-base);
    transition: all 0.2s ease;
    background-color: var(--white);
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* الجداول */
.table {
    width: 100%;
    border-collapse: collapse;
    background: var(--white);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.table th {
    background: var(--gray-50);
    padding: var(--spacing-4);
    text-align: right;
    font-weight: 600;
    color: var(--gray-700);
    border-bottom: 1px solid var(--gray-200);
}

.table td {
    padding: var(--spacing-4);
    border-bottom: 1px solid var(--gray-100);
    color: var(--gray-900);
}

.table tbody tr:hover {
    background-color: var(--gray-50);
}

/* التنبيهات */
.alert {
    padding: var(--spacing-4);
    border-radius: var(--border-radius);
    border: 1px solid transparent;
    margin-bottom: var(--spacing-4);
}

.alert-info {
    background-color: rgba(37, 99, 235, 0.1);
    border-color: rgba(37, 99, 235, 0.2);
    color: var(--primary-dark);
}

.alert-success {
    background-color: rgba(34, 197, 94, 0.1);
    border-color: rgba(34, 197, 94, 0.2);
    color: #166534;
}

.alert-warning {
    background-color: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.2);
    color: #92400e;
}

.alert-error {
    background-color: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.2);
    color: #991b1b;
}

/* الاستجابة للشاشات الصغيرة */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
    
    .main-content {
        margin-right: 0;
    }
    
    .page-header,
    .page-content {
        padding-left: var(--spacing-4);
        padding-right: var(--spacing-4);
    }
}

/* إزالة المسافات الزائدة */
.no-margin { margin: 0 !important; }
.no-padding { padding: 0 !important; }
.no-gap { gap: 0 !important; }

/* فئات المساعدة */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.d-flex { display: flex; }
.d-block { display: block; }
.d-none { display: none; }

.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.align-center { align-items: center; }

.w-full { width: 100%; }
.h-full { height: 100%; }

.mb-0 { margin-bottom: 0; }
.mb-2 { margin-bottom: var(--spacing-2); }
.mb-4 { margin-bottom: var(--spacing-4); }
.mb-6 { margin-bottom: var(--spacing-6); }

.mt-0 { margin-top: 0; }
.mt-2 { margin-top: var(--spacing-2); }
.mt-4 { margin-top: var(--spacing-4); }
.mt-6 { margin-top: var(--spacing-6); }
"""
    
    return unified_css

def main():
    """إنشاء ملف CSS الموحد"""
    print("🎨 إنشاء نظام التصميم الموحد...")
    
    # إنشاء مجلد static/css إذا لم يكن موجوداً
    css_dir = Path('static/css')
    css_dir.mkdir(parents=True, exist_ok=True)
    
    # إنشاء ملف CSS الموحد
    unified_css = create_unified_css()
    
    with open(css_dir / 'unified-design.css', 'w', encoding='utf-8') as f:
        f.write(unified_css)
    
    print("✅ تم إنشاء ملف CSS الموحد: static/css/unified-design.css")
    print("📏 حجم الملف: {:.1f} KB".format(len(unified_css) / 1024))
    print("🎨 الألوان المستخدمة: أبيض، أسود، رمادي، أزرق")
    print("📱 متجاوب مع جميع أحجام الشاشات")

if __name__ == "__main__":
    main()
