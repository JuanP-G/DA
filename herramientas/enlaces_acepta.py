#!/usr/bin/env python3
"""Mantiene los enlaces a Acepta el Reto (aceptaelreto.com).

Fuente de datos: herramientas/acepta_el_reto.json
Qué actualiza (todo entre marcadores, así que se puede ejecutar las veces que haga falta):
  · README.md de cada carpeta de ejercicio: una línea «🔗 Pruébalo en Acepta el Reto».
  · README.md de la raíz: la sección «Probar sin el juez: Acepta el Reto».
La web (sitio/construir.py) lee el mismo JSON, no hace falta tocar nada más.

Uso:  python3 herramientas/enlaces_acepta.py
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "herramientas" / "acepta_el_reto.json"
URL = "https://aceptaelreto.com/problem/statement.php?id={num}"

EJ_INI, EJ_FIN = "<!-- acr:inicio -->", "<!-- acr:fin -->"
RA_INI, RA_FIN = "<!-- acr-seccion:inicio -->", "<!-- acr-seccion:fin -->"

ETIQUETA = {
    "igual": "mismo problema",
    "parecido": "casi el mismo problema",
    "relacionado": "problema relacionado",
}


def cargar():
    return json.loads(DATOS.read_text(encoding="utf-8"))["ejercicios"]


def enlace(e):
    return f"[#{e['num']} · {e['problema']}]({URL.format(num=e['num'])})"


def linea_ejercicio(e):
    if e["tipo"] == "relacionado":
        cab = "🔗 **Para practicar lo mismo en Acepta el Reto:**"
    else:
        cab = "🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura):"
    return f"{EJ_INI}\n{cab} {enlace(e)} — *{ETIQUETA[e['tipo']]}*. {e.get('nota', '')}\n{EJ_FIN}"


def poner_bloque(texto, bloque, ini, fin, despues_de=None):
    """Sustituye el bloque entre marcadores o lo inserta (tras la línea indicada o tras el título)."""
    patron = re.compile(re.escape(ini) + r".*?" + re.escape(fin), re.S)
    if patron.search(texto):
        return patron.sub(lambda _m: bloque, texto, count=1)
    lineas = texto.split("\n")
    pos = 1                                   # tras el título
    if despues_de:
        for i, l in enumerate(lineas):
            if l.startswith(despues_de):
                pos = i + 1
                break
    return "\n".join(lineas[:pos] + ["", bloque] + lineas[pos:])


def quitar_bloque(texto, ini, fin):
    return re.sub(r"\n?\n?" + re.escape(ini) + r".*?" + re.escape(fin) + r"\n?", "\n", texto, flags=re.S)


def actualizar_readmes(datos):
    tocados = 0
    for e in datos:
        carpetas = e["carpeta"] if isinstance(e["carpeta"], list) else [e["carpeta"]]
        for c in carpetas:
            p = RAIZ / c / "README.md"
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8")
            if e["tipo"] == "ninguno":
                nuevo = quitar_bloque(t, EJ_INI, EJ_FIN) if EJ_INI in t else t
            else:
                nuevo = poner_bloque(t, linea_ejercicio(e), EJ_INI, EJ_FIN, despues_de="📄")
            if nuevo != t:
                p.write_text(nuevo, encoding="utf-8")
                tocados += 1
    return tocados


def seccion_raiz(datos):
    con = [e for e in datos if e["tipo"] != "ninguno"]
    sin = [e for e in datos if e["tipo"] == "ninguno"]
    f = ["## Probar sin el juez: Acepta el Reto", ""]
    f.append("Muchos enunciados de la asignatura salen de [Acepta el Reto](https://aceptaelreto.com), "
             "que es público y no hace falta tener acceso al juez de la UCM: puedes enviar ahí tu solución y comprobar si es correcta sin mirar la mía. "
             "Cuatro cosas que conviene saber antes:")
    f.append("")
    f.append("- **Mismo problema** no siempre significa misma entrada: la versión de la asignatura puede empezar con el número de casos, "
             "mientras que en Acepta el Reto algunos terminan con una línea especial (por ejemplo `0 0 0 0`). Mira la sección *Entrada* y adapta el bucle de lectura.")
    f.append("- **Casi el mismo problema** cambia algún límite o el formato; la idea de la solución sirve igual.")
    f.append("- **Relacionado** es otro problema que practica la misma técnica.")
    f.append("- Los enlaces se han comprobado a mano comparando enunciados; si encuentras alguno mal, avisa o corrígelo en `herramientas/acepta_el_reto.json`.")
    f.append("")
    f.append("| Nº | Ejercicio | Acepta el Reto | Relación | A tener en cuenta |")
    f.append("|:--:|---|---|---|---|")
    for e in con:
        titulo = e.get("titulo_contiene")
        etq = e["problema"] if not titulo else f"{e['problema']} ({titulo})"
        f.append(f"| {e['id']} | {etq} | [#{e['num']}]({URL.format(num=e['num'])}) | {ETIQUETA[e['tipo']]} | {e.get('nota', '')} |")
    f.append("")
    f.append("**Sin equivalente que haya encontrado:** " + ", ".join(e["id"] for e in sin) +
             ". Son enunciados propios de la asignatura (o no aparecen en el buscador de Acepta el Reto).")
    f.append("")
    f.append("Para añadir o corregir un enlace: edita `herramientas/acepta_el_reto.json` y ejecuta `python3 herramientas/enlaces_acepta.py`.")
    return f"{RA_INI}\n" + "\n".join(f) + f"\n{RA_FIN}"


def actualizar_raiz(datos):
    p = RAIZ / "README.md"
    t = p.read_text(encoding="utf-8")
    bloque = seccion_raiz(datos)
    patron = re.compile(re.escape(RA_INI) + r".*?" + re.escape(RA_FIN), re.S)
    if patron.search(t):
        nuevo = patron.sub(lambda _m: bloque, t, count=1)
    else:
        marca = "## Visualizaciones interactivas"
        if marca not in t:
            sys.exit("No encuentro la sección «Visualizaciones interactivas» en el README raíz.")
        nuevo = t.replace(marca, bloque + "\n\n---\n\n" + marca, 1)
    if nuevo != t:
        p.write_text(nuevo, encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    d = cargar()
    print(f"READMEs de ejercicio actualizados: {actualizar_readmes(d)}")
    print(f"README raíz actualizado: {actualizar_raiz(d)}")
