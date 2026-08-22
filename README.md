# aimax-interactive

Landing de conversión para **AIMAX Interactive** — pantallas interactivas con IA
para aulas y salas de reuniones (Rosario, Argentina).

El tráfico de Meta Ads entra acá, mira el video y sale por WhatsApp. Una sola
página, un solo objetivo, sin menú y sin salidas laterales.

## Deploy

`index.html` es un archivo estático autónomo. No hay build step, ni framework,
ni dependencias en runtime: se sirve tal cual desde cualquier hosting estático
(Vercel, Netlify, GitHub Pages, un `public_html` común).

Las imágenes y el video **no** viven en el repo: se sirven desde Supabase
Storage, bucket público `algoritmia-img`, carpeta `aimax/`.

```
https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/algoritmia-img/aimax/
```

## Cómo se edita

No se toca `index.html` a mano. Todo sale de un solo archivo fuente:

```bash
python build_landing.py
```

`build_landing.py` tiene el CSS y el contenido en un solo lugar y genera:

| Archivo          | Para qué                                              |
|------------------|-------------------------------------------------------|
| `index.html`     | la página de producción                                |
| `Main.dc.html`   | artboard desktop del canvas de diseño (no se commitea) |
| `Mobile.dc.html` | artboard mobile del canvas de diseño (no se commitea)  |

Los otros dos scripts se corren solo cuando cambian los assets:

- `prep_logos.py` — normaliza los logos de los clientes para el carrusel.
- `subir_supabase.py` — sube imágenes y video al bucket y **verifica cada uno
  con un GET** (Supabase Storage rechaza `HEAD`). Necesita la service key en la
  variable de entorno `SUPABASE_SERVICE_KEY`; no está en el repo.

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
