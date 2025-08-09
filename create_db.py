from app import app, db

with app.app_context():
    # إنشاء الجداول مع الحقول الجديدة
    db.create_all()
    print('✅ تم إنشاء/تحديث قاعدة البيانات مع حقول المدفوعات')

    # فحص الجداول المنشأة
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f'📋 الجداول المنشأة: {tables}')

    # فحص أعمدة جدول المبيعات
    if 'sale' in tables:
        columns = [col['name'] for col in inspector.get_columns('sale')]
        print(f'📊 أعمدة جدول المبيعات: {columns}')

        payment_fields = ['payment_status', 'paid_amount', 'payment_date', 'payment_method']
        missing_fields = [field for field in payment_fields if field not in columns]

        if missing_fields:
            print(f'⚠️ حقول مفقودة في جدول المبيعات: {missing_fields}')
        else:
            print('✅ جميع حقول المدفوعات موجودة في جدول المبيعات')

    print('🎉 قاعدة البيانات جاهزة!')
