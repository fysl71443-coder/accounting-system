#!/usr/bin/env python3
import requests
import webbrowser
import time

def quick_test():
    print("🧪 اختبار سريع للنظام...")
    
    try:
        # اختبار الاتصال
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ النظام يعمل!")
            print("🌐 فتح المتصفح...")
            webbrowser.open('http://localhost:5000')
        else:
            print("❌ النظام لا يعمل")
    except:
        print("❌ لا يمكن الوصول للنظام")
        print("💡 تأكد من تشغيل النظام أولاً")

if __name__ == "__main__":
    quick_test()
