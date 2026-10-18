#!/usr/bin/env python3
"""Genera la versión de cada solución lista para enviar a Acepta el Reto.

Acepta el Reto solo admite UN fichero .cpp, así que `#include "Grafo.h"` (o IndexPQ.h, Digrafo.h…) no compila allí.
Este script toma la solución de la asignatura y produce, en `Acepta el Reto/`, un fichero que:
  1. lleva dentro las cabeceras propias (las copia en el sitio del #include), y
  2. cambia la lectura de la entrada y la salida al formato de Acepta el Reto cuando difiere del de la asignatura
     (por ejemplo, terminar en `0 0 0 0` en vez de empezar con el número de casos, o escribir `----` como separador).

Nunca se toca la solución original: los ficheros de `Acepta el Reto/` se regeneran, no se editan a mano.

Uso:
  python3 herramientas/para_acepta.py            genera los ficheros
  python3 herramientas/para_acepta.py --probar   además los compila y ejecuta con las pruebas de `Acepta el Reto/pruebas/`
"""
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "Acepta el Reto"
PRUEBAS = SALIDA / "pruebas"
URL = "https://aceptaelreto.com/problem/statement.php?id={num}"

# Lectura «hasta el final del fichero»: lo que usa Acepta el Reto cuando el enunciado no da número de casos ni marca de fin.
HASTA_EOF = "while (cin >> ws && cin.peek() != EOF)"

# num -> datos. `cambios` son (regex, sustitución, explicación); cada regex debe encontrarse exactamente una vez.
EJERCICIOS = {
    303: dict(id="01-1", titulo="¿Es un árbol AVL?", fuente="1-Arboles AVL/EJ_01-1/EJ 01-1.cpp", slug="es_un_arbol_AVL", cambios=[]),
    289: dict(id="02-1", titulo="Lo que cuesta sumar", fuente="2-Colas de prioridad/EJ_02-1/EJ_02-1.cpp", slug="lo_que_cuesta_sumar", cambios=[]),
    351: dict(id="02-2", titulo="Unidad Curiosa de Monitorización", fuente="2-Colas de prioridad/EJ_02-2/EJ_02-2.cpp", slug="unidad_curiosa_de_monitorizacion",
              cambios=[(r'cout << "---\\n";', r'cout << "----\\n";', "el separador de cada caso es `----` (cuatro guiones)")]),
    341: dict(id="02-3", titulo="Reina del súper", fuente="2-Colas de prioridad/EJ_02-3/EJ_02-3.cpp", slug="reina_del_super",
              cambios=[(r"cin >> cajas;", "if (!(cin >> cajas)) return false;", "la entrada termina al acabarse el fichero (no hay caso `0 0`)")]),
    311: dict(id="02-5", titulo="Ordenando a los pacientes en urgencias", fuente="2-Colas de prioridad/EJ_02-5/EJ_02-5.cpp", slug="pacientes_en_urgencias",
              cambios=[(r'cout << "---\\n";', r'cout << "----\\n";', "el separador de cada caso es `----` (cuatro guiones)")]),
    505: dict(id="03-1", titulo="Volando drones", fuente="3-Colas de prioridad variable (Heapsort)/EJ_03-1/EJ_03-1.cpp", slug="volando_drones", cambios=[]),
    649: dict(id="03-3", titulo="Multitarea", fuente="3-Colas de prioridad variable (Heapsort)/EJ_03-3/EJ_03-3.cpp", slug="multitarea",
              cambios=[
                  (r"int casos;\s*cin >> casos;\s*for \(int i = 0; i < casos; i\+\+\)\s*resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                   "no hay número de casos: se lee hasta el final del fichero"),
                  (r"IndexPQ<pair<int, int>>", "IndexPQ<pair<long long, long long>>", "los instantes llegan hasta 10^9: `long long`"),
                  (r"vector<int> periodo", "vector<long long> periodo", "los instantes llegan hasta 10^9: `long long`"),
                  (r"int ini, fin;", "long long ini, fin;", "los instantes llegan hasta 10^9: `long long`"),
                  (r"int ini, fin, p;", "long long ini, fin, p;", "los instantes llegan hasta 10^9: `long long`"),
                  (r"int tiempoActual = 0;", "long long tiempoActual = 0;", "los instantes llegan hasta 10^9: `long long`"),
                  (r"int ini = tarea\.prioridad\.first;", "long long ini = tarea.prioridad.first;", "los instantes llegan hasta 10^9: `long long`"),
                  (r"int fin = tarea\.prioridad\.second;", "long long fin = tarea.prioridad.second;", "los instantes llegan hasta 10^9: `long long`"),
              ]),
    271: dict(id="03-4", titulo="Pájaros en vuelo", fuente="3-Colas de prioridad variable (Heapsort)/EJ_03-4/EJ_03-4.cpp", slug="pajaros_en_vuelo", cambios=[]),
    307: dict(id="04-1", titulo="Árboles libres", fuente="4-Grafos no dirigidos/EJ_04-1/EJ_04-1.cpp", slug="arboles_libres",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                        "no hay número de casos: se lee hasta el final del fichero")]),
    352: dict(id="04-2", titulo="Los amigos de mis amigos son mis amigos", fuente="4-Grafos no dirigidos/EJ_04-2/EJ_04-2.cpp", slug="amigos_de_mis_amigos", cambios=[]),
    279: dict(id="04-7", titulo="Grafo bipartito", fuente="4-Grafos no dirigidos/EJ_04-7/EJ_04-7.cpp", slug="grafo_bipartito",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                        "no hay número de casos: se lee hasta el final del fichero")]),
    319: dict(id="05-1", titulo="La máquina calculadora", fuente="5-Grafos dirigidos/EJ_05-1/EJ_05-1.cpp", slug="maquina_calculadora",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(g\);", HASTA_EOF + " resuelveCaso(g);",
                        "no hay número de casos: se lee hasta el final del fichero")]),
    253: dict(id="05-5", titulo="Haciendo trampas en Serpientes y Escaleras", fuente="5-Grafos dirigidos/EJ_05-5/EJ_05-5.cpp", slug="serpientes_y_escaleras",
              cambios=[
                  (r"void resuelveCaso\(\) \{", "bool resuelveCaso() {", "la entrada termina con la línea `0 0 0 0`"),
                  (r"cin >> N >> K >> S >> E;", "if (!(cin >> N >> K >> S >> E) || N == 0) return false;", "la entrada termina con la línea `0 0 0 0`"),
                  (r"(cout << t\.distancia\(casillas - 1\) << '\\n';)", r"\1\n    return true;", "la entrada termina con la línea `0 0 0 0`"),
                  (r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", "while (resuelveCaso());", "la entrada termina con la línea `0 0 0 0`"),
              ]),
    288: dict(id="06-1", titulo="Petroleros hundidos", fuente="6-Conjuntos disjuntos y grafos valorados/EJ_06-1/EJ_06-1.cpp", slug="petroleros_hundidos",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                        "no hay número de casos: se lee hasta el final del fichero (el mar va como espacio en blanco: la solución solo mira dónde hay `#`)")]),
    646: dict(id="06-2", titulo="Camiones de reparto", fuente="6-Conjuntos disjuntos y grafos valorados/EJ_06-2/EJ_06-2.cpp", slug="camiones_de_reparto",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                        "no hay número de casos: se lee hasta el final del fichero")]),
    645: dict(id="06-3", titulo="Recorriendo el archipiélago en bicicleta", fuente="6-Conjuntos disjuntos y grafos valorados/EJ_06-3/EJ_06-3.cpp", slug="archipielago_en_bicicleta",
              cambios=[(r"int casos;\s*cin >> casos;\s*while \(casos--\) resuelveCaso\(\);", HASTA_EOF + " resuelveCaso();",
                        "no hay número de casos: se lee hasta el final del fichero")]),
}


