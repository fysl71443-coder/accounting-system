#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db
import sqlite3

def fix_expense_table():
    """إصلاح جدول expense بإضافة الأعمدة المفقودة"""
    with app.app_context():
        try:
            # الاتصال بقاعدة البيانات مباشرة
            db_path = 'instance/accounting.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # التحقق من الأعمدة الموجودة
            cursor.execute("PRAGMA table_info(expense)")
            columns = [column[1] for column in cursor.fetchall()]
            print('الأعمدة الحالية لجدول expense:', columns)
            
            # إضافة الأعمدة المفقودة
            missing_columns = [
                ('expense_number', 'VARCHAR(50)'),
                ('expense_type', 'VARCHAR(50)'),
                ('reference', 'VARCHAR(100)'),
                ('vendor', 'VARCHAR(100)')
            ]
            
            for column_name, column_def in missing_columns:
                if column_name not in columns:
                    print(f'إضافة عمود {column_name}...')
                    cursor.execute(f'ALTER TABLE expense ADD COLUMN {column_name} {column_def}')
                else:
                    print(f'✅ عمود {column_name} موجود بالفعل')
            
            # إضافة فهرس فريد لـ expense_number إذا لم يكن موجوداً
            if 'expense_number' not in columns:
                cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_expense_expense_number ON expense(expense_number)')
                
                # تحديث السجلات الموجودة بأرقام مصروفات
                cursor.execute('SELECT id FROM expense ORDER BY id')
                expenses = cursor.fetchall()
                
                for i, (expense_id,) in enumerate(expenses, 1):
                    expense_number = f'EXP-{expense_id:06d}'
                    cursor.execute('UPDATE expense SET expense_number = ? WHERE id = ?', (expense_number, expense_id))
                
                print(f'✅ تم تحديث {len(expenses)} سجل مصروف برقم مصروف')
            
            conn.commit()
            
            # التحقق من النتيجة النهائية
            cursor.execute("PRAGMA table_info(expense)")
            columns = [column[1] for column in cursor.fetchall()]
            print('✅ الأعمدة النهائية لجدول expense:', columns)
            
            conn.close()
            print('🎉 تم إصلاح جدول expense بنجاح!')
            
        except Exception as e:
            print(f'❌ خطأ: {e}')

if __name__ == '__main__':
    fix_expense_table()
