#!/usr/bin/env python3
"""Genera los casos de prueba del juez de la web (juez/tests/<ejercicio>/N.in y N.out).

Uso:  PYTHONUTF8=1 python3 herramientas/generar_tests_juez.py [ejercicio ...]

Cada ejercicio tiene:
  · ejemplos del enunciado (escritos a mano, ver EJEMPLOS),
  · casos propios (bordes y aleatorios con semilla fija),
y la salida esperada la calcula un solucionador INDEPENDIENTE escrito aquí en Python
(no la solución del repo), de modo que sirve también para comprobar esa solución.
"""
import pathlib, random, sys
from collections import deque

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DEST = RAIZ / "juez" / "tests"


def escribe(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:   # siempre LF
        f.write(texto)


# ---------- 04-3 · Detección de manchas negras ----------
def manchas(F, C, filas):
    visto = [[False] * C for _ in range(F)]
    n = mayor = 0
    for i in range(F):
        for j in range(C):
            if filas[i][j] == "#" and not visto[i][j]:
                n += 1
                tam = 0
                cola = deque([(i, j)])
                visto[i][j] = True
                while cola:
                    a, b = cola.popleft()
                    tam += 1
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        x, y = a + da, b + db
                        if 0 <= x < F and 0 <= y < C and filas[x][y] == "#" and not visto[x][y]:
                            visto[x][y] = True
                            cola.append((x, y))
                mayor = max(mayor, tam)
    return n, mayor


def aleatorio(rng, F, C, p):
    return ["".join("#" if rng.random() < p else "-" for _ in range(C)) for _ in range(F)]


def caso_a_texto(filas):
    return f"{len(filas)} {len(filas[0])}\n" + "\n".join(filas) + "\n"


def tests_04_3():
    rng = random.Random(43)
    ejemplo1 = ["-#-#---#", "-###---#", "----####", "-#------", "-#-#----", "-###-##-", "###--##-", "--#-----"]
    ejemplo2 = ["#-#-#-###-", "#-#-#-#-#-", "#-#-#-#-#-", "#-#-#-#-#-"]
    grupos = [
        ("enunciado", [ejemplo1, ejemplo2]),
        ("bordes", [["#"], ["-"], ["#" * 7], ["#-", "-#"], ["--", "--"]]),                 # diagonales no cuentan
        ("aleatorios pequeños", [aleatorio(rng, rng.randint(1, 9), rng.randint(1, 9), rng.choice([.3, .5, .7])) for _ in range(30)]),
        ("tablero y rayas", [["#-" * 20 if i % 2 == 0 else "-#" * 20 for i in range(20)], ["#" * 30 if i % 2 == 0 else "-" * 30 for i in range(15)]]),
        ("grande", [aleatorio(rng, 400, 400, .35)]),
    ]
    res = []
    for nombre, casos in grupos:
        ent = f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos)
        sal = "".join("%d %d\n" % manchas(len(c), len(c[0]), c) for c in casos)
        res.append((nombre, ent, sal))
    return res


GENERADORES = {"04-3": tests_04_3}

if __name__ == "__main__":
    for ej in sys.argv[1:] or GENERADORES:
        for k, (nombre, ent, sal) in enumerate(GENERADORES[ej](), 1):
            escribe(DEST / ej / f"{k}.in", ent)
            escribe(DEST / ej / f"{k}.out", sal)
            escribe(DEST / ej / f"{k}.txt", nombre + "\n")
            print(ej, k, nombre, len(ent), "bytes")
