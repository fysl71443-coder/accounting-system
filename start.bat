@echo off
echo ========================================
echo    نظام المحاسبة - Accounting System
echo ========================================
echo.
echo 🚀 بدء تشغيل الخادم...
echo 🚀 Starting server...
echo.

cd /d "D:\New folder\ACCOUNTS PROGRAM"

set SECRET_KEY=dev-secret-key-change-in-production
set DATABASE_URL=sqlite:///accounting.db
set FLASK_ENV=development
set FLASK_DEBUG=1

echo 📍 الخادم سيعمل على: http://localhost:5000
echo 📍 Server will run on: http://localhost:5000
echo.
echo.
echo 🛑 لإيقاف الخادم اضغط Ctrl+C
echo ========================================
echo.

python app.py

pause
