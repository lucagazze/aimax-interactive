# aimax-interactive

Landing de conversión para **AIMAX Interactive** — pantallas interactivas con IA
para aulas y salas de reuniones (Rosario, Argentina).

El tráfico de Meta Ads entra acá, mira el video y sale por WhatsApp. Una sola
página, un solo objetivo, sin menú y sin salidas laterales.

## Estructura

```
public/          lo único que se publica
  index.html         la página, estática y sin dependencias en runtime
  favicon.ico        16/32/48 en un solo archivo
  favicon-16/32.png  apple-touch-icon.png  icon-192.png  icon-512.png
  site.webmanifest   robots.txt   sitemap.xml
src/             fuentes; no se despliegan (ver .vercelignore)
  build_landing.py   genera public/index.html y los artboards
  prep_logos.py      normaliza los logos de clientes
  prep_marca.py      genera favicons e imagen de Open Graph
  subir_supabase.py  sube los assets al bucket
  assets/            imágenes fuente + og-image.jpg
  canvas/            artboards del canvas de diseño (git-ignored)
vercel.json      outputDirectory: public, cleanUrls y headers
```

## SEO

Todo sale de `build_landing.py`, no hay nada escrito a mano en el `<head>`.

- `title` de 50 caracteres y `description` de 138: por debajo del corte de
  Google en ambos casos.
- `canonical`, `robots`, `og:*` completos, `twitter:card` de imagen grande,
  `robots.txt` y `sitemap.xml`.
- **Open Graph**: tarjeta de 1200×630 con el logo, servida desde Supabase con
  URL absoluta, así el preview anda aun antes de conectar el dominio.
- **JSON-LD** con `Organization`, `WebSite`, `WebPage` y `VideoObject`. Solo
  datos verificados: sin precios ni reseñas inventadas, que además Google
  penaliza.
- Imágenes con `width`/`height` y `alt`; todas diferidas menos el poster del
  video, que va con `fetchpriority="high"`.

### Cambiar el dominio

`SITIO`, arriba de `src/build_landing.py`, es la única línea a tocar: de ahí
salen el `canonical`, el `og:url` y el `sitemap.xml`. Hoy apunta al dominio por
defecto de Vercel. Si se conecta uno propio, se cambia esa línea y se corre
`python src/build_landing.py`.

### Regenerar los íconos

```bash
python src/prep_marca.py        # favicons + og-image.jpg
python src/subir_supabase.py    # sube og-image.jpg al bucket
```

El logo original de AIMAX es un JPEG de 150×150 (foto de perfil de Instagram),
muy chico para un ícono de 512. `prep_marca.py` lo reconstruye vectorialmente
respetando las proporciones medidas sobre el original: fondo `#1e028a`, radio
del 22,5 %, y el texto ocupando el 89 % del ancho.

## Deploy en Vercel

Importás el repo y listo. `vercel.json` ya declara `outputDirectory: "public"`,
así que **no hay que configurar nada en el panel**: Framework Preset en *Other*,
Build Command y Install Command vacíos.

No hay build step, ni framework, ni dependencias en runtime. `public/index.html`
se sirve tal cual, así que también anda en Netlify, GitHub Pages o un
`public_html` común copiando esa carpeta.

Las imágenes y el video **no** viven en el repo: se sirven desde Supabase
Storage, bucket público `algoritmia-img`, carpeta `aimax/`.

```
https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/algoritmia-img/aimax/
```

## Cómo se edita

No se toca `public/index.html` a mano: lo pisa el generador. Todo el contenido
y el CSS están en un solo archivo fuente.

```bash
python src/build_landing.py
```

| Salida                      | Para qué                              |
|-----------------------------|---------------------------------------|
| `public/index.html`         | la página de producción               |
| `src/canvas/Main.dc.html`   | artboard desktop del canvas de diseño |
| `src/canvas/Mobile.dc.html` | artboard mobile del canvas de diseño  |

Los otros dos scripts se corren solo cuando cambian los assets:

- `src/prep_logos.py` — normaliza los logos de los clientes para el carrusel.
- `src/subir_supabase.py` — sube imágenes y video al bucket y **verifica cada
  uno con un GET** (Supabase Storage rechaza `HEAD`). Necesita la service key en
  la variable de entorno `SUPABASE_SERVICE_KEY`; no está en el repo.

## Los logos del carrusel

Los siete salen de fuentes oficiales, ninguno recreado a mano:

| Logo                             | Origen                                        |
|----------------------------------|-----------------------------------------------|
| YPF                              | Wikimedia Commons                             |
| Terminal 6                       | `terminal6.com.ar`                            |
| ODESUR                           | `odesur.org`                                  |
| UNL — Escuela Industrial Superior| `eis.unl.edu.ar`                              |
| Tecnoteca Rosario                | Facebook oficial                              |
| CIMAES Marcelloni                | Facebook oficial                              |
| Baravalle & Granados             | wordmark de `baravalle-granados.com.ar`       |

Escuela Industrial y Baravalle solo publican su logo en blanco sobre fondo
oscuro. Sobre fondo blanco van en negro, que es la variante oscura del mismo
wordmark.

## Pendiente

- [ ] **Logo de Molino Dos Hermanos.** No tiene dominio, ni Instagram, ni
      Facebook, ni figura en registros de empresas. Lo tiene que mandar el
      cliente. Por ahora aparece como texto abajo del carrusel.
- [ ] **VSL definitiva.** Hoy corre el video del sitio actual de AIMAX,
      comprimido de 83 MB a 5,6 MB.
- [ ] **Testimonios.** El bloque está maquetado y marcado como placeholder;
      falta el texto real.

## Verificación antes de publicar

Probado en 320, 375, 390, 430, 600, 768, 834, 1024, 1280, 1440 y 1920 px:
sin scroll horizontal, sin errores de consola, sin objetivos táctiles por
debajo de 44 px y sin requests fallidos.

---

Hecho por [Algoritmia](https://algoritmiadesarrollos.com.ar) · Meta Ads y
desarrollo web.
