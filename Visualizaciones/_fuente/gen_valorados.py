#!/usr/bin/env python3
"""
Genera tema6-kruskal.frag.html y tema7-dijkstra.frag.html a partir de valorado.tpl.html.
El código C++ que muestran las páginas se LEE de los ficheros reales del repositorio
(Estructuras de datos/*.h y las soluciones EJ_*), para que nunca se desincronice.

    python3 gen_valorados.py && python3 build.py
"""
import json, pathlib, re, sys

AQUI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AQUI))
from gen_grafos import leer, bloque_clase, quita_bloque, sin_doc, li, fila  # noqa: E402

TPL = (AQUI / "valorado.tpl.html").read_text(encoding="utf-8")
TEMA6 = "6-Conjuntos disjuntos y grafos valorados"
TEMA7 = "7-Digrafos valorados y caminos minimos"


def js(nombre):
    return (AQUI / nombre).read_text(encoding="utf-8")


def con_template(lineas, nombre):
    """Clase de plantilla: la línea 'template <...>' que la precede."""
    ini = next(i for i, l in enumerate(lineas) if re.match(rf"\s*class {nombre}\b", l))
    pre = [lineas[ini - 1]] if ini and lineas[ini - 1].lstrip().startswith("template") else []
    return pre + bloque_clase(lineas, nombre)


def clase_tpl(ruta, nombre, quitar=()):
    c = sin_doc(con_template(leer(ruta), nombre))
    for patron, repl in quitar:
        c = quita_bloque(c, patron, repl)
    return c


def funcion(ruta, firma):
    ls = leer(ruta)
    ini = next(i for i, l in enumerate(ls) if firma in l)
    fin = next(i for i in range(ini, len(ls)) if ls[i].rstrip() == "}")
    return ls[ini:fin + 1]


def cd_pc():
    """ConjuntosDisjuntos.h sin las funciones de depuración."""
    ls = leer("Estructuras de datos/ConjuntosDisjuntos.h")
    ini = next(i for i, l in enumerate(ls) if l.startswith("class ConjuntosDisjuntos"))
    fin = next(i for i, l in enumerate(ls) if "escritura para depurar" in l)
    c = [l for l in ls[ini:fin]]
    while c and not c[-1].strip():
        c.pop()
    return c + ["};"]


def sin_comentarios_de_linea(ls):
    return [l for l in ls if l.strip() != "//"]


def pagina(plantilla_extra):
    s = TPL
    for k in sorted(plantilla_extra, key=len, reverse=True):
        s = s.replace(f"@@{k}@@", plantilla_extra[k])
    assert "@@" not in s, re.findall(r"@@\w+@@", s)
    return s


LEG_COMUN = (
    '<span><b style="border-color:var(--accent);background:var(--accent-soft)"></b>arista / vértice actual</span>'
    '<span><b style="border-color:var(--blue);background:var(--blue-soft)"></b>arista aceptada · vértice en el árbol</span>'
    '<span><b style="border-color:var(--red);background:var(--red-soft)"></b>arista descartada</span>'
    '<span><b style="border-color:var(--green);background:var(--green-soft)"></b>resultado final</span>'
    '<span><b style="border-color:var(--line);background:var(--bg);opacity:.5"></b>no se mira / no vale</span>'
)

