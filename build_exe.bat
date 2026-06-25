@echo off
echo ========================================
echo Building executables with .venv
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv virtual environment not found!
    echo Please make sure .venv folder exists in project root.
    echo.
    pause
    exit /b 1
)

echo [1/4] Virtual environment found
echo Done!
echo.

REM Check if PyInstaller is installed - use venv python directly
echo [2/4] Checking PyInstaller...
.venv\Scripts\python.exe -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found, installing...
    .venv\Scripts\pip.exe install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
    echo Done!
) else (
    echo PyInstaller is already installed
)
echo.

REM Build predict - use venv python directly
echo [3/4] Building predict.exe... (this may take several minutes)
.venv\Scripts\pyinstaller.exe --clean predict.spec > build_predict.log 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Failed to build predict.exe!
    echo See build_predict.log for details.
    echo.
    pause
    exit /b 1
)
echo Done!
echo.

REM Build process_result - use venv python directly
echo [4/4] Building process_result.exe...
.venv\Scripts\pyinstaller.exe --clean process_result.spec > build_process_result.log 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Failed to build process_result.exe!
    echo See build_process_result.log for details.
    echo.
    pause
    exit /b 1
)
echo Done!
echo.

REM Clean up build folder
echo Cleaning up temporary build files...
if exist "build" rmdir /s /q "build"
echo Done!
echo.

echo ========================================
echo Build complete!
echo Output locations:
echo   - dist\predict\
echo   - dist\process_result.exe
echo ========================================
echo.
pause
