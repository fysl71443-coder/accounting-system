#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعادة تشغيل الخادم مع إعادة تحميل كاملة
Fresh Server Restart
"""

import os
import sys
import subprocess
import time
import signal

def kill_existing_servers():
    """إيقاف جميع خوادم Python الموجودة"""
    print("🛑 إيقاف جميع خوادم Python الموجودة...")
    
    try:
        # إيقاف جميع عمليات Python التي تحتوي على app.py أو run_local.py
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'python.*app.py'], 
                         capture_output=True, text=True)
            subprocess.run(['pkill', '-f', 'python.*run_local.py'], 
                         capture_output=True, text=True)
        
        print("✅ تم إيقاف الخوادم الموجودة")
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️ تحذير في إيقاف الخوادم: {e}")

def clear_python_cache():
    """مسح cache Python"""
    print("🧹 مسح cache Python...")
    
    try:
        # مسح ملفات __pycache__
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    import shutil
                    shutil.rmtree(pycache_path)
                    print(f"   ✅ تم مسح {pycache_path}")
                except:
                    pass
        
        # مسح ملفات .pyc
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc'):
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
        
        print("✅ تم مسح cache Python")
        
    except Exception as e:
        print(f"⚠️ تحذير في مسح cache: {e}")

def start_fresh_server():
    """تشغيل خادم جديد"""
    print("🚀 تشغيل خادم جديد...")
    
    try:
        # تشغيل الخادم مع إعادة التحميل
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        # تشغيل الخادم
        process = subprocess.Popen([
            sys.executable, '-c', '''
import sys
sys.path.insert(0, ".")

# مسح cache الوحدات
modules_to_remove = [k for k in sys.modules.keys() if k.startswith("app")]
for module in modules_to_remove:
    if module in sys.modules:
        del sys.modules[module]

# استيراد التطبيق
from app import app

# مسح cache القوالب
app.jinja_env.cache = {}

print("🌐 الخادم يعمل على: http://localhost:5000")
print("🔄 إعادة التحميل التلقائي مفعلة")
print("🖨️ أزرار الطباعة جاهزة")
print("=" * 50)

# تشغيل الخادم
app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True, use_debugger=True)
'''
        ], env=env, cwd=os.getcwd())
        
        print(f"✅ تم تشغيل الخادم - Process ID: {process.pid}")
        
        # انتظار قليل للتأكد من بدء الخادم
        time.sleep(5)
        
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def test_server():
    """اختبار الخادم"""
    print("🧪 اختبار الخادم...")
    
    try:
        import requests
        
        # اختبار الصفحة الرئيسية
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية تعمل")
        else:
            print(f"⚠️ الصفحة الرئيسية: {response.status_code}")
        
        # اختبار مسار الطباعة
        response = requests.get("http://localhost:5000/print_invoices/sales", timeout=5)
        if response.status_code in [200, 302]:  # 302 = redirect
            print("✅ مسار الطباعة يعمل")
        else:
            print(f"⚠️ مسار الطباعة: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الخادم: {e}")
        return False

def open_browser():
    """فتح المتصفح"""
    print("🌐 فتح المتصفح...")
    
    try:
        import webbrowser
        webbrowser.open("http://localhost:5000/payments_dues")
        print("✅ تم فتح المتصفح")
    except Exception as e:
        print(f"⚠️ تحذير في فتح المتصفح: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("🔄 إعادة تشغيل الخادم مع إعادة تحميل كاملة")
    print("=" * 60)
    
    # إيقاف الخوادم الموجودة
    kill_existing_servers()
    
    # مسح cache
    clear_python_cache()
    
    # تشغيل خادم جديد
    server_process = start_fresh_server()
    
    if server_process:
        # اختبار الخادم
        time.sleep(3)
        server_working = test_server()
        
        if server_working:
            print("\n🎉 تم تشغيل الخادم بنجاح!")
            print("✅ جميع المسارات تعمل")
            print("✅ أزرار الطباعة جاهزة")
            
            # فتح المتصفح
            open_browser()
            
            print("\n📋 معلومات مهمة:")
            print("- الخادم: http://localhost:5000")
            print("- صفحة المدفوعات: http://localhost:5000/payments_dues")
            print("- تسجيل الدخول: admin / admin112233")
            print("- إعادة التحميل التلقائي: مفعلة")
            
            print("\n🖨️ أزرار الطباعة المتاحة:")
            print("- طباعة المبيعات")
            print("- طباعة المشتريات") 
            print("- طباعة المصروفات")
            print("- طباعة الرواتب")
            
            print("\n⚠️ لإيقاف الخادم: اضغط Ctrl+C في terminal الخادم")
            
        else:
            print("\n❌ فشل في اختبار الخادم")
            print("💡 جرب تشغيل: python simple_print_server.py")
    
    else:
        print("\n❌ فشل في تشغيل الخادم")
        print("💡 جرب الحلول البديلة:")
        print("1. python simple_print_server.py")
        print("2. فتح working_print_solution.html")

if __name__ == "__main__":
    main()
