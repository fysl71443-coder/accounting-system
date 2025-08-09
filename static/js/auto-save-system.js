/**
 * نظام الحفظ التلقائي المتقدم
 * Advanced Auto-Save System
 */

class AutoSaveSystem {
    constructor(options = {}) {
        this.options = {
            interval: 30000, // 30 ثانية
            debounceDelay: 2000, // 2 ثانية
            maxRetries: 3,
            retryDelay: 1000,
            enableFormRecovery: true,
            enableOfflineMode: true,
            ...options
        };
        
        this.forms = new Map();
        this.timers = new Map();
        this.retryCounters = new Map();
        this.isOnline = navigator.onLine;
        this.pendingOperations = [];
        
        this.init();
    }

    init() {
        // مراقبة حالة الاتصال
        this.setupOnlineDetection();
        
        // إعداد الحفظ التلقائي للنماذج
        this.setupFormAutoSave();
        
        // استعادة البيانات المحفوظة محلياً
        this.recoverSavedData();
        
        console.log('🚀 نظام الحفظ التلقائي جاهز');
    }

    setupOnlineDetection() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            showSuccess('تم استعادة الاتصال - سيتم حفظ البيانات المعلقة');
            this.processPendingOperations();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            showWarning('انقطع الاتصال - سيتم حفظ البيانات محلياً');
        });
    }

    setupFormAutoSave() {
        // البحث عن جميع النماذج
        document.addEventListener('DOMContentLoaded', () => {
            this.scanForForms();
        });

        // مراقبة النماذج الجديدة
        const observer = new MutationObserver(() => {
            this.scanForForms();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    scanForForms() {
        const forms = document.querySelectorAll('form[data-auto-save]');
        
        forms.forEach(form => {
            if (!this.forms.has(form.id)) {
                this.registerForm(form);
            }
        });
    }

    registerForm(form) {
        if (!form.id) {
            form.id = 'form_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }

        const formConfig = {
            element: form,
            endpoint: form.dataset.autoSave,
            method: form.dataset.method || 'POST',
            lastSaved: null,
            isDirty: false
        };

        this.forms.set(form.id, formConfig);

        // مراقبة التغييرات
        this.setupFormListeners(form);

        console.log(`📝 تم تسجيل النموذج للحفظ التلقائي: ${form.id}`);
    }

    setupFormListeners(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            ['input', 'change', 'blur'].forEach(event => {
                input.addEventListener(event, () => {
                    this.markFormDirty(form.id);
                });
            });
        });
    }

    markFormDirty(formId) {
        const formConfig = this.forms.get(formId);
        if (!formConfig) return;

        formConfig.isDirty = true;
        
        // إلغاء المؤقت السابق
        if (this.timers.has(formId)) {
            clearTimeout(this.timers.get(formId));
        }

        // إعداد مؤقت جديد
        const timer = setTimeout(() => {
            this.autoSaveForm(formId);
        }, this.options.debounceDelay);

        this.timers.set(formId, timer);
    }

    async autoSaveForm(formId) {
        const formConfig = this.forms.get(formId);
        if (!formConfig || !formConfig.isDirty) return;

        const formData = this.getFormData(formConfig.element);
        
        // حفظ محلي أولاً
        this.saveLocally(formId, formData);

        if (this.isOnline) {
            try {
                await this.saveToServer(formConfig, formData);
                formConfig.isDirty = false;
                formConfig.lastSaved = new Date();
                
                // إزالة النسخة المحلية بعد الحفظ الناجح
                this.removeLocalSave(formId);
                
            } catch (error) {
                console.error('خطأ في الحفظ التلقائي:', error);
                this.handleSaveError(formId, formData, error);
            }
        } else {
            this.addToPendingOperations(formConfig, formData);
        }
    }

    async saveToServer(formConfig, formData) {
        const response = await fetch(formConfig.endpoint, {
            method: formConfig.method,
            headers: {
                'Content-Type': 'application/json',
                'X-Auto-Save': 'true'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || 'فشل في الحفظ');
        }

        // إشعار نجاح خفيف
        this.showSaveSuccess(formConfig.element);
        
        return result;
    }

    showSaveSuccess(form) {
        // إضافة مؤشر بصري خفيف
        const indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator';
        indicator.innerHTML = '<i class="fas fa-check text-success"></i> محفوظ';
        indicator.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 5px 10px;
            border-radius: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            font-size: 12px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        form.style.position = 'relative';
        form.appendChild(indicator);

        // إظهار المؤشر
        setTimeout(() => {
            indicator.style.opacity = '1';
        }, 100);

        // إخفاء المؤشر
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
            }, 300);
        }, 2000);
    }

    getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // إضافة معلومات إضافية
        data._autoSave = true;
        data._timestamp = new Date().toISOString();
        data._formId = form.id;
        
        return data;
    }

    saveLocally(formId, data) {
        if (!this.options.enableFormRecovery) return;
        
        try {
            const key = `autosave_${formId}`;
            localStorage.setItem(key, JSON.stringify({
                data: data,
                timestamp: new Date().toISOString(),
                formId: formId
            }));
        } catch (error) {
            console.warn('فشل في الحفظ المحلي:', error);
        }
    }

    removeLocalSave(formId) {
        try {
            const key = `autosave_${formId}`;
            localStorage.removeItem(key);
        } catch (error) {
            console.warn('فشل في حذف الحفظ المحلي:', error);
        }
    }

    recoverSavedData() {
        if (!this.options.enableFormRecovery) return;
        
        try {
            const keys = Object.keys(localStorage).filter(key => key.startsWith('autosave_'));
            
            keys.forEach(key => {
                const saved = JSON.parse(localStorage.getItem(key));
                const formId = saved.formId;
                const form = document.getElementById(formId);
                
                if (form && saved.data) {
                    this.showRecoveryOption(form, saved);
                }
            });
        } catch (error) {
            console.warn('فشل في استعادة البيانات:', error);
        }
    }

    showRecoveryOption(form, savedData) {
        const timeDiff = new Date() - new Date(savedData.timestamp);
        const minutes = Math.floor(timeDiff / 60000);
        
        if (minutes > 60) {
            // حذف البيانات القديمة
            this.removeLocalSave(savedData.formId);
            return;
        }

        showConfirm(
            `تم العثور على بيانات محفوظة من ${minutes} دقيقة. هل تريد استعادتها؟`,
            () => {
                this.restoreFormData(form, savedData.data);
                this.removeLocalSave(savedData.formId);
                showSuccess('تم استعادة البيانات المحفوظة');
            },
            () => {
                this.removeLocalSave(savedData.formId);
            }
        );
    }

    restoreFormData(form, data) {
        Object.keys(data).forEach(key => {
            if (key.startsWith('_')) return; // تجاهل البيانات الداخلية
            
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
                
                // تفعيل الأحداث
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }

    addToPendingOperations(formConfig, formData) {
        this.pendingOperations.push({
            formConfig: formConfig,
            data: formData,
            timestamp: new Date().toISOString()
        });

        showInfo(`تم حفظ البيانات محلياً - سيتم الحفظ على الخادم عند استعادة الاتصال`);
    }

    async processPendingOperations() {
        if (this.pendingOperations.length === 0) return;

        showInfo(`جاري حفظ ${this.pendingOperations.length} عملية معلقة...`);

        for (const operation of this.pendingOperations) {
            try {
                await this.saveToServer(operation.formConfig, operation.data);
            } catch (error) {
                console.error('فشل في حفظ العملية المعلقة:', error);
            }
        }

        this.pendingOperations = [];
        showSuccess('تم حفظ جميع العمليات المعلقة');
    }

    handleSaveError(formId, formData, error) {
        const retryCount = this.retryCounters.get(formId) || 0;
        
        if (retryCount < this.options.maxRetries) {
            this.retryCounters.set(formId, retryCount + 1);
            
            setTimeout(() => {
                this.autoSaveForm(formId);
            }, this.options.retryDelay * (retryCount + 1));
            
            showWarning(`محاولة إعادة الحفظ ${retryCount + 1}/${this.options.maxRetries}`);
        } else {
            this.retryCounters.delete(formId);
            showError('فشل في الحفظ - تم حفظ البيانات محلياً');
        }
    }

    // طرق للتحكم اليدوي
    saveForm(formId) {
        return this.autoSaveForm(formId);
    }

    saveAllForms() {
        const promises = [];
        this.forms.forEach((config, formId) => {
            if (config.isDirty) {
                promises.push(this.autoSaveForm(formId));
            }
        });
        return Promise.all(promises);
    }

    enableAutoSave(formId) {
        const formConfig = this.forms.get(formId);
        if (formConfig) {
            formConfig.enabled = true;
        }
    }

    disableAutoSave(formId) {
        const formConfig = this.forms.get(formId);
        if (formConfig) {
            formConfig.enabled = false;
        }
        
        // إلغاء المؤقت
        if (this.timers.has(formId)) {
            clearTimeout(this.timers.get(formId));
            this.timers.delete(formId);
        }
    }
}

// إنشاء نسخة عامة
const autoSaveSystem = new AutoSaveSystem();

// دوال مساعدة
function enableAutoSave(formSelector, endpoint, options = {}) {
    const form = document.querySelector(formSelector);
    if (!form) return false;
    
    form.dataset.autoSave = endpoint;
    form.dataset.method = options.method || 'POST';
    
    autoSaveSystem.registerForm(form);
    return true;
}

function saveFormNow(formId) {
    return autoSaveSystem.saveForm(formId);
}

function saveAllFormsNow() {
    return autoSaveSystem.saveAllForms();
}

// حفظ عند مغادرة الصفحة
window.addEventListener('beforeunload', (event) => {
    const hasDirtyForms = Array.from(autoSaveSystem.forms.values()).some(config => config.isDirty);
    
    if (hasDirtyForms) {
        // محاولة حفظ سريع
        autoSaveSystem.saveAllForms();
        
        // تحذير المستخدم
        event.preventDefault();
        event.returnValue = 'يوجد بيانات غير محفوظة. هل تريد المغادرة؟';
        return event.returnValue;
    }
});

/**
 * نظام إدارة البيانات المتقدم
 * Advanced Data Management System
 */
class DataManager {
    constructor() {
        this.cache = new Map();
        this.operations = [];
        this.maxOperations = 50;
    }

    // حفظ بيانات مع تتبع العمليات
    async save(endpoint, data, options = {}) {
        const operation = {
            id: this.generateOperationId(),
            type: 'save',
            endpoint: endpoint,
            data: data,
            timestamp: new Date().toISOString(),
            status: 'pending'
        };

        this.addOperation(operation);

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Operation-ID': operation.id
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                operation.status = 'success';
                operation.result = result;

                showSuccess(options.successMessage || 'تم الحفظ بنجاح');

                // تحديث الكاش
                if (result.id) {
                    this.cache.set(`${endpoint}_${result.id}`, result);
                }

                return result;
            } else {
                throw new Error(result.message || 'فشل في الحفظ');
            }
        } catch (error) {
            operation.status = 'failed';
            operation.error = error.message;

            showError(options.errorMessage || `خطأ في الحفظ: ${error.message}`);
            throw error;
        }
    }

    // حذف بيانات
    async delete(endpoint, id, options = {}) {
        const operation = {
            id: this.generateOperationId(),
            type: 'delete',
            endpoint: endpoint,
            targetId: id,
            timestamp: new Date().toISOString(),
            status: 'pending'
        };

        this.addOperation(operation);

        try {
            const response = await fetch(`${endpoint}/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Operation-ID': operation.id
                }
            });

            const result = await response.json();

            if (result.success) {
                operation.status = 'success';
                operation.result = result;

                showSuccess(options.successMessage || 'تم الحذف بنجاح');

                // إزالة من الكاش
                this.cache.delete(`${endpoint}_${id}`);

                return result;
            } else {
                throw new Error(result.message || 'فشل في الحذف');
            }
        } catch (error) {
            operation.status = 'failed';
            operation.error = error.message;

            showError(options.errorMessage || `خطأ في الحذف: ${error.message}`);
            throw error;
        }
    }

    // تحديث بيانات
    async update(endpoint, id, data, options = {}) {
        const operation = {
            id: this.generateOperationId(),
            type: 'update',
            endpoint: endpoint,
            targetId: id,
            data: data,
            timestamp: new Date().toISOString(),
            status: 'pending'
        };

        this.addOperation(operation);

        try {
            const response = await fetch(`${endpoint}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Operation-ID': operation.id
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                operation.status = 'success';
                operation.result = result;

                showSuccess(options.successMessage || 'تم التحديث بنجاح');

                // تحديث الكاش
                this.cache.set(`${endpoint}_${id}`, result);

                return result;
            } else {
                throw new Error(result.message || 'فشل في التحديث');
            }
        } catch (error) {
            operation.status = 'failed';
            operation.error = error.message;

            showError(options.errorMessage || `خطأ في التحديث: ${error.message}`);
            throw error;
        }
    }

    addOperation(operation) {
        this.operations.unshift(operation);

        // الحفاظ على حد أقصى من العمليات
        if (this.operations.length > this.maxOperations) {
            this.operations = this.operations.slice(0, this.maxOperations);
        }
    }

    generateOperationId() {
        return 'op_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // الحصول على تاريخ العمليات
    getOperationHistory() {
        return this.operations;
    }

    // التراجع عن آخر عملية
    async undoLastOperation() {
        const lastOperation = this.operations.find(op => op.status === 'success' && op.type !== 'delete');

        if (!lastOperation) {
            showWarning('لا توجد عمليات للتراجع عنها');
            return false;
        }

        // تنفيذ التراجع حسب نوع العملية
        try {
            if (lastOperation.type === 'save') {
                await this.delete(lastOperation.endpoint, lastOperation.result.id);
                showSuccess('تم التراجع عن العملية');
                return true;
            }
        } catch (error) {
            showError(`فشل في التراجع: ${error.message}`);
            return false;
        }
    }
}

// إنشاء نسخة عامة
const dataManager = new DataManager();

// دوال مساعدة عامة
async function saveData(endpoint, data, options = {}) {
    return dataManager.save(endpoint, data, options);
}

async function deleteData(endpoint, id, options = {}) {
    return dataManager.delete(endpoint, id, options);
}

async function updateData(endpoint, id, data, options = {}) {
    return dataManager.update(endpoint, id, data, options);
}

function undoLastOperation() {
    return dataManager.undoLastOperation();
}

// تصدير للاستخدام في modules أخرى
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AutoSaveSystem,
        autoSaveSystem,
        enableAutoSave,
        saveFormNow,
        saveAllFormsNow,
        DataManager,
        dataManager,
        saveData,
        deleteData,
        updateData,
        undoLastOperation
    };
}
