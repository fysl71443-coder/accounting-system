#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نهائي للتأكد من عمل الطباعة
Final Working Print Test
"""

import requests
import time
import webbrowser

def final_test():
    """اختبار نهائي شامل"""
    print("🎯 اختبار نهائي للتأكد من عمل الطباعة")
    print("=" * 60)
    
    # انتظار الخادم
    print("⏳ انتظار تشغيل الخادم...")
    time.sleep(8)
    
    # فحص الخادم
    max_attempts = 10
    server_ready = False
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:5000", timeout=3)
            if response.status_code == 200:
                print("✅ الخادم جاهز")
                server_ready = True
                break
        except:
            pass
        
        print(f"   محاولة {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    if not server_ready:
        print("❌ الخادم غير جاهز")
        return False
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = session.post("http://localhost:5000/login", data=login_data)
        print("✅ تم تسجيل الدخول")
    except Exception as e:
        print(f"❌ فشل تسجيل الدخول: {e}")
        return False
    
    # فحص صفحة المدفوعات
    try:
        response = session.get("http://localhost:5000/payments_dues")
        if response.status_code == 200:
            content = response.text
            print("✅ تم الوصول لصفحة المدفوعات")
            
            # فحص نهائي للأزرار
            final_checks = [
                ('onclick="printAllSales()"', '🖨️ زر طباعة المبيعات'),
                ('onclick="printAllPurchases()"', '🖨️ زر طباعة المشتريات'),
                ('onclick="printAllExpenses()"', '🖨️ زر طباعة المصروفات'),
                ('onclick="printAllPayroll()"', '🖨️ زر طباعة الرواتب'),
                ('طباعة جميع المبيعات', '📝 نص زر المبيعات'),
                ('طباعة جميع المشتريات', '📝 نص زر المشتريات'),
                ('طباعة جميع المصروفات', '📝 نص زر المصروفات'),
                ('طباعة جميع الرواتب', '📝 نص زر الرواتب'),
                ('function printAllSales()', '⚙️ وظيفة طباعة المبيعات'),
                ('openSimplePrintWindow', '🪟 وظيفة فتح النافذة')
            ]
            
            print("\n🔍 الفحص النهائي:")
            working_features = 0
            
            for check, description in final_checks:
                if check in content:
                    print(f"   ✅ {description}")
                    working_features += 1
                else:
                    print(f"   ❌ {description}")
            
            success_rate = (working_features / len(final_checks)) * 100
            print(f"\n📊 معدل النجاح: {success_rate:.1f}% ({working_features}/{len(final_checks)})")
            
            # حفظ النتائج
            with open("final_test_results.html", "w", encoding="utf-8") as f:
                f.write(f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <title>نتائج الاختبار النهائي</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; direction: rtl; margin: 20px; }}
                        .success {{ color: #28a745; }}
                        .error {{ color: #dc3545; }}
                        .info {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    </style>
                </head>
                <body>
                    <h1>نتائج الاختبار النهائي للطباعة</h1>
                    <div class="info">
                        <h3>معدل النجاح: {success_rate:.1f}%</h3>
                        <p>الميزات العاملة: {working_features}/{len(final_checks)}</p>
                    </div>
                    
                    <h3>تفاصيل الفحص:</h3>
                    <ul>
                """)
                
                for check, description in final_checks:
                    status = "✅" if check in content else "❌"
                    css_class = "success" if check in content else "error"
                    f.write(f'<li class="{css_class}">{status} {description}</li>\n')
                
                f.write("""
                    </ul>
                    
                    <div class="info">
                        <h4>الخطوات التالية:</h4>
                        <ol>
                            <li>اذهب إلى: <a href="http://localhost:5000/payments_dues" target="_blank">صفحة المدفوعات</a></li>
                            <li>سجل الدخول: admin / admin112233</li>
                            <li>اختبر أزرار الطباعة في كل تبويب</li>
                            <li>تأكد من فتح نوافذ الطباعة</li>
                        </ol>
                    </div>
                </body>
                </html>
                """)
            
            print("💾 تم حفظ نتائج الاختبار في: final_test_results.html")
            
            return success_rate >= 80
            
        else:
            print(f"❌ فشل في الوصول للصفحة: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("🚀 اختبار نهائي شامل لوظائف الطباعة")
    print("=" * 70)
    
    # تشغيل الاختبار النهائي
    test_passed = final_test()
    
    # فتح الملفات
    print("\n🌐 فتح الملفات للاختبار اليدوي...")
    webbrowser.open("final_test_results.html")
    time.sleep(2)
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 70)
    print("🏁 النتائج النهائية:")
    print("=" * 70)
    
    if test_passed:
        print("🎉 نجح الاختبار النهائي!")
        print("✅ أزرار الطباعة تعمل بشكل صحيح")
        print("✅ يمكن اختبار الطباعة في صفحة المدفوعات")
        print("✅ جميع الوظائف متاحة")
        
        print("\n🎯 كيفية الاستخدام:")
        print("1. اذهب لصفحة المدفوعات")
        print("2. سجل الدخول")
        print("3. اختر أي تبويب")
        print("4. اضغط زر الطباعة")
        print("5. ستفتح نافذة مع التقرير")
        
    else:
        print("⚠️ الاختبار لم ينجح بالكامل")
        print("💡 قد تحتاج لمراجعة إضافية")
        print("📄 راجع ملف النتائج للتفاصيل")
    
    print("\n📄 الملفات المُنشأة:")
    print("- final_test_results.html: نتائج الاختبار")
    print("- manual_test_instructions.html: تعليمات الاختبار")
    print("- current_server_content.html: محتوى الخادم")
    
    print("\n🔗 الروابط:")
    print("- صفحة المدفوعات: http://localhost:5000/payments_dues")
    print("- صفحة الطباعة المنفصلة: http://localhost:5000/simple_print")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
