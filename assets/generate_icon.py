# assets/generate_icon.py — Genera el icono .ico/.png del teclado hack

import os
import math

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def generate_icon(output_dir: str, theme_color: str = "#00ff41"):
    """Genera icon.ico e icon.png en output_dir."""
    if not HAS_PIL:
        print("[icon] Pillow no instalado — omitiendo generación de icono.")
        return None

    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        img = _draw_icon(size, theme_color)
        images.append(img)

    ico_path = os.path.join(output_dir, "icon.ico")
    png_path = os.path.join(output_dir, "icon.png")

    # Guardar .ico con múltiples tamaños
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    # Guardar .png 256x256
    images[0].save(png_path, format="PNG")

    print(f"[icon] Generado: {ico_path}")
    print(f"[icon] Generado: {png_path}")
    return ico_path


def _draw_icon(size: int, color: str = "#00ff41"):
    """Dibuja el icono en el tamaño dado."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fondo redondeado
    margin = size // 12
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 6,
        fill=(10, 10, 10, 255),
        outline=_hex_to_rgb(color) + (220,),
        width=max(1, size // 32),
    )

    # Glow exterior (simulado con anillos)
    glow_color = _hex_to_rgb(color)
    for i in range(3, 0, -1):
        alpha = 40 + i * 15
        draw.rounded_rectangle(
            [margin - i, margin - i, size - margin + i, size - margin + i],
            radius=size // 6 + i,
            fill=None,
            outline=glow_color + (alpha,),
            width=1,
        )

    # Teclas mini en cuadrícula
    key_rows = 3
    key_cols = 5
    pad = size * 0.18
    kw = (size - pad * 2) / key_cols
    kh = (size - pad * 2) / (key_rows + 1.5)
    gap = size * 0.025

    for row in range(key_rows):
        for col in range(key_cols):
            x0 = pad + col * kw + gap
            y0 = pad + row * kh + gap + kh * 0.4
            x1 = x0 + kw - gap * 2
            y1 = y0 + kh - gap * 2
            # Sombra
            draw.rounded_rectangle(
                [x0 + 1, y0 + 1, x1 + 1, y1 + 1],
                radius=max(1, size // 40),
                fill=(0, 0, 0, 180),
            )
            # Tecla
            draw.rounded_rectangle(
                [x0, y0, x1, y1],
                radius=max(1, size // 40),
                fill=_hex_to_rgb(color) + (30,),
                outline=_hex_to_rgb(color) + (200,),
                width=max(1, size // 64),
            )

    # Barra espaciadora
    sb_y0 = pad + key_rows * kh + gap + kh * 0.4
    sb_y1 = sb_y0 + kh - gap * 2
    sb_x0 = pad + kw + gap
    sb_x1 = size - pad - kw - gap
    draw.rounded_rectangle(
        [sb_x0, sb_y0, sb_x1, sb_y1],
        radius=max(1, size // 40),
        fill=_hex_to_rgb(color) + (50,),
        outline=_hex_to_rgb(color) + (220,),
        width=max(1, size // 48),
    )

    # Punto de brillo central (efecto lens flare)
    if size >= 32:
        cx = int(size * 0.72)
        cy = int(size * 0.25)
        r = max(2, size // 16)
        for i in range(r, 0, -1):
            alpha = int(200 * (i / r) ** 2)
            draw.ellipse(
                [cx - i, cy - i, cx + i, cy + i],
                fill=_hex_to_rgb("#ffffff") + (alpha,)
            )

    return img


def _hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__))
    generate_icon(out, "#00ff41")