# ----------------------------------------------------------------------------------------------- tema 6
def tema6():
    qf = clase_tpl("Estructuras de datos/ConjuntosDisjuntos_variantes.h", "BusquedaRapida")
    qu = clase_tpl("Estructuras de datos/ConjuntosDisjuntos_variantes.h", "UnionRapida")
    sz = clase_tpl("Estructuras de datos/ConjuntosDisjuntos_variantes.h", "UnionPorTamanos")
    lab_codes = {
        "qf": {"f": "ConjuntosDisjuntos_variantes.h · BusquedaRapida", "lines": qf},
        "qu": {"f": "ConjuntosDisjuntos_variantes.h · UnionRapida", "lines": qu},
        "sz": {"f": "ConjuntosDisjuntos_variantes.h · UnionPorTamanos", "lines": sz},
        "pc": {"f": "ConjuntosDisjuntos.h (resumen)", "lines": cd_pc()},
    }
    clase = clase_tpl("Estructuras de datos/GrafoValorado.h", "GrafoValorado",
                      [("(std::istream & flujo", "// ... constructor desde un flujo de entrada omitido"), ("void print(", "// ... print() omitido")])
    arista = clase_tpl("Estructuras de datos/GrafoValorado.h", "Arista", [("void print(", "// ... print() omitido")])
    codes = {
        "clase": {"f": "GrafoValorado.h (resumen)", "tab": "GrafoValorado.h", "lines": clase},
        "arista": {"f": "GrafoValorado.h · Arista", "tab": "Arista", "lines": arista},
        "kruskal": {"f": "GrafoValorado_algoritmos.h · ARM_Kruskal", "tab": "ARM_Kruskal", "lines": clase_tpl("Estructuras de datos/GrafoValorado_algoritmos.h", "ARM_Kruskal")},
        "prim": {"f": "GrafoValorado_algoritmos.h · ARM_Prim", "tab": "ARM_Prim", "lines": clase_tpl("Estructuras de datos/GrafoValorado_algoritmos.h", "ARM_Prim")},
        "e63": {"f": "EJ_06-3.cpp", "tab": "06-3", "lines": funcion(f"{TEMA6}/EJ_06-3/EJ_06-3.cpp", "void resuelveCaso()")},
        "e64": {"f": "EJ_06-4.cpp", "tab": "06-4", "lines": funcion(f"{TEMA6}/EJ_06-4/EJ_06-4.cpp", "bool resuelveCaso()")},
        "e65": {"f": "EJ_06-5.cpp", "tab": "06-5", "lines": funcion(f"{TEMA6}/EJ_06-5/EJ_06-5.cpp", "void resuelveCaso()")},
        "e6L": {"f": "EJ_06-L.cpp", "tab": "06-L", "lines": funcion(f"{TEMA6}/EJ_06-L/EJ_06-L.cpp", "void resuelveCaso()")},
        "e62": {"f": "EJ_06-2.cpp", "tab": "06-2", "lines": clase_tpl(f"{TEMA6}/EJ_06-2/EJ_06-2.cpp", "Alcanzables")},
    }
    algo_list = [
        {"id": "kr_clase", "nombre": "Kruskal: árbol de coste mínimo (ARM_Kruskal)", "src": False, "dst": False, "code": "kruskal"},
        {"id": "prim", "nombre": "Prim: crecer el árbol desde el vértice 0 (ARM_Prim)", "src": False, "dst": False, "code": "prim"},
        {"id": "kr_suma", "nombre": "06-3 Archipiélago: suma del ARM o «No hay puentes suficientes»", "src": False, "dst": False, "code": "e63"},
        {"id": "kr_ultima", "nombre": "06-4 Tarzán: última arista aceptada o «Imposible»", "src": False, "dst": False, "code": "e64"},
        {"id": "kr_minimax", "nombre": "06-5 Trajano: Kruskal hasta unir origen y destino", "src": True, "dst": True, "code": "e65"},
        {"id": "kr_aero", "nombre": "06-L Aeropuertos: Kruskal solo con carreteras C < A, un aeropuerto por grupo", "src": False, "dst": False, "par": "A", "code": "e6L"},
        {"id": "dfsancho", "nombre": "06-2 Camiones: DFS que solo usa aristas con valor ≥ ancho", "src": True, "dst": True, "par": "ancho", "code": "e62"},
    ]
    p = lambda n, nombre, e, **kw: dict(nombre=nombre, n=n, e=e, **kw)
    presets = [
        p(6, "El grafo del vídeo del tema (6 vértices)", [[4, 5, 2], [0, 2, 3], [3, 4, 4], [1, 3, 5], [3, 5, 6], [2, 3, 7], [0, 1, 8], [2, 4, 9], [1, 2, 10]],
          algo="kr_clase", src=0, dst=5, pos=[[110, 150], [110, 330], [290, 90], [300, 260], [480, 160], [500, 350]]),
        p(4, "06-3 · Archipiélago (ejemplo 1: 4 islas, 5 puentes)", [[0, 1, 5], [0, 2, 10], [1, 3, 7], [0, 3, 8], [2, 3, 2]],
          algo="kr_suma", src=0, dst=3, pos=[[130, 90], [130, 330], [500, 90], [500, 330]]),
        p(4, "06-3 · No hay puentes suficientes (ejemplo 2)", [[0, 1, 3], [1, 3, 5], [3, 0, 8]],
          algo="kr_suma", src=0, dst=3, pos=[[120, 100], [320, 100], [540, 250], [220, 320]]),
        p(4, "06-4 · La selva de Tarzán (ejemplo 1)", [[0, 1, 5], [1, 2, 10], [2, 0, 7], [1, 3, 8]],
          algo="kr_ultima", src=0, dst=3, pos=[[130, 110], [330, 210], [130, 320], [540, 110]]),
        p(4, "06-5 · Las minas de Trajano (ejemplo 1: de la cámara 1 a la 4)", [[0, 1, 2], [1, 3, 5], [3, 0, 10], [0, 2, 6]],
          algo="kr_minimax", src=0, dst=3, pos=[[130, 210], [320, 90], [320, 340], [520, 210]]),
        p(4, "06-L · Aeropuertos (ejemplo 1: A = 100)", [[0, 1, 10], [1, 2, 30], [3, 0, 40], [3, 2, 20]],
          algo="kr_aero", src=0, dst=3, par=100, pos=[[130, 100], [500, 100], [500, 330], [130, 330]]),
        p(3, "06-L · Aeropuertos (ejemplo 3: C = A no se construye)", [[0, 1, 20], [1, 2, 50], [0, 2, 80]],
          algo="kr_aero", src=0, dst=2, par=50, pos=[[130, 210], [330, 90], [530, 210]]),
        p(5, "06-2 · Camiones de reparto (ejemplo: de la 2 a la 5 con ancho 15)", [[0, 1, 10], [0, 2, 30], [1, 3, 20], [2, 3, 15], [3, 4, 12]],
          algo="dfsancho", src=1, dst=4, par=15, pos=[[100, 210], [260, 90], [260, 330], [430, 210], [570, 210]]),
        p(7, "Un grafo con ciclos (Kruskal descarta varias aristas)", [[0, 1, 7], [0, 3, 5], [1, 2, 8], [1, 3, 9], [1, 4, 7], [2, 4, 5], [3, 4, 15], [3, 5, 6], [4, 5, 8], [4, 6, 9], [5, 6, 11]],
          algo="kr_clase", src=0, dst=6, pos=[[90, 120], [250, 70], [450, 70], [170, 280], [340, 190], [330, 350], [540, 300]]),
    ]
    ideas = "\n".join([
        li("Una partición que solo sabe juntar", "Los elementos están repartidos en conjuntos disjuntos y la única operación que cambia algo es <code>unir(a, b)</code>. Sirve cuando una relación solo <b>crece</b>: celdas de petróleo que se añaden (06-1), aristas que Kruskal acepta (06-3, 06-4, 06-5)."),
        li("Búsqueda rápida frente a unión rápida", "Con el vector <code>id[]</code>, <code>buscar</code> cuesta 1 pero <code>unir</code> cuesta N. Con árboles es al revés: <code>unir</code> cambia un enlace, pero <code>buscar</code> sube por el árbol, que puede ser una <b>cadena</b> de N nodos. Prueba «Peor caso: cadena»."),
        li("Por tamaños y con compresión", "Colgar siempre el árbol pequeño del grande mantiene la altura ≤ log₂N. Comprimir caminos deja cada nodo visitado colgando de la raíz. Juntas: M operaciones en O(N + M·lg*N), que en la práctica es lineal. Es <code>ConjuntosDisjuntos.h</code>."),
        li("Propiedad del corte", "Si repartes los vértices en dos grupos, la arista <b>más barata</b> que cruza de un grupo a otro pertenece a algún árbol de recubrimiento mínimo. Kruskal y Prim son dos formas de ir aplicándola."),
        li("Kruskal = ordenar + partición", "Ordena las aristas por valor y recórrelas: si sus extremos ya están unidos cerrarían un <b>ciclo</b> y se descartan; si no, se aceptan y se unen. <code>unidos</code> detecta el ciclo en casi O(1). Coste O(A log A)."),
        li("Prim = crecer un árbol", "Parte de un vértice y repite: toma de la cola de prioridad la arista más barata que sale del árbol. Si sus dos extremos ya están dentro, sobra. Mismo coste mínimo que Kruskal (el árbol puede cambiar si hay valores repetidos)."),
        li("Un mismo bucle, tres preguntas", "<b>06-3</b>: suma de los valores aceptados. <b>06-4</b>: valor de la <i>última</i> arista aceptada (el máximo del ARM). <b>06-5</b>: parar en cuanto <code>unidos(origen, destino)</code>; esa arista es el mejor camino «de cuello de botella»."),
        li("Cuando no hace falta ARM", "En 06-2 solo se pregunta si <b>se puede llegar</b> usando aristas con valor ≥ ancho. Basta un DFS que ignora las demás; Kruskal solo compensa si hay muchísimas consultas."),
    ])
    tabla = "\n".join([
        fila("06-1", "Petroleros hundidos", "Conjuntos disjuntos sobre las celdas (8 vecinos): <code>unir</code> y <code>cardinal</code>"),
        fila("06-2", "Camiones de reparto", "<code>GrafoValorado</code> + DFS por consulta con umbral de anchura"),
        fila("06-3", "Recorriendo el archipiélago en bicicleta", "Kruskal: suma del ARM o «No hay puentes suficientes»"),
        fila("06-4", "La selva de Tarzán", "Kruskal: la última arista aceptada es la cuerda mínima"),
        fila("06-5", "Las minas del emperador Trajano", "Kruskal hasta que origen y destino quedan unidos"),
    ])
    tabs = '  <nav class="tabs" aria-label="Secciones"><button class="btn on" data-t="lab">① Conjuntos disjuntos</button><button class="btn" data-t="graf">② Grafo valorado · Kruskal y Prim</button></nav>'
    lab_js = ("const LAB_CODES = " + json.dumps(lab_codes, ensure_ascii=False) + ";\n" + js("lab_dsu.js") + "\nlabReinit(10);\n")
    return pagina({
        "TITULO": "Conjuntos disjuntos y Kruskal", "TEMA": "6", "H1": "Conjuntos disjuntos, grafos valorados y árbol de recubrimiento mínimo",
        "LEDE": "Primero una partición que solo sabe juntar conjuntos (cuatro implementaciones, de la más lenta a la del juez); después un grafo no dirigido con valores en las aristas, donde Kruskal y Prim encuentran el árbol de coste mínimo. Todo se ejecuta paso a paso sobre el código real.",
        "GRAFO": "grafo valorado", "GRAFO_H2": "Grafo valorado (arrastra los vértices)", "HEADER": "<code>ConjuntosDisjuntos.h</code> y <code>GrafoValorado.h</code>", "DIR": "false",
        "PASO1": "1", "PASO2": "2", "EXTRA_CSS": "", "TABS_HTML": tabs, "LAB_HTML": (AQUI / "lab_dsu.html").read_text(encoding="utf-8"),
        "IDEAS": ideas, "TABLA": tabla,
        "PRESETS": json.dumps(presets, ensure_ascii=False), "CODES": json.dumps(codes, ensure_ascii=False), "ALGO_LIST": json.dumps(algo_list, ensure_ascii=False),
        "ALGOS": js("valorado_algos_t6.js"), "LEGEND": json.dumps(LEG_COMUN, ensure_ascii=False),
        "PESO_RND": "pesos[pi++]",
        "L_PON1": "L('clase','if (v < 0'),L('clase','throw'),L('clase','++_A')",
        "L_PON2": "L('clase','_ady[v].push_back(arista)')", "L_PON3": "L('clase','_ady[w].push_back(arista)')",
        "LAB_INIT": lab_js, "LAB_START": "mostrarTab(location.hash === '#graf' ? 'graf' : 'lab');",
        "EXPORTS": "DSU, LAB, labUnir, Grid, gridAdd, kruskal",
    })


