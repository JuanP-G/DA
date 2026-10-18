"""Vídeo 06-0 · Tema 6: conjuntos disjuntos, grafos valorados y árbol de recubrimiento de coste mínimo.

Las trazas salen de simular los algoritmos aquí mismo (los ejercicios del juez aún no tienen .cpp).
El código que sale en pantalla es el de las cabeceras reales de la asignatura:
Estructuras de datos/ConjuntosDisjuntos.h y GrafoValorado.h.
"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C, W, H

CD = "../../Estructuras de datos/ConjuntosDisjuntos.h"
GV = "../../Estructuras de datos/GrafoValorado.h"
TEMA = "Tema 6 · Conjuntos disjuntos y grafos valorados"


# ---------------------------------------------------------------------------
# simulaciones
# ---------------------------------------------------------------------------
class UF:
    """Conjuntos disjuntos para simular: modo 'qf' (búsqueda rápida), 'qu' (unión rápida), 'sz' (por tamaños)."""
    def __init__(self, n, modo):
        self.n, self.modo = n, modo
        self.p = list(range(n))
        self.t = [1] * n
        self.id = list(range(n))

    def raiz(self, a):
        while self.p[a] != a:
            a = self.p[a]
        return a

    def unir(self, a, b):
        if self.modo == "qf":
            ia, ib = self.id[a], self.id[b]
            if ia != ib:
                self.id = [ib if x == ia else x for x in self.id]
            return
        ra, rb = self.raiz(a), self.raiz(b)
        if ra == rb:
            return
        if self.modo == "qu":
            self.p[ra] = rb
        elif self.t[ra] >= self.t[rb]:      # criterio de las transparencias: en empate, b cuelga de a
            self.t[ra] += self.t[rb]
            self.p[rb] = ra
        else:
            self.t[rb] += self.t[ra]
            self.p[ra] = rb


PARES = [(9, 0), (3, 4), (5, 8), (7, 2), (2, 1), (5, 7), (0, 3), (4, 2)]    # autoevaluación 6.1

PAL = [(255, 206, 92), (92, 192, 255), (112, 222, 152), (255, 118, 108), (196, 150, 255),
       (255, 160, 90), (120, 230, 230), (240, 140, 200), (170, 200, 90), (150, 160, 255)]


def forest(s, p, x, y, w, sizes=None, hl=(), dy=62, r=19, color=None):
    """Dibuja el bosque definido por p[] dentro de la caja (x, y, w). Los hijos cuelgan de su padre."""
    n = len(p)
    ch = {}
    for i, q in enumerate(p):
        if q != i:
            ch.setdefault(q, []).append(i)
    raices = [i for i in range(n) if p[i] == i]

    def hojas(v):
        return 1 if v not in ch else sum(hojas(c) for c in ch[v])
    total = sum(hojas(rt) for rt in raices)
    paso = min(100, w / max(1, total))
    pos = {}
    cur = [x]

    def colocar(v, depth):
        if v not in ch:
            pos[v] = (cur[0] + paso / 2, y + depth * dy)
            cur[0] += paso
            return
        xs = []
        for c in sorted(ch[v]):
            colocar(c, depth + 1)
            xs.append(pos[c][0])
        pos[v] = ((xs[0] + xs[-1]) / 2, y + depth * dy)
    for rt in raices:
        colocar(rt, 0)
        cur[0] += 6
    for v, q in enumerate(p):
        if q != v:
            s.d.line((pos[v], pos[q]), fill=C["dim"], width=3)
    for v in range(n):
        px, py = pos[v]
        fill = (color or {}).get(v, C["node"] if p[v] != v else C["gold"])
        if v in hl:
            s.d.ellipse((px - r - 5, py - r - 5, px + r + 5, py + r + 5), outline=C["red"], width=4)
        s.d.ellipse((px - r, py - r, px + r, py + r), fill=fill)
        s.text((px, py), str(v), size=18, color="node_t", bold=True, anchor="mm")
        if sizes and p[v] == v and sizes[v] > 1:
            s.text((px + r + 4, py - r), f"tam {sizes[v]}", size=14, color="muted", anchor="la")
    return pos


def wgraph(s, pos, edges, es=None, ns=None, r=22, order=False, lsize=18):
    """Grafo valorado: edges = [(a, b, valor)]; es = {(a,b): (color, grosor)}; ns = {v: (relleno, texto, aro)}."""
    es, ns = es or {}, ns or {}
    for a, b, wv in edges:
        col, g = es.get((a, b)) or es.get((b, a)) or ("dim", 3)
        s.d.line((pos[a], pos[b]), fill=C.get(col, col), width=g)
    for a, b, wv in edges:
        col, g = es.get((a, b)) or es.get((b, a)) or ("dim", 3)
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        tw = s.d.textlength(str(wv), font=__import__("vidlib").font(lsize - 2, True))
        s.d.rounded_rectangle((mx - tw / 2 - 6, my - 12, mx + tw / 2 + 6, my + 12), 9, fill=C["panel"],
                              outline=C.get(col, col), width=2)
        s.text((mx, my), str(wv), size=lsize - 2, color="gold" if col in ("dim", "muted") else col, bold=True, anchor="mm")
    for v, (x, y) in pos.items():
        fill, tcol, ring = ns.get(v, ("node", "node_t", None))
        if ring:
            s.d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), outline=C.get(ring, ring), width=4)
        s.d.ellipse((x - r, y - r, x + r, y + r), fill=C.get(fill, fill))
        s.text((x, y), str(v), size=lsize, color=tcol, bold=True, anchor="mm")


def limpia(lineas):
    """Quita líneas en blanco y de comentario para que el código quepa con letra legible."""
    return [(n, s) for n, s in lineas if s.strip() and not s.strip().startswith(("//", "/*", "*"))]


def tabla(s, x, y, cols, filas, cw, rh=38, size=19, head="gold"):
    """Tabla sencilla: cols = cabeceras, filas = lista de listas, cw = anchos."""
    xx = x
    for c, w_ in zip(cols, cw):
        s.text((xx + 10, y + 6), c, size=size - 1, color=head, bold=True)
        xx += w_
    s.d.line((x, y + rh - 2, x + sum(cw), y + rh - 2), fill=C["border"], width=2)
    for k, fila in enumerate(filas):
        yy = y + rh + k * rh
        xx = x
        for j, (c, w_) in enumerate(zip(fila, cw)):
            col = "text"
            if isinstance(c, tuple):
                c, col = c
            s.text((xx + 10, yy + 5), c, size=size, color=col, bold=(j == 0))
            xx += w_
        s.d.line((x, yy + rh - 2, x + sum(cw), yy + rh - 2), fill=(30, 50, 90), width=1)


def comp_text(uf):
    g = {}
    for v in range(uf.n):
        g.setdefault(uf.raiz(v), []).append(v)
    return "   ".join("{" + ",".join(map(str, sorted(m))) + "}" for m in sorted(g.values(), key=lambda m: m[0]))


# ---------------------------------------------------------------------------
# grafo de demostración para Kruskal y Prim (6 vértices, valores distintos)
# ---------------------------------------------------------------------------
GE = [(4, 5, 2), (0, 2, 3), (3, 4, 4), (1, 3, 5), (3, 5, 6), (2, 3, 7), (0, 1, 8), (2, 4, 9), (1, 2, 10)]
GP = {0: (110, 150), 1: (110, 330), 2: (290, 90), 3: (300, 260), 4: (480, 160), 5: (500, 350)}
GOF = (30, 100)       # desplazamiento del dibujo dentro de la diapositiva


def gpos(dx=0, dy=0, k=1.0):
    return {v: (x * k + dx, y * k + dy) for v, (x, y) in GP.items()}


def sim_kruskal():
    uf = UF(6, "qu")
    ev, tot, acc = [], 0, 0
    for k, (a, b, w) in enumerate(sorted(GE, key=lambda e: e[2])):
        if acc == 5:
            ev.append(("para", k, (a, b, w), comp_text(uf), tot, acc))
            break
        if uf.raiz(a) != uf.raiz(b):
            uf.unir(a, b)
            tot += w
            acc += 1
            ev.append(("acepta", k, (a, b, w), comp_text(uf), tot, acc))
        else:
            ev.append(("rechaza", k, (a, b, w), comp_text(uf), tot, acc))
    return ev


def sim_prim():
    dentro, ev, tot = {0}, [], 0
    while len(dentro) < 6:
        front = sorted([e for e in GE if (e[0] in dentro) != (e[1] in dentro)], key=lambda e: e[2])
        e = front[0]
        nuevo = e[1] if e[0] in dentro else e[0]
        tot += e[2]
        ev.append((sorted(dentro), front, e, nuevo, tot))
        dentro.add(nuevo)
    return ev


def sim_petroleros():
    """Ejemplo 2 del 06-1: 3×4 vacío; celdas (2,2), (3,4), (2,3)."""
    F, Cc = 3, 4
    pasos = [(2, 2), (3, 4), (2, 3)]
    negro = set()
    res = [(set(), [0] * 12, 0)]
    for (f, c) in pasos:
        negro.add((f - 1, c - 1))
        uf = UF(F * Cc, "sz")
        for (i, j) in negro:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if (di or dj) and (i + di, j + dj) in negro:
                        uf.unir(i * Cc + j, (i + di) * Cc + j + dj)
        mayor = max(uf.t[uf.raiz(i * Cc + j)] for (i, j) in negro)
        res.append((set(negro), [uf.raiz(i * Cc + j) if (i, j) in negro else -1 for i in range(F) for j in range(Cc)], mayor))
    return pasos, res


EJ1 = ["-#-#---#", "-###--##", "-----###", "-#------", "-#-#----", "-###-##-", "###--##-", "--#-----"]


def manchas(bm):
    F, Cc = len(bm), len(bm[0])
    uf = UF(F * Cc, "sz")
    for i in range(F):
        for j in range(Cc):
            if bm[i][j] == "#":
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        a, b = i + di, j + dj
                        if (di or dj) and 0 <= a < F and 0 <= b < Cc and bm[a][b] == "#":
                            uf.unir(i * Cc + j, a * Cc + b)
    cols, tam = {}, {}
    for i in range(F):
        for j in range(Cc):
            if bm[i][j] == "#":
                rt = uf.raiz(i * Cc + j)
                if rt not in cols:
                    cols[rt] = PAL[len(cols) % len(PAL)]
                tam[rt] = uf.t[rt]
    fills = {(i, j): cols[uf.raiz(i * Cc + j)] for i in range(F) for j in range(Cc) if bm[i][j] == "#"}
    return fills, max(tam.values()) if tam else 0


# ---------------------------------------------------------------------------
def main(preview=False):
    segs, cap = [], {}

    def add(sl, nar, dmin=0, cap_title=None):
        if cap_title:
            cap[len(segs)] = cap_title
        segs.append((sl, nar, dmin))

    # ------------------------------------------------------------------ 0 · portada y plan
    add(portada("Conjuntos disjuntos y grafos valorados", "TEMA 6", "Árbol de recubrimiento de coste mínimo · Kruskal y Prim"),
        "Tema seis. Conjuntos disjuntos, grafos valorados y árboles de recubrimiento de coste mínimo. "
        "En este vídeo vemos cómo funciona todo, paso a paso, y cómo se aplica a los cinco ejercicios de la semana.",
        cap_title="Introducción")
    s = Slide("Plan del vídeo", TEMA)
    s.bullets(70, 120, W - 140, [
        ("1 · Conjuntos disjuntos: búsqueda rápida, unión rápida, por tamaños y compresión de caminos.", "text"),
        ("2 · Ejercicio 06-1: Petroleros hundidos.", "gold"),
        ("3 · Grafos valorados: Arista y GrafoValorado.", "text"),
        ("4 · Ejercicio 06-2: Camiones de reparto.", "gold"),
        ("5 · Árbol de recubrimiento de coste mínimo: propiedad del corte, Kruskal y Prim.", "text"),
        ("6 · Ejercicios 06-3, 06-4 y 06-5: el mismo Kruskal con tres preguntas distintas.", "gold"),
    ], size=24, gap=22)
    add(s, "Empezamos con los conjuntos disjuntos y el primer ejercicio. Después, los grafos valorados y el segundo ejercicio. "
           "Por último, los árboles de recubrimiento mínimo con Kruskal y Prim, que resuelven los tres ejercicios restantes.")

    # ------------------------------------------------------------------ 1 · relación de equivalencia dinámica
    rels = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1)]
    for k in range(len(rels) + 1):
        s = Slide("Relaciones de equivalencia dinámicas", "conjuntos disjuntos")
        uf = UF(10, "qu")
        for a, b in rels[:k]:
            uf.unir(a, b)
        colores = {}
        for v in range(10):
            rt = uf.raiz(v)
            colores.setdefault(rt, PAL[len(colores) % len(PAL)])
        posn = {v: (560 + (v % 5) * 120, 200 + (v // 5) * 170) for v in range(10)}
        s.box(520, 100, 700, 420, "los elementos 0 … 9")
        for a, b in rels[:k]:
            s.d.line((posn[a], posn[b]), fill=C["gold"], width=4)
        for v, (x, y) in posn.items():
            s.d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=colores[uf.raiz(v)])
            s.text((x, y), str(v), size=22, color="node_t", bold=True, anchor="mm")
        s.box(40, 100, 440, 420, "relaciones que van apareciendo")
        for i, (a, b) in enumerate(rels[:k]):
            s.text((70, 150 + i * 48), f"{a} R {b}", size=26, color="gold", bold=True)
        s.caption("Dos elementos relacionados quedan en el mismo conjunto: una partición que va cambiando." if k == 0 else
                  f"Conjuntos ahora: {comp_text(uf)}", y=600)
        nar = {0: "Muchos problemas necesitan una relación de equivalencia: reflexiva, simétrica y transitiva. "
                  "Una relación así reparte los elementos en conjuntos disjuntos, una partición. Aquí empezamos con diez elementos, cada uno solo.",
               1: "La relación es dinámica: van apareciendo nuevos pares. Cuatro relacionado con tres, y ya forman un conjunto.",
               2: "Tres con ocho. Por transitividad, cuatro, tres y ocho quedan juntos.",
               3: "Seis con cinco.", 4: "Nueve con cuatro: el conjunto crece.", 5: "Y dos con uno."}[k]
        add(s, nar)

    s = Slide("El TAD de los conjuntos disjuntos", "conjuntos disjuntos")
    tabla(s, 70, 120, ["Operación", "Qué hace"], [
        ["ConjuntosDisjuntos(N)", "partición unitaria de 0 … N−1"],
        ["unir(a, b)", "fusiona los conjuntos de a y de b"],
        ["buscar(a)", "representante del conjunto de a"],
        ["unidos(a, b)", "¿están en el mismo conjunto?"],
        ["cardinal(a)", "tamaño del conjunto de a"],
        ["num_cjtos()", "cuántos conjuntos hay"],
    ], [380, 700], rh=50, size=23)
    s.caption("Solo se puede unir, nunca separar.", y=560)
    add(s, "El tipo abstracto tiene estas operaciones: crear la partición unitaria, unir dos conjuntos, buscar el representante de un elemento, "
           "preguntar si dos elementos están juntos, el cardinal de un conjunto y el número de conjuntos. "
           "Fíjate en que solo se puede unir, nunca separar. Eso es lo que lo hace tan eficiente.")

    # ------------------------------------------------------------------ 2 · búsqueda rápida
    for etapa, ids in enumerate([[0, 1, 1, 8, 8, 0, 0, 1, 8, 8], [1, 1, 1, 8, 8, 1, 1, 1, 8, 8]]):
        s = Slide("Búsqueda rápida: un vector id[ ]", "primera implementación")
        s.cells(60, 140, "id[ ]", ids, cw=84, size=26, colors={i: tuple(int(c * .45) for c in PAL[{0: 0, 1: 1, 8: 2}[ids[i]] if ids[i] in (0, 1, 8) else 3]) for i in range(10)})
        s.bullets(70, 270, W - 140, [
            "id[i] es el nombre del conjunto de i  ⇒  buscar y unidos son inmediatos: O(1).",
            ("Pero unir(6, 1) obliga a recorrer TODO el vector reetiquetando: O(N).", "red") if etapa else "Conjuntos: {0,5,6}  {1,2,7}  {3,4,8,9}.",
        ], size=24, gap=20)
        if etapa:
            s.caption("Todos los de id 0 pasan a tener id 1.  Con N uniones: coste N·M.", y=600)
        add(s, ["Primera idea: un vector id. El elemento i guarda el nombre de su conjunto. Preguntar si dos elementos están juntos es inmediato.",
                "Pero unir exige recorrer todo el vector reetiquetando. Con muchas uniones, el coste es de orden N por M."][etapa],
            cap_title="Búsqueda rápida" if etapa == 0 else None)

    # ------------------------------------------------------------------ 3 · unión rápida
    s = Slide("Unión rápida: un árbol por conjunto", "segunda implementación")
    s.box(40, 100, 1200, 300)
    uf = UF(10, "qu")
    for a, b in [(4, 3), (3, 8), (9, 4), (6, 5), (2, 1)]:
        uf.unir(a, b)
    forest(s, uf.p, 70, 150, 1130)
    s.cells(60, 440, "p[ ]", uf.p, cw=84, size=24)
    s.caption("p[i] es el padre de i. La raíz es su propio padre y representa al conjunto.", y=560)
    add(s, "Segunda idea: cada conjunto es un árbol. El vector p guarda el padre de cada elemento, y la raíz es su propio padre: "
           "ella representa al conjunto. Unir dos conjuntos es colgar una raíz de la otra, y eso cuesta tiempo constante.",
        cap_title="Unión rápida")

    for k in range(1, 5):
        uf = UF(5, "qu")
        for a in range(k):
            uf.unir(0, a + 1)
        s = Slide("Unión rápida: el peor caso", "segunda implementación")
        s.box(40, 100, 700, 420, f"unir(0,1) … unir(0,{k})")
        forest(s, uf.p, 90, 175, 560, dy=66)
        s.cells(780, 160, "p[ ]", uf.p, cw=56, size=22)
        if k == 4:
            s.bullets(780, 280, 440, ["Cada unir cuelga la raíz de 0 bajo la nueva: sale una CADENA.", ("Buscar el 0 cuesta O(N).", "red")], size=22)
            s.caption("Unir es rápido, pero buscar puede ser lento.", y=600)
        add(s, ["Pero hay un problema. Si unimos siempre cero con uno, luego cero con dos, y así sucesivamente...",
                "... el árbol se va alargando.", "... cada unión cuelga la raíz bajo un nuevo elemento...",
                "El resultado es una cadena. Unir es rápido, pero buscar el cero cuesta orden N: de nuevo, N por M en el peor caso."][k - 1])

    # ------------------------------------------------------------------ 4 · por tamaños y compresión
    s = ideas("Unión por tamaños", [
        "Guardamos el tamaño de cada árbol.",
        ("Al unir, el árbol PEQUEÑO pasa a ser hijo del GRANDE.", "gold"),
        "Un elemento solo cambia de profundidad al quedar en el árbol pequeño: cada vez, el árbol que lo contiene al menos se DUPLICA.",
        "Por eso la profundidad es como mucho log₂ N  ⇒  buscar y unir cuestan O(log N).",
    ], "conjuntos disjuntos")
    add(s, "La solución es unir por tamaños. Guardamos el tamaño de cada árbol, y al unir, el árbol pequeño pasa a ser hijo del grande. "
           "Así, un elemento solo baja de nivel cuando su árbol se une a otro al menos igual de grande, y su conjunto se duplica. "
           "Por eso la profundidad es como mucho logaritmo de N.", cap_title="Unión por tamaños")

    s = Slide("Unión por tamaños: cómo se decide", "conjuntos disjuntos")
    s.box(60, 110, 540, 300, "unir(a, b)  con raíces ra y rb")
    s.text((90, 160), "tam[ra] mayor que tam[rb]:", size=22, bold=True)
    s.text((90, 200), "rb cuelga de ra", size=24, color="gold")
    s.text((90, 270), "tam[ra] menor que tam[rb]:", size=22, bold=True)
    s.text((90, 310), "ra cuelga de rb", size=24, color="gold")
    s.box(640, 110, 580, 300, "¡y si empatan!")
    s.bullets(660, 160, 540, [
        "Las transparencias: en empate, rb cuelga de ra.",
        "La cabecera ConjuntosDisjuntos.h: en empate, ra cuelga de rb.",
        ("Los dos son correctos; solo cambian los árboles.", "muted"),
    ], size=21, gap=14)
    s.caption("Cuidado al comparar con las transparencias: el desempate cambia el resultado paso a paso.", y=470)
    add(s, "Si el árbol de a es mayor, el de b cuelga de él, y al revés. Cuando empatan hay que elegir un criterio, y aquí hay una pequeña diferencia: "
           "las transparencias cuelgan b de a, y la cabecera de la asignatura cuelga a de b. Los dos son correctos, pero los árboles que salen son distintos. "
           "En este vídeo seguimos el criterio de las transparencias.")

    s = Slide("Compresión de caminos", "conjuntos disjuntos")
    cad = [1, 2, 3, 4, 4]
    s.box(40, 100, 580, 360, "antes de buscar(0)")
    forest(s, cad, 120, 175, 420, dy=62)
    s.box(660, 100, 580, 360, "después: todos cuelgan de la raíz")
    forest(s, [4, 4, 4, 4, 4], 700, 175, 480, dy=62)
    s.caption("Al buscar la raíz de x, cada nodo del camino pasa a colgar directamente de la raíz.", y=500)
    s.caption("Con tamaños y compresión: M operaciones cuestan  O(N + M · lg* N)  ≈ casi constante por operación.", y=560)
    add(s, "Y hay una segunda mejora: la compresión de caminos. Después de buscar la raíz de un elemento, hacemos que todos los nodos del camino cuelguen directamente de la raíz. "
           "Así, las siguientes búsquedas son casi inmediatas. Con las dos mejoras juntas, M operaciones cuestan N más M por logaritmo iterado de N, "
           "que en la práctica es constante.", cap_title="Compresión de caminos y costes")

    s = Slide("Resumen de costes", "M operaciones sobre N elementos")
    tabla(s, 100, 120, ["Implementación", "Caso peor"], [
        ["búsqueda rápida", ("N · M", "red")],
        ["unión rápida", ("N · M", "red")],
        ["unión rápida por tamaños", "N + M log N"],
        ["unión rápida con compresión", "N + M log N"],
        ["tamaños + compresión de caminos", ("N + M lg* N", "green")],
    ], [640, 400], rh=56, size=26)
    s.caption("lg* N es menor que 6 para cualquier N razonable.", y=520)
    add(s, "Resumen de costes. Búsqueda rápida y unión rápida a secas son de orden N por M. Por tamaños, o con compresión, N más M por log N. "
           "Y con las dos a la vez, N más M por logaritmo iterado, casi lineal. Es lo que implementa la cabecera de la asignatura.")

    lb = find_line(CD, "int buscar")
    lu = find_line(CD, "void unir")
    ln = find_line(CD, "int num_cjtos")
    partes = [
        ("constructor y buscar", find_line(CD, "protected:"), find_line(CD, "// unir los conjuntos") - 1,
         {lb, find_line(CD, "return p[a] = buscar(p[a])")},
         ["tam guarda el tamaño de cada árbol; p[i] = i: partición unitaria.", "buscar es recursivo.",
          ("p[a] = buscar(p[a]) comprime el camino: cada nodo pasa a colgar de la raíz.", "gold")],
         "Así queda en C más más. El constructor crea la partición unitaria: cada elemento es su propio padre, con tamaño uno. "
         "Buscar es recursivo, y al volver, p de a se actualiza con la raíz: esa es la compresión de caminos."),
        ("unir, unidos y cardinal", lu, ln,
         {find_line(CD, "if (tam[i] > tam[j])")},
         ["unir busca las dos raíces.", "Cuelga la de menor tamaño de la de mayor y suma los tamaños.", "ncjtos baja en uno con cada unión efectiva.",
          ("unidos y cardinal se apoyan en buscar.", "muted")],
         "Unir busca las dos raíces. Si ya son la misma, no hace nada. Si no, cuelga la de menor tamaño de la de mayor, suma los tamaños, y baja el número de conjuntos. "
         "Unidos y cardinal se apoyan en buscar."),
    ]
    for (sub, a_, b_, hl_, bl, nar) in partes:
        s = Slide("ConjuntosDisjuntos.h", sub)
        s.code(24, 84, 760, 530, limpia(code_lines(CD, a_, b_, maxc=62)), hl=hl_, title="ConjuntosDisjuntos.h", size=20)
        s.box(804, 84, 452, 530, "qué hay que fijarse")
        s.bullets(824, 130, 410, bl, size=21, gap=16)
        add(s, nar)

    # ------------------------------------------------------------------ 5 · autoevaluación
    s = Slide("Autoevaluación 6.1", "uniones: 9-0  3-4  5-8  7-2  2-1  5-7  0-3  4-2")
    uf = UF(10, "qf")
    filas = [["inicial"] + [str(x) for x in uf.id]]
    for a, b in PARES:
        uf.unir(a, b)
        filas.append([f"unir({a},{b})"] + [str(x) for x in uf.id])
    tabla(s, 40, 96, ["búsqueda rápida"] + [str(i) for i in range(10)], filas, [240] + [96] * 10, rh=44, size=21)
    add(s, "Ahora el ejercicio de autoevaluación. Partimos de diez elementos y hacemos estas ocho uniones. "
           "Con búsqueda rápida, cada unión cambia en el vector los identificadores del conjunto del primer elemento por el del segundo. "
           "Al final solo quedan dos conjuntos: el seis solo, y todos los demás.", cap_title="Autoevaluación 6.1")

    s = Slide("Autoevaluación 6.1 · unión rápida", "la raíz de a pasa a ser hija de la raíz de b")
    uf = UF(10, "qu")
    filas = [["inicial"] + [str(x) for x in uf.p]]
    for a, b in PARES:
        uf.unir(a, b)
        filas.append([f"unir({a},{b})"] + [str(x) for x in uf.p])
    tabla(s, 40, 96, ["unión rápida"] + [str(i) for i in range(10)], filas, [240] + [96] * 10, rh=44, size=21)
    add(s, "Con unión rápida, el vector p cambia solo en la raíz que se cuelga. Por ejemplo, al unir cinco con siete, la raíz de cinco es ocho, "
           "la de siete es uno, y ocho pasa a colgar de uno.")
    s = Slide("Autoevaluación 6.1 · los árboles", "unión rápida: árbol final")
    s.box(40, 100, 1200, 420)
    forest(s, uf.p, 80, 150, 1100, dy=82, r=24)
    s.caption("Altura máxima 3. Con otro orden de uniones podría ser una cadena de N nodos.", y=560)
    add(s, "Y estos son los árboles finales. El mayor tiene como raíz el uno, con altura tres. El seis sigue solo.")

    uf = UF(10, "sz")
    snaps = []
    for a, b in PARES:
        uf.unir(a, b)
        snaps.append((a, b, list(uf.p), list(uf.t)))
    for k, (a, b, p, t) in enumerate(snaps):
        s = Slide(f"Autoevaluación 6.1 · por tamaños · unir({a},{b})", f"paso {k + 1} de 8")
        s.box(40, 100, 1200, 380)
        forest(s, p, 70, 140, 1140, sizes=t, dy=76, r=22)
        s.cells(60, 520, "p[ ]", p, cw=76, size=22)
        nota = {0: "tamaños 1 y 1: empate → 0 cuelga de 9 (criterio de las transparencias).",
                1: "empate 1 y 1 → 4 cuelga de 3.", 2: "empate → 8 cuelga de 5.", 3: "empate → 2 cuelga de 7.",
                4: "raíz de 2 es 7 (tamaño 2) contra raíz de 1 (tamaño 1) → 1 cuelga de 7.",
                5: "raíz de 5 (tamaño 2) contra raíz de 7 (tamaño 3) → el pequeño cuelga del grande.",
                6: "raíces 9 y 3, ambas de tamaño 2: empate → 3 cuelga de 9.",
                7: "raíz 9 (tamaño 4) contra raíz 7 (tamaño 5) → 9 cuelga de 7. Un árbol de 9 elementos."}[k]
        s.caption(nota, y=600)
        add(s, ["Con unión por tamaños. Primero, nueve con cero: empate, y cero cuelga de nueve.",
                "Tres con cuatro: empate, y cuatro cuelga de tres.", "Cinco con ocho, igual.", "Siete con dos, igual.",
                "Dos con uno: la raíz de dos es siete, con tamaño dos, y la de uno solo tiene tamaño uno. Uno cuelga de siete.",
                "Cinco con siete: el árbol de cinco tiene tamaño dos, y el de siete, tres. El pequeño cuelga del grande.",
                "Cero con tres. Las raíces son nueve y tres, las dos con tamaño dos. Empate, y tres cuelga de nueve.",
                "Por último, cuatro con dos. La raíz nueve tiene tamaño cuatro, y la siete, cinco. Nueve cuelga de siete. "
                "Resultado: un árbol de nueve elementos con altura tres, el máximo que permite un logaritmo."][k])

    # ------------------------------------------------------------------ 6 · 06-1 Petroleros
    s = ideas("Ejercicio 06-1 · Petroleros hundidos", [
        "Rejilla F × C: «-» mar, «#» petróleo. Mancha = celdas negras conectadas en 8 direcciones.",
        "Se van añadiendo celdas negras una a una.",
        ("Hay que escribir el tamaño de la mancha mayor al principio y tras cada celda nueva.", "gold"),
    ], "EJ 06-1")
    add(s, "Ejercicio seis uno, petroleros hundidos. Tenemos una rejilla con mar y petróleo. Una mancha son las celdas de petróleo conectadas en ocho direcciones. "
           "Se van añadiendo celdas de petróleo una a una, y tenemos que escribir el tamaño de la mancha mayor al principio y tras cada celda nueva.",
        cap_title="Ejercicio 06-1 · Petroleros hundidos")

    s = Slide("¿Y con lo que ya sabemos?", "EJ 06-1")
    s.box(40, 100, 600, 420, "solución del tema 4, en cada imagen")
    s.bullets(60, 150, 560, ["Un DFS de toda la rejilla tras cada celda nueva.", "Coste: O(F·C) por imagen.", ("N + 1 imágenes  ⇒  O((N+1)·F·C)", "red"), "F·C = 10⁶ y N = 10⁵:  ≈ 10¹¹ operaciones."], size=21, gap=16)
    s.box(660, 100, 580, 420, "con conjuntos disjuntos")
    s.bullets(680, 150, 540, ["Las celdas solo SE AÑADEN: las manchas crecen o se funden, nunca se parten.", ("Eso es exactamente unir conjuntos.", "gold"),
                              "Cada celda nueva: ≤ 8 uniones y 1 cardinal.", ("Total O(F·C + N)", "green")], size=21, gap=16)
    add(s, "Con la solución del tema cuatro tendríamos que repetir un recorrido de toda la rejilla tras cada celda nueva: orden de N por F por C, unos cien mil millones de operaciones. "
           "Pero fíjate: las celdas solo se añaden. Las manchas crecen o se funden, pero nunca se parten. Eso es exactamente unir conjuntos. "
           "Cada celda nueva cuesta como mucho ocho uniones, y el total es lineal.")

    s = Slide("Modelo", "EJ 06-1")
    tabla(s, 60, 120, ["Idea", "En el problema"], [
        ["Elemento", "cada celda (i, j)  →  número  i·C + j"],
        ["Conjunto", "una mancha"],
        ["unir(a, b)", "dos celdas negras vecinas (8 direcciones)"],
        ["cardinal(a)", "tamaño de la mancha de a"],
    ], [300, 820], rh=56, size=24)
    s.bullets(70, 400, W - 140, ["Imagen inicial: unir cada celda negra con sus vecinas negras y quedarse con el mayor cardinal.",
                                 "Cada celda nueva: marcarla, unir con sus vecinas negras y  mayor = max(mayor, cardinal(celda))."], size=22, gap=16)
    add(s, "Cada celda es un elemento, con el número i por C más j. Un conjunto es una mancha. Dos celdas negras vecinas se unen, y el cardinal es el tamaño de la mancha. "
           "Procesamos la imagen inicial una vez, y por cada celda nueva la marcamos, la unimos con sus vecinas negras, y actualizamos el máximo con su cardinal. "
           "No hace falta recalcular el máximo: solo ha podido cambiar la mancha de la celda nueva, y el máximo nunca baja.")

    fills, mayor = manchas(EJ1)
    s = Slide("Ejemplo 1 · imagen inicial", "EJ 06-1")
    s.grid(80, 110, EJ1, 62, fills=fills)
    s.box(640, 110, 600, 340, "manchas")
    s.bullets(660, 160, 560, ["Cada color es un conjunto distinto.", ("La mayor tiene 10 celdas (amarilla).", "gold"), "Salida inicial: 10"], size=22, gap=16)
    add(s, "En el primer ejemplo, la imagen inicial tiene varias manchas, cada una de un color. La mayor tiene diez celdas, así que empezamos escribiendo diez.")
    nuevas = [(6, 8), (2, 5), (6, 5)]
    bm2 = [list(r) for r in EJ1]
    for (f, c) in nuevas:
        bm2[f - 1][c - 1] = "#"
    bm2 = ["".join(r) for r in bm2]
    fills2, mayor2 = manchas(bm2)
    s = Slide("Ejemplo 1 · tras añadir (6,8), (2,5) y (6,5)", "EJ 06-1")
    s.grid(80, 110, bm2, 62, fills=fills2, rings=[(f - 1, c - 1) for f, c in nuevas])
    s.box(640, 110, 600, 340, "salida")
    s.text((670, 170), "10   10   12   16", size=44, color="gold", bold=True)
    s.bullets(660, 250, 560, ["Las celdas nuevas llevan marco rojo.", "Las dos primeras no cambian el máximo.", "La tercera funde varias manchas de golpe: 16."], size=21, gap=14)
    add(s, "Añadimos las tres celdas nuevas. Las dos primeras no cambian el máximo, pero la tercera funde varias manchas de golpe y el máximo pasa a dieciséis. "
           "La salida es diez, diez, doce, dieciséis.")

    pasos, res = sim_petroleros()
    for k, (negros, ids, mayor_k) in enumerate(res):
        s = Slide("Ejemplo 2 · rejilla 3 × 4 vacía", f"paso {k} de 3" if k else "inicio")
        bm = ["".join("#" if (i, j) in negros else "-" for j in range(4)) for i in range(3)]
        fl, _ = manchas(bm)
        s.grid(90, 120, bm, 88, fills=fl, labels={(i, j): i * 4 + j for i in range(3) for j in range(4)}, lsize=17, esquina=True)
        s.box(520, 110, 720, 300, "estado")
        s.text((550, 150), f"mayor = {mayor_k}", size=40, color="gold", bold=True)
        if k:
            f, c = pasos[k - 1]
            s.text((550, 220), f"celda nueva ({f},{c})  →  número {(f - 1) * 4 + c - 1}", size=24)
            vec = [(i, j) for i in range(3) for j in range(4) if (i, j) in negros and (i, j) != (f - 1, c - 1)
                   and abs(i - (f - 1)) <= 1 and abs(j - (c - 1)) <= 1]
            s.text((550, 270), "vecinas negras: " + (", ".join(str(i * 4 + j) for i, j in vec) if vec else "ninguna"), size=22, color="muted")
        s.caption("Salida acumulada: " + " ".join(str(r[2]) for r in res[:k + 1]), y=600)
        add(s, ["Segundo ejemplo: una rejilla de tres por cuatro, sin petróleo. El máximo vale cero.",
                "Aparece la celda dos, dos, el número cinco. No tiene vecinas negras: mancha de una celda.",
                "Después la tres, cuatro, el número once. Tampoco toca a la anterior: otra mancha de una celda.",
                "Y por último la dos, tres, el número seis. Toca al cinco en horizontal y al once en diagonal: las tres celdas quedan unidas. Máximo tres."][k])

    # ------------------------------------------------------------------ 7 · Grafos valorados
    s = Slide("Grafos valorados", "aristas con un valor")
    gv = {0: (160, 150), 1: (330, 340), 2: (350, 130), 3: (560, 300), 4: (720, 150)}
    gve = [(0, 2, 10), (0, 1, 20), (2, 1, 30), (1, 3, 40), (3, 4, 50), (2, 4, 60)]
    s.box(40, 100, 800, 400, "ejemplo")
    wgraph(s, {v: (x + 20, y + 20) for v, (x, y) in gv.items()}, gve, r=26, lsize=22)
    s.bullets(870, 120, 380, ["Cada arista lleva un valor: distancia, tiempo, tarifa, anchura…", ("Sin dirección en esta semana.", "gold"), "La semana siguiente: dirigidos."], size=21, gap=16)
    add(s, "Un grafo valorado es un grafo cuyas aristas llevan un valor asociado. Puede ser una distancia, un tiempo, una tarifa o una anchura. "
           "Esta semana trabajamos con grafos no dirigidos, y la semana que viene veremos los dirigidos.", cap_title="Grafos valorados")

    s = Slide("Arista y GrafoValorado", "GrafoValorado.h")
    la = find_line(GV, "class Arista")
    s.code(24, 84, 600, 300, limpia(code_lines(GV, find_line(GV, "Arista(int v, int w, Valor valor)"), find_line(GV, "bool operator>"), maxc=56,
                                         skip=[(find_line(GV, "//Método para depurar"), find_line(GV, "bool operator<") - 2)])),
           title="Arista<Valor>")
    s.code(644, 84, 612, 300, limpia(code_lines(GV, find_line(GV, "void ponArista"), find_line(GV, "std::vector<Arista<Valor>> aristas()") + 7, maxc=56)),
           title="GrafoValorado<Valor>")
    s.box(24, 404, 1232, 200, "cómo se usa")
    s.text((50, 450), "for (auto a : g.ady(v)) { int w = a.otro(v);  … a.valor() … }", size=24, color="gold", mono=True)
    s.bullets(50, 500, 1180, ["La arista es un objeto compartido: las dos listas de adyacencia apuntan a la misma.", "aristas() devuelve cada arista UNA sola vez; a < b compara por valor."], size=20, gap=10)
    add(s, "La arista guarda sus dos extremos y su valor. Uno devuelve un extremo, otro devuelve el contrario de un vértice dado, y valor devuelve el valor. "
           "Se comparan por valor. El grafo guarda las listas de adyacencia, y al poner una arista, la añade a las listas de sus dos extremos, pero es un único objeto compartido. "
           "Para recorrer los adyacentes de v, usamos ady, y el otro extremo con otro. El método aristas devuelve cada arista una sola vez.")

    s = Slide("Listas de adyacencia", "GrafoValorado.h")
    s.box(40, 100, 560, 400)
    wgraph(s, {0: (110, 190), 1: (200, 400), 2: (330, 160), 3: (440, 330), 4: (540, 190)}, gve, r=24, lsize=20)
    s.box(630, 100, 610, 400, "ady(v)")
    ady = {v: [] for v in range(5)}
    for a, b, wv in gve:
        ady[a].append((b, wv))
        ady[b].append((a, wv))
    for v in range(5):
        s.text((660, 150 + v * 62), f"{v}:", size=26, color="gold", bold=True)
        x = 710
        for (w_, wv) in ady[v]:
            x = s.pill(x, 144 + v * 62, f"→{w_} ({wv})", fill="blue_d", color="text", size=19) + 8
    add(s, "Así quedan las listas de adyacencia: para cada vértice, sus aristas con el otro extremo y el valor. La arista del cero al dos aparece en la lista del cero y en la del dos.")

    # ------------------------------------------------------------------ 8 · 06-2 Camiones
    s = ideas("Ejercicio 06-2 · Camiones de reparto", [
        "Ciudad con V intersecciones y E calles de doble sentido, cada una con una anchura máxima.",
        "K consultas: origen, destino y anchura de un camión.",
        ("¿Puede ir del origen al destino usando solo calles por las que cabe?  SI / NO.", "gold"),
    ], "EJ 06-2")
    add(s, "Ejercicio seis dos, camiones de reparto. Una ciudad con calles de doble sentido, cada una con una anchura máxima. "
           "Para cada consulta, un camión de cierta anchura: ¿puede ir del origen al destino usando solo calles por las que cabe?",
        cap_title="Ejercicio 06-2 · Camiones de reparto")
    CE = [(1, 2, 10), (1, 3, 30), (2, 4, 20), (3, 4, 15), (4, 5, 12)]
    CP = {1: (110, 270), 2: (260, 130), 3: (260, 400), 4: (450, 270), 5: (620, 270)}
    consultas = [(1, 5, 8, "SI"), (1, 4, 15, "SI"), (2, 5, 15, "NO")]
    for q, (o, d, anch, resp) in enumerate(consultas):
        s = Slide(f"Consulta {o} → {d}, camión de anchura {anch}", "EJ 06-2")
        ok = {(a, b): anch <= wv for a, b, wv in CE}
        # alcanzables
        vis, pila = {o}, [o]
        while pila:
            u = pila.pop()
            for a, b, wv in CE:
                if wv >= anch and u in (a, b):
                    w_ = b if u == a else a
                    if w_ not in vis:
                        vis.add(w_)
                        pila.append(w_)
        s.box(30, 100, 740, 440, "calles: anchura máxima (rojo: no cabe)")
        es = {(a, b): ("green", 5) if ok[(a, b)] else ("red", 3) for a, b, wv in CE}
        ns = {v: (("green" if v in vis else "node"), "node_t", ("gold" if v in (o, d) else None)) for v in CP}
        wgraph(s, {v: (x + 20, y + 40) for v, (x, y) in CP.items()}, CE, es=es, ns=ns, r=24, lsize=22)
        s.box(790, 100, 450, 440, "recorrido")
        s.bullets(810, 150, 410, ["Desde el origen, el DFS solo cruza calles con valor ≥ anchura del camión.", ("a.valor() >= ancho", "gold"),
                                   f"Alcanza: {', '.join(map(str, sorted(vis)))}", (f"El {d} " + ("SÍ" if resp == "SI" else "NO") + " está  ⇒  " + resp, "green" if resp == "SI" else "red")], size=20, gap=14)
        s.caption("Se repite para cada consulta (K ≤ 10): O(K·(V+E)).", y=590)
        add(s, [f"Primera consulta: del uno al cinco con un camión de anchura ocho. Todas las calles valen: se alcanza el cinco. Sí.",
                "Segunda: del uno al cuatro con anchura quince. La calle del uno al dos, de diez, no cabe, pero por el tres sí: uno, tres, cuatro. La calle de quince admite justo quince, porque la comparación es mayor o igual. Sí.",
                "Tercera: del dos al cinco con quince. La única calle que llega al cinco admite doce, y no cabe. No."][q])

    # ------------------------------------------------------------------ 9 · ARM
    s = Slide("Árbol de recubrimiento", "grafo no dirigido conexo")
    s.box(30, 100, 400, 420, "es un árbol de recubrimiento")
    t1 = [(4, 5, 2), (0, 2, 3), (3, 4, 4), (1, 3, 5), (2, 3, 7)]
    wgraph(s, gpos(40, 120, 0.68), GE, es={(a, b): ("gold", 5) for a, b, _ in t1}, r=16, lsize=14)
    s.box(450, 100, 400, 420, "no es árbol (ciclo)")
    cyc = [(0, 2, 3), (2, 3, 7), (1, 3, 5), (0, 1, 8), (4, 5, 2)]
    wgraph(s, gpos(470, 120, 0.68), GE, es={(a, b): ("red", 5) for a, b, _ in cyc}, r=16, lsize=14)
    s.box(870, 100, 380, 420, "no es de recubrimiento")
    t3 = [(4, 5, 2), (0, 2, 3), (3, 4, 4)]
    wgraph(s, gpos(890, 120, 0.68), GE, es={(a, b): ("blue", 5) for a, b, _ in t3}, r=16, lsize=14)
    s.caption("Con V vértices, un árbol de recubrimiento tiene exactamente V − 1 aristas.", y=570)
    add(s, "Un árbol de recubrimiento de un grafo conexo es un subgrafo que conecta todos los vértices y no tiene ciclos. "
           "A la izquierda lo es. En el centro hay un ciclo, y a la derecha no llega a todos los vértices. "
           "Con V vértices, un árbol de recubrimiento tiene exactamente V menos uno aristas.", cap_title="Árbol de recubrimiento de coste mínimo")

    s = Slide("Árbol de recubrimiento de coste mínimo (ARM)", "sumando los valores de las aristas")
    s.box(40, 100, 700, 440, f"coste = 2 + 3 + 4 + 5 + 7 = 21")
    wgraph(s, gpos(110, 60), GE, es={(a, b): ("green", 6) for a, b, _ in t1}, r=24, lsize=20)
    s.bullets(770, 120, 470, ["De todos los árboles de recubrimiento, el de menor suma.", ("Aplicaciones: diseñar redes de carreteras, eléctricas, de datos…", "muted"),
                              "Dos simplificaciones: grafo conexo (existe ARM) y valores distintos (ARM único)."], size=21, gap=16)
    add(s, "El árbol de recubrimiento de coste mínimo es el de menor suma de valores. En este grafo cuesta veintiuno. "
           "Sirve para diseñar redes de carreteras, eléctricas o de datos. Para empezar suponemos que el grafo es conexo, y que los valores son todos distintos, de modo que el árbol es único.")

    s = Slide("La propiedad del corte", "por qué funcionan Kruskal y Prim")
    s.box(30, 100, 760, 440, "un corte reparte los vértices en dos conjuntos")
    P = gpos(40, 75)
    S = {0, 2}
    ns = {v: (("blue_d" if v in S else "purple_d"), "text", ("blue" if v in S else "purple")) for v in range(6)}
    es = {(a, b): (("gold", 7) if (a, b, w_) == (2, 3, 7) else ("red", 4)) for a, b, w_ in GE if (a in S) != (b in S)}
    wgraph(s, P, GE, es=es, ns=ns, r=22, lsize=20)
    s.box(810, 100, 430, 440, "propiedad del corte")
    s.bullets(830, 150, 390, ["Corte: {0, 2}  contra  {1, 3, 4, 5}.", "Aristas que lo cruzan en rojo.", ("La de menor valor (2-3, valor 7) pertenece al ARM.", "gold")], size=21, gap=18)
    add(s, "Un corte reparte los vértices en dos conjuntos. Las aristas que lo cruzan están en rojo. La propiedad del corte dice que la arista de menor valor que cruza un corte cualquiera pertenece al árbol de recubrimiento mínimo. "
           "En el ejemplo, la de valor siete, que va del dos al tres. Todo Kruskal y Prim se basa en esta idea.")

    # ------------------------------------------------------------------ 10 · Kruskal
    s = ideas("Algoritmo de Kruskal", [
        "1 · Ordenar las aristas por valor creciente.",
        "2 · Partición unitaria de los vértices (conjuntos disjuntos).",
        "3 · Para cada arista (v, w), en ese orden:",
        ("      si v y w están en conjuntos distintos  ⇒  se acepta y se unen,", "green"),
        ("      si ya están unidos  ⇒  cerraría un ciclo: se descarta.", "red"),
        "4 · Parar al aceptar V − 1 aristas.",
    ], "ARM")
    add(s, "El algoritmo de Kruskal: ordenamos las aristas de menor a mayor valor y creamos una partición unitaria de los vértices. "
           "Por cada arista, si sus extremos están en conjuntos distintos, la aceptamos y los unimos. Si ya estaban unidos, cerraría un ciclo y la descartamos. "
           "Paramos al aceptar V menos uno aristas. Los conjuntos disjuntos nos dan la detección de ciclos casi gratis.", cap_title="Algoritmo de Kruskal")

    ev = sim_kruskal()
    ordenadas = sorted(GE, key=lambda e: e[2])
    for (tipo, k, (a, b, w_), comps, tot, acc) in ev:
        s = Slide(f"Kruskal · arista {a}-{b} (valor {w_})", f"{acc} aristas aceptadas")
        s.box(24, 84, 640, 420, "grafo")
        es = {}
        for j, (x_, y_, wv) in enumerate(ordenadas):
            if j < k:
                est = [e for e in ev if e[1] == j][0][0]
                es[(x_, y_)] = ("green", 6) if est == "acepta" else ("red", 2)
        es[(a, b)] = ("gold", 8) if tipo != "rechaza" else ("red", 8)
        wgraph(s, gpos(40, 70), GE, es=es, r=22, lsize=19)
        s.box(684, 84, 572, 420, "aristas ordenadas")
        for j, (x_, y_, wv) in enumerate(ordenadas):
            col, fl = "muted", "panel"
            if j < k:
                est = [e for e in ev if e[1] == j][0][0]
                col, fl = ("green", "green_d") if est == "acepta" else ("red", "red_d")
            if j == k:
                col, fl = "gold", "gold_d"
            xx, yy = 710 + (j % 3) * 180, 130 + (j // 3) * 90
            s.d.rounded_rectangle((xx, yy, xx + 165, yy + 66), 12, fill=C[fl], outline=C[col], width=3)
            s.text((xx + 82, yy + 20), f"{x_}-{y_}", size=22, color="text", bold=True, anchor="mm")
            s.text((xx + 82, yy + 47), f"valor {wv}", size=17, color=col, anchor="mm")
        s.box(24, 520, 1232, 86, "conjuntos")
        s.text((50, 556), comps, size=24, color="gold", bold=True)
        s.text((1230, 556), f"coste = {tot}", size=24, color="green", bold=True, anchor="ra")
        if tipo == "para":
            s.caption("Ya hay 5 = V − 1 aristas: se para.", y=628)
        else:
            s.caption({"acepta": f"{a} y {b} están en conjuntos distintos → se acepta y se unen", "rechaza": f"{a} y {b} ya están unidos → cerraría un ciclo → se descarta"}[tipo], y=628)
        nombre = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez"}
        if tipo == "acepta":
            nar = f"La arista {a} {b}, de valor {nombre[w_]}: están en conjuntos distintos. Se acepta y se unen."
        elif tipo == "rechaza":
            nar = f"La arista {a} {b}, de valor {nombre[w_]}: tres y cinco ya están unidos a través del cuatro. Cerraría un ciclo, así que se descarta."
        else:
            nar = f"Ya tenemos cinco aristas, que son V menos uno. Paramos. El coste del árbol es {tot}."
        add(s, nar)

    # ------------------------------------------------------------------ 11 · Prim
    s = ideas("Algoritmo de Prim", [
        "1 · Empezar en un vértice cualquiera: ese es el árbol.",
        "2 · Mirar las aristas que unen un vértice del árbol con uno de FUERA.",
        ("3 · Aceptar la de menor valor (se saca de una cola de prioridad) y añadir su vértice.", "gold"),
        "4 · Repetir hasta tener V − 1 aristas.",
        ("Coste O(A log V). Si el grafo no es conexo, solo recubre la componente del inicio.", "muted"),
    ], "ARM")
    add(s, "El algoritmo de Prim hace otra cosa: empieza en un vértice y va haciendo crecer un único árbol. "
           "En cada paso mira las aristas que unen el árbol con vértices de fuera, y acepta la de menor valor. "
           "Por la propiedad del corte, esa arista siempre es buena. Con una cola de prioridad, el coste es de orden A por logaritmo de V.", cap_title="Algoritmo de Prim")
    for k, (dentro, front, e, nuevo, tot) in enumerate(sim_prim(), 1):
        s = Slide(f"Prim desde el 0 · paso {k}", f"coste = {tot}")
        s.box(24, 84, 640, 420, "grafo (verde: en el árbol)")
        es = {}
        for (a, b, wv) in GE:
            if (a in dentro or b in dentro) and (a in dentro) != (b in dentro):
                es[(a, b)] = ("blue", 4)
        prev = [x for x in sim_prim()[:k - 1]]
        for (_, _, e2, _, _) in prev:
            es[(e2[0], e2[1])] = ("green", 7)
        es[(e[0], e[1])] = ("gold", 8)
        ns = {v: (("green" if v in dentro else "node"), "node_t", ("gold" if v == nuevo else None)) for v in range(6)}
        wgraph(s, gpos(40, 70), GE, es=es, ns=ns, r=22, lsize=19)
        s.box(684, 84, 572, 420, "aristas que cruzan (árbol ↔ fuera)")
        for j, (a, b, wv) in enumerate(front):
            xx, yy = 710 + (j % 3) * 180, 130 + (j // 3) * 80
            col, fl = ("gold", "gold_d") if j == 0 else ("blue", "blue_d")
            s.d.rounded_rectangle((xx, yy, xx + 165, yy + 62), 12, fill=C[fl], outline=C[col], width=3)
            s.text((xx + 82, yy + 20), f"{a}-{b}", size=22, bold=True, anchor="mm")
            s.text((xx + 82, yy + 45), f"valor {wv}", size=17, color=col, anchor="mm")
        s.box(24, 520, 1232, 86, "árbol")
        s.text((50, 556), "{" + ",".join(map(str, dentro)) + "}  +  " + str(nuevo), size=24, color="gold", bold=True)
        s.caption(f"La más barata que sale del árbol: {e[0]}-{e[1]} (valor {e[2]}). Entra el vértice {nuevo}.", y=628)
        add(s, f"Paso {k}. De las aristas que salen del árbol, la más barata es la {e[0]} {e[1]}, con valor {e[2]}. Entra el vértice {nuevo}.")
    s = Slide("Kruskal y Prim dan el mismo árbol", "coste 21")
    tabla(s, 100, 130, ["", "Kruskal", "Prim"], [
        ["Estructura", "ordenar aristas + conjuntos disjuntos", "cola de prioridad de aristas"],
        ["Cómo crece", "un bosque que se va fundiendo", "un único árbol"],
        ["Coste", "O(V + A log A)", "O(A log V)"],
        ["Mejor con…", "pocas aristas", "muchas aristas"],
    ], [220, 460, 400], rh=64, size=22)
    s.caption("Con valores distintos, el ARM es único: los dos obtienen el mismo.", y=520)
    add(s, "Los dos algoritmos obtienen el mismo árbol, porque con valores distintos es único. Kruskal ordena las aristas y usa conjuntos disjuntos. Prim usa una cola de prioridad. "
           "Kruskal es muy cómodo cuando hay pocas aristas, y es el que usaremos en los ejercicios.")

    # ------------------------------------------------------------------ 12 · 06-3, 06-4, 06-5
    s = Slide("Los tres ejercicios de Kruskal", "06-3 · 06-4 · 06-5")
    tabla(s, 40, 110, ["Ejercicio", "Pregunta", "Qué se guarda", "Cuándo se para"], [
        ["06-3 Archipiélago", "coste mínimo para conectar todo", "SUMA de las aristas aceptadas", "V−1 aceptadas (o se acaban)"],
        ["06-4 Tarzán", "cuerda mínima para conectar todo", "ÚLTIMA arista aceptada", "queda 1 conjunto"],
        ["06-5 Trajano", "aguante mínimo entre DOS cámaras", "la arista que las conecta", "unidos(origen, destino)"],
    ], [230, 390, 340, 270], rh=90, size=17)
    s.caption("El mismo Kruskal; cambia solo lo que se pregunta.", y=520)
    add(s, "Los tres ejercicios restantes son el mismo Kruskal con tres preguntas distintas. En el seis tres se suma el coste de las aristas aceptadas. "
           "En el seis cuatro, se guarda el valor de la última arista aceptada. Y en el seis cinco, se para en cuanto el origen y el destino quedan unidos.",
        cap_title="Ejercicios 06-3, 06-4 y 06-5")

    # 06-3
    s = Slide("06-3 · Recorriendo el archipiélago en bicicleta", "ejemplo 1")
    isl = {1: (150, 150), 2: (330, 130), 3: (170, 370), 4: (350, 330)}
    ie = [(1, 2, 5), (1, 3, 10), (2, 4, 7), (1, 4, 8), (3, 4, 2)]
    s.box(30, 100, 520, 420, "puentes presupuestados")
    wgraph(s, {v: (x + 80, y + 20) for v, (x, y) in isl.items()}, ie, es={(3, 4): ("green", 7), (1, 2): ("green", 7), (2, 4): ("green", 7), (1, 4): ("red", 2), (1, 3): ("red", 2)}, r=24, lsize=22)
    s.box(570, 100, 670, 420, "Kruskal")
    s.text((600, 150), "ordenados:  3-4 (2)   1-2 (5)   2-4 (7)   1-4 (8)   1-3 (10)", size=19, color="muted")
    s.bullets(600, 200, 620, ["3-4 (2): se acepta  →  suma 2", "1-2 (5): se acepta  →  suma 7", "2-4 (7): se acepta  →  suma 14, ya hay 3 = I − 1: parar",
                              ("Respuesta: 14", "gold"), "Si se acaban las aristas con menos de I − 1: «No hay puentes suficientes»."], size=20, gap=12)
    add(s, "Ejercicio seis tres, el archipiélago. Ordenamos los puentes: tres cuatro cuesta dos, uno dos cinco, dos cuatro siete. Los aceptamos, y ya tenemos tres, que son islas menos una. "
           "La suma es catorce. Si se acaban los puentes y hay menos de islas menos uno aceptados, hay que escribir que no hay puentes suficientes. Con una sola isla, la respuesta es cero.")
    # 06-4
    s = Slide("06-4 · La selva de Tarzán", "ejemplo 1")
    te = [(1, 2, 5), (2, 3, 10), (3, 1, 7), (2, 4, 8)]
    tp = {1: (150, 150), 2: (350, 150), 3: (250, 340), 4: (500, 150)}
    s.box(30, 100, 560, 420, "saltos posibles (longitud mínima de cuerda)")
    wgraph(s, {v: (x + 20, y + 20) for v, (x, y) in tp.items()}, te, es={(1, 2): ("green", 7), (3, 1): ("green", 7), (2, 4): ("gold", 8), (2, 3): ("red", 2)}, r=24, lsize=22)
    s.box(610, 100, 630, 420, "Kruskal: la última arista aceptada")
    s.bullets(630, 150, 590, ["1-2 (5): se acepta   ultima = 5", "3-1 (7): se acepta   ultima = 7", "2-4 (8): se acepta   ultima = 8  →  queda 1 conjunto", "2-3 (10): ni se mira",
                              ("Respuesta: 8", "gold"), "Si al final quedan 2 o más conjuntos:  Imposible.  Con N = 1: 0."], size=20, gap=12)
    add(s, "Ejercicio seis cuatro, la selva de Tarzán. Con una cuerda de longitud L se pueden hacer todos los saltos de valor menor o igual que L. "
           "Necesitamos el menor L que conecte todo, y eso es la última arista que acepta Kruskal. Aquí es ocho. El salto de diez nunca hace falta. "
           "Si quedan dos o más conjuntos, es imposible. Con un solo árbol, la respuesta es cero.")
    # 06-5
    s = Slide("06-5 · Las minas del emperador Trajano", "ejemplo 1: de la cámara 1 a la 4")
    me = [(1, 2, 2), (2, 4, 5), (4, 1, 10), (1, 3, 6)]
    mp = {1: (130, 280), 2: (300, 140), 3: (130, 420), 4: (470, 280)}
    s.box(30, 100, 560, 440, "galerías (segundos)")
    wgraph(s, {v: (x + 20, y - 20) for v, (x, y) in mp.items()}, me, es={(1, 2): ("green", 7), (2, 4): ("gold", 8), (4, 1): ("red", 2), (1, 3): ("dim", 3)},
           ns={1: ("green", "node_t", "gold"), 4: ("green", "node_t", "gold")}, r=24, lsize=22)
    s.box(610, 100, 630, 440, "Kruskal con parada")
    s.bullets(630, 150, 590, ["Si origen = destino  ⇒  0.", "1-2 (2): unir  →  ¿1 y 4 unidos? no", "2-4 (5): unir  →  ¿1 y 4 unidos? SÍ",
                              ("Respuesta: 5  (la galería que los conecta)", "gold"),
                              "La galería directa 1-4 tarda 10 s: peor que el rodeo, cuyo máximo es 5.",
                              ("No es un camino mínimo por SUMA: cuenta la galería más larga.", "muted"), "Si no se unen nunca:  IMPOSIBLE."], size=20, gap=10)
    add(s, "Ejercicio seis cinco, las minas de Trajano. Hay que ir de la cámara uno a la cuatro minimizando la galería más larga del camino. "
           "Kruskal une galerías en orden de tiempo, y paramos en cuanto el origen y el destino quedan en el mismo conjunto. "
           "Tras la galería de dos segundos no están unidos. Tras la de cinco, sí. La respuesta es cinco. "
           "Si el origen es el destino, es cero, y si nunca se unen, imposible.")

    # ------------------------------------------------------------------ 13 · resumen
    add(cierre("Conjuntos disjuntos y grafos valorados", [
        "Conjuntos disjuntos: solo unir; con tamaños y compresión, casi O(1) por operación.",
        "06-1: celdas = elementos, uniones al añadir petróleo, cardinal para el máximo.",
        "Grafo valorado: aristas con valor; ady(v), a.otro(v), a.valor(), aristas().",
        "06-2: recorrido que solo cruza aristas con valor ≥ anchura.",
        "ARM: propiedad del corte. Kruskal (ordenar + conjuntos disjuntos) o Prim (cola de prioridad).",
        "06-3 suma · 06-4 última arista · 06-5 parar al unir origen y destino.",
    ]), "Resumiendo: los conjuntos disjuntos permiten unir y preguntar si dos elementos están juntos en tiempo casi constante. Los usamos en el seis uno para las manchas, y en Kruskal para detectar ciclos. "
        "Un grafo valorado lleva un valor en cada arista, y en el seis dos recorremos filtrando por ese valor. "
        "El árbol de recubrimiento mínimo se obtiene con Kruskal o con Prim, y los ejercicios seis tres, seis cuatro y seis cinco son tres preguntas distintas sobre el mismo Kruskal.",
        cap_title="Resumen")

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/06-0_{i:03}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4", chapters=cap)
        print(f"06-0: {t / 60:.1f} min")


if __name__ == "__main__":
    main("--preview" in sys.argv)
