/**
 * وظائف شاشة المدفوعات والمستحقات
 * Payments & Dues Screen Functions
 */

console.log('🔧 تحميل وظائف المدفوعات والمستحقات...');

// وظائف الطباعة البسيطة لكل قسم

// طباعة فواتير المبيعات
async function printSalesInvoices() {
    console.log('🖨️ طباعة فواتير المبيعات');

    try {
        // محاولة جلب البيانات من API أولاً
        let salesData = [];

        try {
            const response = await fetch('/api/sales/list');
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.sales) {
                    salesData = data.sales;
                }
            }
        } catch (apiError) {
            console.warn('⚠️ فشل جلب البيانات من API، سيتم استخدام البيانات من الجدول');
        }

        // إذا فشل API، استخدم البيانات من الجدول
        if (salesData.length === 0) {
            const salesRows = document.querySelectorAll('#sales-table tbody tr:not(.no-data)');
            if (salesRows.length === 0) {
                alert('لا توجد فواتير مبيعات للطباعة');
                return;
            }

            // تحويل بيانات الجدول إلى تنسيق مناسب
            salesData = Array.from(salesRows).map((row, index) => {
                const cells = row.querySelectorAll('td');
                return {
                    id: index + 1,
                    date: cells[1]?.textContent || 'غير محدد',
                    customer: { name: cells[2]?.textContent || 'عميل غير محدد' },
                    subtotal: parseFloat(cells[3]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    discount: parseFloat(cells[4]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    total: parseFloat(cells[5]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    payment_status: 'unpaid'
                };
            });
        }

        // إنشاء HTML للطباعة
        let printHTML = createPrintHTMLFromData('فواتير المبيعات', salesData, [
            'رقم الفاتورة', 'تاريخ الفاتورة', 'اسم العميل', 'المبلغ الفرعي', 'الخصم', 'المبلغ النهائي', 'حالة الدفع'
        ], 'sales');

        openPrintWindow(printHTML);

    } catch (error) {
        console.error('❌ خطأ في طباعة المبيعات:', error);
        alert('حدث خطأ في طباعة فواتير المبيعات');
    }
}

// طباعة فواتير المشتريات
async function printPurchasesInvoices() {
    console.log('🖨️ طباعة فواتير المشتريات');

    try {
        // محاولة جلب البيانات من API أولاً
        let purchasesData = [];

        try {
            const response = await fetch('/api/purchases/list');
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.purchases) {
                    purchasesData = data.purchases;
                }
            }
        } catch (apiError) {
            console.warn('⚠️ فشل جلب البيانات من API، سيتم استخدام البيانات من الجدول');
        }

        // إذا فشل API، استخدم البيانات من الجدول
        if (purchasesData.length === 0) {
            const purchasesRows = document.querySelectorAll('#purchases-table tbody tr:not(.no-data)');
            if (purchasesRows.length === 0) {
                alert('لا توجد فواتير مشتريات للطباعة');
                return;
            }

            // تحويل بيانات الجدول إلى تنسيق مناسب
            purchasesData = Array.from(purchasesRows).map((row, index) => {
                const cells = row.querySelectorAll('td');
                return {
                    id: index + 1,
                    date: cells[1]?.textContent || 'غير محدد',
                    supplier: { name: cells[2]?.textContent || 'مورد غير محدد' },
                    subtotal: parseFloat(cells[3]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    discount: parseFloat(cells[4]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    total: parseFloat(cells[5]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    payment_status: 'unpaid'
                };
            });
        }

        // إنشاء HTML للطباعة
        let printHTML = createPrintHTMLFromData('فواتير المشتريات', purchasesData, [
            'رقم الفاتورة', 'تاريخ الفاتورة', 'اسم المورد', 'المبلغ الفرعي', 'الخصم', 'المبلغ النهائي', 'حالة الدفع'
        ], 'purchases');

        openPrintWindow(printHTML);

    } catch (error) {
        console.error('❌ خطأ في طباعة المشتريات:', error);
        alert('حدث خطأ في طباعة فواتير المشتريات');
    }
}

// طباعة فواتير المصروفات
async function printExpensesInvoices() {
    console.log('🖨️ طباعة فواتير المصروفات');

    try {
        // محاولة جلب البيانات من API أولاً
        let expensesData = [];

        try {
            const response = await fetch('/api/expenses/list');
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.expenses) {
                    expensesData = data.expenses;
                }
            }
        } catch (apiError) {
            console.warn('⚠️ فشل جلب البيانات من API، سيتم استخدام البيانات من الجدول');
        }

        // إذا فشل API، استخدم البيانات من الجدول
        if (expensesData.length === 0) {
            const expensesRows = document.querySelectorAll('#expenses-table tbody tr:not(.no-data)');
            if (expensesRows.length === 0) {
                alert('لا توجد فواتير مصروفات للطباعة');
                return;
            }

            // تحويل بيانات الجدول إلى تنسيق مناسب
            expensesData = Array.from(expensesRows).map((row, index) => {
                const cells = row.querySelectorAll('td');
                return {
                    id: index + 1,
                    date: cells[1]?.textContent || 'غير محدد',
                    description: cells[2]?.textContent || 'وصف غير محدد',
                    category: cells[3]?.textContent || 'فئة غير محددة',
                    amount: parseFloat(cells[4]?.textContent.replace(/[^\d.-]/g, '')) || 0,
                    payment_status: 'unpaid'
                };
            });
        }

        // إنشاء HTML للطباعة
        let printHTML = createPrintHTMLFromData('فواتير المصروفات', expensesData, [
            'رقم المصروف', 'تاريخ المصروف', 'وصف المصروف', 'الفئة', 'المبلغ', 'حالة الدفع'
        ], 'expenses');

        openPrintWindow(printHTML);

    } catch (error) {
        console.error('❌ خطأ في طباعة المصروفات:', error);
        alert('حدث خطأ في طباعة فواتير المصروفات');
    }
}

