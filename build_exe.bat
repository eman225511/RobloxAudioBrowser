@echo off
echo Building Roblox Audio Browser executable...
echo.

REM Activate virtual environment and check if PyInstaller is installed
.venv\Scripts\python.exe -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing PyInstaller in virtual environment...
    .venv\Scripts\python.exe -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller. Please check your virtual environment.
        pause
        exit /b 1
    )
)

REM Using existing logo file

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

REM Build the executable
echo.
echo Building executable with PyInstaller using virtual environment...
echo Using existing logo: app_logo.ico
echo.

.venv\Scripts\pyinstaller.exe --onefile --windowed --icon=app_logo.ico --name="RobloxAudioBrowser" roblox_audio_browser.py

if errorlevel 1 (
    echo.
    echo Build failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\RobloxAudioBrowser.exe
echo.

REM Ask if user wants to run the executable
set /p run_exe="Do you want to run the executable now? (y/n): "
if /i "%run_exe%"=="y" (
    echo Running executable...
    start "" "dist\RobloxAudioBrowser.exe"
)

echo.
echo Press any key to exit...
pause >nul
