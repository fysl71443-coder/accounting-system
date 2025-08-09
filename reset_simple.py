import os
import sys
from app import app, db, User, Customer, Supplier, Product, Sale, Purchase, Expense, Employee, Payroll
from werkzeug.security import generate_password_hash

def reset_database():
    print("Resetting database...")
    
    with app.app_context():
        db.drop_all()
        print("Dropped old tables")
        
        db.create_all()
        print("Created new tables")
        
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin112233'),
            is_admin=True
        )
        db.session.add(admin_user)
        print("Created admin user")
        
        customers = [
            Customer(name='Company A', phone='0501234567', email='a@example.com'),
            Customer(name='Company B', phone='0507654321', email='b@example.com'),
            Customer(name='Company C', phone='0509876543', email='c@example.com'),
            Customer(name='Company D', phone='0502468135', email='d@example.com'),
            Customer(name='Cash Customer', phone='0500000000', email='cash@example.com')
        ]
        for customer in customers:
            db.session.add(customer)
        print("Created customers")
        
        suppliers = [
            Supplier(name='Supplier A', phone='0111234567', email='sa@example.com'),
            Supplier(name='Supplier B', phone='0117654321', email='sb@example.com'),
            Supplier(name='Supplier C', phone='0119876543', email='sc@example.com'),
            Supplier(name='Supplier D', phone='0112468135', email='sd@example.com')
        ]
        for supplier in suppliers:
            db.session.add(supplier)
        print("Created suppliers")
        
        products = [
            Product(name='Product A', price=100, cost=70, quantity=50, category='Cat 1'),
            Product(name='Product B', price=200, cost=140, quantity=30, category='Cat 2'),
            Product(name='Product C', price=150, cost=100, quantity=40, category='Cat 1'),
            Product(name='Product D', price=300, cost=200, quantity=20, category='Cat 3')
        ]
        for product in products:
            db.session.add(product)
        print("Created products")
        
        sales = [
            Sale(customer_id=1, subtotal=2700, discount=200, total=2500),
            Sale(customer_id=2, subtotal=2000, discount=200, total=1800),
            Sale(customer_id=3, subtotal=3500, discount=300, total=3200),
            Sale(customer_id=4, subtotal=1650, discount=150, total=1500),
            Sale(customer_id=5, subtotal=1000, discount=50, total=950)
        ]
        for sale in sales:
            db.session.add(sale)
        print("Created sales with discount")
        
        purchases = [
            Purchase(supplier_id=1, subtotal=6000, discount=500, total=5500),
            Purchase(supplier_id=2, subtotal=3500, discount=300, total=3200),
            Purchase(supplier_id=3, subtotal=4400, discount=300, total=4100),
            Purchase(supplier_id=4, subtotal=3000, discount=200, total=2800)
        ]
        for purchase in purchases:
            db.session.add(purchase)
        print("Created purchases with discount")
        
        expenses = [
            Expense(description='Admin Expenses', amount=800, category='Admin'),
            Expense(description='Operating Expenses', amount=1200, category='Operating'),
            Expense(description='Maintenance Expenses', amount=650, category='Maintenance'),
            Expense(description='Transport Expenses', amount=450, category='Transport')
        ]
        for expense in expenses:
            db.session.add(expense)
        print("Created expenses")
        
        employees = [
            Employee(name='Ahmed Ali', position='Sales Manager', salary=8500, phone='0501111111'),
            Employee(name='Fatima Salem', position='Accountant', salary=6200, phone='0502222222'),
            Employee(name='Mohammed Hassan', position='Admin', salary=4800, phone='0503333333'),
            Employee(name='Sara Mohammed', position='Secretary', salary=4200, phone='0504444444')
        ]
        for employee in employees:
            db.session.add(employee)
        print("Created employees")
        
        payrolls = [
            Payroll(employee_id=1, amount=8500, month='2024-01'),
            Payroll(employee_id=2, amount=6200, month='2024-01'),
            Payroll(employee_id=3, amount=4800, month='2024-01'),
            Payroll(employee_id=4, amount=4200, month='2024-01')
        ]
        for payroll in payrolls:
            db.session.add(payroll)
        print("Created payrolls")
        
        db.session.commit()
        print("Saved all data")
        
        print("\nDatabase reset successfully!")
        print("Login: admin / admin112233")

if __name__ == '__main__':
    reset_database()
