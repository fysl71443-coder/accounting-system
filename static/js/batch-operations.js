/**
 * نظام العمليات المجمعة
 * Batch Operations System
 */

class BatchOperationSystem {
    constructor() {
        this.queue = [];
        this.isProcessing = false;
        this.maxBatchSize = 10;
        this.batchDelay = 1000; // 1 ثانية
    }

    // إضافة عملية للطابور
    addOperation(operation) {
        this.queue.push({
            ...operation,
            id: this.generateId(),
            timestamp: new Date().toISOString(),
            status: 'queued'
        });

        this.processQueue();
    }

    // معالجة الطابور
    async processQueue() {
        if (this.isProcessing || this.queue.length === 0) return;

        this.isProcessing = true;
        
        try {
            // تجميع العمليات حسب النوع والـ endpoint
            const batches = this.groupOperations();
            
            for (const batch of batches) {
                await this.processBatch(batch);
                await this.delay(this.batchDelay);
            }
        } catch (error) {
            console.error('خطأ في معالجة الطابور:', error);
        } finally {
            this.isProcessing = false;
        }
    }

    groupOperations() {
        const groups = new Map();
        const queuedOps = this.queue.filter(op => op.status === 'queued');
        
        queuedOps.forEach(operation => {
            const key = `${operation.type}_${operation.endpoint}`;
            
            if (!groups.has(key)) {
                groups.set(key, []);
            }
            
            groups.get(key).push(operation);
        });

        // تحويل إلى مصفوفة من المجموعات
        return Array.from(groups.values()).map(group => 
            group.slice(0, this.maxBatchSize)
        );
    }

    async processBatch(batch) {
        if (batch.length === 0) return;

        const operation = batch[0];
        
        try {
            if (batch.length === 1) {
                // عملية واحدة
                await this.processSingleOperation(operation);
            } else {
                // عمليات متعددة
                await this.processMultipleOperations(batch);
            }
        } catch (error) {
            console.error('خطأ في معالجة المجموعة:', error);
            batch.forEach(op => {
                op.status = 'failed';
                op.error = error.message;
            });
        }
    }

    async processSingleOperation(operation) {
        operation.status = 'processing';
        
        try {
            let response;
            
            switch (operation.type) {
                case 'save':
                    response = await fetch(operation.endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(operation.data)
                    });
                    break;
                    
                case 'update':
                    response = await fetch(`${operation.endpoint}/${operation.targetId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(operation.data)
                    });
                    break;
                    
                case 'delete':
                    response = await fetch(`${operation.endpoint}/${operation.targetId}`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    break;
                    
                default:
                    throw new Error(`نوع عملية غير مدعوم: ${operation.type}`);
            }

            const result = await response.json();
            
            if (result.success) {
                operation.status = 'completed';
                operation.result = result;
                
                // إزالة من الطابور
                this.removeFromQueue(operation.id);
                
                // إشعار النجاح
                this.showOperationSuccess(operation);
            } else {
                throw new Error(result.message || 'فشل في العملية');
            }
        } catch (error) {
            operation.status = 'failed';
            operation.error = error.message;
            
            this.showOperationError(operation, error);
        }
    }

    async processMultipleOperations(operations) {
        // إعداد البيانات للحفظ المجمع
        const batchData = {
            operations: operations.map(op => ({
                type: op.type,
                data: op.data,
                targetId: op.targetId
            }))
        };

        try {
            const response = await fetch('/api/batch/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(batchData)
            });

            const result = await response.json();
            
            if (result.success) {
                operations.forEach((op, index) => {
                    op.status = 'completed';
                    op.result = result.results[index];
                    this.removeFromQueue(op.id);
                });
                
                showSuccess(`تم حفظ ${operations.length} عنصر بنجاح`);
            } else {
                throw new Error(result.message || 'فشل في العملية المجمعة');
            }
        } catch (error) {
            // في حالة فشل العملية المجمعة، نعالج كل عملية منفردة
            for (const operation of operations) {
                await this.processSingleOperation(operation);
            }
        }
    }

    showOperationSuccess(operation) {
        const messages = {
            save: 'تم الحفظ',
            update: 'تم التحديث', 
            delete: 'تم الحذف'
        };
        
        const message = messages[operation.type] || 'تمت العملية';
        showSuccess(message);
    }

    showOperationError(operation, error) {
        const messages = {
            save: 'فشل الحفظ',
            update: 'فشل التحديث',
            delete: 'فشل الحذف'
        };
        
        const message = messages[operation.type] || 'فشلت العملية';
        showError(`${message}: ${error.message}`);
    }

    removeFromQueue(operationId) {
        this.queue = this.queue.filter(op => op.id !== operationId);
    }

    generateId() {
        return 'batch_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // الحصول على حالة الطابور
    getQueueStatus() {
        return {
            total: this.queue.length,
            pending: this.queue.filter(op => op.status === 'queued').length,
            processing: this.queue.filter(op => op.status === 'processing').length,
            completed: this.queue.filter(op => op.status === 'completed').length,
            failed: this.queue.filter(op => op.status === 'failed').length
        };
    }

    // مسح الطابور
    clearQueue() {
        this.queue = [];
        showInfo('تم مسح طابور العمليات');
    }

    // إعادة محاولة العمليات الفاشلة
    async retryFailedOperations() {
        const failedOps = this.queue.filter(op => op.status === 'failed');
        
        if (failedOps.length === 0) {
            showInfo('لا توجد عمليات فاشلة لإعادة المحاولة');
            return;
        }

        showInfo(`جاري إعادة محاولة ${failedOps.length} عملية...`);
        
        for (const operation of failedOps) {
            operation.status = 'queued';
            delete operation.error;
        }

        await this.processQueue();
    }
}

// إنشاء نسخة عامة
const batchSystem = new BatchOperationSystem();

// دوال مساعدة للحفظ المجمع
function batchSave(endpoint, data, options = {}) {
    batchSystem.addOperation({
        type: 'save',
        endpoint: endpoint,
        data: data,
        ...options
    });
}

function batchUpdate(endpoint, id, data, options = {}) {
    batchSystem.addOperation({
        type: 'update',
        endpoint: endpoint,
        targetId: id,
        data: data,
        ...options
    });
}

function batchDelete(endpoint, id, options = {}) {
    batchSystem.addOperation({
        type: 'delete',
        endpoint: endpoint,
        targetId: id,
        ...options
    });
}

function getBatchStatus() {
    return batchSystem.getQueueStatus();
}

function clearBatchQueue() {
    return batchSystem.clearQueue();
}

function retryFailedBatch() {
    return batchSystem.retryFailedOperations();
}

// تصدير
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        BatchOperationSystem,
        batchSystem,
        batchSave,
        batchUpdate,
        batchDelete,
        getBatchStatus,
        clearBatchQueue,
        retryFailedBatch
    };
}
