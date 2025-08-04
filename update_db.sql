-- تحديث قاعدة البيانات لدعم نظام الصلاحيات
-- Database Update Script for Permissions System

-- 1. إنشاء جدول الأدوار
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(80) UNIQUE NOT NULL,
    name_ar VARCHAR(80) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- صلاحيات الوصول للشاشات
    can_access_sales BOOLEAN DEFAULT 0,
    can_access_purchases BOOLEAN DEFAULT 0,
    can_access_inventory BOOLEAN DEFAULT 0,
    can_access_reports BOOLEAN DEFAULT 0,
    can_access_employees BOOLEAN DEFAULT 0,
    can_access_costs BOOLEAN DEFAULT 0,
    can_access_taxes BOOLEAN DEFAULT 0,
    can_access_settings BOOLEAN DEFAULT 0,
    can_access_financial_statements BOOLEAN DEFAULT 0,
    can_access_payments BOOLEAN DEFAULT 0,
    can_access_expenses BOOLEAN DEFAULT 0,
    can_access_suppliers BOOLEAN DEFAULT 0,
    
    -- صلاحيات العمليات CRUD
    can_create BOOLEAN DEFAULT 0,
    can_edit BOOLEAN DEFAULT 0,
    can_delete BOOLEAN DEFAULT 0,
    can_print BOOLEAN DEFAULT 0,
    can_export BOOLEAN DEFAULT 0
);

-- 2. إضافة الأعمدة الجديدة لجدول المستخدمين
ALTER TABLE users ADD COLUMN role_id INTEGER;
ALTER TABLE users ADD COLUMN old_role VARCHAR(20) DEFAULT 'user';
ALTER TABLE users ADD COLUMN login_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN locked_until DATETIME;

-- 3. إدراج الأدوار الافتراضية
INSERT OR IGNORE INTO roles (
    name, name_ar, description, is_active,
    can_access_sales, can_access_purchases, can_access_inventory, 
    can_access_reports, can_access_employees, can_access_costs,
    can_access_taxes, can_access_settings, can_access_financial_statements,
    can_access_payments, can_access_expenses, can_access_suppliers,
    can_create, can_edit, can_delete, can_print, can_export
) VALUES 
-- مشرف عام - جميع الصلاحيات
('admin', 'مشرف عام', 'صلاحيات كاملة لجميع أجزاء النظام', 1,
 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  -- صلاحيات الوصول
 1, 1, 1, 1, 1),  -- صلاحيات العمليات

-- محاسب - صلاحيات محاسبية
('accountant', 'محاسب', 'صلاحيات محاسبية ومالية', 1,
 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1,  -- صلاحيات الوصول
 1, 1, 0, 1, 1),  -- صلاحيات العمليات

-- موظف - صلاحيات محدودة
('employee', 'موظف', 'صلاحيات محدودة للعمليات الأساسية', 1,
 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  -- صلاحيات الوصول
 1, 0, 0, 1, 0),  -- صلاحيات العمليات

-- مراقب - عرض فقط
('viewer', 'مراقب', 'صلاحيات عرض فقط', 1,
 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1,  -- صلاحيات الوصول
 0, 0, 0, 1, 0),  -- صلاحيات العمليات

-- مدير - صلاحيات إدارية
('manager', 'مدير', 'صلاحيات إدارية مع قيود محددة', 1,
 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,  -- صلاحيات الوصول
 1, 1, 0, 1, 1);   -- صلاحيات العمليات

-- 4. تحديث المستخدمين الموجودين
-- نسخ الدور القديم إلى old_role
UPDATE users SET old_role = role WHERE old_role IS NULL OR old_role = '';

-- ربط المستخدمين بالأدوار الجديدة
UPDATE users SET role_id = (SELECT id FROM roles WHERE name = 'admin') 
WHERE role = 'admin' OR old_role = 'admin';

UPDATE users SET role_id = (SELECT id FROM roles WHERE name = 'employee') 
WHERE (role = 'user' OR old_role = 'user') AND role_id IS NULL;

-- 5. إنشاء جدول جلسات المستخدمين (اختياري)
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 6. عرض النتائج
SELECT 'تم إنشاء الأدوار التالية:' as message;
SELECT name, name_ar, description FROM roles;

SELECT 'المستخدمين المحدثين:' as message;
SELECT u.username, u.full_name, r.name_ar as role_name 
FROM users u 
LEFT JOIN roles r ON u.role_id = r.id;
