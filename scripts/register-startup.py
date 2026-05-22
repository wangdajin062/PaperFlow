"""Register PaperFlow to Windows auto-start."""
import os
import sys
import subprocess
from pathlib import Path


def register():
    project_root = Path(__file__).parent.parent
    electron_dir = project_root / "electron"
    startup_script = electron_dir / "start-paperflow.bat"

    bat_content = f"""@echo off
cd /d {electron_dir}
start "" "{electron_dir}\\node_modules\\.bin\\electron.cmd" "{electron_dir}"
"""
    startup_script.write_text(bat_content)

    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut_path = startup_dir / "PaperFlow.lnk"

    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
    $Shortcut.TargetPath = '{startup_script}'
    $Shortcut.WorkingDirectory = '{electron_dir}'
    $Shortcut.Save()
    """
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    print(f"PaperFlow added to startup: {shortcut_path}")


def unregister():
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut_path = startup_dir / "PaperFlow.lnk"
    if shortcut_path.exists():
        shortcut_path.unlink()
        print("Removed from startup")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "unregister":
        unregister()
    else:
        register()
