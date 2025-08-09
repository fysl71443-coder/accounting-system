#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل فحص شاشة المدفوعات والمستحقات
Run Payments and Dues Screen Testing
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_server_running():
    """فحص إذا كان الخادم يعمل"""
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """تشغيل الخادم"""
    print("🚀 تشغيل الخادم...")
    
    # البحث عن ملفات التشغيل
    start_files = [
        "simple_start.py",
        "start_server.py", 
        "run_server.py",
        "app.py"
    ]
    
    for start_file in start_files:
        if Path(start_file).exists():
            print(f"📄 استخدام ملف: {start_file}")
            try:
                # تشغيل الخادم في الخلفية
                process = subprocess.Popen([sys.executable, start_file], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
                
                # انتظار قليل للتأكد من بدء التشغيل
                time.sleep(5)
                
                # فحص إذا كان الخادم يعمل
                if check_server_running():
                    print("✅ الخادم يعمل بنجاح")
                    return process
                else:
                    print("❌ فشل في تشغيل الخادم")
                    process.terminate()
                    
            except Exception as e:
                print(f"❌ خطأ في تشغيل {start_file}: {e}")
    
    return None

def run_python_tests():
    """تشغيل اختبارات Python"""
    print("\n🐍 تشغيل اختبارات Python...")
    
    if not Path("test_payments_dues_screen.py").exists():
        print("❌ ملف الاختبار غير موجود")
        return False
    
    try:
        result = subprocess.run([sys.executable, "test_payments_dues_screen.py"], 
                              capture_output=True, text=True, timeout=60)
        
        print("📋 نتائج اختبارات Python:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ تحذيرات/أخطاء:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ انتهت مهلة الاختبار")
        return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل الاختبارات: {e}")
        return False

def open_browser_for_manual_test():
    """فتح المتصفح للفحص اليدوي"""
    print("\n🌐 فتح المتصفح للفحص اليدوي...")
    
    urls = [
        "http://localhost:5000/payments_dues",
        "http://localhost:5000/login"
    ]
    
    for url in urls:
        try:
            webbrowser.open(url)
            print(f"🔗 تم فتح: {url}")
            time.sleep(2)  # انتظار بين فتح الروابط
        except Exception as e:
            print(f"❌ فشل فتح {url}: {e}")

def show_manual_test_instructions():
    """عرض تعليمات الفحص اليدوي"""
    print("\n" + "="*80)
    print("📋 تعليمات الفحص اليدوي لشاشة المدفوعات والمستحقات")
    print("📋 Manual Testing Instructions for Payments and Dues Screen")
    print("="*80)
    
    instructions = [
        "1. 🔐 تسجيل الدخول: admin / admin123",
        "2. 📄 الانتقال لشاشة المدفوعات والمستحقات",
        "3. 🔍 اختبار الفلاتر في كل تبويب (الكل، مدفوع، جزئي، معلق)",
        "4. 🖨️ اختبار أزرار الطباعة في كل تبويب",
        "5. 📅 اختبار اختيار الشهر في نافذة الطباعة",
        "6. 👁️ اختبار معاينة الطباعة",
        "7. 🖨️ اختبار الطباعة المباشرة",
        "8. 🧪 استخدام أزرار الفحص في أسفل الصفحة",
        "9. 🔍 فحص وحدة التحكم (F12) للأخطاء",
        "10. ✅ التأكد من عمل جميع الوظائف"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")
    
    print("\n💡 نصائح:")
    print("   🔍 افتح Developer Tools (F12) لمراقبة الأخطاء")
    print("   🧪 استخدم أزرار الفحص في أسفل الصفحة")
    print("   📊 راجع نتائج الفحص في Console")
    print("   🔄 جرب الوظائف عدة مرات للتأكد")
    
    print("\n🎯 معايير النجاح:")
    print("   ✅ جميع الفلاتر تعمل بدون أخطاء")
    print("   ✅ جميع أزرار الطباعة تفتح النافذة")
    print("   ✅ معاينة الطباعة تعمل")
    print("   ✅ الطباعة المباشرة تعمل")
    print("   ✅ لا توجد أخطاء في Console")
    print("="*80)

def main():
    """الوظيفة الرئيسية"""
    print("="*80)
    print("🔍 فاحص شاشة المدفوعات والمستحقات الشامل")
    print("🔍 Comprehensive Payments and Dues Screen Tester")
    print("="*80)
    
    # فحص إذا كان الخادم يعمل
    if check_server_running():
        print("✅ الخادم يعمل بالفعل")
        server_process = None
    else:
        print("⚠️ الخادم لا يعمل - محاولة تشغيله...")
        server_process = start_server()
        
        if not server_process:
            print("❌ فشل في تشغيل الخادم")
            print("💡 يرجى تشغيل الخادم يدوياً ثم إعادة تشغيل هذا السكريبت")
            return
    
    try:
        # تشغيل اختبارات Python
        python_tests_passed = run_python_tests()
        
        # فتح المتصفح للفحص اليدوي
        open_browser_for_manual_test()
        
        # عرض تعليمات الفحص اليدوي
        show_manual_test_instructions()
        
        # انتظار المستخدم
        print("\n⏳ اضغط Enter بعد انتهاء الفحص اليدوي...")
        input()
        
        # النتائج النهائية
        print("\n" + "="*80)
        print("📊 ملخص نتائج الفحص")
        print("="*80)
        
        if python_tests_passed:
            print("✅ اختبارات Python: نجحت")
        else:
            print("❌ اختبارات Python: فشلت")
        
        print("\n💭 هل جميع الوظائف تعمل بشكل صحيح؟")
        manual_result = input("اكتب 'نعم' أو 'y' إذا كانت جميع الوظائف تعمل: ").lower().strip()
        
        if manual_result in ['نعم', 'y', 'yes', 'ن']:
            print("🎉 ممتاز! شاشة المدفوعات والمستحقات تعمل 100%")
            print("🚀 يمكن الآن المتابعة لإنشاء التقارير")
        else:
            print("⚠️ يحتاج مراجعة وإصلاح المشاكل قبل المتابعة")
            print("📋 يرجى مراجعة الأخطاء وإصلاحها")
        
    finally:
        # إغلاق الخادم إذا تم تشغيله من هنا
        if server_process:
            print("\n🛑 إغلاق الخادم...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    main()
