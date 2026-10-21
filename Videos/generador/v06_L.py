"""Vídeo EJ 06-L · ¿Dónde construimos los aeropuertos?"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07_comun import etiquetas

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-L/EJ_06-L.cpp"
NOMBRE = "¿Dónde construimos los aeropuertos?"
TEMA = "Tema 6 · Conjuntos disjuntos y grafos valorados"

L_ORD = find_line(CPP, "sort(carreteras.begin()")
L_BRK = find_line(CPP, "if (c.valor() >= A) break;")
L_UNI = find_line(CPP, "cd.unir(u, v);")
L_SUM = find_line(CPP, "coste += c.valor();")
L_AER = find_line(CPP, "int aeropuertos = cd.num_cjtos();")
L_TOT = find_line(CPP, "coste += (long long)aeropuertos * A;")
L_ARI = find_line(CPP, "g.ponArista({x - 1, y - 1, c});")
L_LL = find_line(CPP, "long long coste = 0;")
CODE = code_lines(CPP, find_line(CPP, "void resuelveCaso()"), find_line(CPP, "cout << coste"), maxc=70)

# ejemplo 1 (N=4, A=100) y ejemplo 3 (N=3, A=50)
EJ1 = dict(n=4, A=100, pos={0: (760, 190), 1: (1000, 190), 2: (1000, 400), 3: (760, 400)},
           E=[(0, 1, 10), (1, 2, 30), (3, 0, 40), (3, 2, 20)])
EJ3 = dict(n=3, A=50, pos={0: (760, 380), 1: (880, 200), 2: (1060, 380)},
           E=[(0, 1, 20), (1, 2, 50), (0, 2, 80)])


def simula(ej):
    """Kruskal con C < A: lista de pasos (arista, decisión, grupos, total)."""
    n, A = ej["n"], ej["A"]
    p = list(range(n))

    def f(x):
        while p[x] != x:
            x = p[x]
        return x
    tot, pasos = 0, []
    for k, (a, b, c) in sorted(enumerate(ej["E"]), key=lambda t: t[1][2]):
        if c >= A:
            pasos.append((k, "para", None, tot))
            break
        if f(a) != f(b):
            p[f(a)] = f(b)
            tot += c
            pasos.append((k, "une", len({f(i) for i in range(n)}), tot))
        else:
            pasos.append((k, "ciclo", len({f(i) for i in range(n)}), tot))
    grupos = {}
    for i in range(n):
        grupos.setdefault(f(i), []).append(i + 1)
    return pasos, list(grupos.values())


def dibuja(s, ej, hasta, k_actual=None, final=False):
    """Pinta el grafo con las carreteras construidas hasta el paso `hasta` (exclusive)."""
    pasos, grupos = simula(ej)
    pos, E = ej["pos"], ej["E"]
    es, hl, ns = {}, {}, {}
    for (k, d, g, t) in pasos[:hasta]:
        a, b, c = E[k]
        if d == "une":
            es[(a, b)] = ("green", 6)
            hl[k] = "green"
        elif d == "ciclo":
            es[(a, b)] = ("muted", 3)
        else:
            es[(a, b)] = ("red", 4)
            hl[k] = "red"
    if k_actual is not None:
        a, b, c = E[k_actual]
        es[(a, b)] = ("gold", 7)
        hl[k_actual] = "gold"
    if final:
        for gi, g in enumerate(grupos):
            for v in g:
                ns[v - 1] = (("gold" if len(g) else "node"), "node_t", None)
    s.graph(pos, [(a, b) for a, b, c in E], ns=ns, es=es, r=24, labels=[str(v + 1) for v in range(ej["n"])])
    etiquetas(s, pos, E, hl)


def slide_traza(titulo, ej, i, nombre_ej):
    """Una diapositiva por carretera."""
    pasos, grupos = simula(ej)
    A = ej["A"]
    k, d, g, tot = pasos[i]
    a, b, c = ej["E"][k]
    s = Slide(titulo, TEMA)
    s.box(24, 84, 600, 520, "carreteras ordenadas por coste")
    ordenadas = sorted(ej["E"], key=lambda e: e[2])
    for j, (x, y, cc) in enumerate(ordenadas):
        col = "gold" if (x, y, cc) == ej["E"][k] else "text"
        marca = ""
        if j < i:
            marca = {"une": "  ✓ construida", "ciclo": "  ✗ ciclo", "para": ""}[pasos[j][1]]
        s.text((56, 136 + j * 44), f"{x + 1}–{y + 1}   coste {cc}{marca}", size=24, mono=True, color=col)
    s.text((56, 136 + len(ordenadas) * 44 + 16), f"A = {A}  (coste de un aeropuerto)", size=22, color="muted")
    s.box(644, 84, 612, 520, nombre_ej)
    dibuja(s, ej, i, k)
    if d == "para":
        s.caption(f"{c} ≥ A = {A}: ya no compensa. Se para.", y=626)
    elif d == "une":
        s.caption(f"{c} < {A} y grupos distintos: se construye. Total carreteras: {tot}.", y=626)
    else:
        s.caption(f"{a + 1} y {b + 1} ya están unidos: cerraría un ciclo, se descarta.", y=626)
    return s, pasos[i]


def narra_traza(titulo, ej, nombre_ej):
    pasos, grupos = simula(ej)
    segs = []
    A = ej["A"]
    for i in range(len(pasos)):
        s, (k, d, g, tot) = slide_traza(titulo, ej, i, nombre_ej)
        a, b, c = ej["E"][k]
        if d == "une":
            nar = f"La carretera de la localidad {a + 1} a la {b + 1} cuesta {c}, menos que {A}, y une dos grupos distintos: se construye. Llevamos {tot} en carreteras."
        elif d == "ciclo":
            nar = f"La carretera de la {a + 1} a la {b + 1} ya tiene sus dos extremos unidos: cerraría un ciclo, se descarta."
        else:
            nar = f"La carretera de la {a + 1} a la {b + 1} cuesta {c}, que no es menor que {A}. Como van ordenadas, las siguientes cuestan aún más: paramos."
        segs.append((s, nar, 0))
    return segs, pasos, grupos


def slide_final(titulo, ej, nombre_ej, texto):
    pasos, grupos = simula(ej)
    A = ej["A"]
    tot = pasos[-1][3]
    s = Slide(titulo, TEMA)
    s.box(24, 84, 600, 520, "recuento")
    s.text((56, 140), f"grupos que quedan:  {len(grupos)}", size=28, bold=True, color="gold")
    s.text((56, 190), "  ".join("{" + ",".join(map(str, g)) + "}" for g in grupos), size=26, mono=True)
    s.text((56, 260), f"aeropuertos = {len(grupos)}", size=26)
    s.text((56, 310), f"coste = {tot} + {len(grupos)} · {A}", size=26, mono=True)
    s.text((56, 370), f"{tot + len(grupos) * A}  {len(grupos)}", size=52, bold=True, color="gold")
    s.text((56, 440), "(coste mínimo, nº de aeropuertos)", size=19, color="muted")
    s.box(644, 84, 612, 520, nombre_ej)
    dibuja(s, ej, len(pasos), None, final=True)
    s.caption(texto, y=626)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 06-L", TEMA),
             "¿Dónde construimos los aeropuertos? Un problema de laboratorio del tema seis: es un Kruskal al que solo le dejamos construir las carreteras que de verdad compensan.", 0)]

    segs.append((ideas("El problema", [
        "N localidades (hasta 10.000) y M carreteras posibles de doble sentido, cada una con su coste. Puede haber varias entre el mismo par.",
        "Un aeropuerto cuesta A.",
        "Cada localidad debe tener aeropuerto o poder llegar por carretera a otra que lo tenga.",
        ("Salida: coste mínimo y número de aeropuertos. Si hay empate de coste, el que tenga MÁS aeropuertos.", "gold"),
    ]), "Tenemos localidades y carreteras posibles, cada una con su coste, y un aeropuerto cuesta A. Cada localidad debe tener un aeropuerto o poder llegar por carretera a otra que lo tenga. "
        "Hay que dar el coste mínimo y el número de aeropuertos, y si varias soluciones empatan en coste, la que tenga más aeropuertos.", 0))

    s = Slide("Grupos conexos, un aeropuerto por grupo", TEMA)
    s.box(40, 100, 1200, 200, "idea")
    s.text((70, 150), "coste  =  (carreteras construidas)  +  A · (nº de grupos)", size=34, mono=True, color="gold")
    s.text((70, 215), "Las carreteras construidas parten las localidades en grupos; cada grupo necesita un único aeropuerto.", size=22, color="muted")
    s.bullets(60, 330, 1160, [
        "Unir dos grupos con una carretera de coste C ahorra un aeropuerto, es decir, A.",
        ("Compensa solo si  C < A.", "gold"),
        "Es Kruskal: carreteras por coste creciente, descartando las que cierran ciclo.",
        "Pero se para en cuanto una carretera cuesta A o más: las siguientes cuestan aún más.",
    ], size=23, gap=16)
    segs.append((s, "La clave es que una solución es un conjunto de carreteras que parte las localidades en grupos conexos, con un único aeropuerto por grupo. "
                    "El coste es la suma de las carreteras construidas más A por el número de grupos. Unir dos grupos con una carretera de coste C ahorra un aeropuerto, que cuesta A, "
                    "así que solo compensa si C es menor que A. Es un Kruskal normal, pero que se detiene en cuanto una carretera cuesta A o más, porque las siguientes cuestan todavía más.", 0))

    s = Slide("El empate: C = A no se construye", TEMA)
    s.box(40, 100, 560, 300, "ejemplo 3: A = 50")
    dibuja(s, dict(EJ3, pos={0: (120, 340), 1: (320, 180), 2: (520, 340)}), 0)
    s.box(620, 100, 620, 300, "las dos soluciones")
    s.text((650, 150), "construir 2–3 (coste 50):", size=22, color="muted")
    s.text((650, 185), "20 + 50 + 1·50 = 120   → 1 aeropuerto", size=24, mono=True)
    s.text((650, 245), "no construirla:", size=22, color="muted")
    s.text((650, 280), "20 + 2·50 = 120   → 2 aeropuertos", size=24, mono=True, color="gold")
    s.bullets(60, 430, 1160, [
        "Mismo coste: el enunciado pide el que tenga MÁS aeropuertos.",
        ("Por eso la condición es estricta: C < A.  Con C = A se para.", "gold"),
    ], size=23, gap=14)
    segs.append((s, "Atención al empate. Si una carretera cuesta exactamente A, construirla cuesta lo mismo que el aeropuerto que se ahorra. "
                    "En el ejemplo tres, con A igual a cincuenta, construir la carretera da ciento veinte con un aeropuerto, y no construirla da ciento veinte con dos. "
                    "Como se piden más aeropuertos en caso de empate, no se construye: por eso la condición es estricta, C menor que A.", 0))

    s = Slide("El código", "EJ_06-L.cpp")
    s.code(24, 84, 800, 520, CODE, hl={L_ARI, L_ORD, L_BRK, L_UNI, L_AER, L_TOT}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["GrafoValorado + ponArista, restando 1 a las localidades.",
                              "sort: carreteras por coste creciente.",
                              "valor() >= A  ⇒  break.",
                              "Si no están unidos: unir y sumar el coste.",
                              "aeropuertos = cd.num_cjtos().",
                              "long long: el coste llega a ~2·10⁹."], size=19, gap=14)
    segs.append((s, "En el código se construye el grafo restando uno a cada localidad, se ordenan las carreteras por coste, y se recorren con un conjunto disjunto. "
                    "Si el coste es mayor o igual que A, se sale del bucle. Si los extremos no están unidos, se unen y se suma el coste. "
                    "Al final, el número de aeropuertos es el número de conjuntos que quedan, y el coste total se acumula en un long long, porque puede acercarse a dos mil millones.", 0))

    t1, p1, g1 = narra_traza("Ejemplo 1: Kruskal con C < A", EJ1, "ejemplo 1 · A = 100")
    segs += t1
    segs.append((slide_final("Ejemplo 1: resultado", EJ1, "ejemplo 1 · A = 100", "Todas las carreteras útiles se construyen: un solo grupo, un aeropuerto."),
                 "Queda un único grupo, así que un solo aeropuerto: sesenta de carreteras más cien del aeropuerto, ciento sesenta.", 0))

    t3, p3, g3 = narra_traza("Ejemplo 3: C = A", EJ3, "ejemplo 3 · A = 50")
    segs += t3
    segs.append((slide_final("Ejemplo 3: resultado", EJ3, "ejemplo 3 · A = 50", "La carretera de coste 50 no se construye: quedan 2 grupos, 2 aeropuertos."),
                 "Quedan dos grupos, así que dos aeropuertos: veinte de carretera más dos por cincuenta, ciento veinte con dos aeropuertos.", 0))

    segs.append((ideas("Detalles y coste", [
        "Varias carreteras entre el mismo par: Kruskal se queda con la más barata y descarta las demás como ciclo.",
        "N = 1: un grupo y un aeropuerto, coste A.",
        "Primera línea de cada caso: N M A, así que no sirve GrafoValorado(cin, 1): se usa ponArista.",
        "long long para el coste total.",
        ("Coste: O(M log M) por ordenar, más los conjuntos disjuntos.", "gold"),
    ]), "Algunos detalles. Varias carreteras entre el mismo par no molestan: Kruskal se queda con la más barata y descarta las demás. Con una sola localidad, un aeropuerto. "
        "Como la primera línea trae tres números, se añaden las aristas con ponArista. Y el coste está dominado por la ordenación.", 0))

    segs.append((cierre(NOMBRE, [
        "Kruskal solo con las carreteras de coste C < A.",
        "Se para al llegar a la primera con C ≥ A (están ordenadas).",
        "Un aeropuerto por cada grupo que queda: cd.num_cjtos().",
        "coste = carreteras + aeropuertos · A, en long long.",
        "Con C = A no se construye: se prefieren más aeropuertos.",
    ]), "Resumiendo: Kruskal solo con las carreteras más baratas que A, parando en la primera que no lo es. Un aeropuerto por cada grupo que queda, "
        "y el coste es el de las carreteras más aeropuertos por A. Con un empate, no se construye la carretera.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/06-L_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../06-L_aeropuertos.mp4")
        print(f"06-L: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
