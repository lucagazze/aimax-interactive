# -*- coding: utf-8 -*-
"""
Landing AIMAX Interactive — generador.

Una sola fuente de verdad (CSS + BODY) que emite:
  public/index.html   la página que sirve Vercel (assets desde Supabase)
  src/canvas/Main.dc.html    artboard desktop 1440 del canvas de diseño
  src/canvas/Mobile.dc.html  artboard mobile 390 del canvas de diseño
  src/canvas/canvas.json     layout del canvas

Datos: aimax.com.ar (bundle + assets reales), info.txt del cliente y
la propuesta AIMAX_Propuesta_Algoritmia_2026-08-19.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))        # src/
RAIZ = os.path.dirname(AQUI)                             # raíz del repo
ASSETS = os.path.join(AQUI, "assets")                    # imágenes fuente
PUBLICO = os.path.join(RAIZ, "public")                   # lo que sirve Vercel
CANVAS = os.path.join(AQUI, "canvas")                    # artboards del diseño

for _d in (PUBLICO, CANVAS):
    os.makedirs(_d, exist_ok=True)

# ── Datos que hay que confirmar con el cliente ──────────────────────────────
WA_NUMERO = "5493413889575"          # +54 9 3413 88-9575, confirmado por Luca 22-08-2026
WA_TEXTO = "Hola%20AIMAX%2C%20quiero%20informaci%C3%B3n%20sobre%20las%20pantallas%20interactivas"
WA_HREF = "https://wa.me/%s?text=%s" % (WA_NUMERO, WA_TEXTO)
IG = "https://www.instagram.com/aimax_interactive/"

# Assets servidos desde Supabase Storage (bucket público algoritmia-img).
# Se suben con subir_supabase.py, que verifica cada archivo con GET.
CDN = ("https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public"
       "/algoritmia-img/aimax")
VSL_MP4 = CDN + "/vsl-aimax.mp4"

# ── SEO ─────────────────────────────────────────────────────────────────────
# SITIO es el dominio final. Hoy apunta al dominio por defecto que le da
# Vercel al repo. Si se conecta un dominio propio, se cambia SOLO acá:
# de esto salen el canonical, el og:url y el sitemap.
SITIO = "https://aimax-interactive.vercel.app"

# Título hasta ~60 y descripción hasta ~155: pasado eso Google los corta.
# La palabra clave va primero y la marca al final.
TITULO = "Pantallas interactivas con IA en Argentina | AIMAX"
DESC = ("Escribís a mano y la IA lo reconoce. Android y Windows en un solo "
        "equipo. Ya instalada en YPF San Lorenzo, Terminal 6 y los Juegos "
        "Odesur.")
OG_TITULO = "AIMAX Interactive — La pantalla interactiva líder en Argentina"
OG_DESC = ("Escribís a mano y la IA lo reconoce. Ya instalada en YPF San "
           "Lorenzo, Terminal 6 y los Juegos Odesur.")
OG_IMG = CDN + "/og-image.jpg"

# El video que se sube: 58,5 s reales, medidos con ffprobe.
VSL_SEGUNDOS = 58
VSL_SUBIDO = "2026-08-22"

IMAGENES = [
    "vsl-poster.jpg",
    "demo-escritura.jpg",
    "fila-anotacion.webp",
    "fila-android-windows.webp",
    "instalacion.webp",
    "logo-ypf.png",
    "logo-terminal6.png",
    "logo-odesur.png",
    "logo-eis.png",
    "logo-tecnoteca.png",
    "logo-cimaes.png",
    "logo-baravalle.png",
    "logo-dos-hermanos.png",
    "caso-educacion.webp",
    "caso-empresas.webp",
    "caso-arquitectura.webp",
    "og-image.jpg",
]


def jsonld():
    """Datos estructurados. Solo hechos verificados: nada de precios ni
    reseñas inventadas, que además Google penaliza."""
    grafo = [
        {
            "@type": "Organization",
            "@id": SITIO + "/#organizacion",
            "name": "AIMAX Interactive",
            "alternateName": "AIMAX",
            "url": SITIO + "/",
            "logo": {
                "@type": "ImageObject",
                "url": SITIO + "/icon-512.png",
                "width": 512, "height": 512,
            },
            "image": OG_IMG,
            "description": ("Pantallas interactivas con IA para aulas, salas de "
                            "reuniones, estudios de arquitectura y organismos "
                            "públicos."),
            "telephone": "+54 9 3413 88-9575",
            "areaServed": {"@type": "Country", "name": "Argentina"},
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Rosario",
                "addressRegion": "Santa Fe",
                "addressCountry": "AR",
            },
            "sameAs": [IG, "https://aimax.com.ar"],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "sales",
                "telephone": "+54 9 3413 88-9575",
                "availableLanguage": ["Spanish"],
                "areaServed": "AR",
            },
        },
        {
            "@type": "WebSite",
            "@id": SITIO + "/#sitio",
            "url": SITIO + "/",
            "name": "AIMAX Interactive",
            "inLanguage": "es-AR",
            "publisher": {"@id": SITIO + "/#organizacion"},
        },
        {
            "@type": "WebPage",
            "@id": SITIO + "/#pagina",
            "url": SITIO + "/",
            "name": TITULO,
            "description": DESC,
            "inLanguage": "es-AR",
            "isPartOf": {"@id": SITIO + "/#sitio"},
            "about": {"@id": SITIO + "/#organizacion"},
            "primaryImageOfPage": {"@type": "ImageObject", "url": CDN + "/vsl-poster.jpg"},
        },
        {
            "@type": "VideoObject",
            "name": "La pantalla interactiva AIMAX funcionando",
            "description": ("Demostración real de la pantalla interactiva AIMAX: "
                            "escritura a mano reconocida por IA, anotación en vivo "
                            "y el módulo Windows."),
            "thumbnailUrl": [CDN + "/vsl-poster.jpg"],
            "contentUrl": VSL_MP4,
            "uploadDate": VSL_SUBIDO,
            "duration": "PT%dS" % VSL_SEGUNDOS,
            "publisher": {"@id": SITIO + "/#organizacion"},
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": grafo},
                      ensure_ascii=False, separators=(",", ":"))

FUENTE = ("https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:"
          "wght@400;500;600;700;800;900&display=swap")

# ═══════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════

CSS = """
:root {
  --ink:        #1d1d1f;
  --ink-2:      #52525b;
  --ink-3:      #86868b;
  --line:       #e8e8ed;
  --surface:    #f5f5f7;
  --violet:     #1e028a;
  --violet-2:   #3a17c4;
  --violet-ink: #2c0fb0;
  --tint:       #f4f1ff;
  --wrap:       1120px;
}

