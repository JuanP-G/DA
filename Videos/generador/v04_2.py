"""Vídeo EJ 04-2 · Los amigos de mis amigos son mis amigos"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line

CPP = "../../EJ_04-2/EJ_04-2.cpp"
NOMBRE = "Los amigos de mis amigos"

# caso 2 del enunciado; personas 1..10 -> vértices 0..9 (Grafo(cin, 1) resta 1)
ENTRADA = [(1, 2), (3, 1), (3, 4), (5, 4), (3, 5), (4, 6), (5, 2), (7, 10), (9, 10), (8, 9)]
N = 10
E = [(a - 1, b - 1) for a, b in ENTRADA]
LAB = {v: str(v + 1) for v in range(N)}
P = {0: (720, 170), 2: (835, 135), 3: (950, 175), 5: (985, 310), 4: (860, 285), 1: (735, 330),
     6: (1100, 145), 9: (1195, 205), 8: (1195, 320), 7: (1100, 360)}

L_FOR0 = find_line(CPP, "for (int v = 0; v < g.V(); ++v)")
L_NEW = find_line(CPP, "if (!visit[v])")
L_TAM = find_line(CPP, "int tam = dfs(g, v);")
L_MAX = find_line(CPP, "maxim = max(maxim, tam);")
L_DFS = find_line(CPP, "int dfs(")
L_VIS = find_line(CPP, "visit[v] = true;", L_DFS)
L_T1 = find_line(CPP, "int tam = 1;")
L_REC = find_line(CPP, "if (!visit[w]) tam += dfs(g, w);")
L_RET = find_line(CPP, "return tam;")
CODE = code_lines(CPP, find_line(CPP, "class MaximaCompConexa"), find_line(CPP, "};", L_DFS))
COMP_COL = ["blue", "purple", "green"]


def traza():
    a = [[] for _ in range(N)]
    for v, w in E:
        a[v].append(w)
        a[w].append(v)
    visit = [False] * N
    comp = [None] * N
    pasos = []
    st = dict(maxim=0, c=-1)
    pila = []

    def snap(tipo, v, extra=None):
        pasos.append((tipo, v, extra, comp[:], pila[:], st["maxim"]))

    def dfs(v):
        visit[v] = True
        comp[v] = st["c"]
        pila.append(v)
        snap("entra", v)
        tam = 1
        for w in a[v]:
            if not visit[w]:
                tam += dfs(w)
        snap("devuelve", v, tam)
        pila.pop()
        return tam

    for v in range(N):
        if not visit[v]:
            st["c"] += 1
            snap("nueva", v)
            tam = dfs(v)
            st["maxim"] = max(st["maxim"], tam)
            snap("max", v, tam)
    return pasos


def slide_paso(k, n, tipo, v, extra, comp, pila, maxim, hl, cap):
    s = Slide("Ejecución · Caso 2", f"paso {k} de {n}")
    s.code(24, 84, 610, 520, CODE, hl=hl, title="class MaximaCompConexa")
    s.box(652, 84, 604, 330, "grafo (personas 1..10)")
    ns = {u: (COMP_COL[c], "node_t", None) for u, c in enumerate(comp) if c is not None}
    for u in pila:
        ns[u] = ("gold", "node_t", None)
    if v is not None:
        ns[v] = (ns.get(v, ("node",))[0], "node_t", "text")
    es = {}
    for i in range(1, len(pila)):
        es[(pila[i - 1], pila[i])] = ("gold", 5)
    s.graph(P, E, ns=ns, es=es, labels=LAB)
    s.box(652, 430, 604, 174, "estado")
    s.text((672, 470), "pila de llamadas", size=17, color="muted", bold=True)
    s.text((850, 469), " → ".join(f"dfs({u + 1})" for u in pila) if pila else "vacía", size=17, bold=True)
    tams = {}
    for c in comp:
        if c is not None:
            tams[c] = tams.get(c, 0) + 1
    s.text((672, 520), "maxim", size=17, color="muted", bold=True)
    s.pill(760, 512, str(maxim), fill="gold")
    x = 850
    for c, t in sorted(tams.items()):
        x = s.pill(x, 512, f"comp {c + 1}: {t} visitados", fill=COMP_COL[c], size=16) + 10
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-2", "son mis amigos · Tema 4 · Grafos no dirigidos"),
             "Los amigos de mis amigos son mis amigos. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    s = Slide("El problema")
    s.box(60, 90, 620, 400, "caso 2: 10 personas, 10 amistades")
    s.graph({v: (x - 600, y + 40) for v, (x, y) in P.items()}, E, labels=LAB)
    s.bullets(720, 120, 500, [
        "Si A y B son amigos, y B y C también, entonces A y C son amigos.",
        "Hay que contar las personas del grupo de amigos más grande.",
        "Una pareja puede repetirse (2 3 y 3 2): sigue siendo una sola amistad.",
    ], size=22)
    segs.append((s, "Tenemos personas y parejas de amigos. Por el refrán, si A es amigo de B y B de C, entonces A y C también son amigos. "
                    "Nos piden cuántas personas tiene el grupo de amigos más grande.", 0))

    s = Slide("Cómo se plantea")
    s.box(60, 90, 620, 400, "grupo de amigos = componente conexa")
    s.graph({v: (x - 600, y + 40) for v, (x, y) in P.items()}, E, labels=LAB,
            ns={v: ("blue" if v < 6 else "purple", "node_t", None) for v in range(N)})
    s.bullets(720, 120, 500, [
        "Persona → vértice.  Amistad → arista.",
        "A y C son amigos ⇔ hay un CAMINO entre ellos.",
        "Un grupo de amigos es una COMPONENTE CONEXA.",
        ("Respuesta = tamaño de la componente conexa más grande.", "gold"),
    ], size=22)
    s.caption("Componentes: {1,2,3,4,5,6} → 6     {7,8,9,10} → 4     ⇒  6", y=540)
    segs.append((s, "Lo modelamos como un grafo: cada persona es un vértice y cada amistad una arista. "
                    "Que el amigo de mi amigo sea mi amigo significa que estamos en el mismo grupo si hay un camino entre nosotros.", 0))
    segs.append((s, "Es decir, un grupo de amigos es exactamente una componente conexa. "
                    "Y lo que nos piden es el tamaño de la componente conexa más grande. En este ejemplo hay dos, de seis y de cuatro personas: la respuesta es seis.", 0))

    segs.append((ideas("El algoritmo", [
        "Recorro los vértices en orden. Si v NO está visitado, empieza una componente nueva.",
        "Lanzo un dfs desde v que visita toda su componente y DEVUELVE cuántos vértices ha visitado.",
        "Me quedo con el máximo de esos tamaños.",
        "visit es compartido: cada vértice se visita UNA vez en total, aunque haya muchas componentes.",
    ], note="Las parejas repetidas no molestan: el dfs nunca entra dos veces en un vértice ya visitado."),
        "El algoritmo es el clásico de componentes conexas. Recorro los vértices en orden y, cuando encuentro uno sin visitar, "
        "empieza una componente nueva. Lanzo un D F S desde él, que visita toda la componente y devuelve cuántos vértices ha visitado. "
        "Me quedo con el máximo.", 0))
    segs.append((segs[-1][0], "Como el vector de visitados es compartido, cada vértice se visita una sola vez en total. "
                              "Y las parejas repetidas no molestan, porque el recorrido nunca vuelve a entrar en un vértice ya visitado.", 0))

    s = Slide("El código", "EJ_04-2.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_NEW, L_TAM, L_MAX, L_T1, L_REC, L_RET}, title="class MaximaCompConexa")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, [
        "El constructor recorre todos los vértices y lanza dfs en los no visitados.",
        "dfs empieza contando el propio v (tam = 1).",
        "Suma lo que devuelve cada llamada a un vecino nuevo.",
        "Grafo(cin, 1) pasa las personas de 1..N a 0..N-1.",
    ], size=20, gap=16)
    segs.append((s, "En el código, la función dfs empieza con tamaño uno, el propio vértice, y le suma lo que devuelve cada llamada "
                    "a un vecino que aún no está visitado. Así, la llamada inicial devuelve el tamaño de toda la componente. "
                    "Las personas van de uno a ene, y el constructor del grafo con un uno les resta uno al leerlas.", 0))

    pasos = traza()
    n = len(pasos)
    for k, (tipo, v, extra, comp, pila, maxim) in enumerate(pasos, 1):
        if tipo == "nueva":
            hl, cap = {L_FOR0, L_NEW}, f"La persona {v + 1} no está visitada: empieza una componente nueva"
            nar = f"La persona {v + 1} no está visitada, así que empieza una componente nueva. Lanzamos dfs desde ella."
        elif tipo == "entra":
            hl, cap = {L_VIS, L_T1}, f"dfs({v + 1}): marcamos {v + 1}, tam empieza en 1"
            nar = f"Entramos en el {v + 1} y lo marcamos."
        elif tipo == "devuelve":
            hl = {L_RET}
            cap = f"dfs({v + 1}) devuelve {extra}"
            nar = (f"El {v + 1} no tiene más vecinos nuevos: devuelve {extra}." if extra > 1 else
                   f"El {v + 1} no tiene vecinos nuevos: devuelve uno.")
        else:
            hl, cap = {L_TAM, L_MAX}, f"La componente tiene {extra} personas → maxim = {maxim}"
            nar = f"La componente tiene {extra} personas. El máximo pasa a ser {maxim}."
        segs.append((slide_paso(k, n, tipo, v if tipo != "max" else None, extra, comp, pila, maxim, hl, cap), nar, 0))

    s = Slide("Resultado · Caso 2")
    s.graph({v: (x - 300, y + 40) for v, (x, y) in P.items()}, E, labels=LAB,
            ns={v: ("blue" if v < 6 else "purple", "node_t", None) for v in range(N)})
    s.caption("Componentes de 6 y 4 personas   ⇒   se escribe 6", y=500)
    segs.append((s, "Al terminar el recorrido hemos visto dos componentes, de seis y de cuatro personas. La respuesta es seis.", 0))

    segs.append((cierre(NOMBRE, [
        "Grupo de amigos = componente conexa.",
        "Un dfs por cada vértice no visitado; el dfs devuelve el tamaño de su componente.",
        "Respuesta: el máximo de esos tamaños.",
        "Coste: O(N + M) por caso.",
        ("Ojo: el dfs recursivo puede bajar hasta N = 20.000 niveles (en Visual Studio podría desbordar la pila).", "muted"),
    ]), "Resumiendo: un grupo de amigos es una componente conexa. Lanzamos un D F S por cada vértice no visitado, "
        "cada uno devuelve el tamaño de su componente y nos quedamos con el máximo. El coste es lineal en personas más amistades.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-2_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-2_amigos_de_mis_amigos.mp4")
        print(f"04-2: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