// طباعة كشف الرواتب
async function printPayrollInvoices() {
    console.log('🖨️ طباعة كشف الرواتب من قاعدة البيانات');

    try {
        // جلب البيانات الحقيقية من قاعدة البيانات
        const response = await fetch('/api/payroll/list');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.success || !data.payrolls || data.payrolls.length === 0) {
            alert('لا توجد رواتب للطباعة');
            return;
        }

        // إنشاء HTML للطباعة من البيانات الحقيقية
        let printHTML = createPrintHTMLFromData('كشف الرواتب', data.payrolls, [
            'رقم الراتب', 'تاريخ الراتب', 'اسم الموظف', 'الشهر', 'المبلغ', 'حالة الدفع'
        ], 'payroll');

        openPrintWindow(printHTML);

    } catch (error) {
        console.error('❌ خطأ في طباعة الرواتب:', error);
        alert('حدث خطأ في طباعة كشف الرواتب: ' + error.message);
    }
}

// وظيفة جديدة لإنشاء HTML من البيانات الحقيقية
function createPrintHTMLFromData(title, dataArray, headers, dataType) {
    const currentDate = new Date().toLocaleDateString('ar-SA');

    let printHTML = `
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>${title}</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; direction: rtl; }
                .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px; }
                .company-name { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
                .report-title { font-size: 18px; color: #666; margin-bottom: 5px; }
                .report-date { font-size: 14px; color: #999; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
                th { background-color: #f8f9fa; font-weight: bold; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .total { background-color: #e9ecef; font-weight: bold; }
                .status-paid { color: #28a745; font-weight: bold; }
                .status-unpaid { color: #dc3545; font-weight: bold; }
                .status-partial { color: #ffc107; font-weight: bold; }
                @media print { body { margin: 0; } }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-name">نظام المحاسبة المتكامل</div>
                <div class="report-title">${title}</div>
                <div class="report-date">تاريخ التقرير: ${currentDate}</div>
            </div>
            <table>
                <thead>
                    <tr>
    `;

    // إضافة رؤوس الأعمدة
    headers.forEach(header => {
        printHTML += `<th>${header}</th>`;
    });

    printHTML += `
                    </tr>
                </thead>
                <tbody>
    `;

    let totalAmount = 0;

    // إضافة البيانات الحقيقية
    dataArray.forEach(item => {
        printHTML += '<tr>';

        if (dataType === 'sales') {
            const customerName = item.customer ? item.customer.name : 'عميل غير محدد';
            const paymentStatus = getPaymentStatusText(item.payment_status);
            const itemDate = new Date(item.date).toLocaleDateString('ar-SA');

            printHTML += `
                <td>${item.id}</td>
                <td>${itemDate}</td>
                <td>${customerName}</td>
                <td>${item.subtotal.toFixed(2)} ريال</td>
                <td>${item.discount.toFixed(2)} ريال</td>
                <td>${item.total.toFixed(2)} ريال</td>
                <td class="status-${item.payment_status}">${paymentStatus}</td>
            `;
            totalAmount += item.total;

        } else if (dataType === 'purchases') {
            const supplierName = item.supplier ? item.supplier.name : 'مورد غير محدد';
            const paymentStatus = getPaymentStatusText(item.payment_status);
            const itemDate = new Date(item.date).toLocaleDateString('ar-SA');

            printHTML += `
                <td>${item.id}</td>
                <td>${itemDate}</td>
                <td>${supplierName}</td>
                <td>${item.subtotal.toFixed(2)} ريال</td>
                <td>${item.discount.toFixed(2)} ريال</td>
                <td>${item.total.toFixed(2)} ريال</td>
                <td class="status-${item.payment_status}">${paymentStatus}</td>
            `;
            totalAmount += item.total;

        } else if (dataType === 'expenses') {
            const paymentStatus = getPaymentStatusText(item.payment_status);
            const itemDate = new Date(item.date).toLocaleDateString('ar-SA');

            printHTML += `
                <td>${item.id}</td>
                <td>${itemDate}</td>
                <td>${item.description}</td>
                <td>${item.category || 'غير محدد'}</td>
                <td>${item.amount.toFixed(2)} ريال</td>
                <td class="status-${item.payment_status}">${paymentStatus}</td>
            `;
            totalAmount += item.amount;

        } else if (dataType === 'payroll') {
            const employeeName = item.employee ? item.employee.name : 'موظف غير محدد';
            const paymentStatus = getPaymentStatusText(item.payment_status);
            const itemDate = new Date(item.date).toLocaleDateString('ar-SA');

            printHTML += `
                <td>${item.id}</td>
                <td>${itemDate}</td>
                <td>${employeeName}</td>
                <td>${item.month}</td>
                <td>${item.amount.toFixed(2)} ريال</td>
                <td class="status-${item.payment_status}">${paymentStatus}</td>
            `;
            totalAmount += item.amount;
        }

        printHTML += '</tr>';
    });

    printHTML += `
                </tbody>
                <tfoot>
                    <tr class="total">
                        <td colspan="${headers.length - 1}">المجموع الإجمالي</td>
                        <td>${totalAmount.toFixed(2)} ريال</td>
                    </tr>
                </tfoot>
                </table>
                <div style="text-align: center; margin-top: 30px; color: #666;">
                    تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل - ${currentDate}
                </div>
            </body>
            </html>
    `;

    return printHTML;
}

