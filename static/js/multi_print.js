/**
 * وظائف الطباعة المتعددة للفواتير
 * Multi-Print Functions for Invoices
 */

console.log('🖨️ تحميل وظائف الطباعة المتعددة...');

// وظائف المبيعات
function toggleAllSales(masterCheckbox) {
    console.log('🔄 تبديل تحديد جميع المبيعات:', masterCheckbox.checked);
    
    const checkboxes = document.querySelectorAll('.sales-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = masterCheckbox.checked;
    });
    
    updateSalesCounter();
}

function selectAllSales() {
    console.log('✅ تحديد جميع المبيعات');
    
    const masterCheckbox = document.getElementById('selectAllSalesCheckbox');
    const checkboxes = document.querySelectorAll('.sales-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
    });
    
    if (masterCheckbox) {
        masterCheckbox.checked = true;
    }
    
    updateSalesCounter();
}

function updateSalesCounter() {
    const selectedCheckboxes = document.querySelectorAll('.sales-checkbox:checked');
    const count = selectedCheckboxes.length;
    
    console.log(`📊 عدد المبيعات المحددة: ${count}`);
    
    // تحديث النص في الزر
    const printButton = document.querySelector('[onclick="printSelectedSales()"]');
    if (printButton) {
        const icon = printButton.querySelector('i');
        const iconHTML = icon ? icon.outerHTML : '<i class="fas fa-print me-1"></i>';
        printButton.innerHTML = `${iconHTML} طباعة المحدد (${count})`;
        
        // تفعيل/إلغاء تفعيل الزر
        printButton.disabled = count === 0;
        if (count === 0) {
            printButton.classList.add('disabled');
        } else {
            printButton.classList.remove('disabled');
        }
    }
}

function printSelectedSales() {
    console.log('🖨️ طباعة المبيعات المحددة');
    
    const selectedCheckboxes = document.querySelectorAll('.sales-checkbox:checked');
    
    if (selectedCheckboxes.length === 0) {
        alert('يرجى تحديد فاتورة واحدة على الأقل للطباعة');
        return;
    }
    
    // جمع بيانات الفواتير المحددة
    const selectedInvoices = [];
    selectedCheckboxes.forEach(checkbox => {
        selectedInvoices.push({
            id: checkbox.value,
            invoice_number: checkbox.dataset.invoice,
            customer: checkbox.dataset.customer,
            amount: parseFloat(checkbox.dataset.amount),
            date: checkbox.dataset.date
        });
    });
    
    console.log('📋 الفواتير المحددة:', selectedInvoices);
    
    // إنشاء HTML للطباعة
    const printHTML = createSalesPrintHTML(selectedInvoices);
    
    // فتح نافذة الطباعة
    openPrintWindow(printHTML);
}

