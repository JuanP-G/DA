"""Vídeo EJ 05-4 · Sumidero en un grafo dirigido"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../5-Grafos dirigidos/EJ_05-4/EJ_05-4.cpp"
NOMBRE = "Sumidero en un grafo dirigido"
TEMA = "Tema 5 · Grafos dirigidos"

# ejemplo 1 (con sumidero) y ejemplo 2 (sin sumidero), en el orden de entrada
E1 = [(1, 0), (0, 2), (3, 2), (1, 2)]
E2 = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
N = 4
BASE = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}

L_FN = find_line(CPP, "int sumidero(")
L_ENT = find_line(CPP, "vector<int> entrada(")
L_CUENTA = find_line(CPP, "++entrada[w];")
L_BUSCA = find_line(CPP, "if (g.ady(v).empty()")
L_RET = find_line(CPP, "return v;")
L_NO = find_line(CPP, "return -1;")
CODE = code_lines(CPP, L_FN, L_NO + 1, maxc=64)
CODE_S = code_lines(CPP, L_FN, L_NO + 1, maxc=52)


def pos(ox, oy, sx, sy):
    return {v: (ox + c * sx, oy + f * sy) for v, (c, f) in BASE.items()}


def salidas(E):
    s = [0] * N
    for a, _ in E:
        s[a] += 1
    return s


def slide_estado(titulo, corner, E, ent, sal, marca, hl, cap, vhot=None, edge_hot=None, ent_final=False, sink=None):
    s = Slide(titulo, corner)
    s.code(24, 84, 600, 520, CODE_S, hl=hl, title="int sumidero(Digrafo const& g)")
    s.box(644, 84, 612, 300, "el digrafo")
    ns = {}
    if vhot is not None:
        ns[vhot] = ("gold", "node_t", None)
    if sink is not None:
        ns[sink] = ("green", "node_t", None)
    es = {e: ("dim", 3) for e in E}
    if edge_hot is not None:
        es[edge_hot] = ("gold", 6)
    s.dgraph(pos(790, 150, 280, 150), E, ns=ns, es=es, labels={v: str(v) for v in range(N)}, r=28)
    s.box(644, 400, 612, 204, "grados")
    s.cells(664, 440, "salida", sal, cw=60, colors={vhot: "blue_d"} if vhot is not None else None)
    s.cells(664, 520, "entrada", ent, cw=60, hl={marca} if marca is not None else None,
            colors={vhot: "blue_d"} if vhot is not None else None)
    s.text((1130, 440 + 8), "= ady(v).size()", size=15, color="muted", anchor="la")
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-4", TEMA),
             "Sumidero en un grafo dirigido. Vemos qué es un sumidero, cómo se calculan los grados de entrada y de salida "
             "con las listas de adyacencia, y por qué basta un recorrido de todas las aristas.", 0)]

    segs.append((ideas("El problema", [
        "Un vértice s es SUMIDERO si todos los demás vértices tienen una arista hacia s y s no tiene ninguna hacia ellos.",
        ("Es decir: grado de salida 0 y grado de entrada V − 1.", "gold"),
        "Entrada: V (1 … 10.000), A (0 … 100.000) y A aristas «origen destino» (vértices desde 0).",
        "Salida: «SI s» si hay sumidero, o «NO». Varios casos, hasta el final de la entrada.",
    ]), "Un vértice es un sumidero si todos los demás vértices tienen una arista hacia él y él no tiene ninguna hacia ellos. "
        "Es decir, su grado de salida es cero y su grado de entrada es V menos uno. Hay que decir si el grafo tiene un sumidero y cuál es.", 0))

    # modelo
    ent1 = [0] * N
    for a, b in E1:
        ent1[b] += 1
    s = Slide("Ejemplo 1: el vértice 2 es sumidero", TEMA)
    s.box(40, 90, 600, 440, "grafo con 4 vértices y 4 aristas")
    s.dgraph(pos(190, 190, 300, 220), E1, labels={v: str(v) for v in range(N)}, r=34,
             ns={2: ("green", "node_t", None)}, es={e: ("muted", 4) for e in E1})
    s.box(670, 90, 570, 440, "grados")
    s.cells(690, 140, "salida", salidas(E1), cw=70)
    s.cells(690, 230, "entrada", ent1, cw=70, hl={2}, colors={2: "green_d"} if "green_d" in C else None)
    s.bullets(690, 330, 530, [
        "Vértice 2: salida 0 y entrada 3 = V − 1.",
        ("Los otros tres apuntan a él y él a ninguno.", "gold"),
    ], size=21, gap=12)
    segs.append((s, "En el primer ejemplo, el vértice dos es sumidero: no tiene ninguna arista de salida y le llegan tres, que son todos los demás vértices. "
                    "Los otros tres apuntan a él, y él no apunta a ninguno.", 0))

    segs.append((ideas("¿Cómo se calculan los grados?", [
        ("Salida de v:  g.ady(v).size()   →   O(1).", "gold"),
        ("Entrada de v:  cuántas veces aparece v en las listas de adyacencia de todos los vértices.", "gold"),
        "Un recorrido de TODAS las listas: para cada arista v → w, ++entrada[w].   →   O(V + A) en total.",
        "(El digrafo no guarda el grado de entrada: habría que recorrer las listas, o mirar g.inverso().)",
        "Después: buscar un vértice con salida 0 y entrada V − 1.",
    ]), "El grado de salida es inmediato: es el tamaño de la lista de adyacentes. "
        "El grado de entrada no está guardado: hay que recorrer las listas de todos los vértices y, por cada arista de v a w, sumar uno a la entrada de w. "
        "Eso cuesta V más A en total. Después buscamos un vértice con salida cero y entrada V menos uno.", 0))

    s = Slide("El código", "EJ_05-4.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_ENT, L_CUENTA, L_BUSCA}, title="int sumidero(Digrafo const& g)")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["entrada[v] empieza en 0.",
                              "Para cada v y cada w de ady(v): ++entrada[w].",
                              "Busca v con ady(v) vacía y entrada[v] == V − 1.",
                              "Devuelve v, o −1 si no hay.",
                              "La lectura es Digrafo g(cin): ya trae V, A y las aristas."], size=19, gap=14)
    segs.append((s, "El código crea el vector de entradas a cero. Recorre todas las listas y, por cada arista de v a w, suma uno a la entrada de w. "
                    "Después busca un vértice cuya lista de adyacentes esté vacía y cuya entrada valga V menos uno, y lo devuelve; si no hay, devuelve menos uno. "
                    "La lectura es directamente el constructor del digrafo, que ya lee los vértices, las aristas y los pares.", 0))

    # traza ejemplo 1
    ent = [0] * N
    sal = salidas(E1)
    segs.append((slide_estado("Ejemplo 1: contar entradas", "paso 0", E1, ent[:], sal, None, {L_ENT},
                              "entrada = [0, 0, 0, 0]: aún no hemos mirado ninguna arista"),
                 "Empezamos con todas las entradas a cero.", 0))
    for k, (a, b) in enumerate(E1, 1):
        ent[b] += 1
        segs.append((slide_estado("Ejemplo 1: contar entradas", f"arista {k} de {len(E1)}", E1, ent[:], sal, b, {L_CUENTA},
                                  f"arista {a} → {b}:  ++entrada[{b}]  =  {ent[b]}", edge_hot=(a, b)),
                     f"Arista de {a} a {b}: sumamos uno a la entrada de {b}, que pasa a valer {ent[b]}.", 0))
    for v in range(3):
        cap = (f"vértice {v}: salida {sal[v]} ≠ 0  ⇒  no puede ser sumidero" if sal[v] != 0 else
               f"vértice {v}: salida 0 y entrada {ent[v]} = V − 1 = {N - 1}  ⇒  SUMIDERO  ⇒  SI {v}")
        nar = (f"Buscamos. El vértice {v} tiene salida {sal[v]}, así que no es sumidero." if sal[v] != 0 else
               f"El vértice {v} tiene salida cero y entrada {ent[v]}, que es V menos uno. Es el sumidero: la respuesta es sí {v}.")
        segs.append((slide_estado("Ejemplo 1: buscar el sumidero", f"vértice {v}", E1, ent[:], sal, v, {L_BUSCA, L_RET} if sal[v] == 0 else {L_BUSCA},
                                  cap, vhot=v if sal[v] != 0 else None, sink=v if sal[v] == 0 else None), nar, 0))

    # ejemplo 2
    ent2 = [0] * N
    for a, b in E2:
        ent2[b] += 1
    sal2 = salidas(E2)
    s = slide_estado("Ejemplo 2: no hay sumidero", TEMA, E2, ent2, sal2, 3, {L_BUSCA, L_NO},
                     "único vértice con salida 0: el 3, pero su entrada es 2 ≠ 3 (el 0 no apunta a él)  ⇒  NO", vhot=3)
    segs.append((s, "En el segundo ejemplo, el único vértice con salida cero es el tres, pero su entrada es dos, no tres: "
                    "el cero no tiene ninguna arista hacia él. Por tanto no hay sumidero, y la respuesta es no.", 0))

    segs.append((ideas("Detalles", [
        "Como mucho hay UN sumidero: si s y t lo fueran, existiría t → s y t no tendría salida 0.",
        "Sin lazos ni aristas repetidas: entrada V − 1 significa que TODOS los demás apuntan a s.",
        "V = 1: el único vértice tiene salida 0 y entrada 0 = V − 1  ⇒  SI 0.",
        "Con matriz de adyacencia existe un truco en O(V); con listas no compensa, porque leer las aristas ya cuesta O(A).",
        ("Coste: O(V + A) por caso.", "gold"),
    ]), "Algunos detalles. Como mucho hay un sumidero, porque si hubiera dos, uno apuntaría al otro y ya no tendría salida cero. "
        "Como no hay lazos ni aristas repetidas, tener entrada V menos uno significa que todos los demás apuntan a él. "
        "Con un único vértice, el sumidero es el cero. Y el coste es V más A por caso.", 0))

    segs.append((cierre(NOMBRE, [
        "Sumidero: salida 0 y entrada V − 1.",
        "Salida de v: g.ady(v).size().",
        "Entrada de v: contar cuántas veces aparece en todas las listas.",
        "Buscar el vértice con ady vacía y entrada V − 1.",
        "Coste O(V + A).",
    ]), "Resumiendo: un sumidero tiene salida cero y entrada V menos uno. La salida es el tamaño de la lista, la entrada se cuenta recorriendo todas las listas, "
        "y después se busca el vértice que cumpla las dos condiciones. El coste es lineal.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-4_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-4_sumidero.mp4")
        print(f"05-4: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
