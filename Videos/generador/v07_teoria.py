"""Vídeo 07-0 · Tema 7: dígrafos valorados y caminos de coste mínimo (Dijkstra).

Las trazas salen de simular Dijkstra con el mismo criterio que el código (v07_comun.traza). El código que sale
en pantalla se lee de las cabeceras reales: Estructuras de datos/DigrafoValorado.h y DigrafoValorado_algoritmos.h.
"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C, W, H, font
from v07_comun import traza, dibuja_grafo, etiquetas, INF, FINITO

DV = "../../Estructuras de datos/DigrafoValorado.h"
AL = "../../Estructuras de datos/DigrafoValorado_algoritmos.h"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# El digrafo de las transparencias (8 vértices)
EDGES = [(0, 1, 5), (0, 7, 8), (0, 4, 9), (1, 3, 15), (1, 2, 12), (1, 7, 4), (7, 2, 7), (7, 5, 6),
         (4, 7, 5), (4, 5, 4), (4, 6, 20), (5, 2, 1), (5, 6, 13), (2, 3, 3), (2, 6, 11), (3, 6, 9)]
POS = {0: (90, 300), 1: (250, 170), 3: (610, 170), 7: (250, 320), 2: (440, 310), 5: (330, 450), 4: (90, 520), 6: (680, 520)}


def pick(path, nums):
    ls = open(path, encoding="utf-8", errors="replace").read().split("\n")
    return [(n, ls[n - 1]) for n in nums]


def limpia(ls):
    return [(n, t) for n, t in ls if t.strip()]


def tabla_estado(s, paso, x, y, w, h, hot=None):
    s.box(x, y, w, h, "dist[]  y  ulti[]")
    cabecera = y + 40
    s.text((x + 30, cabecera), "v", size=18, color="muted", bold=True)
    s.text((x + 110, cabecera), "dist", size=18, color="muted", bold=True)
    s.text((x + 230, cabecera), "ulti", size=18, color="muted", bold=True)
    for v in range(8):
        yy = cabecera + 34 + v * 38
        if hot == v:
            s.d.rectangle((x + 10, yy - 4, x + w - 10, yy + 30), fill=(78, 66, 30))
        d = paso["dist"][v]
        s.text((x + 30, yy), str(v), size=22, bold=True, color="text")
        s.text((x + 110, yy), "∞" if not FINITO(d) else str(d), size=22, mono=True, color="green" if paso["done"][v] else "text")
        u = paso["ulti"][v]
        s.text((x + 230, yy), "–" if u is None else f"{u} → {v}", size=22, mono=True, color="blue" if u is not None else "dim")
    cola = [f"{v}({paso['dist'][v]})" for v in paso["cola"]]
    s.queue_row(x + 16, y + h - 54, "cola", cola, size=16)


def slide_dij(k, n, paso, cap, titulo="Dijkstra paso a paso"):
    s = Slide(titulo, f"paso {k} de {n}")
    s.box(24, 84, 740, 520, "el digrafo de las transparencias (origen: 0)")
    dibuja_grafo(s, POS, EDGES, paso, dirigido=True, r=22, hl_edge=paso.get("k"), first=0)
    tabla_estado(s, paso, 784, 84, 472, 520, hot=paso.get("w") if paso.get("w") is not None else paso.get("v"))
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs, cap = [], {}

    def add(sl, nar, dmin=0, cap_title=None):
        if cap_title:
            cap[len(segs)] = cap_title
        segs.append((sl, nar, dmin))

    # ------------------------------------------------------------------ 0 · portada y plan
    add(portada("Dígrafos valorados y caminos mínimos", "TEMA 7", "Relajación de aristas · Dijkstra"),
        "Tema siete. Dígrafos valorados y caminos de coste mínimo. En este vídeo vemos cómo funciona el algoritmo de Dijkstra, paso a paso, "
        "y cómo se adapta a los tres ejercicios de la semana.", cap_title="Introducción")
    s = Slide("Plan del vídeo", TEMA)
    s.bullets(70, 120, W - 140, [
        ("1 · Dígrafos valorados: AristaDirigida y DigrafoValorado.", "text"),
        ("2 · Caminos de coste mínimo: dist, ulti y árbol de caminos mínimos.", "text"),
        ("3 · Relajación de aristas y condiciones de optimalidad.", "text"),
        ("4 · El algoritmo de Dijkstra: idea, traza, código, corrección y coste.", "gold"),
        ("5 · Recuperar el camino, y Dijkstra con un vector en vez de una cola.", "text"),
        ("6 · ¿Es el árbol de caminos mínimos un árbol de recubrimiento mínimo?", "text"),
        ("7 · Ejercicios 07-1, 07-2 y 07-3.", "gold"),
    ], size=25, gap=18)
    add(s, "Veremos los dígrafos valorados, qué es un camino de coste mínimo y cómo se representa, la relajación de aristas y las condiciones de optimalidad. "
           "Después, el algoritmo de Dijkstra con una traza completa, su código, su corrección y su coste. Veremos cómo recuperar el camino, la variante con un vector, "
           "si el árbol de caminos mínimos es un árbol de recubrimiento mínimo, y los tres ejercicios.")

    # ------------------------------------------------------------------ 1 · dígrafos valorados
    s = Slide("Dígrafos valorados", TEMA)
    s.text((70, 100), "Un grafo con aristas orientadas, y un VALOR (peso, coste, tiempo) en cada una.", size=24, bold=True, color="gold")
    s.box(40, 150, 620, 430, "ejemplo: 5 vértices, 8 aristas")
    P = {0: (130, 300), 1: (300, 200), 2: (340, 410), 3: (500, 330), 4: (560, 520)}
    E = [(0, 1, 18), (0, 2, 10), (1, 0, 25), (1, 2, 30), (2, 3, 20), (3, 1, 40), (3, 4, 35), (4, 2, 50)]
    p0 = dict(dist=[INF] * 5, ulti=[None] * 5, done=[False] * 5, cola=[], tipo="ini")
    dibuja_grafo(s, P, E, p0, dirigido=True, r=22)
    s.text((700, 170), "_ady  (lista de aristas que SALEN de cada vértice)", size=18, color="muted", bold=True)
    for v in range(5):
        lst = "  ".join(f"{b}({c})" for a, b, c in E if a == v)
        s.text((700, 215 + v * 44), f"{v}:", size=22, mono=True, color="gold")
        s.text((750, 215 + v * 44), lst, size=22, mono=True)
    s.wrap(700, 450, 520, "Una arista v → w se guarda UNA vez, en la lista de v. A diferencia del GrafoValorado del tema 6, aquí tiene sentido.", size=20, color="text")
    add(s, "Un dígrafo valorado es un grafo con aristas orientadas, y un valor en cada una: un peso, un coste, un tiempo. "
           "Se guarda con listas de adyacencia: cada arista va de v a w, y se guarda una sola vez, en la lista de v. "
           "A diferencia del grafo valorado del tema seis, aquí las aristas tienen sentido.", cap_title="Dígrafos valorados")

    s = Slide("DigrafoValorado.h", TEMA)
    s.code(24, 84, 600, 330, [(20, "AristaDirigida(int v, int w, Valor valor)")] + pick(DV, [22, 24, 26, 32, 33, 34]), hl={22, 24, 26}, title="AristaDirigida<Valor>")
    s.code(644, 84, 612, 330, pick(DV, [63, 92, 93, 94, 95, 96, 97, 98, 111, 112, 113, 114, 115]), hl={97, 114}, title="DigrafoValorado<Valor>")
    s.bullets(60, 450, 1160, [
        "desde(), hasta(), valor(): los tres datos de la arista.   ady(v): las aristas que SALEN de v.",
        "ponArista añade v → w solo a la lista de v.   inverso() da la vuelta a todas las aristas.",
        "Para un grafo NO dirigido: llamar dos veces a ponArista, v → w y w → v.",
    ], size=20, gap=10)
    add(s, "La arista dirigida guarda el vértice de origen, el de destino y el valor, con los métodos desde, hasta y valor. "
           "El dígrafo valorado tiene ponArista, que añade la arista solo a la lista de v, ady de v, que devuelve las aristas que salen de v, e inverso, que da la vuelta a todas. "
           "Para representar un grafo no dirigido, basta llamar dos veces a ponArista, una en cada sentido. Es lo que haremos en los ejercicios con calles de doble sentido.")

    # ------------------------------------------------------------------ 2 · caminos mínimos
    add(ideas("Caminos de coste mínimo", [
        "Dado un dígrafo valorado, encontrar el camino mínimo de s a t.",
        "¿Entre qué vértices?  Origen único (s → todos), destino único, de punto a punto, o entre todos los pares.",
        "Pesos: no negativos (Dijkstra), arbitrarios (Bellman-Ford).   Ciclos: con o sin ciclos.",
        ("Esta semana: ORIGEN ÚNICO con pesos NO NEGATIVOS.", "gold"),
        "Todos los caminos mínimos desde s forman un ÁRBOL de caminos mínimos.",
    ], note="Se representa con dos vectores: dist[v] (longitud del camino más corto de s a v) y ulti[v] (la última arista de ese camino)."),
        "El problema: dado un dígrafo valorado, encontrar el camino de coste mínimo de un vértice s a otro t. Hay variantes según los vértices que se pidan, "
        "los pesos, que pueden ser no negativos o arbitrarios, y la presencia de ciclos. Esta semana estudiamos origen único con pesos no negativos. "
        "Todos los caminos mínimos desde el origen forman un árbol, que se guarda con dos vectores: dist, la longitud del camino más corto, y ulti, la última arista de ese camino.",
        cap_title="Caminos de coste mínimo")

    pf = traza(8, EDGES, 0)[-1]
    s = Slide("El árbol de caminos mínimos", TEMA)
    s.box(24, 84, 740, 520, "origen 0: las aristas azules son ulti[]")
    dibuja_grafo(s, POS, EDGES, dict(pf, tipo="fin", v=None, cola=[]), dirigido=True, r=22)
    tabla_estado(s, pf, 784, 84, 472, 520)
    s.caption("dist[v] = longitud del camino mínimo de 0 a v;  ulti[v] = su última arista.  Hacia atrás desde 6: 2, 5, 4, 0", y=628)
    add(s, "Aquí vemos el resultado final para un dígrafo de ejemplo con el origen en el vértice cero. La tabla guarda, para cada vértice, la distancia mínima y la última arista del camino. "
           "Y las aristas azules forman el árbol de caminos mínimos. Para llegar al seis, por ejemplo, la última arista es la que sale del dos; antes, la que sale del cinco; antes, la del cuatro; y antes, la del cero.")

    # ------------------------------------------------------------------ 3 · relajación
    def rel(titulo, dw, nar, cap_txt, mejora):
        s = Slide(titulo, TEMA)
        s.box(40, 90, 1200, 420, "relajar la arista v → w")
        pl = {0: (190, 380), 1: (600, 220), 2: (1010, 380)}
        d = dict(dist=[0, 30, dw if not mejora else 55], ulti=[None] * 3, done=[False] * 3, cola=[], tipo="ini")
        ed = [(0, 1, 30), (1, 2, 25), (0, 2, "?")]
        s.dgraph({0: pl[0], 1: pl[1], 2: pl[2]}, [(0, 1), (1, 2)], ns={0: ("blue", "node_t", None), 1: ("gold", "node_t", None), 2: ("node", "node_t", "text")},
                 es={(0, 1): ("muted", 4), (1, 2): ("gold", 6)}, labels=["s", "v", "w"], r=34, lsize=26)
        etiquetas(s, pl, [(0, 1, 30), (1, 2, 25)], {1: "gold"})
        s.text((600, 175), "dist[v] = 30", size=22, bold=True, color="gold", anchor="mm")
        s.text((1010, 440), f"dist[w] = {dw}" + ("   →   55" if mejora else ""), size=22, bold=True, color="green" if mejora else "text", anchor="mm")
        s.text((60, 540), "void relajar(AristaDirigida<Valor> a) {", size=22, mono=True)
        s.text((60, 575), "   if (dist[w] > dist[v] + a.valor()) { dist[w] = dist[v] + a.valor(); ulti[w] = a; }", size=22, mono=True, color="gold")
        s.text((60, 610), "}", size=22, mono=True)
        s.caption(cap_txt, y=655)
        return s
    add(rel("Relajación de aristas (1)", 70, "", "dist[v] + valor = 30 + 25 = 55 < 70 = dist[w]  ⇒  se actualizan dist[w] y ulti[w]", True),
        "La operación básica es relajar una arista. Supongamos que conocemos un camino hasta v de longitud treinta, y otro hasta w de longitud setenta. "
        "Si la arista de v a w cuesta veinticinco, pasar por v nos daría un camino hasta w de longitud cincuenta y cinco, que es menor que setenta. "
        "Entonces actualizamos dist de w a cincuenta y cinco, y ulti de w pasa a ser esa arista.", cap_title="Relajación y optimalidad")
    add(rel("Relajación de aristas (2)", 40, "", "dist[v] + valor = 30 + 25 = 55 ≥ 40 = dist[w]  ⇒  no se cambia nada", False),
        "Si, en cambio, ya conocíamos un camino hasta w de longitud cuarenta, pasar por v no mejora nada, y no cambiamos nada.")

    add(ideas("Condiciones de optimalidad", [
        "dist[] contiene las distancias mínimas desde s si y solo si:",
        ("1 · dist[s] = 0", "gold"),
        ("2 · para todo v, dist[v] es la longitud de ALGÚN camino de s a v", "gold"),
        ("3 · para toda arista v → w:   dist[w] ≤ dist[v] + valor(v → w)", "gold"),
        "Necesarias: si alguna arista se pudiera relajar, habría un camino más corto.",
        "Suficientes: se suman las desigualdades a lo largo de un camino mínimo.",
    ]), "¿Cuándo sabemos que dist tiene las distancias mínimas? Si y solo si se cumplen tres condiciones. Primera, la distancia del origen es cero. "
        "Segunda, la distancia de cada vértice es la longitud de algún camino real desde el origen. Y tercera, para toda arista de v a w, la distancia de w es menor o igual que la de v más el valor de la arista; "
        "es decir, ninguna arista se puede relajar más. Es necesaria porque, si alguna arista se pudiera relajar, habría un camino más corto. "
        "Y es suficiente porque, si sumamos esas desigualdades a lo largo de un camino mínimo, la distancia de w es menor o igual que la longitud de ese camino.")

    # ------------------------------------------------------------------ 4 · Dijkstra
    add(ideas("El algoritmo de Dijkstra", [
        "Considera los vértices en ORDEN CRECIENTE de distancia desde el origen.",
        "Añade el vértice al árbol y relaja todas las aristas que salen de él.",
        "Con una cola de prioridad variable (IndexPQ) ordenada por dist.",
        ("Requisito: todos los valores ≥ 0.", "gold"),
    ], note="1) dist[origen] = 0 y pq.push(origen, 0).   2) mientras haya cola: v = pq.top(); pop; relajar sus aristas (update si mejora)."),
        "El algoritmo de Dijkstra considera los vértices en orden creciente de distancia desde el origen. Añade el vértice al árbol y relaja todas las aristas que salen de él. "
        "Usa una cola de prioridad variable, la IndexPQ del tema tres, ordenada por la distancia. Y exige que todos los valores sean mayores o iguales que cero.",
        cap_title="El algoritmo de Dijkstra")

    pasos = traza(8, EDGES, 0)
    n = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            c = "dist[0] = 0 y el origen entra en la cola con prioridad 0; el resto, ∞"
            nar = "Empezamos: la distancia del origen es cero y entra en la cola. El resto, infinito."
        elif t == "saca":
            c = f"pop: sale el vértice {v}, dist = {p['dist'][v]}: ya es definitiva. Ahora se relajan sus aristas"
            nar = f"Sacamos el vértice {v}, a distancia {p['dist'][v]}. Es el más cercano que queda, y su distancia ya es definitiva."
        else:
            w = p["w"]
            if t == "mejora":
                ant = "∞" if not FINITO(p["ant"]) else p["ant"]
                c = f"{v} → {w}: {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: dist[{w}] = {p['nuevo']}, ulti[{w}] = {v} → {w}"
                nar = f"Arista de {v} a {w}: {p['dist'][v]} más {p['c']} son {p['nuevo']}, " + ("y antes era infinito" if not FINITO(p["ant"]) else f"menos que {p['ant']}") + ". Mejora: actualizamos."
            else:
                c = f"{v} → {w}: {p['dist'][v]} + {p['c']} = {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
                nar = f"Arista de {v} a {w}: {p['nuevo']}, que no mejora {p['dist'][w]}."
        add(slide_dij(k, n, p, c), nar)

    # código
    s = Slide("Dijkstra: el código", "DigrafoValorado_algoritmos.h")
    ini = find_line(AL, "class Dijkstra")
    fin_cls = find_line(AL, "};", ini)
    cod = limpia(code_lines(AL, ini, fin_cls, maxc=64, skip=[(find_line(AL, "// Camino mínimo origen -> v") , find_line(AL, "// Camino mínimo origen -> v") + 9)]))
    s.code(24, 84, 760, 520, cod, hl={find_line(AL, "pq.push(origen, 0);"), find_line(AL, "int v = pq.top().elem; pq.pop();"), find_line(AL, "pq.update(w, dist[w]);")}, title="class Dijkstra")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["dist empieza en INF, ulti sin rellenar, pq para N vértices.",
                              "push(origen, 0) y bucle hasta vaciar la cola.",
                              "pop(): el de menor dist; relajar todas sus aristas.",
                              "relajar: si mejora, dist y ulti, y update en la cola (push si no estaba)."], size=19, gap=14)
    add(s, "En el código, el constructor inicializa dist a infinito, pone a cero la distancia del origen y lo mete en la cola con prioridad cero. "
           "Mientras haya cola, saca el vértice de menor distancia y relaja todas sus aristas. "
           "Y relajar es lo que vimos: si el camino por v mejora la distancia de w, se actualizan dist y ulti, y con update se cambia la prioridad de w en la cola, o se inserta si no estaba.")

    add(ideas("Corrección y coste", [
        "Corrección (valores ≥ 0): cada arista v → w se relaja EXACTAMENTE una vez, al sacar v.",
        "Tras relajarla: dist[w] ≤ dist[v] + valor. Y se mantiene hasta el final:",
        "   · dist[w] no puede aumentar   · dist[v] ya no cambia (es definitiva).",
        ("Se cumplen las condiciones de optimalidad  ⇒  dist son las distancias mínimas.", "green"),
        ("Coste: O(A log V),  espacio adicional O(V).", "gold"),
        "inicializar vectores: V · construir cola: V · pop: V veces, log V · update: A veces, log V.",
    ]), "¿Por qué es correcto? Con valores no negativos, cada arista de v a w se relaja exactamente una vez, cuando se saca v, y deja la desigualdad que pedía la condición de optimalidad. "
        "Esa desigualdad se mantiene hasta el final, porque la distancia de w no puede aumentar, y la de v ya es definitiva. Así que se cumplen las condiciones de optimalidad. "
        "El coste: hacemos V pops y como mucho A updates, cada uno de coste logaritmo de V. En total, A por logaritmo de V, con espacio adicional proporcional a V.")

    # ------------------------------------------------------------------ 5 · camino y vector
    pf = dict(traza(8, EDGES, 0)[-1], tipo="fin", v=None, cola=[])
    camino = [6, 2, 5, 4, 0]
    for i in range(1, len(camino) + 1):
        cur = camino[:i]
        s = Slide("Recuperar el camino con ulti[]", TEMA)
        s.box(24, 84, 740, 520, "camino mínimo de 0 a 6")
        es = {(camino[j + 1], camino[j]): ("gold", 7) for j in range(i - 1)}
        hl = {k: "gold" for k, (a, b, c) in enumerate(EDGES) if (a, b) in es}
        dibuja_grafo(s, POS, EDGES, pf, dirigido=True, r=22, es_extra=es, hl_extra=hl, extra_ns={u: ("green", "node_t", "gold") for u in cur})
        tabla_estado(s, pf, 784, 84, 472, 520, hot=cur[-1])
        s.caption("camino.push_front(ulti[v]):  " + "  ←  ".join(str(u) for u in cur), y=628)
        nar = ("Para recuperar el camino mínimo hasta el seis, retrocedemos con ulti. Empezamos en el seis." if i == 1 else
               f"La última arista que llega a {camino[i - 2]} sale de {camino[i - 1]}." + (" Y hemos llegado al origen." if i == len(camino) else " Seguimos hacia atrás."))
        add(s, nar, cap_title="Camino y variantes" if i == 1 else None)
    add(ideas("El camino completo", [
        "camino: 0 → 4 → 5 → 2 → 6   con coste 9 + 4 + 1 + 11 = 25.",
        "Se retrocede desde el destino con ulti[] y se mete cada arista POR DELANTE (push_front).",
        "Hay que comprobar antes hayCamino(v): dist[v] != INF.",
        "Con dist[destino] ya definitivo se puede parar Dijkstra al sacar el destino.",
    ]), "El camino completo es cero, cuatro, cinco, dos, seis, con coste veinticinco. Lo recuperamos hacia atrás desde el destino con ulti, metiendo cada arista por delante. "
        "Antes hay que comprobar que hay camino, es decir, que la distancia no es infinito. Y si solo nos interesa un destino, podemos parar al sacarlo de la cola.")

    # Dijkstra con vector
    s = Slide("Reflexión: Dijkstra con un vector", TEMA)
    s.bullets(70, 110, W - 140, [
        "La cola de prioridad solo sirve para obtener «el vértice no tratado de menor dist».",
        "Alternativa: un vector dist[] y un tratado[]; en cada paso se RECORRE el vector buscando el mínimo (O(V)).",
        ("Coste total: O(V²) para las búsquedas + O(A) para relajar  =  O(V² + A).", "gold"),
    ], size=24, gap=18)
    s.box(70, 330, 1140, 240, "¿cuál conviene?")
    s.text((100, 380), "Con IndexPQ:   O(A log V)", size=26, mono=True, color="blue")
    s.text((100, 430), "Con vector:    O(V² + A)", size=26, mono=True, color="gold")
    s.text((100, 490), "Grafo disperso (A ≈ V):   gana la cola.        Grafo denso (A ≈ V²):   gana el vector.", size=22, color="text")
    s.text((100, 530), "Está implementado como DijkstraVector en DigrafoValorado_algoritmos.h.", size=20, color="muted")
    add(s, "Una reflexión: la cola de prioridad solo sirve para encontrar el vértice no tratado de menor distancia. "
           "Podemos sustituirla por un vector: en cada paso, recorremos dist buscando el mínimo entre los no tratados, en tiempo proporcional a V. "
           "El coste total pasa a ser V al cuadrado más A. Con la cola, es A por logaritmo de V. "
           "Si el grafo es disperso, con pocas aristas, gana la cola. Si es denso, con del orden de V al cuadrado aristas, gana el vector, que además es más simple.")

    # caminos mínimos vs ARM
    s = Slide("¿Es el árbol de caminos mínimos un ARM?", TEMA)
    s.box(40, 100, 560, 400, "triángulo: 0–1 (2), 1–2 (2), 0–2 (3); origen 0")
    P3 = {0: (120, 420), 1: (320, 190), 2: (520, 420)}
    E3 = [(0, 1, 2), (1, 2, 2), (0, 2, 3)]
    s.graph(P3, [(a, b) for a, b, c in E3], ns={}, es={(0, 1): ("dim", 4), (1, 2): ("dim", 4), (0, 2): ("dim", 4)}, r=26)
    etiquetas(s, P3, E3, {})
    s.box(640, 100, 600, 190, border="blue")
    s.text((660, 114), "ARM:  0–1 y 1–2", size=24, bold=True, color="blue")
    s.text((660, 156), "coste total 4", size=22, color="text")
    s.text((660, 196), "pero el camino 0 → 2 cuesta 4, y hay uno de 3", size=20, color="muted")
    s.box(640, 310, 600, 190, border="gold")
    s.text((660, 324), "Caminos mínimos desde 0:  0–1 y 0–2", size=24, bold=True, color="gold")
    s.text((660, 366), "coste total 5", size=22, color="text")
    s.text((660, 406), "pesa más que el ARM", size=20, color="muted")
    s.wrap(60, 530, 1160, "NO: el árbol de caminos mínimos depende del origen y minimiza la distancia a cada vértice; el ARM no depende del origen y minimiza la suma de las aristas.", size=22, color="text", center=True)
    add(s, "La pregunta del campus: ¿es el árbol de caminos mínimos un árbol de recubrimiento de coste mínimo? En general, no. Este triángulo tiene tres aristas: de cero a uno, dos; de uno a dos, dos; y de cero a dos, tres. "
           "El árbol de recubrimiento mínimo usa las dos aristas de valor dos, y cuesta cuatro. Pero llegar al vértice dos por él cuesta cuatro, mientras que el camino directo cuesta tres. "
           "El árbol de caminos mínimos desde el cero usa la arista de dos y la de tres, y cuesta cinco: más que el ARM. "
           "Son dos preguntas distintas: uno minimiza la distancia a cada vértice, y depende del origen; el otro minimiza la suma de las aristas, y no depende de ningún origen.")

    # ------------------------------------------------------------------ 6 · ejercicios
    add(ideas("07-1 · Navegando sin teclado", [
        "Páginas web con enlaces dirigidos; cada PÁGINA tarda en cargar y cada ENLACE tarda en pulsarse.",
        "Dos tipos de coste: el de los vértices se suma a la arista que ENTRA en ellos.",
        ("coste(v → w) = enlace + carga[w]     y     dist[origen] = carga[origen]", "gold"),
        "Dijkstra directo.  Sin camino: IMPOSIBLE.   Coste O(M log N).",
    ]), "Ejercicio siete uno, navegando sin teclado. Hay páginas con tiempo de carga y enlaces con su tiempo. Hay dos tipos de coste, así que sumamos la carga de cada página a la arista que entra en ella, "
        "y la carga de la primera va en la distancia inicial. Después, Dijkstra directo. Si no se llega, imposible.", cap_title="Los ejercicios")
    add(ideas("07-2 · Camino al cole", [
        "Cuántos caminos de longitud mínima hay de la intersección 1 a la N (calles de doble sentido).",
        "Dijkstra con un vector más: formas[v] = número de caminos mínimos hasta v.",
        ("Mejora ⇒ formas[w] = formas[v].     Empate ⇒ formas[w] += formas[v].", "gold"),
        "formas[0] = 1 (no moverse).   Sin camino: 0.   Cada calle = dos aristas dirigidas.",
    ]), "Ejercicio siete dos, camino al cole. Hay que contar cuántos caminos de longitud mínima existen. Añadimos un vector formas. Si encontramos un camino más corto, sustituimos. "
        "Si empata, sumamos. La casa tiene una forma, y cada calle son dos aristas dirigidas.")
    add(ideas("07-3 · RapidEats con ruta", [
        "Tiempo mínimo entre dos puntos de la ciudad Y la ruta (tramos de doble sentido, hasta 10 pedidos por caso).",
        "Dijkstra directo, y ulti[w] = vértice anterior cada vez que se mejora dist[w].",
        ("La ruta: retroceder desde el destino con ulti y meter por delante.", "gold"),
        "Salida:  «40: 4 -> 3 -> 1»  o  NO LLEGA;  y  ---  después de cada caso.",
    ]), "Ejercicio siete tres, RapidEats con ruta. Dijkstra directo para el tiempo mínimo, y guardamos el vértice anterior para recuperar la ruta, retrocediendo desde el destino. "
        "Si no hay camino, no llega, y después de cada caso, una línea de guiones.")

    add(cierre("Dígrafos valorados y caminos mínimos", [
        "DigrafoValorado: aristas v → w con valor; para no dirigidos, dos ponArista.",
        "Relajar: si dist[v] + valor < dist[w], actualizar dist[w] y ulti[w].",
        "Dijkstra (valores ≥ 0): sacar el más cercano de la IndexPQ y relajar sus aristas.  O(A log V).",
        "Con un vector en vez de cola: O(V² + A), mejor en grafos densos.",
        "El árbol de caminos mínimos NO es en general un ARM.",
    ]), "Resumiendo. El dígrafo valorado guarda aristas con sentido y valor. Relajar una arista es actualizar la distancia y la última arista si el camino por v mejora. "
        "Dijkstra saca siempre el vértice más cercano de la cola y relaja sus aristas, con coste A por logaritmo de V. Con un vector en vez de una cola, el coste es V al cuadrado, mejor en grafos densos. "
        "Y el árbol de caminos mínimos no es, en general, un árbol de recubrimiento mínimo.", cap_title="Resumen")

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-0_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-0_digrafos_valorados_caminos_minimos_teoria.mp4", chapters=cap)
        print(f"07-0: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
