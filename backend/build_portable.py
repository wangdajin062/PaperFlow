"""Create a portable Python bundle for Electron distribution."""
import os
import sys
import shutil
import subprocess
from pathlib import Path

BACKEND_DIR = Path(__file__).parent
BUNDLE_DIR = BACKEND_DIR / "dist-portable"
PYTHON_SRC = Path(r"C:\Users\wangd\AppData\Local\Programs\Python\Python314")


def main():
    if BUNDLE_DIR.exists():
        shutil.rmtree(BUNDLE_DIR)

    # Step 1: Copy Python runtime (exe + DLLs)
    python_dir = BUNDLE_DIR / "python"
    python_dir.mkdir(parents=True, exist_ok=True)

    for f in ["python.exe", "python3.dll", "python314.dll"]:
        shutil.copy2(PYTHON_SRC / f, python_dir / f)

    # Step 2: Copy compiled extension modules (DLLs/*.pyd) — essential for _socket, _ssl, etc.
    dlls_src = PYTHON_SRC / "DLLs"
    dlls_dst = python_dir / "DLLs"
    dlls_dst.mkdir(exist_ok=True)
    for f in dlls_src.iterdir():
        if f.suffix in (".pyd", ".dll") or f.is_file():
            shutil.copy2(f, dlls_dst / f.name)

    # Step 4: Copy stdlib zip (contains most of the standard library)
    stdlib_zip = PYTHON_SRC / "python314.zip"
    if stdlib_zip.exists():
        shutil.copy2(stdlib_zip, python_dir / "python314.zip")

    # Step 5: Copy minimal Lib (for remaining stdlib modules)
    lib_src = PYTHON_SRC / "Lib"
    lib_dst = python_dir / "Lib"
    shutil.copytree(
        lib_src, lib_dst,
        ignore=shutil.ignore_patterns(
            "test", "tests", "__pycache__", "*.pyc",
            "ensurepip", "turtledemo", "idlelib", "lib2to3",
            "site-packages",
        ),
    )

    # Step 6: Install dependencies into the bundle's site-packages
    site_packages = python_dir / "Lib" / "site-packages"
    print("Installing pip dependencies...")
    subprocess.run(
        [
            sys.executable, "-m", "pip", "install",
            "--target", str(site_packages),
            "-r", str(BACKEND_DIR / "requirements.txt"),
        ],
        check=True,
        capture_output=False,
    )

    # Step 7: Clean unnecessary files from site-packages
    for root, dirs, files in os.walk(site_packages):
        for d in dirs:
            if d in ("__pycache__", "tests", "test"):
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
        for f in files:
            if f.endswith(".pyc") and os.path.getsize(os.path.join(root, f)) == 0:
                os.remove(os.path.join(root, f))

    # Step 8: Copy our app source
    app_dst = BUNDLE_DIR / "app"
    shutil.copytree(
        BACKEND_DIR, app_dst,
        ignore=shutil.ignore_patterns(
            ".venv", "__pycache__", "*.pyc", "*.db",
            "dist-exe", "dist-portable", "tests", ".pytest_cache",
            "requirements-dev.txt", "backend.spec", "run_server.py",
        ),
        dirs_exist_ok=True,
    )

    # Step 9: Create run script
    run_script = BUNDLE_DIR / "run_backend.py"
    run_script.write_text(
        '"""Launcher: start uvicorn with bundled Python."""\n'
        "import sys, os\n"
        "sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))\n"
        "os.chdir(os.path.join(os.path.dirname(__file__), 'app'))\n"
        "import uvicorn\n"
        "from main import app\n"
        "uvicorn.run(app, host='127.0.0.1', port=8765, log_level='info')\n"
    )

    # Calculate total size
    total_size = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, dn, fns in os.walk(BUNDLE_DIR) for f in fns
    )
    print(f"\nBundle created at: {BUNDLE_DIR}")
    print(f"Size: {total_size / 1024 / 1024:.1f} MB")

    # Count files
    file_count = sum(1 for _ in BUNDLE_DIR.rglob("*") if _.is_file())
    print(f"Files: {file_count}")


if __name__ == "__main__":
    main()
