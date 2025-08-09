/**
 * JavaScript للمدفوعات والمستحقات
 * Payments and Dues JavaScript Functions
 */

console.log('📄 تم تحميل ملف payments_dues.js');

// Global variables
let currentFilters = {
    sales: 'all',
    purchases: 'all', 
    expenses: 'all',
    payroll: 'all'
};

/**
 * فتح نافذة الطباعة
 * Open print modal
 */
function openPrintModal(type) {
    console.log('🖨️ فتح نافذة الطباعة لنوع:', type);
    
    try {
        const modalElement = document.getElementById('printModal');
        if (!modalElement) {
            throw new Error('نافذة الطباعة غير موجودة');
        }

        const printType = document.getElementById('printType');
        const printMonth = document.getElementById('printMonth');

        if (!printType || !printMonth) {
            throw new Error('عناصر النافذة غير موجودة');
        }

        // Set the invoice type
        printType.value = type;

        // Update the option text based on type
        const typeTexts = {
            'sales': 'فواتير المبيعات',
            'purchases': 'فواتير المشتريات',
            'expenses': 'فواتير المصروفات',
            'payroll': 'رواتب الموظفين'
        };

        printType.innerHTML = `<option value="${type}">${typeTexts[type]}</option>`;

        // Set current month as default
        const now = new Date();
        const currentMonth = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
        printMonth.value = currentMonth;

        // Create and show modal
        let modal;
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            // Fallback for when Bootstrap is not available
            modalElement.style.display = 'block';
            modalElement.classList.add('show');
            modalElement.style.backgroundColor = 'rgba(0,0,0,0.5)';
        }

        console.log('✅ تم فتح نافذة الطباعة بنجاح');
        
    } catch (error) {
        console.error('❌ خطأ في فتح نافذة الطباعة:', error);
        alert('حدث خطأ في فتح نافذة الطباعة: ' + error.message);
    }
}

/**
 * فلترة جدول المبيعات
 * Filter sales table
 */
function filterSalesTable() {
    filterTable('sales', 'sales-status-filter');
}

/**
 * فلترة جدول المشتريات
 * Filter purchases table
 */
function filterPurchasesTable() {
    filterTable('purchases', 'purchases-status-filter');
}

/**
 * فلترة جدول المصروفات
 * Filter expenses table
 */
function filterExpensesTable() {
    filterTable('expenses', 'expenses-status-filter');
}

/**
 * فلترة جدول عام
 * Generic table filter function
 */
