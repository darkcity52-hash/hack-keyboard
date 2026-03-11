# ⌨ HACK KEYBOARD v2.0

> Teclado virtual futurista construido en Python + Tkinter  
> Optimizado para **OnePlus 11 5G** (1080×2412px · Android 16)

![Python](https://img.shields.io/badge/Python-3.10%2B-00ff41?style=flat-square&logo=python&logoColor=white&labelColor=0a0a0a)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-00ff41?style=flat-square&labelColor=0a0a0a)
![License](https://img.shields.io/badge/license-MIT-00ff41?style=flat-square&labelColor=0a0a0a)

---

## 🚀 Características

| Función | Descripción |
|---|---|
| 🎨 **5 Temas visuales** | Matrix, Cyberpunk, Blood Red, Ice Cold, Amber Terminal |
| 🔊 **Sonidos futuristas** | Generados por código (numpy) — sin archivos externos |
| ⬛ **Teclas ajustables** | Tamaño de 28px a 56px desde el menú |
| 🔤 **Fuente ajustable** | 7pt a 14pt desde el menú |
| 📐 **Dimensiones** | Ancho, alto y área de texto proporcionales |
| ⌨ **Teclado físico** | Sincronizado con el virtual |
| 📋 **Atajos completos** | Ctrl+C/V/X/Z/Y/A/S/N/F |
| 🖥 **Icono de escritorio** | Generado automáticamente con Pillow |

---

## 📦 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/hack-keyboard.git
cd hack-keyboard

# 2. Setup automático (instala deps + genera icono + acceso directo)
python setup.py

# 3. Ejecutar
python keyboard.py
```

### Instalación manual de dependencias
```bash
pip install -r requirements.txt
```

En Linux también necesitas:
```bash
sudo apt install python3-tk
```

---

## 🗂 Estructura del proyecto

```
hack-keyboard/
├── keyboard.py              # App principal
├── setup.py                 # Instalador automático
├── requirements.txt
├── README.md
├── themes/
│   ├── __init__.py
│   └── themes.py            # Todos los temas de color
├── sounds/
│   ├── __init__.py
│   └── sound_engine.py      # Motor de sonidos (numpy)
└── assets/
    ├── __init__.py
    ├── generate_icon.py     # Generador de icono .ico/.png
    ├── icon.ico             # Generado en setup
    └── icon.png             # Generado en setup
```

---

## 🎨 Temas disponibles

| Nombre | Colores |
|---|---|
| **Matrix** | Verde neón `#00ff41` / Negro |
| **Cyberpunk** | Cyan `#00eeff` / Magenta `#ff00aa` |
| **Blood Red** | Rojo `#ff2200` / Negro |
| **Ice Cold** | Cyan frío `#00cfff` / Azul profundo |
| **Amber Terminal** | Ámbar `#ffaa00` / Negro |

---

## ⌨ Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl+C` | Copiar |
| `Ctrl+V` | Pegar |
| `Ctrl+X` | Cortar |
| `Ctrl+Z` | Deshacer |
| `Ctrl+Y` | Rehacer |
| `Ctrl+A` | Seleccionar todo |
| `Ctrl+S` | Guardar archivo |
| `Ctrl+N` | Nuevo archivo |
| `Ctrl+F` | Buscar texto |
| `Alt+F4` | Cerrar |

---

## 📱 OnePlus 11 5G — Notas de uso

- Pantalla: **1080×2412px** (ratio 20:9)
- Escala sugerida: tamaño de tecla **34px**, fuente **8pt**
- Para mejor ajuste usa **Dimensiones → Ancho: 90%**

---

## 📄 Licencia

MIT © 2025 — Hack Keyboard Project
