#!/usr/bin/env python3
"""
Genera tema4-grafo.frag.html y tema5-digrafo.frag.html a partir de grafo.tpl.html.
El código C++ que muestran las páginas se LEE de los ficheros reales del repositorio
(Estructuras de datos/*.h y las soluciones EJ_*), para que nunca se desincronice.

    python3 gen_grafos.py && python3 build.py
"""
import json, pathlib, re

AQUI = pathlib.Path(__file__).parent
RAIZ = AQUI.parent.parent
TPL = (AQUI / "grafo.tpl.html").read_text(encoding="utf-8")


def leer(ruta):
    return (RAIZ / ruta).read_text(encoding="utf-8").splitlines()


def bloque_clase(lineas, nombre):
    """Líneas desde 'class nombre' hasta el '};' que la cierra."""
    ini = next(i for i, l in enumerate(lineas) if re.match(rf"\s*class {nombre}\b", l))
    fin = next(i for i in range(ini, len(lineas)) if lineas[i].rstrip() == "};")
    return lineas[ini:fin + 1]


def quita_bloque(lineas, patron, reemplazo):
    """Quita el método cuya primera línea contiene 'patron' (hasta su '}' con la misma sangría)."""
    i = next(k for k, l in enumerate(lineas) if patron in l)
    sang = len(lineas[i]) - len(lineas[i].lstrip())
    j = next(k for k in range(i, len(lineas)) if lineas[k].rstrip() == " " * sang + "}")
    return lineas[:i] + [" " * sang + reemplazo] + lineas[j + 1:]


def sin_doc(lineas):
    out, dentro = [], False
    for l in lineas:
        t = l.strip()
        if dentro:
            if "*/" in t:
                dentro = False
            continue
        if t.startswith("/**"):
            if "*/" not in t:
                dentro = True
            continue
        out.append(l)
    # sin blancos duplicados ni blancos al inicio de bloque
    res = []
    for l in out:
        if not l.strip() and res and not res[-1].strip():
            continue
        res.append(l)
    return res


def clase_cabecera(ruta, nombre):
    c = bloque_clase(leer(ruta), nombre)
    c = sin_doc(c)
    c = quita_bloque(c, "(std::istream & flujo", "// ... constructor desde un flujo de entrada omitido")
    c = quita_bloque(c, "void print(", "// ... print() omitido")
    return c


def clase_ejercicio(ruta, nombre):
    return bloque_clase(leer(ruta), nombre)


