"""11-L · La fiesta de graduación: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso son DOS líneas con una lista de canciones (hasta 1.000 palabras
cada una, con repeticiones; una línea puede estar vacía). Salida: por caso, una línea con una lista de
la longitud máxima que sea subsecuencia de las dos (o una línea vacía si no hay ninguna).
Vale cualquier lista óptima: por eso lleva comprobador propio (comprobadores/11-l.{py,js}).
ALTERNATIVA da otra lista óptima y el verificador comprueba que se acepta.
El solucionador es propio: la tabla se rellena por SUFIJOS (de atrás hacia delante) y la lista sale
ya en orden, al revés que la solución del repo. Validado contra fuerza bruta (todas las subsecuencias
de la primera lista) en miles de casos pequeños.
"""
import itertools
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-L/EJ_11-L.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["    reverse(lista.begin(), lista.end());\n", ""],
}


def resuelve(a, b, alt=False):
    """Una lista común máxima; alt=True da otra (en los empates avanza por el otro lado)."""
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if a[i] == b[j] else max(t[i + 1][j], t[i][j + 1])
    r, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] == b[j]:
            r.append(a[i]); i += 1; j += 1
        elif t[i][j + 1] > t[i + 1][j] or (t[i][j + 1] == t[i + 1][j] and not alt):
            j += 1
        else:
            i += 1
    return r


def _es_sub(x, a):
    it = iter(a)
    return all(any(c == d for d in it) for c in x)


def fuerza_bruta(a, b):
    """Longitud máxima probando todas las subsecuencias de a (a pequeña)."""
    mejor = 0
    for mask in range(1 << len(a)):
        x = [a[i] for i in range(len(a)) if mask >> i & 1]
        if len(x) > mejor and _es_sub(x, b):
            mejor = len(x)
    return mejor


def texto(casos):
    return f"{len(casos)}\n" + "".join(f"{' '.join(a)}\n{' '.join(b)}\n" for a, b in casos)


def salida(casos, alt=False):
    return "".join(" ".join(resuelve(a, b, alt)) + "\n" for a, b in casos)


def _asegura():
    r = random.Random(9)
    for _ in range(800):
        k = r.choice([2, 3, 5])
        a = [f"c{r.randrange(k)}" for _ in range(r.randint(0, 9))]
        b = [f"c{r.randrange(k)}" for _ in range(r.randint(0, 9))]
        for alt in (False, True):
            x = resuelve(a, b, alt)
            assert len(x) == fuerza_bruta(a, b) and _es_sub(x, a) and _es_sub(x, b)
_asegura()


def alea(rng, n, m, k, hueco=0.0):
    """Dos listas de n y m canciones tomadas de k títulos distintos."""
    return ([f"T{rng.randrange(k)}" for _ in range(n)], [f"T{rng.randrange(k)}" for _ in range(m)])


def _conjunto(a, b):
    """«Intersección en orden»: lo que sale si se coge cada canción de a que aparece en b (sin repetir uso)."""
    return len(resuelve(a, b))


def _voraz(a, b):
    """Voraz que falla: para cada canción de a, la primera aparición posible en b."""
    j, r = 0, []
    for c in a:
        k = j
        while k < len(b) and b[k] != c:
            k += 1
        if k < len(b):
            r.append(c); j = k + 1
    return len(r)


def _voraces_que_fallan(rng, cuantos):
    ok = []
    while len(ok) < cuantos:
        a, b = alea(rng, rng.randint(5, 9), rng.randint(5, 9), 4)
        if _voraz(a, b) < len(resuelve(a, b)):
            ok.append((a, b))
    return ok


def _con_repetidas(rng, cuantos):
    """Casos donde hay canciones repetidas y la longitud solo sale bien si cada repetición usa su propia aparición."""
    ok = []
    while len(ok) < cuantos:
        a, b = alea(rng, rng.randint(6, 10), rng.randint(6, 10), 3)
        conj = len({c for c in a} & {c for c in b})
        if len(resuelve(a, b)) > conj:
            ok.append((a, b))
    return ok


