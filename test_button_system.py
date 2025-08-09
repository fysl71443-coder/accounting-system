#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Button System Test
اختبار شامل لنظام الأزرار
"""

import requests
import json
import time
from datetime import datetime

class ButtonSystemTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def login(self, username="admin", password="admin123"):
        """Login to the system"""
        print("🔐 Logging in to the system...")
        
        # Get login page first to get any CSRF tokens
        login_page = self.session.get(f"{self.base_url}/login")
        
        # Login
        login_data = {
            'username': username,
            'password': password,
            'language': 'ar'
        }
        
        response = self.session.post(f"{self.base_url}/login", data=login_data)
        
        if response.status_code == 200 and 'dashboard' in response.url:
            print("✅ Login successful")
            return True
        else:
            print("❌ Login failed")
            return False
    
    def test_api_endpoint(self, method, endpoint, data=None, description=""):
        """Test an API endpoint"""
        print(f"🧪 Testing: {description}")
        print(f"   {method} {endpoint}")
        
        try:
            if method == "GET":
                response = self.session.get(f"{self.base_url}{endpoint}")
            elif method == "POST":
                response = self.session.post(
                    f"{self.base_url}{endpoint}", 
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
            elif method == "PUT":
                response = self.session.put(
                    f"{self.base_url}{endpoint}", 
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
            elif method == "DELETE":
                response = self.session.delete(f"{self.base_url}{endpoint}")
            
            result = {
                'endpoint': endpoint,
                'method': method,
                'description': description,
                'status_code': response.status_code,
                'success': False,
                'response_data': None,
                'error': None
            }
            
            if response.status_code == 200:
                try:
                    result['response_data'] = response.json()
                    result['success'] = result['response_data'].get('success', False)
                    print(f"   ✅ Status: {response.status_code}")
                    if result['success']:
                        print(f"   ✅ API Response: Success")
                    else:
                        print(f"   ⚠️ API Response: {result['response_data'].get('message', 'Unknown error')}")
                except:
                    result['success'] = True  # Non-JSON response but 200 status
                    print(f"   ✅ Status: {response.status_code} (Non-JSON response)")
            else:
                result['error'] = f"HTTP {response.status_code}"
                print(f"   ❌ Status: {response.status_code}")
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            result = {
                'endpoint': endpoint,
                'method': method,
                'description': description,
                'status_code': 0,
                'success': False,
                'response_data': None,
                'error': str(e)
            }
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(result)
            return result
    
    def test_sales_buttons(self):
        """Test all sales button endpoints"""
        print("\n" + "="*60)
        print("🛒 TESTING SALES BUTTON SYSTEM")
        print("="*60)
        
        # Test Save Record
        save_data = {
            'invoice_number': f'INV-{int(time.time())}',
            'customer_name': 'Test Customer',
            'total_amount': 100.00,
            'tax_amount': 15.00,
            'final_amount': 115.00,
            'payment_method': 'cash',
            'payment_status': 'pending',
            'notes': 'Test invoice created by button system test'
        }
        
        save_result = self.test_api_endpoint(
            "POST", "/api/sales/save", save_data,
            "Sales - Save Record Button"
        )
        
        # If save was successful, get the ID for other tests
        record_id = None
        if save_result['success'] and save_result['response_data']:
            record_id = save_result['response_data'].get('id')
        
        if record_id:
            # Test Edit Record
            edit_data = {
                'customer_name': 'Updated Test Customer',
                'total_amount': 150.00,
                'notes': 'Updated by button system test'
            }
            self.test_api_endpoint(
                "PUT", f"/api/sales/edit/{record_id}", edit_data,
                "Sales - Edit Record Button"
            )
            
            # Test Preview Record
            self.test_api_endpoint(
                "GET", f"/api/sales/preview/{record_id}", None,
                "Sales - Preview Record Button"
            )
            
            # Test Print Record
            self.test_api_endpoint(
                "GET", f"/api/sales/print/{record_id}", None,
                "Sales - Print Record Button"
            )
            
            # Test Register Payment
            payment_data = {
                'invoice_id': record_id,
                'amount_paid': 115.00,
                'payment_method': 'cash',
                'payment_date': datetime.now().strftime('%Y-%m-%d'),
                'notes': 'Test payment'
            }
            self.test_api_endpoint(
                "POST", "/api/sales/register_payment", payment_data,
                "Sales - Register Payment Button"
            )
            
            # Test Delete Record (last, as it removes the record)
            self.test_api_endpoint(
                "DELETE", f"/api/sales/delete/{record_id}", None,
                "Sales - Delete Record Button"
            )
        
        # Test Select Invoice
        self.test_api_endpoint(
            "GET", "/api/sales/select_invoice", None,
            "Sales - Select Invoice Button"
        )
    
    def test_products_buttons(self):
        """Test all products button endpoints"""
        print("\n" + "="*60)
        print("📦 TESTING PRODUCTS BUTTON SYSTEM")
        print("="*60)
        
        # Test Save Product
        product_data = {
            'product_code': f'PROD-{int(time.time())}',
            'product_name': 'Test Product',
            'description': 'Test product created by button system test',
            'unit_cost': 50.00,
            'selling_price': 75.00,
            'category': 'Test Category',
            'unit_type': 'قطعة',
            'min_stock_level': 10,
            'current_stock': 100
        }
        
        save_result = self.test_api_endpoint(
            "POST", "/api/products/save", product_data,
            "Products - Save Record Button"
        )
        
        # Get product ID for other tests
        product_id = None
        if save_result['success'] and save_result['response_data']:
            product_id = save_result['response_data'].get('id')
        
        if product_id:
            # Test Edit Product
            edit_data = {
                'product_name': 'Updated Test Product',
                'selling_price': 80.00,
                'current_stock': 150
            }
            self.test_api_endpoint(
                "PUT", f"/api/products/edit/{product_id}", edit_data,
                "Products - Edit Record Button"
            )
            
            # Test Print Product
            self.test_api_endpoint(
                "GET", f"/api/products/print/{product_id}", None,
                "Products - Print Record Button"
            )
            
            # Test Delete Product
            self.test_api_endpoint(
                "DELETE", f"/api/products/delete/{product_id}", None,
                "Products - Delete Record Button"
            )
        
        # Test Search Products
        self.test_api_endpoint(
            "GET", "/api/products/search?q=Test", None,
            "Products - Search Records Button"
        )
    
    def test_reports_buttons(self):
        """Test all reports button endpoints"""
        print("\n" + "="*60)
        print("📊 TESTING REPORTS BUTTON SYSTEM")
        print("="*60)
        
        # Test Preview Report
        report_data = {
            'report_type': 'sales_summary',
            'date_from': '2024-01-01',
            'date_to': '2024-12-31'
        }
        
        self.test_api_endpoint(
            "POST", "/api/reports/preview", report_data,
            "Reports - Preview Report Button"
        )
        
        # Test Print Report
        self.test_api_endpoint(
            "POST", "/api/reports/print", report_data,
            "Reports - Print Report Button"
        )
        
        # Test Export Report
        export_data = {
            **report_data,
            'format': 'excel'
        }
        self.test_api_endpoint(
            "POST", "/api/reports/export", export_data,
            "Reports - Export Report Button"
        )
    
    def test_general_endpoints(self):
        """Test general endpoints for other screens"""
        print("\n" + "="*60)
        print("🔧 TESTING GENERAL BUTTON ENDPOINTS")
        print("="*60)
        
        screens = ['purchases', 'employees', 'taxes', 'expenses', 'suppliers', 'customers']
        
        for screen in screens:
            # Test Save
            self.test_api_endpoint(
                "POST", f"/api/{screen}/save", {'test': 'data'},
                f"{screen.title()} - Save Record Button"
            )
            
            # Test Edit
            self.test_api_endpoint(
                "PUT", f"/api/{screen}/edit/1", {'test': 'data'},
                f"{screen.title()} - Edit Record Button"
            )
            
            # Test Delete
            self.test_api_endpoint(
                "DELETE", f"/api/{screen}/delete/1", None,
                f"{screen.title()} - Delete Record Button"
            )
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*80)
        print("📋 BUTTON SYSTEM TEST REPORT")
        print("="*80)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - successful_tests
        
        print(f"📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Successful: {successful_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📈 Success Rate: {(successful_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['description']}")
                    print(f"     {result['method']} {result['endpoint']}")
                    print(f"     Error: {result['error'] or 'API returned success=false'}")
        
        print(f"\n✅ Successful Tests:")
        for result in self.test_results:
            if result['success']:
                print(f"   • {result['description']}")
        
        # Save detailed report
        with open('button_system_test_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'failed_tests': failed_tests,
                    'success_rate': successful_tests/total_tests*100
                },
                'results': self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: button_system_test_report.json")

def main():
    """Run comprehensive button system test"""
    print("🚀 Starting Comprehensive Button System Test")
    print("=" * 80)
    
    tester = ButtonSystemTester()
    
    # Login first
    if not tester.login():
        print("❌ Cannot proceed without login")
        return
    
    # Run all tests
    tester.test_sales_buttons()
    tester.test_products_buttons()
    tester.test_reports_buttons()
    tester.test_general_endpoints()
    
    # Generate report
    tester.generate_report()
    
    print("\n🎉 Button System Test Completed!")
    print("=" * 80)

if __name__ == "__main__":
    main()
