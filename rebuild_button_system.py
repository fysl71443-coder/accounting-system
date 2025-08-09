#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Button System Rebuild for Accounting Application
إعادة بناء نظام الأزرار الكامل لتطبيق المحاسبة
"""

import os
import json
from pathlib import Path
from datetime import datetime

class ButtonSystemBuilder:
    def __init__(self):
        self.templates_dir = Path('templates')
        self.static_dir = Path('static')
        self.js_dir = self.static_dir / 'js'
        self.css_dir = self.static_dir / 'css'
        
        # Create directories if they don't exist
        self.js_dir.mkdir(parents=True, exist_ok=True)
        self.css_dir.mkdir(parents=True, exist_ok=True)
        
        # Button configurations for each screen
        self.button_configs = {
            'sales': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnPreview', 'text': {'ar': 'معاينة', 'en': 'Preview'}, 'icon': 'eye', 'class': 'btn-info', 'handler': 'PreviewRecord'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'},
                    {'id': 'btnSelectInvoice', 'text': {'ar': 'اختيار فاتورة', 'en': 'Select Invoice'}, 'icon': 'search', 'class': 'btn-secondary', 'handler': 'SelectInvoice'},
                    {'id': 'btnRegisterPayment', 'text': {'ar': 'تسجيل دفعة', 'en': 'Register Payment'}, 'icon': 'credit-card', 'class': 'btn-success', 'handler': 'RegisterPayment'}
                ]
            },
            'purchases': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnPreview', 'text': {'ar': 'معاينة', 'en': 'Preview'}, 'icon': 'eye', 'class': 'btn-info', 'handler': 'PreviewRecord'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'},
                    {'id': 'btnSelectInvoice', 'text': {'ar': 'اختيار فاتورة', 'en': 'Select Invoice'}, 'icon': 'search', 'class': 'btn-secondary', 'handler': 'SelectInvoice'},
                    {'id': 'btnRegisterPayment', 'text': {'ar': 'تسجيل دفعة', 'en': 'Register Payment'}, 'icon': 'credit-card', 'class': 'btn-success', 'handler': 'RegisterPayment'}
                ]
            },
            'products': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnSearch', 'text': {'ar': 'بحث', 'en': 'Search'}, 'icon': 'search', 'class': 'btn-info', 'handler': 'SearchRecords'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            },
            'payments': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'},
                    {'id': 'btnRegisterPayment', 'text': {'ar': 'تسجيل دفعة', 'en': 'Register Payment'}, 'icon': 'credit-card', 'class': 'btn-success', 'handler': 'RegisterPayment'}
                ]
            },
            'employees': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnSearch', 'text': {'ar': 'بحث', 'en': 'Search'}, 'icon': 'search', 'class': 'btn-info', 'handler': 'SearchRecords'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            },
            'reports': {
                'buttons': [
                    {'id': 'btnPreview', 'text': {'ar': 'معاينة', 'en': 'Preview'}, 'icon': 'eye', 'class': 'btn-info', 'handler': 'PreviewReport'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintReport'},
                    {'id': 'btnExport', 'text': {'ar': 'تصدير', 'en': 'Export'}, 'icon': 'download', 'class': 'btn-success', 'handler': 'ExportReport'}
                ]
            },
            'advanced_reports': {
                'buttons': [
                    {'id': 'btnPreview', 'text': {'ar': 'معاينة', 'en': 'Preview'}, 'icon': 'eye', 'class': 'btn-info', 'handler': 'PreviewReport'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintReport'},
                    {'id': 'btnExport', 'text': {'ar': 'تصدير', 'en': 'Export'}, 'icon': 'download', 'class': 'btn-success', 'handler': 'ExportReport'}
                ]
            },
            'taxes': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            },
            'financial_statements': {
                'buttons': [
                    {'id': 'btnPreview', 'text': {'ar': 'معاينة', 'en': 'Preview'}, 'icon': 'eye', 'class': 'btn-info', 'handler': 'PreviewReport'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintReport'},
                    {'id': 'btnExport', 'text': {'ar': 'تصدير', 'en': 'Export'}, 'icon': 'download', 'class': 'btn-success', 'handler': 'ExportReport'}
                ]
            },
            'expenses': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            },
            'suppliers': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnSearch', 'text': {'ar': 'بحث', 'en': 'Search'}, 'icon': 'search', 'class': 'btn-info', 'handler': 'SearchRecords'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            },
            'customers': {
                'buttons': [
                    {'id': 'btnSave', 'text': {'ar': 'حفظ', 'en': 'Save'}, 'icon': 'save', 'class': 'btn-success', 'handler': 'SaveRecord'},
                    {'id': 'btnEdit', 'text': {'ar': 'تعديل', 'en': 'Edit'}, 'icon': 'edit', 'class': 'btn-warning', 'handler': 'EditRecord'},
                    {'id': 'btnDelete', 'text': {'ar': 'حذف', 'en': 'Delete'}, 'icon': 'trash', 'class': 'btn-danger', 'handler': 'DeleteRecord'},
                    {'id': 'btnSearch', 'text': {'ar': 'بحث', 'en': 'Search'}, 'icon': 'search', 'class': 'btn-info', 'handler': 'SearchRecords'},
                    {'id': 'btnPrint', 'text': {'ar': 'طباعة', 'en': 'Print'}, 'icon': 'print', 'class': 'btn-primary', 'handler': 'PrintRecord'}
                ]
            }
        }
    
    def create_button_html_template(self, screen_name):
        """Create HTML template for buttons"""
        config = self.button_configs.get(screen_name, {})
        buttons = config.get('buttons', [])
        
        html = f'''<!-- Button System for {screen_name.title()} Screen -->
<div class="button-toolbar mb-3" role="toolbar">
    <div class="btn-group me-2" role="group">
'''
        
        for button in buttons:
            html += f'''        <button type="button" 
                id="{button['id']}" 
                class="btn {button['class']} btn-sm"
                onclick="{screen_name}Handler.{button['handler']}()"
                data-bs-toggle="tooltip" 
                title="{{{{ session.get('language', 'ar') == 'ar' and '{button['text']['ar']}' or '{button['text']['en']}' }}}}">
            <i class="fas fa-{button['icon']} me-1"></i>
            {{{{ session.get('language', 'ar') == 'ar' and '{button['text']['ar']}' or '{button['text']['en']}' }}}}
        </button>
'''
        
        html += '''    </div>
</div>

<!-- Special Modals -->
'''
        
        # Add Register Payment Modal if needed
        if any(btn['id'] == 'btnRegisterPayment' for btn in buttons):
            html += self.create_payment_modal()
        
        # Add Select Invoice Modal if needed
        if any(btn['id'] == 'btnSelectInvoice' for btn in buttons):
            html += self.create_select_invoice_modal()
        
        return html
    
    def create_payment_modal(self):
        """Create payment registration modal"""
        return '''
<!-- Register Payment Modal -->
<div class="modal fade" id="paymentModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    {{ session.get('language', 'ar') == 'ar' and 'تسجيل دفعة' or 'Register Payment' }}
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="paymentForm">
                    <div class="mb-3">
                        <label class="form-label">
                            {{ session.get('language', 'ar') == 'ar' and 'المبلغ المدفوع' or 'Amount Paid' }}
                        </label>
                        <input type="number" class="form-control" id="amountPaid" step="0.01" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">
                            {{ session.get('language', 'ar') == 'ar' and 'طريقة الدفع' or 'Payment Method' }}
                        </label>
                        <select class="form-select" id="paymentMethod" required>
                            <option value="cash">{{ session.get('language', 'ar') == 'ar' and 'نقداً' or 'Cash' }}</option>
                            <option value="card">{{ session.get('language', 'ar') == 'ar' and 'بطاقة' or 'Card' }}</option>
                            <option value="bank_transfer">{{ session.get('language', 'ar') == 'ar' and 'تحويل بنكي' or 'Bank Transfer' }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">
                            {{ session.get('language', 'ar') == 'ar' and 'تاريخ الدفع' or 'Payment Date' }}
                        </label>
                        <input type="date" class="form-control" id="paymentDate" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">
                            {{ session.get('language', 'ar') == 'ar' and 'ملاحظات' or 'Notes' }}
                        </label>
                        <textarea class="form-control" id="notes" rows="3"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    {{ session.get('language', 'ar') == 'ar' and 'إلغاء' or 'Cancel' }}
                </button>
                <button type="button" class="btn btn-success" onclick="savePayment()">
                    {{ session.get('language', 'ar') == 'ar' and 'حفظ الدفعة' or 'Save Payment' }}
                </button>
            </div>
        </div>
    </div>
</div>
'''
    
    def create_select_invoice_modal(self):
        """Create select invoice modal"""
        return '''
<!-- Select Invoice Modal -->
<div class="modal fade" id="selectInvoiceModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    {{ session.get('language', 'ar') == 'ar' and 'اختيار فاتورة' or 'Select Invoice' }}
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="table-responsive">
                    <table class="table table-striped" id="invoicesTable">
                        <thead>
                            <tr>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'رقم الفاتورة' or 'Invoice Number' }}</th>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'التاريخ' or 'Date' }}</th>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'العميل' or 'Customer' }}</th>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'المبلغ' or 'Amount' }}</th>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'الحالة' or 'Status' }}</th>
                                <th>{{ session.get('language', 'ar') == 'ar' and 'اختيار' or 'Select' }}</th>
                            </tr>
                        </thead>
                        <tbody id="invoicesTableBody">
                            <!-- Invoices will be loaded here -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
'''

def main():
    """Main function to rebuild button system"""
    print("🔧 Starting Complete Button System Rebuild")
    print("=" * 60)
    
    builder = ButtonSystemBuilder()
    
    # Create button templates for each screen
    screens = list(builder.button_configs.keys())
    
    for screen in screens:
        print(f"📝 Creating button template for {screen}...")
        
        # Create button HTML template
        button_html = builder.create_button_html_template(screen)
        
        # Save to components directory
        components_dir = Path('templates/components')
        components_dir.mkdir(exist_ok=True)
        
        with open(components_dir / f'{screen}_buttons.html', 'w', encoding='utf-8') as f:
            f.write(button_html)
        
        print(f"✅ Created {screen}_buttons.html")
    
    print("\n" + "=" * 60)
    print("🎉 Button System Templates Created Successfully!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Run create_backend_handlers.py to create Flask routes")
    print("2. Run create_frontend_handlers.py to create JavaScript handlers")
    print("3. Update your HTML templates to include the button components")
    print("4. Test all button functionality")

if __name__ == "__main__":
    main()
