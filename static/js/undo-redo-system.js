/**
 * نظام التراجع والإعادة
 * Undo/Redo System
 */

class UndoRedoSystem {
    constructor() {
        this.history = [];
        this.currentIndex = -1;
        this.maxHistorySize = 50;
        this.isEnabled = true;
        
        this.setupKeyboardShortcuts();
        this.createUndoRedoUI();
    }

    // إضافة عملية للتاريخ
    addOperation(operation) {
        if (!this.isEnabled) return;

        // إزالة العمليات بعد المؤشر الحالي (في حالة التراجع ثم عملية جديدة)
        this.history = this.history.slice(0, this.currentIndex + 1);
        
        // إضافة العملية الجديدة
        this.history.push({
            ...operation,
            id: this.generateId(),
            timestamp: new Date().toISOString()
        });
        
        this.currentIndex = this.history.length - 1;
        
        // الحفاظ على حد أقصى للتاريخ
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
            this.currentIndex--;
        }
        
        this.updateUI();
    }

    // التراجع
    async undo() {
        if (!this.canUndo()) {
            showWarning('لا توجد عمليات للتراجع عنها');
            return false;
        }

        const operation = this.history[this.currentIndex];
        
        try {
            await this.executeUndo(operation);
            this.currentIndex--;
            this.updateUI();
            
            showSuccess(`تم التراجع عن: ${operation.description}`);
            return true;
        } catch (error) {
            showError(`فشل التراجع: ${error.message}`);
            return false;
        }
    }

    // الإعادة
    async redo() {
        if (!this.canRedo()) {
            showWarning('لا توجد عمليات للإعادة');
            return false;
        }

        this.currentIndex++;
        const operation = this.history[this.currentIndex];
        
        try {
            await this.executeRedo(operation);
            this.updateUI();
            
            showSuccess(`تم إعادة: ${operation.description}`);
            return true;
        } catch (error) {
            this.currentIndex--;
            showError(`فشل الإعادة: ${error.message}`);
            return false;
        }
    }

    async executeUndo(operation) {
        switch (operation.type) {
            case 'create':
                // حذف العنصر المُنشأ
                await this.deleteItem(operation.endpoint, operation.result.id);
                break;
                
            case 'update':
                // استعادة القيم السابقة
                await this.restoreItem(operation.endpoint, operation.targetId, operation.previousData);
                break;
                
            case 'delete':
                // إعادة إنشاء العنصر المحذوف
                await this.recreateItem(operation.endpoint, operation.deletedData);
                break;
                
            default:
                throw new Error(`نوع عملية غير مدعوم للتراجع: ${operation.type}`);
        }
    }

    async executeRedo(operation) {
        switch (operation.type) {
            case 'create':
                // إعادة إنشاء العنصر
                await this.recreateItem(operation.endpoint, operation.data);
                break;
                
            case 'update':
                // إعادة تطبيق التحديث
                await this.updateItem(operation.endpoint, operation.targetId, operation.data);
                break;
                
            case 'delete':
                // إعادة حذف العنصر
                await this.deleteItem(operation.endpoint, operation.targetId);
                break;
                
            default:
                throw new Error(`نوع عملية غير مدعوم للإعادة: ${operation.type}`);
        }
    }

    async deleteItem(endpoint, id) {
        const response = await fetch(`${endpoint}/delete/${id}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error(`فشل في الحذف: ${response.status}`);
        }
        
        return response.json();
    }

    async updateItem(endpoint, id, data) {
        const response = await fetch(`${endpoint}/update/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`فشل في التحديث: ${response.status}`);
        }
        
        return response.json();
    }

    async recreateItem(endpoint, data) {
        const response = await fetch(`${endpoint}/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`فشل في الإنشاء: ${response.status}`);
        }
        
        return response.json();
    }

    async restoreItem(endpoint, id, data) {
        return this.updateItem(endpoint, id, data);
    }

    canUndo() {
        return this.currentIndex >= 0;
    }

    canRedo() {
        return this.currentIndex < this.history.length - 1;
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey) {
                if (event.key === 'z' && !event.shiftKey) {
                    event.preventDefault();
                    this.undo();
                } else if ((event.key === 'y') || (event.key === 'z' && event.shiftKey)) {
                    event.preventDefault();
                    this.redo();
                }
            }
        });
    }

    createUndoRedoUI() {
        // إنشاء أزرار التراجع والإعادة
        const toolbar = document.createElement('div');
        toolbar.id = 'undo-redo-toolbar';
        toolbar.className = 'undo-redo-toolbar';
        toolbar.innerHTML = `
            <button id="undo-btn" class="btn btn-outline-secondary btn-sm" title="تراجع (Ctrl+Z)" disabled>
                <i class="fas fa-undo"></i>
            </button>
            <button id="redo-btn" class="btn btn-outline-secondary btn-sm" title="إعادة (Ctrl+Y)" disabled>
                <i class="fas fa-redo"></i>
            </button>
            <span class="ms-2 small text-muted" id="history-status">0 عمليات</span>
        `;

        // إضافة الأنماط
        const styles = document.createElement('style');
        styles.textContent = `
            .undo-redo-toolbar {
                position: fixed;
                bottom: 20px;
                left: 20px;
                background: white;
                padding: 8px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 1000;
                display: none; /* مخفي بشكل افتراضي */
                align-items: center;
                gap: 5px;
            }

            .undo-redo-toolbar button {
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            @media (max-width: 768px) {
                .undo-redo-toolbar {
                    bottom: 10px;
                    left: 10px;
                }
            }
        `;
        document.head.appendChild(styles);

        // إضافة للصفحة
        document.body.appendChild(toolbar);

        // ربط الأحداث
        document.getElementById('undo-btn').onclick = () => this.undo();
        document.getElementById('redo-btn').onclick = () => this.redo();
    }

    updateUI() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');
        const statusSpan = document.getElementById('history-status');

        if (undoBtn) {
            undoBtn.disabled = !this.canUndo();
        }

        if (redoBtn) {
            redoBtn.disabled = !this.canRedo();
        }

        if (statusSpan) {
            statusSpan.textContent = `${this.history.length} عمليات`;
        }
    }

    // الحصول على تاريخ العمليات
    getHistory() {
        return this.history;
    }

    // مسح التاريخ
    clearHistory() {
        this.history = [];
        this.currentIndex = -1;
        this.updateUI();
        showInfo('تم مسح تاريخ العمليات');
    }

    // تفعيل/تعطيل النظام
    enable() {
        this.isEnabled = true;
        document.getElementById('undo-redo-toolbar').style.display = 'flex';
    }

    disable() {
        this.isEnabled = false;
        document.getElementById('undo-redo-toolbar').style.display = 'none';
    }

    generateId() {
        return 'undo_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
}

// إنشاء نسخة عامة
const undoRedoSystem = new UndoRedoSystem();

// دوال مساعدة
function recordOperation(type, endpoint, data, options = {}) {
    undoRedoSystem.addOperation({
        type: type,
        endpoint: endpoint,
        data: data,
        description: options.description || `${type} operation`,
        ...options
    });
}

function undoLastOperation() {
    return undoRedoSystem.undo();
}

function redoLastOperation() {
    return undoRedoSystem.redo();
}

function clearOperationHistory() {
    return undoRedoSystem.clearHistory();
}

function getOperationHistory() {
    return undoRedoSystem.getHistory();
}

// تصدير
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        UndoRedoSystem,
        undoRedoSystem,
        recordOperation,
        undoLastOperation,
        redoLastOperation,
        clearOperationHistory,
        getOperationHistory
    };
}
