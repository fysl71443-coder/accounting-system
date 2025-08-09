// =============================================================================
// SALES BUTTONS SYSTEM - نظام أزرار المبيعات
// =============================================================================

console.log('🚀 Sales buttons system loaded');

// متغيرات عامة
let selectedInvoiceId = null;
const isRTL = document.documentElement.dir === 'rtl' || document.documentElement.lang === 'ar';

// بيانات تجريبية للفواتير غير المدفوعة
let unpaidInvoices = [
    { id: 1, number: 'INV-001', customer: 'أحمد محمد السعيد', amount: 1500.00, paid: 500.00, remaining: 1000.00 },
    { id: 2, number: 'INV-002', customer: 'شركة الأغذية المتقدمة', amount: 2800.00, paid: 0.00, remaining: 2800.00 },
    { id: 3, number: 'INV-003', customer: 'فاطمة علي الزهراني', amount: 950.00, paid: 200.00, remaining: 750.00 },
    { id: 4, number: 'INV-004', customer: 'محمد عبدالله القحطاني', amount: 3200.00, paid: 1000.00, remaining: 2200.00 }
];

// =============================================================================
// وظائف عرض الرسائل
// =============================================================================

function showToast(message, type = 'info') {
    console.log('📢 Toast:', type, message);
    
    // إنشاء toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'success' ? 'success' : type === 'warning' ? 'warning' : type === 'danger' ? 'danger' : 'info'} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'warning' ? 'exclamation' : type === 'danger' ? 'times' : 'info'}-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // إزالة تلقائية بعد 4 ثوان
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 4000);
}

// =============================================================================
// وظائف الأزرار الرئيسية
// =============================================================================

// إنشاء فاتورة جديدة
function createNewInvoice() {
    console.log('✅ Creating new invoice...');
    alert('🆕 زر إنشاء فاتورة جديدة يعمل بنجاح!');

    try {
        showToast(isRTL ? 'جاري فتح نافذة إنشاء فاتورة جديدة...' : 'Opening new invoice window...', 'info');

        setTimeout(() => {
            showNewInvoiceModal();
        }, 500);
    } catch (error) {
        console.error('Error in createNewInvoice:', error);
        alert('خطأ في فتح نافذة الفاتورة: ' + error.message);
    }
}

// طباعة الفاتورة
function printInvoice() {
    console.log('🖨️ Print invoice clicked, selectedInvoiceId:', selectedInvoiceId);
    
    if (!selectedInvoiceId) {
        showToast(isRTL ? 'يرجى تحديد فاتورة للطباعة' : 'Please select an invoice to print', 'warning');
        return;
    }
    
    showToast(isRTL ? 'جاري إعداد الفاتورة للطباعة...' : 'Preparing invoice for printing...', 'info');
    
    setTimeout(() => {
        printInvoiceDocument(selectedInvoiceId);
    }, 1000);
}

// حذف الفاتورة
function deleteInvoice() {
    console.log('🗑️ Delete invoice clicked, selectedInvoiceId:', selectedInvoiceId);
    
    if (!selectedInvoiceId) {
        showToast(isRTL ? 'يرجى تحديد فاتورة للحذف' : 'Please select an invoice to delete', 'warning');
        return;
    }
    
    const confirmMessage = isRTL ? 'هل أنت متأكد من حذف هذه الفاتورة؟' : 'Are you sure you want to delete this invoice?';
    
    if (confirm(confirmMessage)) {
        showToast(isRTL ? 'تم حذف الفاتورة بنجاح' : 'Invoice deleted successfully', 'success');
        selectedInvoiceId = null;
        updateButtonStates();
    }
}

// تسجيل دفعة
function recordPayment() {
    console.log('💰 Record payment clicked');
    showToast(isRTL ? 'جاري فتح نافذة تسجيل الدفعة...' : 'Opening payment window...', 'info');
    
    setTimeout(() => {
        showPaymentModal();
    }, 500);
}

