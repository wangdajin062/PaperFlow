@echo off
echo PaperFlow E2E Test
echo ==================
echo.

:: 1. Start backend
echo [1/4] Starting backend...
start "PaperFlow-Backend" /B cmd /c "cd /d %~dp0..\backend && .venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8765 --log-level error"
timeout /t 3 /nobreak >nul

:: 2. Test health endpoint
echo [2/4] Testing health API...
curl -s http://127.0.0.1:8765/api/health
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: Backend not responding
    goto :cleanup
)
echo.

:: 3. Test workflow CRUD
echo [3/4] Testing workflow API...
curl -s -X POST http://127.0.0.1:8765/api/workflows -H "Content-Type: application/json" -d "{\"name\":\"E2E Test\",\"nodes\":[],\"edges\":[]}"
echo.
curl -s http://127.0.0.1:8765/api/workflows
echo.

:: 4. Test frontend build
echo [4/4] Checking frontend build...
cd /d %~dp0..\frontend
call npx tsc --noEmit
if %ERRORLEVEL% EQU 0 (
    echo Frontend TypeScript check: PASSED
) else (
    echo Frontend TypeScript check: FAILED
)

:cleanup
:: Stop backend
echo.
echo Stopping backend...
taskkill /f /fi "WINDOWTITLE eq PaperFlow-Backend" >nul 2>&1
echo Done.
