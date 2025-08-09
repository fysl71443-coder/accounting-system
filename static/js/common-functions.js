// Common JavaScript Functions for Accounting System
// نظام الوظائف المشتركة لنظام المحاسبة

// Global variables
const isRTL = document.documentElement.dir === 'rtl' || document.documentElement.lang === 'ar';

// Enhanced Toast Notification System
function showToast(message, type = 'info', duration = 4000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        ${isRTL ? 'left' : 'right'}: 20px;
        z-index: 9999;
        min-width: 320px;
        max-width: 400px;
        box-shadow: var(--shadow-lg);
        border-radius: var(--border-radius);
        animation: slideIn 0.3s ease-out;
    `;

    const icons = {
        'success': 'check-circle',
        'danger': 'times-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };

    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${icons[type] || 'info-circle'} me-2"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close ms-2" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;

    document.body.appendChild(toast);

    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// Form Validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            showFieldError(field, isRTL ? 'هذا الحقل مطلوب' : 'This field is required');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
            hideFieldError(field);
        }
    });
    
    return isValid;
}

function showFieldError(field, message) {
    hideFieldError(field);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function hideFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function clearFormValidation(form) {
    const invalidFields = form.querySelectorAll('.is-invalid');
    invalidFields.forEach(field => {
        field.classList.remove('is-invalid');
    });
    
    const errorMessages = form.querySelectorAll('.invalid-feedback');
    errorMessages.forEach(msg => msg.remove());
}

// Loading States
function showLoading(element, text = null) {
    const originalText = element.innerHTML;
    const loadingText = text || (isRTL ? 'جاري المعالجة...' : 'Processing...');
    element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + loadingText;
    element.disabled = true;
    element.dataset.originalText = originalText;
}

function hideLoading(element) {
    if (element.dataset.originalText) {
        element.innerHTML = element.dataset.originalText;
        element.disabled = false;
        delete element.dataset.originalText;
    }
}

// Confirmation Dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Search Functionality
function initializeSearch(searchInputId, containerId, searchColumns = []) {
    const searchInput = document.getElementById(searchInputId);
    const container = document.getElementById(containerId);
    
    if (searchInput && container) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            // For table search
            const rows = container.querySelectorAll('tbody tr');
            if (rows.length > 0) {
                rows.forEach(row => {
                    let found = false;
                    const cells = row.querySelectorAll('td');
                    
                    if (searchColumns.length === 0) {
                        found = Array.from(cells).some(cell => 
                            cell.textContent.toLowerCase().includes(searchTerm)
                        );
                    } else {
                        found = searchColumns.some(colIndex => 
                            cells[colIndex] && cells[colIndex].textContent.toLowerCase().includes(searchTerm)
                        );
                    }
                    
                    row.style.display = found ? '' : 'none';
                });
            }
            
            // For card search
            const cards = container.querySelectorAll('.card');
            if (cards.length > 0) {
                cards.forEach(card => {
                    const cardText = card.textContent.toLowerCase();
                    const found = cardText.includes(searchTerm);
                    card.closest('.col-md-6, .col-lg-4, .col-xl-3').style.display = found ? '' : 'none';
                });
            }
        });
    }
}

// Export Functions
function exportToPDF() {
    showToast(isRTL ? 'جاري تصدير PDF...' : 'Exporting to PDF...', 'info');
    // Simulate export
    setTimeout(() => {
        showToast(isRTL ? 'تم تصدير PDF بنجاح' : 'PDF exported successfully', 'success');
    }, 2000);
}

function exportToExcel() {
    showToast(isRTL ? 'جاري تصدير Excel...' : 'Exporting to Excel...', 'info');
    // Simulate export
    setTimeout(() => {
        showToast(isRTL ? 'تم تصدير Excel بنجاح' : 'Excel exported successfully', 'success');
    }, 2000);
}

function printReport() {
    showToast(isRTL ? 'جاري الطباعة...' : 'Printing...', 'info');
    window.print();
}

// Delete Functions
function deleteItem(id, itemType, callback) {
    const message = isRTL ? 
        `هل أنت متأكد من حذف ${itemType} رقم ${id}؟` : 
        `Are you sure you want to delete ${itemType} #${id}?`;
    
    confirmAction(message, function() {
        const deleteBtn = event.target.closest('button');
        showLoading(deleteBtn);
        
        // Simulate API call
        setTimeout(() => {
            hideLoading(deleteBtn);
            showToast(isRTL ? `تم حذف ${itemType} بنجاح` : `${itemType} deleted successfully`, 'success');
            
            // Remove the item from DOM
            const itemElement = deleteBtn.closest('.card, tr');
            if (itemElement) {
                itemElement.style.animation = 'fadeOut 0.3s ease-in';
                setTimeout(() => itemElement.remove(), 300);
            }
            
            if (callback) callback();
        }, 1000);
    });
}

// Save Functions
function saveItem(formId, itemType, callback) {
    const form = document.getElementById(formId);
    
    if (!validateForm(form)) {
        showToast(isRTL ? 'يرجى ملء جميع الحقول المطلوبة' : 'Please fill all required fields', 'warning');
        return;
    }
    
    const saveBtn = form.querySelector('.btn-primary');
    showLoading(saveBtn);
    
    // Simulate API call
    setTimeout(() => {
        hideLoading(saveBtn);
        showToast(isRTL ? `تم حفظ ${itemType} بنجاح` : `${itemType} saved successfully`, 'success');
        
        // Close modal if exists
        const modal = form.closest('.modal');
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        }
        
        // Reset form
        form.reset();
        clearFormValidation(form);
        
        if (callback) callback();
    }, 1000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(${isRTL ? '-' : ''}100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(${isRTL ? '-' : ''}100%); opacity: 0; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for common buttons
    document.querySelectorAll('[onclick*="export"]').forEach(btn => {
        if (!btn.onclick) {
            if (btn.textContent.includes('PDF') || btn.textContent.includes('pdf')) {
                btn.onclick = exportToPDF;
            } else if (btn.textContent.includes('Excel') || btn.textContent.includes('excel')) {
                btn.onclick = exportToExcel;
            }
        }
    });
    
    // Add print functionality
    document.querySelectorAll('[onclick*="print"]').forEach(btn => {
        if (!btn.onclick) {
            btn.onclick = printReport;
        }
    });
});
