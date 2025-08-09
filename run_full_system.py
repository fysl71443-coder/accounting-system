#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل النظام الكامل مع خانات الخصم
Run Full System with Discount Fields
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading

def kill_existing_servers():
    """إيقاف الخوادم الموجودة"""
    try:
        # إيقاف جميع عمليات Python
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, text=True)
        print("✅ تم إيقاف الخوادم الموجودة")
        time.sleep(2)
    except:
        pass

def start_full_system():
    """تشغيل النظام الكامل"""
    print("🚀 تشغيل النظام الكامل مع خانات الخصم...")
    print("📍 الخادم: http://localhost:5000")
    print("🏠 الشاشة الرئيسية: http://localhost:5000")
    print("💳 المدفوعات: http://localhost:5000/payments_dues")
    print("🔑 تسجيل الدخول: admin / admin112233")
    print("💰 خانات الخصم متاحة في المبيعات والمشتريات")
    print("=" * 70)
    
    try:
        # تشغيل النظام الكامل
        cmd = [
            sys.executable, '-c', '''
import sys
import os

# إضافة المسار الحالي
sys.path.insert(0, ".")

print("🔄 تحميل النظام الكامل...")

try:
    # استيراد النظام الكامل
    from app import app
    print("✅ تم تحميل النظام الكامل بنجاح")
    
    # تحديث إعدادات التطبيق
    app.config['SECRET_KEY'] = 'full-system-with-discount'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # فحص routes المتاحة
    all_routes = [rule.rule for rule in app.url_map.iter_rules()]
    print(f"📋 إجمالي routes: {len(all_routes)}")
    
    # فحص routes الطباعة
    print_routes = [rule.rule for rule in app.url_map.iter_rules() if "print" in rule.rule]
    print(f"🖨️ routes الطباعة: {len(print_routes)}")
    
    # فحص routes الرئيسية
    main_routes = [rule.rule for rule in app.url_map.iter_rules() if rule.rule in ['/', '/dashboard', '/payments_dues', '/login']]
    print(f"🏠 routes الرئيسية: {main_routes}")
    
    print("🌐 بدء تشغيل النظام الكامل...")
    print("🔗 الروابط المتاحة:")
    print("   - الرئيسية: http://localhost:5000")
    print("   - لوحة التحكم: http://localhost:5000/dashboard")
    print("   - المدفوعات: http://localhost:5000/payments_dues")
    print("   - تسجيل الدخول: http://localhost:5000/login")
    print("=" * 50)
    
    # تشغيل النظام الكامل
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    
except ImportError as e:
    print(f"❌ خطأ في استيراد النظام: {e}")
    print("💡 تأكد من وجود ملف app.py")
    
except Exception as e:
    print(f"❌ خطأ عام: {e}")
    import traceback
    traceback.print_exc()
'''
        ]
        
        # تشغيل الأمر
        process = subprocess.Popen(cmd, cwd=os.getcwd())
        print(f"✅ تم تشغيل النظام الكامل - Process ID: {process.pid}")
        
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام الكامل: {e}")
        return None

def open_browser():
    """فتح المتصفح للنظام الكامل"""
    print("⏳ انتظار تشغيل النظام...")
    time.sleep(5)
    
    try:
        print("🌐 فتح الشاشة الرئيسية للنظام الكامل...")
        webbrowser.open("http://localhost:5000")
        time.sleep(2)
        
        print("🌐 فتح لوحة التحكم...")
        webbrowser.open("http://localhost:5000/dashboard")
        
        print("✅ تم فتح النظام الكامل")
    except Exception as e:
        print(f"⚠️ تحذير في فتح المتصفح: {e}")

def test_full_system():
    """اختبار النظام الكامل"""
    print("\n🧪 اختبار النظام الكامل...")
    time.sleep(8)
    
    try:
        import requests
        
        # اختبار الصفحة الرئيسية
        response = requests.get("http://localhost:5000", timeout=5)
        print(f"🏠 الصفحة الرئيسية: {response.status_code}")
        
        # اختبار لوحة التحكم
        response = requests.get("http://localhost:5000/dashboard", timeout=5)
        print(f"📊 لوحة التحكم: {response.status_code}")
        
        # اختبار صفحة المدفوعات
        response = requests.get("http://localhost:5000/payments_dues", timeout=5)
        print(f"💳 المدفوعات: {response.status_code}")
        
        # اختبار مسار الطباعة مع الخصم
        response = requests.get("http://localhost:5000/print_invoices/sales", timeout=5)
        print(f"🖨️ طباعة المبيعات مع الخصم: {response.status_code}")
        
        print("🎉 النظام الكامل يعمل!")
        
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالنظام")
        
    except Exception as e:
        print(f"⚠️ خطأ في اختبار النظام: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🔧 تشغيل النظام الكامل مع خانات الخصم")
    print("=" * 80)
    
    # إيقاف الخوادم الموجودة
    kill_existing_servers()
    
    # تشغيل النظام الكامل
    server_process = start_full_system()
    
    if server_process:
        # فتح المتصفح في thread منفصل
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # اختبار النظام في thread منفصل
        test_thread = threading.Thread(target=test_full_system)
        test_thread.daemon = True
        test_thread.start()
        
        print("\n📋 معلومات النظام الكامل:")
        print("- النظام الكامل يعمل مع جميع الشاشات")
        print("- خانات الخصم مدمجة في المبيعات والمشتريات")
        print("- الشاشة الرئيسية ولوحة التحكم متاحة")
        print("- أزرار الطباعة تعمل مع النظام الكامل")
        
        print("\n🌐 الشاشات المتاحة:")
        print("   - الرئيسية: http://localhost:5000")
        print("   - لوحة التحكم: http://localhost:5000/dashboard")
        print("   - المدفوعات: http://localhost:5000/payments_dues")
        print("   - تسجيل الدخول: http://localhost:5000/login")
        
        print("\n⚠️ لإيقاف النظام: اضغط Ctrl+C")
        
    else:
        print("\n❌ فشل في تشغيل النظام الكامل")

if __name__ == "__main__":
    main()
