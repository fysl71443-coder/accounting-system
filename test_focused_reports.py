#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار التقارير المركزة - التأكد من طباعة المعلومات المهمة فقط
Test Focused Reports - Ensure printing only important information
"""

import requests
import re
from datetime import datetime

class FocusedReportsTest:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        
    def login(self):
        """تسجيل الدخول"""
        try:
            login_data = {'username': 'admin', 'password': 'admin123'}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            return response.status_code == 200
        except:
            return False
    
    def test_report_content(self, report_type):
        """اختبار محتوى التقرير للتأكد من التركيز على المهم"""
        try:
            response = self.session.get(f"{self.base_url}/print_invoices/{report_type}")
            
            if response.status_code != 200:
                return False, f"خطأ HTTP: {response.status_code}"
            
            content = response.text
            
            # فحص العناصر المهمة الموجودة
            important_elements = {
                'header': 'نظام المحاسبة المتكامل' in content,
                'title': f'تقرير' in content,
                'date': 'تاريخ الطباعة' in content,
                'summary': 'ملخص' in content,
                'table': '<table>' in content,
                'total': 'المجموع الإجمالي' in content,
                'payment_status': 'حالة الدفع' in content or 'مدفوع' in content
            }
            
            # فحص العناصر غير المرغوبة (يجب ألا تكون موجودة)
            unwanted_elements = {
                'debug_info': 'debug' in content.lower(),
                'technical_details': 'console.log' in content,
                'excessive_styling': content.count('style=') > 20,
                'too_many_columns': content.count('<th>') > 8,
                'verbose_text': len(content) > 15000  # تقرير طويل جداً
            }
            
            # حساب النقاط
            important_score = sum(important_elements.values())
            unwanted_score = sum(unwanted_elements.values())
            
            # تحليل المحتوى
            analysis = {
                'important_elements': important_elements,
                'unwanted_elements': unwanted_elements,
                'important_score': important_score,
                'unwanted_score': unwanted_score,
                'content_length': len(content),
                'table_columns': content.count('<th>'),
                'has_summary': 'ملخص' in content,
                'has_totals': 'المجموع' in content
            }
            
            return True, analysis
            
        except Exception as e:
            return False, f"خطأ: {e}"
    
    def test_all_reports(self):
        """اختبار جميع التقارير"""
        print("📊 اختبار التقارير المركزة:")
        print("=" * 50)
        
        reports = [
            ('sales', 'المبيعات'),
            ('purchases', 'المشتريات'),
            ('expenses', 'المصروفات'),
            ('payroll', 'الرواتب')
        ]
        
        results = {}
        
        for report_type, name in reports:
            print(f"\n🔍 اختبار تقرير {name}:")
            
            success, analysis = self.test_report_content(report_type)
            
            if success:
                important_score = analysis['important_score']
                unwanted_score = analysis['unwanted_score']
                content_length = analysis['content_length']
                table_columns = analysis['table_columns']
                
                print(f"  ✅ التقرير يعمل")
                print(f"  📏 طول المحتوى: {content_length:,} حرف")
                print(f"  📋 عدد الأعمدة: {table_columns}")
                print(f"  ⭐ العناصر المهمة: {important_score}/7")
                print(f"  ⚠️ العناصر غير المرغوبة: {unwanted_score}/5")
                
                # تقييم جودة التقرير
                if important_score >= 6 and unwanted_score <= 1 and table_columns <= 6:
                    quality = "ممتاز"
                    quality_icon = "🟢"
                elif important_score >= 5 and unwanted_score <= 2:
                    quality = "جيد"
                    quality_icon = "🟡"
                else:
                    quality = "يحتاج تحسين"
                    quality_icon = "🔴"
                
                print(f"  {quality_icon} جودة التقرير: {quality}")
                
                results[report_type] = {
                    'success': True,
                    'quality': quality,
                    'important_score': important_score,
                    'unwanted_score': unwanted_score,
                    'content_length': content_length,
                    'table_columns': table_columns
                }
            else:
                print(f"  ❌ فشل التقرير: {analysis}")
                results[report_type] = {'success': False, 'error': analysis}
        
        return results
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("📋 اختبار شامل للتقارير المركزة")
        print("=" * 60)
        
        # تسجيل الدخول
        if not self.login():
            print("❌ فشل تسجيل الدخول")
            return False
        
        print("✅ تم تسجيل الدخول بنجاح")
        
        # اختبار التقارير
        results = self.test_all_reports()
        
        # تحليل النتائج
        print("\n" + "=" * 60)
        print("📊 تحليل نتائج التقارير المركزة:")
        print("=" * 60)
        
        successful_reports = 0
        excellent_reports = 0
        
        for report_type, result in results.items():
            if result['success']:
                successful_reports += 1
                if result.get('quality') == 'ممتاز':
                    excellent_reports += 1
        
        total_reports = len(results)
        success_rate = (successful_reports / total_reports * 100) if total_reports > 0 else 0
        excellence_rate = (excellent_reports / total_reports * 100) if total_reports > 0 else 0
        
        print(f"📈 معدل النجاح: {success_rate:.1f}%")
        print(f"⭐ معدل الامتياز: {excellence_rate:.1f}%")
        print(f"✅ تقارير ناجحة: {successful_reports}/{total_reports}")
        print(f"🏆 تقارير ممتازة: {excellent_reports}/{total_reports}")
        
        if excellence_rate >= 75:
            print("\n🎉 ممتاز! التقارير مركزة ومهنية")
            print("📋 جميع التقارير تعرض المعلومات المهمة فقط")
        elif success_rate >= 75:
            print("\n🟢 جيد - التقارير تعمل بشكل مقبول")
        else:
            print("\n🔴 يحتاج تحسين - التقارير تحتاج مراجعة")
        
        return excellence_rate >= 75

if __name__ == "__main__":
    tester = FocusedReportsTest()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 نظام التقارير المركزة جاهز!")
        print("📊 جميع التقارير تركز على المعلومات المهمة فقط")
    else:
        print("\n⚠️ النظام يحتاج مراجعة لتحسين التركيز على المهم")
