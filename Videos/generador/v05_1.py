"""Vídeo EJ 05-1 · Juego de Transformación Modular"""
import math
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../EJ_05-1/EJ_05-1.cpp"
NOMBRE = "Juego de Transformación Modular"
TEMA = "Tema 5 · Grafos dirigidos"

# ejemplo 2 del enunciado: M=5, S=1, T=0, operaciones (2,1) y (3,1)
M, S, T = 5, 1, 0
OPS = [(2, 1), (3, 1)]
OPCOL = ["blue", "gold"]
PENT = {v: (970 + 105 * math.sin(2 * math.pi * v / 5), 262 - 100 * math.cos(2 * math.pi * v / 5)) for v in range(5)}


def vecinos(x):
    return [(op[0] * x + op[1]) % M for op in OPS]


ARISTAS = []
for x in range(M):
    for y in vecinos(x):
        if (x, y) not in ARISTAS:
            ARISTAS.append((x, y))

L_BFS = find_line(CPP, "void bfs(")
L_INI = [find_line(CPP, "dist[s] = 0;"), find_line(CPP, "q.push(s);")]
L_POP = find_line(CPP, "int x = q.front(); q.pop();")
L_T = find_line(CPP, "if (x == t) return;")
L_FOR = find_line(CPP, "for (int y : g.ady(x))")
L_CONS = find_line(CPP, "g.ponArista(x, (op.first")
L_NEW = find_line(CPP, "if (dist[y] == -1)")
L_SET = [find_line(CPP, "dist[y] = dist[x] + 1;"), find_line(CPP, "q.push(y);")]
CODE = code_lines(CPP, find_line(CPP, "class TransformacionModular"), find_line(CPP, "};", L_BFS), maxc=74,
                  skip=[(find_line(CPP, "TransformacionModular(Digrafo"), find_line(CPP, "TransformacionModular(Digrafo") + 4),
                        (find_line(CPP, "// minimo de jugadas") - 1, find_line(CPP, "vector<int> dist;") + 1)])
CODE_MAIN = code_lines(CPP, find_line(CPP, "void resuelveCaso"), find_line(CPP, "}", find_line(CPP, "cout << tm.jugadas")), maxc=74)
L_DEDUP = find_line(CPP, "ops.erase(unique")
L_TM = find_line(CPP, "TransformacionModular tm(")


def traza():
    dist = [-1] * M
    q = deque([S])
    dist[S] = 0
    pasos = [("ini", S, None, None, dist[:], list(q))]
    while q:
        x = q.popleft()
        if x == T:
            pasos.append(("fin", x, None, None, dist[:], list(q)))
            break
        pasos.append(("saca", x, None, None, dist[:], list(q)))
        for i, y in enumerate(vecinos(x)):
            if dist[y] == -1:
                dist[y] = dist[x] + 1
                q.append(y)
                pasos.append(("nuevo", x, y, i, dist[:], list(q)))
            else:
                pasos.append(("visto", x, y, i, dist[:], list(q)))
    return pasos


def estilo(dist, actual):
    ns = {}
    for u, d in enumerate(dist):
        if d >= 0:
            ns[u] = (["gold", "blue", "purple", "green"][min(d, 3)], "node_t", None)
    ns[actual] = (ns.get(actual, ("node",))[0], "node_t", "text")
    return ns


