import subprocess
import sys
import os

# تغيير المجلد الحالي
os.chdir(r"D:\New folder\ACCOUNTS PROGRAM")

print("🚀 تشغيل خادم المحاسبة...")
print("📍 http://localhost:5000")
print("👤 admin / admin123")
print("=" * 40)

# تشغيل الخادم مباشرة
try:
    subprocess.run([sys.executable, "app.py"], check=True)
except KeyboardInterrupt:
    print("\n🛑 تم إيقاف الخادم")
except Exception as e:
    print(f"❌ خطأ: {e}")
    input("اضغط Enter للخروج...")
