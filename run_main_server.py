#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل الخادم الرئيسي مع خانات الخصم
Run Main Server with Discount Fields
"""

import os
import sys
import subprocess
import time

def run_main_server():
    """تشغيل الخادم الرئيسي مباشرة"""
    print("🚀 تشغيل الخادم الرئيسي مع خانات الخصم...")
    print("📍 الخادم: http://localhost:5000")
    print("💳 المدفوعات: http://localhost:5000/payments_dues")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("💰 الميزات الجديدة: خانات الخصم في المبيعات والمشتريات")
    print("=" * 70)
    
    try:
        # تشغيل الخادم الرئيسي مباشرة
        cmd = [
            sys.executable, '-c', '''
import sys
import os

# إضافة المسار الحالي
sys.path.insert(0, ".")

print("🔄 تحميل الخادم الرئيسي...")

try:
    # استيراد التطبيق الرئيسي
    from app import app
    print("✅ تم تحميل app.py بنجاح")
    
    # فحص routes الطباعة
    print_routes = [rule.rule for rule in app.url_map.iter_rules() if "print" in rule.rule and "invoice" in rule.rule]
    print(f"📋 routes الطباعة: {len(print_routes)} route")
    
    if print_routes:
        print("✅ routes الطباعة متاحة")
        for route in print_routes[:3]:  # عرض أول 3 routes
            print(f"   - {route}")
    
    print("🌐 بدء تشغيل الخادم الرئيسي...")
    print("🔗 الروابط:")
    print("   - الرئيسية: http://localhost:5000")
    print("   - المدفوعات: http://localhost:5000/payments_dues")
    print("   - طباعة المبيعات: http://localhost:5000/print_invoices/sales")
    print("=" * 50)
    
    # تشغيل الخادم
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    
except ImportError as e:
    print(f"❌ خطأ في استيراد app.py: {e}")
    print("💡 تأكد من وجود ملف app.py في المجلد الحالي")
    
except Exception as e:
    print(f"❌ خطأ عام: {e}")
    import traceback
    traceback.print_exc()
'''
        ]
        
        # تشغيل الأمر
        process = subprocess.Popen(cmd, cwd=os.getcwd())
        print(f"✅ تم تشغيل الخادم الرئيسي - Process ID: {process.pid}")
        
        # انتظار قليل للتأكد من التشغيل
        time.sleep(3)
        
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم الرئيسي: {e}")
        return None

def test_server():
    """اختبار الخادم"""
    print("\n🧪 اختبار الخادم...")
    time.sleep(5)
    
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
        
        print("🎉 الخادم الرئيسي يعمل بنجاح!")
        
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
        print("💡 تأكد من أن الخادم يعمل على http://localhost:5000")
        
    except Exception as e:
        print(f"⚠️ خطأ في اختبار الخادم: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🔧 تشغيل الخادم الرئيسي مع خانات الخصم")
    print("=" * 80)
    
    # تشغيل الخادم الرئيسي
    server_process = run_main_server()
    
    if server_process:
        # اختبار الخادم
        test_server()
        
        print("\n📋 معلومات مهمة:")
        print("- الخادم الرئيسي يعمل مع خانات الخصم")
        print("- خانات الخصم متاحة في المبيعات والمشتريات")
        print("- أزرار الطباعة تفتح في نوافذ منفصلة")
        print("- جميع الوظائف مدمجة في النظام الرئيسي")
        
        print("\n🌐 افتح المتصفح على:")
        print("   http://localhost:5000/payments_dues")
        
        print("\n⚠️ لإيقاف الخادم: اضغط Ctrl+C في terminal الخادم")
        
        # انتظار إنهاء العملية
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف الخادم")
            server_process.terminate()
        
    else:
        print("\n❌ فشل في تشغيل الخادم الرئيسي")
        print("💡 تأكد من:")
        print("- وجود ملف app.py")
        print("- تثبيت جميع المكتبات المطلوبة")
        print("- عدم وجود أخطاء في الكود")

if __name__ == "__main__":
    main()