def leer(p):
    b = Path(p).read_bytes()
    if b.startswith(b"\xef\xbb\xbf"):
        b = b[3:]
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("cp1252")
    return t.replace("\r\n", "\n").replace("\r", "\n")


def ascii_(t):
    """Sin acentos ni símbolos raros: así ningún compilador ni juez se queja de la codificación."""
    t = t.replace("→", "->").replace("≤", "<=").replace("≥", ">=").replace("≠", "!=").replace("×", "x")
    t = t.replace("–", "-").replace("—", "-").replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    t = unicodedata.normalize("NFKD", t)
    return t.encode("ascii", "ignore").decode("ascii")


def inlinear(ruta, vistos):
    """Sustituye cada `#include "x.h"` por el contenido de x.h (buscado junto al fichero o en «Estructuras de datos»)."""
    ruta = Path(ruta)
    txt = leer(ruta)

    def sustituye(m):
        nombre = m.group(1)
        for base in (ruta.parent, RAIZ / "Estructuras de datos"):
            if (base / nombre).is_file():
                p = (base / nombre).resolve()
                if p in vistos:
                    return f"// (#include \"{nombre}\" ya incluido arriba)"
                vistos.add(p)
                cuerpo = inlinear(p, vistos).replace("#pragma once", "")
                return f"// ---------- {nombre} (copiado aqui porque Acepta el Reto solo admite un fichero) ----------\n{cuerpo}\n// ---------- fin de {nombre} ----------"
        raise SystemExit(f"No encuentro la cabecera {nombre} incluida desde {ruta}")

    return re.sub(r'^[ \t]*#include\s+"([^"]+)"[^\n]*$', sustituye, txt, flags=re.M)


