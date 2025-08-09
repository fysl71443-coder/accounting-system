#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخة نظيفة من app.py لاختبار شاشة المبيعات
Clean version of app.py for testing Sales screen
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import logging

# إعداد التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-key-for-development')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد قاعدة البيانات
db = SQLAlchemy(app)

# إعداد تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# النماذج الأساسية
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    invoice_date = db.Column(db.Date, nullable=False, default=date.today)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer_name = db.Column(db.String(100))
    total_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='sales')
    branch = db.relationship('Branch', backref='sales')
    creator = db.relationship('User', backref='sales')

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0)
    
    sale = db.relationship('Sale', backref='items')
    product = db.relationship('Product', backref='sale_items')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# الصفحات الأساسية
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('sales'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# شاشة المبيعات
@app.route('/sales')
@login_required
def sales():
    """شاشة المبيعات الرئيسية"""
    try:
        sales = Sale.query.order_by(Sale.created_at.desc()).all()
        return render_template('sales.html', sales=sales)
    except Exception as e:
        logger.error(f"خطأ في شاشة المبيعات: {e}")
        flash('حدث خطأ في تحميل شاشة المبيعات')
        return render_template('sales.html', sales=[])

# API routes للمبيعات
@app.route('/api/sales/delete/<int:record_id>', methods=['DELETE'])
@login_required
def sales_delete_record(record_id):
    """Delete sales record"""
    try:
        logger.info(f"🔵 Sales - Delete Record button clicked for ID: {record_id}")
        
        sale = Sale.query.get_or_404(record_id)
        invoice_number = sale.invoice_number
        
        # Delete related sale items first
        SaleItem.query.filter_by(sale_id=record_id).delete()
        
        # Delete the sale record
        db.session.delete(sale)
        db.session.commit()
        
        logger.info(f"✅ Sales record {invoice_number} deleted successfully")
        return jsonify({'success': True, 'message': f'Sales record {invoice_number} deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error deleting sales record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting record: {str(e)}'})

@app.route('/api/sales/preview/<int:record_id>')
@login_required
def sales_preview_record(record_id):
    """Preview sales record"""
    try:
        logger.info(f"🔵 Sales - Preview Record button clicked for ID: {record_id}")
        
        sale = Sale.query.get_or_404(record_id)
        sale_items = SaleItem.query.filter_by(sale_id=record_id).all()
        
        # Generate preview HTML
        preview_html = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>معاينة الفاتورة {sale.invoice_number}</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
                .invoice-header {{ text-align: center; margin-bottom: 30px; }}
                .invoice-details {{ margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
                .total {{ font-weight: bold; background-color: #e9ecef; }}
            </style>
        </head>
        <body>
            <div class="invoice-header">
                <h2>فاتورة مبيعات</h2>
                <h3>رقم الفاتورة: {sale.invoice_number}</h3>
            </div>
            <div class="invoice-details">
                <p><strong>العميل:</strong> {sale.customer_name or 'عميل نقدي'}</p>
                <p><strong>التاريخ:</strong> {sale.invoice_date}</p>
                <p><strong>الفرع:</strong> {sale.branch.name if sale.branch else 'غير محدد'}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>المنتج</th>
                        <th>الكمية</th>
                        <th>السعر</th>
                        <th>الإجمالي</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for item in sale_items:
            preview_html += f"""
                    <tr>
                        <td>{item.product.name if item.product else 'منتج محذوف'}</td>
                        <td>{item.quantity}</td>
                        <td>{item.unit_price:.2f} ريال</td>
                        <td>{item.total_price:.2f} ريال</td>
                    </tr>
            """
        
        preview_html += f"""
                </tbody>
                <tfoot>
                    <tr class="total">
                        <td colspan="3">المجموع الفرعي</td>
                        <td>{sale.total_amount:.2f} ريال</td>
                    </tr>
                    <tr class="total">
                        <td colspan="3">الضريبة</td>
                        <td>{sale.tax_amount:.2f} ريال</td>
                    </tr>
                    <tr class="total">
                        <td colspan="3">المجموع النهائي</td>
                        <td>{sale.final_amount:.2f} ريال</td>
                    </tr>
                </tfoot>
            </table>
        </body>
        </html>
        """
        
        logger.info(f"✅ Preview generated for sales record {sale.invoice_number}")
        return jsonify({'success': True, 'html': preview_html})
        
    except Exception as e:
        logger.error(f"❌ Error preparing sales record for preview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing preview: {str(e)}'})

@app.route('/api/sales/register_payment', methods=['POST'])
@login_required
def sales_register_payment():
    """Register payment for sales invoice"""
    try:
        logger.info("🔵 Sales - Register Payment button clicked")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['invoice_id', 'amount', 'payment_method', 'payment_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        invoice_id = int(data['invoice_id'])
        amount = float(data['amount'])
        payment_method = data['payment_method']
        payment_date = data['payment_date']
        notes = data.get('notes', '')
        
        # Validate invoice exists
        sale = Sale.query.get_or_404(invoice_id)
        
        # Update the sale record with payment info
        sale.payment_method = payment_method
        sale.payment_status = 'paid' if amount >= sale.final_amount else 'partial'
        sale.notes = f"{sale.notes or ''}\nPayment: {amount} SAR on {payment_date} via {payment_method}. {notes}".strip()
        
        db.session.commit()
        
        logger.info(f"✅ Payment registered for invoice {sale.invoice_number}: {amount} SAR")
        return jsonify({
            'success': True, 
            'message': f'Payment of {amount} SAR registered successfully for invoice {sale.invoice_number}'
        })
        
    except Exception as e:
        logger.error(f"❌ Error registering payment: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error registering payment: {str(e)}'})

def create_default_data():
    """إنشاء البيانات الافتراضية"""
    try:
        # إنشاء مستخدم افتراضي
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
        
        # إنشاء فرع افتراضي
        if not Branch.query.first():
            branch = Branch(name='الفرع الرئيسي', location='الرياض')
            db.session.add(branch)
        
        # إنشاء منتجات تجريبية
        if not Product.query.first():
            products = [
                Product(name='منتج 1', price=100.0, stock_quantity=50),
                Product(name='منتج 2', price=200.0, stock_quantity=30),
                Product(name='منتج 3', price=150.0, stock_quantity=40)
            ]
            for product in products:
                db.session.add(product)
        
        # إنشاء عملاء تجريبيين
        if not Customer.query.first():
            customers = [
                Customer(name='عميل 1', phone='0501234567', email='customer1@example.com'),
                Customer(name='عميل 2', phone='0507654321', email='customer2@example.com')
            ]
            for customer in customers:
                db.session.add(customer)
        
        db.session.commit()
        logger.info("✅ Default data created successfully")
        
    except Exception as e:
        logger.error(f"❌ Error creating default data: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data()
    
    print("🚀 تشغيل خادم اختبار شاشة المبيعات")
    print("📍 http://localhost:5000/sales")
    print("👤 admin / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
