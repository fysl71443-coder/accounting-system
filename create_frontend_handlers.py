#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontend JavaScript Handlers for Button System
معالجات JavaScript الأمامية لنظام الأزرار
"""

import os
from pathlib import Path

def create_frontend_handlers():
    """Create JavaScript handlers for all button actions"""
    
    js_code = '''/**
 * Frontend Button Handlers for Accounting System
 * معالجات الأزرار الأمامية لنظام المحاسبة
 */

// Global variables
let selectedInvoiceId = null;
let currentRecordId = null;

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

function showConfirmDialog(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function logButtonClick(screen, action, data = {}) {
    console.log(`🔵 Button Click: ${screen} - ${action}`, data);
}

// ============================================================================
// SALES HANDLERS
// ============================================================================

const salesHandler = {
    SaveRecord: function() {
        logButtonClick('Sales', 'Save Record');
        
        const formData = this.getFormData();
        if (!this.validateFormData(formData)) {
            return;
        }
        
        fetch('/api/sales/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('تم حفظ السجل بنجاح / Record saved successfully', 'success');
                this.clearForm();
                this.refreshTable();
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في حفظ السجل / Error saving record', 'danger');
        });
    },
    
    EditRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار سجل للتعديل / Please select a record to edit', 'warning');
            return;
        }
        
        logButtonClick('Sales', 'Edit Record', {id});
        
        const formData = this.getFormData();
        
        fetch(`/api/sales/edit/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('تم تحديث السجل بنجاح / Record updated successfully', 'success');
                this.refreshTable();
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في تحديث السجل / Error updating record', 'danger');
        });
    },
    
    DeleteRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار سجل للحذف / Please select a record to delete', 'warning');
            return;
        }
        
        logButtonClick('Sales', 'Delete Record', {id});
        
        showConfirmDialog('هل أنت متأكد من حذف هذا السجل؟ / Are you sure you want to delete this record?', () => {
            fetch(`/api/sales/delete/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('تم حذف السجل بنجاح / Record deleted successfully', 'success');
                    this.clearForm();
                    this.refreshTable();
                    currentRecordId = null;
                } else {
                    showToast(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('حدث خطأ في حذف السجل / Error deleting record', 'danger');
            });
        });
    },
    
    PreviewRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار سجل للمعاينة / Please select a record to preview', 'warning');
            return;
        }
        
        logButtonClick('Sales', 'Preview Record', {id});
        
        fetch(`/api/sales/preview/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showPreviewModal(data.data);
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في معاينة السجل / Error previewing record', 'danger');
        });
    },
    
    PrintRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار سجل للطباعة / Please select a record to print', 'warning');
            return;
        }
        
        logButtonClick('Sales', 'Print Record', {id});
        
        fetch(`/api/sales/print/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.open(data.print_url, '_blank');
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في طباعة السجل / Error printing record', 'danger');
        });
    },
    
    SelectInvoice: function() {
        logButtonClick('Sales', 'Select Invoice');
        
        fetch('/api/sales/select_invoice')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showSelectInvoiceModal(data.invoices);
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في جلب الفواتير / Error fetching invoices', 'danger');
        });
    },
    
    RegisterPayment: function() {
        if (!selectedInvoiceId) {
            showToast('يرجى اختيار فاتورة أولاً / Please select an invoice first', 'warning');
            return;
        }
        
        logButtonClick('Sales', 'Register Payment', {invoiceId: selectedInvoiceId});
        
        // Show payment modal
        const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
        
        // Set today's date as default
        document.getElementById('paymentDate').value = new Date().toISOString().split('T')[0];
        
        paymentModal.show();
    },
    
    // Helper functions
    getFormData: function() {
        return {
            invoice_number: document.getElementById('invoiceNumber')?.value || '',
            customer_name: document.getElementById('customerName')?.value || '',
            total_amount: document.getElementById('totalAmount')?.value || 0,
            tax_amount: document.getElementById('taxAmount')?.value || 0,
            final_amount: document.getElementById('finalAmount')?.value || 0,
            payment_method: document.getElementById('paymentMethod')?.value || 'cash',
            payment_status: document.getElementById('paymentStatus')?.value || 'pending',
            notes: document.getElementById('notes')?.value || ''
        };
    },
    
    validateFormData: function(data) {
        if (!data.invoice_number) {
            showToast('رقم الفاتورة مطلوب / Invoice number is required', 'warning');
            return false;
        }
        if (!data.customer_name) {
            showToast('اسم العميل مطلوب / Customer name is required', 'warning');
            return false;
        }
        if (!data.total_amount || data.total_amount <= 0) {
            showToast('المبلغ الإجمالي مطلوب / Total amount is required', 'warning');
            return false;
        }
        return true;
    },
    
    clearForm: function() {
        const form = document.getElementById('salesForm');
        if (form) {
            form.reset();
        }
        currentRecordId = null;
    },
    
    refreshTable: function() {
        // Reload the sales table
        if (typeof loadSalesTable === 'function') {
            loadSalesTable();
        } else {
            location.reload();
        }
    },
    
    showPreviewModal: function(data) {
        // Create and show preview modal
        const modalHtml = `
            <div class="modal fade" id="previewModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">معاينة الفاتورة / Invoice Preview</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <strong>رقم الفاتورة / Invoice Number:</strong> ${data.sale.invoice_number}
                                </div>
                                <div class="col-md-6">
                                    <strong>التاريخ / Date:</strong> ${data.sale.invoice_date}
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-md-6">
                                    <strong>العميل / Customer:</strong> ${data.sale.customer_name}
                                </div>
                                <div class="col-md-6">
                                    <strong>المبلغ النهائي / Final Amount:</strong> ${data.sale.final_amount}
                                </div>
                            </div>
                            <hr>
                            <h6>العناصر / Items:</h6>
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>المنتج / Product</th>
                                        <th>الكمية / Quantity</th>
                                        <th>السعر / Price</th>
                                        <th>الإجمالي / Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.items.map(item => `
                                        <tr>
                                            <td>${item.product_name}</td>
                                            <td>${item.quantity}</td>
                                            <td>${item.unit_price}</td>
                                            <td>${item.total_price}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إغلاق / Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('previewModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add new modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('previewModal'));
        modal.show();
    },
    
    showSelectInvoiceModal: function(invoices) {
        const tableBody = document.getElementById('invoicesTableBody');
        if (!tableBody) return;
        
        tableBody.innerHTML = invoices.map(invoice => `
            <tr>
                <td>${invoice.invoice_number}</td>
                <td>${invoice.invoice_date}</td>
                <td>${invoice.customer_name}</td>
                <td>${invoice.final_amount}</td>
                <td><span class="badge bg-${invoice.payment_status === 'paid' ? 'success' : 'warning'}">${invoice.payment_status}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="selectInvoice(${invoice.id}, '${invoice.invoice_number}')">
                        اختيار / Select
                    </button>
                </td>
            </tr>
        `).join('');
        
        const modal = new bootstrap.Modal(document.getElementById('selectInvoiceModal'));
        modal.show();
    }
};

// ============================================================================
// PRODUCTS HANDLERS
// ============================================================================

const productsHandler = {
    SaveRecord: function() {
        logButtonClick('Products', 'Save Record');
        
        const formData = this.getFormData();
        if (!this.validateFormData(formData)) {
            return;
        }
        
        fetch('/api/products/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('تم حفظ المنتج بنجاح / Product saved successfully', 'success');
                this.clearForm();
                this.refreshTable();
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في حفظ المنتج / Error saving product', 'danger');
        });
    },
    
    EditRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار منتج للتعديل / Please select a product to edit', 'warning');
            return;
        }
        
        logButtonClick('Products', 'Edit Record', {id});
        // Implementation similar to sales edit
    },
    
    DeleteRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار منتج للحذف / Please select a product to delete', 'warning');
            return;
        }
        
        logButtonClick('Products', 'Delete Record', {id});
        // Implementation similar to sales delete
    },
    
    SearchRecords: function() {
        logButtonClick('Products', 'Search Records');
        
        const searchTerm = document.getElementById('searchTerm')?.value || '';
        
        fetch(`/api/products/search?q=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.displaySearchResults(data.products);
                showToast(`تم العثور على ${data.products.length} منتج / Found ${data.products.length} products`, 'info');
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في البحث / Error searching products', 'danger');
        });
    },
    
    PrintRecord: function(recordId = null) {
        const id = recordId || currentRecordId;
        if (!id) {
            showToast('يرجى اختيار منتج للطباعة / Please select a product to print', 'warning');
            return;
        }
        
        logButtonClick('Products', 'Print Record', {id});
        // Implementation for printing product details
    },
    
    // Helper functions
    getFormData: function() {
        return {
            product_code: document.getElementById('productCode')?.value || '',
            product_name: document.getElementById('productName')?.value || '',
            description: document.getElementById('description')?.value || '',
            unit_cost: document.getElementById('unitCost')?.value || 0,
            selling_price: document.getElementById('sellingPrice')?.value || 0,
            category: document.getElementById('category')?.value || '',
            unit_type: document.getElementById('unitType')?.value || 'قطعة',
            min_stock_level: document.getElementById('minStockLevel')?.value || 0,
            current_stock: document.getElementById('currentStock')?.value || 0
        };
    },
    
    validateFormData: function(data) {
        if (!data.product_code) {
            showToast('كود المنتج مطلوب / Product code is required', 'warning');
            return false;
        }
        if (!data.product_name) {
            showToast('اسم المنتج مطلوب / Product name is required', 'warning');
            return false;
        }
        return true;
    },
    
    clearForm: function() {
        const form = document.getElementById('productsForm');
        if (form) {
            form.reset();
        }
        currentRecordId = null;
    },
    
    refreshTable: function() {
        if (typeof loadProductsTable === 'function') {
            loadProductsTable();
        } else {
            location.reload();
        }
    },
    
    displaySearchResults: function(products) {
        const tableBody = document.getElementById('productsTableBody');
        if (!tableBody) return;
        
        tableBody.innerHTML = products.map(product => `
            <tr onclick="selectProduct(${product.id})">
                <td>${product.product_code}</td>
                <td>${product.product_name}</td>
                <td>${product.category}</td>
                <td>${product.unit_cost}</td>
                <td>${product.selling_price}</td>
                <td>${product.current_stock}</td>
            </tr>
        `).join('');
    }
};

// ============================================================================
// REPORTS HANDLERS
// ============================================================================

const reportsHandler = {
    PreviewReport: function() {
        logButtonClick('Reports', 'Preview Report');
        
        const reportData = this.getReportData();
        
        fetch('/api/reports/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reportData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showReportPreview(data.report_data);
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في معاينة التقرير / Error previewing report', 'danger');
        });
    },
    
    PrintReport: function() {
        logButtonClick('Reports', 'Print Report');
        
        const reportData = this.getReportData();
        // Implementation for printing report
        window.print();
    },
    
    ExportReport: function() {
        logButtonClick('Reports', 'Export Report');
        
        const reportData = this.getReportData();
        const exportFormat = document.getElementById('exportFormat')?.value || 'excel';
        
        fetch('/api/reports/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...reportData,
                format: exportFormat
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Download the exported file
                window.open(data.download_url, '_blank');
                showToast('تم تصدير التقرير بنجاح / Report exported successfully', 'success');
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('حدث خطأ في تصدير التقرير / Error exporting report', 'danger');
        });
    },
    
    getReportData: function() {
        return {
            report_type: document.getElementById('reportType')?.value || 'sales_summary',
            date_from: document.getElementById('dateFrom')?.value || '',
            date_to: document.getElementById('dateTo')?.value || '',
            branch_id: document.getElementById('branchId')?.value || '',
            customer_id: document.getElementById('customerId')?.value || ''
        };
    },
    
    showReportPreview: function(reportData) {
        // Implementation to show report preview
        console.log('Report Preview:', reportData);
    }
};

// ============================================================================
// GLOBAL FUNCTIONS
// ============================================================================

function selectInvoice(invoiceId, invoiceNumber) {
    selectedInvoiceId = invoiceId;
    showToast(`تم اختيار الفاتورة: ${invoiceNumber} / Invoice selected: ${invoiceNumber}`, 'info');
    
    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('selectInvoiceModal'));
    if (modal) {
        modal.hide();
    }
}

function selectProduct(productId) {
    currentRecordId = productId;
    // Highlight selected row or perform other actions
}

function savePayment() {
    const paymentData = {
        invoice_id: selectedInvoiceId,
        amount_paid: document.getElementById('amountPaid').value,
        payment_method: document.getElementById('paymentMethod').value,
        payment_date: document.getElementById('paymentDate').value,
        notes: document.getElementById('notes').value
    };
    
    if (!paymentData.amount_paid || paymentData.amount_paid <= 0) {
        showToast('يرجى إدخال مبلغ صحيح / Please enter a valid amount', 'warning');
        return;
    }
    
    fetch('/api/sales/register_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(paymentData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('تم تسجيل الدفعة بنجاح / Payment registered successfully', 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
            if (modal) {
                modal.hide();
            }
            
            // Clear form
            document.getElementById('paymentForm').reset();
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('حدث خطأ في تسجيل الدفعة / Error registering payment', 'danger');
    });
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

console.log('✅ Button System JavaScript Handlers Loaded Successfully');
'''
    
    return js_code

def main():
    """Create frontend JavaScript handlers"""
    print("🔧 Creating Frontend JavaScript Handlers")
    print("=" * 60)
    
    js_code = create_frontend_handlers()
    
    # Create static/js directory if it doesn't exist
    js_dir = Path('static/js')
    js_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JavaScript file
    with open(js_dir / 'button_handlers.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print("✅ Created static/js/button_handlers.js")
    
    print("\n📋 JavaScript Handlers Created:")
    handlers = [
        "salesHandler.SaveRecord()",
        "salesHandler.EditRecord()",
        "salesHandler.DeleteRecord()",
        "salesHandler.PreviewRecord()",
        "salesHandler.PrintRecord()",
        "salesHandler.SelectInvoice()",
        "salesHandler.RegisterPayment()",
        "productsHandler.SaveRecord()",
        "productsHandler.SearchRecords()",
        "reportsHandler.PreviewReport()",
        "reportsHandler.ExportReport()"
    ]
    
    for handler in handlers:
        print(f"  • {handler}")
    
    print("\n📋 Instructions:")
    print("1. Include button_handlers.js in your HTML templates")
    print("2. Make sure Bootstrap 5 is loaded for modals and toasts")
    print("3. Test each button handler in the browser console")
    print("4. Customize the form field IDs to match your HTML")

if __name__ == "__main__":
    main()