function getPaymentStatusText(status) {
    const statusMap = {
        'paid': 'مدفوع',
        'partial': 'مدفوع جزئياً',
        'unpaid': 'غير مدفوع',
        'overdue': 'متأخر'
    };
    return statusMap[status] || 'غير محدد';
}

// وظيفة مساعدة لإنشاء HTML للطباعة (النسخة القديمة للتوافق)
function createPrintHTML(title, rows, headers) {
    let printHTML = `
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>${title}</title>
            <style>
                body { font-family: Arial, sans-serif; direction: rtl; margin: 20px; }
                h1 { text-align: center; color: #333; margin-bottom: 30px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                th { background-color: #f2f2f2; font-weight: bold; }
                .total { font-weight: bold; background-color: #e9ecef; }
                .print-date { text-align: left; margin-bottom: 20px; color: #666; }
            </style>
        </head>
        <body>
            <div class="print-date">تاريخ الطباعة: ${new Date().toLocaleDateString('ar-SA')}</div>
            <h1>${title}</h1>
            <table>
                <thead><tr>
    `;

    // إضافة رؤوس الأعمدة
    headers.forEach(header => {
        printHTML += `<th>${header}</th>`;
    });

    printHTML += '</tr></thead><tbody>';

    let totalAmount = 0;

    // إضافة صفوف البيانات
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        printHTML += '<tr>';

        cells.forEach((cell, index) => {
            const cellText = cell.textContent.trim();
            printHTML += `<td>${cellText}</td>`;

            // حساب المجموع من عمود المبلغ (عادة العمود الرابع أو الثالث)
            if (index === 3 || index === 4) {
                const amount = parseFloat(cellText.replace(/[^\d.-]/g, ''));
                if (!isNaN(amount)) {
                    totalAmount += amount;
                }
            }
        });

        printHTML += '</tr>';
    });

    printHTML += `
            </tbody>
            <tfoot>
                <tr class="total">
                    <td colspan="${headers.length - 1}">المجموع الإجمالي</td>
                    <td>${totalAmount.toFixed(2)} ريال</td>
                </tr>
            </tfoot>
            </table>
            <div style="text-align: center; margin-top: 30px; color: #666;">
                تم إنشاء هذا التقرير بواسطة نظام المحاسبة المتكامل
            </div>
        </body>
        </html>
    `;

    return printHTML;
}

