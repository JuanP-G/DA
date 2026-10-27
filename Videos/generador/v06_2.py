"""Vídeo EJ 06-2 · Camiones de reparto (DFS con filtro valor >= anchura)."""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line
from v06_teoria import limpia, wgraph
from v06e_comun import TEMA, pinta_preview

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-2/EJ_06-2.cpp"
NOMBRE = "Camiones de reparto"
COR = "EJ 06-2"
C0, C1 = find_line(CPP, "class Alcanzables"), find_line(CPP, "void dfs(")
CLASE = limpia(code_lines(CPP, C0, C1 + 6, maxc=72))
R0 = find_line(CPP, "void resuelveCaso()")
RES = limpia(code_lines(CPP, R0, find_line(CPP, "cout << (a.alcanzable") + 2, maxc=72))
L_FILT = find_line(CPP, "if (a.valor() >= ancho")
L_DFS = find_line(CPP, "dfs(g, origen);")
L_VIS = find_line(CPP, "visitado(g.V(), false)")
L_LEE = find_line(CPP, "GrafoValorado<int> g(cin, 1);")
L_NEW = find_line(CPP, "Alcanzables a(g, origen - 1, ancho);")
L_OUT = find_line(CPP, "cout << (a.alcanzable")

V = 5
E = [(1, 2, 10), (1, 3, 30), (2, 4, 20), (3, 4, 15), (4, 5, 12)]
POS = {1: (730, 330), 2: (880, 170), 3: (880, 490), 4: (1040, 330), 5: (1190, 330)}
QS = [(1, 5, 8), (1, 4, 12), (1, 4, 15), (2, 5, 15)]


def dfs_orden(org, ancho):
    ady = {v: [] for v in range(1, V + 1)}
    for a, b, c in E:
        ady[a].append((b, c))
        ady[b].append((a, c))
    vis, orden = set(), []

    def rec(v):
        vis.add(v)
        orden.append(v)
        for w, c in ady[v]:
            if c >= ancho and w not in vis:
                rec(w)
    rec(org)
    return orden


def slide_consulta(i):
    org, dst, ancho = QS[i]
    orden = dfs_orden(org, ancho)
    ok = dst in orden
    s = Slide(f"Consulta {i + 1}: de {org} a {dst}, camión {ancho}", COR)
    s.box(24, 84, 600, 520, "qué calles valen (anchura ≥ camión)")
    for j, (a, b, c) in enumerate(E):
        val = c >= ancho
        s.text((56, 132 + j * 40), f"{a}–{b}  (anchura {c})   {'✓' if val else '✗  estrecha'}", size=23, mono=True,
               color="green" if val else "red")
    s.text((56, 345), "DFS desde " + str(org) + ":", size=22, color="muted")
    s.text((56, 382), "  ".join(map(str, orden)), size=32, mono=True, color="gold", bold=True)
    s.text((56, 450), f"¿llega a {dst}?", size=26)
    s.text((56, 495), "SI" if ok else "NO", size=64, bold=True, color="green" if ok else "red")
    s.box(644, 84, 612, 520, f"camión de anchura {ancho}")
    es = {}
    for a, b, c in E:
        es[(a, b)] = ("green", 6) if c >= ancho else ("red", 2)
    ns = {}
    for v in POS:
        ns[v] = ("gold" if v in orden else "node", "node_t", "blue" if v == org else ("red" if v == dst else None))
    wgraph(s, POS, E, es=es, ns=ns, r=24, lsize=22)
    for k, v in enumerate(orden):
        x, y = POS[v]
        s.pill(x - 14, y + 30, str(k + 1), fill="blue_d", color="text", size=15, padx=7, pady=1)
    s.text((664, 560), "los números azules son el orden en que el DFS visita cada vértice", size=16, color="muted")
    return s, org, dst, ancho, orden, ok


NARRA = [
    "Primera consulta: de la intersección 1 a la 5 con un camión de anchura 8. Todas las calles admiten al menos 8, así que el recorrido pasa por todas. Visita 1, 2, 4, 3 y 5: llega. Sí.",
    "Segunda: de la 1 a la 4, anchura 12. La calle de 1 a 2 solo admite 10, así que se ignora. Desde la 1 se va a la 3, y de la 3 a la 4, que mide 15. Llega. Sí.",
    "Tercera: de la 1 a la 4, anchura 15. Se ignoran la calle de 1 a 2, que mide 10, y la de 4 a 5, que mide 12. Pero la de 3 a 4 mide justo 15, y un camión de anchura 15 cabe: por eso la condición es mayor o igual. Sí.",
    "Cuarta: de la 2 a la 5, anchura 15. Solo valen las calles 1–3, 2–4 y 3–4. Desde la 2 se llega a la 4, la 3 y la 1, pero la calle de 4 a 5 mide 12 y no vale. No se llega a la 5. No.",
]


