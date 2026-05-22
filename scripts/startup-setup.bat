@echo off
echo Adding PaperFlow to Windows startup...
set STARTUP_DIR="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set SCRIPT_PATH="%~dp0..\electron\node_modules\.bin\electron.cmd"
set WORK_DIR="%~dp0..\electron"

:: Create shortcut using PowerShell
powershell -Command ^
  $WshShell = New-Object -ComObject WScript.Shell; ^
  $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PaperFlow.lnk'); ^
  $Shortcut.TargetPath = '%PROGRAMFILES%\nodejs\node.exe'; ^
  $Shortcut.Arguments = '%WORK_DIR%\node_modules\.bin\electron %WORK_DIR%'; ^
  $Shortcut.WorkingDirectory = '%WORK_DIR%'; ^
  $Shortcut.Save()
echo Done. PaperFlow will start automatically on next boot.