// وظيفة مساعدة لفتح نافذة الطباعة
function openPrintWindow(htmlContent) {
    const printWindow = window.open('', '_blank', 'width=1000,height=700,scrollbars=yes');
    
    if (!printWindow) {
        alert('تم حظر النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة وإعادة المحاولة.');
        return;
    }
    
    printWindow.document.write(htmlContent);
    printWindow.document.close();

    // تشغيل الطباعة تلقائياً
    printWindow.onload = function() {
        setTimeout(() => {
            printWindow.print();
        }, 500);
    };

    console.log('✅ تم فتح نافذة الطباعة');
}

// وظائف اختبار سريع
function testPrintModal() {
    console.log('🧪 اختبار نافذة الطباعة');
    
    // اختبار طباعة المبيعات
    printSalesInvoices();
}

function quickPrintTest() {
    console.log('⚡ اختبار سريع للطباعة');
    
    // إنشاء بيانات تجريبية للاختبار
    const testHTML = createPrintHTML('اختبار الطباعة', [], ['العمود 1', 'العمود 2', 'المبلغ']);
    
    if (testHTML.includes('اختبار الطباعة')) {
        alert('✅ وظائف الطباعة تعمل بشكل صحيح!');
        console.log('✅ اختبار الطباعة نجح');
    } else {
        alert('❌ هناك مشكلة في وظائف الطباعة');
        console.error('❌ اختبار الطباعة فشل');
    }
}

function showDirectPrintForm() {
    console.log('🖨️ فتح form الطباعة المباشر');
    
    // إنشاء نافذة طباعة مباشرة
    const currentMonth = new Date().getFullYear() + '-' + String(new Date().getMonth() + 1).padStart(2, '0');
    const printUrl = `/print_invoices_preview?type=sales&month=${currentMonth}&status=all&details=true`;
    
    window.open(printUrl, '_blank', 'width=1200,height=800,scrollbars=yes');
    
    console.log('✅ تم فتح نافذة الطباعة المباشرة');
}

// تهيئة الوظائف عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ تم تحميل وظائف المدفوعات والمستحقات');
    
    // إضافة event listeners للأزرار
    const printButtons = document.querySelectorAll('[onclick*="print"]');
    console.log(`📊 عدد أزرار الطباعة الموجودة: ${printButtons.length}`);
    
    // تحقق من وجود الجداول
    const tables = ['#sales-table', '#purchases-table', '#expenses-table', '#payroll-table'];
    tables.forEach(tableId => {
        const table = document.querySelector(tableId);
        if (table) {
            console.log(`✅ جدول ${tableId} موجود`);
        } else {
            console.warn(`⚠️ جدول ${tableId} غير موجود`);
        }
    });
});

console.log('✅ تم تحميل جميع وظائف المدفوعات والمستحقات');
