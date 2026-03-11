# keyboard.py — HACK KEYBOARD v2.0
# Teclado virtual futurista con temas, sonidos y personalización completa
# Optimizado para OnePlus 11 5G (1080x2412 px, Android 16)

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

from themes.themes import THEMES, DEFAULT_THEME
import sounds.sound_engine as SFX

# ── Layout completo del teclado ───────────────────────────────────────────────
ROWS = [
    [("ESC",1.2),("F1",1),("F2",1),("F3",1),("F4",1),
     ("F5",1),("F6",1),("F7",1),("F8",1),
     ("F9",1),("F10",1),("F11",1),("F12",1),
     ("PrtSc",1.3),("ScrLk",1.3),("Pause",1.3)],

    [("`",1),("1",1),("2",1),("3",1),("4",1),("5",1),("6",1),
     ("7",1),("8",1),("9",1),("0",1),("-",1),("=",1),("⌫",2)],

    [("Tab",1.5),("Q",1),("W",1),("E",1),("R",1),("T",1),("Y",1),
     ("U",1),("I",1),("O",1),("P",1),("[",1),("]",1),("\\",1.5)],

    [("CapsLk",1.8),("A",1),("S",1),("D",1),("F",1),("G",1),("H",1),
     ("J",1),("K",1),("L",1),(";",1),("'",1),("Enter",2.2)],

    [("⇧Shift",2.5),("Z",1),("X",1),("C",1),("V",1),("B",1),("N",1),
     ("M",1),(",",1),(".",1),("/",1),("⇧Shift",2.5)],

    [("Ctrl",1.5),("❖Win",1.3),("Alt",1.2),("SPACE",6.2),
     ("Alt",1.2),("Fn",1.1),("▤Menu",1.2),("Ctrl",1.5)],
]

SHIFT_MAP = {
    "`":"~","1":"!","2":"@","3":"#","4":"$","5":"%","6":"^",
    "7":"&","8":"*","9":"(","0":")","-":"_","=":"+",
    "[":"{","]":"}","\\":"|",";":":","'":'"',",":"<",".":">","/":"?",
}

SHORTCUTS = {
    ("Ctrl","C"):  "Copiar",
    ("Ctrl","V"):  "Pegar",
    ("Ctrl","X"):  "Cortar",
    ("Ctrl","Z"):  "Deshacer",
    ("Ctrl","Y"):  "Rehacer",
    ("Ctrl","A"):  "Seleccionar todo",
    ("Ctrl","S"):  "Guardar",
    ("Ctrl","N"):  "Nuevo",
    ("Ctrl","F"):  "Buscar",
    ("Alt","F4"):  "Cerrar",
}

MODIFIER_KEYS = {"Ctrl","Alt","⇧Shift","CapsLk","Fn","❖Win","▤Menu"}
FUNCTION_KEYS = {f"F{i}" for i in range(1, 13)}
SYSTEM_KEYS   = {"ESC","PrtSc","ScrLk","Pause","❖Win","▤Menu"}

# Dimensiones base (escala para OnePlus 11 5G 1080×2412 → ~412×915 dp)
BASE_UNIT   = 38   # px por unidad de tecla
BASE_HEIGHT = 2    # filas de texto
FONT_SIZES  = [7, 8, 9, 10, 11, 12, 14]
KEY_SIZES   = list(range(28, 58, 2))   # 28..56 px


class HackKeyboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⌨  HACK KEYBOARD")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)

        # ── Estado ──
        self.shift_on  = False
        self.caps_on   = False
        self.ctrl_on   = False
        self.alt_on    = False
        self.fn_on     = False
        self.sound_on  = True

        self.undo_stack  = []
        self.redo_stack  = []
        self._last_text  = ""

        # ── Config personalizable ──
        self.current_theme   = DEFAULT_THEME
        self.key_unit        = tk.IntVar(value=BASE_UNIT)
        self.font_size       = tk.IntVar(value=9)
        self.text_area_lines = tk.IntVar(value=6)
        self.kb_width_scale  = tk.DoubleVar(value=1.0)
        self.kb_height_scale = tk.DoubleVar(value=1.0)

        self.key_buttons = {}   # label → [Button]

        self._load_icon()
        self._build_menu()
        self._build_ui()
        self._bind_physical_keyboard()

        # Aplicar tema inicial
        self._apply_theme(self.current_theme)

    # ─── Icono ────────────────────────────────────────────────────────────────

    def _load_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if not os.path.exists(icon_path):
                from assets.generate_icon import generate_icon
                icon_path = generate_icon(
                    os.path.join(os.path.dirname(__file__), "assets"),
                    THEMES[DEFAULT_THEME]["glow"]
                )
            if icon_path and os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

    # ─── Menú principal ───────────────────────────────────────────────────────

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg="#0d1a0d", fg="#00ff41",
                          activebackground="#00ff41", activeforeground="#000",
                          tearoff=False)

        # ── Temas ──
        theme_menu = tk.Menu(menubar, tearoff=False,
                             bg="#0d1a0d", fg="#00ff41",
                             activebackground="#00ff41", activeforeground="#000")
        for name in THEMES:
            theme_menu.add_command(
                label=name,
                command=lambda n=name: self._apply_theme(n)
            )
        menubar.add_cascade(label="🎨 Temas", menu=theme_menu)

        # ── Tamaño de teclas ──
        keysize_menu = tk.Menu(menubar, tearoff=False,
                               bg="#0d1a0d", fg="#00ff41",
                               activebackground="#00ff41", activeforeground="#000")
        for sz in KEY_SIZES:
            keysize_menu.add_command(
                label=f"{sz}px",
                command=lambda s=sz: self._set_key_size(s)
            )
        menubar.add_cascade(label="⬛ Teclas", menu=keysize_menu)

        # ── Fuente ──
        font_menu = tk.Menu(menubar, tearoff=False,
                            bg="#0d1a0d", fg="#00ff41",
                            activebackground="#00ff41", activeforeground="#000")
        for fsz in FONT_SIZES:
            font_menu.add_command(
                label=f"{fsz}pt",
                command=lambda f=fsz: self._set_font_size(f)
            )
        menubar.add_cascade(label="🔤 Fuente", menu=font_menu)

        # ── Dimensiones del teclado ──
        dim_menu = tk.Menu(menubar, tearoff=False,
                           bg="#0d1a0d", fg="#00ff41",
                           activebackground="#00ff41", activeforeground="#000")

        # Ancho
        width_menu = tk.Menu(dim_menu, tearoff=False,
                             bg="#0d1a0d", fg="#00ff41",
                             activebackground="#00ff41", activeforeground="#000")
        for pct in [70, 80, 90, 100, 110, 120]:
            width_menu.add_command(
                label=f"{pct}%",
                command=lambda p=pct: self._set_scale("width", p / 100)
            )
        dim_menu.add_cascade(label="↔ Ancho", menu=width_menu)

        # Alto
        height_menu = tk.Menu(dim_menu, tearoff=False,
                              bg="#0d1a0d", fg="#00ff41",
                              activebackground="#00ff41", activeforeground="#000")
        for pct in [70, 80, 90, 100, 110, 120]:
            height_menu.add_command(
                label=f"{pct}%",
                command=lambda p=pct: self._set_scale("height", p / 100)
            )
        dim_menu.add_cascade(label="↕ Alto", menu=height_menu)

        # Líneas área de texto
        lines_menu = tk.Menu(dim_menu, tearoff=False,
                             bg="#0d1a0d", fg="#00ff41",
                             activebackground="#00ff41", activeforeground="#000")
        for ln in [3, 4, 5, 6, 8, 10, 12]:
            lines_menu.add_command(
                label=f"{ln} líneas",
                command=lambda l=ln: self._set_text_lines(l)
            )
        dim_menu.add_cascade(label="📄 Área de texto", menu=lines_menu)

        menubar.add_cascade(label="📐 Dimensiones", menu=dim_menu)

        # ── Sonido ──
        sound_menu = tk.Menu(menubar, tearoff=False,
                             bg="#0d1a0d", fg="#00ff41",
                             activebackground="#00ff41", activeforeground="#000")
        sound_menu.add_command(label="🔊 Activar sonido",  command=lambda: self._set_sound(True))
        sound_menu.add_command(label="🔇 Silenciar",       command=lambda: self._set_sound(False))
        menubar.add_cascade(label="🔊 Sonido", menu=sound_menu)

        # ── Ayuda ──
        help_menu = tk.Menu(menubar, tearoff=False,
                            bg="#0d1a0d", fg="#00ff41",
                            activebackground="#00ff41", activeforeground="#000")
        help_menu.add_command(label="Atajos de teclado", command=self._show_shortcuts)
        help_menu.add_command(label="Acerca de",         command=self._show_about)
        menubar.add_cascade(label="❓ Ayuda", menu=help_menu)

        self.root.config(menu=menubar)

    # ─── UI principal ─────────────────────────────────────────────────────────

    def _build_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill="both", expand=True)

        # Título
        self.title_label = tk.Label(
            self.main_frame,
            text="[ HACK KEYBOARD v2.0 ]",
            bg="#0a0a0a", fg="#00ff41",
            font=("Courier New", 15, "bold")
        )
        self.title_label.pack(pady=(10, 4))

        # Área de texto
        self.text_outer = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.text_outer.pack(padx=14, pady=(0, 6), fill="x")

        self.display = tk.Text(
            self.text_outer,
            height=self.text_area_lines.get(),
            width=72,
            bg="#050f05", fg="#00ff41",
            insertbackground="#00ff41",
            font=("Courier New", 11),
            relief="flat", bd=0,
            padx=10, pady=8,
            wrap="word",
            undo=True,
        )
        self.display.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(
            self.text_outer, command=self.display.yview,
            bg="#003300", troughcolor="#050f05",
        )
        self.scrollbar.pack(side="right", fill="y")
        self.display.configure(yscrollcommand=self.scrollbar.set)

        # Barra de estado
        self.status_var = tk.StringVar(value="  ▶ READY")
        self.status_bar = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            bg="#001a00", fg="#00cc33",
            font=("Courier New", 8),
            anchor="w", padx=10,
        )
        self.status_bar.pack(fill="x", padx=14)

        # Indicadores LED
        self.ind_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.ind_frame.pack(pady=(5, 2))
        self.ind_caps  = self._make_indicator("CAPS")
        self.ind_shift = self._make_indicator("SHIFT")
        self.ind_ctrl  = self._make_indicator("CTRL")
        self.ind_alt   = self._make_indicator("ALT")
        self.ind_fn    = self._make_indicator("FN")
        self.ind_sound = self._make_indicator("SND")
        self._indicator_on(self.ind_sound)   # sonido ON por defecto

        # Teclado
        self.kb_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.kb_frame.pack(padx=14, pady=(4, 12))
        self._render_keyboard()

    def _make_indicator(self, text):
        lbl = tk.Label(
            self.ind_frame, text=text, width=5,
            bg="#001100", fg="#004400",
            font=("Courier New", 7, "bold"),
            relief="groove", bd=1
        )
        lbl.pack(side="left", padx=2)
        return lbl

    def _indicator_on(self, lbl):
        t = THEMES[self.current_theme]
        lbl.configure(bg=t["ind_on_bg"], fg=t["ind_on_fg"])

    def _indicator_off(self, lbl):
        t = THEMES[self.current_theme]
        lbl.configure(bg=t["ind_off_bg"], fg=t["ind_off_fg"])

    # ─── Render del teclado ───────────────────────────────────────────────────

    def _render_keyboard(self):
        # Limpiar
        for w in self.kb_frame.winfo_children():
            w.destroy()
        self.key_buttons.clear()

        t   = THEMES[self.current_theme]
        u   = int(self.key_unit.get() * self.kb_width_scale.get())
        h   = int(self.key_unit.get() * self.kb_height_scale.get() * 0.52)
        fsz = self.font_size.get()
        kfont = tkfont.Font(family="Courier New", size=fsz, weight="bold")

        for row_data in ROWS:
            row_frame = tk.Frame(self.kb_frame, bg="#0a0a0a")
            row_frame.pack(anchor="w", pady=1)

            for label, width_mult in row_data:
                w_px = max(1, int(width_mult * u // 10))
                is_mod = any(m in label for m in ["Shift","Ctrl","Alt","Fn","CapsLk","Win","Menu"])
                bg = t["key_mod_bg"] if is_mod else t["key_bg"]
                fg = t["key_mod_fg"] if is_mod else t["key_fg"]

                btn = tk.Button(
                    row_frame,
                    text=label,
                    width=w_px,
                    height=h,
                    bg=bg,
                    fg=fg,
                    activebackground=t["key_active_bg"],
                    activeforeground=t["key_active_fg"],
                    relief="raised",
                    bd=1,
                    font=kfont,
                    cursor="hand2",
                    command=lambda l=label: self._on_key_click(l),
                )
                btn.pack(side="left", padx=1)
                self.key_buttons.setdefault(label, []).append(btn)

    # ─── Lógica de teclas ─────────────────────────────────────────────────────

    def _on_key_click(self, label):
        self._flash_key(label)

        # Modificadores
        if "CapsLk" in label:
            self.caps_on = not self.caps_on
            (self._indicator_on if self.caps_on else self._indicator_off)(self.ind_caps)
            SFX.play("modifier")
            self._set_status(f"  CAPS LOCK {'ON' if self.caps_on else 'OFF'}")
            return

        if "Shift" in label:
            self.shift_on = not self.shift_on
            (self._indicator_on if self.shift_on else self._indicator_off)(self.ind_shift)
            SFX.play("modifier")
            return

        if "Ctrl" in label:
            self.ctrl_on = not self.ctrl_on
            (self._indicator_on if self.ctrl_on else self._indicator_off)(self.ind_ctrl)
            SFX.play("modifier")
            return

        if "Alt" in label:
            self.alt_on = not self.alt_on
            (self._indicator_on if self.alt_on else self._indicator_off)(self.ind_alt)
            SFX.play("modifier")
            return

        if "Fn" in label:
            self.fn_on = not self.fn_on
            (self._indicator_on if self.fn_on else self._indicator_off)(self.ind_fn)
            SFX.play("modifier")
            return

        # Atajos Ctrl+X
        base_label = label.replace("⇧","").replace("❖","").replace("▤","").strip()
        if self.ctrl_on and base_label not in ("Ctrl","Alt","Shift"):
            shortcut = ("Ctrl", base_label.upper())
            if shortcut in SHORTCUTS:
                SFX.play("shortcut")
                self._execute_shortcut(shortcut, base_label.upper())
                self.ctrl_on = False
                self._indicator_off(self.ind_ctrl)
                return

        if self.alt_on and base_label not in ("Ctrl","Alt","Shift"):
            shortcut = ("Alt", base_label)
            if shortcut in SHORTCUTS:
                SFX.play("shortcut")
                self._execute_shortcut(shortcut, base_label)
                self.alt_on = False
                self._indicator_off(self.ind_alt)
                return

        # Teclas de acción
        if "⌫" in label:
            SFX.play("backspace")
            self._backspace()
            return
        if label == "Enter":
            SFX.play("enter")
            self._save_undo()
            self._insert_text("\n")
            return
        if label == "Tab":
            SFX.play("key")
            self._save_undo()
            self._insert_text("    ")
            return
        if "SPACE" in label:
            SFX.play("space")
            self._save_undo()
            self._insert_text(" ")
            return
        if base_label in SYSTEM_KEYS or base_label.startswith("F") and base_label[1:].isdigit():
            SFX.play("modifier")
            self._set_status(f"  [{base_label}] presionado")
            return

        # Carácter normal
        char = base_label
        if len(char) == 1:
            if self.shift_on:
                char = SHIFT_MAP.get(char, char.upper())
                self.shift_on = False
                self._indicator_off(self.ind_shift)
            elif self.caps_on and char.isalpha():
                char = char.upper()
            else:
                char = char.lower() if char.isalpha() else char

            SFX.play("key")
            self._save_undo()
            self._insert_text(char)

    def _execute_shortcut(self, shortcut, key):
        name = SHORTCUTS.get(shortcut, "")
        self._set_status(f"  ⚡ {shortcut[0]}+{key}  →  {name}")
        actions = {
            "C": self.copy,
            "V": self.paste,
            "X": self.cut,
            "Z": self.undo,
            "Y": self.redo,
            "A": self.select_all,
            "S": self.save_text,
            "N": self.new_file,
            "F": self.find_text,
            "F4": lambda: self.root.destroy(),
        }
        fn = actions.get(key)
        if fn:
            fn()

    # ─── Acciones de texto ────────────────────────────────────────────────────

    def _insert_text(self, char):
        self.display.insert(tk.INSERT, char)
        self.display.see(tk.INSERT)

    def _backspace(self):
        try:
            if self.display.tag_ranges(tk.SEL):
                self._save_undo()
                self.display.delete(tk.SEL_FIRST, tk.SEL_LAST)
            else:
                pos = self.display.index(tk.INSERT)
                if pos != "1.0":
                    self._save_undo()
                    self.display.delete(f"{pos} -1c", pos)
        except tk.TclError:
            pass

    def _save_undo(self):
        content = self.display.get("1.0", tk.END)
        if self.undo_stack and self.undo_stack[-1] == content:
            return
        self.undo_stack.append(content)
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def copy(self):
        try:
            text = self.display.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._set_status("  📋 Copiado al portapapeles")
        except tk.TclError:
            self._set_status("  ⚠ Nada seleccionado")

    def paste(self):
        try:
            text = self.root.clipboard_get()
            self._save_undo()
            self.display.insert(tk.INSERT, text)
            self._set_status("  📋 Pegado desde portapapeles")
        except tk.TclError:
            self._set_status("  ⚠ Portapapeles vacío")

    def cut(self):
        try:
            text = self.display.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._save_undo()
            self.display.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self._set_status("  ✂ Cortado")
        except tk.TclError:
            self._set_status("  ⚠ Nada seleccionado")

    def undo(self):
        if self.undo_stack:
            current = self.display.get("1.0", tk.END)
            self.redo_stack.append(current)
            prev = self.undo_stack.pop()
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", prev.rstrip("\n"))
            self._set_status("  ↩ Deshacer")
        else:
            SFX.play("error")
            self._set_status("  ⚠ Nada que deshacer")

    def redo(self):
        if self.redo_stack:
            self._save_undo()
            nxt = self.redo_stack.pop()
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", nxt.rstrip("\n"))
            self._set_status("  ↪ Rehacer")
        else:
            SFX.play("error")
            self._set_status("  ⚠ Nada que rehacer")

    def select_all(self):
        self.display.tag_add(tk.SEL, "1.0", tk.END)
        self._set_status("  ☐ Todo seleccionado")

    def save_text(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.display.get("1.0", tk.END))
            self._set_status(f"  💾 Guardado: {os.path.basename(path)}")

    def new_file(self):
        if messagebox.askyesno("Nuevo", "¿Borrar el texto actual?"):
            self._save_undo()
            self.display.delete("1.0", tk.END)
            self._set_status("  📄 Nuevo archivo")

    def find_text(self):
        term = simpledialog.askstring("Buscar", "Texto a buscar:")
        if not term:
            return
        content = self.display.get("1.0", tk.END)
        idx = content.lower().find(term.lower())
        if idx >= 0:
            # Convertir índice lineal a índice tkinter
            lines = content[:idx].split("\n")
            row = len(lines)
            col = len(lines[-1])
            self.display.mark_set(tk.INSERT, f"{row}.{col}")
            self.display.tag_remove(tk.SEL, "1.0", tk.END)
            self.display.tag_add(tk.SEL, f"{row}.{col}", f"{row}.{col+len(term)}")
            self.display.see(tk.INSERT)
            self._set_status(f"  🔍 '{term}' encontrado")
        else:
            SFX.play("error")
            self._set_status(f"  ⚠ '{term}' no encontrado")

    # ─── Personalización ──────────────────────────────────────────────────────

    def _apply_theme(self, name):
        if name not in THEMES:
            return
        self.current_theme = name
        t = THEMES[name]

        self.root.configure(bg=t["bg"])
        self.main_frame.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["title_fg"])
        self.text_outer.configure(bg=t["bg"])
        self.display.configure(
            bg=t["text_bg"], fg=t["text_fg"],
            insertbackground=t["cursor"]
        )
        self.scrollbar.configure(bg=t["scrollbar"], troughcolor=t["text_bg"])
        self.status_bar.configure(bg=t["status_bg"], fg=t["status_fg"])
        self.ind_frame.configure(bg=t["bg"])
        self.kb_frame.configure(bg=t["bg"])

        # Indicadores
        for ind, state in [
            (self.ind_caps,  self.caps_on),
            (self.ind_shift, self.shift_on),
            (self.ind_ctrl,  self.ctrl_on),
            (self.ind_alt,   self.alt_on),
            (self.ind_fn,    self.fn_on),
            (self.ind_sound, self.sound_on),
        ]:
            ind.configure(bg=t["bg"])
            (self._indicator_on if state else self._indicator_off)(ind)

        # Re-render teclado con nuevo tema
        self._render_keyboard()
        self._set_status(f"  🎨 Tema: {name}")

    def _set_key_size(self, size):
        self.key_unit.set(size)
        self._render_keyboard()
        self._set_status(f"  Tamaño de tecla: {size}px")

    def _set_font_size(self, size):
        self.font_size.set(size)
        self._render_keyboard()
        self.display.configure(font=("Courier New", max(9, size + 1)))
        self._set_status(f"  Fuente: {size}pt")

    def _set_scale(self, axis, value):
        if axis == "width":
            self.kb_width_scale.set(value)
        else:
            self.kb_height_scale.set(value)
        self._render_keyboard()
        self._set_status(f"  {axis.capitalize()}: {int(value*100)}%")

    def _set_text_lines(self, lines):
        self.text_area_lines.set(lines)
        self.display.configure(height=lines)
        self._set_status(f"  Área de texto: {lines} líneas")

    def _set_sound(self, state):
        self.sound_on = state
        SFX.set_enabled(state)
        (self._indicator_on if state else self._indicator_off)(self.ind_sound)
        self._set_status(f"  Sonido: {'ON 🔊' if state else 'OFF 🔇'}")

    # ─── Flash de tecla ───────────────────────────────────────────────────────

    def _flash_key(self, label):
        t = THEMES[self.current_theme]
        btns = self.key_buttons.get(label, [])
        for btn in btns:
            btn.configure(bg=t["key_active_bg"], fg=t["key_active_fg"])
        is_mod = any(m in label for m in ["Shift","Ctrl","Alt","Fn","CapsLk","Win","Menu"])
        restore_bg = t["key_mod_bg"] if is_mod else t["key_bg"]
        restore_fg = t["key_mod_fg"] if is_mod else t["key_fg"]
        self.root.after(120, lambda: [
            b.configure(bg=restore_bg, fg=restore_fg)
            for b in btns if b.winfo_exists()
        ])

    # ─── Estado ───────────────────────────────────────────────────────────────

    def _set_status(self, msg):
        self.status_var.set(msg)
        self.root.after(3000, lambda: self.status_var.set("  ▶ READY"))

    # ─── Teclado físico ───────────────────────────────────────────────────────

    def _bind_physical_keyboard(self):
        self.root.bind("<KeyPress>", self._on_physical_key)

    def _on_physical_key(self, event):
        char = event.char
        keysym = event.keysym

        if keysym == "BackSpace":
            SFX.play("backspace")
            self._backspace()
        elif keysym == "Return":
            SFX.play("enter")
            self._save_undo()
            self._insert_text("\n")
        elif keysym == "Tab":
            SFX.play("key")
            self._save_undo()
            self._insert_text("    ")
        elif char and char.isprintable():
            SFX.play("key")
            self._save_undo()
            self._insert_text(char)

        # Sincronizar Ctrl físico con indicador
        if event.state & 0x4:  # Ctrl held
            pass

    # ─── Ayuda ────────────────────────────────────────────────────────────────

    def _show_shortcuts(self):
        t = THEMES[self.current_theme]
        win = tk.Toplevel(self.root)
        win.title("Atajos de teclado")
        win.configure(bg=t["bg"])
        txt = "\n".join(f"  {k[0]}+{k[1]:<4}  →  {v}" for k, v in SHORTCUTS.items())
        tk.Label(win, text="[ ATAJOS DISPONIBLES ]",
                 bg=t["bg"], fg=t["title_fg"],
                 font=("Courier New", 11, "bold")).pack(pady=8)
        tk.Label(win, text=txt, justify="left",
                 bg=t["bg"], fg=t["text_fg"],
                 font=("Courier New", 10)).pack(padx=20, pady=(0, 12))

    def _show_about(self):
        t = THEMES[self.current_theme]
        win = tk.Toplevel(self.root)
        win.title("Acerca de")
        win.configure(bg=t["bg"])
        info = (
            "HACK KEYBOARD v2.0\n\n"
            "Teclado virtual futurista\n"
            "Construido con Python + Tkinter\n\n"
            "Optimizado para OnePlus 11 5G\n"
            "Resolución: 1080×2412 (Android 16)\n\n"
            "github.com/tu-usuario/hack-keyboard"
        )
        tk.Label(win, text=info, justify="center",
                 bg=t["bg"], fg=t["text_fg"],
                 font=("Courier New", 10)).pack(padx=24, pady=16)

    # ─── Arranque ─────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = HackKeyboard()
    app.run()
