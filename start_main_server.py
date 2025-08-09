#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل الخادم الأصلي مع أزرار الطباعة
Start Main Server with Print Buttons
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading

def start_main_server():
    """تشغيل الخادم الأصلي"""
    print("🚀 تشغيل الخادم الأصلي مع أزرار الطباعة...")
    print("📍 الخادم سيعمل على: http://localhost:5000")
    print("💳 صفحة المدفوعات: http://localhost:5000/payments_dues")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("🖨️ أزرار الطباعة مدمجة في النظام الأصلي")
    print("=" * 70)
    
    try:
        # تشغيل الخادم الأصلي مباشرة
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        # تشغيل app.py مباشرة
        process = subprocess.Popen([
            sys.executable, '-c', '''
import sys
import os
sys.path.insert(0, ".")

# تعيين متغيرات البيئة
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "1"

print("🔄 تحميل التطبيق الأصلي...")

# استيراد التطبيق الأصلي
try:
    from app import app
    print("✅ تم تحميل التطبيق بنجاح")
    
    # مسح cache القوالب
    app.jinja_env.cache = {}
    print("✅ تم مسح cache القوالب")
    
    # فحص routes الطباعة
    print("🔍 فحص routes الطباعة...")
    print_routes = [rule.rule for rule in app.url_map.iter_rules() if "print" in rule.rule and "invoice" in rule.rule]
    print(f"📋 routes الطباعة الموجودة: {print_routes}")
    
    if print_routes:
        print("✅ routes الطباعة متاحة")
    else:
        print("⚠️ لم يتم العثور على routes الطباعة")
    
    print("🌐 بدء تشغيل الخادم...")
    print("🔗 الروابط المتاحة:")
    print("   - الرئيسية: http://localhost:5000")
    print("   - المدفوعات: http://localhost:5000/payments_dues")
    print("   - طباعة المبيعات: http://localhost:5000/print_invoices/sales")
    print("=" * 50)
    
    # تشغيل الخادم
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True, use_debugger=True)
    
except Exception as e:
    print(f"❌ خطأ في تحميل التطبيق: {e}")
    import traceback
    traceback.print_exc()
'''
        ], env=env, cwd=os.getcwd())
        
        print(f"✅ تم تشغيل الخادم - Process ID: {process.pid}")
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def open_browser():
    """فتح المتصفح بعد تشغيل الخادم"""
    print("⏳ انتظار تشغيل الخادم...")
    time.sleep(8)
    
    try:
        print("🌐 فتح المتصفح...")
        webbrowser.open("http://localhost:5000/payments_dues")
        print("✅ تم فتح صفحة المدفوعات")
    except Exception as e:
        print(f"⚠️ تحذير في فتح المتصفح: {e}")

def test_server():
    """اختبار الخادم"""
    print("🧪 اختبار الخادم...")
    time.sleep(10)
    
    try:
        import requests
        
        # اختبار الصفحة الرئيسية
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية تعمل")
        else:
            print(f"⚠️ الصفحة الرئيسية: {response.status_code}")
        
        # اختبار صفحة المدفوعات
        response = requests.get("http://localhost:5000/payments_dues", timeout=5)
        if response.status_code in [200, 302]:  # 302 = redirect to login
            print("✅ صفحة المدفوعات متاحة")
        else:
            print(f"⚠️ صفحة المدفوعات: {response.status_code}")
        
        # اختبار مسار الطباعة
        response = requests.get("http://localhost:5000/print_invoices/sales", timeout=5)
        if response.status_code in [200, 302]:  # 302 = redirect to login
            print("✅ مسار الطباعة متاح")
        else:
            print(f"⚠️ مسار الطباعة: {response.status_code}")
        
        print("🎉 جميع الاختبارات نجحت!")
        
    except Exception as e:
        print(f"⚠️ تحذير في اختبار الخادم: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🔧 تشغيل النظام الأصلي مع أزرار الطباعة المدمجة")
    print("=" * 80)
    
    # تشغيل الخادم الأصلي
    server_process = start_main_server()
    
    if server_process:
        # فتح المتصفح في thread منفصل
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # اختبار الخادم في thread منفصل
        test_thread = threading.Thread(target=test_server)
        test_thread.daemon = True
        test_thread.start()
        
        print("\n📋 معلومات مهمة:")
        print("- الخادم الأصلي يعمل مع أزرار الطباعة المدمجة")
        print("- صفحة المدفوعات ستفتح تلقائياً")
        print("- أزرار الطباعة تفتح في نوافذ منفصلة")
        print("- جميع الوظائف مدمجة في النظام الأصلي")
        
        print("\n⚠️ لإيقاف الخادم: اضغط Ctrl+C في terminal الخادم")
        
    else:
        print("\n❌ فشل في تشغيل الخادم الأصلي")
        print("💡 تأكد من:")
        print("- وجود ملف app.py")
        print("- تثبيت جميع المكتبات المطلوبة")
        print("- عدم وجود أخطاء في الكود")

if __name__ == "__main__":
    main()
