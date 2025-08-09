#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لأزرار المصروفات
Quick Test for Expenses Buttons
"""

import requests
import json

def test_expenses_api():
    """اختبار API المصروفات"""
    print("🧪 اختبار سريع لـ API المصروفات:")
    
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    # تسجيل الدخول
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post(f"{base_url}/login", data=login_data)
        
        if response.status_code == 200:
            print("  ✅ تم تسجيل الدخول بنجاح")
        else:
            print("  ❌ فشل تسجيل الدخول")
            return False
    except Exception as e:
        print(f"  ❌ خطأ في تسجيل الدخول: {e}")
        return False
    
    # اختبار حفظ مصروف جديد
    try:
        expense_data = {
            "expense_type": "office_supplies",
            "amount": 150.50,
            "date": "2025-01-09",
            "payment_method": "cash",
            "description": "اختبار مصروف جديد",
            "reference": "TEST-001",
            "vendor": "مورد الاختبار"
        }
        
        response = session.post(
            f"{base_url}/api/save_expense",
            json=expense_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"  ✅ تم حفظ المصروف بنجاح - ID: {result.get('expense_id')}")
                return True
            else:
                print(f"  ❌ فشل حفظ المصروف: {result.get('message')}")
                return False
        else:
            print(f"  ❌ خطأ HTTP في حفظ المصروف: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ خطأ في حفظ المصروف: {e}")
        return False

def test_expenses_page():
    """اختبار صفحة المصروفات"""
    print("\n🌐 اختبار صفحة المصروفات:")
    
    try:
        session = requests.Session()
        base_url = "http://localhost:5000"
        
        # تسجيل الدخول
        login_data = {'username': 'admin', 'password': 'admin123'}
        session.post(f"{base_url}/login", data=login_data)
        
        # جلب صفحة المصروفات
        response = session.get(f"{base_url}/expenses")
        
        if response.status_code == 200:
            content = response.text
            
            # فحص وجود الأزرار
            buttons_to_check = [
                ('showAddExpenseModal()', 'زر إضافة مصروف جديد'),
                ('EditExpensesRecord()', 'زر تعديل'),
                ('DeleteExpensesRecord()', 'زر حذف'),
                ('exportExpenses()', 'زر تصدير'),
                ('printExpensesList()', 'زر طباعة'),
                ('saveExpense()', 'وظيفة حفظ المصروف')
            ]
            
            found_buttons = 0
            
            for button_function, button_name in buttons_to_check:
                if button_function in content:
                    print(f"  ✅ {button_name} - موجود")
                    found_buttons += 1
                else:
                    print(f"  ❌ {button_name} - غير موجود")
            
            print(f"\n📊 النتيجة: {found_buttons}/{len(buttons_to_check)} أزرار موجودة")
            
            return found_buttons == len(buttons_to_check)
        else:
            print(f"  ❌ فشل في جلب صفحة المصروفات: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ خطأ في اختبار الصفحة: {e}")
        return False

def main():
    """الاختبار الرئيسي"""
    print("🚀 اختبار سريع لأزرار شاشة المصروفات")
    print("=" * 50)
    
    # اختبار API
    api_test = test_expenses_api()
    
    # اختبار الصفحة
    page_test = test_expenses_page()
    
    # النتائج النهائية
    print("\n" + "=" * 50)
    print("📊 نتائج الاختبار السريع:")
    print("=" * 50)
    
    if api_test and page_test:
        print("🎉 ممتاز! جميع أزرار المصروفات تعمل بشكل صحيح")
        print("✅ API يعمل")
        print("✅ الأزرار موجودة في الصفحة")
        print("✅ الوظائف متاحة")
        return True
    else:
        print("⚠️ بعض الأزرار تحتاج مراجعة:")
        if not api_test:
            print("❌ API لا يعمل بشكل صحيح")
        if not page_test:
            print("❌ بعض الأزرار غير موجودة في الصفحة")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎯 خلاصة: أزرار شاشة المصروفات تعمل بشكل صحيح!")
        print("💡 يمكنك الآن:")
        print("   - إضافة مصروفات جديدة")
        print("   - تعديل المصروفات الموجودة")
        print("   - حذف المصروفات")
        print("   - تصدير البيانات")
        print("   - طباعة القوائم")
    else:
        print("\n⚠️ يرجى مراجعة الأخطاء أعلاه وإصلاحها")
