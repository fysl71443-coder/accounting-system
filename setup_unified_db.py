#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد قاعدة البيانات للشاشة الموحدة
Setup Database for Unified Products Screen
"""

from app import app, db, RawMaterial, ProductCost
import datetime

def setup_database():
    """إعداد قاعدة البيانات وإضافة البيانات التجريبية"""
    
    with app.app_context():
        # إنشاء الجداول الجديدة
        db.create_all()
        print('✅ تم إنشاء الجداول الجديدة')
        
        # إضافة مواد خام تجريبية
        sample_materials = [
            {'name': 'دجاج طازج', 'unit': 'كيلو', 'price': 25.00, 'stock': 50.0, 'min_stock': 10.0, 'supplier': 'مؤسسة اللحوم الطازجة'},
            {'name': 'أرز بسمتي', 'unit': 'كيلو', 'price': 8.50, 'stock': 100.0, 'min_stock': 20.0, 'supplier': 'شركة الحبوب المتحدة'},
            {'name': 'بصل أحمر', 'unit': 'كيلو', 'price': 3.00, 'stock': 30.0, 'min_stock': 5.0, 'supplier': 'سوق الخضار المركزي'},
            {'name': 'طماطم طازجة', 'unit': 'كيلو', 'price': 4.50, 'stock': 25.0, 'min_stock': 5.0, 'supplier': 'سوق الخضار المركزي'},
            {'name': 'زيت الذرة', 'unit': 'لتر', 'price': 12.00, 'stock': 20.0, 'min_stock': 3.0, 'supplier': 'شركة الزيوت النباتية'},
            {'name': 'ملح طعام', 'unit': 'كيلو', 'price': 2.00, 'stock': 10.0, 'min_stock': 2.0, 'supplier': 'شركة الملح الصافي'},
            {'name': 'فلفل أسود مطحون', 'unit': 'جرام', 'price': 0.05, 'stock': 500.0, 'min_stock': 100.0, 'supplier': 'محل البهارات العربية'},
            {'name': 'كمون مطحون', 'unit': 'جرام', 'price': 0.08, 'stock': 300.0, 'min_stock': 50.0, 'supplier': 'محل البهارات العربية'},
            {'name': 'هيل مطحون', 'unit': 'جرام', 'price': 0.15, 'stock': 200.0, 'min_stock': 30.0, 'supplier': 'محل البهارات العربية'},
            {'name': 'جزر طازج', 'unit': 'كيلو', 'price': 3.50, 'stock': 20.0, 'min_stock': 5.0, 'supplier': 'سوق الخضار المركزي'},
            {'name': 'بازلاء مجمدة', 'unit': 'كيلو', 'price': 6.00, 'stock': 15.0, 'min_stock': 3.0, 'supplier': 'شركة الخضار المجمدة'},
            {'name': 'زبدة طبيعية', 'unit': 'كيلو', 'price': 18.00, 'stock': 10.0, 'min_stock': 2.0, 'supplier': 'مصنع منتجات الألبان'},
            {'name': 'دقيق أبيض', 'unit': 'كيلو', 'price': 4.00, 'stock': 40.0, 'min_stock': 10.0, 'supplier': 'مطاحن الدقيق'},
            {'name': 'سكر أبيض', 'unit': 'كيلو', 'price': 3.50, 'stock': 25.0, 'min_stock': 5.0, 'supplier': 'مصفاة السكر'},
            {'name': 'بيض طازج', 'unit': 'قطعة', 'price': 0.50, 'stock': 200.0, 'min_stock': 50.0, 'supplier': 'مزرعة الدواجن'},
            {'name': 'حليب طازج', 'unit': 'لتر', 'price': 5.00, 'stock': 30.0, 'min_stock': 10.0, 'supplier': 'مصنع منتجات الألبان'},
            {'name': 'جبن موزاريلا', 'unit': 'كيلو', 'price': 35.00, 'stock': 8.0, 'min_stock': 2.0, 'supplier': 'مصنع الأجبان الإيطالية'},
            {'name': 'خس طازج', 'unit': 'كيلو', 'price': 4.00, 'stock': 15.0, 'min_stock': 3.0, 'supplier': 'سوق الخضار المركزي'},
            {'name': 'خيار طازج', 'unit': 'كيلو', 'price': 2.50, 'stock': 20.0, 'min_stock': 5.0, 'supplier': 'سوق الخضار المركزي'},
            {'name': 'ليمون طازج', 'unit': 'كيلو', 'price': 6.00, 'stock': 12.0, 'min_stock': 3.0, 'supplier': 'سوق الفواكه'}
        ]
        
        added_count = 0
        for material_data in sample_materials:
            existing = RawMaterial.query.filter_by(name=material_data['name']).first()
            if not existing:
                material = RawMaterial(
                    name=material_data['name'],
                    unit=material_data['unit'],
                    purchase_price=material_data['price'],
                    current_stock=material_data['stock'],
                    min_stock_level=material_data['min_stock'],
                    supplier=material_data['supplier'],
                    is_active=True,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                db.session.add(material)
                added_count += 1
        
        db.session.commit()
        
        print(f'✅ تم إضافة {added_count} مادة خام جديدة')
        
        # عرض إجمالي المواد الخام
        total_materials = RawMaterial.query.filter_by(is_active=True).count()
        print(f'📦 إجمالي المواد الخام: {total_materials}')
        
        # عرض المواد التي تحتاج تجديد مخزون
        low_stock = RawMaterial.query.filter(RawMaterial.current_stock <= RawMaterial.min_stock_level).all()
        if low_stock:
            print(f'⚠️ مواد تحتاج تجديد مخزون ({len(low_stock)}):')
            for material in low_stock:
                print(f'   - {material.name}: {material.current_stock} {material.unit} (الحد الأدنى: {material.min_stock_level})')
        else:
            print('✅ جميع المواد الخام متوفرة بكميات كافية')
        
        print('\n🎉 تم إعداد قاعدة البيانات بنجاح!')
        print('🌐 يمكنك الآن الوصول للشاشة الموحدة على: http://localhost:5000/unified_products')

if __name__ == "__main__":
    setup_database()
