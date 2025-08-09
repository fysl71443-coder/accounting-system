# PowerShell script to start the accounting system server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   نظام المحاسبة - Accounting System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 بدء تشغيل الخادم..." -ForegroundColor Green
Write-Host "🚀 Starting server..." -ForegroundColor Green
Write-Host ""

# Set working directory
Set-Location "D:\New folder\ACCOUNTS PROGRAM"

# Set environment variables
$env:SECRET_KEY = "dev-secret-key-change-in-production"
$env:DATABASE_URL = "sqlite:///accounting.db"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

Write-Host "📍 الخادم سيعمل على: http://localhost:5000" -ForegroundColor Yellow
Write-Host "📍 Server will run on: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host ""
Write-Host "🛑 لإيقاف الخادم اضغط Ctrl+C" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python app.py
}
catch {
    Write-Host "❌ خطأ في تشغيل الخادم: $_" -ForegroundColor Red
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "اضغط أي مفتاح للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
