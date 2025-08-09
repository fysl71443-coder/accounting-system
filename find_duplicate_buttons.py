#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
البحث عن الأزرار المكررة وحذفها
Find and Remove Duplicate Buttons
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class DuplicateButtonFinder:
    def __init__(self):
        self.templates_dir = Path('templates')
        self.duplicates = defaultdict(list)
        self.all_buttons = []
        
    def extract_buttons_from_file(self, file_path):
        """استخراج الأزرار من ملف"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            buttons = []
            
            # أنماط البحث عن الأزرار
            button_patterns = [
                # أزرار HTML
                r'<button[^>]*>(.*?)</button>',
                r'<input[^>]*type=["\'](?:button|submit)["\'][^>]*>',
                # روابط تعمل كأزرار
                r'<a[^>]*class=["\'][^"\']*btn[^"\']*["\'][^>]*>(.*?)</a>',
                # أزرار JavaScript
                r'onclick=["\']([^"\']*)["\']',
                # عناصر قابلة للنقر
                r'data-bs-toggle=["\']([^"\']*)["\']',
                r'data-bs-target=["\']([^"\']*)["\']'
            ]
            
            for pattern in button_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1] if len(match) > 1 else str(match)
                    
                    # تنظيف النص
                    clean_text = re.sub(r'<[^>]+>', '', str(match)).strip()
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    
                    if clean_text and len(clean_text) > 2:
                        buttons.append({
                            'text': clean_text,
                            'file': file_path.name,
                            'pattern': pattern,
                            'full_match': str(match)[:100]
                        })
            
            return buttons
            
        except Exception as e:
            print(f"خطأ في قراءة {file_path}: {e}")
            return []
    
    def find_all_buttons(self):
        """البحث عن جميع الأزرار"""
        print("🔍 البحث عن جميع الأزرار في النظام...")
        
        for html_file in self.templates_dir.glob('*.html'):
            buttons = self.extract_buttons_from_file(html_file)
            self.all_buttons.extend(buttons)
            print(f"📄 {html_file.name}: {len(buttons)} زر")
        
        print(f"📊 إجمالي الأزرار المكتشفة: {len(self.all_buttons)}")
    
    def find_duplicates(self):
        """البحث عن الأزرار المكررة"""
        print("\n🔍 البحث عن الأزرار المكررة...")
        
        # تجميع الأزرار حسب النص
        button_groups = defaultdict(list)
        for button in self.all_buttons:
            # تطبيع النص للمقارنة
            normalized_text = button['text'].lower().strip()
            # إزالة الرموز التعبيرية والرموز الخاصة
            normalized_text = re.sub(r'[^\w\s]', '', normalized_text)
            button_groups[normalized_text].append(button)
        
        # العثور على المكررات
        for text, buttons in button_groups.items():
            if len(buttons) > 1:
                self.duplicates[text] = buttons
        
        print(f"🔄 عدد الأزرار المكررة: {len(self.duplicates)}")
        
        # عرض المكررات
        for text, buttons in self.duplicates.items():
            print(f"\n📋 نص مكرر: '{text}'")
            for button in buttons:
                print(f"   📄 {button['file']}: {button['full_match'][:50]}...")
    
    def find_similar_functions(self):
        """البحث عن الوظائف المتشابهة"""
        print("\n🔍 البحث عن الوظائف المتشابهة...")
        
        # وظائف JavaScript مشتركة
        common_functions = [
            'save', 'delete', 'edit', 'add', 'remove', 'update', 'refresh',
            'clear', 'reset', 'submit', 'cancel', 'close', 'open'
        ]
        
        function_usage = defaultdict(list)
        
        for button in self.all_buttons:
            text_lower = button['text'].lower()
            for func in common_functions:
                if func in text_lower:
                    function_usage[func].append(button)
        
        print("📊 استخدام الوظائف المشتركة:")
        for func, buttons in function_usage.items():
            if len(buttons) > 1:
                print(f"   🔧 {func}: {len(buttons)} مرة")
                files = set(b['file'] for b in buttons)
                print(f"      📁 في الملفات: {', '.join(files)}")
    
    def generate_cleanup_recommendations(self):
        """إنشاء توصيات التنظيف"""
        print("\n💡 توصيات التنظيف:")
        
        recommendations = []
        
        # توصيات للأزرار المكررة
        for text, buttons in self.duplicates.items():
            if len(buttons) > 2:
                recommendations.append({
                    'type': 'duplicate',
                    'text': text,
                    'count': len(buttons),
                    'files': [b['file'] for b in buttons],
                    'recommendation': f"دمج {len(buttons)} أزرار مكررة في مكون واحد"
                })
        
        # توصيات للملفات الكبيرة
        file_button_count = defaultdict(int)
        for button in self.all_buttons:
            file_button_count[button['file']] += 1
        
        for file, count in file_button_count.items():
            if count > 50:
                recommendations.append({
                    'type': 'large_file',
                    'file': file,
                    'count': count,
                    'recommendation': f"تقسيم الملف {file} ({count} زر) إلى مكونات أصغر"
                })
        
        # عرض التوصيات
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['recommendation']}")
            if rec['type'] == 'duplicate':
                print(f"   📁 الملفات: {', '.join(rec['files'])}")
            elif rec['type'] == 'large_file':
                print(f"   📄 الملف: {rec['file']}")
        
        return recommendations
    
    def run_analysis(self):
        """تشغيل التحليل الكامل"""
        print("🧹 بدء تحليل الأزرار المكررة")
        print("=" * 50)
        
        self.find_all_buttons()
        self.find_duplicates()
        self.find_similar_functions()
        recommendations = self.generate_cleanup_recommendations()
        
        print("\n" + "=" * 50)
        print("📊 ملخص التحليل:")
        print(f"📈 إجمالي الأزرار: {len(self.all_buttons)}")
        print(f"🔄 أزرار مكررة: {len(self.duplicates)}")
        print(f"💡 توصيات التحسين: {len(recommendations)}")
        print("=" * 50)
        
        return recommendations

def main():
    """الوظيفة الرئيسية"""
    finder = DuplicateButtonFinder()
    recommendations = finder.run_analysis()
    
    # حفظ التقرير
    with open('duplicate_buttons_report.txt', 'w', encoding='utf-8') as f:
        f.write("تقرير الأزرار المكررة\n")
        f.write("=" * 30 + "\n\n")
        
        f.write(f"إجمالي الأزرار: {len(finder.all_buttons)}\n")
        f.write(f"أزرار مكررة: {len(finder.duplicates)}\n\n")
        
        f.write("الأزرار المكررة:\n")
        f.write("-" * 20 + "\n")
        for text, buttons in finder.duplicates.items():
            f.write(f"\nنص مكرر: '{text}'\n")
            for button in buttons:
                f.write(f"  - {button['file']}: {button['full_match'][:50]}...\n")
        
        f.write("\nتوصيات التحسين:\n")
        f.write("-" * 20 + "\n")
        for i, rec in enumerate(recommendations, 1):
            f.write(f"{i}. {rec['recommendation']}\n")
    
    print("\n📄 تم حفظ التقرير في: duplicate_buttons_report.txt")

if __name__ == "__main__":
    main()