* { box-sizing: border-box; }

/* Nada puede ser más ancho que la pantalla ni generar scroll horizontal.
   `clip` y no `hidden`: hidden crea un contenedor de scroll y rompe el
   position:sticky del navbar. */
html { max-width: 100%; overflow-x: clip; }

body {
  margin: 0;
  max-width: 100%; overflow-x: clip;
  background: #ffffff;
  color: var(--ink);
  font-family: "Schibsted Grotesk", -apple-system, BlinkMacSystemFont,
               "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 17px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

a { color: var(--violet-ink); text-decoration: none; }
a:hover { color: var(--violet-2); }

img, video, svg, iframe { max-width: 100%; }
img { display: block; }

h1, h2, h3 { margin: 0; letter-spacing: -0.035em; line-height: 1.06; font-weight: 800; }
p { margin: 0; text-wrap: pretty; }

.wrap { width: 100%; max-width: var(--wrap); margin: 0 auto; padding: 0 24px; }

/* ── Navegación ─────────────────────────────────────────────────────────── */
.nav {
  position: sticky; top: 0; z-index: 50;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.nav-in {
  height: 56px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  max-width: var(--wrap); margin: 0 auto; padding: 0 24px;
}
.brand { display: flex; align-items: center; gap: 10px; }
.mark {
  width: 32px; height: 32px; border-radius: 9px;
  background: var(--violet);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 9px; font-weight: 900; letter-spacing: -0.02em;
}
.brand-name { font-size: 16px; font-weight: 700; letter-spacing: -0.02em; }

/* ── Botones ────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 9px;
  border-radius: 980px; font-weight: 600; letter-spacing: -0.01em;
  border: 1px solid transparent; cursor: pointer;
  transition: transform 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
  text-decoration: none;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary {
  background: var(--violet); color: #fff;
  padding: 17px 30px; font-size: 17px; min-height: 56px;
  box-shadow: 0 1px 2px rgba(30, 2, 138, 0.28), 0 12px 30px -12px rgba(30, 2, 138, 0.55);
}
.btn-primary:hover { background: var(--violet-2); color: #fff; }
.btn-sm { padding: 9px 18px; font-size: 14px; min-height: 44px; }
.btn-light {
  background: #fff; color: var(--violet); padding: 17px 30px;
  font-size: 17px; min-height: 56px;
}
.btn-light:hover { background: #f0ecff; color: var(--violet); }

/* ── Hero ───────────────────────────────────────────────────────────────── */
.hero { padding: 58px 0 0; text-align: center; }
h1 {
  font-size: clamp(36px, 4.4vw, 62px);
  font-weight: 800;
  max-width: 20ch; margin: 0 auto;
  letter-spacing: -0.038em; word-spacing: 0.04em;
  text-wrap: balance;
}
h1 .h1-a { display: block; }
h1 em { font-style: normal; color: var(--violet); display: block; }
.hero-cta {
  display: flex; flex-wrap: wrap; align-items: center; justify-content: center;
  gap: 12px; margin-top: 44px;
}
.hero-micro {
  margin-top: 18px; font-size: 14px; color: var(--ink-3); font-weight: 500;
}

/* ── Reproductor VSL ────────────────────────────────────────────────────── */
.vsl { margin-top: 48px; }
.player {
  position: relative; width: 100%; aspect-ratio: 16 / 9;
  border-radius: 26px; overflow: hidden; background: #0b0b0f;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05), 0 40px 80px -40px rgba(30, 2, 138, 0.45);
  cursor: pointer;
}
.player img { width: 100%; height: 100%; object-fit: cover; }
.player video { width: 100%; height: 100%; object-fit: cover; display: block; }
.player-veil {
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(11, 11, 15, 0.10) 0%,
              rgba(11, 11, 15, 0.06) 45%, rgba(11, 11, 15, 0.55) 100%);
  display: flex; align-items: center; justify-content: center;
}
.play {
  width: 84px; height: 84px; border-radius: 50%;
  background: rgba(255, 255, 255, 0.94);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
  transition: transform 0.2s ease;
}
.player:hover .play { transform: scale(1.06); }
.play-label {
  position: absolute; left: 50%; bottom: 24px; transform: translateX(-50%);
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 17px; border-radius: 980px; white-space: nowrap;
  background: rgba(11, 11, 15, 0.62);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  color: #fff; font-size: 14px; font-weight: 600; letter-spacing: -0.01em;
}
/* ── Botón flotante de WhatsApp ─────────────────────────────────────────── */
.wa-float {
  position: fixed; right: 24px; bottom: 24px; z-index: 60;
  width: 58px; height: 58px; border-radius: 50%;
  background: #25d366; color: #fff;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35), 0 16px 40px -12px rgba(7, 94, 84, 0.55);
  transition: transform 0.2s ease, background 0.2s ease;
}
.wa-float:hover { background: #1eb457; color: #fff; transform: scale(1.07); }
.wa-float svg { width: 29px; height: 29px; }

/* ── Banda de clientes ──────────────────────────────────────────────────── */
.proof { padding: 76px 0 8px; }
.proof-title {
  text-align: center; font-size: 13px; font-weight: 600;
  letter-spacing: 0.09em; text-transform: uppercase; color: var(--ink-3);
}
/* Carrusel continuo. La pista lleva la tanda de logos CUATRO veces y se
   desplaza un 50% exacto: al terminar vuelve al origen y el empalme no se
   nota. Van cuatro y no dos porque la mitad de la pista tiene que ser más
   ancha que la pantalla; con dos tandas (1330 px) se abría un hueco al
   cerrar el ciclo en monitores anchos. No se frena nunca. */
.marquee {
  overflow: hidden; margin-top: 34px;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 7%, #000 93%, transparent 100%);
          mask-image: linear-gradient(90deg, transparent 0, #000 7%, #000 93%, transparent 100%);
}
.marquee-pista {
  display: flex; width: max-content;
  animation: desfile 60s linear infinite;
  will-change: transform; pointer-events: none;
}
@keyframes desfile {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
.logo-celda {
  flex: 0 0 190px; height: 78px;
  display: flex; align-items: center; justify-content: center;
}
/* Cada logo va como background-image en su clase, no como <img>: la pista
   repite la tanda cuatro veces y así la referencia entra una sola vez. */
.logo-img {
  display: block; background-repeat: no-repeat;
  background-position: center; background-size: contain;
}
.logos-mas {
  text-align: center; margin-top: 24px;
  font-size: 14px; color: var(--ink-3); font-weight: 500;
}

/* ── Secciones ──────────────────────────────────────────────────────────── */
.section { padding: 116px 0; }
.section.tinted { background: var(--surface); }
.eyebrow {
  font-size: 13px; font-weight: 600; letter-spacing: 0.09em;
  text-transform: uppercase; color: var(--violet-ink);
}
h2 { font-size: clamp(30px, 3.6vw, 46px); margin-top: 14px; max-width: 20ch; }
h2.una-linea { max-width: none; white-space: nowrap; }
.section-lead {
  font-size: 19px; color: var(--ink-2); max-width: 62ch; margin-top: 18px; font-weight: 400;
}
.center { text-align: center; }
.center h2, .center .section-lead { margin-left: auto; margin-right: auto; }

/* ── Filas de funciones ─────────────────────────────────────────────────── */
.rows { display: flex; flex-direction: column; gap: 104px; margin-top: 76px; }
.row {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 64px; align-items: center;
}
.row.flip .row-media { order: -1; }
.row-media {
  border-radius: 22px; overflow: hidden; background: var(--surface);
  border: 1px solid var(--line);
  box-shadow: 0 30px 60px -40px rgba(0, 0, 0, 0.4);
}
/* height:auto es necesario: si no, el atributo HTML height="427" le gana
   al aspect-ratio y la imagen queda recortada mucho más angosta que 16:9. */
.row-media img { width: 100%; height: auto; aspect-ratio: 16 / 9; object-fit: cover; }
.row h3 { font-size: clamp(25px, 2.4vw, 33px); font-weight: 800; }
.row p { margin-top: 16px; font-size: 18px; color: var(--ink-2); line-height: 1.56; }
.row-tag {
  display: inline-flex; align-items: center; gap: 9px;
  font-size: 13px; font-weight: 600; color: var(--violet-ink);
  letter-spacing: 0.02em; margin-bottom: 14px;
}

/* ── Especificaciones ───────────────────────────────────────────────────── */
.specs {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px; margin-top: 58px;
}
.spec {
  background: #fff; border: 1px solid var(--line); border-radius: 20px;
  padding: 28px 24px; display: flex; flex-direction: column; gap: 10px;
}
.spec-k { font-size: 13px; font-weight: 700; letter-spacing: 0.06em;
  text-transform: uppercase; color: var(--violet-ink); }
.spec-v { font-size: 21px; font-weight: 700; letter-spacing: -0.025em; }
.spec-d { font-size: 15px; color: var(--ink-2); line-height: 1.5; }

/* ── Casos de uso ───────────────────────────────────────────────────────── */
.cases {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px; margin-top: 58px;
}
.case {
  background: var(--surface); border-radius: 22px; padding: 34px 32px;
  display: flex; flex-direction: column; gap: 12px;
  border: 1px solid transparent; transition: border-color 0.2s ease, background 0.2s ease;
}
.case:hover { background: #fff; border-color: var(--line); }
.case-ico { color: var(--violet); }
.case h3 { font-size: 22px; font-weight: 700; letter-spacing: -0.025em; }
.case p { font-size: 16px; color: var(--ink-2); line-height: 1.56; }

/* ── Instalaciones ──────────────────────────────────────────────────────── */
.install { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: start; }
.install-media {
  border-radius: 22px; overflow: hidden; border: 1px solid var(--line);
  position: sticky; top: 88px;
  box-shadow: 0 30px 60px -40px rgba(0, 0, 0, 0.4);
}
/* Sin esto, el atributo HTML height="..." queda fijo y no escala con el
   ancho (misma trampa que .row-media img). */
.install-media img { width: 100%; height: auto; }
.install-list { display: flex; flex-direction: column; gap: 2px; margin-top: 28px; }
.install-item {
  display: flex; align-items: baseline; gap: 14px;
  padding: 13px 0; border-bottom: 1px solid var(--line);
}
.install-item b { font-size: 16.5px; font-weight: 700; letter-spacing: -0.02em; }
.install-item span { font-size: 14.5px; color: var(--ink-3); margin-left: auto; }

/* ── Galería de casos reales ────────────────────────────────────────────── */
.real-cases { margin-top: 96px; }
.real-cases-head { max-width: 62ch; }
.real-cases-head h3 { font-size: clamp(22px, 2.2vw, 27px); font-weight: 800; }
.real-cases-head p { margin-top: 10px; font-size: 16.5px; color: var(--ink-2); line-height: 1.55; }
.real-grid {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: start; gap: 20px; margin-top: 34px;
}
.real-card {
  border-radius: 20px; overflow: hidden;
  box-shadow: 0 24px 50px -30px rgba(0, 0, 0, 0.45);
}
/* Sin object-fit ni aspect-ratio: la imagen entra entera, sin recortar. */
.real-card img { width: 100%; height: auto; display: block; }

/* ── CTA final ──────────────────────────────────────────────────────────── */
.cta { background: var(--violet); color: #fff; padding: 108px 0; text-align: center; }
.cta h2 { color: #fff; margin: 0 auto; max-width: 18ch; }
.cta p {
  color: rgba(255, 255, 255, 0.76); font-size: 19px;
  max-width: 46ch; margin: 20px auto 0; line-height: 1.55;
}
.cta-actions {
  display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 36px;
}
.cta small { display: block; margin-top: 20px; font-size: 14px; color: rgba(255, 255, 255, 0.6); }

/* ── Mobile ─────────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
  body { font-size: 16px; }
  .wrap, .nav-in { padding: 0 20px; }
  .brand-name { font-size: 15px; }
  .hero { padding: 48px 0 0; }
  /* En mobile el título va en DOS líneas: "La pantalla interactiva" entera
     arriba y "líder en Argentina" abajo. El tamaño se ata al ancho de pantalla
     para que la primera línea entre sin cortarse ni desbordar. */
  h1 { max-width: 100%; letter-spacing: -0.035em; font-size: min(7.6vw, 44px); }
  h2.una-linea { white-space: normal; }
  .wa-float { right: 16px; bottom: 16px; width: 54px; height: 54px; }
  .wa-float svg { width: 27px; height: 27px; }
  .hero-cta { margin-top: 32px; }
  .hero-cta .btn { width: 100%; }
  .vsl { margin-top: 34px; }
  .player { border-radius: 20px; }
  .play { width: 62px; height: 62px; }
  .play svg { width: 21px; height: 24px; }
  .play-label { bottom: 14px; font-size: 12.5px; padding: 7px 14px; }
  .section { padding: 76px 0; }
  .proof { padding: 56px 0 0; }
  .marquee { margin-top: 26px; }
  .marquee-pista { animation-duration: 42s; }
  .logo-celda { flex: 0 0 148px; height: 66px; }
  .logos-mas { margin-top: 20px; font-size: 13px; }
  .rows { gap: 64px; margin-top: 48px; }
  .row { grid-template-columns: minmax(0, 1fr); gap: 26px; }
  .row.flip .row-media { order: 0; }
  .row p { font-size: 17px; }
  .specs { grid-template-columns: minmax(0, 1fr); gap: 14px; margin-top: 38px; }
  .spec { padding: 24px 22px; }
  .cases { grid-template-columns: minmax(0, 1fr); margin-top: 38px; }
  .case { padding: 28px 24px; }
  .install { grid-template-columns: minmax(0, 1fr); gap: 34px; }
  .install-media { order: -1; position: static; }
  .real-cases { margin-top: 56px; }
  .real-grid { grid-template-columns: minmax(0, 1fr); gap: 14px; margin-top: 24px; }
  .cta { padding: 80px 0; }
  .cta-actions .btn { width: 100%; }
}

/* ── Teléfonos angostos (iPhone SE y similares) ─────────────────────────── */
@media (max-width: 400px) {
  .wrap, .nav-in { padding: 0 16px; }
  .brand { gap: 8px; }
  .brand-name { font-size: 13px; white-space: nowrap; }
  .nav .btn-sm { padding: 9px 15px; font-size: 13.5px; }
  .btn-primary, .btn-light { font-size: 16px; padding-left: 22px; padding-right: 22px; }
  .logo-celda { flex: 0 0 132px; }
  .case { padding: 24px 20px; }
  .spec { padding: 22px 20px; }
}
"""

# ═══════════════════════════════════════════════════════════════════════════
# ICONOS (SVG en línea, trazo 1.6, grilla 24)
# ═══════════════════════════════════════════════════════════════════════════

WA_ICO = (
    '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" '
    'aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 '
    '3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 '
    '9.91-9.91S17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 '
    '8.18 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 8.24 8.24c0 '
    '4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.79.97-.14.16-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.12-.15.16-.25.25-.42.08-.16.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.42h-.47c-.16 '
    '0-.43.06-.65.31-.22.25-.85.83-.85 2.03s.87 2.35.99 2.51c.12.16 1.71 2.61 4.15 '
    '3.66.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.11-.22-.17-.47-.29Z"/></svg>'
)

WA_ICO_XL = WA_ICO.replace('width="19" height="19"', 'width="29" height="29"')


def ico(paths):
    return ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % paths)

ICO_EDU = ico('<path d="M3 8.5 12 4l9 4.5-9 4.5-9-4.5Z"/><path d="M7 10.8V16c0 '
              '1.4 2.2 2.6 5 2.6s5-1.2 5-2.6v-5.2"/><path d="M21 8.5V14"/>')
ICO_EMP = ico('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 '
              '2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 12.5h18"/>')
ICO_ARQ = ico('<path d="M4 20V8.5L12 4l8 4.5V20"/><path d="M9.5 20v-5.5h5V20"/>'
              '<path d="M4 20h16"/>')
ICO_GOB = ico('<path d="M3 9.5 12 4l9 5.5"/><path d="M5 9.5V19"/><path d="M9.5 '
              '9.5V19"/><path d="M14.5 9.5V19"/><path d="M19 9.5V19"/>'
              '<path d="M3 19h18"/>')
ICO_PLAY = ('<svg width="28" height="32" viewBox="0 0 28 32" fill="#1d1d1f" '
            'aria-hidden="true"><path d="M27 14.27a2 2 0 0 1 0 3.46L3 31.6A2 2 0 0 '
            '1 0 29.87V2.13A2 2 0 0 1 3 .4l24 13.87Z"/></svg>')

def tagico(paths):
    return ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % paths)

# ═══════════════════════════════════════════════════════════════════════════
# CONTENIDO
# ═══════════════════════════════════════════════════════════════════════════

# Logos descargados de fuentes oficiales y normalizados a gris con prep_logos.py.
# Falta solo Molino Dos Hermanos: no tiene web ni redes indexadas.
# El alto es óptico, elegido a ojo para que todos pesen parecido en la fila.
LOGOS = [
    ("logo-ypf.png",          "lg-ypf",          "YPF",                               30),
    ("logo-terminal6.png",    "lg-t6",           "Terminal 6",                        44),
    ("logo-odesur.png",       "lg-odesur",       "ODESUR",                            52),
    ("logo-dos-hermanos.png", "lg-dos-hermanos", "Molino Dos Hermanos",               44),
    ("logo-eis.png",          "lg-eis",          "UNL — Escuela Industrial Superior", 44),
    ("logo-tecnoteca.png",    "lg-tecnoteca",    "Tecnoteca Rosario",                 48),
    ("logo-cimaes.png",       "lg-cimaes",       "CIMAES Marcelloni",                 60),
    ("logo-baravalle.png",    "lg-baravalle",    "Baravalle &amp; Granados",          32),
]

# Ancho de celda por breakpoint; el logo nunca puede pasar de celda - 16 px.
CELDA = {"desktop": 190, "mobile": 148, "angosto": 132}


def css_logos():
    """Una regla por logo, con el tamaño calculado desde el PNG real."""
    from PIL import Image

    def bloque(escala, celda, sangria=""):
        filas = []
        for archivo, clase, _alt, alto in LOGOS:
            with Image.open(os.path.join(ASSETS, archivo)) as im:
                razon = im.width / im.height
            h = round(alto * escala)
            w = round(h * razon)
            tope = celda - 16
            if w > tope:                      # no puede desbordar la celda
                w, h = tope, round(tope / razon)
            filas.append("%s.%-13s { width: %3dpx; height: %2dpx; }"
                         % (sangria, clase, w, h))
        return "\n".join(filas)

    imagenes = "\n".join(
        '.%-13s { background-image: url("@@CSSIMG:%s@@"); }' % (clase, archivo)
        for archivo, clase, _alt, _alto in LOGOS)

    return "\n".join([
        "\n/* ── Tamaños de los logos del carrusel ─────────────────────────────── */",
        imagenes,
        bloque(1.0, CELDA["desktop"]),
        "@media (max-width: 900px) {",
        bloque(0.82, CELDA["mobile"], "  "),
        "}",
        "@media (max-width: 400px) {",
        bloque(0.74, CELDA["angosto"], "  "),
        "}",
    ])

INSTALACIONES = [
    ("Refinería YPF San Lorenzo", "Industria"),
    ("Terminal6", "Industria"),
    ("Juegos Odesur", "Evento internacional"),
    ("Molino Dos Hermanos", "Industria"),
    ("Escuela Industrial de Santa Fe", "Educación"),
    ("Tecnoteca Rosario", "Educación"),
    ("CIMAES", "Salud"),
    ("Baravalle &amp; Granados", "Estudio jurídico"),
    ("Santa Fe Bio", "Industria"),
    ("Franco Pisso", "Capacitación"),
    ("Buena Vista Desarrollos", "Desarrollo inmobiliario"),
    ("Deal Buró", "Servicios"),
    ("Proglobal", "Industria"),
]

CASOS_REALES = [
    ("caso-educacion.webp", 1856, 2304),
    ("caso-empresas.webp", 1856, 2304),
    ("caso-arquitectura.webp", 1856, 2304),
]

FILAS = [
    dict(
        tag="Reconocimiento de escritura",
        titulo="Escribí a mano.<br>La pantalla lo entiende.",
        texto="Resolvés una fórmula con el marcador y la pantalla la reconoce, la "
              "digitaliza y la deja lista para compartir. Sin escanear, sin pasarla "
              "en limpio después, sin que se pierda al borrar.",
        img="demo-escritura.jpg",
        alt="Docente resolviendo una derivada a mano sobre una pantalla AIMAX",
        flip=False,
    ),
    dict(
        tag="Anotación en vivo",
        titulo="Anotá encima<br>de lo que estés mostrando.",
        texto="Un gráfico, una planilla, cualquier cosa que tengas abierta. Escribís "
              "arriba sin salir de la aplicación y todo queda guardado en el mismo "
              "archivo. La reunión termina y el material ya está listo para enviar.",
        img="fila-anotacion.webp",
        alt="Pantalla AIMAX con una anotación a mano sobre un gráfico de barras",
        flip=True,
    ),
    dict(
        tag="Antes y después",
        titulo="Dos formas de<br>hacer una reunión.",
        texto="Cables enredados, un proyector que tarda en prender y todos mirando una "
              "pantalla chica. Con AIMAX es una sola pantalla lista para la videollamada, "
              "la presentación y el gráfico al mismo tiempo. Reuniones que arrancan y "
              "terminan más rápido.",
        img="fila-android-windows.webp",
        alt="Comparación entre una sala tradicional, con proyector y cables, y una sala con AIMAX",
        flip=False,
    ),
]

SPECS = [
    ("Android", "Versión 14", "4 GB de RAM, 32 GB de almacenamiento, CPU de 8 núcleos y GPU de 4 núcleos."),
    ("Windows", "Core i7", "Módulo Windows 10 con 8 GB de RAM y 1 TB de disco."),
    ("Conectividad", "Anda sin internet", "Las funciones básicas siguen funcionando aunque se caiga la red."),
    ("Origen", "Marca argentina", "Empresa con base en Rosario, Santa Fe."),
]

CASOS = [
    (ICO_EDU, "Educación",
     "Generá preguntas automáticas según el nivel del curso, integrá modelos 3D y "
     "traducí en tiempo real. Las clases se vuelven participativas sin que el docente "
     "pelee con la tecnología."),
    (ICO_EMP, "Empresas y reuniones",
     "Presentaciones automáticas, diagramas inteligentes y colaboración en vivo. "
     "Equipos alineados, decisiones más rápidas y menos tiempo perdido en lo técnico."),
    (ICO_ARQ, "Arquitectura y diseño",
     "Convertí una imagen en un modelo 3D o en video y presentá el proyecto con impacto. "
     "Corregís sobre la misma pantalla, con el cliente adelante, y no quedan malentendidos."),
    (ICO_GOB, "Gobierno y organismos públicos",
     "Digitalizá audiencias, capacitaciones y procesos administrativos con reconocimiento "
     "de voz y de escritura. Más eficiencia y trazabilidad en cada paso."),
]


def build_body():
    b = []
    a = b.append

    # ── NAV
    a('<header class="nav"><div class="nav-in">')
    a('<div class="brand"><div class="mark">AIMAX</div>')
    a('<div class="brand-name">Pantallas interactivas</div></div>')
    a('<a class="btn btn-primary btn-sm" href="%s" target="_blank" rel="noopener">'
      'Contactar</a>' % WA_HREF)
    a('</div></header>')

    a('<main>')

    # ── HERO
    a('<section class="hero"><div class="wrap">')
    a('<h1><span class="h1-a">La pantalla interactiva</span>'
      '<em>líder en Argentina</em></h1>')

    # ── VSL — va inmediatamente debajo del H1
    a('<div class="vsl"><div class="player" id="vsl" role="button" tabindex="0" '
      'aria-label="Reproducir el video de la pantalla AIMAX funcionando">')
    a('<img src="@@IMG:vsl-poster.jpg@@" width="1180" height="663" fetchpriority="high" decoding="async" alt="Pantalla interactiva AIMAX instalada, con una fórmula escrita a mano">')
    a('<div class="player-veil"><div class="play">%s</div>' % ICO_PLAY)
    a('<div class="play-label">Mirá la pantalla funcionando &middot; 1 min</div></div>')
    a('</div></div>')

    # ── Botones, debajo del video
    a('<div class="hero-cta">')
    a('<a class="btn btn-primary" href="%s" target="_blank" rel="noopener">%s Escribinos por WhatsApp</a>'
      % (WA_HREF, WA_ICO))
    a('</div>')
    a('<p class="hero-micro">Te responde Alejo, directo. Sin formularios ni call center.</p>')
    a('</div></section>')

    # ── CLIENTES
    a('<section class="proof">')
    a('<div class="wrap"><p class="proof-title">Ya está instalada en</p></div>')
    # La pista lleva la tanda cuatro veces; las tres copias son decorativas
    # y van ocultas a los lectores de pantalla.
    tanda = ''.join(
        '<div class="logo-celda"><span class="logo-img %s" role="img" '
        'aria-label="%s"></span></div>' % (c, alt)
        for _f, c, alt, _h in LOGOS)
    copia = tanda.replace('role="img"', 'role="presentation"')
    copia = copia.replace('<div class="logo-celda">',
                          '<div class="logo-celda" aria-hidden="true">')
    a('<div class="marquee"><div class="marquee-pista">%s%s</div></div>'
      % (tanda, copia * 3))
    a('</section>')

    # ── FILAS DE FUNCIONES
    a('<section class="section" id="funciones"><div class="wrap">')
    a('<div class="center"><p class="eyebrow">Funciones</p>')
    a('<h2 class="una-linea">Qué hace la pantalla</h2>')
    a('<p class="section-lead">Es una computadora táctil de 4K con IA adentro, no un '
      'televisor grande con un lápiz. Estas son las tres cosas que cambian el primer '
      'día que la enchufás.</p></div>')
    a('<div class="rows">')
    for f in FILAS:
        a('<div class="row%s">' % (' flip' if f['flip'] else ''))
        a('<div class="row-copy">')
        a('<div class="row-tag">%s%s</div>'
          % (tagico('<path d="M20 6 9 17l-5-5"/>'), f['tag']))
        a('<h3>%s</h3><p>%s</p>' % (f['titulo'], f['texto']))
        a('</div>')
        a('<div class="row-media"><img src="@@IMG:%s@@" width="760" height="427" loading="lazy" decoding="async" alt="%s"></div>' % (f['img'], f['alt']))
        a('</div>')
    a('</div></div></section>')

    # ── SPECS
    a('<section class="section tinted"><div class="wrap">')
    a('<div class="center"><p class="eyebrow">Ficha técnica</p>')
    a('<h2>Lo que hay adentro.</h2></div>')
    a('<div class="specs">')
    for k, v, d in SPECS:
        a('<div class="spec"><div class="spec-k">%s</div><div class="spec-v">%s</div>'
          '<div class="spec-d">%s</div></div>' % (k, v, d))
    a('</div></div></section>')

    # ── CASOS DE USO
    a('<section class="section" id="casos"><div class="wrap">')
    a('<div class="center"><p class="eyebrow">Para quién es</p>')
    a('<h2>Cuatro espacios, cuatro formas de usarla.</h2></div>')
    a('<div class="cases">')
    for icono, titulo, texto in CASOS:
        a('<div class="case"><div class="case-ico">%s</div><h3>%s</h3><p>%s</p></div>'
          % (icono, titulo, texto))
    a('</div></div></section>')

    # ── INSTALACIONES
    a('<section class="section tinted"><div class="wrap"><div class="install">')
    a('<div><p class="eyebrow">Prueba social</p>')
    a('<h2>La misma pantalla que está en una refinería de YPF.</h2>')
    a('<p class="section-lead">No es un producto nuevo buscando su primer cliente. '
      'Estas son instalaciones hechas, funcionando todos los días.</p>')
    a('<div class="install-list">')
    for nombre, rubro in INSTALACIONES:
        a('<div class="install-item"><b>%s</b><span>%s</span></div>' % (nombre, rubro))
    a('</div>')
    a('</div>')
    a('<div class="install-media"><img src="@@IMG:instalacion.webp@@" '
      'width="1024" height="1536" loading="lazy" decoding="async" '
      'alt="Pantalla interactiva AIMAX: Android 14 + Windows 11, 4K UHD, '
      'videoconferencia integrada, duplicación inalámbrica e interacción multitáctil"></div>')
    a('</div>')
    a('<div class="real-cases"><div class="real-cases-head">')
    a('<h3>Tres formas de usarla todos los días</h3>')
    a('<p>Educación, reuniones de trabajo y arquitectura: así se ve la pantalla '
      'funcionando en cada escenario.</p>')
    a('</div>')
    a('<div class="real-grid">')
    for img, w, h in CASOS_REALES:
        a('<div class="real-card"><img src="@@IMG:%s@@" width="%d" height="%d" '
          'loading="lazy" decoding="async" alt="Pantalla interactiva AIMAX en uso"></div>'
          % (img, w, h))
    a('</div></div>')
    a('</div></section>')

    # ── CTA FINAL
    a('<section class="cta"><div class="wrap">')
    a('<h2>¿Sirve para tu aula o tu sala de reuniones?</h2>')
    a('<p>Contanos qué espacio querés equipar y cuántas pantallas necesitás. '
      'Te decimos qué configuración te corresponde y cuánto sale. Sin vueltas.</p>')
    a('<div class="cta-actions">')
    a('<a class="btn btn-light" href="%s" target="_blank" rel="noopener">%s Escribinos por WhatsApp</a>'
      % (WA_HREF, WA_ICO))
    a('</div>')
    a('<small>Rosario, Santa Fe &middot; Te responde Alejo personalmente</small>')
    a('</div></section>')

    a('</main>')

    # ── Botón flotante de WhatsApp
    a('<a class="wa-float" href="%s" target="_blank" rel="noopener" '
      'aria-label="Escribinos por WhatsApp">%s</a>' % (WA_HREF, WA_ICO_XL))

    return '\n'.join(b)


BODY = build_body()
HOJA = CSS + css_logos()

# ═══════════════════════════════════════════════════════════════════════════
# SALIDAS
# ═══════════════════════════════════════════════════════════════════════════

def con_nombres(html):
    """Referencias por nombre de archivo — para los artboards del canvas."""
    for n in IMAGENES:
        html = html.replace('@@IMG:%s@@' % n, n)
        html = html.replace('@@CSSIMG:%s@@' % n, './' + n)
    return html


def con_cdn(html):
    """Referencias a Supabase Storage — para el archivo de producción."""
    for n in IMAGENES:
        url = '%s/%s' % (CDN, n)
        html = html.replace('@@IMG:%s@@' % n, url)
        html = html.replace('@@CSSIMG:%s@@' % n, url)
    return html


DC = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="%s">
  <style>%s</style>
</helmet>
<div class="page">
%s
</div>
</x-dc>
</body>
</html>
"""

for archivo in ("Main.dc.html", "Mobile.dc.html"):
    with open(os.path.join(CANVAS, archivo), 'w', encoding='utf-8') as fh:
        fh.write(DC % (FUENTE, con_nombres(HOJA), con_nombres(BODY)))

# ── canvas.json
canvas = {
    "artboards": [
        {"file": "Main.dc.html", "x": 0, "y": 0, "w": 1440, "h": 6700,
         "title": "Landing AIMAX — Desktop", "expand": "fill", "print": "flow"},
        {"file": "Mobile.dc.html", "x": 1560, "y": 0, "w": 390, "h": 7600,
         "title": "Landing AIMAX — Mobile", "print": "flow"},
    ],
    "annotations": [
        {"id": "pendientes", "x": 0, "y": -190, "w": 620,
         "text": "PENDIENTE ANTES DE PUBLICAR\n"
                 "1. El video de la VSL (hoy se ve el poster: frame real del producto).\n"
                 "2. Confirmar que envían e instalan a todo el país.\n"
                 "\n"
                 "Resuelto 2026-09-03: se sacó el testimonio placeholder (Alejo dijo "
                 "que se puede eliminar por ahora) y se sumaron FAPyD, Black Swan "
                 "Inversiones y Municipalidad de Rosario, con logo y foto real cada uno."},
        {"id": "h1-claim", "x": 660, "y": -190, "w": 460,
         "text": "El H1 dice \"N.º 1 del mercado\". Es un superlativo sin fuente "
                 "verificable: Meta lo puede observar y un comprador B2B lo puede "
                 "cuestionar. La prueba fuerte y verificable es YPF / Terminal6 / Odesur."},
    ],
    "launch": {"view": "focused", "file": "Main.dc.html"},
}
with open(os.path.join(CANVAS, "canvas.json"), 'w', encoding='utf-8') as fh:
    json.dump(canvas, fh, ensure_ascii=False, indent=2)

# ── Archivo de producción
PROD = """<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(sitio)s/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="AIMAX Interactive">
<meta name="geo.region" content="AR-S">
<meta name="geo.placename" content="Rosario, Santa Fe">

<meta property="og:type" content="website">
<meta property="og:site_name" content="AIMAX Interactive">
<meta property="og:locale" content="es_AR">
<meta property="og:url" content="%(sitio)s/">
<meta property="og:title" content="%(og_titulo)s">
<meta property="og:description" content="%(og_desc)s">
<meta property="og:image" content="%(og_img)s">
<meta property="og:image:secure_url" content="%(og_img)s">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="AIMAX Interactive — pantallas interactivas con IA">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(og_titulo)s">
<meta name="twitter:description" content="%(og_desc)s">
<meta name="twitter:image" content="%(og_img)s">
<meta name="twitter:image:alt" content="AIMAX Interactive — pantallas interactivas con IA">

<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1e028a">
<meta name="apple-mobile-web-app-title" content="AIMAX">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://czocbnyoenjbpxmcqobn.supabase.co">
<link rel="stylesheet" href="%(fuente)s">
<style>%(css)s</style>
<script type="application/ld+json">%(jsonld)s</script>
</head>
<body>
%(body)s
<script>
(function () {
  var caja = document.getElementById('vsl');
  if (!caja) return;
  function reproducir() {
    var v = document.createElement('video');
    v.src = '%(video)s';
    v.controls = true;
    v.autoplay = true;
    v.playsInline = true;
    v.setAttribute('playsinline', '');
    caja.innerHTML = '';
    caja.style.cursor = 'default';
    caja.appendChild(v);
  }
  caja.addEventListener('click', reproducir);
  caja.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); reproducir(); }
  });
})();
</script>
</body>
</html>
"""

with open(os.path.join(PUBLICO, "index.html"), 'w', encoding='utf-8') as fh:
    fh.write(PROD % dict(fuente=FUENTE, css=con_cdn(HOJA),
                         body=con_cdn(BODY), video=VSL_MP4,
                         titulo=TITULO, desc=DESC, sitio=SITIO,
                         og_titulo=OG_TITULO, og_desc=OG_DESC, og_img=OG_IMG,
                         jsonld=jsonld()))

# ── Archivos de raíz del sitio ──────────────────────────────────────────────
with open(os.path.join(PUBLICO, "robots.txt"), 'w', encoding='utf-8') as fh:
    fh.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITIO)

with open(os.path.join(PUBLICO, "sitemap.xml"), 'w', encoding='utf-8') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             '  <url>\n'
             '    <loc>%s/</loc>\n'
             '    <changefreq>monthly</changefreq>\n'
             '    <priority>1.0</priority>\n'
             '  </url>\n'
             '</urlset>\n' % SITIO)

with open(os.path.join(PUBLICO, "site.webmanifest"), 'w', encoding='utf-8') as fh:
    json.dump({
        "name": "AIMAX Interactive",
        "short_name": "AIMAX",
        "description": OG_DESC,
        "lang": "es-AR",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#1e028a",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "maskable"},
        ],
    }, fh, ensure_ascii=False, indent=2)

for carpeta, f in ((CANVAS, "Main.dc.html"), (CANVAS, "Mobile.dc.html"),
                   (CANVAS, "canvas.json"), (PUBLICO, "index.html")):
    ruta = os.path.join(carpeta, f)
    print("%-24s %8.1f KB" % (os.path.relpath(ruta, RAIZ), os.path.getsize(ruta) / 1024))
