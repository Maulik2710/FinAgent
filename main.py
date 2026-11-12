import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def find_python_with_uvicorn():
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python" / "Python312" / "python.exe",
        Path(r"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

def main():
    try:
        import uvicorn
    except ModuleNotFoundError:
        py312 = find_python_with_uvicorn()
        if py312 and py312 != sys.executable:
            print(f"[FinAgent] Automatically switching to Python 3.12 environment ({py312})...")
            args = [py312, str(Path(__file__).resolve())] + sys.argv[1:]
            sys.exit(subprocess.call(args))
        else:
            print("\n[ERROR] 'uvicorn' is not installed in the current Python environment.")
            print(f"Current interpreter: {sys.executable}")
            print("\nPlease run with Python 3.12 where your packages are installed:")
            print(r'& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" main.py')
            sys.exit(1)

    if "--streamlit" in sys.argv:
        from app.frontend.dashboard import main as streamlit_main
        streamlit_main()
    else:
        from app.api.server import app
        print("=" * 65)
        print("FinAgent — AI-Powered Portfolio Manager & Quantitative Analytics")
        print("Serving at: http://127.0.0.1:8000")
        print("=" * 65)
        uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
