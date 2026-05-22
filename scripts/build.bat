@echo off
chcp 65001 >nul
title PaperFlow Build
echo ========================================
echo   PaperFlow - Build Windows Installer
echo ========================================
echo.

:: Step 1: Build frontend
echo [1/4] Building frontend...
cd /d %~dp0frontend
call npx tsc --noEmit
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: TypeScript errors in frontend
    exit /b 1
)
call npx vite build
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: Vite build failed
    exit /b 1
)
echo Frontend build: OK
echo.

:: Step 2: Package with Electron Builder
echo [2/4] Packaging Electron app...
cd /d %~dp0electron
call npx electron-builder --win --x64
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: Electron build failed
    exit /b 1
)
echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
echo.
echo Installer: %~dp0electron\release\PaperFlow-Setup-0.1.0.exe
echo.
echo Prerequisites for running:
echo - Python 3.11+ installed and in PATH
echo - pip install -r backend\requirements.txt
echo.
pause
