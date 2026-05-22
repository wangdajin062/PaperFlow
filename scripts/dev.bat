@echo off
echo Starting PaperFlow development environment...
echo.

:: Start backend
start "PaperFlow-Backend" cmd /c "cd /d %~dp0..\backend && python -m uvicorn main:app --reload --port 8765"

:: Start frontend
start "PaperFlow-Frontend" cmd /c "cd /d %~dp0..\frontend && npm run dev"

echo Backend starting on http://localhost:8765
echo Frontend starting on http://localhost:5173
