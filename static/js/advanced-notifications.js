/**
 * نظام الإشعارات المتقدم للنظام المحاسبي
 * Advanced Notification System for Accounting System
 */

class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.maxNotifications = 5;
        this.defaultDuration = 4000;
        this.container = null;
        this.init();
    }

    init() {
        // إنشاء حاوية الإشعارات
        this.createContainer();
        
        // إضافة الأنماط
        this.addStyles();
    }

    createContainer() {
        if (document.getElementById('notification-container')) return;
        
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = 'notification-container';
        document.body.appendChild(this.container);
    }

    addStyles() {
        if (document.getElementById('notification-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                max-width: 400px;
                pointer-events: none;
            }

            .notification {
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                margin-bottom: 10px;
                padding: 16px;
                border-left: 4px solid;
                transform: translateX(100%);
                transition: all 0.3s ease;
                pointer-events: auto;
                position: relative;
                overflow: hidden;
            }

            .notification.show {
                transform: translateX(0);
            }

            .notification.success {
                border-left-color: #28a745;
                background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            }

            .notification.error {
                border-left-color: #dc3545;
                background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            }

            .notification.warning {
                border-left-color: #ffc107;
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            }

            .notification.info {
                border-left-color: #17a2b8;
                background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            }

            .notification-header {
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                font-weight: 600;
            }

            .notification-icon {
                margin-left: 8px;
                font-size: 18px;
            }

            .notification-title {
                flex: 1;
                font-size: 14px;
            }

            .notification-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                opacity: 0.7;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .notification-close:hover {
                opacity: 1;
            }

            .notification-message {
                font-size: 13px;
                line-height: 1.4;
                color: #333;
            }

            .notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: rgba(0,0,0,0.2);
                transition: width linear;
            }

            .notification.success .notification-progress {
                background: #28a745;
            }

            .notification.error .notification-progress {
                background: #dc3545;
            }

            .notification.warning .notification-progress {
                background: #ffc107;
            }

            .notification.info .notification-progress {
                background: #17a2b8;
            }

            @media (max-width: 768px) {
                .notification-container {
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    show(message, type = 'info', options = {}) {
        const notification = this.createNotification(message, type, options);
        this.addNotification(notification);
        return notification;
    }

    createNotification(message, type, options) {
        const {
            title = this.getDefaultTitle(type),
            duration = this.defaultDuration,
            persistent = false,
            actions = []
        } = options;

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        const id = 'notif_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        notification.id = id;

        notification.innerHTML = `
            <div class="notification-header">
                <i class="notification-icon ${this.getIcon(type)}"></i>
                <span class="notification-title">${title}</span>
                <button class="notification-close" onclick="notificationSystem.remove('${id}')">&times;</button>
            </div>
            <div class="notification-message">${message}</div>
            ${!persistent ? '<div class="notification-progress"></div>' : ''}
        `;

        // إضافة الأكشن buttons إذا وجدت
        if (actions.length > 0) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'notification-actions mt-2';
            actions.forEach(action => {
                const btn = document.createElement('button');
                btn.className = `btn btn-sm btn-outline-${type} me-2`;
                btn.textContent = action.text;
                btn.onclick = action.callback;
                actionsDiv.appendChild(btn);
            });
            notification.appendChild(actionsDiv);
        }

        // إعداد التوقيت التلقائي
        if (!persistent && duration > 0) {
            const progressBar = notification.querySelector('.notification-progress');
            if (progressBar) {
                progressBar.style.width = '100%';
                setTimeout(() => {
                    progressBar.style.width = '0%';
                }, 100);
            }

            setTimeout(() => {
                this.remove(id);
            }, duration);
        }

        return notification;
    }

    addNotification(notification) {
        // إزالة الإشعارات الزائدة
        while (this.notifications.length >= this.maxNotifications) {
            this.remove(this.notifications[0].id);
        }

        this.container.appendChild(notification);
        this.notifications.push(notification);

        // تفعيل الأنيميشن
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
    }

    remove(id) {
        const notification = document.getElementById(id);
        if (!notification) return;

        notification.classList.remove('show');
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            this.notifications = this.notifications.filter(n => n.id !== id);
        }, 300);
    }

    clear() {
        this.notifications.forEach(notification => {
            this.remove(notification.id);
        });
    }

    getDefaultTitle(type) {
        const titles = {
            success: 'نجح العملية',
            error: 'خطأ',
            warning: 'تحذير',
            info: 'معلومات'
        };
        return titles[type] || 'إشعار';
    }

    getIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || 'fas fa-bell';
    }

    // طرق مختصرة
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }

    error(message, options = {}) {
        return this.show(message, 'error', options);
    }

    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }

    info(message, options = {}) {
        return this.show(message, 'info', options);
    }

    // إشعار مع إجراءات
    confirm(message, onConfirm, onCancel = null) {
        const actions = [
            {
                text: 'تأكيد',
                callback: () => {
                    onConfirm();
                    this.remove(notification.id);
                }
            }
        ];

        if (onCancel) {
            actions.push({
                text: 'إلغاء',
                callback: () => {
                    onCancel();
                    this.remove(notification.id);
                }
            });
        }

        const notification = this.show(message, 'warning', {
            title: 'تأكيد العملية',
            persistent: true,
            actions: actions
        });

        return notification;
    }
}

// إنشاء نسخة عامة
const notificationSystem = new NotificationSystem();

// دوال مختصرة للاستخدام السهل
function showNotification(message, type = 'info', options = {}) {
    return notificationSystem.show(message, type, options);
}

function showSuccess(message, options = {}) {
    return notificationSystem.success(message, options);
}

function showError(message, options = {}) {
    return notificationSystem.error(message, options);
}

function showWarning(message, options = {}) {
    return notificationSystem.warning(message, options);
}

function showInfo(message, options = {}) {
    return notificationSystem.info(message, options);
}

function showConfirm(message, onConfirm, onCancel = null) {
    return notificationSystem.confirm(message, onConfirm, onCancel);
}

// تصدير للاستخدام في modules أخرى
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        NotificationSystem,
        notificationSystem,
        showNotification,
        showSuccess,
        showError,
        showWarning,
        showInfo,
        showConfirm
    };
}
