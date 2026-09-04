# -*- coding: utf-8 -*-
"""
Sube los assets de la landing de AIMAX al bucket público `algoritmia-img`.

Project: czocbnyoenjbpxmcqobn · carpeta destino: aimax/
La key legacy service_role sigue funcionando contra Storage REST en este
project (verificado 2026-08-22), aunque las legacy keys estén desactivadas
para el resto de la API.

Verificar SIEMPRE con GET: Supabase Storage rechaza HEAD.
"""
import os
import sys
import mimetypes
import urllib.request
import urllib.error

PROJECT = "czocbnyoenjbpxmcqobn"
BUCKET = "algoritmia-img"
CARPETA = "aimax"
BASE = "https://%s.supabase.co/storage/v1" % PROJECT
PUBLICO = "%s/object/public/%s/%s" % (BASE, BUCKET, CARPETA)

# La key NO va en el repo. Sale del entorno o del .env.local de Creattia.
def leer_key():
    k = os.environ.get("SUPABASE_SERVICE_KEY")
    if k:
        return k.strip()
    env = r"C:\Users\lucag\Desktop\CLAUDE\creattia\.env.local"
    if os.path.exists(env):
        for linea in open(env, encoding="utf-8", errors="ignore"):
            if linea.startswith("SUPABASE_SERVICE_ROLE_KEY"):
                return linea.split("=", 1)[1].strip().strip('"').strip("'")
    print("Falta la key. Exportá SUPABASE_SERVICE_KEY y volvé a correr.")
    sys.exit(1)


KEY = leer_key()

AQUI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SCRATCH = (r"C:\Users\lucag\AppData\Local\Temp\claude\c--Users-lucag--claude"
           r"\6a3b4ef6-9780-4a03-8b1c-f4fff44207c0\scratchpad")

ARCHIVOS = [
    (AQUI, "vsl-poster.jpg"),
    (AQUI, "demo-escritura.jpg"),
    (AQUI, "demo-anotacion.jpg"),
    (AQUI, "demo-ia.jpg"),
    (AQUI, "instalacion.webp"),
    (AQUI, "logo-ypf.png"),
    (AQUI, "logo-terminal6.png"),
    (AQUI, "logo-odesur.png"),
    (AQUI, "logo-eis.png"),
    (AQUI, "logo-tecnoteca.png"),
    (AQUI, "logo-cimaes.png"),
    (AQUI, "logo-baravalle.png"),
    (AQUI, "logo-dos-hermanos.png"),
    (AQUI, "caso-educacion.webp"),
    (AQUI, "caso-empresas.webp"),
    (AQUI, "caso-arquitectura.webp"),
    (AQUI, "og-image.jpg"),
    (SCRATCH, "vsl-aimax.mp4"),
]


def pedir(url, metodo="GET", datos=None, tipo=None, cabeceras=None):
    req = urllib.request.Request(url, data=datos, method=metodo)
    req.add_header("User-Agent", "curl/8.7.1")
    for k, v in (cabeceras or {}).items():
        req.add_header(k, v)
    if tipo:
        req.add_header("Content-Type", tipo)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


auth = {"Authorization": "Bearer " + KEY, "apikey": KEY}

# El bucket ya existe (lo usan otras landings de Algoritmia); igual lo chequeo.
est, cuerpo = pedir("%s/bucket/%s" % (BASE, BUCKET), cabeceras=auth)
if est != 200:                      # ojo: un bucket inexistente da 400, no 404
    print("bucket %s no accesible (%s): %s" % (BUCKET, est, cuerpo[:200]))
    sys.exit(1)
print("bucket %s ok" % BUCKET)

fallos = []
for carpeta, nombre in ARCHIVOS:
    ruta = os.path.join(carpeta, nombre)
    if not os.path.exists(ruta):
        print("%-22s FALTA en disco" % nombre)
        fallos.append(nombre)
        continue
    with open(ruta, "rb") as fh:
        datos = fh.read()
    tipo = mimetypes.guess_type(nombre)[0] or "application/octet-stream"
    destino = "%s/object/%s/%s/%s" % (BASE, BUCKET, CARPETA, nombre)
    cab = dict(auth)
    cab["x-upsert"] = "true"        # reemplaza si ya estaba
    est, cuerpo = pedir(destino, "POST", datos, tipo, cab)
    if est != 200:
        print("%-22s SUBIDA %s %s" % (nombre, est, cuerpo[:150]))
        fallos.append(nombre)
        continue

    # verificación real: GET, nunca HEAD (Storage rechaza HEAD)
    est_v, cuerpo_v = pedir("%s/%s" % (PUBLICO, nombre))
    ok = est_v == 200 and len(cuerpo_v) == len(datos)
    print("%-22s %6.1f KB  subida=%s  verificada=%s%s"
          % (nombre, len(datos) / 1024, est, est_v,
             "" if ok else "  <-- REVISAR (bajó %d bytes)" % len(cuerpo_v)))
    if not ok:
        fallos.append(nombre)

print()
print("URL base:", PUBLICO + "/")
print("FALLARON:", fallos if fallos else "ninguno")
