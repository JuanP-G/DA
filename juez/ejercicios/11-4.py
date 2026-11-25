"""11-4 · Seis grados de separación: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso tiene «P R» (P personas 1..500, R relaciones 0..10.000) y R
líneas con los nombres (hasta 10 letras inglesas, distintos entre mayúsculas y minúsculas) de dos
personas distintas que se conocen. Los nombres pueden repetirse en varias relaciones, y puede haber
personas que no salen en ninguna (cuentan en P). Una relación puede repetirse.
Salida: el grado de separación de la red (el mayor número mínimo de relaciones entre dos personas)
o DESCONECTADA si hay algún par sin camino. La respuesta es única. (Con una sola persona no se
prueba: el enunciado no dice qué pasa sin pares.)
El solucionador es propio: un recorrido en anchura desde cada persona (la solución del repo usa
Floyd-Warshall). Validado contra Floyd-Warshall y contra fuerza bruta en miles de redes pequeñas.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-4/EJ_11-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["dist[x][y] = dist[y][x] = 1;", "dist[x][y] = 1;"],
}


def resuelve(P, relaciones):
    ids = {}
    ady = [[] for _ in range(P)]
    for a, b in relaciones:
        for x in (a, b):
            if x not in ids:
                ids[x] = len(ids)
        ady[ids[a]].append(ids[b])
        ady[ids[b]].append(ids[a])
    grado = 0
    for s in range(P):
        d = [-1] * P
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in ady[u]:
                if d[w] < 0:
                    d[w] = d[u] + 1
                    q.append(w)
        if min(d) < 0:
            return "DESCONECTADA"
        grado = max(grado, max(d))
    return str(grado)


def floyd(P, relaciones):
    ids = {}
    INF = 10 ** 6
    d = [[INF] * P for _ in range(P)]
    for i in range(P):
        d[i][i] = 0
    for a, b in relaciones:
        for x in (a, b):
            if x not in ids:
                ids[x] = len(ids)
        d[ids[a]][ids[b]] = d[ids[b]][ids[a]] = 1
    for k in range(P):
        for i in range(P):
            for j in range(P):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    m = max(max(f) for f in d)
    return "DESCONECTADA" if m >= INF else str(m)


def nombre(k, largo=0):
    s = "".join(chr(97 + (k // 26 ** i) % 26) for i in range(3)).capitalize()
    return s + "x" * max(0, largo - len(s))


def texto(casos):
    out = [str(len(casos))]
    for P, rel in casos:
        out.append(f"{P} {len(rel)}")
        out += [f"{a} {b}" for a, b in rel]
    return "\n".join(out) + "\n"


def salida(casos):
    return "".join(resuelve(P, r) + "\n" for P, r in casos)


# ------------------------------------------------------------ redes
def camino(P, desde=0):
    return (P, [(nombre(i + desde), nombre(i + 1 + desde)) for i in range(P - 1)])


def mezcla(rng, red):
    """Mismas relaciones en otro orden: los números de las personas dejan de seguir la cadena."""
    P, rel = red
    rel = list(rel)
    rng.shuffle(rel)
    return (P, rel)


def anillo(P):
    return (P, [(nombre(i), nombre((i + 1) % P)) for i in range(P)])


def estrella(P):
    return (P, [(nombre(0), nombre(i)) for i in range(1, P)])


def completo(P):
    return (P, [(nombre(i), nombre(j)) for i in range(P) for j in range(i + 1, P)])


def alea(rng, P, R, conexo=False):
    rel = []
    if conexo:
        orden = list(range(P))
        rng.shuffle(orden)
        for i in range(1, P):
            rel.append((nombre(orden[i]), nombre(orden[rng.randrange(i)])))
    while len(rel) < R:
        a, b = rng.sample(range(P), 2)
        rel.append((nombre(a), nombre(b)))
    rng.shuffle(rel)
    return (P, rel[:max(R, P - 1 if conexo else 0)])


def _asegura():
    r = random.Random(3)
    for _ in range(600):
        P = r.randint(2, 9)
        rel = [tuple(nombre(x) for x in r.sample(range(P), 2)) for _ in range(r.randint(0, 14))]
        assert resuelve(P, rel) == floyd(P, rel), (P, rel)


_asegura()


def pruebas():
    rng = random.Random(1104)
    L = []

    def prueba(nombre_, tipo, casos, comprueba, si, pistas):
        for P, rel in casos:
            assert 1 <= P <= 500 and len(rel) <= 10000
            assert all(a != b and len(a) <= 10 and len(b) <= 10 for a, b in rel)
            assert len({x for r in rel for x in r}) <= P
        L.append(Prueba(nombre_, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplos del enunciado", "enunciado",
           [(4, [("Marta", "Mario"), ("Mario", "Roberto"), ("Roberto", "Raquel"), ("Mario", "Raquel")]),
            (4, [("Roberto", "Mario"), ("Marta", "Raquel")]),
            (5, [("Lucia", "Pablo"), ("Pablo", "Elena"), ("Elena", "Lucia"), ("Lucia", "Jorge")])],
           "Los tres casos del enunciado: grado 2, dos parejas sin conexión y una persona que no sale en ninguna relación.",
           {"wa": "Falla el ejemplo: mira cuál de los tres casos es (la línea). Los dos últimos deben dar DESCONECTADA: una red es desconectada si algún par no tiene camino, aunque la persona aislada no salga en ninguna relación.",
            "pe": "Escribe un resultado por línea: un número, o la palabra DESCONECTADA."},
           ["En el caso 3 hay 5 personas pero solo 4 nombres en las relaciones: ¿cuenta la quinta?",
            "Matriz P × P con infinito donde no se sabe nada: la persona que no sale en ninguna relación se queda con infinito a todos.",
            "El grado es el máximo de la matriz de distancias; si queda algún infinito, DESCONECTADA."])

    # ------------------------------------------------------------------ bordes
    prueba("Dos personas", "borde", [(2, [("Ana", "Beto")]), (2, []), (2, [("Ana", "Beto"), ("Beto", "Ana"), ("Ana", "Beto")])],
           "Una pareja que se conoce (1), una pareja sin relaciones (DESCONECTADA) y una relación repetida de varias formas (1).",
           {"wa": "Con dos personas que se conocen el grado es 1; sin relaciones, DESCONECTADA; una relación repetida no cambia nada.",
            "rte": "Con R = 0 no hay líneas de relaciones: no leas ninguna."},
           ["Con R = 0 hay que seguir leyendo bien el caso siguiente.",
            "La relación es simétrica: «Ana Beto» y «Beto Ana» son la misma."])

    # ------------------------------------------------------------------ trampas
    prueba("Personas que no salen en ninguna relación", "trampa",
           [(3, [("Ana", "Beto")]), (6, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")]), (4, [("W", "X"), ("X", "Y"), ("Y", "Z")]), (3, [("Pepe", "Luis"), ("Luis", "Ana")])],
           "Hay más personas que nombres en las relaciones: las que no salen están aisladas, así que la red está desconectada. El último caso (3 personas, las 3 salen) sí es conexo.",
           {"wa": "Solo cuentas las personas que salen en las relaciones: P es el número TOTAL de personas, y quien no sale en ninguna está aislado (red desconectada). Otra causa frecuente: dar la distancia MENOR (o una media) en vez de la mayor de todos los pares."},
           ["En el primer caso P = 3 y solo salen Ana y Beto: falta alguien.",
            "Crea la matriz (o el grafo) de P × P personas, no del número de nombres distintos que lees."])
    prueba("Todos se conocen", "trampa", [completo(2), completo(3), completo(6), completo(12)],
           "Todos con todos: el grado es 1 (nunca 0, ni 2).",
           {"wa": "En una red completa cualquier par está a una relación: la diagonal (de una persona a sí misma) vale 0, no infinito. Y cada relación se marca en los DOS sentidos: dist[x][y] y dist[y][x]."},
           ["Si dist[i][i] empieza en infinito, el paso de Floyd la rebaja a 2 (ir y volver).",
            "Pon dist[i][i] = 0 antes de empezar."])
    prueba("Una cadena larga", "trampa", [mezcla(rng, camino(10)), mezcla(rng, camino(30)), mezcla(rng, camino(64, 5)), mezcla(rng, camino(100))],
           "Una fila de personas: el grado es P − 1 (los de los extremos están a P − 1 relaciones).",
           {"wa": "Para llegar al final de una cadena larga hay que pasar por todas las personas intermedias: revisa el orden de los tres bucles de Floyd-Warshall (el intermedio k va FUERA).",
            "tle": "Debe ser O(P³) como mucho: cada caso con 500 personas son unas 10⁸ operaciones simples."},
           ["En una cadena de 10 personas el grado es 9; las relaciones llegan mezcladas, así que los números de las personas no van en orden a lo largo de la cadena.",
            "k (el intermedio permitido) debe ser el bucle de fuera, y i, j los de dentro."])
    prueba("Mayor separación, no la media ni la menor", "trampa", [estrella(6), anillo(6), anillo(7), (7, [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "G")])],
           "En una estrella los extremos están a 2 aunque del centro a cada uno haya 1; en un anillo de 6, el opuesto está a 3.",
           {"wa": "El grado de la red es el MÁXIMO de las distancias mínimas entre pares (no la menor, ni la del primero con el último)."},
           ["En la estrella de 6 el centro está a 1 de todos, pero dos hojas están a 2.",
            "Calcula la matriz completa de distancias y quédate con su valor máximo."])
    prueba("La relación vale en los dos sentidos", "trampa", [(4, [("B", "A"), ("B", "C"), ("D", "C")]), (3, [("Z", "Y"), ("Y", "X")]), (5, [("E", "D"), ("D", "C"), ("C", "B"), ("B", "A")])],
           "Los nombres de cada relación van en cualquier orden: «B A» también significa que A conoce a B.",
           {"wa": "La relación es simétrica: debes marcar dist[x][y] y también dist[y][x]."},
           ["En el primer caso A–B–C–D es una cadena aunque las relaciones estén escritas al revés.",
            "dist[x][y] = dist[y][x] = 1."])
    prueba("Mayúsculas y minúsculas son personas distintas", "trampa", [(4, [("Ana", "ana"), ("ana", "ANA"), ("ANA", "Anna")]), (2, [("Pepe", "pepe")])],
           "Los nombres de este caso se parecen pero son personas distintas: Ana, ana, ANA y Anna.",
           {"wa": "Tratas «Ana» y «ana» como la misma persona: los nombres son únicos tal y como se escriben (distinguen mayúsculas)."},
           ["No conviertas los nombres a minúsculas.",
            "Basta un unordered_map<string, int> con el nombre tal cual."])
    prueba("Dos grupos unidos por una sola relación", "trampa",
           [(8, [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D"), ("C", "D"), ("G", "A"), ("H", "F")]),
            (6, [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D")])],
           "Dos triángulos unidos por un puente (conexa, grado 5 con dos colas) y dos triángulos sin puente (DESCONECTADA).",
           {"wa": "Un solo puente conecta toda la red: si queda algún par sin camino es DESCONECTADA; si no, el grado puede ser mayor de lo esperado."},
           ["En el segundo caso no hay ninguna relación entre {A, B, C} y {D, E, F}.",
            "Comprueba que miras TODOS los pares, no solo los vecinos."])
    prueba("Nombres de diez letras", "trampa", [(3, [(nombre(0, 10), nombre(1, 10)), (nombre(1, 10), nombre(2, 10))]), (2, [("abcdefghij", "ABCDEFGHIJ")])],
           "Nombres de la longitud máxima (10 letras).",
           {"wa": "Algo falla al leer nombres largos: léelos como string completos.",
            "rte": "Estás leyendo los nombres en un char[] pequeño: usa string."},
           ["Los nombres tienen hasta 10 letras, sin espacios.",
            "Lee con cin >> string."])
    prueba("Varios casos seguidos", "trampa",
           [camino(30), (3, [("Pepe", "Luis")]), completo(4), (5, [("a", "b"), ("c", "d")]), camino(3), estrella(9)],
           "Una cadena larga y luego redes más pequeñas y desconectadas: nada de lo anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (el mapa de nombres, la matriz o el máximo): créalos dentro de resuelveCaso.",
            "rte": "El mapa de nombres de un caso anterior ya tiene más de P personas: vacíalo (créalo en cada caso)."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de la función.",
            "El unordered_map de nombres debe empezar vacío en cada caso."])

    # ------------------------------------------------------------------ aleatorios
    casos = []
    while len(casos) < 150:
        P = rng.randint(2, 8)
        casos.append(alea(rng, P, rng.randint(0, 14)))
    prueba("Redes pequeñas al azar", "aleatorio", casos,
           "150 redes de hasta 8 personas, con relaciones repetidas, redes conexas y desconectadas.",
           {"wa": "Algún caso falla: es pequeño, dibuja el grafo y calcula a mano las distancias."},
           ["Localiza el caso en la entrada y dibuja la red.",
            "Revisa la persona aislada, el sentido de las relaciones y la diagonal."])
    casos = [alea(rng, P, rng.randint(P - 1, P * 2), conexo=rng.random() < 0.7) for P in (rng.randint(15, 60) for _ in range(40))]
    prueba("Redes medianas al azar", "aleatorio", casos,
           "40 redes de 15 a 60 personas, casi todas conexas (con un grado de separación entre 4 y 15).",
           {"wa": "Los casos pequeños salen bien y estos no: revisa el orden de los bucles de Floyd-Warshall.",
            "tle": "Debe ser O(P³): ¿recalculas las distancias para cada par?"},
           ["Si dibujar a mano es difícil, mira al menos qué caso es el primero que falla.",
            "El intermedio k va en el bucle de fuera."])

    # ------------------------------------------------------------------ rendimiento
    prueba("500 personas en fila", "rendimiento", [camino(500)],
           "El caso más duro para Floyd: una cadena de 500 personas (grado 499).",
           {"tle": "Debe costar unas P³ = 1,25·10⁸ operaciones: con un acceso lento (map<string, …> en cada paso del bucle) se pasa del tiempo.",
            "wa": "En una cadena de 500 el grado es 499: revisa el orden de los bucles y que cabe 499 en el tipo que usas."},
           ["Trabaja con enteros (identificadores), no con nombres, dentro de los bucles.",
            "Matriz<EntInf> P × P y tres bucles anidados."])
    prueba("500 personas con 10.000 relaciones", "rendimiento", [alea(rng, 500, 10000, conexo=True), alea(rng, 500, 10000, conexo=True)],
           "Dos redes de 500 personas con el máximo de relaciones: se lee mucha entrada y se hace Floyd dos veces.",
           {"tle": "Dos casos de P = 500 son 2,5·10⁸ operaciones simples: usa enteros y evita copiar la matriz.",
            "mle": "Basta una matriz de 500 × 500 enteros."},
           ["Lee las relaciones con cin >> string; si es lento, añade ios::sync_with_stdio(false).",
            "Usa un unordered_map<string, int> para pasar los nombres a números."])
    prueba("500 personas sin relaciones y con muchas repetidas", "rendimiento",
           [(500, []), (300, [(nombre(rng.randrange(5)), nombre(5 + rng.randrange(5))) for _ in range(10000)]), (500, [("Solo", "Dos")])],
           "R = 0 con 500 personas y 10.000 relaciones repetidas sobre muy pocos nombres.",
           {"tle": "Cuando se sabe que está desconectada se puede acabar, pero incluso así debe ser rápido: no repitas trabajo.",
            "wa": "500 personas y R = 0 es DESCONECTADA; 300 personas con solo 10 nombres también (faltan personas)."},
           ["Muchas relaciones repetidas no cambian el grafo.",
            "Las personas que faltan en las relaciones están aisladas: DESCONECTADA."])
    return L


# ------------------------------------------------------------ variantes (fallos típicos)
VARIANTES = [
    Variante("ignora a las personas que no salen", [("    // quien no sale en ninguna relacion se queda con distancia infinita a todos los demas\n", "    P = numero.size();\n")], prueba=3, v="wa"),
    Variante("el grado es la menor distancia", [("EntInf grado = 0;", "EntInf grado = Infinito;"), ("if (dist[i][j] > grado) grado = dist[i][j];", "if (i != j && dist[i][j] < grado) grado = dist[i][j];")], prueba=3, v="wa"),
    Variante("la relación solo vale en un sentido", [("dist[x][y] = dist[y][x] = 1;", "dist[x][y] = 1;")], prueba=4, v="wa"),
    Variante("el intermedio k va dentro (orden de bucles)", [("for (int k = 0; k < P; ++k)\n        for (int i = 0; i < P; ++i) {", "for (int i = 0; i < P; ++i)\n        for (int k = 0; k < P; ++k) {")], prueba=5, v="wa"),
    Variante("la diagonal no vale 0", [("    for (int i = 0; i < P; ++i) dist[i][i] = 0;\n", "")], prueba=4, v="wa"),
    Variante("DESCONECTADA mal escrita", [('cout << "DESCONECTADA\\n";', 'cout << "Desconectada\\n";')], prueba=3, v="wa"),
    Variante("nombres en minúsculas", [("        int x = id(a), y = id(b);", "        for (char& c : a) c = tolower(c);\n        for (char& c : b) c = tolower(c);\n        int x = id(a), y = id(b);")], prueba=8, v="wa"),
]
