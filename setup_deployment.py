#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إعداد النشر السريع
Quick Deployment Setup Tool
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def generate_secret_key():
    """توليد مفتاح سري قوي"""
    return secrets.token_urlsafe(32)

def check_git_repo():
    """التحقق من وجود مستودع Git"""
    if Path(".git").exists():
        print("✅ مستودع Git موجود")
        print("✅ Git repository found")
        return True
    else:
        print("❌ لا يوجد مستودع Git")
        print("❌ No Git repository found")
        return False

def init_git_repo():
    """تهيئة مستودع Git جديد"""
    try:
        subprocess.run(["git", "init"], check=True)
        print("✅ تم تهيئة مستودع Git")
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ فشل في تهيئة مستودع Git")
        print("❌ Failed to initialize Git repository")
        return False

def create_gitignore():
    """إنشاء ملف .gitignore"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite3

# Environment Variables
.env
.env.local
.env.production

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Render
.render/

# Local development
accounting.db
data/
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("✅ تم إنشاء ملف .gitignore")
    print("✅ .gitignore file created")

def create_env_example():
    """إنشاء ملف .env.example"""
    secret_key = generate_secret_key()
    
    env_content = f"""# Environment Variables for Accounting System

# Security
SECRET_KEY={secret_key}

# Database
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# Flask Environment
FLASK_ENV=production
FLASK_DEBUG=0

# Application Settings
APP_NAME=Integrated Accounting System
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ تم إنشاء ملف .env.example")
    print("✅ .env.example file created")
    print(f"🔑 مفتاح سري جديد: {secret_key}")
    print(f"🔑 New secret key: {secret_key}")

def update_render_yaml():
    """تحديث ملف render.yaml"""
    render_content = """services:
  - type: web
    name: accounting-system
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: accounting-db
          property: connectionString
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: 0
    
  - type: pserv
    name: accounting-db
    env: postgresql
    plan: free
    databaseName: accounting_system
    user: accounting_user
"""
    
    with open("render.yaml", "w", encoding="utf-8") as f:
        f.write(render_content)
    
    print("✅ تم تحديث ملف render.yaml")
    print("✅ render.yaml file updated")

def create_readme_deployment():
    """إنشاء ملف README للنشر"""
    readme_content = """# نشر نظام المحاسبة - Accounting System Deployment

## 🚀 خطوات النشر السريع - Quick Deployment Steps

### 1. رفع الكود إلى GitHub
```bash
git add .
git commit -m "Initial deployment setup"
git push origin main
```

### 2. إنشاء حساب على Render
- اذهب إلى [render.com](https://render.com)
- أنشئ حساباً جديداً أو سجل الدخول

### 3. إنشاء قاعدة البيانات
- اضغط "New +" → "PostgreSQL"
- اسم قاعدة البيانات: `accounting-db`
- خطة: Free

### 4. إنشاء خدمة الويب
- اضغط "New +" → "Web Service"
- اربط مستودع GitHub
- استخدم الإعدادات من `render.yaml`

### 5. تسجيل الدخول
- المستخدم: `admin`
- كلمة المرور: `admin123`

## 📞 الدعم
راجع `DEPLOYMENT_GUIDE.md` للتفاصيل الكاملة.
"""
    
    with open("DEPLOYMENT_README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ تم إنشاء ملف DEPLOYMENT_README.md")
    print("✅ DEPLOYMENT_README.md file created")

def commit_changes():
    """حفظ التغييرات في Git"""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Setup deployment configuration"], check=True)
        print("✅ تم حفظ التغييرات في Git")
        print("✅ Changes committed to Git")
        return True
    except subprocess.CalledProcessError:
        print("❌ فشل في حفظ التغييرات")
        print("❌ Failed to commit changes")
        return False

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🏢 نظام المحاسبة المتكامل - Integrated Accounting System")
    print("🚀 أداة إعداد النشر - Deployment Setup Tool")
    print("=" * 60)
    print()
    
    # التحقق من الملفات المطلوبة
    required_files = ["app.py", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ الملف المطلوب غير موجود: {file}")
            print(f"❌ Required file not found: {file}")
            return
    
    print("✅ جميع الملفات المطلوبة موجودة")
    print("✅ All required files found")
    print()
    
    # التحقق من Git أو تهيئته
    if not check_git_repo():
        init_git = input("هل تريد تهيئة مستودع Git جديد؟ (y/n) / Initialize new Git repo? (y/n): ").lower().strip()
        if init_git in ['y', 'yes', 'نعم', 'ن']:
            if not init_git_repo():
                return
        else:
            print("⚠️ يُنصح بإنشاء مستودع Git للنشر")
            print("⚠️ Git repository recommended for deployment")
    
    print("\n🔧 إعداد ملفات النشر...")
    print("🔧 Setting up deployment files...")
    
    # إنشاء الملفات
    create_gitignore()
    create_env_example()
    update_render_yaml()
    create_readme_deployment()
    
    print("\n✅ تم إعداد جميع ملفات النشر بنجاح!")
    print("✅ All deployment files setup successfully!")
    
    # حفظ التغييرات في Git
    if check_git_repo():
        commit_git = input("\nهل تريد حفظ التغييرات في Git؟ (y/n) / Commit changes to Git? (y/n): ").lower().strip()
        if commit_git in ['y', 'yes', 'نعم', 'ن']:
            commit_changes()
    
    print("\n" + "=" * 60)
    print("🎉 إعداد النشر مكتمل!")
    print("🎉 Deployment setup complete!")
    print()
    print("📋 الخطوات التالية:")
    print("📋 Next steps:")
    print("1. ارفع الكود إلى GitHub / Push code to GitHub")
    print("2. أنشئ حساب على Render / Create Render account")
    print("3. اتبع دليل النشر في DEPLOYMENT_GUIDE.md")
    print("   Follow deployment guide in DEPLOYMENT_GUIDE.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
