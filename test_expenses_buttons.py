#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار أزرار شاشة المصروفات
Test Expenses Screen Buttons
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class ExpensesButtonsTest:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.driver = None
        
    def setup_driver(self):
        """إعداد متصفح Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"❌ فشل في إعداد المتصفح: {e}")
            return False
    
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {'username': 'admin', 'password': 'admin123'}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def test_buttons_exist(self):
        """اختبار وجود الأزرار"""
        print("🔍 اختبار وجود الأزرار في شاشة المصروفات:")
        
        if not self.setup_driver():
            return False
            
        try:
            # تسجيل الدخول في المتصفح
            self.driver.get(f"{self.base_url}/login")
            
            # ملء نموذج تسجيل الدخول
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys("admin")
            password_field.send_keys("admin123")
            
            # النقر على زر تسجيل الدخول
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # انتظار تحميل الصفحة الرئيسية
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # الانتقال إلى صفحة المصروفات
            self.driver.get(f"{self.base_url}/expenses")
            
            # انتظار تحميل الصفحة
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # اختبار وجود الأزرار
            buttons_to_test = [
                ("إضافة مصروف جديد", "showAddExpenseModal()"),
                ("تعديل", "EditExpensesRecord()"),
                ("حذف", "DeleteExpensesRecord()"),
                ("تصدير", "exportExpenses()"),
                ("طباعة", "printExpensesList()")
            ]
            
            found_buttons = 0
            
            for button_text, onclick_function in buttons_to_test:
                try:
                    # البحث عن الزر بالنص أو بالوظيفة
                    button = None
                    
                    # البحث بالنص
                    buttons_by_text = self.driver.find_elements(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                    if buttons_by_text:
                        button = buttons_by_text[0]
                    else:
                        # البحث بالوظيفة onclick
                        buttons_by_onclick = self.driver.find_elements(By.XPATH, f"//button[contains(@onclick, '{onclick_function}')]")
                        if buttons_by_onclick:
                            button = buttons_by_onclick[0]
                    
                    if button:
                        print(f"  ✅ زر '{button_text}' موجود")
                        found_buttons += 1
                        
                        # اختبار إمكانية النقر
                        if button.is_enabled():
                            print(f"    ✅ الزر قابل للنقر")
                        else:
                            print(f"    ⚠️ الزر غير قابل للنقر")
                    else:
                        print(f"  ❌ زر '{button_text}' غير موجود")
                        
                except Exception as e:
                    print(f"  ❌ خطأ في اختبار زر '{button_text}': {e}")
            
            print(f"\n📊 النتيجة: {found_buttons}/{len(buttons_to_test)} أزرار موجودة")
            
            return found_buttons == len(buttons_to_test)
            
        except Exception as e:
            print(f"❌ خطأ في اختبار الأزرار: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def test_add_button_functionality(self):
        """اختبار وظيفة زر الإضافة"""
        print("\n🧪 اختبار وظيفة زر الإضافة:")
        
        if not self.setup_driver():
            return False
            
        try:
            # تسجيل الدخول والانتقال للصفحة
            self.driver.get(f"{self.base_url}/login")
            
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys("admin")
            password_field.send_keys("admin123")
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.driver.get(f"{self.base_url}/expenses")
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # البحث عن زر الإضافة والنقر عليه
            add_button = self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'showAddExpenseModal')]")
            add_button.click()
            
            # انتظار ظهور النموذج
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "expenseModal"))
            )
            
            # التحقق من ظهور النموذج
            modal = self.driver.find_element(By.ID, "expenseModal")
            if modal.is_displayed():
                print("  ✅ تم فتح نموذج إضافة المصروف بنجاح")
                return True
            else:
                print("  ❌ النموذج غير ظاهر")
                return False
                
        except Exception as e:
            print(f"  ❌ خطأ في اختبار زر الإضافة: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🧪 اختبار شامل لأزرار شاشة المصروفات")
        print("=" * 60)
        
        tests = [
            ("اختبار وجود الأزرار", self.test_buttons_exist),
            ("اختبار وظيفة زر الإضافة", self.test_add_button_functionality)
        ]
        
        passed_tests = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed_tests += 1
                    print(f"✅ {test_name} - نجح")
                else:
                    print(f"❌ {test_name} - فشل")
            except Exception as e:
                print(f"❌ {test_name} - خطأ: {e}")
            
            print("-" * 40)
        
        # النتائج النهائية
        print("=" * 60)
        print("📊 نتائج اختبار أزرار المصروفات:")
        print("=" * 60)
        
        success_rate = (passed_tests / len(tests) * 100) if len(tests) > 0 else 0
        
        print(f"📈 نسبة النجاح: {success_rate:.1f}%")
        print(f"✅ اختبارات ناجحة: {passed_tests}/{len(tests)}")
        
        if success_rate == 100:
            print("🎉 ممتاز! جميع أزرار المصروفات تعمل بشكل صحيح")
        elif success_rate >= 80:
            print("🟢 جيد - معظم الأزرار تعمل")
        else:
            print("🔴 يحتاج إصلاح - بعض الأزرار لا تعمل")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = ExpensesButtonsTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 أزرار شاشة المصروفات تعمل بشكل صحيح!")
    else:
        print("\n⚠️ بعض أزرار المصروفات تحتاج إصلاح")
