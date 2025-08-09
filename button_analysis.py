#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل شامل لجميع أزرار النظام
Comprehensive Button Analysis
"""

import os
import re
from pathlib import Path

class ButtonAnalyzer:
    def __init__(self):
        self.buttons_found = []
        self.templates_dir = Path('templates')
        self.static_dir = Path('static')
        
    def analyze_html_buttons(self, file_path):
        """تحليل الأزرار في ملفات HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن الأزرار
            button_patterns = [
                r'<button[^>]*>(.*?)</button>',
                r'<input[^>]*type=["\']button["\'][^>]*>',
                r'<input[^>]*type=["\']submit["\'][^>]*>',
                r'<a[^>]*class=["\'][^"\']*btn[^"\']*["\'][^>]*>(.*?)</a>',
                r'onclick=["\']([^"\']*)["\']'
            ]
            
            for pattern in button_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1] if len(match) > 1 else str(match)
                    
                    self.buttons_found.append({
                        'file': file_path.name,
                        'type': 'HTML Button',
                        'content': match.strip()[:100],
                        'pattern': pattern
                    })
        
        except Exception as e:
            print(f"خطأ في تحليل {file_path}: {e}")
    
    def analyze_javascript_functions(self, file_path):
        """تحليل الوظائف في JavaScript"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن الوظائف
            js_patterns = [
                r'function\s+(\w+)\s*\(',
                r'(\w+)\s*=\s*function\s*\(',
                r'onclick\s*=\s*["\']([^"\']*)["\']',
                r'addEventListener\s*\(\s*["\']([^"\']*)["\']',
                r'\.click\s*\(',
                r'submit\s*\('
            ]
            
            for pattern in js_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    self.buttons_found.append({
                        'file': file_path.name,
                        'type': 'JavaScript Function',
                        'content': match[:50],
                        'pattern': pattern
                    })
        
        except Exception as e:
            print(f"خطأ في تحليل JS {file_path}: {e}")
    
    def analyze_flask_routes(self):
        """تحليل routes في Flask"""
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن routes
            route_patterns = [
                r'@app\.route\(["\']([^"\']*)["\'].*?\)\s*\n\s*def\s+(\w+)',
                r'@app\.route\(["\']([^"\']*)["\'].*?methods\s*=\s*\[["\']([^"\']*)["\']'
            ]
            
            for pattern in route_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        self.buttons_found.append({
                            'file': 'app.py',
                            'type': 'Flask Route',
                            'content': f"{match[0]} -> {match[1]}",
                            'pattern': 'Route'
                        })
        
        except Exception as e:
            print(f"خطأ في تحليل Flask routes: {e}")
    
    def run_analysis(self):
        """تشغيل التحليل الشامل"""
        print("🔍 بدء التحليل الشامل لجميع أزرار النظام")
        print("=" * 60)
        
        # تحليل ملفات HTML
        if self.templates_dir.exists():
            print("📄 تحليل ملفات HTML...")
            for html_file in self.templates_dir.glob('*.html'):
                self.analyze_html_buttons(html_file)
                # تحليل JavaScript المدمج في HTML
                self.analyze_javascript_functions(html_file)
        
        # تحليل ملفات JavaScript المنفصلة
        if self.static_dir.exists():
            print("📜 تحليل ملفات JavaScript...")
            for js_file in self.static_dir.rglob('*.js'):
                self.analyze_javascript_functions(js_file)
        
        # تحليل Flask routes
        print("🌐 تحليل Flask routes...")
        self.analyze_flask_routes()
        
        # عرض النتائج
        self.show_results()
    
    def show_results(self):
        """عرض نتائج التحليل"""
        print("\n" + "=" * 60)
        print("📊 نتائج التحليل الشامل للأزرار")
        print("=" * 60)
        
        # تجميع النتائج حسب النوع
        by_type = {}
        for button in self.buttons_found:
            btn_type = button['type']
            if btn_type not in by_type:
                by_type[btn_type] = []
            by_type[btn_type].append(button)
        
        total_buttons = len(self.buttons_found)
        print(f"📈 إجمالي الأزرار والوظائف المكتشفة: {total_buttons}")
        
        for btn_type, buttons in by_type.items():
            print(f"\n🔹 {btn_type} ({len(buttons)} عنصر):")
            
            # عرض أول 10 عناصر من كل نوع
            for i, button in enumerate(buttons[:10]):
                content = button['content'].replace('\n', ' ').strip()
                if len(content) > 50:
                    content = content[:47] + "..."
                print(f"   {i+1:2d}. {button['file']}: {content}")
            
            if len(buttons) > 10:
                print(f"   ... و {len(buttons) - 10} عنصر آخر")
        
        # تحليل الملفات الرئيسية
        print(f"\n📋 تحليل الملفات:")
        files_analysis = {}
        for button in self.buttons_found:
            file_name = button['file']
            if file_name not in files_analysis:
                files_analysis[file_name] = 0
            files_analysis[file_name] += 1
        
        for file_name, count in sorted(files_analysis.items(), key=lambda x: x[1], reverse=True):
            print(f"   📄 {file_name}: {count} عنصر")
        
        # توصيات الاختبار
        print(f"\n🎯 توصيات الاختبار:")
        print("1. اختبار جميع أزرار HTML في المتصفح")
        print("2. اختبار وظائف JavaScript")
        print("3. اختبار Flask routes عبر HTTP requests")
        print("4. اختبار التفاعل بين الأزرار والخادم")
        print("5. اختبار الاستجابة في حالات الخطأ")
        
        print("\n" + "=" * 60)

def main():
    """الوظيفة الرئيسية"""
    analyzer = ButtonAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
