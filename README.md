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

La lista de instalaciones (`INSTALACIONES` en `build_landing.py`) tiene
además 5 nombres sin logo ni foto, solo texto — igual que Molino Dos
Hermanos —: Santa Fe Bio, Franco Pisso, Buena Vista Desarrollos, Deal Buró
y Proglobal, confirmados por Alejo el 2026-09-03.

## Carrusel "Así se ve en el día a día"

Sección nueva (2026-09-03), debajo de la galería de casos, antes del CTA
final. Son las 7 fotos reales que mandó Luca por WhatsApp (arquitectura con
AutoCAD, un stand de Urbania, un taller accesible para personas mayores),
en carrusel continuo (mismo mecanismo CSS que el marquee de logos: la tanda
se repite 2 veces y se anima `translateX(-50%)` infinito). Sin texto ni
nombre de cliente encima — a diferencia de la galería de arriba, acá no se
sabe ni hace falta saber de qué instalación es cada foto, son solo "gente
usándola". Alto fijo (`.uso-card`, 340px desktop / 220px mobile) y ancho
automático por imagen (`carrusel-1.webp` a `carrusel-7.webp`): cada foto
entra completa, sin recortar ni deformar, igual que el resto de las
imágenes del sitio desde el 2026-09-03.

## Galería "Tres formas de usarla todos los días" y filas de funciones

Las 3 imágenes de la galería (`caso-educacion.webp`, `caso-empresas.webp`,
`caso-arquitectura.webp`) y `fila-anotacion.webp` (fila "Anotación en
vivo") son gráficos generados con IA (nano-banana pro, con
`instalacion.webp` como referencia de producto para mantener el diseño
real del equipo), no fotos de instalaciones ni de clientes puntuales.
`fila-android-windows.webp` (fila "Antes y después") es en cambio la
imagen real que mandó Alejo ("Dos formas de hacer una reunión."), recortada
para sacarle el título que traía arriba porque duplicaba el `<h3>` de la
fila. La primera fila (`demo-escritura.jpg`) sigue siendo una captura real
del producto.

Hasta el 2026-09-03 la galería mostraba 3 fotos reales atribuidas a FAPyD,
Black Swan Inversiones y Municipalidad de Rosario — Alejo avisó que esas
fotos no correspondían a esos casos de uso, así que se sacó la atribución.
Alejo pidió después reemplazarlas por gráficos de producto con los
beneficios integrados (mandó 3 referencias) y usar el mismo estilo en la
fila de "Anotación en vivo"; para la fila "Android + Windows" mandó
directamente la imagen final, que ahora se llama "Antes y después" (tag y
texto reescritos para que hablen de la comparación de salas, no de
Android/Windows — ese copy quedó desactualizado un par de commits).

Los 7 textos de la galería (`Todo en uno`, `Interacción real`, `Colaboración
sin límites`, `Conectividad total`, `Mejora la atención`, `Ahorro de tiempo
y recursos`, `Preparada para el futuro`) son la lista de "Ventajas de una
pantalla interactiva" que mandó Alejo, repartida 3/2/2 entre las 3 imágenes.

**Trampa de CSS resuelta el 2026-09-03:** `.row-media img` tenía
`aspect-ratio: 16/9` pero el atributo HTML `height="427"` (fijo para las 3
filas) le ganaba a la aspect-ratio — el navegador usaba 427px de alto literal
en vez de calcularlo desde el ancho, así que el recorte real terminaba siendo
~1.18:1 en vez de 16:9 y se comía el 30%+ del ancho de la imagen por cada
lado. Afectaba a las 3 filas desde siempre, no solo a las nuevas — se notó
recién con los gráficos de IA porque tienen texto pegado a mitad de la
imagen. Primero se arregló agregando `height: auto;` explícito. Después,
al recortarle el título a `fila-android-windows.webp`, esa imagen quedó
mucho más ancha que 16:9 (2.1:1) — forzarla a 16:9 le recortaba los costados
a las dos cards. Se sacó `aspect-ratio`/`object-fit` de `.row-media img` del
todo: ahora cada fila entra con su proporción real (`w`/`h` por fila en
`FILAS`, ya no `width="760" height="427"` fijo para las tres).

Misma trampa, otra víctima: `.install-media img` no tenía NINGUNA regla
propia (solo el `max-width:100%` global), así que al cambiar
`instalacion.webp` por una imagen mucho más vertical (1024×1536, la
referencia "Una pantalla. Múltiples formas de trabajar." que mandó Alejo)
el `height="1536"` del atributo quedó fijo mientras el ancho se achicaba al
de la columna — la imagen se veía estirada 3 veces más alta de lo real.
Mismo arreglo: `.install-media img { width:100%; height:auto; }` explícito.
Ojo con esto en cualquier imagen nueva que se agregue con `width`/`height`
en el `<img>` y algo (aspect-ratio o no) controlando el tamaño por CSS: si
`height` no queda explícitamente en `auto`, el atributo gana.

## Pendiente

- [ ] **Logo de Molino Dos Hermanos.** No tiene dominio, ni Instagram, ni
      Facebook, ni figura en registros de empresas. Lo tiene que mandar el
      cliente. Por ahora aparece como texto abajo del carrusel.
- [ ] **VSL definitiva.** Hoy corre el video del sitio actual de AIMAX,
      comprimido de 83 MB a 5,6 MB.
- [ ] **Fotos reales de casos de uso.** La galería de "Tres formas de
      usarla" hoy es IA genérica; reemplazar por fotos reales verificadas
      cuando Alejo las confirme.
- [x] **Testimonios.** Se sacó el bloque placeholder (2026-09-03, a pedido de
      Alejo); se puede volver a agregar más adelante con texto real.

## Verificación antes de publicar

Probado en 320, 375, 390, 430, 600, 768, 834, 1024, 1280, 1440 y 1920 px:
sin scroll horizontal, sin errores de consola, sin objetivos táctiles por
debajo de 44 px y sin requests fallidos.

---

Hecho por [Algoritmia](https://algoritmiadesarrollos.com.ar) · Meta Ads y
desarrollo web.
