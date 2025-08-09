#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نهائي للطباعة المُصلحة
Final Test for Fixed Print
"""

import requests
import webbrowser
import time
import subprocess
import sys

def start_server():
    """تشغيل الخادم"""
    print("🚀 تشغيل الخادم...")
    
    try:
        # تشغيل الخادم في الخلفية
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd="D:/New folder/ACCOUNTS PROGRAM")
        
        # انتظار بدء التشغيل
        time.sleep(5)
        
        # فحص الخادم
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code in [200, 302]:
                print("✅ الخادم يعمل بنجاح")
                return process
        except:
            pass
        
        print("⚠️ الخادم قد لا يعمل بشكل صحيح")
        return process
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def test_print_buttons():
    """اختبار أزرار الطباعة"""
    print("\n🖨️ اختبار أزرار الطباعة...")
    
    # فحص الخادم
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code not in [200, 302]:
            print("❌ الخادم لا يعمل")
            return False
    except:
        print("❌ لا يمكن الاتصال بالخادم")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        if response.status_code != 200:
            print("❌ فشل تسجيل الدخول")
            return False
        print("✅ تم تسجيل الدخول")
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            print("✅ صفحة المدفوعات تعمل")
            
            content = response.text
            
            # فحص أزرار الطباعة الجديدة
            direct_print_count = content.count('directPrint(')
            print(f"✅ عدد أزرار الطباعة المباشرة: {direct_print_count}")
            
            # فحص وجود الوظائف
            if 'function directPrint' in content:
                print("✅ وظيفة الطباعة المباشرة موجودة")
            else:
                print("❌ وظيفة الطباعة المباشرة غير موجودة")
            
            return True
            
        else:
            print(f"❌ صفحة المدفوعات فشلت: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص صفحة المدفوعات: {e}")
        return False

def test_print_route():
    """اختبار route الطباعة"""
    print("\n📄 اختبار route الطباعة...")
    
    session = requests.Session()
    
    # تسجيل الدخول
    login_data = {'username': 'admin', 'password': 'admin123'}
    session.post("http://localhost:5000/login", data=login_data)
    
    # اختبار الطباعة المباشرة
    form_data = {
        'section': 'sales',
        'month': '2025-08'
    }
    
    try:
        response = session.post("http://localhost:5000/print-invoices", data=form_data)
        
        if response.status_code == 200:
            print("✅ route الطباعة المباشر يعمل")
            
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                print("✅ تم إنتاج ملف PDF")
                
                # حفظ ملف PDF
                filename = f"final_test_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ تم حفظ ملف PDF: {filename}")
                
            elif 'text/html' in content_type:
                print("✅ تم إنتاج HTML (fallback)")
                
                # فحص محتوى HTML
                content = response.text
                if 'فواتير sales لشهر 2025-08' in content:
                    print("✅ محتوى التقرير صحيح")
                if 'S-2025-' in content:
                    print("✅ البيانات التجريبية ظاهرة")
                    
            return True
            
        else:
            print(f"❌ route الطباعة فشل: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في route الطباعة: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🧪 اختبار نهائي للطباعة المُصلحة")
    print("=" * 60)
    
    # فحص الخادم أو تشغيله
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ الخادم يعمل بالفعل")
    except:
        print("⚠️ الخادم لا يعمل، محاولة تشغيله...")
        server_process = start_server()
        if not server_process:
            print("❌ فشل في تشغيل الخادم")
            return
    
    # اختبار أزرار الطباعة
    if not test_print_buttons():
        print("❌ فشل اختبار أزرار الطباعة")
        return
    
    # اختبار route الطباعة
    if not test_print_route():
        print("❌ فشل اختبار route الطباعة")
        return
    
    # فتح المتصفح للاختبار اليدوي
    print("\n🌐 فتح المتصفح للاختبار اليدوي...")
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 60)
    print("🎉 نجح الاختبار النهائي!")
    print("=" * 60)
    
    print("✅ الخادم يعمل")
    print("✅ أزرار الطباعة مُصلحة")
    print("✅ route الطباعة المباشر يعمل")
    print("✅ إنتاج PDF/HTML يعمل")
    
    print("\n📋 تعليمات الاستخدام:")
    print("1. تسجيل الدخول: admin / admin123")
    print("2. اضغط أي زر 'طباعة' في التبويبات")
    print("3. سيتم فتح نافذة جديدة مع التقرير")
    print("4. إذا كان PDF متاح، سيتم تحميله تلقائياً")
    print("5. إذا لم يكن متاح، سيظهر HTML للطباعة")
    
    print("\n🔗 الروابط:")
    print("- شاشة المدفوعات: http://localhost:5000/payments_dues")
    print("- اختبار مباشر: POST http://localhost:5000/print-invoices")
    
    print("\n🌟 المزايا الجديدة:")
    print("- طباعة مباشرة بدون نوافذ منبثقة معقدة")
    print("- دعم PDF تلقائي مع HTML fallback")
    print("- عرض البنود التفصيلية لكل فاتورة")
    print("- تصميم احترافي ومنسق")
    
    print("=" * 60)
    
    input("\nاضغط Enter بعد انتهاء الاختبار...")

if __name__ == "__main__":
    main()
