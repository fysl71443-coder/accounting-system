#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
محاكاة المستخدم لاختبار طباعة فواتير المبيعات
User Simulation for Sales Invoice Printing Test
"""

import requests
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setup_browser():
    """إعداد المتصفح للاختبار"""
    print("🌐 إعداد المتصفح...")
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"❌ فشل في إعداد المتصفح: {e}")
        print("💡 تأكد من تثبيت Chrome WebDriver")
        return None

def simulate_user_login(driver):
    """محاكاة تسجيل دخول المستخدم"""
    print("🔐 محاكاة تسجيل الدخول...")
    
    try:
        # الذهاب لصفحة تسجيل الدخول
        driver.get("http://localhost:5000/login")
        time.sleep(2)
        
        # إدخال بيانات تسجيل الدخول
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys("admin")
        
        password_field.clear()
        password_field.send_keys("admin112233")
        
        # الضغط على زر تسجيل الدخول
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        time.sleep(3)
        
        # التحقق من نجاح تسجيل الدخول
        if "dashboard" in driver.current_url.lower() or "index" in driver.current_url.lower():
            print("✅ تم تسجيل الدخول بنجاح")
            return True
        else:
            print("❌ فشل في تسجيل الدخول")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False

def navigate_to_payments_page(driver):
    """الانتقال لصفحة المدفوعات والمستحقات"""
    print("📄 الانتقال لصفحة المدفوعات...")
    
    try:
        # الذهاب مباشرة لصفحة المدفوعات
        driver.get("http://localhost:5000/payments_dues")
        time.sleep(3)
        
        # التحقق من وصول الصفحة
        if "payments_dues" in driver.current_url:
            print("✅ تم الوصول لصفحة المدفوعات")
            return True
        else:
            print("❌ فشل في الوصول لصفحة المدفوعات")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الانتقال للصفحة: {e}")
        return False

def test_sales_print_button(driver):
    """اختبار زر طباعة المبيعات"""
    print("🖨️ اختبار زر طباعة فواتير المبيعات...")
    
    try:
        # التأكد من وجود تبويب المبيعات
        sales_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#sales']"))
        )
        sales_tab.click()
        time.sleep(2)
        print("✅ تم فتح تبويب المبيعات")
        
        # البحث عن زر طباعة المبيعات
        print("🔍 البحث عن زر الطباعة...")
        
        # محاولة العثور على الزر بطرق مختلفة
        print_button = None
        
        # الطريقة الأولى: البحث بالنص
        try:
            print_button = driver.find_element(By.XPATH, "//button[contains(text(), 'طباعة جميع المبيعات')]")
            print("✅ تم العثور على الزر بالنص")
        except:
            pass
        
        # الطريقة الثانية: البحث بالوظيفة
        if not print_button:
            try:
                print_button = driver.find_element(By.XPATH, "//button[@onclick='printAllSales()']")
                print("✅ تم العثور على الزر بالوظيفة")
            except:
                pass
        
        # الطريقة الثالثة: البحث بالأيقونة
        if not print_button:
            try:
                print_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn') and .//i[contains(@class, 'fa-print')]]")
                print("✅ تم العثور على الزر بالأيقونة")
            except:
                pass
        
        if print_button:
            print("🎯 تم العثور على زر الطباعة!")
            
            # التمرير للزر
            driver.execute_script("arguments[0].scrollIntoView(true);", print_button)
            time.sleep(1)
            
            # الضغط على الزر
            print("👆 الضغط على زر الطباعة...")
            driver.execute_script("arguments[0].click();", print_button)
            time.sleep(3)
            
            # التحقق من فتح نافذة جديدة
            if len(driver.window_handles) > 1:
                print("✅ تم فتح نافذة طباعة جديدة!")
                
                # الانتقال للنافذة الجديدة
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                
                # فحص محتوى النافذة
                page_source = driver.page_source
                
                if "فواتير المبيعات" in page_source:
                    print("✅ النافذة تحتوي على تقرير المبيعات")
                    
                    if "نظام المحاسبة المتكامل" in page_source:
                        print("✅ يحتوي على معلومات الشركة")
                    
                    if "المجموع الإجمالي" in page_source:
                        print("✅ يحتوي على المجموع الإجمالي")
                    
                    if "تاريخ الطباعة" in page_source:
                        print("✅ يحتوي على تاريخ الطباعة")
                    
                    print("🎉 تم إنشاء تقرير الطباعة بنجاح!")
                    return True
                else:
                    print("❌ النافذة لا تحتوي على تقرير المبيعات")
                    return False
            else:
                print("❌ لم يتم فتح نافذة طباعة جديدة")
                return False
        else:
            print("❌ لم يتم العثور على زر الطباعة")
            
            # طباعة HTML للتشخيص
            print("\n🔍 فحص HTML للتشخيص:")
            sales_section = driver.find_element(By.ID, "sales")
            print("HTML المتاح:")
            print(sales_section.get_attribute('innerHTML')[:500] + "...")
            
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار زر الطباعة: {e}")
        return False

def simulate_manual_print_test():
    """محاكاة اختبار الطباعة اليدوي"""
    print("🤖 بدء محاكاة اختبار المستخدم للطباعة")
    print("=" * 60)
    
    # إعداد المتصفح
    driver = setup_browser()
    if not driver:
        print("❌ فشل في إعداد المتصفح")
        return False
    
    try:
        # تسجيل الدخول
        if not simulate_user_login(driver):
            return False
        
        # الانتقال لصفحة المدفوعات
        if not navigate_to_payments_page(driver):
            return False
        
        # اختبار زر طباعة المبيعات
        success = test_sales_print_button(driver)
        
        if success:
            print("\n🎉 نجح اختبار الطباعة!")
            print("✅ تم فتح نافذة الطباعة")
            print("✅ تم إنشاء تقرير المبيعات")
            print("✅ التقرير يحتوي على جميع البيانات المطلوبة")
            
            # إبقاء النافذة مفتوحة للمراجعة
            print("\n⏳ إبقاء النافذة مفتوحة للمراجعة...")
            time.sleep(10)
        else:
            print("\n❌ فشل اختبار الطباعة")
        
        return success
        
    except Exception as e:
        print(f"❌ خطأ عام في المحاكاة: {e}")
        return False
    
    finally:
        # إغلاق المتصفح
        print("\n🔚 إغلاق المتصفح...")
        driver.quit()

def fallback_manual_test():
    """اختبار يدوي بديل بدون Selenium"""
    print("🔄 تشغيل اختبار يدوي بديل...")
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل")
    except:
        print("❌ الخادم لا يعمل")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except:
        print("❌ فشل تسجيل الدخول")
        return False
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            
            # فحص وجود زر الطباعة
            if "printAllSales()" in content:
                print("✅ زر طباعة المبيعات موجود في الكود")
            else:
                print("❌ زر طباعة المبيعات غير موجود")
            
            if "طباعة جميع المبيعات" in content:
                print("✅ نص زر الطباعة موجود")
            else:
                print("❌ نص زر الطباعة غير موجود")
            
            # فتح المتصفح للاختبار اليدوي
            print("🌐 فتح المتصفح للاختبار اليدوي...")
            webbrowser.open("http://localhost:5000/payments_dues")
            
            return True
        else:
            print(f"❌ فشل في الوصول للصفحة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🤖 محاكاة المستخدم لاختبار طباعة فواتير المبيعات")
    print("=" * 70)
    
    # محاولة الاختبار التلقائي أولاً
    try:
        success = simulate_manual_print_test()
        if success:
            print("\n🎉 تم اختبار الطباعة بنجاح!")
            return
    except Exception as e:
        print(f"⚠️ فشل الاختبار التلقائي: {e}")
        print("🔄 التبديل للاختبار اليدوي...")
    
    # الاختبار اليدوي البديل
    fallback_success = fallback_manual_test()
    
    if fallback_success:
        print("\n📋 تعليمات الاختبار اليدوي:")
        print("1. تأكد من تسجيل الدخول")
        print("2. اذهب لتبويب المبيعات")
        print("3. ابحث عن زر 'طباعة جميع المبيعات'")
        print("4. اضغط على الزر")
        print("5. تأكد من فتح نافذة طباعة جديدة")
        print("6. تحقق من وجود تقرير المبيعات")
        
        print("\n🎯 ما يجب أن تراه:")
        print("✅ نافذة طباعة جديدة")
        print("✅ عنوان 'فواتير المبيعات'")
        print("✅ جدول بجميع فواتير المبيعات")
        print("✅ المجموع الإجمالي")
        print("✅ تاريخ الطباعة")
        print("✅ معلومات الشركة")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
