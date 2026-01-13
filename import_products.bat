@echo off
echo ============================================
echo CSV to MySQL Import Script
echo ============================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if CSV file exists
if not exist "products_template.csv" (
    echo ❌ Error: products.csv not found
    echo.
    echo Please create products_template.csv file or specify path:
    echo   python import_csv.py C:\drive_D\Vitriproductos\price_list_app\products_template.csv
    pause
    exit /b 1
)

REM Run import
python import_csv.py products_template.csv

echo
echo Press any key to exit...
pause > nul