def pruebas():
    rng = random.Random(1111)
    L = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        for a, b in casos:
            assert len(a) <= 1000 and len(b) <= 1000
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    VARIAS = "Vale cualquier lista común de la longitud máxima."
    S = lambda t: t.split()
    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado",
           [(S("One Respect Radio_Ga_Ga One Volando_voy Caruso"), S("Respect One Volando_voy Ne_me_quitte_pas Radio_Ga_Ga"))],
           "Respect, One y Volando_voy están en las dos listas en ese orden: 3 canciones. " + VARIAS,
           {"wa": "Falla el primer ejemplo: la lista común más larga es «Respect One Volando_voy» (3 canciones, en el orden de las dos listas).",
            "pe": "Las canciones van en una sola línea separadas por un espacio."},
           ["Radio_Ga_Ga está en las dos listas, pero si la usas ya no caben One ni Volando_voy.",
            "larga(i, j) = larga(i−1, j−1) + 1 si coinciden; si no, el máximo de quitar la última de una lista o de la otra."])
    prueba("Ejemplo 2 del enunciado", "enunciado",
           [(S("Despacito Fiesta_pagana"), S("Grandola_Vila_Morena")), (S("Ay"), S("Ay"))],
           "Ninguna canción en común: se escribe una línea vacía.",
           {"wa": "Sin canciones comunes hay que escribir una línea vacía (no un 0 ni nada más).",
            "rte": "Una lista de una sola canción y otra distinta: revisa los índices."},
           ["¿Qué escribe tu programa cuando la lista es vacía?",
            "larga(n, m) = 0: la reconstrucción no coge ninguna canción pero el salto de línea sí se escribe."])
    prueba("Ejemplo 3 del enunciado", "enunciado",
           [(S("Yesterday Macarena Mocatriz Buleria Orobroy Thriller"), S("Macarena Buleria Texas_Hold'em Vagabundo Thriller Bizcochito"))],
           "Macarena, Buleria y Thriller están en las dos en el mismo orden: las tres.",
           {"wa": "La lista debe salir en el orden de las listas originales: Macarena Buleria Thriller. Si la reconstruyes de atrás hacia delante, dale la vuelta."},
           ["La reconstrucción empieza por el final de las listas: las canciones salen de la última a la primera.",
            "Guárdalas en un vector y haz reverse antes de escribirlas."])
    prueba("Ejemplo 4 del enunciado", "enunciado",
           [(S("Columbia Bohemian_Rhapsody"), S("Bohemian_Rhapsody Columbia"))],
           "Las dos canciones están en las dos listas pero en orden contrario: solo cabe una. " + VARIAS,
           {"wa": "El orden importa: Columbia y Bohemian_Rhapsody están al revés, así que la lista tiene UNA canción, no dos."},
           ["No basta con «está en las dos»: tienen que respetar el orden.",
            "Es una subsecuencia común más larga, no una intersección de conjuntos."])

    # ------------------------------------------------------------------ bordes
    prueba("Una lista vacía", "borde",
           [([], []), ([], S("A B C")), (S("A B C"), []), (S("A"), S("B")), (S("A"), S("A"))],
           "Las dos listas vacías, una vacía y la otra no, y listas de una canción: se lee con getline y la línea puede estar vacía.",
           {"wa": "Una lista puede ocupar una línea vacía: léela con getline (con cin >> te comerías la línea siguiente) y escribe una línea vacía si no hay nada en común.",
            "rte": "Con n = 0 o m = 0 la tabla es de 1 fila o 1 columna: revisa que no te sales."},
           ["¿Qué hace tu lectura con una línea vacía?",
            "larga(i, 0) = larga(0, j) = 0, y el bucle de reconstrucción no debe ejecutarse."])
    prueba("Listas iguales o contenidas", "borde",
           [(S("A B C D"), S("A B C D")), (S("A B C D E"), S("B D")), (S("B D"), S("A B C D E")), (S("X"), S("X X X"))],
           "Listas iguales y una dentro de otra: la lista común es entera la más corta.",
           {"wa": "Si una lista está contenida en la otra, la respuesta es la más corta entera."},
           ["Con listas iguales, la reconstrucción recorre la diagonal entera.",
            "Comprueba el caso en que una lista es la otra con canciones intercaladas."])

    # ------------------------------------------------------------------ trampas
    prueba("Varios casos seguidos", "trampa",
           [(S("A A"), S("A A")), (S("A"), S("A")), ([], []), (S("B B"), S("Z B B")), (S("Z"), S("Y")), (S("K K K K K K"), S("K K K K K K K K"))],
           "Varios casos seguidos, también con listas vacías: la lectura de la primera línea debe consumir el salto del número de casos y nada del caso anterior debe quedar en la tabla ni en la lista.",
           {"wa": "Algo falla al encadenar casos: tras leer el número de casos con cin >> queda un salto de línea que el primer getline se come (lee una lista vacía), y la tabla y la lista se crean dentro de resuelveCaso.",
            "rte": "La lista o la tabla de un caso anterior tenía otro tamaño: créalas en cada caso."},
           ["Tras leer el número de casos con cin >> queda el salto de línea: el primer getline lo lee vacío.",
            "Declara la tabla y la lista dentro de resuelveCaso."])
    prueba("La lista sale en orden", "trampa",
           [(S("A B C D"), S("A B C D")), (S("X A Y B Z C"), S("A Q B R C")), (S("One Two Three"), S("Zero One Two Three Four")), (S("Q R S T U"), S("R T U V"))],
           "La reconstrucción empieza por el final de las listas: las canciones salen de la última a la primera y hay que darles la vuelta.",
           {"wa": "La lista debe salir en el orden de las listas originales: si reconstruyes de atrás hacia delante, dale la vuelta (reverse) antes de escribirla."},
           ["Compara tu lista con la esperada: ¿tiene las mismas canciones pero al revés?",
            "Guarda las canciones en un vector al reconstruir y haz reverse antes de escribirlas."])
    prueba("Cada repetición con su propia aparición", "trampa",
           [(S("A A A"), S("A A")), (S("A A A A"), S("A A A")), (S("A A"), S("A A A A A")), (S("A B A"), S("A A")), (S("A B A B A"), S("B A B"))],
           "Las canciones se repiten: «A A A» y «A A» comparten solo dos A, no tres ni una. Una repetición necesita una aparición distinta en cada lista.",
           {"wa": "Las repeticiones cuentan: cada aparición de una canción en la lista final usa una aparición distinta en cada lista. Con «A A A» y «A A» la lista común es «A A»."},
           ["Mira «A A A» frente a «A A»: ¿cuántas A pueden salir?",
            "No uses conjuntos: la tabla trabaja con posiciones, no con títulos."])
    prueba("Subsecuencia, no subcadena", "trampa",
           [(S("A X A"), S("A A Y Z")), (S("A"), S("A X")), (S("A X B Y A"), S("A B A")), (S("P A Q A R"), S("A Z A")), (S("A X B Y B Z A"), S("A B B A")), (S("M K M"), S("M M"))],
           "La lista común puede saltarse canciones entre medias: no tienen que estar seguidas.",
           {"wa": "No hace falta que las canciones estén seguidas en las listas: es una subsecuencia, puede saltarse las que sobran. Si no coinciden, toma el máximo de quitar la última de una lista o de la otra."},
           ["En «A X B Y A» y «A B A» la lista común es entera «A B A» aunque haya canciones por medio.",
            "En el caso a_i ≠ b_j la tabla no vuelve a 0: hereda el máximo de dos vecinas."])
    prueba("El voraz no sirve", "trampa",
           [(S("X A B A"), S("A B A X")), (S("D A A"), S("A A D")), (S("C A B A"), S("A B A C")), (S("Q A Q"), S("A Q A Q A"))],
           "Coger cada canción de la primera lista en su primera aparición posible de la segunda da una lista más corta que la óptima.",
           {"wa": "Un voraz (emparejar cada canción con su primera aparición posible) no siempre es óptimo: a veces conviene saltarse una canción para que quepan más después. Usa la tabla de programación dinámica."},
           ["Salta alguna canción de la primera lista y mira si caben más después.",
            "larga(i, j) elige entre usar la coincidencia o descartar una canción de cualquiera de las dos listas."])
    # ------------------------------------------------------------------ aleatorios
    casos = [alea(rng, rng.randint(0, 9), rng.randint(0, 9), rng.choice([2, 3, 5])) for _ in range(200)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 casos de listas de hasta 9 canciones con muchas repeticiones (2 a 5 títulos). " + VARIAS,
           {"wa": "Algún caso falla: son pequeños, calcula a mano la lista común más larga.",
            "pe": "Revisa el formato: una línea por caso y las canciones separadas por un espacio."},
           ["Localiza el caso en la entrada y comprueba la longitud de tu lista contra la de la tabla.",
            "El «Por qué» del veredicto dice si tu lista no cabe en una de las dos o si es demasiado corta."])
    casos = [alea(rng, rng.randint(30, 80), rng.randint(30, 80), rng.choice([4, 10, 40])) for _ in range(30)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "30 casos de 30 a 80 canciones. " + VARIAS,
           {"wa": "Los casos pequeños salen bien y estos no: revisa el tamaño de la tabla ((n + 1) × (m + 1)) y la reconstrucción.",
            "tle": "Una recursión sin memoria es exponencial. Guarda cada larga(i, j) en una tabla."},
           ["¿Calculas la misma larga(i, j) muchas veces? Apúntalo en una tabla.",
            "Reconstruye desde (n, m) hacia atrás."])

    # ------------------------------------------------------------------ rendimiento
    prueba("1000 y 1000 canciones", "rendimiento",
           [alea(rng, 1000, 1000, 30), alea(rng, 1000, 1000, 1000)],
           "El tamaño máximo: dos listas de 1.000 canciones (un millón de casillas), con pocos y con muchos títulos distintos.",
           {"tle": "Debe ser O(n · m): una recursión sin memoria es exponencial, y comparar cadenas largas dentro de tres bucles es lento.",
            "mle": "La tabla de 1.001 × 1.001 enteros son unos 4 MB: no guardes una copia de la lista en cada casilla.",
            "rte": "Con tablas tan grandes no uses un array local (pila): usa Matriz o vector."},
           ["n · m = 10⁶ casillas con trabajo constante cada una: muy poco.",
            "No copies cadenas dentro de los bucles: compara a[i − 1] con b[j − 1]."])
    return L


