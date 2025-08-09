
# Additional Database Models for Button System
# Add these to your app.py file

class Purchase(db.Model):
    """Purchase model for purchases functionality"""
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_number = db.Column(db.String(50), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    purchase_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PurchaseItem(db.Model):
    """Purchase item model"""
    __tablename__ = 'purchase_items'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)

class Payment(db.Model):
    """Payment model for payment tracking"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, nullable=False)
    invoice_type = db.Column(db.String(20), nullable=False)  # 'sale' or 'purchase'
    amount_paid = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    """Employee model"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    salary = db.Column(db.Float, default=0.0)
    hire_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Tax(db.Model):
    """Tax model"""
    __tablename__ = 'taxes'
    
    id = db.Column(db.Integer, primary_key=True)
    tax_name = db.Column(db.String(100), nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    tax_type = db.Column(db.String(50))  # 'percentage' or 'fixed'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    """Expense model"""
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100))
    payment_method = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
