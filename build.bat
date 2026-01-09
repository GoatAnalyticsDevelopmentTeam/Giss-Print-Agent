@echo off
cd /d %~dp0
echo Initializing Giss Print Agent Build Process...

echo Installing requirements...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller is not installed.
    pause
    exit /b 1
)

echo Building GissPrintAgent.exe...
python -m PyInstaller --onefile --noconsole --name GissPrintAgent src/main.py

echo.
echo Build complete! The executable is in the 'dist' folder.
echo IMPORTANT: Place SumatraPDF.exe in the same folder as GissPrintAgent.exe.
pause