def slide_paso(k, n, tipo, x, y, i, dist, q, hl, cap):
    s = Slide("Ejecución · M = 5, inicio 1, objetivo 0", f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="class TransformacionModular")
    s.box(684, 84, 572, 310, "el Digrafo construido (M = 5)")
    es = {a: ("dim", 3) for a in ARISTAS}
    if y is not None:
        es[(x, y)] = ("gold", 6)
    s.dgraph(PENT, ARISTAS, ns=estilo(dist, x), es=es, r=22, under={u: f"d={d}" for u, d in enumerate(dist) if d >= 0})
    s.box(684, 410, 572, 194, "estado")
    s.cells(704, 436, "dist", [d if d >= 0 else "·" for d in dist], first=0,
            colors={u: "blue_d" for u, d in enumerate(dist) if d >= 0}, hl={y} if y is not None else None)
    s.queue_row(704, 506, "cola", q)
    s.text((704, 560), "operaciones:", size=16, color="muted", bold=True)
    s.pill(840, 553, "1:  2x + 1", fill="blue" if i == 0 else "blue_d", color="node_t" if i == 0 else "text", size=16)
    s.pill(980, 553, "2:  3x + 1", fill="gold" if i == 1 else "gold_d", color="node_t" if i == 1 else "text", size=16)
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-1", TEMA),
             "Juego de transformación modular. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    segs.append((ideas("El problema", [
        "Hay un módulo M y N operaciones: x  →  (a·x + b) mod M.",
        "Partimos de un número S y queremos llegar a un número T.",
        "Cada jugada aplica UNA de las operaciones al número actual.",
        "Piden el MÍNIMO de jugadas, o -1 si es imposible.",
    ]), "Tenemos un módulo y varias operaciones. Cada operación toma el número actual, lo multiplica por un factor, le suma un sumando, "
        "y se queda con el resto de dividir entre el módulo. Partimos de un número y queremos llegar a otro, con el menor número de jugadas. "
        "Si no hay manera, la respuesta es menos uno.", 0))

    # modelo
    s = Slide("La clave: los números son vértices")
    s.box(40, 90, 620, 440, "ejemplo: M = 5, operaciones 2x+1 y 3x+1")
    el = {}
    for x in range(M):
        for i, y in enumerate(vecinos(x)):
            t, c = el.get((x, y), ("", None))
            el[(x, y)] = (t + ("," if t else "") + str(i + 1), "text")
    PL = {v: (350 + 140 * math.sin(2 * math.pi * v / 5), 300 - 140 * math.cos(2 * math.pi * v / 5)) for v in range(5)}
    s.dgraph(PL, ARISTAS, r=26, elabels=el, es={a: ("muted", 3) for a in ARISTAS})
    s.bullets(690, 120, 540, [
        "Vértices: los números 0 … M−1.",
        ("Arista  x → (a·x + b) mod M  por cada operación.", "gold"),
        "Jugadas mínimas = camino más corto de S a T.",
        "Sin pesos  ⇒  BFS desde S.",
        "Es DIRIGIDO: de x se llega a y, pero no hace falta que se pueda volver.",
    ], size=21, gap=14)
    segs.append((s, "La clave es ver los números como vértices de un grafo. Cada operación es una arista que sale de x y llega a a por x más b, módulo M. "
                    "Las etiquetas de las flechas dicen qué operación la produce.", 0))
    segs.append((s, "Entonces, el mínimo de jugadas es el camino más corto del número de partida al objetivo, y como las aristas no tienen pesos, "
                    "usamos un B F S. Ojo: el grafo es dirigido. De x se llega a y, pero no hay por qué poder volver.", 0))

    # construcción
    s = Slide("Construimos el Digrafo con ponArista")
    s.box(60, 100, 1160, 270, "con M = 10.000 y N = 100: hasta un millón de aristas por caso (unos 4 MB)")
    s.text((100, 160), "Digrafo g(m);", size=26, mono=True)
    s.text((100, 215), "for (int x = 0; x < m; ++x)", size=26, mono=True)
    s.text((100, 265), "    for (auto const& op : ops)", size=26, mono=True)
    s.text((100, 315), "        g.ponArista(x, (op.first * x + op.second) % m);", size=26, mono=True, color="gold")
    s.wrap(60, 400, 1160, "a·x + b ≤ 9.999 · 9.999 + 9.999 < 10⁸: cabe en un int.   Si S = T, la respuesta es 0.", size=22, color="text", center=True)
    s.wrap(60, 450, 1160, "Operaciones repetidas (mismos a y b módulo M) se quitan antes: no añaden aristas.", size=22, color="muted", center=True)
    segs.append((s, "Construimos el grafo dirigido con la clase Digrafo: para cada número x y cada operación, ponemos una arista de x al resultado de aplicar la operación. "
                    "Con diez mil números y cien operaciones son hasta un millón de aristas por caso. Antes quitamos las operaciones repetidas, que no añaden aristas.", 0))

    # código
    s = Slide("El código", "EJ_05-1.cpp")
    s.code(24, 84, 700, 520, CODE, hl={L_T, L_FOR, L_NEW} | set(L_SET), title="class TransformacionModular")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["dist[x] = -1 significa: aún sin visitar.",
                              "Se saca x de la cola; si es T, ya tiene su distancia mínima.",
                              "Los vecinos de x son g.ady(x); si y es nuevo: dist + 1 y a la cola.",
                              "La respuesta es dist[T]: queda en -1 si no se alcanza."], size=20, gap=16)
    segs.append((s, "En el código, dist vale menos uno para los números sin visitar. Sacamos x de la cola, y si es el objetivo ya tiene su distancia mínima y paramos. "
                    "Si no, recorremos los adyacentes de x: si un vecino es nuevo, le damos la distancia más uno y lo metemos en la cola. "
                    "La respuesta es dist del objetivo, que se queda en menos uno si nunca se alcanza.", 0))

    # traza
    pasos = traza()
    n = len(pasos)
    for k, (tipo, x, y, i, dist, q) in enumerate(pasos, 1):
        if tipo == "ini":
            hl = set(L_INI)
            cap = "dist[1] = 0 y el 1 entra en la cola"
            nar = "Empezamos en el uno: distancia cero, y a la cola."
        elif tipo == "saca":
            hl = {L_POP, L_T}
            cap = f"Sacamos el {x}: no es el objetivo, probamos las dos operaciones"
            nar = f"Sacamos el {x}. No es el objetivo, así que probamos las dos operaciones."
        elif tipo == "nuevo":
            a, b = OPS[i]
            hl = {L_FOR, L_NEW} | set(L_SET)
            cap = f"{a}·{x} + {b} = {a * x + b}  →  mod 5 = {y}: nuevo, dist[{y}] = {dist[y]}"
            nar = f"Operación {i + 1}: {a} por {x} más {b}, {a * x + b}, módulo cinco, {y}. Es nuevo: distancia {dist[y]}."
        elif tipo == "visto":
            a, b = OPS[i]
            hl = {L_FOR, L_NEW}
            cap = f"{a}·{x} + {b} = {a * x + b}  →  mod 5 = {y}: ya visitado, se ignora"
            nar = f"Operación {i + 1}: da {y}, que ya estaba visitado. Se ignora."
        else:
            hl = {L_POP, L_T}
            cap = f"Sacamos el {x} = objetivo: distancia {dist[x]}, paramos"
            nar = f"Sacamos el {x}, que es el objetivo. Su distancia es {dist[x]}: esa es la respuesta."
        segs.append((slide_paso(k, n, tipo, x, y, i, dist, q, hl, cap), nar, 0))

    # casos especiales
    s = Slide("Casos del enunciado")
    s.box(40, 90, 620, 440, "ejemplo 3: M = 10, inicio 2, objetivo 1, operación 2x")
    P3 = {2: (150, 250), 4: (300, 170), 8: (450, 250), 6: (300, 340), 1: (110, 440)}
    E3 = [(2, 4), (4, 8), (8, 6), (6, 2), (1, 2)]
    s.dgraph(P3, E3, ns={2: ("blue", "node_t", None), 1: ("red", "node_t", None)}, r=26,
             es={e: ("muted", 4) for e in E3})
    s.bullets(690, 110, 540, [
        ("2 → 4 → 8 → 6 → 2: un ciclo de números pares.", "text"),
        ("Al 1 no llega ninguna flecha: es inalcanzable ⇒ -1.", "red"),
        "Ejemplo 4: M = 6, inicio 4, objetivo 4  ⇒  0 jugadas.",
        "Ejemplo 1: 2 → 6 con 2x + 2 en una sola jugada  ⇒  1.",
    ], size=21, gap=16)
    segs.append((s, "Veamos los otros casos. Con módulo diez y la operación doble de x, desde el dos solo se recorre el ciclo dos, cuatro, ocho, seis: todos pares. "
                    "Al uno no llega ninguna flecha, así que la respuesta es menos uno. Si el inicio y el objetivo coinciden, son cero jugadas.", 0))

    segs.append((ideas("Resultado y coste", [
        "Ejemplo 2: 1 → 3 → 0 con 2x+1 y luego 3x+1: 2 jugadas.",
        "Si el BFS no llega a T, dist[T] = -1.",
        "Coste: O(M · N) por caso (construir el grafo y recorrerlo).",
        "Con M ≤ 10.000, N ≤ 100 y 500 casos: hasta 5·10⁸ aristas en el peor caso.",
        ("Por eso conviene cortar el BFS al llegar a T y quitar operaciones repetidas.", "muted"),
    ]), "El camino del ejemplo es uno, tres, cero: primero la operación uno y luego la dos, en dos jugadas. "
        "El coste es el número de números por el número de operaciones, en cada caso. "
        "En el peor caso son muchas aristas, por eso conviene parar al llegar al objetivo y quitar operaciones repetidas.", 0))

    segs.append((cierre(NOMBRE, [
        "Los números 0 … M−1 son vértices; cada operación, una arista dirigida de un Digrafo.",
        "Mínimo de jugadas = camino más corto de S a T  ⇒  BFS.",
        "Se construye con ponArista(x, (a·x + b) mod M) y se recorre con g.ady(x).",
        "Si no se alcanza T: -1.   Coste O(M · N).",
    ]), "Resumiendo: los números son vértices y cada operación es una arista dirigida. "
        "El mínimo de jugadas es el camino más corto, que se calcula con un B F S sobre ese grafo. Si no se alcanza el objetivo, menos uno.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-1_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-1_transformacion_modular.mp4")
        print(f"05-1: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
