/**
 * فحص وظائف JavaScript لشاشة المدفوعات والمستحقات
 * JavaScript Functions Testing for Payments and Dues Screen
 */

console.log('🧪 بدء فحص وظائف JavaScript للمدفوعات والمستحقات');

// متغيرات الفحص
let testResults = [];
let testsPassed = 0;
let testsFailed = 0;

/**
 * تسجيل نتيجة الاختبار
 */
function logTest(testName, status, message = '', details = '') {
    const result = {
        test: testName,
        status: status,
        message: message,
        details: details,
        timestamp: new Date().toLocaleTimeString()
    };
    
    testResults.push(result);
    
    const statusIcon = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
    console.log(`${statusIcon} ${testName}: ${message}`);
    
    if (details) {
        console.log(`   📋 ${details}`);
    }
    
    if (status === 'PASS') testsPassed++;
    if (status === 'FAIL') testsFailed++;
}

/**
 * فحص وجود العناصر الأساسية
 */
function testBasicElements() {
    console.log('\n📄 فحص العناصر الأساسية...');
    
    // فحص التبويبات
    const tabs = ['sales', 'purchases', 'expenses', 'payroll'];
    tabs.forEach(tab => {
        const tabElement = document.getElementById(tab);
        if (tabElement) {
            logTest(`تبويب ${tab}`, 'PASS', `تبويب ${tab} موجود`);
        } else {
            logTest(`تبويب ${tab}`, 'FAIL', `تبويب ${tab} غير موجود`);
        }
    });
    
    // فحص الفلاتر
    const filters = [
        'sales-status-filter',
        'purchases-status-filter',
        'expenses-status-filter'
    ];
    
    filters.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            logTest(`فلتر ${filterId}`, 'PASS', `فلتر ${filterId} موجود`);
            
            // فحص خيارات الفلتر
            const options = filter.querySelectorAll('option');
            if (options.length >= 4) {
                logTest(`خيارات ${filterId}`, 'PASS', `${options.length} خيارات متاحة`);
            } else {
                logTest(`خيارات ${filterId}`, 'FAIL', `عدد خيارات غير كافي: ${options.length}`);
            }
        } else {
            logTest(`فلتر ${filterId}`, 'FAIL', `فلتر ${filterId} غير موجود`);
        }
    });
    
    // فحص نافذة الطباعة
    const printModal = document.getElementById('printModal');
    if (printModal) {
        logTest('نافذة الطباعة', 'PASS', 'نافذة الطباعة موجودة');
        
        // فحص عناصر النافذة
        const printType = document.getElementById('printType');
        const printMonth = document.getElementById('printMonth');
        const printStatus = document.getElementById('printStatus');
        
        if (printType && printMonth && printStatus) {
            logTest('عناصر نافذة الطباعة', 'PASS', 'جميع عناصر النافذة موجودة');
        } else {
            logTest('عناصر نافذة الطباعة', 'FAIL', 'بعض عناصر النافذة مفقودة');
        }
    } else {
        logTest('نافذة الطباعة', 'FAIL', 'نافذة الطباعة غير موجودة');
    }
    
    // فحص أزرار الطباعة
    const printButtons = document.querySelectorAll('[onclick*="openPrintModal"]');
    if (printButtons.length >= 4) {
        logTest('أزرار الطباعة', 'PASS', `${printButtons.length} أزرار طباعة موجودة`);
    } else {
        logTest('أزرار الطباعة', 'FAIL', `عدد أزرار طباعة غير كافي: ${printButtons.length}`);
    }
}

/**
 * فحص وظائف الفلاتر
 */
function testFilterFunctions() {
    console.log('\n🔍 فحص وظائف الفلاتر...');
    
    // فحص وجود الوظائف
    const filterFunctions = [
        'filterSalesTable',
        'filterPurchasesTable', 
        'filterExpensesTable',
        'updateFilterCount'
    ];
    
    filterFunctions.forEach(funcName => {
        if (typeof window[funcName] === 'function') {
            logTest(`وظيفة ${funcName}`, 'PASS', `وظيفة ${funcName} موجودة`);
            
            // اختبار تشغيل الوظيفة
            try {
                if (funcName !== 'updateFilterCount') {
                    window[funcName]();
                    logTest(`تشغيل ${funcName}`, 'PASS', `وظيفة ${funcName} تعمل بدون أخطاء`);
                }
            } catch (error) {
                logTest(`تشغيل ${funcName}`, 'FAIL', `خطأ في تشغيل ${funcName}: ${error.message}`);
            }
        } else {
            logTest(`وظيفة ${funcName}`, 'FAIL', `وظيفة ${funcName} غير موجودة`);
        }
    });
}

