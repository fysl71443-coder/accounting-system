@echo off
echo ========================================
echo    نظام المحاسبة - Accounting System
echo ========================================
echo.
echo تشغيل النظام...
echo Starting system...
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    echo تفعيل البيئة الافتراضية...
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo إنشاء البيئة الافتراضية...
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo تثبيت المتطلبات...
    echo Installing requirements...
    pip install Flask Flask-SQLAlchemy Flask-Login
)

echo.
echo ========================================
echo النظام يعمل على: http://localhost:5000
echo System running on: http://localhost:5000
echo.
echo بيانات تسجيل الدخول:
echo Login credentials:
echo المستخدم / Username: admin
echo كلمة المرور / Password: admin123
echo.
echo لإيقاف النظام اضغط Ctrl+C
echo To stop system press Ctrl+C
echo ========================================
echo.

python app.py

pause
