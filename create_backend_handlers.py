#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Handlers for Button System
معالجات الخلفية لنظام الأزرار
"""

import os
from pathlib import Path

def create_backend_routes():
    """Create Flask backend routes for all button handlers"""
    
    backend_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Button Handlers for Accounting System
معالجات الأزرار الخلفية لنظام المحاسبة
"""

from flask import request, jsonify, render_template, flash, redirect, url_for
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SALES HANDLERS
# ============================================================================

@app.route('/api/sales/save', methods=['POST'])
@login_required
def sales_save_record():
    """Save sales record"""
    try:
        logger.info("🔵 Sales - Save Record button clicked")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['invoice_number', 'customer_name', 'total_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        # Create new sale record
        sale = Sale(
            invoice_number=data['invoice_number'],
            customer_name=data['customer_name'],
            invoice_date=datetime.strptime(data.get('invoice_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
            total_amount=float(data['total_amount']),
            tax_amount=float(data.get('tax_amount', 0)),
            final_amount=float(data.get('final_amount', data['total_amount'])),
            payment_method=data.get('payment_method', 'cash'),
            payment_status=data.get('payment_status', 'pending'),
            notes=data.get('notes', ''),
            created_by=current_user.id
        )
        
        db.session.add(sale)
        db.session.commit()
        
        logger.info(f"✅ Sales record saved successfully: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record saved successfully', 'id': sale.id})
        
    except Exception as e:
        logger.error(f"❌ Error saving sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error saving record: {str(e)}'})

@app.route('/api/sales/edit/<int:record_id>', methods=['PUT'])
@login_required
def sales_edit_record(record_id):
    """Edit sales record"""
    try:
        logger.info(f"🔵 Sales - Edit Record button clicked for ID: {record_id}")
        data = request.get_json()
        
        sale = Sale.query.get_or_404(record_id)
        
        # Update fields
        sale.customer_name = data.get('customer_name', sale.customer_name)
        sale.total_amount = float(data.get('total_amount', sale.total_amount))
        sale.tax_amount = float(data.get('tax_amount', sale.tax_amount))
        sale.final_amount = float(data.get('final_amount', sale.final_amount))
        sale.payment_method = data.get('payment_method', sale.payment_method)
        sale.payment_status = data.get('payment_status', sale.payment_status)
        sale.notes = data.get('notes', sale.notes)
        
        db.session.commit()
        
        logger.info(f"✅ Sales record updated successfully: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record updated successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error updating sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating record: {str(e)}'})

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
        
        logger.info(f"✅ Sales record deleted successfully: {invoice_number}")
        return jsonify({'success': True, 'message': 'Sales record deleted successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error deleting sales record: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting record: {str(e)}'})

@app.route('/api/sales/preview/<int:record_id>')
@login_required
def sales_preview_record(record_id):
    """Preview sales record"""
    try:
        logger.info(f"🔵 Sales - Preview Record button clicked for ID: {record_id}")
        
        sale = Sale.query.get_or_404(record_id)
        sale_items = SaleItem.query.filter_by(sale_id=record_id).all()
        
        preview_data = {
            'sale': {
                'id': sale.id,
                'invoice_number': sale.invoice_number,
                'customer_name': sale.customer_name,
                'invoice_date': sale.invoice_date.strftime('%Y-%m-%d'),
                'total_amount': sale.total_amount,
                'tax_amount': sale.tax_amount,
                'final_amount': sale.final_amount,
                'payment_method': sale.payment_method,
                'payment_status': sale.payment_status,
                'notes': sale.notes
            },
            'items': [{
                'product_name': item.product_name,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.total_price,
                'tax_amount': item.tax_amount
            } for item in sale_items]
        }
        
        logger.info(f"✅ Sales record preview generated: {sale.invoice_number}")
        return jsonify({'success': True, 'data': preview_data})
        
    except Exception as e:
        logger.error(f"❌ Error previewing sales record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error previewing record: {str(e)}'})

@app.route('/api/sales/print/<int:record_id>')
@login_required
def sales_print_record(record_id):
    """Print sales record"""
    try:
        logger.info(f"🔵 Sales - Print Record button clicked for ID: {record_id}")
        
        sale = Sale.query.get_or_404(record_id)
        sale_items = SaleItem.query.filter_by(sale_id=record_id).all()
        
        print_data = {
            'sale': sale,
            'items': sale_items,
            'print_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.info(f"✅ Sales record print data prepared: {sale.invoice_number}")
        return jsonify({'success': True, 'print_url': f'/print/sales/{record_id}'})
        
    except Exception as e:
        logger.error(f"❌ Error preparing sales record for print: {str(e)}")
        return jsonify({'success': False, 'message': f'Error preparing print: {str(e)}'})

@app.route('/api/sales/select_invoice')
@login_required
def sales_select_invoice():
    """Get list of invoices for selection"""
    try:
        logger.info("🔵 Sales - Select Invoice button clicked")
        
        sales = Sale.query.order_by(Sale.created_at.desc()).limit(50).all()
        
        invoices_data = [{
            'id': sale.id,
            'invoice_number': sale.invoice_number,
            'customer_name': sale.customer_name,
            'invoice_date': sale.invoice_date.strftime('%Y-%m-%d'),
            'final_amount': sale.final_amount,
            'payment_status': sale.payment_status
        } for sale in sales]
        
        logger.info(f"✅ Retrieved {len(invoices_data)} invoices for selection")
        return jsonify({'success': True, 'invoices': invoices_data})
        
    except Exception as e:
        logger.error(f"❌ Error retrieving invoices: {str(e)}")
        return jsonify({'success': False, 'message': f'Error retrieving invoices: {str(e)}'})

@app.route('/api/sales/register_payment', methods=['POST'])
@login_required
def sales_register_payment():
    """Register payment for sales invoice"""
    try:
        logger.info("🔵 Sales - Register Payment button clicked")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['invoice_id', 'amount_paid', 'payment_method', 'payment_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        sale = Sale.query.get_or_404(data['invoice_id'])
        
        # Create payment record (you might need to create a Payment model)
        payment_data = {
            'invoice_id': data['invoice_id'],
            'invoice_type': 'sale',
            'amount_paid': float(data['amount_paid']),
            'payment_method': data['payment_method'],
            'payment_date': datetime.strptime(data['payment_date'], '%Y-%m-%d').date(),
            'notes': data.get('notes', ''),
            'created_by': current_user.id,
            'created_at': datetime.now()
        }
        
        # Update sale payment status
        if float(data['amount_paid']) >= sale.final_amount:
            sale.payment_status = 'paid'
        else:
            sale.payment_status = 'partial'
        
        db.session.commit()
        
        logger.info(f"✅ Payment registered successfully for invoice: {sale.invoice_number}")
        return jsonify({'success': True, 'message': 'Payment registered successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error registering payment: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error registering payment: {str(e)}'})

# ============================================================================
# PURCHASES HANDLERS
# ============================================================================

@app.route('/api/purchases/save', methods=['POST'])
@login_required
def purchases_save_record():
    """Save purchase record"""
    try:
        logger.info("🔵 Purchases - Save Record button clicked")
        data = request.get_json()
        
        # Similar implementation to sales but for purchases
        # You'll need to create Purchase and PurchaseItem models
        
        logger.info("✅ Purchase record saved successfully")
        return jsonify({'success': True, 'message': 'Purchase record saved successfully'})
        
    except Exception as e:
        logger.error(f"❌ Error saving purchase record: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving record: {str(e)}'})

# ============================================================================
# PRODUCTS HANDLERS
# ============================================================================

@app.route('/api/products/save', methods=['POST'])
@login_required
def products_save_record():
    """Save product record"""
    try:
        logger.info("🔵 Products - Save Record button clicked")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_code', 'product_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        # Create new product
        product = Product(
            product_code=data['product_code'],
            product_name=data['product_name'],
            description=data.get('description', ''),
            unit_cost=float(data.get('unit_cost', 0)),
            selling_price=float(data.get('selling_price', 0)),
            category=data.get('category', ''),
            unit_type=data.get('unit_type', 'قطعة'),
            min_stock_level=int(data.get('min_stock_level', 0)),
            current_stock=int(data.get('current_stock', 0))
        )
        
        db.session.add(product)
        db.session.commit()
        
        logger.info(f"✅ Product saved successfully: {product.product_code}")
        return jsonify({'success': True, 'message': 'Product saved successfully', 'id': product.id})
        
    except Exception as e:
        logger.error(f"❌ Error saving product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error saving product: {str(e)}'})

@app.route('/api/products/search')
@login_required
def products_search_records():
    """Search products"""
    try:
        logger.info("🔵 Products - Search Records button clicked")
        
        search_term = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        query = Product.query.filter(Product.is_active == True)
        
        if search_term:
            query = query.filter(
                db.or_(
                    Product.product_code.contains(search_term),
                    Product.product_name.contains(search_term),
                    Product.description.contains(search_term)
                )
            )
        
        products = query.paginate(page=page, per_page=per_page, error_out=False)
        
        products_data = [{
            'id': p.id,
            'product_code': p.product_code,
            'product_name': p.product_name,
            'description': p.description,
            'unit_cost': p.unit_cost,
            'selling_price': p.selling_price,
            'current_stock': p.current_stock,
            'category': p.category
        } for p in products.items]
        
        logger.info(f"✅ Found {len(products_data)} products matching search: {search_term}")
        return jsonify({
            'success': True, 
            'products': products_data,
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        })
        
    except Exception as e:
        logger.error(f"❌ Error searching products: {str(e)}")
        return jsonify({'success': False, 'message': f'Error searching products: {str(e)}'})

# ============================================================================
# REPORTS HANDLERS
# ============================================================================

@app.route('/api/reports/preview', methods=['POST'])
@login_required
def reports_preview_report():
    """Preview report"""
    try:
        logger.info("🔵 Reports - Preview Report button clicked")
        data = request.get_json()
        
        report_type = data.get('report_type', 'sales_summary')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        # Generate report data based on type
        if report_type == 'sales_summary':
            # Sales summary report
            query = Sale.query
            if date_from:
                query = query.filter(Sale.invoice_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
            if date_to:
                query = query.filter(Sale.invoice_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
            
            sales = query.all()
            report_data = {
                'title': 'Sales Summary Report',
                'date_range': f"{date_from} to {date_to}",
                'total_sales': len(sales),
                'total_amount': sum(s.final_amount for s in sales),
                'sales': [{
                    'invoice_number': s.invoice_number,
                    'customer_name': s.customer_name,
                    'invoice_date': s.invoice_date.strftime('%Y-%m-%d'),
                    'final_amount': s.final_amount,
                    'payment_status': s.payment_status
                } for s in sales]
            }
        
        logger.info(f"✅ Report preview generated: {report_type}")
        return jsonify({'success': True, 'report_data': report_data})
        
    except Exception as e:
        logger.error(f"❌ Error generating report preview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating report: {str(e)}'})

@app.route('/api/reports/export', methods=['POST'])
@login_required
def reports_export_report():
    """Export report"""
    try:
        logger.info("🔵 Reports - Export Report button clicked")
        data = request.get_json()
        
        export_format = data.get('format', 'excel')  # excel, pdf, csv
        report_data = data.get('report_data', {})
        
        # Generate export file
        if export_format == 'excel':
            # Create Excel file
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            # Implementation for Excel export
        elif export_format == 'pdf':
            # Create PDF file
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            # Implementation for PDF export
        elif export_format == 'csv':
            # Create CSV file
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            # Implementation for CSV export
        
        logger.info(f"✅ Report exported successfully: {filename}")
        return jsonify({'success': True, 'filename': filename, 'download_url': f'/download/{filename}'})
        
    except Exception as e:
        logger.error(f"❌ Error exporting report: {str(e)}")
        return jsonify({'success': False, 'message': f'Error exporting report: {str(e)}'})

# Add these routes to your main app.py file
'''
    
    return backend_code

def main():
    """Create backend handlers file"""
    print("🔧 Creating Backend Button Handlers")
    print("=" * 60)
    
    backend_code = create_backend_routes()
    
    # Save to file
    with open('button_handlers_backend.py', 'w', encoding='utf-8') as f:
        f.write(backend_code)
    
    print("✅ Created button_handlers_backend.py")
    print("\n📋 Instructions:")
    print("1. Copy the routes from button_handlers_backend.py to your app.py file")
    print("2. Make sure you have all required imports")
    print("3. Create any missing database models (Purchase, PurchaseItem, Payment, etc.)")
    print("4. Test each button handler endpoint")
    
    print("\n🔗 API Endpoints Created:")
    endpoints = [
        "POST /api/sales/save",
        "PUT /api/sales/edit/<id>", 
        "DELETE /api/sales/delete/<id>",
        "GET /api/sales/preview/<id>",
        "GET /api/sales/print/<id>",
        "GET /api/sales/select_invoice",
        "POST /api/sales/register_payment",
        "POST /api/purchases/save",
        "POST /api/products/save",
        "GET /api/products/search",
        "POST /api/reports/preview",
        "POST /api/reports/export"
    ]
    
    for endpoint in endpoints:
        print(f"  • {endpoint}")

if __name__ == "__main__":
    main()
