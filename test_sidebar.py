#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار القائمة الجانبية والشاشة الموحدة
Test Sidebar and Unified Screen
"""

import requests
from bs4 import BeautifulSoup

def test_sidebar():
    """اختبار القائمة الجانبية"""
    
    print('🧪 اختبار القائمة الجانبية والشاشة الموحدة...')

    # تسجيل الدخول
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'language': 'ar'
    }

    try:
        # تسجيل الدخول
        response = session.post('http://localhost:5000/login', data=login_data)
        if response.status_code == 200:
            print('✅ تم تسجيل الدخول بنجاح')
            
            # الحصول على الصفحة الرئيسية
            response = session.get('http://localhost:5000/dashboard')
            if response.status_code == 200:
                print('✅ تم تحميل الصفحة الرئيسية')
                
                # تحليل HTML للبحث عن القائمة الجانبية
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # البحث عن رابط الشاشة الموحدة
                unified_link = soup.find('a', href='/unified_products')
                if unified_link:
                    print('✅ تم العثور على رابط الشاشة الموحدة في القائمة الجانبية')
                    print(f'   النص: {unified_link.get_text().strip()}')
                    
                    # التحقق من الأيقونة
                    icon = unified_link.find('i', class_='fas fa-cogs')
                    if icon:
                        print('✅ الأيقونة موجودة')
                    else:
                        print('⚠️ الأيقونة غير موجودة')
                        
                    # التحقق من الكلاس المخصص
                    if 'unified-products' in unified_link.get('class', []):
                        print('✅ الكلاس المخصص موجود')
                    else:
                        print('⚠️ الكلاس المخصص غير موجود')
                        
                else:
                    print('❌ لم يتم العثور على رابط الشاشة الموحدة')
                
                # البحث عن جميع روابط القائمة الجانبية
                sidebar_links = soup.find_all('a', class_='nav-link')
                print(f'\\n📋 روابط القائمة الجانبية ({len(sidebar_links)}):')
                for i, link in enumerate(sidebar_links, 1):
                    href = link.get('href', '#')
                    text = link.get_text().strip()
                    if text and href != '#':
                        print(f'   {i}. {text} → {href}')
                
            else:
                print(f'❌ خطأ في تحميل الصفحة الرئيسية: {response.status_code}')
        else:
            print(f'❌ خطأ في تسجيل الدخول: {response.status_code}')
            
        # اختبار الوصول للشاشة الموحدة مباشرة
        print('\\n🌟 اختبار الوصول للشاشة الموحدة...')
        response = session.get('http://localhost:5000/unified_products')
        if response.status_code == 200:
            print('✅ تم تحميل الشاشة الموحدة بنجاح')
            
            # التحقق من وجود التبويبات
            soup = BeautifulSoup(response.text, 'html.parser')
            tabs = soup.find_all('button', {'data-bs-toggle': 'pill'})
            if tabs:
                print(f'✅ تم العثور على {len(tabs)} تبويب:')
                for tab in tabs:
                    tab_text = tab.get_text().strip()
                    print(f'   - {tab_text}')
            else:
                print('⚠️ لم يتم العثور على التبويبات')
                
        else:
            print(f'❌ خطأ في تحميل الشاشة الموحدة: {response.status_code}')
            
    except Exception as e:
        print(f'❌ خطأ: {e}')

    print('\\n🎉 انتهى الاختبار!')

if __name__ == "__main__":
    test_sidebar()
