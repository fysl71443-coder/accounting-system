from app import app, db, Product

with app.app_context():
    try:
        product = Product(
            name='لابتوب ديل',
            description='لابتوب ديل انسبايرون 15',
            price=2500.00,
            cost=2000.00,
            quantity=10,
            category='إلكترونيات'
        )
        db.session.add(product)
        db.session.commit()
        print('✅ Product created successfully')
        
        # Verify
        count = Product.query.count()
        print(f'Total products: {count}')
        
    except Exception as e:
        print(f'Error: {e}')
