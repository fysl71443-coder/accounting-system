#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة المراجعة الذكية للنظام المحاسبي
Smart Audit Tool for Accounting System

هذه الأداة تقوم بفحص ومراجعة جميع شاشات النظام المحاسبي
وتوليد تقرير شامل عن حالة التطوير والأزرار التفاعلية
"""

import os
import re
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class SystemAuditTool:
    """أداة المراجعة الذكية للنظام المحاسبي"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("أداة المراجعة الذكية للنظام المحاسبي - Smart System Audit Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # متغيرات النظام
        self.system_path = Path.cwd()
        self.templates_path = self.system_path / "templates"
        self.static_path = self.system_path / "static"
        self.app_file = self.system_path / "app.py"
        
        # بيانات الشاشات المطلوب فحصها
        self.required_screens = {
            'login': {
                'name_ar': 'تسجيل الدخول',
                'name_en': 'Login',
                'template': 'login.html',
                'route': '/login',
                'required_functions': ['login_user', 'validate_credentials']
            },
            'dashboard': {
                'name_ar': 'الشاشة الرئيسية',
                'name_en': 'Dashboard',
                'template': 'dashboard.html',
                'route': '/dashboard',
                'required_functions': ['load_dashboard_data', 'get_statistics']
            },
            'purchases': {
                'name_ar': 'المشتريات',
                'name_en': 'Purchases',
                'template': 'purchases.html',
                'route': '/purchases',
                'required_functions': ['add_purchase', 'edit_purchase', 'delete_purchase']
            },
            'inventory': {
                'name_ar': 'المخزون',
                'name_en': 'Inventory',
                'template': 'inventory.html',
                'route': '/inventory',
                'required_functions': ['add_item', 'update_stock', 'generate_report']
            },
            'products': {
                'name_ar': 'الأصناف والمنتجات',
                'name_en': 'Products & Items',
                'template': 'products.html',
                'route': '/products',
                'required_functions': ['add_product', 'edit_product', 'calculate_cost']
            },
            'sales': {
                'name_ar': 'المبيعات',
                'name_en': 'Sales',
                'template': 'sales.html',
                'route': '/sales',
                'required_functions': ['create_invoice', 'process_payment', 'print_receipt']
            },
            'suppliers': {
                'name_ar': 'الموردين',
                'name_en': 'Suppliers',
                'template': 'suppliers.html',
                'route': '/suppliers',
                'required_functions': ['add_supplier', 'edit_supplier', 'view_transactions']
            },
            'employee_payroll': {
                'name_ar': 'الموظفين والرواتب',
                'name_en': 'Employees & Payroll',
                'template': 'employee_payroll.html',
                'route': '/employee_payroll',
                'required_functions': ['add_employee', 'process_payroll', 'generate_payslip']
            },
            'reports': {
                'name_ar': 'التقارير',
                'name_en': 'Reports',
                'template': 'reports.html',
                'route': '/reports',
                'required_functions': ['generate_report', 'export_pdf', 'filter_data']
            },
            'payments_dues': {
                'name_ar': 'المدفوعات والمستحقات',
                'name_en': 'Payments & Dues',
                'template': 'payments_dues.html',
                'route': '/payments_dues',
                'required_functions': ['record_payment', 'track_dues', 'send_reminder']
            },
            'advanced_expenses': {
                'name_ar': 'المصروفات المتقدمة',
                'name_en': 'Advanced Expenses',
                'template': 'advanced_expenses.html',
                'route': '/advanced_expenses',
                'required_functions': ['add_expense', 'categorize_expense', 'approve_expense']
            },
            'tax_management': {
                'name_ar': 'ضريبة القيمة المضافة',
                'name_en': 'VAT Management',
                'template': 'tax_management.html',
                'route': '/tax_management',
                'required_functions': ['calculate_vat', 'generate_return', 'submit_return']
            },
            'users': {
                'name_ar': 'المستخدمين والصلاحيات',
                'name_en': 'Users & Permissions',
                'template': 'users.html',
                'route': '/users',
                'required_functions': ['add_user', 'set_permissions', 'manage_roles']
            },
            'settings': {
                'name_ar': 'الإعدادات العامة',
                'name_en': 'General Settings',
                'template': 'settings.html',
                'route': '/settings',
                'required_functions': ['update_settings', 'backup_data', 'restore_data']
            },
            'financial_statements': {
                'name_ar': 'القوائم المالية',
                'name_en': 'Financial Statements',
                'template': 'financial_statements.html',
                'route': '/financial_statements',
                'required_functions': ['generate_balance_sheet', 'income_statement', 'cash_flow']
            }
        }
        
        # نتائج الفحص
        self.audit_results = {}
        
        # إنشاء الواجهة
        self.create_interface()
        
    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🔍 أداة المراجعة الذكية للنظام المحاسبي\nSmart Audit Tool for Accounting System",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50',
            justify='center'
        )
        title_label.pack(expand=True)
        
        # إطار الأزرار
        buttons_frame = tk.Frame(self.root, bg='#ecf0f1', height=60)
        buttons_frame.pack(fill='x', padx=10, pady=5)
        buttons_frame.pack_propagate(False)
        
        # أزرار التحكم
        tk.Button(
            buttons_frame,
            text="🔍 بدء الفحص الشامل\nStart Full Audit",
            command=self.start_full_audit,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        ).pack(side='left', padx=5, pady=10)
        
        tk.Button(
            buttons_frame,
            text="📊 تقرير مفصل\nDetailed Report",
            command=self.generate_detailed_report,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        ).pack(side='left', padx=5, pady=10)
        
        tk.Button(
            buttons_frame,
            text="🔧 إصلاح تلقائي\nAuto Fix",
            command=self.auto_fix_issues,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        ).pack(side='left', padx=5, pady=10)
        
        tk.Button(
            buttons_frame,
            text="📄 تصدير PDF\nExport PDF",
            command=self.export_pdf_report,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        ).pack(side='left', padx=5, pady=10)
        
        tk.Button(
            buttons_frame,
            text="📊 تصدير Excel\nExport Excel",
            command=self.export_excel_report,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        ).pack(side='left', padx=5, pady=10)
        
        # إطار النتائج
        results_frame = tk.Frame(self.root, bg='#ecf0f1')
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # جدول النتائج
        columns = ('الشاشة', 'الحالة', 'القالب', 'الرابط', 'الأزرار', 'المشاكل', 'التوصيات')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=20)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150, anchor='center')
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # شريط الحالة
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز للفحص - Ready for audit")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='#bdc3c7',
            font=('Arial', 9)
        )
        status_bar.pack(side='bottom', fill='x')
        
    def update_status(self, message: str):
        """تحديث شريط الحالة"""
        self.status_var.set(f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update()
        
    def start_full_audit(self):
        """بدء الفحص الشامل للنظام"""
        self.update_status("بدء الفحص الشامل...")
        
        # مسح النتائج السابقة
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.audit_results = {}
        
        # فحص كل شاشة
        for screen_id, screen_info in self.required_screens.items():
            self.update_status(f"فحص شاشة: {screen_info['name_ar']}")
            result = self.audit_screen(screen_id, screen_info)
            self.audit_results[screen_id] = result
            self.add_result_to_tree(screen_id, result)
        
        self.update_status(f"تم الانتهاء من الفحص - فحص {len(self.required_screens)} شاشة")
        messagebox.showinfo("اكتمال الفحص", f"تم فحص {len(self.required_screens)} شاشة بنجاح!")

    def audit_screen(self, screen_id: str, screen_info: Dict) -> Dict:
        """فحص شاشة واحدة"""
        result = {
            'screen_id': screen_id,
            'name_ar': screen_info['name_ar'],
            'name_en': screen_info['name_en'],
            'template_exists': False,
            'route_exists': False,
            'functions_implemented': [],
            'missing_functions': [],
            'buttons_found': [],
            'broken_buttons': [],
            'translation_support': False,
            'database_connected': False,
            'issues': [],
            'recommendations': [],
            'completion_percentage': 0,
            'status': 'غير مكتملة'
        }

        # فحص وجود القالب
        template_path = self.templates_path / screen_info['template']
        if template_path.exists():
            result['template_exists'] = True
            result['template_content'] = self.analyze_template(template_path)
        else:
            result['issues'].append(f"القالب غير موجود: {screen_info['template']}")
            result['recommendations'].append(f"إنشاء قالب: {screen_info['template']}")

        # فحص وجود الرابط في app.py
        if self.app_file.exists():
            app_content = self.app_file.read_text(encoding='utf-8')
            if screen_info['route'] in app_content:
                result['route_exists'] = True
            else:
                result['issues'].append(f"الرابط غير موجود: {screen_info['route']}")
                result['recommendations'].append(f"إضافة رابط: {screen_info['route']}")

        # فحص الوظائف المطلوبة
        for func in screen_info['required_functions']:
            if self.check_function_exists(func):
                result['functions_implemented'].append(func)
            else:
                result['missing_functions'].append(func)
                result['issues'].append(f"الوظيفة غير مطبقة: {func}")
                result['recommendations'].append(f"تطبيق الوظيفة: {func}")

        # حساب نسبة الاكتمال
        total_checks = 5  # template, route, functions, translation, database
        completed_checks = 0

        if result['template_exists']:
            completed_checks += 1
        if result['route_exists']:
            completed_checks += 1
        if len(result['functions_implemented']) > 0:
            completed_checks += len(result['functions_implemented']) / len(screen_info['required_functions'])

        result['completion_percentage'] = int((completed_checks / total_checks) * 100)

        if result['completion_percentage'] >= 80:
            result['status'] = 'مكتملة ✅'
        elif result['completion_percentage'] >= 50:
            result['status'] = 'قيد التطوير 🔄'
        else:
            result['status'] = 'غير مكتملة ❌'

        return result

    def analyze_template(self, template_path: Path) -> Dict:
        """تحليل محتوى القالب"""
        try:
            content = template_path.read_text(encoding='utf-8')

            analysis = {
                'has_forms': bool(re.search(r'<form', content, re.IGNORECASE)),
                'has_tables': bool(re.search(r'<table', content, re.IGNORECASE)),
                'has_buttons': len(re.findall(r'<button|<input[^>]*type=["\']button', content, re.IGNORECASE)),
                'has_modals': bool(re.search(r'modal', content, re.IGNORECASE)),
                'has_javascript': bool(re.search(r'<script|onclick=', content, re.IGNORECASE)),
                'has_arabic': bool(re.search(r'[\u0600-\u06FF]', content)),
                'has_english': bool(re.search(r'[a-zA-Z]', content)),
                'button_functions': self.extract_button_functions(content),
                'missing_elements': []
            }

            # فحص العناصر المفقودة
            if not analysis['has_forms']:
                analysis['missing_elements'].append('نماذج الإدخال')
            if not analysis['has_tables']:
                analysis['missing_elements'].append('جداول البيانات')
            if analysis['has_buttons'] < 3:
                analysis['missing_elements'].append('أزرار كافية')
            if not analysis['has_javascript']:
                analysis['missing_elements'].append('وظائف JavaScript')

            return analysis

        except Exception as e:
            return {'error': str(e)}

    def extract_button_functions(self, content: str) -> List[Dict]:
        """استخراج وظائف الأزرار من المحتوى"""
        buttons = []

        # البحث عن الأزرار مع onclick
        onclick_pattern = r'onclick=["\']([^"\']+)["\']'
        onclick_matches = re.findall(onclick_pattern, content, re.IGNORECASE)

        for match in onclick_matches:
            function_name = match.split('(')[0].strip()
            buttons.append({
                'function': function_name,
                'type': 'onclick',
                'implemented': self.check_function_exists(function_name)
            })

        # البحث عن أزرار النماذج
        form_buttons = re.findall(r'<button[^>]*type=["\']submit["\'][^>]*>([^<]+)</button>', content, re.IGNORECASE)
        for button_text in form_buttons:
            buttons.append({
                'function': 'form_submit',
                'type': 'submit',
                'text': button_text.strip(),
                'implemented': True
            })

        return buttons

    def check_function_exists(self, function_name: str) -> bool:
        """فحص وجود الوظيفة في الملفات"""
        try:
            # فحص في app.py
            if self.app_file.exists():
                app_content = self.app_file.read_text(encoding='utf-8')
                if f"def {function_name}" in app_content or f"function {function_name}" in app_content:
                    return True

            # فحص في ملفات JavaScript
            js_files = list(self.static_path.glob('**/*.js')) if self.static_path.exists() else []
            for js_file in js_files:
                try:
                    js_content = js_file.read_text(encoding='utf-8')
                    if f"function {function_name}" in js_content or f"{function_name} =" in js_content:
                        return True
                except:
                    continue

            # فحص في القوالب
            template_files = list(self.templates_path.glob('*.html')) if self.templates_path.exists() else []
            for template_file in template_files:
                try:
                    template_content = template_file.read_text(encoding='utf-8')
                    if f"function {function_name}" in template_content:
                        return True
                except:
                    continue

            return False

        except Exception:
            return False

    def add_result_to_tree(self, screen_id: str, result: Dict):
        """إضافة نتيجة الفحص إلى الجدول"""
        template_status = "✅" if result['template_exists'] else "❌"
        route_status = "✅" if result['route_exists'] else "❌"

        buttons_count = len(result.get('template_content', {}).get('button_functions', []))
        issues_count = len(result['issues'])

        self.results_tree.insert('', 'end', values=(
            result['name_ar'],
            result['status'],
            template_status,
            route_status,
            f"{buttons_count} أزرار",
            f"{issues_count} مشاكل",
            f"{len(result['recommendations'])} توصيات"
        ))

    def generate_detailed_report(self):
        """توليد تقرير مفصل"""
        if not self.audit_results:
            messagebox.showwarning("تحذير", "يرجى تشغيل الفحص أولاً")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title("التقرير المفصل - Detailed Report")
        report_window.geometry("1000x700")

        # إطار النص
        text_frame = tk.Frame(report_window)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # منطقة النص مع شريط التمرير
        text_widget = tk.Text(text_frame, wrap='word', font=('Arial', 10))
        scrollbar_text = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_text.set)

        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar_text.pack(side='right', fill='y')

        # توليد محتوى التقرير
        report_content = self.generate_report_content()
        text_widget.insert('1.0', report_content)
        text_widget.config(state='disabled')

    def generate_report_content(self) -> str:
        """توليد محتوى التقرير"""
        report = []
        report.append("=" * 80)
        report.append("تقرير المراجعة الشامل للنظام المحاسبي")
        report.append("Comprehensive Audit Report for Accounting System")
        report.append("=" * 80)
        report.append(f"تاريخ التقرير: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"عدد الشاشات المفحوصة: {len(self.audit_results)}")
        report.append("")

        # إحصائيات عامة
        completed_screens = sum(1 for r in self.audit_results.values() if r['completion_percentage'] >= 80)
        in_progress_screens = sum(1 for r in self.audit_results.values() if 50 <= r['completion_percentage'] < 80)
        incomplete_screens = sum(1 for r in self.audit_results.values() if r['completion_percentage'] < 50)

        report.append("📊 الإحصائيات العامة:")
        report.append(f"   الشاشات المكتملة: {completed_screens}")
        report.append(f"   الشاشات قيد التطوير: {in_progress_screens}")
        report.append(f"   الشاشات غير المكتملة: {incomplete_screens}")
        report.append("")

        # تفاصيل كل شاشة
        for screen_id, result in self.audit_results.items():
            report.append("-" * 60)
            report.append(f"🖥️ الشاشة: {result['name_ar']} ({result['name_en']})")
            report.append(f"   الحالة: {result['status']}")
            report.append(f"   نسبة الاكتمال: {result['completion_percentage']}%")
            report.append(f"   القالب موجود: {'✅' if result['template_exists'] else '❌'}")
            report.append(f"   الرابط موجود: {'✅' if result['route_exists'] else '❌'}")

            if result['functions_implemented']:
                report.append(f"   الوظائف المطبقة: {', '.join(result['functions_implemented'])}")

            if result['missing_functions']:
                report.append(f"   الوظائف المفقودة: {', '.join(result['missing_functions'])}")

            if result['issues']:
                report.append("   🚨 المشاكل:")
                for issue in result['issues']:
                    report.append(f"      - {issue}")

            if result['recommendations']:
                report.append("   💡 التوصيات:")
                for rec in result['recommendations']:
                    report.append(f"      - {rec}")

            report.append("")

        return "\n".join(report)

    def auto_fix_issues(self):
        """الإصلاح التلقائي للمشاكل"""
        if not self.audit_results:
            messagebox.showwarning("تحذير", "يرجى تشغيل الفحص أولاً")
            return

        if not messagebox.askyesno("تأكيد الإصلاح", "هل تريد المتابعة مع الإصلاح التلقائي؟\nسيتم إنشاء ملفات جديدة وتعديل الموجود"):
            return

        fixed_issues = 0

        for screen_id, result in self.audit_results.items():
            screen_info = self.required_screens[screen_id]

            # إنشاء القالب المفقود
            if not result['template_exists']:
                self.create_missing_template(screen_id, screen_info)
                fixed_issues += 1
                self.update_status(f"تم إنشاء قالب: {screen_info['template']}")

            # إضافة الرابط المفقود
            if not result['route_exists']:
                self.add_missing_route(screen_id, screen_info)
                fixed_issues += 1
                self.update_status(f"تم إضافة رابط: {screen_info['route']}")

            # إنشاء الوظائف المفقودة
            for func in result['missing_functions']:
                self.create_missing_function(func, screen_id)
                fixed_issues += 1
                self.update_status(f"تم إنشاء وظيفة: {func}")

        messagebox.showinfo("اكتمال الإصلاح", f"تم إصلاح {fixed_issues} مشكلة")

        # إعادة تشغيل الفحص
        self.start_full_audit()

    def create_missing_template(self, screen_id: str, screen_info: Dict):
        """إنشاء قالب مفقود"""
        template_content = f'''
{{% extends "base_simple.html" %}}

{{% block title %}}
    {{% if session.get('language', 'ar') == 'ar' %}}
        {screen_info['name_ar']}
    {{% else %}}
        {screen_info['name_en']}
    {{% endif %}}
{{% endblock %}}

{{% block content %}}
<div class="container-fluid">
    <!-- Page Header -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            {{% if session.get('language', 'ar') == 'ar' %}}
                <i class="fas fa-cog"></i> {screen_info['name_ar']}
            {{% else %}}
                <i class="fas fa-cog"></i> {screen_info['name_en']}
            {{% endif %}}
        </h1>
        <div class="btn-group" role="group">
            <button type="button" class="btn btn-primary" onclick="addNew()">
                {{% if session.get('language', 'ar') == 'ar' %}}
                    <i class="fas fa-plus"></i> إضافة جديد
                {{% else %}}
                    <i class="fas fa-plus"></i> Add New
                {{% endif %}}
            </button>
            <button type="button" class="btn btn-success" onclick="exportData()">
                {{% if session.get('language', 'ar') == 'ar' %}}
                    <i class="fas fa-download"></i> تصدير
                {{% else %}}
                    <i class="fas fa-download"></i> Export
                {{% endif %}}
            </button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h6 class="m-0 font-weight-bold text-primary">
                        {{% if session.get('language', 'ar') == 'ar' %}}
                            {screen_info['name_ar']}
                        {{% else %}}
                            {screen_info['name_en']}
                        {{% endif %}}
                    </h6>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="dataTable">
                            <thead>
                                <tr>
                                    <th>{{% if session.get('language', 'ar') == 'ar' %}}الرقم{{% else %}}ID{{% endif %}}</th>
                                    <th>{{% if session.get('language', 'ar') == 'ar' %}}الاسم{{% else %}}Name{{% endif %}}</th>
                                    <th>{{% if session.get('language', 'ar') == 'ar' %}}التاريخ{{% else %}}Date{{% endif %}}</th>
                                    <th>{{% if session.get('language', 'ar') == 'ar' %}}الإجراءات{{% else %}}Actions{{% endif %}}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Data will be loaded here -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}

{{% block extra_js %}}
<script>
// JavaScript functions for {screen_info['name_en']}
function addNew() {{
    alert('{{% if session.get("language", "ar") == "ar" %}}إضافة جديد{{% else %}}Add New{{% endif %}}');
}}

function editItem(id) {{
    alert('{{% if session.get("language", "ar") == "ar" %}}تعديل العنصر: {{% else %}}Edit item: {{% endif %}}' + id);
}}

function deleteItem(id) {{
    if (confirm('{{% if session.get("language", "ar") == "ar" %}}هل تريد حذف هذا العنصر؟{{% else %}}Are you sure you want to delete this item?{{% endif %}}')) {{
        alert('{{% if session.get("language", "ar") == "ar" %}}تم الحذف{{% else %}}Deleted{{% endif %}}');
    }}
}}

function exportData() {{
    alert('{{% if session.get("language", "ar") == "ar" %}}تصدير البيانات{{% else %}}Export Data{{% endif %}}');
}}

// Initialize page
$(document).ready(function() {{
    console.log('{screen_info['name_en']} page loaded');
}});
</script>
{{% endblock %}}
'''

        template_path = self.templates_path / screen_info['template']
        template_path.write_text(template_content, encoding='utf-8')

    def add_missing_route(self, screen_id: str, screen_info: Dict):
        """إضافة رابط مفقود إلى app.py"""
        if not self.app_file.exists():
            return

        app_content = self.app_file.read_text(encoding='utf-8')

        # إنشاء الرابط الجديد
        route_code = f'''
@app.route('{screen_info['route']}')
@login_required
def {screen_id}():
    """{screen_info['name_ar']}"""
    return render_template('{screen_info['template']}')
'''

        # البحث عن مكان الإدراج (قبل if __name__ == '__main__':)
        if "if __name__ == '__main__':" in app_content:
            app_content = app_content.replace(
                "if __name__ == '__main__':",
                route_code + "\nif __name__ == '__main__':"
            )
        else:
            app_content += route_code

        self.app_file.write_text(app_content, encoding='utf-8')

    def create_missing_function(self, function_name: str, screen_id: str):
        """إنشاء وظيفة مفقودة"""
        # إنشاء وظيفة JavaScript أساسية
        js_function = f'''
function {function_name}() {{
    // TODO: Implement {function_name} for {screen_id}
    console.log('Function {function_name} called');
    alert('Function {function_name} - تحت التطوير');
}}
'''

        # إضافة الوظيفة إلى ملف JavaScript منفصل أو إلى القالب
        js_file_path = self.static_path / 'js' / f'{screen_id}.js'

        if not js_file_path.parent.exists():
            js_file_path.parent.mkdir(parents=True, exist_ok=True)

        if js_file_path.exists():
            existing_content = js_file_path.read_text(encoding='utf-8')
            if function_name not in existing_content:
                js_file_path.write_text(existing_content + js_function, encoding='utf-8')
        else:
            js_file_path.write_text(js_function, encoding='utf-8')

    def export_excel_report(self):
        """تصدير التقرير إلى Excel"""
        if not self.audit_results:
            messagebox.showwarning("تحذير", "يرجى تشغيل الفحص أولاً")
            return

        try:
            # إعداد البيانات للتصدير
            data = []
            for screen_id, result in self.audit_results.items():
                data.append({
                    'الشاشة (عربي)': result['name_ar'],
                    'الشاشة (إنجليزي)': result['name_en'],
                    'الحالة': result['status'],
                    'نسبة الاكتمال': f"{result['completion_percentage']}%",
                    'القالب موجود': 'نعم' if result['template_exists'] else 'لا',
                    'الرابط موجود': 'نعم' if result['route_exists'] else 'لا',
                    'الوظائف المطبقة': len(result['functions_implemented']),
                    'الوظائف المفقودة': len(result['missing_functions']),
                    'عدد المشاكل': len(result['issues']),
                    'عدد التوصيات': len(result['recommendations'])
                })

            # إنشاء DataFrame
            df = pd.DataFrame(data)

            # اختيار مكان الحفظ
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="حفظ تقرير Excel"
            )

            if file_path:
                df.to_excel(file_path, index=False, engine='openpyxl')
                messagebox.showinfo("نجح التصدير", f"تم حفظ التقرير في:\n{file_path}")

        except Exception as e:
            messagebox.showerror("خطأ في التصدير", f"حدث خطأ أثناء التصدير:\n{str(e)}")

    def export_pdf_report(self):
        """تصدير التقرير إلى PDF"""
        if not self.audit_results:
            messagebox.showwarning("تحذير", "يرجى تشغيل الفحص أولاً")
            return

        try:
            # اختيار مكان الحفظ
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="حفظ تقرير PDF"
            )

            if file_path:
                self.create_pdf_report(file_path)
                messagebox.showinfo("نجح التصدير", f"تم حفظ التقرير في:\n{file_path}")

        except Exception as e:
            messagebox.showerror("خطأ في التصدير", f"حدث خطأ أثناء التصدير:\n{str(e)}")

    def create_pdf_report(self, file_path: str):
        """إنشاء تقرير PDF"""
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # العنوان
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )

        story.append(Paragraph("تقرير المراجعة الشامل للنظام المحاسبي", title_style))
        story.append(Paragraph("Comprehensive Audit Report", title_style))
        story.append(Spacer(1, 20))

        # معلومات التقرير
        info_data = [
            ['تاريخ التقرير', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['عدد الشاشات', str(len(self.audit_results))],
            ['الشاشات المكتملة', str(sum(1 for r in self.audit_results.values() if r['completion_percentage'] >= 80))],
            ['الشاشات قيد التطوير', str(sum(1 for r in self.audit_results.values() if 50 <= r['completion_percentage'] < 80))],
            ['الشاشات غير المكتملة', str(sum(1 for r in self.audit_results.values() if r['completion_percentage'] < 50))]
        ]

        info_table = Table(info_data, colWidths=[200, 200])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(info_table)
        story.append(Spacer(1, 30))

        # جدول النتائج
        table_data = [['الشاشة', 'الحالة', 'نسبة الاكتمال', 'المشاكل', 'التوصيات']]

        for result in self.audit_results.values():
            table_data.append([
                result['name_ar'],
                result['status'],
                f"{result['completion_percentage']}%",
                str(len(result['issues'])),
                str(len(result['recommendations']))
            ])

        results_table = Table(table_data, colWidths=[120, 80, 80, 60, 80])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))

        story.append(results_table)

        # بناء المستند
        doc.build(story)

    def run(self):
        """تشغيل الأداة"""
        self.root.mainloop()

def main():
    """الوظيفة الرئيسية"""
    try:
        app = SystemAuditTool()
        app.run()
    except Exception as e:
        print(f"خطأ في تشغيل الأداة: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل الأداة:\n{str(e)}")

if __name__ == "__main__":
    main()
