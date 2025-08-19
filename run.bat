@echo off
echo ========================================
echo    Roblox Audio Browser Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

:: Display Python version
echo Detected Python version:
python --version
echo.

:: Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo Make sure you have the 'venv' module installed.
        echo Try: python -m pip install --upgrade pip
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

:: Check if requirements.txt exists
if not exist "requirements.txt" (
    echo Creating requirements.txt...
    echo pygame^>=2.0.0 > requirements.txt
)

:: Install requirements
echo Installing required packages...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install required packages!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Setup Complete! Starting Application
echo ========================================
echo.

:: Check if main script exists
if not exist "roblox_audio_browser.py" (
    echo ERROR: roblox_audio_browser.py not found in current directory!
    echo Please make sure all files are in the same folder.
    echo.
    pause
    exit /b 1
)

:: Run the application
echo Starting Roblox Audio Browser...
echo.
echo TIP: If you see pygame warnings, you can ignore them - they're harmless!
echo.
python roblox_audio_browser.py

:: Check if the application exited with an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo    Application Exited with Error
    echo ========================================
    echo If you're experiencing issues, please:
    echo 1. Check that all files are in the same directory
    echo 2. Ensure Python 3.7+ is installed
    echo 3. Try running: pip install pygame
    echo 4. Check the README.md for troubleshooting
    echo.
)

echo.
echo Application closed. Press any key to exit...
pause >nul
