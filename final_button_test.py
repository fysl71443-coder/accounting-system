#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
الاختبار النهائي الشامل لجميع الأزرار
Final Comprehensive Button Test
"""

import re
from pathlib import Path

class FinalButtonTester:
    def __init__(self):
        self.test_results = []
        self.templates_dir = Path('templates')
        
    def log_result(self, category, button_name, status, details=""):
        """تسجيل نتيجة الاختبار"""
        self.test_results.append({
            'category': category,
            'button': button_name,
            'status': status,
            'details': details
        })
        
        icon = "✅" if status == "موجود" else "❌" if status == "مفقود" else "⚠️"
        print(f"{icon} {button_name}: {details}")
    
    def test_unified_products_screen(self):
        """اختبار شاشة المنتجات الموحدة"""
        print("🌟 اختبار شاشة المنتجات الموحدة...")
        print("-" * 50)
        
        file_path = self.templates_dir / 'unified_products.html'
        if not file_path.exists():
            self.log_result("الشاشة الموحدة", "ملف الشاشة", "مفقود", "unified_products.html غير موجود")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # اختبار التبويبات
        tabs = [
            ('raw-materials-tab', 'تبويب المواد الخام'),
            ('cost-calculation-tab', 'تبويب حساب التكاليف'),
            ('ready-products-tab', 'تبويب المنتجات الجاهزة')
        ]
        
        for tab_id, tab_name in tabs:
            if tab_id in content:
                self.log_result("التبويبات", tab_name, "موجود", "يعمل بشكل صحيح")
            else:
                self.log_result("التبويبات", tab_name, "مفقود", f"لم يتم العثور على {tab_id}")
        
        # اختبار أزرار المواد الخام
        raw_material_buttons = [
            ('rawMaterialForm', 'نموذج إضافة مادة خام'),
            ('materialName', 'حقل اسم المادة'),
            ('materialUnit', 'حقل الوحدة'),
            ('materialPrice', 'حقل السعر'),
            ('saveRawMaterial', 'وظيفة حفظ المادة')
        ]
        
        for element_id, element_name in raw_material_buttons:
            if element_id in content:
                self.log_result("المواد الخام", element_name, "موجود", "متوفر في الكود")
            else:
                self.log_result("المواد الخام", element_name, "مفقود", f"لم يتم العثور على {element_id}")
        
        # اختبار أزرار حساب التكاليف
        cost_calculation_buttons = [
            ('productForm', 'نموذج إنشاء منتج'),
            ('productName', 'حقل اسم المنتج'),
            ('productServings', 'حقل عدد الحصص'),
            ('addIngredientRow', 'وظيفة إضافة مكون'),
            ('calculateTotalCost', 'وظيفة حساب التكلفة'),
            ('saveProductCost', 'وظيفة حفظ المنتج')
        ]
        
        for element_id, element_name in cost_calculation_buttons:
            if element_id in content:
                self.log_result("حساب التكاليف", element_name, "موجود", "متوفر في الكود")
            else:
                self.log_result("حساب التكاليف", element_name, "مفقود", f"لم يتم العثور على {element_id}")
        
        # اختبار أزرار المنتجات الجاهزة
        ready_products_buttons = [
            ('readyProductsTable', 'جدول المنتجات الجاهزة'),
            ('refreshReadyProducts', 'وظيفة تحديث المنتجات'),
            ('loadReadyProducts', 'وظيفة تحميل المنتجات')
        ]
        
        for element_id, element_name in ready_products_buttons:
            if element_id in content:
                self.log_result("المنتجات الجاهزة", element_name, "موجود", "متوفر في الكود")
            else:
                self.log_result("المنتجات الجاهزة", element_name, "مفقود", f"لم يتم العثور على {element_id}")
    
    def test_dashboard_screen(self):
        """اختبار شاشة لوحة التحكم"""
        print(f"\n🏠 اختبار شاشة لوحة التحكم...")
        print("-" * 50)
        
        file_path = self.templates_dir / 'dashboard.html'
        if not file_path.exists():
            self.log_result("لوحة التحكم", "ملف لوحة التحكم", "مفقود", "dashboard.html غير موجود")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # اختبار أزرار الإحصائيات السريعة
        dashboard_links = [
            ("url_for('new_sale')", 'رابط فاتورة جديدة'),
            ("url_for('unified_products')", 'رابط الشاشة الموحدة'),
            ("url_for('sales')", 'رابط المبيعات'),
            ("url_for('customers')", 'رابط العملاء'),
            ("url_for('suppliers')", 'رابط الموردين')
        ]
        
        for link_pattern, link_name in dashboard_links:
            if link_pattern in content:
                self.log_result("روابط لوحة التحكم", link_name, "موجود", "يعمل بشكل صحيح")
            else:
                self.log_result("روابط لوحة التحكم", link_name, "مفقود", f"لم يتم العثور على {link_pattern}")
        
        # اختبار بطاقات الإحصائيات
        stats_cards = [
            ('إجمالي المبيعات', 'بطاقة إجمالي المبيعات'),
            ('عدد الفواتير', 'بطاقة عدد الفواتير'),
            ('المنتجات', 'بطاقة المنتجات'),
            ('العملاء', 'بطاقة العملاء')
        ]
        
        for card_text, card_name in stats_cards:
            if card_text in content:
                self.log_result("بطاقات الإحصائيات", card_name, "موجود", "متوفرة في الواجهة")
            else:
                self.log_result("بطاقات الإحصائيات", card_name, "مفقود", f"لم يتم العثور على {card_text}")
    
    def test_sidebar_navigation(self):
        """اختبار القائمة الجانبية"""
        print(f"\n📋 اختبار القائمة الجانبية...")
        print("-" * 50)
        
        file_path = self.templates_dir / 'base.html'
        if not file_path.exists():
            self.log_result("القائمة الجانبية", "ملف القالب الأساسي", "مفقود", "base.html غير موجود")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # اختبار روابط القائمة الجانبية
        sidebar_links = [
            ("url_for('dashboard')", 'رابط لوحة التحكم'),
            ("url_for('unified_products')", 'رابط الشاشة الموحدة'),
            ("url_for('new_sale')", 'رابط فاتورة جديدة'),
            ("url_for('sales')", 'رابط المبيعات'),
            ("url_for('logout')", 'رابط تسجيل الخروج')
        ]
        
        for link_pattern, link_name in sidebar_links:
            if link_pattern in content:
                self.log_result("روابط القائمة الجانبية", link_name, "موجود", "يعمل بشكل صحيح")
            else:
                self.log_result("روابط القائمة الجانبية", link_name, "مفقود", f"لم يتم العثور على {link_pattern}")
        
        # اختبار التصميم المميز للشاشة الموحدة
        special_design_elements = [
            ('unified-products', 'كلاس التصميم المميز'),
            ('🌟 إدارة المنتجات والتكاليف', 'النص المميز'),
            ('شاشة موحدة متكاملة', 'الوصف التوضيحي'),
            ('pulse', 'تأثير النبض')
        ]
        
        for element, element_name in special_design_elements:
            if element in content:
                self.log_result("التصميم المميز", element_name, "موجود", "متوفر في التصميم")
            else:
                self.log_result("التصميم المميز", element_name, "مفقود", f"لم يتم العثور على {element}")
    
    def test_sales_screen(self):
        """اختبار شاشة المبيعات"""
        print(f"\n💰 اختبار شاشة المبيعات...")
        print("-" * 50)
        
        file_path = self.templates_dir / 'new_sale.html'
        if not file_path.exists():
            self.log_result("شاشة المبيعات", "ملف فاتورة جديدة", "مفقود", "new_sale.html غير موجود")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # اختبار عناصر فاتورة المبيعات
        sales_elements = [
            ('customer_id', 'حقل اختيار العميل'),
            ('product_search', 'حقل البحث عن المنتج'),
            ('sale_items', 'جدول عناصر الفاتورة'),
            ('total_amount', 'إجمالي الفاتورة'),
            ('addProduct', 'وظيفة إضافة منتج'),
            ('saveSale', 'وظيفة حفظ الفاتورة')
        ]
        
        for element_id, element_name in sales_elements:
            if element_id in content:
                self.log_result("عناصر المبيعات", element_name, "موجود", "متوفر في الشاشة")
            else:
                self.log_result("عناصر المبيعات", element_name, "مفقود", f"لم يتم العثور على {element_id}")
    
    def run_comprehensive_test(self):
        """تشغيل الاختبار الشامل"""
        print("🧪 بدء الاختبار النهائي الشامل لجميع أزرار النظام")
        print("=" * 70)
        
        # تشغيل جميع الاختبارات
        self.test_unified_products_screen()
        self.test_dashboard_screen()
        self.test_sidebar_navigation()
        self.test_sales_screen()
        
        # عرض النتائج النهائية
        self.show_comprehensive_results()
    
    def show_comprehensive_results(self):
        """عرض النتائج الشاملة"""
        print("\n" + "=" * 70)
        print("📊 النتائج النهائية للاختبار الشامل")
        print("=" * 70)
        
        # إحصائيات عامة
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'موجود'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'مفقود'])
        
        print(f"📈 إجمالي العناصر المختبرة: {total_tests}")
        print(f"✅ العناصر الموجودة: {passed_tests}")
        print(f"❌ العناصر المفقودة: {failed_tests}")
        print(f"📊 نسبة النجاح: {(passed_tests/total_tests*100):.1f}%")
        
        # تجميع النتائج حسب الفئة
        by_category = {}
        for result in self.test_results:
            category = result['category']
            if category not in by_category:
                by_category[category] = {'موجود': 0, 'مفقود': 0}
            by_category[category][result['status']] += 1
        
        print(f"\n📋 النتائج حسب الفئة:")
        for category, counts in by_category.items():
            total = counts['موجود'] + counts['مفقود']
            success_rate = (counts['موجود'] / total * 100) if total > 0 else 0
            status_icon = "🟢" if success_rate >= 80 else "🟡" if success_rate >= 60 else "🔴"
            print(f"   {status_icon} {category}: {counts['موجود']}/{total} ({success_rate:.1f}%)")
        
        # عرض العناصر المفقودة المهمة
        critical_missing = [r for r in self.test_results if r['status'] == 'مفقود' and 
                           any(keyword in r['button'].lower() for keyword in ['حفظ', 'إضافة', 'تحديث', 'رابط'])]
        
        if critical_missing:
            print(f"\n⚠️ العناصر المفقودة المهمة:")
            for result in critical_missing[:10]:  # أول 10 عناصر مهمة
                print(f"   - {result['button']} ({result['category']})")
        
        # التوصيات النهائية
        print(f"\n🎯 التوصيات النهائية:")
        if failed_tests == 0:
            print("🎉 ممتاز! جميع العناصر موجودة ويمكن المتابعة للاختبار الفعلي")
        elif failed_tests <= 5:
            print("✅ النظام في حالة جيدة مع بعض العناصر المفقودة البسيطة")
        elif failed_tests <= 15:
            print("⚠️ النظام يحتاج لبعض الإصلاحات قبل الاختبار الفعلي")
        else:
            print("🔧 النظام يحتاج لإصلاحات شاملة")
        
        print(f"\n🌐 للاختبار الفعلي:")
        print("1. شغل التطبيق: python run_fixed.py")
        print("2. افتح المتصفح: http://localhost:5000")
        print("3. سجل الدخول: admin / admin123")
        print("4. اختبر كل زر يدوياً")
        print("=" * 70)

def main():
    """الوظيفة الرئيسية"""
    tester = FinalButtonTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
