#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء قائمة جانبية شاملة مع جميع الشاشات
Create Complete Sidebar with All Screens
"""

def create_complete_sidebar_html():
    """إنشاء HTML للقائمة الجانبية الشاملة"""
    
    sidebar_html = '''        <div class="sidebar-nav">
            <!-- لوحة التحكم الرئيسية -->
            <div class="nav-section">
                <a class="nav-link {{ 'active' if request.endpoint == 'dashboard' else '' }}" href="{{ url_for('dashboard') }}">
                    <i class="fas fa-tachometer-alt nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}لوحة التحكم{% else %}Dashboard{% endif %}
                </a>
            </div>

            <!-- الشاشات المتقدمة والمميزة -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}الشاشات المتقدمة{% else %}Advanced Screens{% endif %}
                </div>
                <a class="nav-link featured {{ 'active' if request.endpoint == 'unified_products' else '' }}" href="{{ url_for('unified_products') }}">
                    <i class="fas fa-cogs nav-icon"></i>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600;">
                            {% if session.get('language', 'ar') == 'ar' %}🌟 إدارة المنتجات والتكاليف{% else %}🌟 Products & Costing{% endif %}
                        </div>
                        <small style="opacity: 0.8;">
                            {% if session.get('language', 'ar') == 'ar' %}شاشة موحدة متكاملة{% else %}Integrated unified screen{% endif %}
                        </small>
                    </div>
                    <span class="badge badge-new">
                        {% if session.get('language', 'ar') == 'ar' %}جديد{% else %}NEW{% endif %}
                    </span>
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'cost_calculation' else '' }}" href="#">
                    <i class="fas fa-calculator nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}حساب التكاليف{% else %}Cost Calculation{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'meal_cost_calculator' else '' }}" href="#">
                    <i class="fas fa-utensils nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}حاسبة تكلفة الوجبات{% else %}Meal Cost Calculator{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'advanced_reports' else '' }}" href="#">
                    <i class="fas fa-chart-pie nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}التقارير المتقدمة{% else %}Advanced Reports{% endif %}
                </a>
            </div>

            <!-- المبيعات والفواتير -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}المبيعات والفواتير{% else %}Sales & Invoices{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'new_sale' else '' }}" href="{{ url_for('new_sale') }}">
                    <i class="fas fa-plus-circle nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}فاتورة جديدة{% else %}New Invoice{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'sales' else '' }}" href="{{ url_for('sales') }}">
                    <i class="fas fa-shopping-cart nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المبيعات{% else %}Sales{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'orders' else '' }}" href="#">
                    <i class="fas fa-clipboard-list nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}الطلبات{% else %}Orders{% endif %}
                </a>
            </div>

            <!-- إدارة المخزون والمنتجات -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}المخزون والمنتجات{% else %}Inventory & Products{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'products' else '' }}" href="#">
                    <i class="fas fa-box nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المنتجات{% else %}Products{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'raw_materials' else '' }}" href="#">
                    <i class="fas fa-cubes nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المواد الخام{% else %}Raw Materials{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'inventory' else '' }}" href="#">
                    <i class="fas fa-warehouse nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}إدارة المخزون{% else %}Inventory Management{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'product_transfer' else '' }}" href="#">
                    <i class="fas fa-exchange-alt nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}نقل المنتجات{% else %}Product Transfer{% endif %}
                </a>
            </div>

            <!-- المشتريات والموردين -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}المشتريات والموردين{% else %}Purchases & Suppliers{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'purchases' else '' }}" href="#">
                    <i class="fas fa-shopping-bag nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المشتريات{% else %}Purchases{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'suppliers' else '' }}" href="#">
                    <i class="fas fa-truck nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}الموردين{% else %}Suppliers{% endif %}
                </a>
            </div>

            <!-- العملاء والعلاقات -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}العملاء والعلاقات{% else %}Customers & Relations{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'customers' else '' }}" href="#">
                    <i class="fas fa-users nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}العملاء{% else %}Customers{% endif %}
                </a>
            </div>

            <!-- المالية والمحاسبة -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}المالية والمحاسبة{% else %}Finance & Accounting{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'expenses' else '' }}" href="#">
                    <i class="fas fa-money-bill-wave nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المصروفات{% else %}Expenses{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'advanced_expenses' else '' }}" href="#">
                    <i class="fas fa-receipt nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المصروفات المتقدمة{% else %}Advanced Expenses{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'payments_dues' else '' }}" href="#">
                    <i class="fas fa-credit-card nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}المدفوعات والمستحقات{% else %}Payments & Dues{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'financial_statements' else '' }}" href="#">
                    <i class="fas fa-file-invoice-dollar nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}القوائم المالية{% else %}Financial Statements{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'tax_management' else '' }}" href="#">
                    <i class="fas fa-percentage nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}إدارة الضرائب{% else %}Tax Management{% endif %}
                </a>
            </div>

            <!-- الموارد البشرية -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}الموارد البشرية{% else %}Human Resources{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'employee_payroll' else '' }}" href="#">
                    <i class="fas fa-user-tie nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}رواتب الموظفين{% else %}Employee Payroll{% endif %}
                </a>
            </div>

            <!-- التقارير والتحليلات -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}التقارير والتحليلات{% else %}Reports & Analytics{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'reports' else '' }}" href="#">
                    <i class="fas fa-chart-bar nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}التقارير{% else %}Reports{% endif %}
                </a>
            </div>

            <!-- الإدارة والإعدادات -->
            <div class="nav-section">
                <div class="nav-section-title">
                    {% if session.get('language', 'ar') == 'ar' %}الإدارة والإعدادات{% else %}Administration & Settings{% endif %}
                </div>
                <a class="nav-link {{ 'active' if request.endpoint == 'user_management' else '' }}" href="#">
                    <i class="fas fa-users-cog nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}إدارة المستخدمين{% else %}User Management{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'role_management' else '' }}" href="#">
                    <i class="fas fa-user-shield nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}إدارة الأدوار{% else %}Role Management{% endif %}
                </a>
                <a class="nav-link {{ 'active' if request.endpoint == 'settings' else '' }}" href="#">
                    <i class="fas fa-cog nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}الإعدادات{% else %}Settings{% endif %}
                </a>
            </div>

            <!-- تسجيل الخروج -->
            <div class="nav-section">
                <a class="nav-link" href="{{ url_for('logout') }}" style="color: var(--gray-600);">
                    <i class="fas fa-sign-out-alt nav-icon"></i>
                    {% if session.get('language', 'ar') == 'ar' %}تسجيل الخروج{% else %}Logout{% endif %}
                </a>
            </div>
        </div>'''
    
    return sidebar_html

def update_base_template():
    """تحديث قالب base.html بالقائمة الجانبية الشاملة"""
    print("📝 تحديث قالب base.html بالقائمة الجانبية الشاملة...")
    
    # قراءة الملف الحالي
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن القائمة الجانبية الحالية واستبدالها
    start_marker = '<div class="sidebar-nav">'
    end_marker = '</div>\n    </nav>'
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)
    
    if start_index != -1 and end_index != -1:
        # استبدال القائمة الجانبية
        new_sidebar = create_complete_sidebar_html()
        new_content = (
            content[:start_index] + 
            new_sidebar + '\n    ' +
            content[end_index:]
        )
        
        # حفظ الملف المحدث
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ تم تحديث القائمة الجانبية بنجاح")
        return True
    else:
        print("❌ لم يتم العثور على القائمة الجانبية في الملف")
        return False

def create_sidebar_summary():
    """إنشاء ملخص القائمة الجانبية الجديدة"""
    summary = '''# 📋 القائمة الجانبية الشاملة - ملخص الشاشات

## 🏠 لوحة التحكم الرئيسية
- لوحة التحكم

## 🌟 الشاشات المتقدمة والمميزة
- 🌟 إدارة المنتجات والتكاليف (الشاشة الموحدة)
- حساب التكاليف
- حاسبة تكلفة الوجبات
- التقارير المتقدمة

## 💰 المبيعات والفواتير
- فاتورة جديدة
- المبيعات
- الطلبات

## 📦 المخزون والمنتجات
- المنتجات
- المواد الخام
- إدارة المخزون
- نقل المنتجات

## 🛒 المشتريات والموردين
- المشتريات
- الموردين

## 👥 العملاء والعلاقات
- العملاء

## 💳 المالية والمحاسبة
- المصروفات
- المصروفات المتقدمة
- المدفوعات والمستحقات
- القوائم المالية
- إدارة الضرائب

## 👔 الموارد البشرية
- رواتب الموظفين

## 📊 التقارير والتحليلات
- التقارير

## ⚙️ الإدارة والإعدادات
- إدارة المستخدمين
- إدارة الأدوار
- الإعدادات

## 🚪 تسجيل الخروج
- تسجيل الخروج

---

**إجمالي الشاشات**: 25 شاشة
**الأقسام**: 10 أقسام منظمة
**الشاشة المميزة**: إدارة المنتجات والتكاليف (الشاشة الموحدة)

## 🎨 المميزات:
- تصنيف منطقي للشاشات
- أيقونات مميزة لكل شاشة
- تمييز خاص للشاشة الموحدة
- دعم اللغتين العربية والإنجليزية
- تصميم نظيف ومنظم
'''
    
    with open('COMPLETE_SIDEBAR_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✅ تم إنشاء ملخص القائمة الجانبية")

def main():
    """تشغيل تحديث القائمة الجانبية"""
    print("📋 بدء تحديث القائمة الجانبية الشاملة")
    print("=" * 60)
    
    # تحديث قالب base.html
    if update_base_template():
        print("✅ تم تحديث القائمة الجانبية بنجاح")
    else:
        print("❌ فشل في تحديث القائمة الجانبية")
        return
    
    # إنشاء ملخص
    create_sidebar_summary()
    
    print("\n" + "=" * 60)
    print("🎉 تم إنجاز تحديث القائمة الجانبية!")
    print("=" * 60)
    
    print("\n📊 إحصائيات القائمة الجانبية:")
    print("📋 إجمالي الشاشات: 25 شاشة")
    print("📂 عدد الأقسام: 10 أقسام")
    print("🌟 الشاشة المميزة: إدارة المنتجات والتكاليف")
    
    print("\n📂 الأقسام الجديدة:")
    print("🏠 لوحة التحكم الرئيسية")
    print("🌟 الشاشات المتقدمة والمميزة")
    print("💰 المبيعات والفواتير")
    print("📦 المخزون والمنتجات")
    print("🛒 المشتريات والموردين")
    print("👥 العملاء والعلاقات")
    print("💳 المالية والمحاسبة")
    print("👔 الموارد البشرية")
    print("📊 التقارير والتحليلات")
    print("⚙️ الإدارة والإعدادات")
    
    print("\n🧪 للاختبار:")
    print("🌐 شغل التطبيق: python app.py")
    print("🌐 افتح: http://localhost:5000")
    print("👤 سجل الدخول: admin / admin123")
    print("📋 تحقق من القائمة الجانبية الجديدة")
    print("=" * 60)

if __name__ == "__main__":
    main()
