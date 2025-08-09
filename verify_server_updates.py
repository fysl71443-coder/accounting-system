#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
التحقق من تطبيق تحديثات الخادم
Verify Server Updates
"""

import requests
import time
import webbrowser

def wait_for_server():
    """انتظار تشغيل الخادم"""
    print("⏳ انتظار تشغيل الخادم...")
    
    max_attempts = 15
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:5000", timeout=3)
            if response.status_code == 200:
                print("✅ الخادم يعمل الآن")
                return True
        except:
            pass
        
        print(f"   محاولة {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ فشل في انتظار الخادم")
    return False

def verify_updates():
    """التحقق من تطبيق التحديثات"""
    print("🔍 التحقق من تطبيق التحديثات...")
    
    # تسجيل الدخول
    session = requests.Session()
    try:
        login_data = {'username': 'admin', 'password': 'admin112233'}
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
            
            # فحص التحديثات المطلوبة
            updates_to_check = [
                ('onclick="printAllSales()"', 'زر طباعة المبيعات'),
                ('onclick="printAllPurchases()"', 'زر طباعة المشتريات'),
                ('onclick="printAllExpenses()"', 'زر طباعة المصروفات'),
                ('onclick="printAllPayroll()"', 'زر طباعة الرواتب'),
                ('function printAllSales()', 'وظيفة طباعة المبيعات'),
                ('بيانات تجريبية', 'البيانات التجريبية'),
                ('openSimplePrintWindow', 'وظيفة فتح النافذة'),
                ('console.log', 'رسائل التشخيص')
            ]
            
            print("\n🔍 فحص التحديثات المطبقة:")
            updates_found = 0
            missing_updates = []
            
            for update, description in updates_to_check:
                if update in content:
                    print(f"   ✅ {description}")
                    updates_found += 1
                else:
                    print(f"   ❌ {description}")
                    missing_updates.append(description)
            
            print(f"\n📊 التحديثات المطبقة: {updates_found}/{len(updates_to_check)}")
            
            if missing_updates:
                print("\n❌ التحديثات المفقودة:")
                for update in missing_updates:
                    print(f"   - {update}")
            
            # حفظ محتوى الصفحة للتشخيص
            with open("current_server_content.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("\n💾 تم حفظ محتوى الصفحة في: current_server_content.html")
            
            return updates_found >= len(updates_to_check) * 0.8
            
        else:
            print(f"❌ فشل في الوصول للصفحة: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في فحص الصفحة: {e}")
        return False

def create_manual_test_instructions():
    """إنشاء تعليمات الاختبار اليدوي"""
    print("\n📋 إنشاء تعليمات الاختبار اليدوي...")
    
    instructions_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تعليمات الاختبار اليدوي</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; margin: 20px; }
            .step-card { margin: 20px 0; padding: 20px; border: 2px solid #007bff; border-radius: 10px; }
            .step-number { background: #007bff; color: white; border-radius: 50%; width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-left: 15px; }
            .important-note { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 15px 0; }
            .success-indicator { color: #28a745; font-weight: bold; }
            .error-indicator { color: #dc3545; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center text-primary mb-4">
                <i class="fas fa-clipboard-check"></i>
                تعليمات الاختبار اليدوي للطباعة
            </h1>
            
            <div class="important-note">
                <h5><i class="fas fa-exclamation-triangle text-warning"></i> ملاحظة مهمة:</h5>
                <p>إذا كانت الأزرار لا تعمل في صفحة المدفوعات، فهذا يعني أن الخادم لم يُعاد تشغيله بعد التحديثات.</p>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">1</span>فتح صفحة المدفوعات</h3>
                <p>اذهب إلى: <a href="http://localhost:5000/payments_dues" target="_blank" class="btn btn-primary">http://localhost:5000/payments_dues</a></p>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">2</span>تسجيل الدخول</h3>
                <ul>
                    <li><strong>اسم المستخدم:</strong> <code>admin</code></li>
                    <li><strong>كلمة المرور:</strong> <code>admin112233</code></li>
                </ul>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">3</span>اختبار أزرار الطباعة</h3>
                <p>في كل تبويب، ابحث عن الأزرار التالية واختبرها:</p>
                <ul>
                    <li><span class="badge bg-primary">تبويب المبيعات:</span> زر "طباعة جميع المبيعات"</li>
                    <li><span class="badge bg-success">تبويب المشتريات:</span> زر "طباعة جميع المشتريات"</li>
                    <li><span class="badge bg-warning">تبويب المصروفات:</span> زر "طباعة جميع المصروفات"</li>
                    <li><span class="badge bg-info">تبويب الرواتب:</span> زر "طباعة جميع الرواتب"</li>
                </ul>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">4</span>النتائج المتوقعة</h3>
                <div class="row">
                    <div class="col-md-6">
                        <h5 class="success-indicator"><i class="fas fa-check"></i> إذا كانت تعمل:</h5>
                        <ul>
                            <li>تفتح نافذة جديدة</li>
                            <li>تظهر تقرير منسق</li>
                            <li>تحتوي على بيانات (حقيقية أو تجريبية)</li>
                            <li>يمكن طباعتها أو حفظها كـ PDF</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h5 class="error-indicator"><i class="fas fa-times"></i> إذا كانت لا تعمل:</h5>
                        <ul>
                            <li>رسالة "Not Found"</li>
                            <li>لا تفتح نافذة</li>
                            <li>رسالة خطأ في المتصفح</li>
                            <li>لا يحدث شيء عند الضغط</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">5</span>استكشاف الأخطاء</h3>
                <p>إذا لم تعمل الأزرار:</p>
                <ol>
                    <li>اضغط F12 لفتح أدوات المطور</li>
                    <li>اذهب لتبويب "Console"</li>
                    <li>اضغط على زر الطباعة</li>
                    <li>ابحث عن رسائل الخطأ</li>
                    <li>تأكد من وجود الوظائف JavaScript</li>
                </ol>
            </div>
            
            <div class="step-card">
                <h3><span class="step-number">6</span>البديل المؤقت</h3>
                <p>إذا لم تعمل الأزرار، يمكنك استخدام:</p>
                <a href="http://localhost:5000/simple_print" target="_blank" class="btn btn-outline-secondary">
                    <i class="fas fa-print"></i>
                    صفحة الطباعة المنفصلة
                </a>
            </div>
            
            <div class="important-note">
                <h5><i class="fas fa-lightbulb text-info"></i> نصائح:</h5>
                <ul>
                    <li>تأكد من إعادة تحميل الصفحة (Ctrl+F5)</li>
                    <li>امسح cache المتصفح إذا لزم الأمر</li>
                    <li>جرب متصفح آخر للتأكد</li>
                    <li>تحقق من أن الخادم يعمل بشكل صحيح</li>
                </ul>
            </div>
        </div>
        
        <script>
            // إضافة مؤشرات تفاعلية
            document.addEventListener('DOMContentLoaded', function() {
                console.log('✅ تم تحميل تعليمات الاختبار اليدوي');
                
                // إضافة تأثيرات بصرية
                const stepCards = document.querySelectorAll('.step-card');
                stepCards.forEach((card, index) => {
                    card.style.animationDelay = `${index * 0.2}s`;
                    card.classList.add('animate__animated', 'animate__fadeInUp');
                });
            });
        </script>
    </body>
    </html>
    """
    
    filename = "manual_test_instructions.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(instructions_html)
    
    print(f"✅ تم إنشاء تعليمات الاختبار: {filename}")
    return filename

