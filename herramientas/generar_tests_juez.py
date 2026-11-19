#!/usr/bin/env python3
"""Genera las pruebas del juez a partir de juez/ejercicios/<id>.py.

Uso:  PYTHONUTF8=1 python3 herramientas/generar_tests_juez.py [id ...]     (sin ids: todos)

Para cada ejercicio escribe en juez/tests/<id>/:
  N.in, N.out      entrada y salida esperada de la prueba N (siempre con LF)
  pruebas.json     nombre, tipo, casos, qué comprueba, qué significa fallarla y pistas de cada prueba
  config.json      solución, cabeceras, límite de tiempo y fallo de demostración (lo leen el
                   servidor del juez y sitio/construir.py)
El formato de los módulos está explicado en juez/ejercicios/_comun.py.
"""
import importlib.util, json, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EJS = RAIZ / "juez" / "ejercicios"
DEST = RAIZ / "juez" / "tests"
sys.path.insert(0, str(EJS))


def escribe(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:   # siempre LF
        f.write(texto)


def modulo(ej):
    spec = importlib.util.spec_from_file_location(f"ej_{ej.replace('-', '_')}", EJS / f"{ej}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def todos():
    return sorted(p.stem for p in EJS.glob("*.py") if not p.stem.startswith("_"))


def generar(ej, silencio=False):
    m = modulo(ej)
    carpeta = DEST / ej
    for viejo in list(carpeta.glob("*.in")) + list(carpeta.glob("*.out")) + list(carpeta.glob("*.txt")):
        viejo.unlink()
    meta, total = [], 0
    for k, p in enumerate(m.pruebas(), 1):
        p = dict(p)
        ent, sal = p.pop("entrada"), p.pop("salida")
        escribe(carpeta / f"{k}.in", ent)
        escribe(carpeta / f"{k}.out", sal)
        total += len(ent.encode()) + len(sal.encode())
        meta.append({"n": k, **p})
        if not silencio:
            print(f"{ej} {k:2} {p['tipo']:11} {len(ent.encode()):>9} B  {p['nombre']}")
    escribe(carpeta / "pruebas.json", json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    escribe(carpeta / "config.json", json.dumps(m.CONFIG, ensure_ascii=False, indent=1) + "\n")
    return m, meta, total


if __name__ == "__main__":
    for ej in sys.argv[1:] or todos():
        _, meta, total = generar(ej)
        print(f"{ej}: {len(meta)} pruebas, {total / 1e6:.2f} MB")
