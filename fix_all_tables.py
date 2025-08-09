#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db
import sqlite3

def fix_all_tables():
    """إصلاح جميع الجداول بإضافة الأعمدة المفقودة"""
    with app.app_context():
        try:
            # الاتصال بقاعدة البيانات مباشرة
            db_path = 'instance/accounting.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            print('🔧 بدء إصلاح جميع الجداول...\n')
            
            # إصلاح جدول purchase
            print('📦 إصلاح جدول purchase...')
            cursor.execute("PRAGMA table_info(purchase)")
            purchase_columns = [column[1] for column in cursor.fetchall()]
            print('الأعمدة الحالية:', purchase_columns)
            
            purchase_missing = [
                ('purchase_number', 'VARCHAR(50)'),
                ('tax_rate', 'FLOAT DEFAULT 15.0'),
                ('tax_amount', 'FLOAT DEFAULT 0')
            ]
            
            for column_name, column_def in purchase_missing:
                if column_name not in purchase_columns:
                    print(f'إضافة عمود {column_name}...')
                    cursor.execute(f'ALTER TABLE purchase ADD COLUMN {column_name} {column_def}')
            
            # إضافة أرقام المشتريات
            if 'purchase_number' not in purchase_columns:
                cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_purchase_purchase_number ON purchase(purchase_number)')
                cursor.execute('SELECT id FROM purchase ORDER BY id')
                purchases = cursor.fetchall()
                for i, (purchase_id,) in enumerate(purchases, 1):
                    purchase_number = f'PUR-{purchase_id:06d}'
                    cursor.execute('UPDATE purchase SET purchase_number = ? WHERE id = ?', (purchase_number, purchase_id))
                print(f'✅ تم تحديث {len(purchases)} سجل مشتريات')
            
            print('✅ تم إصلاح جدول purchase\n')
            
            # التحقق من جدول user
            print('👤 التحقق من جدول user...')
            cursor.execute("PRAGMA table_info(user)")
            user_columns = [column[1] for column in cursor.fetchall()]
            print('الأعمدة الحالية:', user_columns)
            
            user_missing = [
                ('role', 'VARCHAR(50) DEFAULT "user"'),
                ('is_active', 'BOOLEAN DEFAULT 1')
            ]
            
            for column_name, column_def in user_missing:
                if column_name not in user_columns:
                    print(f'إضافة عمود {column_name}...')
                    cursor.execute(f'ALTER TABLE user ADD COLUMN {column_name} {column_def}')
            
            print('✅ تم إصلاح جدول user\n')
            
            conn.commit()
            
            # عرض ملخص نهائي
            print('📊 ملخص الجداول النهائي:')
            tables_to_check = ['sale', 'expense', 'purchase', 'user', 'product', 'customer']
            
            for table_name in tables_to_check:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in cursor.fetchall()]
                print(f'✅ {table_name}: {len(columns)} عمود - {columns[:5]}{"..." if len(columns) > 5 else ""}')
            
            conn.close()
            print('\n🎉 تم إصلاح جميع الجداول بنجاح!')
            
        except Exception as e:
            print(f'❌ خطأ: {e}')

if __name__ == '__main__':
    fix_all_tables()
