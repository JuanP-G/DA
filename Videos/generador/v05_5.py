"""Vídeo EJ 05-5 · Haciendo trampas en Serpientes y Escaleras"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, font, C

CPP = "../../5-Grafos dirigidos/EJ_05-5/EJ_05-5.cpp"
NOMBRE = "Haciendo trampas en Serpientes y Escaleras"
TEMA = "Tema 5 · Grafos dirigidos"

# ejemplo 2 del enunciado: N=4, K=2, serpiente 14→2, escalera 3→12
N, K = 4, 2
SNAKES, LADDERS = [(14, 2)], [(3, 12)]
CAS = N * N

L_DEST = find_line(CPP, "destino[a - 1] = b - 1;")
L_ARI = find_line(CPP, "g.ponArista(v, destino[v + d]);")
L_BFS = find_line(CPP, "void bfs(")
L_FIN = find_line(CPP, "if (v == fin) return;")
L_REL = find_line(CPP, "if (dist[w] == -1)")
L_DIST = find_line(CPP, "dist[w] = dist[v] + 1;")
CODE_T = code_lines(CPP, find_line(CPP, "class Tiradas"), find_line(CPP, "};", L_BFS), maxc=60)
CODE_G = code_lines(CPP, find_line(CPP, "int casillas = N * N;"), L_ARI + 1, maxc=60)

DEST = list(range(CAS))
for a, b in SNAKES + LADDERS:
    DEST[a - 1] = b - 1

NIVEL = ["blue_d", "green_d", "purple_d", "gold_d", "red_d"]


def centro(c, x0, y0, cell):
    """Centro de la casilla c (0-based) en el tablero con numeración en zigzag desde abajo a la izquierda."""
    fila, col = divmod(c, N)
    if fila % 2 == 1:
        col = N - 1 - col
    return x0 + col * cell + cell // 2, y0 + (N - 1 - fila) * cell + cell // 2


def tablero(s, x0, y0, cell, dist=None, actual=None, ring=(), flechas=()):
    for c in range(CAS):
        cx, cy = centro(c, x0, y0, cell)
        fill = "panel"
        if dist is not None and dist[c] >= 0:
            fill = NIVEL[dist[c] % len(NIVEL)]
        s.d.rectangle((cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2), fill=C[fill], outline=C["border"], width=2)
        s.text((cx - cell // 2 + 6, cy - cell // 2 + 4), str(c + 1), size=16, color="muted", bold=True)
        if dist is not None and dist[c] >= 0:
            s.text((cx, cy + 10), str(dist[c]), size=26, color="text", bold=True, anchor="mm")
        if c == actual:
            s.d.rectangle((cx - cell // 2 + 2, cy - cell // 2 + 2, cx + cell // 2 - 2, cy + cell // 2 - 2), outline=C["gold"], width=5)
        elif c in ring:
            s.d.rectangle((cx - cell // 2 + 3, cy - cell // 2 + 3, cx + cell // 2 - 3, cy + cell // 2 - 3), outline=C["blue"], width=3)
    for (a, b), col in flechas:
        (xa, ya), (xb, yb) = centro(a - 1, x0, y0, cell), centro(b - 1, x0, y0, cell)
        s.d.line((xa, ya, xb, yb), fill=C[col], width=6)
        s.d.ellipse((xb - 8, yb - 8, xb + 8, yb + 8), fill=C[col])


FLECHAS = [((a, b), "red") for a, b in SNAKES] + [((a, b), "blue") for a, b in LADDERS]


def traza():
    """Mismo BFS que EJ_05-5.cpp: eventos (pop, dist, cola, nuevos)."""
    ady = [[] for _ in range(CAS)]
    for v in range(CAS):
        for d in range(1, K + 1):
            if v + d < CAS:
                ady[v].append(DEST[v + d])
    dist = [-1] * CAS
    q = deque([0])
    dist[0] = 0
    ev = []
    while q:
        v = q.popleft()
        if v == CAS - 1:
            ev.append((v, dist[:], list(q), [], []))
            break
        nuevos, vistos = [], []
        for w in ady[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                q.append(w)
                nuevos.append(w)
            else:
                vistos.append(w)
        ev.append((v, dist[:], list(q), nuevos, vistos))
    return ev, ady


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-5", TEMA),
             "Haciendo trampas en Serpientes y Escaleras. Con un dado trucado, vemos cómo el tablero se convierte en un grafo dirigido "
             "y por qué el mínimo de tiradas es un recorrido en anchura.", 0)]

    segs.append((ideas("El problema", [
        "Tablero de N × N casillas numeradas de 1 a N² (en zigzag), con serpientes y escaleras.",
        "Dado con K caras (1 … K) TRUCADO: elegimos la cara que sale en cada tirada.",
        "Si caemos en el extremo de una serpiente o escalera, vamos al otro extremo.",
        ("¿Cuál es el mínimo número de tiradas para llegar de la casilla 1 a la N²?", "gold"),
    ]), "Tenemos un tablero de serpientes y escaleras con casillas numeradas de uno a N al cuadrado, y un dado con K caras que podemos trucar: elegimos qué cara sale. "
        "Si caemos en el extremo de una serpiente o de una escalera, la ficha va al otro extremo. "
        "Queremos el mínimo de tiradas para llegar de la casilla uno a la última.", 0))

    # tablero
    s = Slide("Ejemplo 2: tablero 4 × 4, dado de 2 caras", TEMA)
    s.box(40, 90, 560, 500, "serpiente 14 → 2 (rojo) · escalera 3 → 12 (azul)")
    tablero(s, 100, 150, 110, flechas=FLECHAS)
    s.bullets(640, 120, 600, [
        "La numeración en zigzag no importa: solo cuenta el NÚMERO de cada casilla.",
        "Serpientes y escaleras son lo mismo: un salto obligatorio.",
        ("Desde la casilla 1, tirar un 2 lleva a la 3 y la escalera sube a la 12.", "gold"),
        "Es DIRIGIDO: se sube de la 3 a la 12, pero no se baja.",
    ], size=21, gap=16)
    segs.append((s, "En el segundo ejemplo, el tablero es de cuatro por cuatro, con un dado de dos caras, una escalera de la tres a la doce, y una serpiente de la catorce a la dos. "
                    "La numeración en zigzag no importa, solo el número de cada casilla, y las serpientes y las escaleras son lo mismo: un salto obligatorio. "
                    "Por ejemplo, desde la casilla uno, un dos lleva a la tres, y la escalera sube a la doce.", 0))

    # modelo
    s = Slide("El grafo: una arista por tirada", TEMA)
    s.box(40, 90, 1200, 190, "casilla c  →  vértice c − 1;   destino[c] = c, salvo en el origen de una serpiente o escalera")
    s.text((70, 150), "desde v, con d = 1 … K:", size=24, bold=True)
    s.text((70, 196), "v  →  destino[v + d]", size=34, mono=True, color="gold", bold=True)
    s.text((600, 150), "Cada arista es UNA tirada.", size=24, color="text")
    s.text((600, 196), "mínimo de tiradas = camino con menos aristas", size=22, color="green", bold=True)
    s.text((600, 232), "⇒  BFS desde la casilla 1", size=22, color="green", bold=True)
    s.box(40, 300, 1200, 300, "aristas de las primeras casillas (K = 2)")
    filas = [("1", "2, 3→12", "tirar 1 → casilla 2;   tirar 2 → casilla 3, y la escalera sube a la 12"),
             ("2", "3→12, 4", "tirar 1 → casilla 3 → 12;   tirar 2 → casilla 4"),
             ("12", "13, 14→2", "tirar 1 → casilla 13;   tirar 2 → casilla 14, y la serpiente baja a la 2"),
             ("15", "16", "tirar 1 → casilla 16;   tirar 2 se pasaría de la última: no hay arista")]
    for i, (a, b, c) in enumerate(filas):
        y = 350 + i * 56
        s.text((70, y), f"casilla {a}", size=22, bold=True, color="blue")
        s.text((250, y), f"→  {b}", size=22, mono=True, color="gold")
        s.text((480, y + 2), c, size=19, color="muted")
    segs.append((s, "El grafo tiene un vértice por casilla, y desde cada casilla sale una arista por cada cara del dado: "
                    "tirando un d, vamos a destino de v más d, que es la propia casilla salvo que sea el origen de una serpiente o escalera. "
                    "Cada arista es una tirada, así que el mínimo de tiradas es el camino con menos aristas: un recorrido en anchura. "
                    "Por ejemplo, desde la casilla uno vamos a la dos, o a la doce por la escalera; desde la doce, a la trece, o a la dos por la serpiente.", 0))

    # código
    s = Slide("El código (1): construir el digrafo", "EJ_05-5.cpp")
    s.code(24, 84, 760, 520, CODE_G, hl={L_DEST, L_ARI}, title="resuelveCaso()")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["destino[c] = c, salvo en el origen de una serpiente o escalera (se tratan igual).",
                              "Para cada casilla v y cada d = 1 … K (sin pasarse): arista v → destino[v + d].",
                              "El enunciado garantiza que la meta es alcanzable."], size=19, gap=14)
    segs.append((s, "En el código, primero se rellena destino, que es la propia casilla salvo en los extremos de las serpientes y escaleras, que se tratan igual. "
                    "Después, para cada casilla y cada cara del dado sin pasarse del final, se añade una arista a destino de v más d.", 0))
    s = Slide("El código (2): el BFS", "EJ_05-5.cpp")
    s.code(24, 84, 760, 520, CODE_T, hl={L_FIN, L_REL, L_DIST}, title="class Tiradas")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["BFS desde la casilla 1 (vértice 0).",
                              "dist[w] = dist[v] + 1 la primera vez que se llega a w.",
                              "Se para al sacar de la cola la última casilla: su distancia ya es mínima.",
                              "dist = −1 significa «aún no visitada»."], size=19, gap=14)
    segs.append((s, "Y el recorrido en anchura calcula las distancias desde la casilla uno: la primera vez que llegamos a una casilla, su distancia es la del vértice más uno. "
                    "Paramos al sacar la última casilla de la cola, porque su distancia ya es mínima.", 0))

    # traza BFS
    ev, ady = traza()
    for k, (v, dist, cola, nuevos, vistos) in enumerate(ev, 1):
        s = Slide("Ejemplo 2: el BFS", f"paso {k} de {len(ev)}")
        s.box(24, 84, 520, 520, "tablero: número = tiradas mínimas")
        tablero(s, 64, 150, 108, dist=dist, actual=v, ring=set(nuevos), flechas=FLECHAS)
        s.box(564, 84, 692, 520, "estado")
        s.text((590, 124), f"se saca la casilla {v + 1}  (dist = {dist[v]})", size=24, bold=True, color="gold")
        if v == CAS - 1:
            s.wrap(590, 180, 640, "Es la última casilla: su distancia ya es mínima. Fin del BFS.", size=22, color="green", bold=True)
            s.text((590, 260), f"respuesta:  {dist[v]}", size=44, bold=True, color="gold")
            cap = f"se saca la casilla {CAS}: dist = {dist[v]}  ⇒  mínimo de tiradas = {dist[v]}"
            nar = f"Sacamos la casilla {CAS}, la última. Su distancia es {dist[v]}: la respuesta es {dist[v]}."
        else:
            y = 180
            for d, w in enumerate(ady[v], 1):
                tag = "nueva" if w in nuevos else "ya vista"
                col = "green" if w in nuevos else "dim"
                esc = ""
                if v + d < CAS and DEST[v + d] != v + d:
                    esc = f"  (casilla {v + d + 1}, salto a la {w + 1})"
                s.text((590, y), f"tirar {d}  →  casilla {w + 1}{esc}", size=22, mono=False, color="text")
                s.text((1120, y), tag, size=20, color=col, bold=True)
                y += 44
            s.queue_row(590, 330, "cola", [c + 1 for c in cola], size=17)
            s.text((590, 400), "dist (por casilla):", size=17, color="muted", bold=True)
            s.cells(590, 430, "", [d if d >= 0 else "·" for d in dist[:8]], cw=54, first=1, idx=True)
            s.cells(590, 500, "", [d if d >= 0 else "·" for d in dist[8:]], cw=54, first=9, idx=True)
            nn = ", ".join(str(w + 1) for w in nuevos) if nuevos else "ninguna"
            cap = f"casilla {v + 1}: casillas nuevas {nn}  ·  dist = {dist[v] + 1}" if nuevos else f"casilla {v + 1}: no hay casillas nuevas"
            nar = (f"Sacamos la casilla {v + 1}, a {dist[v]} tiradas. " +
                   (("Las casillas nuevas son: " + ", ".join(str(w + 1) for w in nuevos) + f", todas a {dist[v] + 1} tiradas.") if nuevos else "Todas sus casillas ya estaban vistas."))
        s.caption(cap, y=628)
        segs.append((s, nar, 0))

    # ejemplo 1
    s = Slide("Ejemplo 1: tablero 10 × 10, dado de 6 caras", TEMA)
    s.box(40, 100, 1200, 250, "cinco serpientes y seis escaleras; las que importan: 6 → 47 · 51 → 94")
    pasos = [("casilla 1", "gold"), ("6 → 47", "blue"), ("51 → 94", "blue"), ("100", "green")]
    x = 80
    for i, (tx, col) in enumerate(pasos):
        w = int(s.d.textlength(tx, font=font(26, True))) + 36
        s.pill(x, 190, tx, fill=col, size=26, padx=18, pady=10)
        x += w + 20
        if i < len(pasos) - 1:
            s.text((x, 192), "→", size=32, color="muted")
            x += 56
    s.text((90, 270), "tirada 1: un 5 (1 → 6, escalera a la 47)   ·   tirada 2: un 4 (47 → 51, escalera a la 94)   ·   tirada 3: un 6 (94 → 100)", size=18, color="muted")
    s.bullets(60, 390, 1160, [
        ("Resultado: 3 tiradas.", "gold"),
        "Gracias a poder ELEGIR la cara, el BFS siempre prefiere la escalera que más ayuda.",
        "No hace falta tratar aparte las serpientes: si caer en una es malo, el BFS elige otra cara.",
    ], size=22, gap=16)
    segs.append((s, "En el primer ejemplo, el tablero es de diez por diez. Con un cinco caemos en la seis, y la escalera sube a la cuarenta y siete; "
                    "con un cuatro llegamos a la cincuenta y una, y otra escalera sube a la noventa y cuatro; y con un seis llegamos a la cien. Tres tiradas. "
                    "Como podemos elegir la cara, el recorrido siempre prefiere las escaleras que ayudan, y no hace falta tratar aparte las serpientes.", 0))

    segs.append((ideas("Detalles y coste", [
        "Por qué BFS: todas las aristas cuestan 1 (una tirada), y el BFS da el camino con menos aristas.",
        "Solo valen las tiradas que no se pasan de la última casilla (v + d < N²).",
        "Cada casilla es extremo de como mucho una serpiente o escalera; la 1 y la última nunca.",
        "Es dirigido: las escaleras se suben y las serpientes se bajan, pero no al revés.",
        ("Coste: O(N² · K) por caso (N² vértices con K aristas cada uno).", "gold"),
    ]), "Usamos el recorrido en anchura porque todas las aristas cuestan uno, una tirada. Solo valen las tiradas que no se pasan de la última casilla. "
        "El grafo es dirigido, porque las escaleras se suben y las serpientes se bajan, pero no al revés. "
        "Y el coste es N al cuadrado por K, porque hay N al cuadrado vértices con K aristas cada uno.", 0))

    segs.append((cierre(NOMBRE, [
        "Casilla = vértice; tirar d desde v = arista v → destino[v + d].",
        "Serpientes y escaleras: destino[c] = su otro extremo.",
        "Mínimo de tiradas = camino más corto en aristas: BFS desde la casilla 1.",
        "Parar al sacar la última casilla.",
        "Coste O(N² · K).",
    ]), "Resumiendo: cada casilla es un vértice, y cada cara del dado es una arista que va al destino de v más d, aplicando antes la serpiente o la escalera. "
        "Como cada arista es una tirada, el mínimo de tiradas lo da un recorrido en anchura desde la casilla uno, que paramos al sacar la última.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-5_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-5_serpientes_y_escaleras.mp4")
        print(f"05-5: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
