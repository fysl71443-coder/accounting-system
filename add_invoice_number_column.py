#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db
import sqlite3

def add_invoice_number_column():
    """إضافة عمود invoice_number إلى جدول sale"""
    with app.app_context():
        try:
            # الاتصال بقاعدة البيانات مباشرة
            db_path = 'instance/accounting.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # التحقق من وجود العمود
            cursor.execute("PRAGMA table_info(sale)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'invoice_number' not in columns:
                print('إضافة عمود invoice_number...')
                cursor.execute('ALTER TABLE sale ADD COLUMN invoice_number VARCHAR(50)')
                
                # إضافة فهرس فريد للعمود
                cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_sale_invoice_number ON sale(invoice_number)')
                
                # تحديث السجلات الموجودة بأرقام فواتير
                cursor.execute('SELECT id FROM sale ORDER BY id')
                sales = cursor.fetchall()
                
                for i, (sale_id,) in enumerate(sales, 1):
                    invoice_number = f'INV-{sale_id:06d}'
                    cursor.execute('UPDATE sale SET invoice_number = ? WHERE id = ?', (invoice_number, sale_id))
                
                conn.commit()
                print(f'✅ تم إضافة عمود invoice_number وتحديث {len(sales)} سجل')
            else:
                print('✅ عمود invoice_number موجود بالفعل')
            
            # التحقق من النتيجة
            cursor.execute("PRAGMA table_info(sale)")
            columns = [column[1] for column in cursor.fetchall()]
            print('أعمدة جدول sale:', columns)
            
            conn.close()
            
        except Exception as e:
            print(f'❌ خطأ: {e}')

if __name__ == '__main__':
    add_invoice_number_column()
