import subprocess
import shutil
from pathlib import Path
from typing import Optional


def _find_vscode() -> Optional[str]:
    """查找 VS Code 可执行文件路径"""
    candidates = [
        r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Users\wangd\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
        r"C:\Users\wangd\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    # 尝试从 PATH 查找
    return shutil.which("code")


def open_file(file_path: str, line: Optional[int] = None) -> dict:
    """在 VS Code 中打开文件"""
    vscode = _find_vscode()
    if not vscode:
        return {"success": False, "error": "VS Code not found"}

    path = Path(file_path).resolve()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")

    args = [vscode, str(path)]
    if line is not None:
        args.insert(1, f"--goto")
        args.append(f"{path}:{line}")

    try:
        subprocess.Popen(args, shell=True)
        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_folder(folder_path: str) -> dict:
    """在 VS Code 中打开文件夹"""
    vscode = _find_vscode()
    if not vscode:
        return {"success": False, "error": "VS Code not found"}

    path = Path(folder_path).resolve()
    path.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.Popen([vscode, str(path)], shell=True)
        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}
