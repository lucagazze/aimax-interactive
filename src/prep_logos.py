# -*- coding: utf-8 -*-
"""
Prepara los logos de los clientes de AIMAX para el carrusel, EN COLOR.

Origen de cada archivo (todos de fuentes oficiales, ninguno recreado a mano):
  ypf        upload.wikimedia.org/.../YPF_S.A._logo.svg
  terminal6  terminal6.com.ar/resources/original/logos/logo.png
  odesur     odesur.org — LOGO-ODESUR.png
  eis        eis.unl.edu.ar — industrial_2-1.svg
  tecnoteca  facebook.com/tecnotecarosario — foto de perfil 720x720
  cimaes     facebook.com/cimaes.marcelloni — foto de perfil 720x720
  baravalle  baravalle-granados.com.ar — captura del wordmark del header

FALTA: Molino Dos Hermanos. No tiene dominio, ni Instagram, ni Facebook.
Hay que pedirle el archivo a Alejo.

Tres modos según cómo venga el original:
  directo   ya viene en color y con transparencia: solo se recorta y escala.
  blanco    viene sobre fondo BLANCO opaco (las fotos de perfil de Facebook).
            Se calcula el alfa por distancia al blanco y se despremultiplica,
            así el color queda limpio y no lavado sobre el borde.
  tinta     el logo es BLANCO sobre fondo oscuro y no existe versión en color
            (EIS y Baravalle). Se saca el alfa de la luminancia y se pinta del
            color de texto de la página: es la variante oscura del wordmark.
"""
import os
import numpy as np
from PIL import Image

SRC = (r"C:\Users\lucag\AppData\Local\Temp\claude\c--Users-lucag--claude"
       r"\6a3b4ef6-9780-4a03-8b1c-f4fff44207c0\scratchpad\logos")
PNG = SRC + "_png"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

TINTA = (29, 29, 31)            # #1d1d1f, el mismo negro del texto de la página

TRABAJOS = [
    (PNG, "ypf.png",            "logo-ypf.png",       "directo", 300),
    (PNG, "terminal6.png",      "logo-terminal6.png", "directo", 200),
    (PNG, "odesur.png",         "logo-odesur.png",    "directo", 220),
    (PNG, "eis2.png",           "logo-eis.png",       "tinta",   340),
    (SRC, "tecnoteca_fb.jpg",   "logo-tecnoteca.png", "blanco",  200),
    (SRC, "cimaes_fb.jpg",      "logo-cimaes.png",    "blanco",  260),
    (SRC, "_baravalle_raw.png", "logo-baravalle.png", "tinta",   520),
]


def recortar(im):
    caja = im.getbbox()
    return im.crop(caja) if caja else im


def directo(im):
    return im


def blanco(im):
    """Saca el fondo blanco y despremultiplica para recuperar el color real."""
    a = np.array(im).astype(np.float32)
    rgb = a[..., :3]
    # cuánto se aleja el pixel del blanco, por el canal que más se aleja
    alfa = (255.0 - rgb.min(axis=2))
    alfa = np.clip((alfa - 8) * 1.35, 0, 255)
    af = (alfa / 255.0)[..., None]
    with np.errstate(divide="ignore", invalid="ignore"):
        col = np.where(af > 0.004, (rgb - 255.0 * (1 - af)) / af, 0.0)
    col = np.clip(col, 0, 255)
    return Image.fromarray(
        np.dstack([col, alfa]).astype(np.uint8), "RGBA")


def tinta(im):
    """Logo claro sobre fondo oscuro (o blanco puro con alfa) -> versión oscura."""
    a = np.array(im).astype(np.float32)
    lum = a[..., :3].max(axis=2)
    alfa = np.clip((lum - 34) * 1.5, 0, 255)
    if a[..., 3].min() < 250:            # ya traía transparencia: respetarla
        alfa = np.minimum(alfa, a[..., 3])
    plano = np.zeros_like(a)
    plano[..., 0], plano[..., 1], plano[..., 2] = TINTA
    plano[..., 3] = alfa
    return Image.fromarray(plano.astype(np.uint8), "RGBA")


MODOS = {"directo": directo, "blanco": blanco, "tinta": tinta}

for carpeta, origen, destino, modo, ancho in TRABAJOS:
    ruta_in = os.path.join(carpeta, origen)
    if not os.path.exists(ruta_in):
        print("%-22s FALTA %s" % (destino, ruta_in))
        continue
    im = Image.open(ruta_in).convert("RGBA")
    im = recortar(MODOS[modo](recortar(im)))
    if im.width > ancho:
        im = im.resize((ancho, max(1, round(im.height * ancho / im.width))), Image.LANCZOS)
    ruta = os.path.join(OUT, destino)
    im.save(ruta, "PNG", optimize=True)
    print("%-22s %3dx%-3d %5.1f KB  (%s)" % (destino, im.width, im.height,
                                             os.path.getsize(ruta) / 1024, modo))