// =============================================================================
// وظائف إدارة حالة الأزرار
// =============================================================================

// تحديث حالة الأزرار
function updateButtonStates() {
    const printBtn = document.getElementById('printBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    
    if (printBtn && deleteBtn) {
        if (selectedInvoiceId) {
            printBtn.disabled = false;
            deleteBtn.disabled = false;
            printBtn.classList.remove('opacity-50');
            deleteBtn.classList.remove('opacity-50');
        } else {
            printBtn.disabled = true;
            deleteBtn.disabled = true;
            printBtn.classList.add('opacity-50');
            deleteBtn.classList.add('opacity-50');
        }
    }
}

// تحديد فاتورة
function selectInvoice(invoiceId) {
    console.log('📋 Selecting invoice:', invoiceId);
    selectedInvoiceId = invoiceId;
    updateButtonStates();
    
    // إزالة التحديد من جميع الفواتير
    document.querySelectorAll('.invoice-row').forEach(row => {
        row.classList.remove('table-active');
    });
    
    // إضافة التحديد للفاتورة المختارة
    const selectedRow = document.querySelector(`[data-invoice-id="${invoiceId}"]`);
    if (selectedRow) {
        selectedRow.classList.add('table-active');
    }
    
    showToast(isRTL ? `تم تحديد الفاتورة رقم ${invoiceId}` : `Invoice ${invoiceId} selected`, 'success');
}

// =============================================================================
// وظائف النوافذ المنبثقة (Modals)
// =============================================================================

// عرض modal إنشاء فاتورة جديدة
function showNewInvoiceModal() {
    console.log('📝 Showing new invoice modal');
    
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'newInvoiceModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-plus me-2"></i>
                        ${isRTL ? 'إنشاء فاتورة جديدة' : 'Create New Invoice'}
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="newInvoiceForm">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'العميل' : 'Customer'}</label>
                                    <select class="form-select" id="customerId" required>
                                        <option value="">${isRTL ? 'اختر العميل' : 'Select Customer'}</option>
                                        <option value="1">أحمد محمد السعيد</option>
                                        <option value="2">شركة الأغذية المتقدمة</option>
                                        <option value="3">فاطمة علي الزهراني</option>
                                        <option value="4">محمد عبدالله القحطاني</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'تاريخ الفاتورة' : 'Invoice Date'}</label>
                                    <input type="date" class="form-control" id="invoiceDate" value="${new Date().toISOString().split('T')[0]}" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">${isRTL ? 'الأصناف' : 'Items'}</label>
                            <div id="invoiceItems">
                                <div class="row invoice-item mb-2 p-2 bg-light rounded">
                                    <div class="col-md-4">
                                        <input type="text" class="form-control" placeholder="${isRTL ? 'اسم الصنف' : 'Item Name'}" required>
                                    </div>
                                    <div class="col-md-2">
                                        <input type="number" class="form-control qty-input" placeholder="${isRTL ? 'الكمية' : 'Qty'}" min="1" value="1" required>
                                    </div>
                                    <div class="col-md-3">
                                        <input type="number" class="form-control price-input" placeholder="${isRTL ? 'السعر' : 'Price'}" step="0.01" min="0" required>
                                    </div>
                                    <div class="col-md-2">
                                        <input type="number" class="form-control total-input" placeholder="${isRTL ? 'الإجمالي' : 'Total'}" readonly>
                                    </div>
                                    <div class="col-md-1">
                                        <button type="button" class="btn btn-danger btn-sm" onclick="removeInvoiceItem(this)">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="addInvoiceItem()">
                                <i class="fas fa-plus me-1"></i>
                                ${isRTL ? 'إضافة صنف' : 'Add Item'}
                            </button>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'الخصم (%)' : 'Discount (%)'}</label>
                                    <input type="number" class="form-control" id="discountPercent" min="0" max="100" value="0" step="0.01">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'الضريبة (%)' : 'Tax (%)'}</label>
                                    <input type="number" class="form-control" id="taxPercent" min="0" max="100" value="15" step="0.01">
                                </div>
                            </div>
                        </div>
                        
                        <div class="alert alert-info">
                            <div class="row">
                                <div class="col-6">
                                    <strong>${isRTL ? 'المجموع الفرعي:' : 'Subtotal:'}</strong>
                                    <span id="subtotalAmount">0.00</span> ${isRTL ? 'ريال' : 'SAR'}
                                </div>
                                <div class="col-6">
                                    <strong>${isRTL ? 'الإجمالي النهائي:' : 'Total Amount:'}</strong>
                                    <span id="totalAmount">0.00</span> ${isRTL ? 'ريال' : 'SAR'}
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        ${isRTL ? 'إلغاء' : 'Cancel'}
                    </button>
                    <button type="button" class="btn btn-success" onclick="saveNewInvoice()">
                        <i class="fas fa-save me-1"></i>
                        ${isRTL ? 'حفظ الفاتورة' : 'Save Invoice'}
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // إضافة event listeners لحساب الإجمالي
    modal.addEventListener('input', calculateInvoiceTotal);
    
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

