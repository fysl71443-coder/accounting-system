from app import app, db, Product, Customer, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Add admin user if not exists
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@example.com', 
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        print('✅ Admin user created')
    
    # Add sample customers
    if Customer.query.count() == 0:
        customers = [
            Customer(name='شركة الأعمال المتقدمة', email='info@advanced.com', phone='0501234567'),
            Customer(name='مؤسسة التقنية الحديثة', email='contact@tech.com', phone='0507654321'),
            Customer(name='شركة الحلول الذكية', email='sales@smart.com', phone='0509876543')
        ]
        for c in customers:
            db.session.add(c)
        print('✅ Sample customers created')
    
    # Add sample products
    if Product.query.count() == 0:
        products = [
            Product(
                name='لابتوب ديل انسبايرون 15',
                description='لابتوب ديل انسبايرون 15 - معالج Intel Core i5',
                price=2500.00,
                cost=2000.00,
                stock_quantity=10,
                category='إلكترونيات',
                is_active=True
            ),
            Product(
                name='ماوس لاسلكي لوجيتك',
                description='ماوس لاسلكي لوجيتك MX Master 3',
                price=150.00,
                cost=100.00,
                stock_quantity=50,
                category='إكسسوارات',
                is_active=True
            ),
            Product(
                name='كيبورد ميكانيكي',
                description='كيبورد ميكانيكي للألعاب RGB',
                price=300.00,
                cost=200.00,
                stock_quantity=25,
                category='إكسسوارات',
                is_active=True
            )
        ]
        for p in products:
            db.session.add(p)
        print('✅ Sample products created')
    
    db.session.commit()
    print('🎉 Database setup completed')
