@echo off
echo 🚀 Flask Price List Application - Setup
echo ========================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check .env
if not exist ".env" (
    echo ⚙️  Creating .env file...
    (
        echo SECRET_KEY=change-this-secret-key-in-production
        echo DATABASE_URL=mysql+pymysql://root:password@localhost:3306/price_list_db
        echo FLASK_APP=app.py
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
    ) > .env
    echo ✅ .env file created
)

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Starting application...
echo 📍 Open: http://localhost:5000
echo 🛑 Press CTRL+C to stop
echo.

REM Run application
python app.py