def generar(num, d):
    fuente = RAIZ / d["fuente"]
    if not fuente.is_file():
        raise SystemExit(f"No existe {d['fuente']}")
    codigo = inlinear(fuente, {fuente.resolve()})
    explicaciones = []
    for patron, sust, expl in d["cambios"]:
        codigo, n = re.subn(patron, sust, codigo)
        if n != 1:
            raise SystemExit(f"[{num}] el cambio {patron!r} se aplicó {n} veces (debería ser 1): ¿ha cambiado {d['fuente']}?")
        if expl and expl not in explicaciones:
            explicaciones.append(expl)
    cab = [
        "// =====================================================================",
        f"// Acepta el Reto #{num} - {d['titulo']}",
        f"// {URL.format(num=num)}",
        "//",
        "// Version lista para enviar: un solo fichero, con las cabeceras dentro.",
        f"// Generada por herramientas/para_acepta.py a partir de {d['fuente']}",
        "// (no la edites a mano: se vuelve a generar).",
    ]
    if explicaciones:
        cab.append("//")
        cab.append("// Cambios respecto a la version de la asignatura:")
        cab += [f"//  - {e}" for e in explicaciones]
    cab.append("// =====================================================================\n")
    nombre = f"ACR-{num}_{d['slug']}.cpp"
    (SALIDA / nombre).write_text(ascii_("\n".join(cab) + "\n" + codigo.strip("\n") + "\n"), encoding="utf-8", newline="\n")
    return nombre


def escribir_readme(generados):
    f = ["# Acepta el Reto: versiones listas para enviar", "",
         "Acepta el Reto ([aceptaelreto.com](https://aceptaelreto.com)) es un juez público: se registra uno y puede enviar su solución sin pasar por el de la asignatura. "
         "Solo admite **un fichero `.cpp`**, así que `#include \"Grafo.h\"` no compila allí. Los ficheros de esta carpeta son las soluciones del repo con:", "",
         "1. las cabeceras propias (`Grafo.h`, `Digrafo.h`, `IndexPQ.h`) copiadas dentro, y",
         "2. la lectura de la entrada y la salida cambiadas al formato de Acepta el Reto cuando difiere del de la asignatura.", "",
         "**Cómo usarlos:** abre el que corresponda, copia **todo** su contenido y pégalo en la página de envío del problema (lenguaje C++).", "",
         "> No los edites a mano: se regeneran con `python3 herramientas/para_acepta.py` (añade `--probar` para compilarlos y ejecutarlos con las pruebas de [`pruebas/`](pruebas)). "
         "Si cambias una solución, vuelve a ejecutar el script.", "",
         "| Ejercicio | Problema en Acepta el Reto | Fichero | Qué cambia respecto a la asignatura |", "|:--:|---|---|---|"]
    for num, d, nombre, expl in generados:
        cambios = "; ".join(expl) if expl else "solo se copian las cabeceras (el formato ya coincide)" if "#include \"" in leer(RAIZ / d["fuente"]) else "nada: el formato ya coincide"
        f.append(f"| {d['id']} | [#{num} · {d['titulo']}]({URL.format(num=num)}) | [`{nombre}`]({nombre.replace(' ', '%20')}) | {cambios} |")
    f += ["", "Las versiones de `pruebas/` son los ejemplos de los enunciados (los de Acepta el Reto y los de la asignatura, en el formato de Acepta el Reto)."]
    (SALIDA / "README.md").write_text("\n".join(f) + "\n", encoding="utf-8", newline="\n")


def probar(num, nombre):
    """Compila y ejecuta con todas las pruebas ACR-<num>*.in de pruebas/. Devuelve (ok, mensaje)."""
    ins = sorted(PRUEBAS.glob(f"{num}*.in"))
    if not ins:
        return None, "sin pruebas"
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "sol"
        c = subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-o", str(exe), str(SALIDA / nombre)], capture_output=True, text=True)
        if c.returncode:
            return False, "no compila:\n" + c.stderr[:1500]
        avisos = [l for l in c.stderr.splitlines() if "warning" in l]
        for i in ins:
            esperado = i.with_suffix(".out").read_text(encoding="utf-8")
            r = subprocess.run([str(exe)], stdin=i.open("rb"), capture_output=True, text=True, timeout=20)
            if r.stdout.split() != esperado.split():
                return False, f"{i.name}: salida distinta\n--- esperado\n{esperado}\n--- obtenido\n{r.stdout}"
        return True, f"{len(ins)} prueba(s) bien" + (f", {len(avisos)} aviso(s) del compilador" if avisos else "")


def main():
    SALIDA.mkdir(exist_ok=True)
    hacer_pruebas = "--probar" in sys.argv
    mal = 0
    generados = []
    for num, d in sorted(EJERCICIOS.items(), key=lambda x: x[1]["id"]):
        nombre = generar(num, d)
        generados.append((num, d, nombre, list(dict.fromkeys(c[2] for c in d["cambios"] if c[2]))))
        linea = f"{d['id']}  #{num}  {nombre}"
        if hacer_pruebas:
            ok, msg = probar(num, nombre)
            marca = {True: "OK ", False: "MAL", None: "-- "}[ok]
            linea = f"{marca} {linea}  {msg}"
            mal += ok is False
        print(linea)
    escribir_readme(generados)
    if hacer_pruebas and mal:
        sys.exit(f"{mal} ejercicio(s) con pruebas fallidas")


if __name__ == "__main__":
    main()