// عرض modal تسجيل الدفعة
function showPaymentModal() {
    console.log('💳 Showing payment modal');
    
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'paymentModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-warning text-dark">
                    <h5 class="modal-title">
                        <i class="fas fa-money-bill-wave me-2"></i>
                        ${isRTL ? 'تسجيل دفعة' : 'Record Payment'}
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="paymentForm">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'مبلغ الدفع' : 'Payment Amount'}</label>
                                    <input type="number" class="form-control" id="paymentAmount" step="0.01" min="0" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">${isRTL ? 'طريقة الدفع' : 'Payment Method'}</label>
                                    <select class="form-select" id="paymentMethod" required>
                                        <option value="">${isRTL ? 'اختر طريقة الدفع' : 'Select Payment Method'}</option>
                                        <option value="cash">${isRTL ? 'نقداً' : 'Cash'}</option>
                                        <option value="transfer">${isRTL ? 'تحويل بنكي' : 'Bank Transfer'}</option>
                                        <option value="card">${isRTL ? 'بطاقة ائتمان' : 'Credit Card'}</option>
                                        <option value="mada">${isRTL ? 'مدى' : 'Mada'}</option>
                                        <option value="check">${isRTL ? 'شيك' : 'Check'}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">${isRTL ? 'ملاحظات' : 'Notes'}</label>
                            <textarea class="form-control" id="paymentNotes" rows="2" placeholder="${isRTL ? 'ملاحظات إضافية (اختياري)' : 'Additional notes (optional)'}"></textarea>
                        </div>
                        
                        <hr>
                        
                        <h6>${isRTL ? 'الفواتير غير المدفوعة' : 'Unpaid Invoices'}</h6>
                        <div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
                            <table class="table table-sm">
                                <thead class="table-light">
                                    <tr>
                                        <th width="50">
                                            <input type="checkbox" id="selectAllInvoices" onchange="toggleAllInvoices()">
                                        </th>
                                        <th>${isRTL ? 'رقم الفاتورة' : 'Invoice #'}</th>
                                        <th>${isRTL ? 'العميل' : 'Customer'}</th>
                                        <th>${isRTL ? 'المبلغ الإجمالي' : 'Total Amount'}</th>
                                        <th>${isRTL ? 'المدفوع' : 'Paid'}</th>
                                        <th>${isRTL ? 'المتبقي' : 'Remaining'}</th>
                                        <th>${isRTL ? 'المبلغ المطبق' : 'Applied Amount'}</th>
                                    </tr>
                                </thead>
                                <tbody id="unpaidInvoicesTable">
                                    ${unpaidInvoices.map(invoice => `
                                        <tr>
                                            <td>
                                                <input type="checkbox" class="invoice-checkbox" data-invoice-id="${invoice.id}" onchange="updatePaymentDistribution()">
                                            </td>
                                            <td>${invoice.number}</td>
                                            <td>${invoice.customer}</td>
                                            <td>${invoice.amount.toFixed(2)}</td>
                                            <td>${invoice.paid.toFixed(2)}</td>
                                            <td class="text-danger fw-bold">${invoice.remaining.toFixed(2)}</td>
                                            <td>
                                                <input type="number" class="form-control form-control-sm applied-amount" 
                                                       data-invoice-id="${invoice.id}" 
                                                       step="0.01" min="0" max="${invoice.remaining}" 
                                                       value="0" onchange="updatePaymentDistribution()">
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        
                        <div class="alert alert-info mt-3">
                            <div class="row">
                                <div class="col-6">
                                    <strong>${isRTL ? 'إجمالي المطبق:' : 'Total Applied:'}</strong>
                                    <span id="totalApplied">0.00</span> ${isRTL ? 'ريال' : 'SAR'}
                                </div>
                                <div class="col-6">
                                    <strong>${isRTL ? 'المتبقي من الدفعة:' : 'Remaining Payment:'}</strong>
                                    <span id="remainingPayment">0.00</span> ${isRTL ? 'ريال' : 'SAR'}
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        ${isRTL ? 'إلغاء' : 'Cancel'}
                    </button>
                    <button type="button" class="btn btn-warning" onclick="savePayment()">
                        <i class="fas fa-save me-1"></i>
                        ${isRTL ? 'حفظ الدفعة' : 'Save Payment'}
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

// =============================================================================
// وظائف مساعدة
// =============================================================================

// إضافة صنف جديد للفاتورة
function addInvoiceItem() {
    const itemsContainer = document.getElementById('invoiceItems');
    const newItem = document.createElement('div');
    newItem.className = 'row invoice-item mb-2 p-2 bg-light rounded';
    newItem.innerHTML = `
        <div class="col-md-4">
            <input type="text" class="form-control" placeholder="${isRTL ? 'اسم الصنف' : 'Item Name'}" required>
        </div>
        <div class="col-md-2">
            <input type="number" class="form-control qty-input" placeholder="${isRTL ? 'الكمية' : 'Qty'}" min="1" value="1" required>
        </div>
        <div class="col-md-3">
            <input type="number" class="form-control price-input" placeholder="${isRTL ? 'السعر' : 'Price'}" step="0.01" min="0" required>
        </div>
        <div class="col-md-2">
            <input type="number" class="form-control total-input" placeholder="${isRTL ? 'الإجمالي' : 'Total'}" readonly>
        </div>
        <div class="col-md-1">
            <button type="button" class="btn btn-danger btn-sm" onclick="removeInvoiceItem(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    itemsContainer.appendChild(newItem);
}

// حذف صنف من الفاتورة
function removeInvoiceItem(button) {
    const item = button.closest('.invoice-item');
    if (document.querySelectorAll('.invoice-item').length > 1) {
        item.remove();
        calculateInvoiceTotal();
    } else {
        showToast(isRTL ? 'يجب أن تحتوي الفاتورة على صنف واحد على الأقل' : 'Invoice must contain at least one item', 'warning');
    }
}

// حساب إجمالي الفاتورة
function calculateInvoiceTotal() {
    let subtotal = 0;
    
    document.querySelectorAll('.invoice-item').forEach(item => {
        const qtyInput = item.querySelector('.qty-input');
        const priceInput = item.querySelector('.price-input');
        const totalInput = item.querySelector('.total-input');
        
        const qty = parseFloat(qtyInput?.value) || 0;
        const price = parseFloat(priceInput?.value) || 0;
        const total = qty * price;
        
        if (totalInput) {
            totalInput.value = total.toFixed(2);
        }
        subtotal += total;
    });
    
    const discountPercent = parseFloat(document.getElementById('discountPercent')?.value) || 0;
    const taxPercent = parseFloat(document.getElementById('taxPercent')?.value) || 0;
    
    const discountAmount = subtotal * (discountPercent / 100);
    const afterDiscount = subtotal - discountAmount;
    const taxAmount = afterDiscount * (taxPercent / 100);
    const finalTotal = afterDiscount + taxAmount;
    
    const subtotalElement = document.getElementById('subtotalAmount');
    const totalElement = document.getElementById('totalAmount');
    
    if (subtotalElement) subtotalElement.textContent = subtotal.toFixed(2);
    if (totalElement) totalElement.textContent = finalTotal.toFixed(2);
}

// حفظ فاتورة جديدة
function saveNewInvoice() {
    const form = document.getElementById('newInvoiceForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    showToast(isRTL ? 'جاري حفظ الفاتورة...' : 'Saving invoice...', 'info');
    
    setTimeout(() => {
        showToast(isRTL ? 'تم حفظ الفاتورة بنجاح' : 'Invoice saved successfully', 'success');
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('newInvoiceModal'));
        modal.hide();
    }, 1500);
}

// حفظ الدفعة
function savePayment() {
    const form = document.getElementById('paymentForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const paymentAmount = parseFloat(document.getElementById('paymentAmount').value);
    
    if (paymentAmount <= 0) {
        showToast(isRTL ? 'يرجى إدخال مبلغ دفع صحيح' : 'Please enter a valid payment amount', 'warning');
        return;
    }
    
    showToast(isRTL ? 'جاري حفظ الدفعة...' : 'Saving payment...', 'info');
    
    setTimeout(() => {
        showToast(isRTL ? 'تم حفظ الدفعة بنجاح' : 'Payment saved successfully', 'success');
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
        modal.hide();
    }, 1500);
}

// تحديد/إلغاء تحديد جميع الفواتير
function toggleAllInvoices() {
    const selectAll = document.getElementById('selectAllInvoices');
    const checkboxes = document.querySelectorAll('.invoice-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
    
    updatePaymentDistribution();
}

// تحديث توزيع الدفعة
function updatePaymentDistribution() {
    const paymentAmount = parseFloat(document.getElementById('paymentAmount')?.value) || 0;
    const checkedInvoices = document.querySelectorAll('.invoice-checkbox:checked');
    
    if (checkedInvoices.length === 0) {
        document.querySelectorAll('.applied-amount').forEach(input => {
            input.value = '0';
        });
    } else {
        let remainingAmount = paymentAmount;
        
        checkedInvoices.forEach(checkbox => {
            const invoiceId = checkbox.dataset.invoiceId;
            const invoice = unpaidInvoices.find(inv => inv.id == invoiceId);
            const appliedInput = document.querySelector(`.applied-amount[data-invoice-id="${invoiceId}"]`);
            
            if (invoice && appliedInput) {
                const maxApplicable = Math.min(invoice.remaining, remainingAmount);
                appliedInput.value = maxApplicable.toFixed(2);
                remainingAmount -= maxApplicable;
            }
        });
    }
    
    updatePaymentSummary();
}

// تحديث ملخص الدفعة
function updatePaymentSummary() {
    const paymentAmount = parseFloat(document.getElementById('paymentAmount')?.value) || 0;
    let totalApplied = 0;
    
    document.querySelectorAll('.applied-amount').forEach(input => {
        totalApplied += parseFloat(input.value) || 0;
    });
    
    const remainingPayment = paymentAmount - totalApplied;
    
    const totalAppliedElement = document.getElementById('totalApplied');
    const remainingElement = document.getElementById('remainingPayment');
    
    if (totalAppliedElement) totalAppliedElement.textContent = totalApplied.toFixed(2);
    if (remainingElement) {
        remainingElement.textContent = remainingPayment.toFixed(2);
        
        if (remainingPayment > 0) {
            remainingElement.className = 'text-warning fw-bold';
        } else if (remainingPayment < 0) {
            remainingElement.className = 'text-danger fw-bold';
        } else {
            remainingElement.className = 'text-success fw-bold';
        }
    }
}

// طباعة الفاتورة
function printInvoiceDocument(invoiceId) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html dir="${isRTL ? 'rtl' : 'ltr'}" lang="${isRTL ? 'ar' : 'en'}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${isRTL ? 'فاتورة مبيعات' : 'Sales Invoice'}</title>
            <style>
                body { 
                    font-family: 'Arial', sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    font-size: 14px;
                    direction: ${isRTL ? 'rtl' : 'ltr'};
                }
                .header { 
                    text-align: center; 
                    border-bottom: 2px solid #333; 
                    padding-bottom: 20px; 
                    margin-bottom: 30px; 
                }
                .logo { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #2c3e50; 
                    margin-bottom: 10px; 
                }
                .company-info { 
                    color: #666; 
                    line-height: 1.6; 
                }
                .invoice-details { 
                    display: flex; 
                    justify-content: space-between; 
                    margin-bottom: 30px; 
                }
                .invoice-details div { 
                    flex: 1; 
                }
                .invoice-table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-bottom: 30px; 
                }
                .invoice-table th, .invoice-table td { 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: ${isRTL ? 'right' : 'left'}; 
                }
                .invoice-table th { 
                    background-color: #f8f9fa; 
                    font-weight: bold; 
                }
                .totals { 
                    float: ${isRTL ? 'left' : 'right'}; 
                    width: 300px; 
                }
                .totals table { 
                    width: 100%; 
                    border-collapse: collapse; 
                }
                .totals td { 
                    padding: 8px; 
                    border-bottom: 1px solid #eee; 
                }
                .total-final { 
                    font-weight: bold; 
                    font-size: 16px; 
                    background-color: #f8f9fa; 
                }
                .footer { 
                    margin-top: 50px; 
                    text-align: center; 
                    color: #666; 
                    border-top: 1px solid #eee; 
                    padding-top: 20px; 
                }
                @media print {
                    body { margin: 0; }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">${isRTL ? 'شركة المحاسبة المتقدمة' : 'Advanced Accounting Company'}</div>
                <div class="company-info">
                    ${isRTL ? 'الرياض، المملكة العربية السعودية' : 'Riyadh, Saudi Arabia'}<br>
                    ${isRTL ? 'هاتف: +966 11 123 4567' : 'Phone: +966 11 123 4567'}<br>
                    ${isRTL ? 'بريد إلكتروني: info@company.com' : 'Email: info@company.com'}
                </div>
            </div>
            
            <div class="invoice-details">
                <div>
                    <h3>${isRTL ? 'فاتورة مبيعات' : 'Sales Invoice'}</h3>
                    <p><strong>${isRTL ? 'رقم الفاتورة:' : 'Invoice #:'}</strong> INV-${invoiceId.toString().padStart(3, '0')}</p>
                    <p><strong>${isRTL ? 'التاريخ:' : 'Date:'}</strong> ${new Date().toLocaleDateString(isRTL ? 'ar-SA' : 'en-US')}</p>
                </div>
                <div>
                    <h4>${isRTL ? 'بيانات العميل' : 'Customer Information'}</h4>
                    <p><strong>${isRTL ? 'الاسم:' : 'Name:'}</strong> أحمد محمد السعيد</p>
                    <p><strong>${isRTL ? 'الهاتف:' : 'Phone:'}</strong> +966 50 123 4567</p>
                    <p><strong>${isRTL ? 'العنوان:' : 'Address:'}</strong> ${isRTL ? 'الرياض، السعودية' : 'Riyadh, Saudi Arabia'}</p>
                </div>
            </div>
            
            <table class="invoice-table">
                <thead>
                    <tr>
                        <th>${isRTL ? 'الصنف' : 'Item'}</th>
                        <th>${isRTL ? 'الكمية' : 'Quantity'}</th>
                        <th>${isRTL ? 'السعر' : 'Price'}</th>
                        <th>${isRTL ? 'الإجمالي' : 'Total'}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${isRTL ? 'منتج تجريبي 1' : 'Sample Product 1'}</td>
                        <td>2</td>
                        <td>500.00</td>
                        <td>1,000.00</td>
                    </tr>
                    <tr>
                        <td>${isRTL ? 'منتج تجريبي 2' : 'Sample Product 2'}</td>
                        <td>1</td>
                        <td>300.00</td>
                        <td>300.00</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="totals">
                <table>
                    <tr>
                        <td>${isRTL ? 'المجموع الفرعي:' : 'Subtotal:'}</td>
                        <td>1,300.00 ${isRTL ? 'ريال' : 'SAR'}</td>
                    </tr>
                    <tr>
                        <td>${isRTL ? 'الخصم:' : 'Discount:'}</td>
                        <td>0.00 ${isRTL ? 'ريال' : 'SAR'}</td>
                    </tr>
                    <tr>
                        <td>${isRTL ? 'الضريبة (15%):' : 'Tax (15%):'}</td>
                        <td>195.00 ${isRTL ? 'ريال' : 'SAR'}</td>
                    </tr>
                    <tr class="total-final">
                        <td>${isRTL ? 'الإجمالي النهائي:' : 'Total Amount:'}</td>
                        <td>1,495.00 ${isRTL ? 'ريال' : 'SAR'}</td>
                    </tr>
                </table>
            </div>
            
            <div style="clear: both;"></div>
            
            <div class="footer">
                <p>${isRTL ? 'شكراً لتعاملكم معنا' : 'Thank you for your business'}</p>
                <p>${isRTL ? 'هذه فاتورة مُنشأة إلكترونياً' : 'This is an electronically generated invoice'}</p>
            </div>
            
            <script>
                window.onload = function() {
                    window.print();
                    window.onafterprint = function() {
                        window.close();
                    };
                };
            </script>
        </body>
        </html>
    `);
    printWindow.document.close();
}

// =============================================================================
// تهيئة النظام
// =============================================================================

// إضافة event listeners عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 DOM loaded, initializing sales buttons system...');
    
    // تحديث حالة الأزرار في البداية
    updateButtonStates();
    
    // إضافة event listeners للأزرار
    const createBtn = document.getElementById('createBtn');
    const printBtn = document.getElementById('printBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const paymentBtn = document.getElementById('paymentBtn');
    
    if (createBtn) {
        createBtn.addEventListener('click', createNewInvoice);
        console.log('✅ Create button listener added');
    }
    
    if (printBtn) {
        printBtn.addEventListener('click', printInvoice);
        console.log('✅ Print button listener added');
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', deleteInvoice);
        console.log('✅ Delete button listener added');
    }
    
    if (paymentBtn) {
        paymentBtn.addEventListener('click', recordPayment);
        console.log('✅ Payment button listener added');
    }
    
    // إضافة event listener لتحديث مبلغ الدفعة
    document.addEventListener('input', function(e) {
        if (e.target.id === 'paymentAmount') {
            updatePaymentDistribution();
        }
    });
    
    // إضافة event listeners للجدول لتحديد الفواتير
    document.addEventListener('click', function(e) {
        if (e.target.closest('tr') && e.target.closest('tbody')) {
            const row = e.target.closest('tr');
            const invoiceId = row.dataset.invoiceId;
            if (invoiceId && !e.target.closest('input')) {
                selectInvoice(parseInt(invoiceId));
            }
        }
    });
    
    console.log('🚀 Sales buttons system initialized successfully!');
});

// تصدير الوظائف للاستخدام العام
window.createNewInvoice = createNewInvoice;
window.printInvoice = printInvoice;
window.deleteInvoice = deleteInvoice;
window.recordPayment = recordPayment;
window.selectInvoice = selectInvoice;
window.addInvoiceItem = addInvoiceItem;
window.removeInvoiceItem = removeInvoiceItem;
window.saveNewInvoice = saveNewInvoice;
window.savePayment = savePayment;
window.toggleAllInvoices = toggleAllInvoices;
window.updatePaymentDistribution = updatePaymentDistribution;
