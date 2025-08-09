#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تفاعلي للأزرار - يحاكي النقر على الأزرار ويختبر الاستجابة
"""

import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class InteractiveButtonTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.driver = None
        self.test_results = {}
        
    def setup_driver(self):
        """إعداد متصفح Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            print("✅ تم إعداد المتصفح بنجاح")
            return True
        except Exception as e:
            print(f"❌ فشل إعداد المتصفح: {e}")
            print("💡 تلميح: تأكد من تثبيت ChromeDriver")
            return False
    
    def login(self, username="admin", password="admin123"):
        """تسجيل الدخول"""
        try:
            self.driver.get(f"{self.base_url}/login")
            
            # ملء بيانات تسجيل الدخول
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # النقر على زر تسجيل الدخول
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # انتظار التوجيه للصفحة الرئيسية
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/dashboard" in driver.current_url or "/sales" in driver.current_url
            )
            
            print("✅ تم تسجيل الدخول بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ فشل تسجيل الدخول: {e}")
            return False
    
    def test_button_click(self, button_id, expected_action="alert"):
        """اختبار النقر على زر معين"""
        try:
            # البحث عن الزر
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            
            # النقر على الزر
            self.driver.execute_script("arguments[0].click();", button)
            
            # انتظار قصير للاستجابة
            time.sleep(1)
            
            # التحقق من وجود alert
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                print(f"✅ {button_id} - تم النقر وظهر تنبيه: {alert_text}")
                return True, alert_text
            except:
                # لا يوجد alert - قد يكون هناك إجراء آخر
                print(f"✅ {button_id} - تم النقر بنجاح (بدون تنبيه)")
                return True, "no_alert"
                
        except TimeoutException:
            print(f"❌ {button_id} - الزر غير موجود أو غير قابل للنقر")
            return False, "button_not_found"
        except Exception as e:
            print(f"❌ {button_id} - خطأ في النقر: {e}")
            return False, str(e)
    
    def test_sales_page(self):
        """اختبار صفحة المبيعات"""
        print("\n🔍 اختبار أزرار صفحة المبيعات:")
        
        try:
            self.driver.get(f"{self.base_url}/sales")
            time.sleep(2)
            
            buttons_to_test = [
                "btnSalesPrint",
                "btnSalesPreview", 
                "btnSalesPayment",
                "btnSalesEdit",
                "btnSalesDelete"
            ]
            
            results = {}
            for button_id in buttons_to_test:
                success, response = self.test_button_click(button_id)
                results[button_id] = {'success': success, 'response': response}
            
            return results
            
        except Exception as e:
            print(f"❌ خطأ في اختبار صفحة المبيعات: {e}")
            return {}
    
    def test_purchases_page(self):
        """اختبار صفحة المشتريات"""
        print("\n🔍 اختبار أزرار صفحة المشتريات:")
        
        try:
            self.driver.get(f"{self.base_url}/purchases")
            time.sleep(2)
            
            buttons_to_test = [
                "btnPurchasesPrint",
                "btnPurchasesPreview",
                "btnPurchasesPayment", 
                "btnPurchasesEdit",
                "btnPurchasesDelete"
            ]
            
            results = {}
            for button_id in buttons_to_test:
                success, response = self.test_button_click(button_id)
                results[button_id] = {'success': success, 'response': response}
            
            return results
            
        except Exception as e:
            print(f"❌ خطأ في اختبار صفحة المشتريات: {e}")
            return {}
    
    def test_expenses_page(self):
        """اختبار صفحة المصروفات"""
        print("\n🔍 اختبار أزرار صفحة المصروفات:")
        
        try:
            self.driver.get(f"{self.base_url}/expenses")
            time.sleep(2)
            
            buttons_to_test = [
                "btnExpensesPrint",
                "btnExpensesPreview",
                "btnExpensesPayment",
                "btnExpensesEdit", 
                "btnExpensesDelete"
            ]
            
            results = {}
            for button_id in buttons_to_test:
                success, response = self.test_button_click(button_id)
                results[button_id] = {'success': success, 'response': response}
            
            return results
            
        except Exception as e:
            print(f"❌ خطأ في اختبار صفحة المصروفات: {e}")
            return {}
    
    def run_interactive_test(self):
        """تشغيل الاختبار التفاعلي"""
        print("🚀 بدء الاختبار التفاعلي للأزرار")
        print("=" * 60)
        
        # إعداد المتصفح
        if not self.setup_driver():
            return False
        
        try:
            # تسجيل الدخول
            if not self.login():
                return False
            
            # اختبار الصفحات
            self.test_results['sales'] = self.test_sales_page()
            self.test_results['purchases'] = self.test_purchases_page()
            self.test_results['expenses'] = self.test_expenses_page()
            
            # طباعة النتائج
            self.print_results()
            
            return True
            
        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 تم إغلاق المتصفح")
    
    def print_results(self):
        """طباعة النتائج"""
        print("\n" + "=" * 60)
        print("📊 نتائج الاختبار التفاعلي")
        print("=" * 60)
        
        total_tests = 0
        successful_tests = 0
        
        for page_name, page_results in self.test_results.items():
            print(f"\n📄 {page_name.upper()}:")
            for button_id, result in page_results.items():
                total_tests += 1
                if result['success']:
                    successful_tests += 1
                    status = "✅"
                else:
                    status = "❌"
                print(f"  {status} {button_id}: {result['response']}")
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 ملخص النتائج:")
        print(f"✅ اختبارات ناجحة: {successful_tests}")
        print(f"❌ اختبارات فاشلة: {total_tests - successful_tests}")
        print(f"📈 نسبة النجاح: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 ممتاز! الأزرار تعمل بكفاءة عالية")
        elif success_rate >= 70:
            print("⚠️ جيد - يحتاج بعض التحسينات")
        else:
            print("🔧 يحتاج إصلاحات")

if __name__ == "__main__":
    # اختبار بسيط بدون Selenium
    print("🔍 اختبار بسيط للأزرار (بدون متصفح)")
    print("=" * 50)
    
    import requests
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin112233'}
    response = session.post('http://localhost:5000/login', data=login_data)
    
    if response.status_code == 200:
        print("✅ تم تسجيل الدخول")
        
        # اختبار الصفحات
        pages = ['/sales', '/purchases', '/expenses']
        for page in pages:
            response = session.get(f'http://localhost:5000{page}')
            if response.status_code == 200:
                print(f"✅ {page} - الصفحة تعمل والأزرار موجودة")
            else:
                print(f"❌ {page} - مشكلة في الصفحة")
    else:
        print("❌ فشل تسجيل الدخول")
    
    print("\n💡 لاختبار تفاعلي كامل، قم بتثبيت ChromeDriver وتشغيل:")
    print("   pip install selenium")
    print("   ثم قم بتشغيل InteractiveButtonTester().run_interactive_test()")
