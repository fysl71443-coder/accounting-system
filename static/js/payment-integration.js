/**
 * نظام ربط المدفوعات والمستحقات
 * Payment Integration System
 */

class PaymentIntegrationSystem {
    constructor() {
        this.updateInterval = 30000; // 30 ثانية
        this.isMonitoring = false;
        this.lastUpdate = null;
        this.pendingUpdates = new Set();
        
        this.init();
    }

    init() {
        // بدء مراقبة التحديثات
        this.startMonitoring();
        
        // ربط الأحداث
        this.setupEventListeners();
        
        console.log('🔗 نظام ربط المدفوعات مفعل');
    }

    startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        
        // تحديث دوري للبيانات
        setInterval(() => {
            this.checkForUpdates();
        }, this.updateInterval);
        
        // تحديث فوري عند التركيز على النافذة
        window.addEventListener('focus', () => {
            this.checkForUpdates();
        });
    }

    setupEventListeners() {
        // مراقبة تغييرات النماذج
        document.addEventListener('DOMContentLoaded', () => {
            this.attachFormListeners();
        });

        // مراقبة العمليات الجديدة
        document.addEventListener('operationCompleted', (event) => {
            this.handleOperationCompleted(event.detail);
        });
    }

    attachFormListeners() {
        // مراقبة نماذج المبيعات
        const salesForms = document.querySelectorAll('.sales-form');
        salesForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleSalesSubmit(e);
            });
        });

        // مراقبة نماذج المشتريات
        const purchaseForms = document.querySelectorAll('.purchases-form');
        purchaseForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handlePurchaseSubmit(e);
            });
        });

        // مراقبة نماذج المصروفات
        const expenseForms = document.querySelectorAll('.expenses-form');
        expenseForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleExpenseSubmit(e);
            });
        });

        // مراقبة نماذج الرواتب
        const payrollForms = document.querySelectorAll('.payroll-form');
        payrollForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handlePayrollSubmit(e);
            });
        });
    }

    async handleSalesSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // تحديد حالة الدفع
        data.payment_status = this.determinePaymentStatus(data);
        
        // إضافة للتحديثات المعلقة
        this.pendingUpdates.add({
            type: 'sale',
            data: data,
            timestamp: Date.now()
        });
        
        // إشعار نظام المدفوعات
        this.notifyPaymentSystem('sale_created', data);
    }

    async handlePurchaseSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        data.payment_status = this.determinePaymentStatus(data);
        
        this.pendingUpdates.add({
            type: 'purchase',
            data: data,
            timestamp: Date.now()
        });
        
        this.notifyPaymentSystem('purchase_created', data);
    }

    async handleExpenseSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        data.payment_status = 'unpaid'; // المصروفات عادة غير مدفوعة عند الإنشاء
        
        this.pendingUpdates.add({
            type: 'expense',
            data: data,
            timestamp: Date.now()
        });
        
        this.notifyPaymentSystem('expense_created', data);
    }

    async handlePayrollSubmit(event) {
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        data.payment_status = 'unpaid'; // الرواتب غير مدفوعة عند الإنشاء
        
        this.pendingUpdates.add({
            type: 'payroll',
            data: data,
            timestamp: Date.now()
        });
        
        this.notifyPaymentSystem('payroll_created', data);
    }

    determinePaymentStatus(data) {
        const total = parseFloat(data.total || 0);
        const paidAmount = parseFloat(data.paid_amount || 0);
        
        if (paidAmount >= total) {
            return 'paid';
        } else if (paidAmount > 0) {
            return 'partial';
        } else {
            return 'unpaid';
        }
    }

    async notifyPaymentSystem(eventType, data) {
        try {
            // إرسال إشعار لنظام المدفوعات
            await fetch('/api/payments/notify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    event_type: eventType,
                    data: data,
                    timestamp: new Date().toISOString()
                })
            });
            
            console.log(`📢 تم إشعار نظام المدفوعات: ${eventType}`);
            
        } catch (error) {
            console.error('خطأ في إشعار نظام المدفوعات:', error);
        }
    }

    async checkForUpdates() {
        try {
            const response = await fetch('/api/payments/check-updates', {
                method: 'GET',
                headers: {
                    'X-Last-Update': this.lastUpdate || '0'
                }
            });
            
            if (response.ok) {
                const result = await response.json();
                
                if (result.hasUpdates) {
                    await this.processUpdates(result.updates);
                    this.lastUpdate = result.timestamp;
                }
            }
            
        } catch (error) {
            console.error('خطأ في فحص التحديثات:', error);
        }
    }

    async processUpdates(updates) {
        for (const update of updates) {
            await this.applyUpdate(update);
        }
        
        // تحديث الواجهة
        this.refreshCurrentScreen();
    }

    async applyUpdate(update) {
        const { type, action, data } = update;
        
        switch (action) {
            case 'payment_registered':
                await this.updatePaymentStatus(type, data.id, data.payment_status);
                break;
                
            case 'payment_deleted':
                await this.updatePaymentStatus(type, data.id, 'unpaid');
                break;
                
            case 'amount_updated':
                await this.updateAmount(type, data.id, data.new_amount);
                break;
        }
    }

    async updatePaymentStatus(type, id, status) {
        // تحديث حالة الدفع في الواجهة
        const row = document.querySelector(`[data-${type}-id="${id}"]`);
        if (row) {
            const statusCell = row.querySelector('.payment-status');
            if (statusCell) {
                statusCell.className = `badge bg-${this.getStatusColor(status)}`;
                statusCell.textContent = this.getStatusText(status);
            }
        }
        
        // تحديث الإحصائيات
        this.updateSummaryCards();
    }

    getStatusColor(status) {
        const colors = {
            'paid': 'success',
            'partial': 'warning',
            'unpaid': 'danger',
            'overdue': 'dark'
        };
        return colors[status] || 'secondary';
    }

    getStatusText(status) {
        const texts = {
            'paid': 'مدفوع',
            'partial': 'جزئي',
            'unpaid': 'غير مدفوع',
            'overdue': 'متأخر'
        };
        return texts[status] || status;
    }

    refreshCurrentScreen() {
        const currentPath = window.location.pathname;
        
        // تحديث حسب الشاشة الحالية
        if (currentPath.includes('/sales')) {
            this.refreshSalesScreen();
        } else if (currentPath.includes('/purchases')) {
            this.refreshPurchasesScreen();
        } else if (currentPath.includes('/expenses')) {
            this.refreshExpensesScreen();
        } else if (currentPath.includes('/payroll')) {
            this.refreshPayrollScreen();
        } else if (currentPath.includes('/payments_dues')) {
            this.refreshPaymentsScreen();
        }
    }

    async refreshSalesScreen() {
        try {
            const response = await fetch('/api/sales/list');
            if (response.ok) {
                const data = await response.json();
                this.updateSalesTable(data.sales);
                this.updateSalesSummary(data.summary);
            }
        } catch (error) {
            console.error('خطأ في تحديث شاشة المبيعات:', error);
        }
    }

    async refreshPurchasesScreen() {
        try {
            const response = await fetch('/api/purchases/list');
            if (response.ok) {
                const data = await response.json();
                this.updatePurchasesTable(data.purchases);
                this.updatePurchasesSummary(data.summary);
            }
        } catch (error) {
            console.error('خطأ في تحديث شاشة المشتريات:', error);
        }
    }

    async refreshExpensesScreen() {
        try {
            const response = await fetch('/api/expenses/list');
            if (response.ok) {
                const data = await response.json();
                this.updateExpensesTable(data.expenses);
                this.updateExpensesSummary(data.summary);
            }
        } catch (error) {
            console.error('خطأ في تحديث شاشة المصروفات:', error);
        }
    }

    async refreshPayrollScreen() {
        try {
            const response = await fetch('/api/payroll/list');
            if (response.ok) {
                const data = await response.json();
                this.updatePayrollTable(data.payrolls);
                this.updatePayrollSummary(data.summary);
            }
        } catch (error) {
            console.error('خطأ في تحديث شاشة الرواتب:', error);
        }
    }

    async refreshPaymentsScreen() {
        try {
            const response = await fetch('/api/payments/summary');
            if (response.ok) {
                const data = await response.json();
                this.updatePaymentsSummary(data.summary);
                this.updatePaymentsTable(data.transactions);
            }
        } catch (error) {
            console.error('خطأ في تحديث شاشة المدفوعات:', error);
        }
    }

    updateSummaryCards() {
        // تحديث بطاقات الملخص في جميع الشاشات
        this.updateSalesCards();
        this.updatePurchasesCards();
        this.updateExpensesCards();
        this.updatePayrollCards();
    }

    updateSalesCards() {
        // تحديث بطاقات ملخص المبيعات
        const elements = {
            'total-sales': document.getElementById('total-sales'),
            'paid-sales': document.getElementById('paid-sales'),
            'pending-sales': document.getElementById('pending-sales')
        };

        // جلب البيانات المحدثة وتحديث العناصر
        this.fetchAndUpdateCards('/api/sales/summary', elements);
    }

    updatePurchasesCards() {
        const elements = {
            'total-purchases': document.getElementById('total-purchases'),
            'paid-purchases': document.getElementById('paid-purchases'),
            'pending-purchases': document.getElementById('pending-purchases')
        };

        this.fetchAndUpdateCards('/api/purchases/summary', elements);
    }

    updateExpensesCards() {
        const elements = {
            'total-expenses': document.getElementById('total-expenses'),
            'paid-expenses': document.getElementById('paid-expenses'),
            'pending-expenses': document.getElementById('pending-expenses')
        };

        this.fetchAndUpdateCards('/api/expenses/summary', elements);
    }

    updatePayrollCards() {
        const elements = {
            'total-payroll': document.getElementById('total-payroll'),
            'paid-payroll': document.getElementById('paid-payroll'),
            'pending-payroll': document.getElementById('pending-payroll')
        };

        this.fetchAndUpdateCards('/api/payroll/summary', elements);
    }

    async fetchAndUpdateCards(endpoint, elements) {
        try {
            const response = await fetch(endpoint);
            if (response.ok) {
                const data = await response.json();
                
                Object.keys(elements).forEach(key => {
                    const element = elements[key];
                    if (element && data[key] !== undefined) {
                        element.textContent = this.formatCurrency(data[key]);
                        
                        // إضافة تأثير بصري للتحديث
                        element.classList.add('updated');
                        setTimeout(() => {
                            element.classList.remove('updated');
                        }, 1000);
                    }
                });
            }
        } catch (error) {
            console.error(`خطأ في تحديث البطاقات من ${endpoint}:`, error);
        }
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('ar-SA', {
            style: 'currency',
            currency: 'SAR',
            minimumFractionDigits: 2
        }).format(amount);
    }

    // تحديث فوري عند تسجيل دفعة
    async onPaymentRegistered(paymentData) {
        const { invoice_type, invoice_id, amount, payment_status } = paymentData;
        
        // تحديث الفاتورة المحددة
        await this.updateInvoiceStatus(invoice_type, invoice_id, payment_status);
        
        // تحديث الإحصائيات
        this.updateSummaryCards();
        
        // إشعار المستخدم
        showSuccess(`تم تحديث حالة الدفع للفاتورة #${invoice_id}`);
        
        // تحديث شاشة المدفوعات إذا كانت مفتوحة
        if (window.location.pathname.includes('/payments_dues')) {
            this.refreshPaymentsScreen();
        }
    }

    async updateInvoiceStatus(type, id, status) {
        try {
            const response = await fetch(`/api/${type}/update-payment-status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: id,
                    payment_status: status
                })
            });
            
            if (response.ok) {
                console.log(`✅ تم تحديث حالة الدفع: ${type} #${id} -> ${status}`);
            }
            
        } catch (error) {
            console.error('خطأ في تحديث حالة الدفع:', error);
        }
    }

    // تحديث الجداول في الوقت الفعلي
    updateSalesTable(salesData) {
        const tbody = document.querySelector('#sales-table tbody');
        if (!tbody) return;

        // تحديث الصفوف الموجودة
        salesData.forEach(sale => {
            const row = tbody.querySelector(`[data-sale-id="${sale.id}"]`);
            if (row) {
                this.updateTableRow(row, sale);
            }
        });
    }

    updatePurchasesTable(purchasesData) {
        const tbody = document.querySelector('#purchases-table tbody');
        if (!tbody) return;

        purchasesData.forEach(purchase => {
            const row = tbody.querySelector(`[data-purchase-id="${purchase.id}"]`);
            if (row) {
                this.updateTableRow(row, purchase);
            }
        });
    }

    updateExpensesTable(expensesData) {
        const tbody = document.querySelector('#expenses-table tbody');
        if (!tbody) return;

        expensesData.forEach(expense => {
            const row = tbody.querySelector(`[data-expense-id="${expense.id}"]`);
            if (row) {
                this.updateTableRow(row, expense);
            }
        });
    }

    updateTableRow(row, data) {
        // تحديث حالة الدفع
        const statusCell = row.querySelector('.payment-status');
        if (statusCell) {
            statusCell.className = `badge bg-${this.getStatusColor(data.payment_status)}`;
            statusCell.textContent = this.getStatusText(data.payment_status);
        }

        // تحديث المبلغ المدفوع
        const paidCell = row.querySelector('.paid-amount');
        if (paidCell) {
            paidCell.textContent = this.formatCurrency(data.paid_amount || 0);
        }

        // تحديث المبلغ المتبقي
        const remainingCell = row.querySelector('.remaining-amount');
        if (remainingCell) {
            const remaining = (data.total_amount || 0) - (data.paid_amount || 0);
            remainingCell.textContent = this.formatCurrency(remaining);
        }

        // إضافة تأثير بصري للتحديث
        row.classList.add('table-updated');
        setTimeout(() => {
            row.classList.remove('table-updated');
        }, 2000);
    }

    // إضافة CSS للتأثيرات البصرية
    addUpdateStyles() {
        const styles = document.createElement('style');
        styles.textContent = `
            .updated {
                animation: pulse-green 1s ease-in-out;
            }

            .table-updated {
                background-color: #d4edda !important;
                transition: background-color 2s ease-out;
            }

            @keyframes pulse-green {
                0% { background-color: transparent; }
                50% { background-color: #d4edda; }
                100% { background-color: transparent; }
            }

            .payment-status-indicator {
                position: relative;
            }

            .payment-status-indicator::after {
                content: '';
                position: absolute;
                top: -2px;
                right: -2px;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #28a745;
                animation: blink 2s infinite;
            }

            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0; }
            }
        `;
        document.head.appendChild(styles);
    }
}

// إنشاء نسخة عامة
const paymentIntegration = new PaymentIntegrationSystem();

// دوال مساعدة
function registerPayment(invoiceType, invoiceId, amount, paymentMethod = 'CASH') {
    return paymentIntegration.onPaymentRegistered({
        invoice_type: invoiceType,
        invoice_id: invoiceId,
        amount: amount,
        payment_method: paymentMethod,
        payment_status: 'paid'
    });
}

function updatePaymentStatus(type, id, status) {
    return paymentIntegration.updateInvoiceStatus(type, id, status);
}

function refreshAllScreens() {
    return paymentIntegration.refreshCurrentScreen();
}

// تصدير
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PaymentIntegrationSystem,
        paymentIntegration,
        registerPayment,
        updatePaymentStatus,
        refreshAllScreens
    };
}
