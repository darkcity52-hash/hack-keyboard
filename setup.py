# setup.py — Configuración inicial del Hack Keyboard

import os
import sys
import subprocess

def install_dependencies():
    print("[setup] Instalando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("[setup] ✓ Dependencias instaladas")

def generate_assets():
    print("[setup] Generando icono...")
    try:
        from assets.generate_icon import generate_icon
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        generate_icon(assets_dir, "#00ff41")
        print("[setup] ✓ Icono generado en assets/")
    except Exception as e:
        print(f"[setup] ⚠ No se pudo generar icono: {e}")

def create_desktop_shortcut():
    """Crea acceso directo en el escritorio (Windows/Linux)."""
    script_path = os.path.abspath("keyboard.py")
    python_path = sys.executable

    if sys.platform == "win32":
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "HackKeyboard.bat")
        with open(shortcut_path, "w") as f:
            f.write(f'@echo off\n"{python_path}" "{script_path}"\n')
        print(f"[setup] ✓ Acceso directo creado: {shortcut_path}")

    elif sys.platform.startswith("linux"):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        icon_path = os.path.abspath("assets/icon.png")
        shortcut_path = os.path.join(desktop, "HackKeyboard.desktop")
        content = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=Hack Keyboard\n"
            f"Exec={python_path} {script_path}\n"
            f"Icon={icon_path}\n"
            "Terminal=false\n"
            "Categories=Utility;\n"
        )
        os.makedirs(desktop, exist_ok=True)
        with open(shortcut_path, "w") as f:
            f.write(content)
        os.chmod(shortcut_path, 0o755)
        print(f"[setup] ✓ Acceso directo creado: {shortcut_path}")
    else:
        print("[setup] Acceso directo no disponible en esta plataforma")

if __name__ == "__main__":
    print("=" * 50)
    print("   HACK KEYBOARD v2.0 — Setup")
    print("=" * 50)
    install_dependencies()
    generate_assets()
    create_desktop_shortcut()
    print("\n[setup] ✅ Todo listo. Ejecuta: python keyboard.py")