# ----------------------------------------------------------------------------------------------- tema 7
def tema7():
    clase = clase_tpl("Estructuras de datos/DigrafoValorado.h", "DigrafoValorado",
                      [("(std::istream & flujo", "// ... constructor desde un flujo de entrada omitido"), ("void print(", "// ... print() omitido")])
    arista = clase_tpl("Estructuras de datos/DigrafoValorado.h", "AristaDirigida", [("void print(", "// ... print() omitido")])
    ej = lambda n, sig="void resuelveCaso()": funcion(f"{TEMA7}/EJ_07-{n}/EJ_07-{n}.cpp", sig)
    codes = {
        "clase": {"f": "DigrafoValorado.h (resumen)", "tab": "DigrafoValorado.h", "lines": clase},
        "arista": {"f": "DigrafoValorado.h · AristaDirigida", "tab": "AristaDirigida", "lines": arista},
        "dijkstra": {"f": "DigrafoValorado_algoritmos.h · Dijkstra", "tab": "Dijkstra", "lines": clase_tpl("Estructuras de datos/DigrafoValorado_algoritmos.h", "Dijkstra")},
        "dijkstra_vec": {"f": "DigrafoValorado_algoritmos.h · DijkstraVector", "tab": "Dijkstra con vector", "lines": clase_tpl("Estructuras de datos/DigrafoValorado_algoritmos.h", "DijkstraVector")},
        "e71": {"f": "EJ_07-1.cpp", "tab": "07-1", "lines": ej(1)},
        "e72": {"f": "EJ_07-2.cpp", "tab": "07-2", "lines": ej(2)},
        "e73": {"f": "EJ_07-3.cpp", "tab": "07-3", "lines": ej(3)},
    }
    algo_list = [
        {"id": "dij_pq", "nombre": "Dijkstra con IndexPQ: caminos mínimos desde un origen (Dijkstra)", "src": True, "dst": False, "code": "dijkstra"},
        {"id": "dij_vec", "nombre": "Dijkstra con vector, sin cola de prioridad (DijkstraVector, O(V²))", "src": True, "dst": False, "code": "dijkstra_vec"},
        {"id": "e71", "nombre": "07-1 Navegando sin teclado: enlace + carga de la página", "src": True, "dst": True, "txt": "cargas", "code": "e71"},
        {"id": "e72", "nombre": "07-2 Camino al cole: contar caminos mínimos (calles de doble sentido)", "src": True, "dst": True, "undir": True, "code": "e72"},
        {"id": "e73", "nombre": "07-3 RapidEats: tiempo y ruta con ulti[] (tramos de doble sentido)", "src": True, "dst": True, "undir": True, "code": "e73"},
    ]
    p = lambda n, nombre, e, **kw: dict(nombre=nombre, n=n, e=e, **kw)
    slides = [[0, 1, 5], [0, 7, 8], [0, 4, 9], [1, 3, 15], [1, 2, 12], [1, 7, 4], [7, 2, 7], [7, 5, 6], [4, 7, 5], [4, 5, 4], [4, 6, 20], [5, 2, 1], [5, 6, 13], [2, 3, 3], [2, 6, 11], [3, 6, 9]]
    pos_slides = [[144, 202], [275, 165], [415, 245], [479, 164], [145, 356], [341, 313], [546, 361], [275, 246]]
    presets = [
        p(8, "El digrafo de las transparencias (8 vértices)", slides, algo="dij_pq", src=0, dst=6, pos=pos_slides),
        p(8, "El mismo digrafo con Dijkstra con vector", slides, algo="dij_vec", src=0, dst=6, pos=pos_slides),
        p(3, "¿Árbol de caminos mínimos = ARM? (triángulo)", [[0, 1, 2], [1, 2, 2], [0, 2, 3]], algo="dij_pq", src=0, dst=2, pos=[[110, 300], [320, 110], [530, 300]]),
        p(4, "07-1 · Navegando sin teclado (ejemplo 1: 53)", [[0, 1, 10], [0, 2, 20], [0, 3, 100], [1, 3, 20], [2, 3, 20]], algo="e71", src=0, dst=3, txt="10 5 15 8", pos=[[80, 210], [270, 90], [270, 330], [520, 210]]),
        p(4, "07-1 · Navegando sin teclado (ejemplo 2: IMPOSIBLE)", [[0, 1, 10], [0, 2, 20], [1, 2, 40], [3, 1, 10]], algo="e71", src=0, dst=3, txt="10 5 15 8", pos=[[80, 210], [270, 90], [270, 330], [520, 210]]),
        p(7, "07-2 · Camino al cole (ejemplo 1: 4 formas)", [[0, 1, 5], [0, 2, 7], [1, 3, 10], [2, 3, 8], [1, 4, 30], [3, 4, 12], [3, 6, 25], [3, 5, 11], [4, 6, 13], [5, 6, 30]], algo="e72", src=0, dst=6, pos=[[60, 210], [190, 90], [190, 330], [320, 210], [450, 90], [450, 330], [580, 210]]),
        p(4, "07-3 · RapidEats (ejemplo 1: del punto 4 al 1)", [[0, 1, 15], [0, 2, 30], [1, 2, 20], [3, 2, 10]], algo="e73", src=3, dst=0, pos=[[120, 210], [300, 90], [330, 300], [540, 300]]),
    ]
    ideas = "\n".join([
        li("Relajar una arista", "Si ir por <code>v → w</code> mejora el camino más corto conocido hasta <code>w</code> (<code>dist[v] + valor &lt; dist[w]</code>), se actualizan <code>dist[w]</code> y <code>ulti[w]</code>. Todo el tema es repetir esto en un orden inteligente."),
        li("Dijkstra: el más cercano primero", "Con valores <b>≥ 0</b>, el vértice de menor <code>dist</code> que aún no se ha tratado ya no puede mejorar: su distancia es <b>definitiva</b>. Se saca de la cola de prioridad y se relajan sus aristas salientes. Cada arista se relaja <b>una vez</b>."),
        li("Por qué O(A log V)", "V <code>pop</code> y como mucho A <code>update</code>, cada uno de coste log V (la <code>IndexPQ</code> del tema 3 permite cambiar la prioridad de un vértice que ya está en la cola)."),
        li("Con un vector en vez de cola", "Si en cada paso se recorre <code>dist</code> buscando el mínimo no tratado, el coste baja a O(V² + A). Peor en grafos dispersos, <b>mejor en los densos</b> (A ≈ V²). Compara los accesos al vector con «Dijkstra con vector»."),
        li("El camino, hacia atrás", "<code>ulti[v]</code> guarda la <b>última arista</b> del camino mínimo hasta <code>v</code>. Para escribir el camino se retrocede desde el destino hasta el origen y se meten los vértices por delante (07-3)."),
        li("Caminos mínimos ≠ ARM", "El árbol de caminos mínimos depende del <b>origen</b> y minimiza la distancia a cada vértice; el ARM no depende de él y minimiza la <b>suma</b> de las aristas. En el triángulo de ejemplo salen costes distintos: 5 frente a 4."),
        li("07-1: coste también en los vértices", "Se suma la carga de la página a la arista que <b>entra</b> en ella y la de la página inicial a <code>dist[origen]</code>: así hay un solo tipo de coste y vale Dijkstra tal cual."),
        li("07-2: contar caminos mínimos", "Con un segundo vector <code>formas[]</code>: si <code>dist[w]</code> mejora, <code>formas[w] = formas[v]</code>; si empata, <code>formas[w] += formas[v]</code>. Las aristas azules son las que aparecen en algún camino mínimo."),
    ])
    tabla = "\n".join([
        fila("07-1", "Navegando sin teclado", "Dijkstra con coste en vértices y aristas: <code>t + carga[w]</code> y <code>dist[0] = carga[0]</code>"),
        fila("07-2", "Camino al cole", "Dijkstra que cuenta caminos mínimos (sustituir si mejora, sumar si empata)"),
        fila("07-3", "RapidEats con ruta", "Dijkstra por pedido y reconstrucción de la ruta con <code>ulti[]</code>"),
    ])
    return pagina({
        "TITULO": "Dijkstra y caminos mínimos", "TEMA": "7", "H1": "Dígrafos valorados y caminos de coste mínimo",
        "LEDE": "Un dígrafo con un valor en cada arista y el algoritmo de Dijkstra: relajación de aristas, cola de prioridad variable (y la variante con un simple vector), árbol de caminos mínimos y las variantes de los ejercicios (cargas en los vértices, contar caminos y escribir la ruta). Todo paso a paso sobre el código real.",
        "GRAFO": "dígrafo valorado", "GRAFO_H2": "Dígrafo valorado (arrastra los vértices)", "HEADER": "<code>DigrafoValorado.h</code> y <code>IndexPQ.h</code>", "DIR": "true",
        "PASO1": "1", "PASO2": "2", "EXTRA_CSS": "", "TABS_HTML": "", "LAB_HTML": "",
        "IDEAS": ideas, "TABLA": tabla,
        "PRESETS": json.dumps(presets, ensure_ascii=False), "CODES": json.dumps(codes, ensure_ascii=False), "ALGO_LIST": json.dumps(algo_list, ensure_ascii=False),
        "ALGOS": js("valorado_algos_t7.js"),
        "LEGEND": json.dumps(
            '<span><b style="border-color:var(--accent);background:var(--accent-soft)"></b>arista que se relaja / vértice que sale de la cola</span>'
            '<span><b style="border-color:var(--blue);background:var(--blue-soft)"></b>arista de <code>ulti[]</code> (mejor camino conocido)</span>'
            '<span><b style="border-color:var(--purple);background:var(--purple-soft)"></b>vértice en la cola</span>'
            '<span><b style="border-color:var(--green);background:var(--green-soft)"></b>distancia definitiva / árbol final</span>'
            '<span><b style="border-color:var(--red);background:var(--red-soft)"></b>destino no alcanzable</span>', ensure_ascii=False),
        "PESO_RND": "pesos[pi++]",
        "L_PON1": "L('clase','if (v < 0'),L('clase','throw'),L('clase','++_A')",
        "L_PON2": "L('clase','_ady[v].push_back(arista)')", "L_PON3": "0",
        "LAB_INIT": "", "LAB_START": "mostrarTab('graf');",
        "EXPORTS": "dijkstra",
    })


if __name__ == "__main__":
    (AQUI / "tema6-kruskal.frag.html").write_text(tema6(), encoding="utf-8")
    (AQUI / "tema7-dijkstra.frag.html").write_text(tema7(), encoding="utf-8")
    print("ok")
