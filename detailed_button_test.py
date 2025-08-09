#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تفصيلي للأزرار الرئيسية
Detailed Button Testing for Main Functions
"""

import re
from pathlib import Path

class DetailedButtonTester:
    def __init__(self):
        self.critical_buttons = []
        self.templates_dir = Path('templates')
        
    def analyze_unified_products_buttons(self):
        """تحليل أزرار الشاشة الموحدة"""
        print("🌟 تحليل أزرار الشاشة الموحدة...")
        
        file_path = self.templates_dir / 'unified_products.html'
        if not file_path.exists():
            print("❌ ملف unified_products.html غير موجود")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن الأزرار المهمة
            button_patterns = {
                'حفظ المادة الخام': r'<button[^>]*type=["\']submit["\'][^>]*>.*?حفظ المادة.*?</button>',
                'إضافة مكون': r'onclick=["\']addIngredientRow\(\)["\']',
                'مسح الكل': r'onclick=["\']clearAllIngredients\(\)["\']',
                'حفظ التكلفة والمنتج': r'onclick=["\']saveProductCost\(\)["\']',
                'تحديث المنتجات': r'onclick=["\']refreshReadyProducts\(\)["\']',
                'تبويب المواد الخام': r'data-bs-target=["\']#raw-materials["\']',
                'تبويب حساب التكاليف': r'data-bs-target=["\']#cost-calculation["\']',
                'تبويب المنتجات الجاهزة': r'data-bs-target=["\']#ready-products["\']'
            }
            
            for button_name, pattern in button_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'unified_products.html',
                        'status': 'موجود',
                        'count': len(matches),
                        'type': 'HTML Button'
                    })
                    print(f"✅ {button_name}: موجود ({len(matches)} مرة)")
                else:
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'unified_products.html',
                        'status': 'غير موجود',
                        'count': 0,
                        'type': 'HTML Button'
                    })
                    print(f"❌ {button_name}: غير موجود")
            
            # البحث عن الوظائف JavaScript
            js_functions = {
                'loadRawMaterials': 'تحميل المواد الخام',
                'saveRawMaterial': 'حفظ مادة خام',
                'createProduct': 'إنشاء منتج',
                'addIngredientRow': 'إضافة مكون',
                'calculateTotalCost': 'حساب التكلفة الإجمالية',
                'saveProductCost': 'حفظ تكلفة المنتج',
                'loadReadyProducts': 'تحميل المنتجات الجاهزة'
            }
            
            print(f"\n📜 تحليل وظائف JavaScript:")
            for func_name, description in js_functions.items():
                pattern = rf'function\s+{func_name}\s*\(|{func_name}\s*=\s*function|\b{func_name}\s*\('
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"✅ {description} ({func_name}): موجود")
                    self.critical_buttons.append({
                        'name': description,
                        'file': 'unified_products.html',
                        'status': 'موجود',
                        'count': len(matches),
                        'type': 'JavaScript Function'
                    })
                else:
                    print(f"❌ {description} ({func_name}): غير موجود")
                    self.critical_buttons.append({
                        'name': description,
                        'file': 'unified_products.html',
                        'status': 'غير موجود',
                        'count': 0,
                        'type': 'JavaScript Function'
                    })
        
        except Exception as e:
            print(f"❌ خطأ في تحليل unified_products.html: {e}")
    
    def analyze_dashboard_buttons(self):
        """تحليل أزرار لوحة التحكم"""
        print(f"\n🏠 تحليل أزرار لوحة التحكم...")
        
        file_path = self.templates_dir / 'dashboard.html'
        if not file_path.exists():
            print("❌ ملف dashboard.html غير موجود")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن أزرار الإحصائيات السريعة
            dashboard_buttons = {
                'فاتورة جديدة': r'href=["\'][^"\']*new_sale[^"\']*["\']',
                'إدارة المنتجات': r'href=["\'][^"\']*unified_products[^"\']*["\']',
                'المبيعات': r'href=["\'][^"\']*sales[^"\']*["\']',
                'العملاء': r'href=["\'][^"\']*customers[^"\']*["\']',
                'الموردين': r'href=["\'][^"\']*suppliers[^"\']*["\']',
                'التقارير': r'href=["\'][^"\']*reports[^"\']*["\']'
            }
            
            for button_name, pattern in dashboard_buttons.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"✅ {button_name}: موجود ({len(matches)} مرة)")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'dashboard.html',
                        'status': 'موجود',
                        'count': len(matches),
                        'type': 'Navigation Link'
                    })
                else:
                    print(f"❌ {button_name}: غير موجود")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'dashboard.html',
                        'status': 'غير موجود',
                        'count': 0,
                        'type': 'Navigation Link'
                    })
        
        except Exception as e:
            print(f"❌ خطأ في تحليل dashboard.html: {e}")
    
    def analyze_sidebar_buttons(self):
        """تحليل أزرار القائمة الجانبية"""
        print(f"\n📋 تحليل أزرار القائمة الجانبية...")
        
        file_path = self.templates_dir / 'base.html'
        if not file_path.exists():
            print("❌ ملف base.html غير موجود")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن روابط القائمة الجانبية
            sidebar_buttons = {
                'لوحة التحكم': r'href=["\'][^"\']*dashboard[^"\']*["\']',
                'الشاشة الموحدة': r'href=["\'][^"\']*unified_products[^"\']*["\']',
                'فاتورة جديدة': r'href=["\'][^"\']*new_sale[^"\']*["\']',
                'المبيعات': r'href=["\'][^"\']*sales[^"\']*["\']',
                'تسجيل الخروج': r'href=["\'][^"\']*logout[^"\']*["\']'
            }
            
            for button_name, pattern in sidebar_buttons.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"✅ {button_name}: موجود ({len(matches)} مرة)")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'base.html',
                        'status': 'موجود',
                        'count': len(matches),
                        'type': 'Sidebar Link'
                    })
                else:
                    print(f"❌ {button_name}: غير موجود")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'base.html',
                        'status': 'غير موجود',
                        'count': 0,
                        'type': 'Sidebar Link'
                    })
        
        except Exception as e:
            print(f"❌ خطأ في تحليل base.html: {e}")
    
    def analyze_sales_buttons(self):
        """تحليل أزرار المبيعات"""
        print(f"\n💰 تحليل أزرار المبيعات...")
        
        file_path = self.templates_dir / 'new_sale.html'
        if not file_path.exists():
            print("❌ ملف new_sale.html غير موجود")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن أزرار المبيعات
            sales_buttons = {
                'إضافة منتج': r'onclick=["\']addProduct\(\)["\']|<button[^>]*>.*?إضافة منتج.*?</button>',
                'حفظ الفاتورة': r'onclick=["\']saveSale\(\)["\']|<button[^>]*>.*?حفظ.*?</button>',
                'طباعة الفاتورة': r'onclick=["\']printInvoice\(\)["\']|<button[^>]*>.*?طباعة.*?</button>',
                'مسح الفاتورة': r'onclick=["\']clearSale\(\)["\']|<button[^>]*>.*?مسح.*?</button>',
                'اختيار العميل': r'<select[^>]*id=["\']customer[^"\']*["\']'
            }
            
            for button_name, pattern in sales_buttons.items():
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    print(f"✅ {button_name}: موجود ({len(matches)} مرة)")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'new_sale.html',
                        'status': 'موجود',
                        'count': len(matches),
                        'type': 'Sales Button'
                    })
                else:
                    print(f"❌ {button_name}: غير موجود")
                    self.critical_buttons.append({
                        'name': button_name,
                        'file': 'new_sale.html',
                        'status': 'غير موجود',
                        'count': 0,
                        'type': 'Sales Button'
                    })
        
        except Exception as e:
            print(f"❌ خطأ في تحليل new_sale.html: {e}")
    
    def run_detailed_analysis(self):
        """تشغيل التحليل التفصيلي"""
        print("🔍 بدء التحليل التفصيلي للأزرار الرئيسية")
        print("=" * 60)
        
        # تحليل الشاشات الرئيسية
        self.analyze_unified_products_buttons()
        self.analyze_dashboard_buttons()
        self.analyze_sidebar_buttons()
        self.analyze_sales_buttons()
        
        # عرض النتائج النهائية
        self.show_detailed_results()
    
    def show_detailed_results(self):
        """عرض النتائج التفصيلية"""
        print("\n" + "=" * 60)
        print("📊 نتائج التحليل التفصيلي للأزرار الرئيسية")
        print("=" * 60)
        
        # إحصائيات عامة
        total_buttons = len(self.critical_buttons)
        working_buttons = len([b for b in self.critical_buttons if b['status'] == 'موجود'])
        missing_buttons = len([b for b in self.critical_buttons if b['status'] == 'غير موجود'])
        
        print(f"📈 إجمالي الأزرار المهمة: {total_buttons}")
        print(f"✅ الأزرار الموجودة: {working_buttons}")
        print(f"❌ الأزرار المفقودة: {missing_buttons}")
        print(f"📊 نسبة النجاح: {(working_buttons/total_buttons*100):.1f}%")
        
        # تجميع حسب النوع
        by_type = {}
        for button in self.critical_buttons:
            btn_type = button['type']
            if btn_type not in by_type:
                by_type[btn_type] = {'موجود': 0, 'غير موجود': 0}
            by_type[btn_type][button['status']] += 1
        
        print(f"\n📋 تحليل حسب النوع:")
        for btn_type, counts in by_type.items():
            total = counts['موجود'] + counts['غير موجود']
            success_rate = (counts['موجود'] / total * 100) if total > 0 else 0
            print(f"   🔹 {btn_type}: {counts['موجود']}/{total} ({success_rate:.1f}%)")
        
        # عرض الأزرار المفقودة
        if missing_buttons > 0:
            print(f"\n❌ الأزرار المفقودة:")
            for button in self.critical_buttons:
                if button['status'] == 'غير موجود':
                    print(f"   - {button['name']} ({button['file']})")
        
        # توصيات
        print(f"\n🎯 توصيات:")
        if missing_buttons == 0:
            print("🎉 ممتاز! جميع الأزرار الرئيسية موجودة")
            print("✅ يمكن المتابعة لاختبار الوظائف")
        else:
            print("🔧 يرجى إضافة الأزرار المفقودة")
            print("⚠️ تحقق من صحة أسماء الوظائف")
        
        print("🌐 للاختبار الفعلي، شغل التطبيق على: http://localhost:5000")
        print("=" * 60)

def main():
    """الوظيفة الرئيسية"""
    tester = DetailedButtonTester()
    tester.run_detailed_analysis()

if __name__ == "__main__":
    main()
