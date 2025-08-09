from app import app, db, Product, Customer, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Add admin user
    try:
        admin = User(
            username='admin',
            email='admin@example.com', 
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin user created')
    except:
        print('Admin user already exists')
    
    # Add sample customer
    try:
        customer = Customer(name='شركة الأعمال المتقدمة', email='info@advanced.com', phone='0501234567')
        db.session.add(customer)
        db.session.commit()
        print('✅ Sample customer created')
    except:
        print('Customer already exists')
    
    # Add sample product with minimal fields
    try:
        product = Product(
            name='لابتوب ديل',
            description='لابتوب ديل انسبايرون 15',
            price=2500.00,
            cost=2000.00,
            category='إلكترونيات'
        )
        db.session.add(product)
        db.session.commit()
        print('✅ Sample product created')
    except Exception as e:
        print(f'Error creating product: {e}')
    
    print('🎉 Setup completed')
