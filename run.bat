@echo off
echo Starting Visitor Feedback Archive System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.7 or higher.
    exit /b 1
)

REM Check if requirements are installed
echo Checking requirements...
pip install -r requirements.txt

REM Initialize the database
echo Setting up the database...
python database/init_db.py

REM Start the Flask application
echo Starting Flask application...
python app.py

pause