# ------------------------------------------------------------ variantes (fallos típicos)
VORAZ = """void resuelveCaso() {
    static bool prim = true;
    if (prim) { string r0; getline(cin, r0); prim = false; }
    vector<string> x0 = leeLista(), y0 = leeLista();
    size_t j = 0; vector<string> res;
    for (auto const& c : x0) {
        size_t k = j;
        while (k < y0.size() && y0[k] != c) ++k;
        if (k < y0.size()) { res.push_back(c); j = k + 1; }
    }
    for (size_t k = 0; k < res.size(); ++k) cout << (k ? " " : "") << res[k];
    cout << '\\n';
    return;
"""

RECURSIVA = """int recl(vector<string> const& a, vector<string> const& b, int i, int j) {
    if (i == 0 || j == 0) return 0;
    if (a[i - 1] == b[j - 1]) return recl(a, b, i - 1, j - 1) + 1;
    return max(recl(a, b, i - 1, j), recl(a, b, i, j - 1));
}

void resuelveCaso() {
    static bool prim = true;
    if (prim) { string r0; getline(cin, r0); prim = false; }
    vector<string> x0 = leeLista(), y0 = leeLista();
    int n0 = x0.size(), m0 = y0.size();
    vector<string> res;
    for (int i = n0, j = m0; i > 0 && j > 0; ) {
        if (x0[i - 1] == y0[j - 1]) { res.push_back(x0[i - 1]); --i; --j; }
        else if (recl(x0, y0, i - 1, j) >= recl(x0, y0, i, j - 1)) --i;
        else --j;
    }
    reverse(res.begin(), res.end());
    for (size_t k = 0; k < res.size(); ++k) cout << (k ? " " : "") << res[k];
    cout << '\\n';
    return;
"""

