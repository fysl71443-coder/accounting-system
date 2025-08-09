/**
 * وظائف CRUD الموحدة
 * Unified CRUD Functions
 */

// متغيرات عامة
let selectedItemId = null;
let isEditMode = false;
let currentLanguage = 'ar';

// تحديد اللغة
function setLanguage(lang) {
    currentLanguage = lang;
}

// رسائل متعددة اللغات
const messages = {
    ar: {
        saveSuccess: 'تم الحفظ بنجاح',
        deleteSuccess: 'تم الحذف بنجاح',
        updateSuccess: 'تم التحديث بنجاح',
        addSuccess: 'تم الإضافة بنجاح',
        confirmDelete: 'هل أنت متأكد من الحذف؟',
        selectItem: 'يرجى اختيار عنصر',
        fillRequired: 'يرجى ملء جميع الحقول المطلوبة',
        saving: 'جاري الحفظ...',
        deleting: 'جاري الحذف...',
        loading: 'جاري التحميل...',
        error: 'حدث خطأ',
        exportSuccess: 'تم التصدير بنجاح',
        refreshSuccess: 'تم التحديث بنجاح'
    },
    en: {
        saveSuccess: 'Saved successfully',
        deleteSuccess: 'Deleted successfully',
        updateSuccess: 'Updated successfully',
        addSuccess: 'Added successfully',
        confirmDelete: 'Are you sure you want to delete?',
        selectItem: 'Please select an item',
        fillRequired: 'Please fill all required fields',
        saving: 'Saving...',
        deleting: 'Deleting...',
        loading: 'Loading...',
        error: 'An error occurred',
        exportSuccess: 'Exported successfully',
        refreshSuccess: 'Refreshed successfully'
    }
};

// الحصول على رسالة باللغة المحددة
function getMessage(key) {
    return messages[currentLanguage][key] || messages.ar[key];
}

// عرض إشعار
function showToast(message, type = 'info', duration = 3000) {
    // إنشاء حاوية الإشعارات إذا لم تكن موجودة
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // إنشاء الإشعار
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${iconMap[type]} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // عرض الإشعار
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: duration });
    toast.show();
    
    // إزالة الإشعار بعد الإخفاء
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// عرض حالة التحميل على الزر
function showLoading(button, text = null) {
    if (!button) return;
    
    button.dataset.originalText = button.innerHTML;
    button.disabled = true;
    
    const loadingText = text || getMessage('loading');
    button.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i>${loadingText}`;
}

// إخفاء حالة التحميل من الزر
function hideLoading(button) {
    if (!button) return;
    
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || button.innerHTML;
}

// وظائف CRUD الأساسية

// إضافة عنصر جديد
function addNew() {
    isEditMode = false;
    selectedItemId = null;
    
    // مسح النموذج
    const form = document.querySelector('form');
    if (form) {
        form.reset();
    }
    
    // عرض النموذج
    const modal = document.querySelector('.modal');
    if (modal) {
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
    }
    
    console.log('🆕 إضافة عنصر جديد');
}

// تعديل عنصر محدد
function editSelected(itemId = null) {
    const id = itemId || selectedItemId;
    
    if (!id) {
        showToast(getMessage('selectItem'), 'warning');
        return;
    }
    
    isEditMode = true;
    selectedItemId = id;
    
    console.log('✏️ تعديل العنصر:', id);
    
    // هنا يتم تحميل بيانات العنصر
    loadItemData(id);
}

// حذف عنصر محدد
function deleteSelected(itemId = null) {
    const id = itemId || selectedItemId;
    
    if (!id) {
        showToast(getMessage('selectItem'), 'warning');
        return;
    }
    
    if (confirm(getMessage('confirmDelete'))) {
        const deleteBtn = document.querySelector(`[onclick*="deleteSelected(${id})"]`);
        showLoading(deleteBtn, getMessage('deleting'));
        
        // محاكاة استدعاء API
        setTimeout(() => {
            hideLoading(deleteBtn);
            
            // إزالة العنصر من الجدول
            const row = deleteBtn?.closest('tr');
            if (row) {
                row.remove();
            }
            
            showToast(getMessage('deleteSuccess'), 'success');
            selectedItemId = null;
        }, 1000);
    }
}

// حفظ البيانات
function saveData() {
    const form = document.querySelector('form');
    const saveBtn = document.querySelector('.btn-primary[onclick*="saveData"]');
    
    if (!form) {
        showToast(getMessage('error'), 'danger');
        return;
    }
    
    if (!form.checkValidity()) {
        form.reportValidity();
        showToast(getMessage('fillRequired'), 'warning');
        return;
    }
    
    showLoading(saveBtn, getMessage('saving'));
    
    // محاكاة استدعاء API
    setTimeout(() => {
        hideLoading(saveBtn);
        
        const message = isEditMode ? getMessage('updateSuccess') : getMessage('addSuccess');
        showToast(message, 'success');
        
        // إغلاق النموذج
        const modal = bootstrap.Modal.getInstance(document.querySelector('.modal'));
        if (modal) {
            modal.hide();
        }
        
        // إعادة تحميل البيانات
        refreshData();
    }, 1500);
}

// إلغاء العملية
function cancelOperation() {
    selectedItemId = null;
    isEditMode = false;
    
    const form = document.querySelector('form');
    if (form) {
        form.reset();
    }
}

// تحديث البيانات
function refreshData() {
    const refreshBtn = document.querySelector('[onclick*="refreshData"]');
    showLoading(refreshBtn, getMessage('loading'));
    
    setTimeout(() => {
        hideLoading(refreshBtn);
        showToast(getMessage('refreshSuccess'), 'success');
        
        // إعادة تحميل الصفحة أو البيانات
        location.reload();
    }, 1000);
}

// تصدير البيانات
function exportData() {
    const exportBtn = document.querySelector('[onclick*="exportData"]');
    showLoading(exportBtn, 'جاري التصدير...');
    
    setTimeout(() => {
        hideLoading(exportBtn);
        showToast(getMessage('exportSuccess'), 'success');
    }, 1500);
}

// تحميل بيانات العنصر للتعديل
function loadItemData(id) {
    console.log('📥 تحميل بيانات العنصر:', id);
    
    // هنا يتم تحميل البيانات من API
    // وملء النموذج بالبيانات
    
    // عرض النموذج
    const modal = document.querySelector('.modal');
    if (modal) {
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
    }
}

// تحديد العنصر المحدد
function selectItem(id) {
    selectedItemId = id;
    
    // إزالة التحديد من جميع الصفوف
    document.querySelectorAll('tr.selected').forEach(row => {
        row.classList.remove('selected');
    });
    
    // إضافة التحديد للصف الحالي
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) {
        row.classList.add('selected');
    }
}

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // تحديد اللغة من الجلسة
    const lang = document.documentElement.lang || 'ar';
    setLanguage(lang);
    
    // إضافة مستمعي الأحداث للجداول
    document.querySelectorAll('table tbody tr').forEach(row => {
        row.addEventListener('click', function() {
            const id = this.dataset.id;
            if (id) {
                selectItem(id);
            }
        });
    });
    
    console.log('✅ تم تهيئة وظائف CRUD');
});
