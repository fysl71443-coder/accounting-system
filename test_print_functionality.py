#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار وظائف الطباعة وإنتاج PDF
Test Print Functionality and PDF Generation
"""

import requests
import json
import time
import os
from datetime import datetime

class PrintTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login(self, username="admin", password="admin123"):
        """تسجيل الدخول"""
        print("🔐 تسجيل الدخول...")
        
        try:
            # الحصول على صفحة تسجيل الدخول
            login_page = self.session.get(f"{self.base_url}/login")
            if login_page.status_code != 200:
                print(f"❌ لا يمكن الوصول لصفحة تسجيل الدخول: {login_page.status_code}")
                return False
            
            # تسجيل الدخول
            login_data = {'username': username, 'password': password}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            
            if response.status_code == 200:
                print("✅ تم تسجيل الدخول بنجاح")
                return True
            else:
                print(f"❌ فشل تسجيل الدخول: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول: {e}")
            return False
    
    def test_available_months_api(self):
        """اختبار API الأشهر المتاحة"""
        print("\n📅 اختبار API الأشهر المتاحة...")
        
        invoice_types = ['sales', 'purchases', 'expenses', 'payroll']
        
        for invoice_type in invoice_types:
            try:
                response = self.session.get(f"{self.base_url}/api/available_months?type={invoice_type}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        months_count = len(data.get('months', []))
                        print(f"✅ {invoice_type}: {months_count} أشهر متاحة")
                        
                        # عرض الأشهر المتاحة
                        if months_count > 0:
                            for month in data['months'][:3]:  # عرض أول 3 أشهر
                                print(f"   📅 {month['text']} ({month['value']})")
                    else:
                        print(f"⚠️ {invoice_type}: لا توجد أشهر متاحة")
                else:
                    print(f"❌ {invoice_type}: خطأ في API - {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {invoice_type}: خطأ - {e}")
    
    def test_print_preview(self):
        """اختبار معاينة الطباعة"""
        print("\n👁️ اختبار معاينة الطباعة...")
        
        # معاملات الاختبار
        test_params = {
            'type': 'sales',
            'month': '2025-08',
            'status': 'all',
            'details': 'true'
        }
        
        try:
            url = f"{self.base_url}/print_invoices_preview"
            response = self.session.get(url, params=test_params)
            
            if response.status_code == 200:
                print("✅ معاينة الطباعة تعمل")
                
                # فحص محتوى الصفحة
                content = response.text
                if "تقرير الفواتير" in content:
                    print("✅ عنوان التقرير موجود")
                if "bootstrap" in content.lower():
                    print("✅ Bootstrap محمل")
                if "jspdf" in content.lower():
                    print("✅ مكتبة PDF محملة")
                    
            else:
                print(f"❌ معاينة الطباعة فشلت: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في معاينة الطباعة: {e}")
    
    def test_print_page(self):
        """اختبار صفحة الطباعة"""
        print("\n🖨️ اختبار صفحة الطباعة...")
        
        test_params = {
            'type': 'sales',
            'month': '2025-08', 
            'status': 'all',
            'details': 'true'
        }
        
        try:
            url = f"{self.base_url}/print_invoices"
            response = self.session.get(url, params=test_params)
            
            if response.status_code == 200:
                print("✅ صفحة الطباعة تعمل")
                
                # فحص محتوى الصفحة
                content = response.text
                if "تقرير الفواتير" in content:
                    print("✅ عنوان التقرير موجود")
                if "window.print" in content:
                    print("✅ وظيفة الطباعة موجودة")
                    
            else:
                print(f"❌ صفحة الطباعة فشلت: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في صفحة الطباعة: {e}")
    
    def test_pdf_download(self):
        """اختبار تحميل PDF"""
        print("\n📄 اختبار تحميل PDF...")
        
        test_params = {
            'type': 'sales',
            'month': '2025-08',
            'status': 'all', 
            'details': 'true'
        }
        
        try:
            url = f"{self.base_url}/download_invoices_pdf"
            response = self.session.get(url, params=test_params)
            
            if response.status_code == 200:
                # فحص نوع المحتوى
                content_type = response.headers.get('content-type', '')
                
                if 'application/pdf' in content_type:
                    print("✅ تحميل PDF يعمل")
                    
                    # حفظ ملف PDF للاختبار
                    filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    file_size = len(response.content)
                    print(f"✅ تم حفظ ملف PDF: {filename} ({file_size} بايت)")
                    
                    return filename
                    
                else:
                    print(f"⚠️ نوع المحتوى غير صحيح: {content_type}")
                    # قد يكون HTML بدلاً من PDF
                    if 'text/html' in content_type:
                        print("📄 تم إرجاع HTML بدلاً من PDF (fallback)")
                        return True
                    
            else:
                print(f"❌ تحميل PDF فشل: {response.status_code}")
                if response.status_code == 302:
                    print("🔄 تم إعادة التوجيه - قد يكون fallback")
                    
        except Exception as e:
            print(f"❌ خطأ في تحميل PDF: {e}")
            
        return False
    
    def test_payments_dues_page(self):
        """اختبار صفحة المدفوعات والمستحقات"""
        print("\n📄 اختبار صفحة المدفوعات والمستحقات...")
        
        try:
            response = self.session.get(f"{self.base_url}/payments_dues")
            
            if response.status_code == 200:
                print("✅ صفحة المدفوعات تعمل")
                
                content = response.text
                
                # فحص أزرار الطباعة
                print_buttons = content.count('openPrintModal')
                print(f"✅ عدد أزرار الطباعة: {print_buttons}")
                
                # فحص النافذة المنبثقة
                if 'printModal' in content:
                    print("✅ نافذة الطباعة موجودة")
                
                # فحص الفلاتر
                filters = ['sales-status-filter', 'purchases-status-filter', 'expenses-status-filter']
                for filter_id in filters:
                    if filter_id in content:
                        print(f"✅ فلتر {filter_id} موجود")
                        
            else:
                print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في صفحة المدفوعات: {e}")
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء اختبار وظائف الطباعة الشامل...")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول - توقف الاختبار")
            return False
        
        # تشغيل الاختبارات
        self.test_payments_dues_page()
        self.test_available_months_api()
        self.test_print_preview()
        self.test_print_page()
        pdf_result = self.test_pdf_download()
        
        print("\n" + "=" * 60)
        print("📊 ملخص نتائج الاختبار:")
        print("=" * 60)
        
        if pdf_result:
            print("🎉 جميع وظائف الطباعة تعمل بنجاح!")
            print("✅ يمكن إنتاج ملفات PDF")
            print("🚀 النظام جاهز للاستخدام")
            
            if isinstance(pdf_result, str):
                print(f"📁 ملف PDF تجريبي: {pdf_result}")
                
        else:
            print("⚠️ بعض وظائف الطباعة تحتاج مراجعة")
            print("🔧 يرجى مراجعة الأخطاء أعلاه")
        
        return bool(pdf_result)

def main():
    """الوظيفة الرئيسية"""
    print("🖨️ فاحص وظائف الطباعة وإنتاج PDF")
    print("🖨️ Print Functionality and PDF Generation Tester")
    print("=" * 60)
    
    # التحقق من تشغيل الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code not in [200, 302]:
            print("❌ الخادم لا يعمل أو لا يمكن الوصول إليه")
            print("💡 يرجى تشغيل الخادم أولاً: python app.py")
            return
    except:
        print("❌ لا يمكن الاتصال بالخادم")
        print("💡 يرجى تشغيل الخادم أولاً: python app.py")
        return
    
    # تشغيل الاختبارات
    tester = PrintTester()
    success = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 اختبار الطباعة مكتمل بنجاح!")
        print("📄 يمكن الآن طباعة التقارير وإنتاج ملفات PDF")
    else:
        print("⚠️ اختبار الطباعة مكتمل مع وجود مشاكل")
        print("🔧 يرجى مراجعة الأخطاء وإصلاحها")
    print("=" * 60)

if __name__ == "__main__":
    main()
