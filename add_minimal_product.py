from app import app, db, Product

with app.app_context():
    try:
        # Create product with only basic fields
        product = Product(
            name='لابتوب ديل',
            description='لابتوب ديل انسبايرون 15',
            price=2500.00,
            cost=2000.00
        )
        db.session.add(product)
        db.session.commit()
        print('✅ Minimal product created successfully')
    except Exception as e:
        print(f'Error: {e}')
        
    # Check products count
    try:
        count = Product.query.count()
        print(f'Products in database: {count}')
    except Exception as e:
        print(f'Error counting products: {e}')
