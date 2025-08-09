/**
 * نظام مراقبة الأداء والإحصائيات
 * Performance Monitoring and Statistics System
 */

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            saveOperations: 0,
            saveTime: [],
            errors: 0,
            networkRequests: 0,
            cacheHits: 0,
            cacheMisses: 0
        };
        
        this.startTime = Date.now();
        this.isMonitoring = true;
        
        this.setupMonitoring();
        this.createPerformanceUI();
    }

    setupMonitoring() {
        // مراقبة طلبات الشبكة
        this.interceptFetch();
        
        // مراقبة أداء الصفحة
        this.monitorPagePerformance();
        
        // مراقبة استخدام الذاكرة
        this.monitorMemoryUsage();
    }

    interceptFetch() {
        const originalFetch = window.fetch;
        const self = this;
        
        window.fetch = async function(...args) {
            const startTime = performance.now();
            self.metrics.networkRequests++;
            
            try {
                const response = await originalFetch.apply(this, args);
                const endTime = performance.now();
                const duration = endTime - startTime;
                
                // تسجيل إحصائيات الحفظ
                if (args[0].includes('/api/') && args[1]?.method === 'POST') {
                    self.metrics.saveOperations++;
                    self.metrics.saveTime.push(duration);
                    
                    // الحفاظ على آخر 100 عملية فقط
                    if (self.metrics.saveTime.length > 100) {
                        self.metrics.saveTime.shift();
                    }
                }
                
                // تسجيل الأخطاء
                if (!response.ok) {
                    self.metrics.errors++;
                }
                
                self.updatePerformanceUI();
                return response;
                
            } catch (error) {
                self.metrics.errors++;
                self.updatePerformanceUI();
                throw error;
            }
        };
    }

    monitorPagePerformance() {
        // مراقبة أداء تحميل الصفحة
        window.addEventListener('load', () => {
            if (performance.navigation) {
                const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
                console.log(`⏱️ وقت تحميل الصفحة: ${loadTime}ms`);
            }
        });
    }

    monitorMemoryUsage() {
        if (performance.memory) {
            setInterval(() => {
                const memory = performance.memory;
                const usedMB = Math.round(memory.usedJSHeapSize / 1048576);
                const totalMB = Math.round(memory.totalJSHeapSize / 1048576);
                
                // تحذير إذا تجاوز الاستخدام 100MB
                if (usedMB > 100) {
                    console.warn(`⚠️ استخدام ذاكرة عالي: ${usedMB}MB`);
                }
            }, 30000); // كل 30 ثانية
        }
    }

    createPerformanceUI() {
        // إنشاء لوحة الأداء
        const panel = document.createElement('div');
        panel.id = 'performance-panel';
        panel.className = 'performance-panel';
        panel.innerHTML = `
            <div class="performance-header">
                <i class="fas fa-chart-line"></i>
                <span>الأداء</span>
                <button class="toggle-btn" onclick="performanceMonitor.togglePanel()">
                    <i class="fas fa-chevron-up"></i>
                </button>
            </div>
            <div class="performance-content">
                <div class="metric">
                    <span class="metric-label">عمليات الحفظ:</span>
                    <span class="metric-value" id="save-count">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">متوسط وقت الحفظ:</span>
                    <span class="metric-value" id="avg-save-time">0ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">الأخطاء:</span>
                    <span class="metric-value" id="error-count">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">طلبات الشبكة:</span>
                    <span class="metric-value" id="network-count">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">وقت التشغيل:</span>
                    <span class="metric-value" id="uptime">0s</span>
                </div>
            </div>
        `;

        // إضافة الأنماط
        const styles = document.createElement('style');
        styles.textContent = `
            .performance-panel {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                min-width: 200px;
                font-size: 12px;
                display: none; /* مخفي بشكل افتراضي */
            }

            .performance-header {
                background: #f8f9fa;
                padding: 8px 12px;
                border-radius: 8px 8px 0 0;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid #dee2e6;
                cursor: pointer;
            }

            .performance-content {
                padding: 8px 12px;
                max-height: 200px;
                overflow-y: auto;
            }

            .performance-content.collapsed {
                display: none;
            }

            .metric {
                display: flex;
                justify-content: space-between;
                margin-bottom: 4px;
                padding: 2px 0;
            }

            .metric-label {
                color: #666;
            }

            .metric-value {
                font-weight: 600;
                color: #333;
            }

            .toggle-btn {
                background: none;
                border: none;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            @media (max-width: 768px) {
                .performance-panel {
                    bottom: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(styles);
        document.body.appendChild(panel);

        // تحديث دوري
        setInterval(() => {
            this.updatePerformanceUI();
        }, 5000);
    }

    updatePerformanceUI() {
        const saveCount = document.getElementById('save-count');
        const avgSaveTime = document.getElementById('avg-save-time');
        const errorCount = document.getElementById('error-count');
        const networkCount = document.getElementById('network-count');
        const uptime = document.getElementById('uptime');

        if (saveCount) {
            saveCount.textContent = this.metrics.saveOperations;
        }

        if (avgSaveTime && this.metrics.saveTime.length > 0) {
            const avg = this.metrics.saveTime.reduce((a, b) => a + b, 0) / this.metrics.saveTime.length;
            avgSaveTime.textContent = Math.round(avg) + 'ms';
        }

        if (errorCount) {
            errorCount.textContent = this.metrics.errors;
            errorCount.style.color = this.metrics.errors > 0 ? '#dc3545' : '#28a745';
        }

        if (networkCount) {
            networkCount.textContent = this.metrics.networkRequests;
        }

        if (uptime) {
            const seconds = Math.floor((Date.now() - this.startTime) / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);
            
            if (hours > 0) {
                uptime.textContent = `${hours}h ${minutes % 60}m`;
            } else if (minutes > 0) {
                uptime.textContent = `${minutes}m ${seconds % 60}s`;
            } else {
                uptime.textContent = `${seconds}s`;
            }
        }
    }

    togglePanel() {
        const content = document.querySelector('.performance-content');
        const icon = document.querySelector('.toggle-btn i');
        
        if (content.classList.contains('collapsed')) {
            content.classList.remove('collapsed');
            icon.className = 'fas fa-chevron-up';
        } else {
            content.classList.add('collapsed');
            icon.className = 'fas fa-chevron-down';
        }
    }

    // تصدير البيانات
    exportMetrics() {
        const data = {
            ...this.metrics,
            sessionDuration: Date.now() - this.startTime,
            timestamp: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `performance-metrics-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
        showSuccess('تم تصدير بيانات الأداء');
    }

    // إعادة تعيين الإحصائيات
    resetMetrics() {
        this.metrics = {
            saveOperations: 0,
            saveTime: [],
            errors: 0,
            networkRequests: 0,
            cacheHits: 0,
            cacheMisses: 0
        };
        
        this.startTime = Date.now();
        this.updatePerformanceUI();
        showInfo('تم إعادة تعيين إحصائيات الأداء');
    }
}

// إنشاء نسخة عامة
const performanceMonitor = new PerformanceMonitor();

// دوال مساعدة
function getPerformanceMetrics() {
    return performanceMonitor.metrics;
}

function exportPerformanceData() {
    return performanceMonitor.exportMetrics();
}

function resetPerformanceMetrics() {
    return performanceMonitor.resetMetrics();
}

// تصدير
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PerformanceMonitor,
        performanceMonitor,
        getPerformanceMetrics,
        exportPerformanceData,
        resetPerformanceMetrics
    };
}
