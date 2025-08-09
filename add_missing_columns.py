#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db
import sqlite3

def add_missing_columns():
    """إضافة الأعمدة المفقودة إلى جدول sale"""
    with app.app_context():
        try:
            # الاتصال بقاعدة البيانات مباشرة
            db_path = 'instance/accounting.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # التحقق من الأعمدة الموجودة
            cursor.execute("PRAGMA table_info(sale)")
            columns = [column[1] for column in cursor.fetchall()]
            print('الأعمدة الحالية:', columns)
            
            # إضافة الأعمدة المفقودة
            missing_columns = [
                ('tax_rate', 'FLOAT DEFAULT 15.0'),
                ('tax_amount', 'FLOAT DEFAULT 0')
            ]
            
            for column_name, column_def in missing_columns:
                if column_name not in columns:
                    print(f'إضافة عمود {column_name}...')
                    cursor.execute(f'ALTER TABLE sale ADD COLUMN {column_name} {column_def}')
                else:
                    print(f'✅ عمود {column_name} موجود بالفعل')
            
            conn.commit()
            
            # التحقق من النتيجة النهائية
            cursor.execute("PRAGMA table_info(sale)")
            columns = [column[1] for column in cursor.fetchall()]
            print('✅ الأعمدة النهائية لجدول sale:', columns)
            
            conn.close()
            print('🎉 تم تحديث جدول sale بنجاح!')
            
        except Exception as e:
            print(f'❌ خطأ: {e}')

if __name__ == '__main__':
    add_missing_columns()