def pagina(modo):
    dirigido = modo == "dir"
    if dirigido:
        clase = clase_cabecera("Estructuras de datos/Digrafo.h", "Digrafo")
        bfs = ["// (el mismo BFS del tema 4, con Digrafo)"] + [l.replace("Grafo const&", "Digrafo const&") for l in clase_ejercicio("4-Grafos no dirigidos/EJ_04-L/EJ_04-L.cpp", "CaminosBFS")]
        topo = clase_ejercicio("5-Grafos dirigidos/EJ_05-3/EJ_05-3.cpp", "OrdenTopologico")
        codes = {
            "clase": {"f": "Digrafo.h (resumen)", "tab": "Digrafo.h", "lines": clase},
            "bfs": {"f": "BFS (EJ_04-L / EJ_05-1)", "tab": "BFS", "lines": bfs},
            "topo": {"f": "EJ_05-3.cpp", "tab": "Orden topológico", "lines": topo},
        }
        algo_list = [
            {"id": "bfs", "nombre": "BFS: distancias desde un origen", "src": True, "dst": True, "code": "bfs"},
            {"id": "topo", "nombre": "DFS: orden topológico y ciclos", "src": False, "dst": False, "code": "topo", "dag": True},
            {"id": "inv", "nombre": "inverso(): invertir todas las aristas", "src": False, "dst": False, "code": "clase"},
        ]
        algos = (AQUI / "grafo_algos_comun.js").read_text(encoding="utf-8") + (AQUI / "grafo_algos_dir.js").read_text(encoding="utf-8")
        presets = [
            {"nombre": "Tareas con precedencias (sin ciclos)", "n": 7, "algo": "topo", "src": 0, "dst": 4,
             "pos": [[90, 110], [250, 60], [250, 200], [420, 110], [570, 110], [90, 320], [330, 330]],
             "e": [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [5, 2], [5, 6], [6, 4]]},
            {"nombre": "Tareas con un ciclo (Imposible)", "n": 6, "algo": "topo", "src": 0, "dst": 3,
             "pos": [[80, 210], [230, 90], [400, 90], [550, 210], [400, 340], [230, 340]],
             "e": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 2], [5, 0], [5, 4]]},
            {"nombre": "Transformación modular M=7 (x→2x+1, x→x+3)", "n": 7, "algo": "bfs", "src": 0, "dst": 5,
             "e": [[x, (2 * x + 1) % 7] for x in range(7)] + [[x, (x + 3) % 7] for x in range(7)]},
            {"nombre": "Camino de ida pero no de vuelta", "n": 5, "algo": "bfs", "src": 0, "dst": 4,
             "pos": [[90, 210], [230, 100], [230, 320], [420, 210], [560, 210]],
             "e": [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]},
        ]
        extra_btn = '<button class="btn" id="bInv" title="Sustituye el grafo por g.inverso()">⇄ Invertir grafo</button>'
        reps = {
            "TITULO": "Grafo dirigido", "TEMA": "5", "H1": "Digrafo: grafos dirigidos con listas de adyacencia",
            "LEDE": "Aquí cada arista <code>v→w</code> tiene sentido: <code>ponArista(v, w)</code> mete <code>w</code> solo en la lista de <code>v</code>. Construye uno, mira cómo se rellenan las listas y ejecuta BFS, orden topológico o <code>inverso()</code> paso a paso sobre el código real.",
            "GRAFO": "digrafo", "GRAFO_H2": "Digrafo (arrastra los vértices)", "HEADER": "Digrafo.h", "DIR": "true",
            "EXTRA_BTN": extra_btn,
            "IDEAS": IDEAS_DIR, "TABLA": TABLA_DIR,
        }
    else:
        clase = clase_cabecera("Estructuras de datos/Grafo.h", "Grafo")
        comp = clase_ejercicio("4-Grafos no dirigidos/EJ_04-2/EJ_04-2.cpp", "MaximaCompConexa")
        bfs = clase_ejercicio("4-Grafos no dirigidos/EJ_04-L/EJ_04-L.cpp", "CaminosBFS")
        bip = clase_ejercicio("4-Grafos no dirigidos/EJ_04-7/EJ_04-7.cpp", "Bipartito")
        codes = {
            "clase": {"f": "Grafo.h (resumen)", "tab": "Grafo.h", "lines": clase},
            "comp": {"f": "EJ_04-2.cpp", "tab": "Componentes (DFS)", "lines": comp},
            "bfs": {"f": "EJ_04-L.cpp", "tab": "BFS", "lines": bfs},
            "bip": {"f": "EJ_04-7.cpp", "tab": "Bipartito (DFS)", "lines": bip},
        }
        algo_list = [
            {"id": "comp", "nombre": "DFS: componentes conexas y tamaños", "src": False, "dst": False, "code": "comp"},
            {"id": "bfs", "nombre": "BFS: distancias desde un origen", "src": True, "dst": True, "code": "bfs"},
            {"id": "bip", "nombre": "DFS: ¿es bipartito? (2 colores)", "src": False, "dst": False, "code": "bip"},
        ]
        algos = (AQUI / "grafo_algos_comun.js").read_text(encoding="utf-8") + (AQUI / "grafo_algos_undir.js").read_text(encoding="utf-8")
        rej = [[i, j] for i in range(9) for j in range(9) if (j == i + 1 and i % 3 != 2) or j == i + 3]
        presets = [
            {"nombre": "Dos componentes", "n": 8, "algo": "comp", "src": 0, "dst": 3,
             "pos": [[100, 110], [240, 70], [240, 190], [390, 130], [110, 320], [260, 340], [470, 300], [570, 190]],
             "e": [[0, 1], [0, 2], [1, 2], [2, 3], [4, 5], [6, 7]]},
            {"nombre": "Ciclo impar (no bipartito)", "n": 6, "algo": "bip", "src": 0, "dst": 3,
             "pos": [[90, 210], [220, 90], [350, 210], [490, 90], [560, 260], [430, 340]],
             "e": [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 2]]},
            {"nombre": "Cuadrícula 3×3 (píxeles como vértices)", "n": 9, "algo": "bfs", "src": 0, "dst": 8,
             "pos": [[170 + 150 * (i % 3), 70 + 140 * (i // 3)] for i in range(9)], "e": rej},
            {"nombre": "Árbol libre (conexo y A = V − 1)", "n": 7, "algo": "comp", "src": 0, "dst": 6,
             "pos": [[320, 60], [170, 170], [470, 170], [90, 300], [250, 300], [390, 300], [550, 300]],
             "e": [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]},
        ]
        reps = {
            "TITULO": "Grafo no dirigido", "TEMA": "4", "H1": "Grafo: listas de adyacencia y recorridos",
            "LEDE": "Un <code>Grafo</code> guarda para cada vértice la lista de sus adyacentes. Construye uno (o carga un ejemplo), mira cómo <code>ponArista</code> rellena las listas y ejecuta DFS o BFS paso a paso sobre el código real de los ejercicios.",
            "GRAFO": "grafo", "GRAFO_H2": "Grafo (arrastra los vértices)", "HEADER": "Grafo.h", "DIR": "false",
            "EXTRA_BTN": "", "IDEAS": IDEAS_UN, "TABLA": TABLA_UN,
        }
    reps.update({
        "PRESETS": json.dumps(presets, ensure_ascii=False),
        "CODES": json.dumps(codes, ensure_ascii=False),
        "ALGO_LIST": json.dumps(algo_list, ensure_ascii=False),
        "ALGOS": algos,
        "LEGEND": json.dumps(
            '<span><b style="border-color:var(--accent);background:var(--accent-soft)"></b>vértice actual</span>'
            '<span><b style="border-color:var(--blue);background:var(--blue-soft)"></b>visitado / en la pila</span>'
            '<span><b style="border-color:var(--purple);background:var(--purple-soft)"></b>en la cola / 2.º color</span>'
            '<span><b style="border-color:var(--green);background:var(--green-soft)"></b>terminado</span>'
            '<span><b style="border-color:var(--red);background:var(--red-soft)"></b>conflicto / ciclo</span>', ensure_ascii=False),
        "L_PON1": "L('clase','if (v < 0'),L('clase','throw'),L('clase','++_A')",
        "L_PON2": "L('clase','_ady[v].push_back(w)')",
        "L_PON3": "L('clase','_ady[w].push_back(v)')" if not dirigido else "0",
    })
    s = TPL
    # orden: sustituir primero los marcadores largos
    for k in sorted(reps, key=len, reverse=True):
        s = s.replace(f"@@{k}@@", reps[k])
    assert "@@" not in s, re.findall(r"@@\w+@@", s)
    return s


def li(titulo, texto):
    return f'      <div class="panel"><h3>{titulo}</h3><p>{texto}</p></div>'


def fila(n, nombre, idea):
    return f"        <tr><td><code>{n}</code></td><td>{nombre}</td><td>{idea}</td></tr>"


IDEAS_UN = "\n".join([
    li("Una lista por vértice", "En vez de una matriz V×V, <code>_ady[v]</code> guarda solo los vecinos de <code>v</code>. La memoria es O(V + A) y recorrer los vecinos cuesta exactamente su grado: justo lo que hace <code>for (int w : g.ady(v))</code>."),
    li("Cada arista aparece dos veces", "<code>ponArista(v, w)</code> hace <code>push_back</code> en <b>las dos</b> listas. <code>A()</code> cuenta la arista una sola vez, pero la suma de las longitudes de las listas es <code>2·A</code>. Por eso un DFS ve cada arista dos veces: una desde cada extremo."),
    li("Un vértice sin visitar abre una componente", "El bucle externo <code>for v</code> lanza un DFS por cada vértice sin visitar; cada llamada cubre <b>una</b> componente conexa. Contar llamadas = número de componentes; lo que devuelve = su tamaño (04-1, 04-2, 04-3, 04-5)."),
    li("DFS o BFS", "Para «¿se llega?» o «¿cuántos?» da igual. Para <b>distancias mínimas</b> hace falta BFS: la cola visita por capas, así que la primera vez que se llega a un vértice es por un camino más corto (04-4, 04-6, 04-L). Un DFS puede llegar por uno larguísimo."),
    li("Dos colores obligan", "Bipartito = se puede colorear con 2 colores sin que una arista una vértices iguales. El DFS propaga el color contrario al vecino; si un vecino ya visitado tiene <b>mi</b> color, hay un ciclo impar y no lo es (04-7)."),
    li("Costes", "<code>ponArista</code> O(1) · <code>ady(v)</code> O(1) · cualquier recorrido completo O(V + A). Cuidado: el DFS recursivo puede bajar hasta V niveles (en el juez no suele dar problemas, en Visual Studio con 1 MB de pila sí)."),
])
IDEAS_DIR = "\n".join([
    li("Una arista, una lista", "<code>ponArista(v, w)</code> añade <code>w</code> solo a <code>_ady[v]</code>. La suma de las longitudes de las listas es exactamente <code>A()</code> (en no dirigido era 2·A). <code>ady(v)</code> son los <b>sucesores</b> de <code>v</code>."),
    li("Llegar no es simétrico", "Que <code>w</code> sea alcanzable desde <code>v</code> no dice nada de <code>v</code> desde <code>w</code>. La BFS desde un origen da la distancia dirigida mínima; los vértices con <code>dist = -1</code> son los no alcanzables (05-1, 05-2)."),
    li("Tres estados en el DFS", "<code>0</code> sin visitar · <code>1</code> en la pila (se está explorando) · <code>2</code> terminado. Si desde <code>v</code> veo un vecino en estado <b>1</b>, esa arista vuelve a un antecesor: <b>ciclo</b>. Ver uno en estado 2 es normal."),
    li("Orden topológico = postorden inverso", "Cuando el DFS termina <code>v</code>, ya terminó todo lo que depende de él; guardando los vértices al terminar y dando la vuelta a la lista, cada tarea queda antes que sus sucesores. Solo existe si el digrafo <b>no tiene ciclos</b> (05-3)."),
    li("inverso()", "Recorre cada arista <code>v→w</code> y mete <code>inv.ponArista(w, v)</code>. Cuesta O(V + A). Sirve para preguntar «¿quién llega a <code>v</code>?» con un recorrido normal sobre el inverso."),
    li("Grafo explícito o implícito", "En 05-2 se construyen los 10.000 vértices con sus 3 aristas de salida y se hace BFS. En 05-1 los vecinos salen de una fórmula <code>(a·x+b) mod M</code>; se puede construir el <code>Digrafo</code> o calcularlos al vuelo (más rápido si M es grande y N pequeño)."),
])
TABLA_UN = "\n".join([
    fila("04-1", "Árboles libres", "DFS: conexo y A = V − 1"),
    fila("04-2", "Los amigos de mis amigos…", "DFS: componente conexa más grande"),
    fila("04-3", "Detección de manchas negras", "Píxel → vértice; DFS: nº de componentes y la mayor"),
    fila("04-4", "Los números de Bacon", "BFS en grafo actor–película"),
    fila("04-5", "¡Las noticias vuelan!", "Aristas en estrella + tamaño de componentes"),
    fila("04-6", "Un nodo muy muy lejano", "BFS con distancias, cortado en el TTL"),
    fila("04-7", "Grafo bipartito", "DFS coloreando con 2 colores"),
    fila("04-L", "Peaje a la sombra", "3 BFS y mínimo de dA + dL + dT"),
])
TABLA_DIR = "\n".join([
    fila("05-1", "Juego de Transformación Modular", "BFS sobre x → (a·x+b) mod M"),
    fila("05-2", "La máquina calculadora", "BFS sobre los 10.000 números del marcador (+1, ×2, ÷3)"),
    fila("05-3", "Ordenando tareas", "Orden topológico (postorden inverso) y detección de ciclos"),
])

if __name__ == "__main__":
    (AQUI / "tema4-grafo.frag.html").write_text(pagina("undir"), encoding="utf-8")
    (AQUI / "tema5-digrafo.frag.html").write_text(pagina("dir"), encoding="utf-8")
    print("ok")