def main():
    """الوظيفة الرئيسية"""
    print("🔧 التحقق من تطبيق تحديثات الخادم")
    print("=" * 60)
    
    # انتظار تشغيل الخادم
    if not wait_for_server():
        print("❌ لم يتم تشغيل الخادم بعد")
        print("💡 تأكد من تشغيل: python run_local.py")
        return
    
    # التحقق من التحديثات
    updates_applied = verify_updates()
    
    # إنشاء تعليمات الاختبار
    instructions_file = create_manual_test_instructions()
    
    # فتح الملفات
    print("\n🌐 فتح الملفات للاختبار...")
    webbrowser.open(instructions_file)
    time.sleep(2)
    webbrowser.open("http://localhost:5000/payments_dues")
    
    print("\n" + "=" * 60)
    print("📊 ملخص التحقق:")
    print("=" * 60)
    
    if updates_applied:
        print("🎉 التحديثات مطبقة بنجاح!")
        print("✅ أزرار الطباعة يجب أن تعمل الآن")
        print("✅ يمكن اختبار الطباعة في صفحة المدفوعات")
    else:
        print("⚠️ بعض التحديثات قد لا تكون مطبقة")
        print("💡 قد تحتاج لإعادة تشغيل الخادم مرة أخرى")
    
    print(f"\n📄 تعليمات الاختبار: {instructions_file}")
    print("📄 صفحة المدفوعات: http://localhost:5000/payments_dues")
    print("📄 ملف التشخيص: current_server_content.html")
    
    print("\n🎯 الخطوات التالية:")
    print("1. اتبع تعليمات الاختبار اليدوي")
    print("2. اختبر كل زر طباعة في كل تبويب")
    print("3. تأكد من فتح نوافذ الطباعة")
    print("4. إذا لم تعمل، راجع ملف التشخيص")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