/**
 * فحص وظائف الطباعة
 */
function testPrintFunctions() {
    console.log('\n🖨️ فحص وظائف الطباعة...');
    
    // فحص وجود الوظائف
    const printFunctions = [
        'openPrintModal',
        'generatePrintReport',
        'printReport'
    ];
    
    printFunctions.forEach(funcName => {
        if (typeof window[funcName] === 'function') {
            logTest(`وظيفة ${funcName}`, 'PASS', `وظيفة ${funcName} موجودة`);
        } else {
            logTest(`وظيفة ${funcName}`, 'FAIL', `وظيفة ${funcName} غير موجودة`);
        }
    });
    
    // اختبار فتح نافذة الطباعة
    try {
        if (typeof openPrintModal === 'function') {
            // محاولة فتح النافذة (بدون عرضها فعلياً)
            const originalShow = bootstrap?.Modal?.prototype?.show;
            let modalShowCalled = false;
            
            if (originalShow) {
                bootstrap.Modal.prototype.show = function() {
                    modalShowCalled = true;
                    return this;
                };
            }
            
            openPrintModal('sales');
            
            if (modalShowCalled || document.getElementById('printModal')?.style.display === 'block') {
                logTest('اختبار فتح نافذة الطباعة', 'PASS', 'نافذة الطباعة تفتح بنجاح');
            } else {
                logTest('اختبار فتح نافذة الطباعة', 'WARN', 'لا يمكن تأكيد فتح النافذة');
            }
            
            // استعادة الوظيفة الأصلية
            if (originalShow) {
                bootstrap.Modal.prototype.show = originalShow;
            }
        }
    } catch (error) {
        logTest('اختبار فتح نافذة الطباعة', 'FAIL', `خطأ في فتح النافذة: ${error.message}`);
    }
}

/**
 * فحص Bootstrap و jQuery
 */
function testDependencies() {
    console.log('\n📚 فحص المكتبات المطلوبة...');
    
    // فحص Bootstrap
    if (typeof bootstrap !== 'undefined') {
        logTest('Bootstrap', 'PASS', 'Bootstrap محمل ومتاح');
        
        // فحص Bootstrap Modal
        if (bootstrap.Modal) {
            logTest('Bootstrap Modal', 'PASS', 'Bootstrap Modal متاح');
        } else {
            logTest('Bootstrap Modal', 'FAIL', 'Bootstrap Modal غير متاح');
        }
    } else {
        logTest('Bootstrap', 'FAIL', 'Bootstrap غير محمل');
    }
    
    // فحص jQuery (اختياري)
    if (typeof $ !== 'undefined') {
        logTest('jQuery', 'PASS', 'jQuery محمل ومتاح');
    } else {
        logTest('jQuery', 'WARN', 'jQuery غير محمل (قد لا يكون مطلوب)');
    }
}

/**
 * فحص البيانات في الجداول
 */
function testTableData() {
    console.log('\n📊 فحص البيانات في الجداول...');
    
    const tables = ['sales', 'purchases', 'expenses', 'payroll'];
    
    tables.forEach(tableId => {
        const table = document.querySelector(`#${tableId} tbody`);
        if (table) {
            const rows = table.querySelectorAll('tr');
            logTest(`جدول ${tableId}`, 'PASS', `جدول ${tableId} موجود مع ${rows.length} صف`);
            
            // فحص وجود أعمدة الحالة
            if (rows.length > 0) {
                const firstRow = rows[0];
                const statusCell = firstRow.cells[6]; // عمود الحالة
                if (statusCell && statusCell.querySelector('.badge')) {
                    logTest(`حالة ${tableId}`, 'PASS', `عمود الحالة موجود في جدول ${tableId}`);
                } else {
                    logTest(`حالة ${tableId}`, 'WARN', `عمود الحالة قد يكون مفقود في جدول ${tableId}`);
                }
            }
        } else {
            logTest(`جدول ${tableId}`, 'FAIL', `جدول ${tableId} غير موجود`);
        }
    });
}