function createSalesPrintHTML(invoices) {
    const currentDate = new Date().toLocaleDateString('ar-SA');
    let totalAmount = 0;
    
    let html = `
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>فواتير المبيعات المحددة</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    direction: rtl; 
                    margin: 20px;
                    background: white;
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 30px; 
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 20px;
                }
                .company-name { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #007bff; 
                    margin-bottom: 10px;
                }
                .report-title { 
                    font-size: 20px; 
                    color: #333; 
                    margin-bottom: 5px;
                }
                .print-date { 
                    color: #666; 
                    font-size: 14px;
                }
                table { 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 12px 8px; 
                    text-align: center;
                }
                th { 
                    background-color: #007bff; 
                    color: white; 
                    font-weight: bold;
                }
                tr:nth-child(even) { 
                    background-color: #f8f9fa; 
                }
                .total-row { 
                    background-color: #e3f2fd !important; 
                    font-weight: bold;
                    font-size: 16px;
                }
                .footer { 
                    text-align: center; 
                    margin-top: 30px; 
                    color: #666; 
                    font-size: 12px;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }
                @media print {
                    body { margin: 0; }
                    .no-print { display: none !important; }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="report-title">تقرير فواتير المبيعات المحددة</div>
                <div class="print-date">تاريخ الطباعة: ${currentDate}</div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>رقم الفاتورة</th>
                        <th>العميل</th>
                        <th>التاريخ</th>
                        <th>المبلغ (ريال)</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    // إضافة صفوف الفواتير
    invoices.forEach((invoice, index) => {
        totalAmount += invoice.amount;
        html += `
                    <tr>
                        <td><strong>${invoice.invoice_number}</strong></td>
                        <td>${invoice.customer}</td>
                        <td>${invoice.date}</td>
                        <td>${invoice.amount.toFixed(2)} ريال</td>
                    </tr>
        `;
    });
    
    // إضافة صف المجموع
    html += `
                    <tr class="total-row">
                        <td colspan="3">المجموع الإجمالي</td>
                        <td>${totalAmount.toFixed(2)} ريال</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="footer">
                <p>عدد الفواتير: ${invoices.length} فاتورة</p>
                <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
            </div>
        </body>
        </html>
    `;
    
    return html;
}

// وظائف المشتريات
function toggleAllPurchases(masterCheckbox) {
    console.log('🔄 تبديل تحديد جميع المشتريات:', masterCheckbox.checked);
    
    const checkboxes = document.querySelectorAll('.purchases-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = masterCheckbox.checked;
    });
    
    updatePurchasesCounter();
}

function selectAllPurchases() {
    console.log('✅ تحديد جميع المشتريات');
    
    const checkboxes = document.querySelectorAll('.purchases-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
    });
    
    updatePurchasesCounter();
}

function updatePurchasesCounter() {
    const selectedCheckboxes = document.querySelectorAll('.purchases-checkbox:checked');
    const count = selectedCheckboxes.length;
    
    console.log(`📊 عدد المشتريات المحددة: ${count}`);
    
    const printButton = document.querySelector('[onclick="printSelectedPurchases()"]');
    if (printButton) {
        const icon = printButton.querySelector('i');
        const iconHTML = icon ? icon.outerHTML : '<i class="fas fa-print me-1"></i>';
        printButton.innerHTML = `${iconHTML} طباعة المحدد (${count})`;
        printButton.disabled = count === 0;
        
        if (count === 0) {
            printButton.classList.add('disabled');
        } else {
            printButton.classList.remove('disabled');
        }
    }
}

function printSelectedPurchases() {
    console.log('🖨️ طباعة المشتريات المحددة');
    
    const selectedCheckboxes = document.querySelectorAll('.purchases-checkbox:checked');
    
    if (selectedCheckboxes.length === 0) {
        alert('يرجى تحديد فاتورة واحدة على الأقل للطباعة');
        return;
    }
    
    // جمع بيانات الفواتير المحددة
    const selectedInvoices = [];
    selectedCheckboxes.forEach(checkbox => {
        selectedInvoices.push({
            id: checkbox.value,
            invoice_number: checkbox.dataset.invoice,
            supplier: checkbox.dataset.supplier,
            amount: parseFloat(checkbox.dataset.amount),
            date: checkbox.dataset.date
        });
    });
    
    console.log('📋 المشتريات المحددة:', selectedInvoices);
    
    // إنشاء HTML للطباعة
    const printHTML = createPurchasesPrintHTML(selectedInvoices);
    
    // فتح نافذة الطباعة
    openPrintWindow(printHTML);
}

function createPurchasesPrintHTML(invoices) {
    const currentDate = new Date().toLocaleDateString('ar-SA');
    let totalAmount = 0;
    
    let html = `
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>فواتير المشتريات المحددة</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; margin: 20px; background: white; }
                .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #28a745; padding-bottom: 20px; }
                .company-name { font-size: 24px; font-weight: bold; color: #28a745; margin-bottom: 10px; }
                .report-title { font-size: 20px; color: #333; margin-bottom: 5px; }
                .print-date { color: #666; font-size: 14px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                th, td { border: 1px solid #ddd; padding: 12px 8px; text-align: center; }
                th { background-color: #28a745; color: white; font-weight: bold; }
                tr:nth-child(even) { background-color: #f8f9fa; }
                .total-row { background-color: #d4edda !important; font-weight: bold; font-size: 16px; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 20px; }
                @media print { body { margin: 0; } .no-print { display: none !important; } }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="report-title">تقرير فواتير المشتريات المحددة</div>
                <div class="print-date">تاريخ الطباعة: ${currentDate}</div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>رقم الفاتورة</th>
                        <th>المورد</th>
                        <th>التاريخ</th>
                        <th>المبلغ (ريال)</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    invoices.forEach((invoice, index) => {
        totalAmount += invoice.amount;
        html += `
                    <tr>
                        <td><strong>${invoice.invoice_number}</strong></td>
                        <td>${invoice.supplier}</td>
                        <td>${invoice.date}</td>
                        <td>${invoice.amount.toFixed(2)} ريال</td>
                    </tr>
        `;
    });
    
    html += `
                    <tr class="total-row">
                        <td colspan="3">المجموع الإجمالي</td>
                        <td>${totalAmount.toFixed(2)} ريال</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="footer">
                <p>عدد الفواتير: ${invoices.length} فاتورة</p>
                <p>تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل</p>
            </div>
        </body>
        </html>
    `;
    
    return html;
}

// وظيفة مساعدة لفتح نافذة الطباعة
function openPrintWindow(htmlContent) {
    console.log('🖨️ فتح نافذة الطباعة');
    
    const printWindow = window.open('', '_blank', 'width=1000,height=700,scrollbars=yes,resizable=yes');
    
    if (!printWindow) {
        alert('تم حظر النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة وإعادة المحاولة.');
        return;
    }
    
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    
    // تشغيل الطباعة تلقائياً بعد تحميل المحتوى
    printWindow.onload = function() {
        setTimeout(() => {
            printWindow.print();
        }, 500);
    };
    
    console.log('✅ تم فتح نافذة الطباعة بنجاح');
}

// تهيئة الوظائف عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ تم تحميل وظائف الطباعة المتعددة');
    
    // إضافة event listeners للـ checkboxes
    const salesCheckboxes = document.querySelectorAll('.sales-checkbox');
    salesCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSalesCounter);
    });
    
    const purchasesCheckboxes = document.querySelectorAll('.purchases-checkbox');
    purchasesCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updatePurchasesCounter);
    });
    
    // تحديث العدادات الأولية
    updateSalesCounter();
    updatePurchasesCounter();
});

console.log('✅ تم تحميل جميع وظائف الطباعة المتعددة');
