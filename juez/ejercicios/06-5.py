"""06-5 · Las minas del emperador Trajano: juez con pruebas pensadas para cada error típico.

Cada caso: «N M», M galerías «cámara cámara tiempo» (sin bucles ni galerías repetidas) y una
línea «origen destino». Salida: el menor tiempo T tal que las galerías de tiempo ≤ T unen el
origen con el destino (camino minimax), 0 si origen = destino, o IMPOSIBLE.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-5/EJ_06-5.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-5/GrafoValorado.h",
                  "6-Conjuntos disjuntos y grafos valorados/EJ_06-5/ConjuntosDisjuntos.h"],
    "limite_ms": 3000,
    "fallo": ["aguante = a.valor();", "aguante += a.valor();"],
}


def resuelve(N, galerias, o, d):
    """Solucionador independiente: búsqueda binaria sobre el tiempo + recorrido (no es Kruskal)."""
    if o == d:
        return "0\n"
    ady = [[] for _ in range(N + 1)]
    for u, v, t in galerias:
        ady[u].append((v, t))
        ady[v].append((u, t))

    def llega(T):
        visto = bytearray(N + 1)
        visto[o] = 1
        pila = [o]
        while pila:
            x = pila.pop()
            for y, t in ady[x]:
                if t <= T and not visto[y]:
                    visto[y] = 1
                    pila.append(y)
        return visto[d]

    tiempos = sorted({t for _, _, t in galerias})
    if not tiempos or not llega(tiempos[-1]):
        return "IMPOSIBLE\n"
    lo, hi = 0, len(tiempos) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if llega(tiempos[mid]):
            hi = mid
        else:
            lo = mid + 1
    return f"{tiempos[lo]}\n"


def caso_a_texto(N, galerias, o, d):
    return f"{N} {len(galerias)}\n" + "".join(f"{u} {v} {t}\n" for u, v, t in galerias) + f"{o} {d}\n"


def aleatorio(rng, N, M, tmax):
    pares = [(u, v) for u in range(1, N + 1) for v in range(u + 1, N + 1)]
    rng.shuffle(pares)
    gal = []
    for u, v in pares[:min(M, len(pares))]:
        if rng.random() < 0.5:
            u, v = v, u
        gal.append((u, v, rng.randint(1, tmax)))
    o, d = rng.randint(1, N), rng.randint(1, N)
    if rng.random() < 0.9 and N > 1:
        while d == o:
            d = rng.randint(1, N)
    return N, gal, o, d


def grande(rng):
    """20.000 cámaras y 110.000 galerías; el tesoro (cámara 20.000) solo se alcanza por la más lenta."""
    N = 20000
    vistos, gal = set(), []
    for k in range(2, N):
        u = rng.randint(1, k - 1)
        vistos.add((u, k))
        gal.append((k, u, rng.randint(1, 999998)))
    while len(gal) < 109999:
        u, v = rng.randint(1, N - 1), rng.randint(1, N - 1)
        if u != v and (min(u, v), max(u, v)) not in vistos:
            vistos.add((min(u, v), max(u, v)))
            gal.append((u, v, rng.randint(1, 999998)))
    gal.append((N, rng.randint(1, N - 1), 1000000))
    rng.shuffle(gal)
    return N, gal, rng.randint(1, N - 1), N


def cadena_profunda():
    """Para conjuntos disjuntos sin unión por tamaños ni compresión: las galerías «k k+1» forman
    una cadena de 19.999 cámaras con el origen al fondo, y luego muchas galerías que sobran."""
    N = 20000
    gal = [(k, k + 1, k) for k in range(1, N - 1)]
    extra, m = [], 0
    while len(extra) < 80000:
        m += 1
        for a in range(1, m - 1):
            extra.append((a, m, 30000 + len(extra)))
    gal += extra[:80000]
    gal.append((N - 1, N, 1000000))
    return N, gal, 1, N


def pruebas():
    rng = random.Random(65)
    ej1 = (4, [(1, 2, 2), (2, 4, 5), (4, 1, 10), (1, 3, 6)], 1, 4)
    ej2 = (1, [], 1, 1)
    ej3 = (2, [], 1, 2)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ej1],
           "El primer ejemplo del PDF: es mejor dar un rodeo por la cámara 2 (galerías de 2 y 5) que ir directo (10).",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: no se busca el camino de menor SUMA, sino el de galería más larga más corta."},
           ["Ejecútalo en tu ordenador con el ejemplo y compara.",
            "Palencia descansa en cada cámara: lo que importa de un camino es su galería MÁS LARGA.",
            "Kruskal: añade galerías de menor a mayor y para en cuanto el origen y el destino queden unidos."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ej2],
           "El segundo ejemplo: una sola cámara, origen y tesoro en el mismo sitio; la respuesta es 0.",
           {"wa": "Si el origen y el destino son la misma cámara no hay que bucear: 0."},
           ["Con origen = destino la respuesta es 0, haya galerías o no.",
            "Comprueba unidos(origen, destino) ANTES de mirar la primera galería."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [ej3],
           "El tercer ejemplo: dos cámaras sin galerías; IMPOSIBLE.",
           {"wa": "Si no se puede llegar hay que escribir exactamente «IMPOSIBLE», en mayúsculas.",
            "rte": "Con M = 0 algo se rompe: revisa la lectura (tras las galerías viene la línea «origen destino»)."},
           ["Sin galerías no se puede ir de la cámara 1 a la 2.",
            "El texto es «IMPOSIBLE», todo en mayúsculas."])
    prueba("Dos cámaras y una galería", "borde", [(2, [(2, 1, 1000000)], 1, 2), (2, [(1, 2, 1)], 2, 1)],
           "La mina más pequeña en la que hay que bucear.",
           {"wa": "Con una sola galería entre origen y destino, la respuesta es su tiempo."},
           ["La galería se puede recorrer en los dos sentidos.",
            "La respuesta es el tiempo de esa única galería."])
    # --- Trampas. El orden importa: las primeras no deben fallar por los errores que buscan las siguientes.
    prueba("Cámaras numeradas desde 1", "trampa", [(2, [(2, 1, 7)], 1, 2)],
           "El tesoro está en la cámara N: hay que restar 1 al origen y al destino, igual que a las galerías.",
           {"rte": "Usas el origen o el destino tal cual: la cámara N se sale de los conjuntos disjuntos. Resta 1 a los dos.",
            "wa": "El origen o el destino caen en otra cámara: resta 1 a los dos (la entrada cuenta desde 1)."},
           ["El tesoro está en la cámara 2 de una mina de 2 cámaras: en base 0, la 1.",
            "Si lees el grafo con GrafoValorado<int>(cin, 1), haz también --origen y --destino."])
    prueba("Se aguanta la galería más larga, no la suma", "trampa",
           [(3, [(1, 2, 2), (2, 3, 5)], 1, 3), (4, [(1, 2, 1), (2, 3, 1), (3, 4, 1)], 4, 1)],
           "En cada cámara se recupera el aliento: lo que cuenta es la galería más larga del camino.",
           {"wa": "Sumas los tiempos de las galerías (como un camino mínimo). Aquí se descansa en cada cámara: la respuesta es un máximo, no una suma."},
           ["En el primer caso el camino 1–2–3 obliga a aguantar 5 segundos (la galería más larga), no 7.",
            "Guarda el tiempo de la última galería que aceptas, sin sumar."])
    prueba("Una galería lenta que no hace falta", "trampa",
           [(3, [(1, 2, 3), (1, 3, 4), (2, 3, 9)], 2, 3), (4, [(1, 2, 2), (1, 3, 2), (1, 4, 2), (4, 3, 900)], 3, 4)],
           "La galería directa es lentísima, pero hay un rodeo mejor: no cuenta.",
           {"wa": "Te quedas con la galería más lenta de las que miras, aunque una cámaras ya unidas. Solo cuenta la galería que consigue unir el origen con el destino."},
           ["En el primer caso, de 2 a 3 el rodeo por la cámara 1 obliga a aguantar 4; la galería directa de 9 sobra.",
            "Actualiza el tiempo solo cuando la galería une dos grupos distintos, y para al unir origen y destino."])
    prueba("No hace falta recorrer toda la mina", "trampa",
           [(4, [(1, 2, 3), (3, 4, 50), (2, 3, 4)], 1, 3), (5, [(1, 2, 1), (2, 3, 2), (4, 5, 1000), (3, 4, 999)], 3, 1)],
           "Solo importan el origen y el destino: las cámaras lejanas no cuentan aunque estén mal comunicadas.",
           {"wa": "Sigues añadiendo galerías hasta unir TODA la mina (eso es la selva de Tarzán, 06-4). Hay que parar en cuanto el origen y el destino queden unidos."},
           ["En el primer caso, de 1 a 3 basta con 3 y 4: la respuesta es 4, aunque la cámara 4 necesite 50.",
            "La condición de parada es unidos(origen, destino), no num_cjtos() == 1."])
    prueba("Palencia ya está en la cámara del tesoro", "trampa", [(3, [(1, 2, 4), (2, 3, 6)], 2, 2)],
           "Origen y destino iguales, aunque haya galerías: no hay que bucear, 0.",
           {"wa": "Miras si el origen y el destino están unidos DESPUÉS de añadir una galería: con origen = destino ya están unidos antes de empezar y la respuesta es 0."},
           ["Palencia y el tesoro están en la cámara 2: la respuesta es 0, no 4.",
            "Pon la comprobación unidos(origen, destino) al principio de cada vuelta (o trata aparte origen == destino)."])
    prueba("Galerías en cualquier orden", "trampa",
           [(3, [(1, 3, 90), (1, 2, 5), (2, 3, 6)], 1, 3), (4, [(1, 4, 9), (1, 2, 8), (2, 3, 2), (3, 4, 3)], 1, 4)],
           "Las galerías no vienen ordenadas: hay que añadirlas de menor a mayor tiempo.",
           {"wa": "No ordenas las galerías por tiempo creciente (o las ordenas al revés). Kruskal necesita mirarlas de más rápida a más lenta."},
           ["En el primer caso de 1 a 3 hay una galería directa de 90 y un rodeo 1–2–3 con galerías de 5 y 6: la respuesta es 6.",
            "Ordena las aristas: sort(v.begin(), v.end()) con Arista ya compara por valor."])
    prueba("Tesoro inalcanzable aunque haya muchas galerías", "trampa",
           [(5, [(1, 2, 1), (2, 3, 2), (3, 1, 3), (4, 5, 4)], 1, 5), (4, [(2, 3, 5), (3, 4, 5), (4, 2, 5)], 2, 1)],
           "El origen y el destino quedan en partes separadas de la mina: IMPOSIBLE.",
           {"wa": "Escribes un tiempo aunque el tesoro sea inalcanzable, o el texto no es exactamente «IMPOSIBLE» (en mayúsculas)."},
           ["En el primer caso las cámaras {1, 2, 3} y {4, 5} no se comunican: IMPOSIBLE.",
            "Al acabar, si !unidos(origen, destino), escribe «IMPOSIBLE»."])
    prueba("Tiempos extremos", "borde",
           [(3, [(1, 2, 1000000), (2, 3, 1000000)], 3, 1), (3, [(1, 2, 1), (2, 3, 1)], 1, 3)],
           "Galerías de 1.000.000 segundos y de 1 segundo.",
           {"wa": "Con los valores extremos algo falla: ¿inicializas el tiempo o un máximo con un valor que no llega a 1.000.000?"},
           ["La respuesta puede ser 1.000.000.",
            "Si usas un valor «infinito», que sea mayor que 1.000.000."])
    prueba("Varias minas seguidas", "trampa",
           [(4, [(1, 2, 70), (2, 3, 80), (3, 4, 90)], 1, 4), (3, [(1, 2, 5)], 3, 3), (2, [(1, 2, 6)], 2, 1), (3, [(1, 2, 1)], 1, 3), (1, [], 1, 1)],
           "Una mina con galerías lentas seguida de otras pequeñas: nada de la anterior debe quedar.",
           {"wa": "Algo se arrastra de una mina a la siguiente: el tiempo o la partición se declaran fuera de resuelveCaso (o como static).",
            "rte": "Un vector de una mina anterior con otro tamaño: crea el grafo y los conjuntos disjuntos en cada caso."},
           ["Fíjate en la segunda mina (origen = destino): debe salir 0, no el tiempo de la anterior.",
            "El tiempo tiene que empezar en 0 en cada caso."])
    casos_al = [aleatorio(rng, rng.randint(1, 7), rng.randint(0, 12), rng.choice([4, 20, 1000000])) for _ in range(100)]
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "100 minas pequeñas al azar: conexas y no conexas, con empates y alguna con origen = destino.",
           {"wa": "Hay alguna mina concreta que no tratas: la línea que falla es el número de caso; búscala y haz Kruskal a mano."},
           ["La línea que falla es el número de caso: busca esa mina en la entrada.",
            "Ordena sus galerías a mano y añádelas hasta que el origen y el destino queden unidos."])
    prueba("Mina grande con el tesoro tras la galería más lenta", "rendimiento", [grande(rng)],
           "20.000 cámaras y 110.000 galerías; al tesoro solo se llega por la galería más lenta, así que hay que mirarlas todas.",
           {"tle": "Tu solución no es O(M log M): ¿llamas a g.aristas() (que crea un vector nuevo) dentro del bucle, o repites un recorrido completo por cada galería o cada tiempo posible?",
            "mle": "Gastas demasiada memoria: no copies el vector de galerías ni uses matrices N × N."},
           ["Ordena las galerías UNA vez y recórrelas en ese orden.",
            "Comprobar unidos(origen, destino) con conjuntos disjuntos es casi O(1): no hace falta un recorrido.",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    prueba("Cadena larga de cámaras", "rendimiento", [cadena_profunda()],
           "Las galerías rápidas forman una fila de 20.000 cámaras con el origen al fondo, y después hay muchas que sobran.",
           {"tle": "Tus conjuntos disjuntos forman árboles muy altos: usa unión por tamaños y compresión de caminos (como ConjuntosDisjuntos.h).",
            "rte": "La búsqueda recursiva baja demasiado: con unión por tamaños la altura es como mucho log N."},
           ["Sin unión por tamaños, unir la fila cámara a cámara deja una cadena: buscar el representante del origen cuesta N pasos en cada vuelta.",
            "Usa la clase ConjuntosDisjuntos de la asignatura."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(*c) for c in casos),
                   salida="".join(resuelve(*c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


INGENUA = """class ConjuntosDisjuntos {
    std::vector<int> p; int n;
public:
    ConjuntosDisjuntos(int N) : p(N), n(N) { for (int i = 0; i < N; ++i) p[i] = i; }
    int buscar(int a) const { while (p[a] != a) a = p[a]; return a; }
    void unir(int a, int b) { int i = buscar(a), j = buscar(b); if (i != j) { p[i] = j; --n; } }
    bool unidos(int a, int b) const { return buscar(a) == buscar(b); }
    int num_cjtos() const { return n; }
};"""

VARIANTES = [
    Variante("no resta 1 al origen y al destino", [("--origen; --destino;", "")], prueba=5, v="rte"),
    Variante("comprueba la llegada después de unir", [("        if (cd.unidos(origen, destino)) break;\n", ""),
                                                      ("aguante = a.valor();", "aguante = a.valor();\n            if (cd.unidos(origen, destino)) break;")], prueba=9, v="wa"),
    Variante("suma los tiempos", [("aguante = a.valor();", "aguante += a.valor();")], prueba=6, v="wa"),
    Variante("galería más lenta de todas", [("if (cd.unidos(origen, destino)) break;", "aguante = max(aguante, a.valor());")], prueba=7, v="wa"),
    Variante("une toda la mina", [("if (cd.unidos(origen, destino)) break;", "if (cd.num_cjtos() == 1) break;")], prueba=8, v="wa"),
    Variante("no ordena las galerías", [("sort(galerias.begin(), galerias.end());", "")], prueba=10, v="wa"),
    Variante("nunca escribe IMPOSIBLE", [("if (cd.unidos(origen, destino)) cout << aguante << '\\n';\n    else cout << \"IMPOSIBLE\\n\";", "cout << aguante << '\\n';")], prueba=11, v="wa"),
    Variante("escribe «Imposible»", [("cout << \"IMPOSIBLE\\n\";", "cout << \"Imposible\\n\";")], prueba=11, v="wa"),
    Variante("tiempo acumulado entre minas", [("int aguante = 0;", "static int aguante = 0;")], prueba=13, v="wa"),
    Variante("llama a g.aristas() en cada vuelta", [("for (auto const& a : galerias) {", "for (size_t k = 0; k < g.aristas().size(); ++k) {\n        auto const& a = galerias[k];")], prueba=15, v="tle"),
    Variante("conjuntos disjuntos sin optimizar", [('#include "ConjuntosDisjuntos.h"  // estructuras de datos de clase', INGENUA)], prueba=16, v="tle"),
]