/**
 * إنشاء تقرير شامل
 */
function generateTestReport() {
    console.log('\n' + '='.repeat(80));
    console.log('📊 تقرير فحص JavaScript للمدفوعات والمستحقات');
    console.log('📊 JavaScript Testing Report for Payments and Dues');
    console.log('='.repeat(80));
    
    const totalTests = testResults.length;
    const warningTests = testResults.filter(t => t.status === 'WARN').length;
    const successRate = totalTests > 0 ? (testsPassed / totalTests * 100).toFixed(1) : 0;
    
    console.log(`\n📈 الإحصائيات العامة:`);
    console.log(`   📊 إجمالي الاختبارات: ${totalTests}`);
    console.log(`   ✅ نجح: ${testsPassed}`);
    console.log(`   ❌ فشل: ${testsFailed}`);
    console.log(`   ⚠️ تحذيرات: ${warningTests}`);
    console.log(`   📊 معدل النجاح: ${successRate}%`);
    
    console.log(`\n📋 تفاصيل النتائج:`);
    testResults.forEach(result => {
        const statusIcon = result.status === 'PASS' ? '✅' : result.status === 'FAIL' ? '❌' : '⚠️';
        console.log(`   ${statusIcon} [${result.timestamp}] ${result.test}: ${result.message}`);
    });
    
    console.log(`\n💡 التوصيات:`);
    if (testsFailed === 0) {
        console.log('   🎉 ممتاز! جميع الاختبارات الأساسية نجحت');
        console.log('   🚀 وظائف JavaScript جاهزة للاستخدام');
    } else {
        console.log('   🔧 يحتاج إصلاح الوظائف الفاشلة');
        console.log('   📋 مراجعة الأخطاء المذكورة أعلاه');
    }
    
    if (warningTests > 0) {
        console.log('   ⚠️ مراجعة التحذيرات لتحسين الأداء');
    }
    
    // حفظ النتائج في localStorage
    try {
        localStorage.setItem('paymentsTestResults', JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: {
                total: totalTests,
                passed: testsPassed,
                failed: testsFailed,
                warnings: warningTests,
                successRate: parseFloat(successRate)
            },
            results: testResults
        }));
        console.log('\n💾 تم حفظ النتائج في localStorage');
    } catch (error) {
        console.log(`\n❌ خطأ في حفظ النتائج: ${error.message}`);
    }
    
    return testsFailed === 0;
}

/**
 * تشغيل جميع الاختبارات
 */
function runAllJSTests() {
    console.log('🚀 بدء فحص JavaScript الشامل للمدفوعات والمستحقات...');
    
    // إعادة تعيين المتغيرات
    testResults = [];
    testsPassed = 0;
    testsFailed = 0;
    
    // تشغيل الاختبارات
    testBasicElements();
    testFilterFunctions();
    testPrintFunctions();
    testDependencies();
    testTableData();
    
    // إنشاء التقرير
    const success = generateTestReport();
    
    console.log('\n' + '='.repeat(80));
    if (success) {
        console.log('✅ اكتمل فحص JavaScript بنجاح');
        console.log('✅ JavaScript testing completed successfully');
    } else {
        console.log('⚠️ اكتمل فحص JavaScript مع وجود مشاكل');
        console.log('⚠️ JavaScript testing completed with issues');
    }
    console.log('='.repeat(80));
    
    return success;
}

// تشغيل الاختبارات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // انتظار قليل للتأكد من تحميل جميع العناصر
    setTimeout(() => {
        console.log('🧪 بدء الفحص التلقائي...');
        runAllJSTests();
    }, 1000);
});

// إضافة وظائف للوحة التحكم
window.runPaymentsJSTests = runAllJSTests;
window.getPaymentsTestResults = () => testResults;
window.clearPaymentsTestResults = () => {
    testResults = [];
    testsPassed = 0;
    testsFailed = 0;
    console.log('🧹 تم مسح نتائج الاختبارات');
};