VARIANTES = [
    Variante("no da la vuelta a la lista", [("    reverse(lista.begin(), lista.end());\n", "")], prueba=8, v="wa"),
    Variante("al no coincidir retrocede siempre en la primera lista", [("        else if (larga[i - 1][j] >= larga[i][j - 1]) --i;\n        else --j;\n", "        else --i;\n")], prueba=10, v="wa"),
    Variante("no consume el salto de línea tras el número de casos", [("static bool primera = true;", "static bool primera = false;")], prueba=7, v="wa"),
    Variante("voraz: primera aparición posible", [("void resuelveCaso() {", VORAZ)], prueba=11, v="wa"),
    Variante("una aparición de la segunda lista sirve para varias repeticiones", [("{ lista.push_back(a[i - 1]); --i; --j; }", "{ lista.push_back(a[i - 1]); --i; }")], prueba=9, v="wa"),
    Variante("recursión sin memoria", [("void resuelveCaso() {", RECURSIVA)], prueba=[13], v="tle"),
]


def ALTERNATIVA(entrada):
    """Otra lista común máxima distinta en los empates."""
    l = entrada.split("\n")
    n = int(l[0])
    casos = [(l[1 + 2 * c].split(), l[2 + 2 * c].split()) for c in range(n)]
    return salida(casos, alt=True)
