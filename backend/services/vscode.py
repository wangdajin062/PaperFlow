import shutil
import subprocess
from pathlib import Path


def _find_vscode() -> str | None:
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


def open_file(file_path: str, line: int | None = None) -> dict:
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
        args.insert(1, "--goto")
        args.append(f"{path}:{line}")

    try:
        subprocess.Popen(args)
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
        subprocess.Popen([vscode, str(path)])
        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}
