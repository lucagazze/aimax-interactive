# -*- coding: utf-8 -*-
"""
Genera los assets de marca: favicons, íconos de app y la tarjeta que se ve
cuando se comparte el link (Open Graph).

El logo original de AIMAX es un JPEG de 150x150 (foto de perfil de Instagram),
demasiado chico para un ícono de 512. Así que se reconstruye vectorialmente
respetando las proporciones medidas sobre el original:

  fondo        #1e028a
  radio        22.5% del lado
  texto        "AIMAX" en blanco, ocupa el 89% del ancho
  centro       la caja del texto queda centrada verticalmente

Se renderiza con Chromium para que la tipografía sea la misma del sitio
(Schibsted Grotesk 800) y salga nítida en cada tamaño.
"""
import os
from PIL import Image
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
PUBLICO = os.path.join(os.path.dirname(AQUI), "public")
ASSETS = os.path.join(AQUI, "assets")
os.makedirs(PUBLICO, exist_ok=True)

VIOLETA = "#1e028a"
FUENTE = ("https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:"
          "wght@700;800;900&display=swap")

PLANTILLA_ICONO = """
<link rel="stylesheet" href="%(fuente)s">
<style>
  html, body { margin: 0; background: transparent; }
  .icono {
    width: %(lado)dpx; height: %(lado)dpx; border-radius: %(radio).1fpx;
    background: %(violeta)s;
    display: flex; align-items: center; justify-content: center;
    font-family: "Schibsted Grotesk", sans-serif;
    overflow: hidden;
  }
  .icono span {
    color: #fff; font-weight: 800;
    font-size: %(fs).2fpx; letter-spacing: %(ls).3fpx;
    line-height: 1; padding-right: %(ls).3fpx;
    white-space: nowrap;
  }
</style>
<div class="icono"><span>AIMAX</span></div>
"""

PLANTILLA_OG = """
<link rel="stylesheet" href="%(fuente)s">
<style>
  html, body { margin: 0; }
  .og {
    width: 1200px; height: 630px; background: %(violeta)s;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 30px;
    font-family: "Schibsted Grotesk", sans-serif;
    position: relative; overflow: hidden;
  }
  /* halo suave arriba, para que no sea un plano muerto */
  .og::before {
    content: ""; position: absolute; top: -320px; left: 50%%;
    transform: translateX(-50%%);
    width: 900px; height: 620px; border-radius: 50%%;
    background: radial-gradient(closest-side, rgba(120, 90, 255, 0.45), transparent);
  }
  .marca {
    position: relative;
    color: #fff; font-weight: 800; font-size: 168px;
    letter-spacing: -2px; line-height: 1;
  }
  .bajada {
    position: relative;
    color: rgba(255, 255, 255, 0.72); font-weight: 500; font-size: 38px;
    letter-spacing: -0.6px;
  }
  .pie {
    position: absolute; bottom: 46px; left: 0; right: 0; text-align: center;
    color: rgba(255, 255, 255, 0.5); font-weight: 600; font-size: 24px;
    letter-spacing: 3px; text-transform: uppercase;
  }
</style>
<div class="og">
  <div class="marca">AIMAX</div>
  <div class="bajada">Pantallas interactivas con IA</div>
  <div class="pie">Rosario &middot; Argentina</div>
</div>
"""


def medir_letras(pg, lado):
    """Busca el font-size y el tracking que hacen que AIMAX ocupe el 89%."""
    objetivo = lado * 0.893
    fs, ls = lado * 0.20, lado * 0.012
    for _ in range(14):
        pg.set_content(PLANTILLA_ICONO % dict(fuente=FUENTE, lado=lado,
                                              radio=lado * 0.225, violeta=VIOLETA,
                                              fs=fs, ls=ls))
        pg.wait_for_timeout(120)
        ancho = pg.evaluate("() => document.querySelector('.icono span').getBoundingClientRect().width")
        if abs(ancho - objetivo) < lado * 0.004:
            break
        fs *= objetivo / max(ancho, 1)
    return fs, ls


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=1)

    # ── Íconos. El de Apple va sin esquinas redondeadas: iOS aplica su
    #    propia máscara y si ya viene redondeado queda doble borde.
    iconos = [
        ("icon-512.png", 512, 0.225),
        ("icon-192.png", 192, 0.225),
        ("apple-touch-icon.png", 180, 0.0),
        ("favicon-32.png", 32, 0.225),
        ("favicon-16.png", 16, 0.225),
    ]
    for nombre, lado, radio in iconos:
        # se renderiza grande y se baja: los tamaños chicos salen mucho mejor
        escala = max(1, round(512 / lado))
        L = lado * escala
        fs, ls = medir_letras(pg, L)
        pg.set_content(PLANTILLA_ICONO % dict(fuente=FUENTE, lado=L,
                                              radio=L * radio, violeta=VIOLETA,
                                              fs=fs, ls=ls))
        pg.wait_for_timeout(200)
        tmp = os.path.join(PUBLICO, "_tmp.png")
        pg.query_selector(".icono").screenshot(path=tmp, omit_background=True)
        im = Image.open(tmp).convert("RGBA")
        if im.width != lado:
            im = im.resize((lado, lado), Image.LANCZOS)
        im.save(os.path.join(PUBLICO, nombre), "PNG", optimize=True)
        os.remove(tmp)
        print("%-24s %dx%d" % (nombre, lado, lado))

    # ── favicon.ico multi-resolución
    base = Image.open(os.path.join(PUBLICO, "icon-512.png")).convert("RGBA")
    ico = os.path.join(PUBLICO, "favicon.ico")
    base.save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    print("%-24s 16/32/48  %.1f KB" % ("favicon.ico", os.path.getsize(ico) / 1024))

    # ── Tarjeta de Open Graph
    pg.set_viewport_size({"width": 1200, "height": 630})
    pg.set_content(PLANTILLA_OG % dict(fuente=FUENTE, violeta=VIOLETA))
    pg.wait_for_timeout(500)
    og_png = os.path.join(PUBLICO, "_og.png")
    pg.query_selector(".og").screenshot(path=og_png)
    og = os.path.join(ASSETS, "og-image.jpg")
    Image.open(og_png).convert("RGB").save(og, "JPEG", quality=88, optimize=True)
    os.remove(og_png)
    print("%-24s 1200x630  %.1f KB" % ("og-image.jpg", os.path.getsize(og) / 1024))

    b.close()