def main(preview=False):
    segs = [(portada(NOMBRE, COR, TEMA),
             "Camiones de reparto. Cada consulta es una pregunta de alcanzabilidad, pero ignorando las calles demasiado estrechas: un recorrido en profundidad con filtro.", 0)]

    segs.append((ideas("El problema", [
        "V intersecciones (hasta 10.000) y E calles de doble sentido (hasta 100.000).",
        "Cada calle tiene la anchura MÁXIMA que puede tener un camión para pasar.",
        "K ≤ 10 consultas: origen, destino y anchura del camión.",
        ("Para cada una: SI si el camión puede ir del origen al destino, NO si no.", "gold"),
    ]), "Tenemos intersecciones y calles de doble sentido, cada una con la anchura máxima que puede tener un camión para pasar. "
        "Nos hacen como mucho diez consultas con un origen, un destino y la anchura del camión, y hay que decir si el camión puede ir del origen al destino.", 0))

    s = Slide("Alcanzabilidad con filtro", TEMA)
    s.box(40, 100, 1200, 150, "idea")
    s.text((70, 150), "¿hay un camino origen → destino con solo aristas de valor ≥ anchura?", size=28, mono=True, color="gold")
    s.text((70, 200), "Grafo valorado no dirigido: intersecciones = vértices, calles = aristas, anchura = valor.", size=22, color="muted")
    s.bullets(60, 290, 1160, [
        "Un DFS desde el origen que ignora las aristas demasiado estrechas lo responde.",
        ("La comparación es  ≥ : un camión de anchura 15 cabe justo por una calle de 15.", "gold"),
        "El filtro cambia con cada camión: se repite el recorrido con un vector de visitados NUEVO.",
        "Coste: O(K · (V + E)), con K ≤ 10.",
    ], size=23, gap=16)
    segs.append((s, "Es una pregunta de alcanzabilidad con un filtro: hay un camino del origen al destino que use solo calles de anchura mayor o igual que la del camión. "
                    "Un recorrido en profundidad desde el origen, que ignore las calles demasiado estrechas, lo responde. Ojo: la comparación es mayor o igual, porque un camión de anchura quince cabe justo por una calle de quince. "
                    "Como el filtro cambia con cada camión, se repite el recorrido con un vector de visitados nuevo. El coste es K por V más E.", 0))

    s = Slide("El código: la clase Alcanzables", "EJ_06-2.cpp")
    s.code(24, 84, 800, 520, CLASE, hl={L_VIS, L_DFS, L_FILT}, title="class Alcanzables", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["El constructor crea visitado a false y lanza el DFS desde el origen.",
                              "dfs marca v como visitado y recorre sus aristas g.ady(v).",
                              "a.otro(v) es el vértice del otro extremo.",
                              ("Solo se baja si  a.valor() >= ancho  y no se ha visitado.", "gold"),
                              "alcanzable(v) consulta el vector."], size=19, gap=14)
    segs.append((s, "La clase Alcanzables lanza el recorrido desde el constructor, con un vector de visitados limpio. El recorrido marca el vértice y mira cada arista. "
                    "Solo baja por una arista si su valor es mayor o igual que el ancho del camión y el otro extremo no se ha visitado. Después, alcanzable consulta el vector.", 0))

    s = Slide("El código: resuelveCaso", "EJ_06-2.cpp")
    s.code(24, 84, 800, 400, RES, hl={L_LEE, L_NEW, L_OUT}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 400, "qué hace")
    s.bullets(864, 130, 372, ["GrafoValorado(cin, 1): lee V, E y las calles, numeradas desde 1.",
                              "Por cada consulta: un objeto Alcanzables nuevo.",
                              "Se resta 1 al origen y al destino.",
                              "Salida: SI o NO."], size=19, gap=14)
    s.bullets(60, 510, 1160, [("Cada Alcanzables nace con su propio vector de visitados: nunca se arrastra el de la consulta anterior.", "gold")], size=21, gap=10)
    segs.append((s, "En resuelveCaso leemos el grafo con las intersecciones numeradas desde uno. Por cada consulta creamos un objeto Alcanzables nuevo, restando uno al origen y al destino, "
                    "y escribimos sí o no. Como cada objeto nace con su propio vector de visitados, nunca se arrastra el de la consulta anterior.", 0))

    s = Slide("El ejemplo", COR)
    s.box(24, 100, 1232, 440, "V = 5, E = 5")
    wgraph(s, {1: (240, 330), 2: (400, 190), 3: (400, 470), 4: (570, 330), 5: (720, 330)}, E, r=24, lsize=22)
    s.bullets(880, 150, 350, ["Aristas: 1–2 (10), 1–3 (30), 2–4 (20), 3–4 (15), 4–5 (12).", ("4 consultas:", "gold"),
                              "1→5, camión 8", "1→4, camión 12", "1→4, camión 15", "2→5, camión 15"], size=19, gap=10)
    segs.append((s, "Veamos el ejemplo: cinco intersecciones y cinco calles, con las anchuras que se ven en el dibujo. Y cuatro consultas.", 0))

    for i in range(4):
        sl, org, dst, ancho, orden, ok = slide_consulta(i)
        segs.append((sl, NARRA[i], 0))

    segs.append((ideas("Detalles y coste", [
        "La comparación es ≥, no >: con > fallaría la tercera consulta.",
        "Reiniciar los visitados en cada consulta (un objeto nuevo).",
        "Calles repetidas entre el mismo par: no molestan, son dos aristas más.",
        "La recursión baja como mucho V = 10.000 niveles: no hay problema de pila.",
        ("Coste: O(K · (V + E)) ≈ 10 · 110.000 operaciones.", "gold"),
    ]), "Detalles. La comparación es mayor o igual, no mayor: con mayor fallaría la tercera consulta. Hay que empezar con visitados nuevos en cada consulta. "
        "Las calles repetidas no molestan, y la recursión baja como mucho diez mil niveles. El coste es K por V más E, unas diez veces ciento diez mil operaciones.", 0))

    segs.append((cierre(NOMBRE, [
        "Intersecciones = vértices, calles = aristas, anchura = valor.",
        "Cada consulta: DFS desde el origen ignorando aristas con valor < anchura.",
        "Condición  a.valor() >= ancho: el camión cabe justo.",
        "Visitados nuevos en cada consulta.",
        "O(K · (V + E)).",
    ]), "Resumiendo: un recorrido en profundidad con filtro, una vez por consulta, ignorando las calles más estrechas que el camión.", 0))

    if preview:
        pinta_preview(segs, "06-2")
    else:
        print(f"06-2: {build(segs, '../06-2_camiones_de_reparto.mp4'):.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