function filterTable(tableType, filterId) {
    console.log(`🔍 تطبيق فلتر ${tableType}`);
    
    try {
        const filter = document.getElementById(filterId);
        if (!filter) {
            throw new Error(`فلتر ${filterId} غير موجود`);
        }
        
        const filterValue = filter.value;
        currentFilters[tableType] = filterValue;
        
        console.log('📋 الفلتر المحدد:', filterValue);
        
        const table = document.querySelector(`#${tableType} tbody`);
        if (!table) {
            throw new Error(`جدول ${tableType} غير موجود`);
        }
        
        const rows = table.querySelectorAll('tr');
        console.log('📊 عدد الصفوف:', rows.length);
        
        let visibleCount = 0;
        
        rows.forEach((row, index) => {
            if (row.cells.length < 7) {
                console.log(`⚠️ صف ${index} لا يحتوي على عدد كافي من الخلايا`);
                return;
            }
            
            const statusCell = row.cells[6]; // Status column
            const statusBadge = statusCell.querySelector('.badge');
            
            if (!statusBadge) {
                console.log(`⚠️ صف ${index} لا يحتوي على badge للحالة`);
                return;
            }
            
            let status = 'pending';
            if (statusBadge.classList.contains('bg-success')) status = 'paid';
            else if (statusBadge.classList.contains('bg-warning')) status = 'partial';
            
            if (filterValue === 'all' || filterValue === status) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        console.log(`✅ تم عرض ${visibleCount} صف من أصل ${rows.length}`);
        updateFilterCount(tableType, filterValue, visibleCount);
        
    } catch (error) {
        console.error(`❌ خطأ في فلتر ${tableType}:`, error);
        alert(`حدث خطأ في الفلتر: ${error.message}`);
    }
}

/**
 * تحديث عداد الفلتر
 * Update filter count
 */
function updateFilterCount(type, filter, visibleCount) {
    try {
        const badge = document.querySelector(`#${type} .badge`);
        
        if (badge) {
            const filterText = filter === 'all' ? 'الكل' : 
                              filter === 'paid' ? 'مدفوع' :
                              filter === 'partial' ? 'جزئي' : 'معلق';
            badge.textContent = `${visibleCount} - ${filterText}`;
            console.log(`📊 تم تحديث العداد لـ ${type}: ${visibleCount} - ${filterText}`);
        } else {
            console.warn(`⚠️ لم يتم العثور على badge لـ ${type}`);
        }
    } catch (error) {
        console.error('❌ خطأ في تحديث العداد:', error);
    }
}

/**
 * إنشاء معاينة التقرير
 * Generate print report preview
 */
function generatePrintReport() {
    console.log('📄 إنشاء معاينة التقرير');
    
    try {
        const type = document.getElementById('printType').value;
        const month = document.getElementById('printMonth').value;
        const status = document.getElementById('printStatus').value;
        const includeDetails = document.getElementById('includeDetails').checked;

        console.log('📋 معاملات التقرير:', { type, month, status, includeDetails });

        if (!month) {
            alert('يرجى اختيار الشهر والسنة');
            return;
        }

        const url = `/print_invoices_preview?type=${type}&month=${month}&status=${status}&details=${includeDetails}`;
        console.log('🔗 رابط المعاينة:', url);
        
        const previewWindow = window.open(url, '_blank', 'width=1000,height=700,scrollbars=yes');
        
        if (!previewWindow) {
            alert('تم حظر النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة وإعادة المحاولة.');
            return;
        }
        
        console.log('✅ تم فتح معاينة التقرير');
        
    } catch (error) {
        console.error('❌ خطأ في إنشاء التقرير:', error);
        alert('حدث خطأ في إنشاء التقرير: ' + error.message);
    }
}

/**
 * طباعة التقرير مباشرة
 * Print report directly
 */
function printReport() {
    console.log('🖨️ طباعة التقرير مباشرة');
    
    try {
        const type = document.getElementById('printType').value;
        const month = document.getElementById('printMonth').value;
        const status = document.getElementById('printStatus').value;
        const includeDetails = document.getElementById('includeDetails').checked;

        if (!month) {
            alert('يرجى اختيار الشهر والسنة');
            return;
        }

        // Close modal
        const modalElement = document.getElementById('printModal');
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) modal.hide();
        } else {
            modalElement.style.display = 'none';
            modalElement.classList.remove('show');
        }

        // Open print page and trigger print
        const url = `/print_invoices?type=${type}&month=${month}&status=${status}&details=${includeDetails}`;
        const printWindow = window.open(url, '_blank', 'width=1000,height=700');

        if (!printWindow) {
            alert('تم حظر النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة وإعادة المحاولة.');
            return;
        }

        printWindow.onload = function() {
            setTimeout(() => {
                printWindow.print();
            }, 500);
        };
        
        console.log('✅ تم إرسال أمر الطباعة');
        
    } catch (error) {
        console.error('❌ خطأ في الطباعة:', error);
        alert('حدث خطأ في الطباعة: ' + error.message);
    }
}

/**
 * وظائف الاختبار
 * Test functions
 */
function testPrintModal() {
    console.log('🧪 اختبار نافذة الطباعة');
    openPrintModal('sales');
}

function testFilters() {
    console.log('🧪 اختبار الفلاتر');
    filterSalesTable();
    filterPurchasesTable();
    filterExpensesTable();
}

/**
 * تهيئة الصفحة
 * Page initialization
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 تم تحميل صفحة المدفوعات والمستحقات');
    
    // تحقق من وجود Bootstrap
    if (typeof bootstrap === 'undefined') {
        console.warn('⚠️ Bootstrap غير متاح');
    } else {
        console.log('✅ Bootstrap متاح');
    }
    
    // تحقق من وجود عناصر الفلاتر
    const filters = [
        'sales-status-filter',
        'purchases-status-filter', 
        'expenses-status-filter'
    ];
    
    filters.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            console.log(`✅ فلتر ${filterId} موجود`);
        } else {
            console.warn(`⚠️ فلتر ${filterId} غير موجود`);
        }
    });
    
    // تحقق من وجود نافذة الطباعة
    const printModal = document.getElementById('printModal');
    if (printModal) {
        console.log('✅ نافذة الطباعة موجودة');
    } else {
        console.warn('⚠️ نافذة الطباعة غير موجودة');
    }
    
    // تحقق من وجود أزرار الطباعة
    const printButtons = document.querySelectorAll('[onclick*="openPrintModal"]');
    console.log(`📊 عدد أزرار الطباعة: ${printButtons.length}`);
    
    console.log('🎉 تم تهيئة الصفحة بنجاح');
});
