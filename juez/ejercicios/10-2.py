"""10-2 · Construyendo dianas: juez con pruebas pensadas para cada error típico.

Entrada: hasta el final del fichero, casos de dos líneas: «V S» (V 1..50.000, S 1..100) y las S
puntuaciones distintas en orden creciente (1..1.000). Cada sector se puede usar las veces que haga
falta.
Salida: «k: p1 p2 ... pk» con el mínimo número k de dardos y unas puntuaciones que suman V, o
«Imposible». Si hay varias soluciones óptimas vale cualquiera: por eso lleva comprobador propio
(comprobadores/10-2.{py,js}), que acepta cualquier solución óptima con las puntuaciones en
cualquier orden. La salida esperada da las puntuaciones de mayor a menor, como el ejemplo.
El solucionador es propio: un recorrido en anchura sobre las sumas 0..V (cada dardo es una arista
de j a j + p), con el padre de cada suma para reconstruir. Validado contra fuerza bruta.
"""
import random
from itertools import combinations_with_replacement
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "10-Programacion dinamica/EJ_10-2/EJ_10-2.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["dardos[i][j] = min(dardos[i][j], dardos[i][j - p[i]] + 1);", "dardos[i][j] = min(dardos[i][j], dardos[i - 1][j - p[i]] + 1);"],
}


def minimos(V, sectores):
    """dist[j] = mínimo de dardos para sumar j, padre[j] = último sector usado (anchura)."""
    dist, padre = [-1] * (V + 1), [0] * (V + 1)
    dist[0] = 0
    frontera = [0]
    while frontera and dist[V] < 0:
        nueva = []
        for j in frontera:
            for p in sectores:
                k = j + p
                if k <= V and dist[k] < 0:
                    dist[k], padre[k] = dist[j] + 1, p
                    nueva.append(k)
        frontera = nueva
    return dist, padre


def resuelve(V, sectores):
    dist, padre = minimos(V, sectores)
    if dist[V] < 0:
        return "Imposible"
    usados, j = [], V
    while j:
        usados.append(padre[j])
        j -= padre[j]
    return f"{dist[V]}: " + " ".join(map(str, sorted(usados, reverse=True)))


def otra(V, sectores):
    """Otra solución óptima: reconstruye con el sector MÁS PEQUEÑO posible en cada paso y la
    escribe de menor a mayor."""
    dist, _ = minimos(V, sectores)
    if dist[V] < 0:
        return "Imposible"
    # mejor[j] = mínimo de dardos para sumar j (tabla completa, por si la anchura paró antes)
    INF = float("inf")
    mejor = [0] + [INF] * V
    for j in range(1, V + 1):
        mejor[j] = min((mejor[j - p] + 1 for p in sectores if p <= j), default=INF)
    usados, j = [], V
    while j:
        p = next(p for p in sectores if p <= j and mejor[j - p] == mejor[j] - 1)
        usados.append(p)
        j -= p
    return f"{len(usados)}: " + " ".join(map(str, sorted(usados)))


def ALTERNATIVA(entrada):
    """Otra respuesta correcta (el enunciado admite cualquier solución óptima): el verificador
    comprueba que el comprobador la acepta."""
    v = list(map(int, entrada.split()))
    p, out = 0, []
    while p + 1 < len(v):
        V, S = v[p], v[p + 1]
        out.append(otra(V, v[p + 2:p + 2 + S]))
        p += 2 + S
    return "\n".join(out) + "\n"


def fuerza_bruta(V, sectores):
    for k in range(1, V // min(sectores) + 1):
        for c in combinations_with_replacement(sectores, k):
            if sum(c) == V:
                return k
    return None


def caso_a_texto(caso):
    V, s = caso
    return f"{V} {len(s)}\n" + " ".join(map(str, s)) + "\n"


def aleatorio(rng, V, S, pmax):
    return V, sorted(rng.sample(range(1, pmax + 1), S))


def pruebas():
    rng = random.Random(1002)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas, fin=""):
        P.append((nombre, tipo, casos, comprueba, si, pistas, fin))

    prueba("Ejemplos del enunciado", "enunciado", [(100, [10, 15, 20, 25, 30]), (8, [1, 4, 6]), (25, [8, 12])],
           "Los tres casos de ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: es el problema del cambio con monedas ilimitadas; dardos(i, j) = mínimo de dardos para sumar j con los sectores 1..i.",
            "pe": "Los datos están bien, pero el formato no: el número de dardos, dos puntos pegados y cada puntuación precedida de un espacio («4: 25 25 25 25»)."},
           ["Haz a mano la tabla del segundo caso (V = 8, sectores 1, 4 y 6).",
            "dardos(i, j) = min(dardos(i−1, j), dardos(i, j − p_i) + 1) si p_i ≤ j: se queda en la fila i porque el sector se puede repetir.",
            "Para escribir las puntuaciones, recorre la tabla desde (S, V) hacia atrás."])
    prueba("Un solo dardo", "borde", [(1, [1]), (1000, [1, 500, 1000]), (7, [7])],
           "V coincide con un sector: «1: V».",
           {"wa": "Con V igual a un sector basta un dardo: revisa los casos base (dardos(·, 0) = 0)."},
           ["¿Qué escribes con V = 7 y un único sector de 7?",
            "El caso base es dardos(i, 0) = 0: con 0 puntos no hace falta ningún dardo."])
    prueba("Valor menor que todos los sectores", "borde", [(1, [2]), (5, [6, 7, 8])],
           "V es menor que la puntuación más pequeña: Imposible.",
           {"wa": "Si V es menor que todos los sectores no se puede: la respuesta es «Imposible».",
            "rte": "Con p_i > j accedes a la posición j − p_i < 0 de la tabla: comprueba p_i ≤ j antes."},
           ["Con V = 1 y un sector de 2, ¿qué casilla de la tabla miras?",
            "Solo se puede usar el sector i para la suma j si p_i ≤ j."])
    prueba("Fin de la entrada", "trampa", [(15, [5, 10])],
           "Un único caso y nada más: la entrada acaba con el fichero, sin número de casos ni centinela.",
           {"wa": "Escribes más líneas de las que tocan: casi seguro tu bucle procesa una vez de más el final del fichero (por ejemplo, con while (!cin.eof())). Lee el caso y comprueba si la lectura ha fallado antes de resolverlo.",
            "tle": "Tu programa no detecta el final de la entrada y se queda esperando o dando vueltas."},
           ["¿Cuántas líneas escribe tu programa con esta entrada? Debe ser exactamente una.",
            "Lee V y S y, si la lectura ha fallado (if (!cin)), termina; no uses eof() antes de leer."])
    prueba("Formato de la respuesta", "trampa", [(30, [10, 20])],
           "«2: 20 10»: el número de dardos, dos puntos pegados y las puntuaciones separadas por un espacio.",
           {"pe": "Los datos son correctos pero el formato no: «2: 20 10», con los dos puntos pegados al número y un espacio antes de cada puntuación.",
            "wa": "Revisa qué escribes: primero el número de dardos, luego dos puntos y luego las puntuaciones."},
           ["Compara tu salida carácter a carácter con «2: 20 10».",
            "Escribe el número, «:» y, por cada puntuación, un espacio seguido de ella; al final, un salto de línea."])
    prueba("Un sector se puede repetir", "trampa", [(8, [4])],
           "Un único sector de 4 y V = 8: «2: 4 4». Cada sector se puede usar varias veces.",
           {"wa": "Usas cada sector una sola vez (como en la mochila 0/1). Aquí los sectores son ilimitados: la recurrencia debe quedarse en la misma fila, dardos(i, j − p_i) + 1.",
            "rte": "Al reconstruir, después de usar un sector pasas al anterior: si el sector se repite, te sales de la tabla. Tras usar el sector i quédate en la fila i.",
            "tle": "Al reconstruir no avanzas: después de usar el sector i, resta su puntuación a j."},
           ["Con un solo sector de 4, ¿cuánto vale tu dardos(1, 8)?",
            "En la opción de usar el sector i, la casilla es dardos(i, j − p_i) (misma fila), no dardos(i − 1, j − p_i).",
            "Al reconstruir, si usas el sector i, resta p_i a j y NO cambies de fila."])
    prueba("Imposible por paridad", "trampa", [(7, [2, 4, 6])],
           "Con puntuaciones pares no se consigue un valor impar: «Imposible».",
           {"wa": "Escribes otra cosa en vez de «Imposible» (revisa la ortografía, con mayúscula) o tu «infinito» desborda: INT_MAX + 1 es negativo y parece una solución.",
            "rte": "Tu infinito desborda (INT_MAX + 1) y luego la reconstrucción se sale de la tabla. No sumes 1 a una casilla que vale infinito.",
            "tle": "Tu infinito desborda (INT_MAX + 1) y la reconstrucción no termina. No sumes 1 a una casilla que vale infinito.",
            "ole": "Tu infinito desborda (INT_MAX + 1) y la reconstrucción escribe sin parar. No sumes 1 a una casilla que vale infinito."},
           ["¿Cuánto vale INT_MAX + 1 en un int?",
            "Antes de usar dardos(i, j − p_i) + 1, comprueba que esa casilla no es infinito (o usa un infinito que no desborde).",
            "Si al final dardos(S, V) es infinito, escribe exactamente «Imposible»."])
    prueba("El voraz no sirve", "trampa", [(12, [1, 6, 9])],
           "Tirar siempre al sector más alto que cabe (9 + 1 + 1 + 1) gasta 4 dardos; lo óptimo es 6 + 6.",
           {"wa": "Eliges siempre la puntuación más alta que cabe: eso es un voraz y no da el mínimo. Hace falta la tabla de programación dinámica."},
           ["¿Cuántos dardos hacen falta para 12 con 1, 6 y 9?",
            "La tabla prueba, para cada suma, todas las puntuaciones posibles para el último dardo."])
    prueba("Muchos dardos", "trampa", [(50000, [1]), (50000, [999, 1000]), (49999, [2, 1000])],
           "V = 50.000: hasta 50.000 dardos en la respuesta (o Imposible).",
           {"wa": "Con valores grandes algo falla: ¿la tabla llega hasta V incluido? ¿escribes todas las puntuaciones?",
            "rte": "La tabla debe tener V + 1 columnas (de 0 a V) y S + 1 filas.",
            "tle": "Pruebas todas las combinaciones de dardos (recursión sin memoria): con V = 50.000 no termina. Guarda cada dardos(i, j) en la tabla."},
           ["Con un único sector de 1 y V = 50.000 hay que escribir 50.000 unos.",
            "Revisa el tamaño de la tabla: (S + 1) × (V + 1)."])
    prueba("Varias soluciones óptimas", "trampa", [(10, list(range(1, 10))), (60, [10, 20, 30, 40, 50])],
           "Hay muchas formas óptimas: vale cualquiera, pero tiene que sumar V y usar el mínimo de dardos.",
           {"wa": "Tu número de dardos o tus puntuaciones no cuadran: comprueba que la reconstrucción suma V y usa exactamente el mínimo."},
           ["Suma las puntuaciones que escribes: ¿dan V?",
            "Reconstruye desde (S, V): si dardos(i, j) == dardos(i−1, j), sube de fila; si no, usa el sector i y resta p_i."])
    prueba("Hay que combinar sectores", "trampa", [(11, [3, 5]), (13, [2, 5, 9])],
           "Para 11 con 3 y 5 hacen falta los dos sectores (5 + 3 + 3); para 13 con 2, 5 y 9, «3: 9 2 2».",
           {"wa": "Tu tabla no combina bien los sectores: revisa que en cada casilla pruebas tanto no usar el sector i como usarlo una vez más."},
           ["Haz a mano la tabla de V = 11 con los sectores 3 y 5.",
            "dardos(i, j) = min(dardos(i−1, j), dardos(i, j − p_i) + 1): las dos opciones en cada casilla."])
    prueba("Varios casos seguidos", "trampa", [(1000, [7, 300, 1000]), (9, [3]), (4, [3]), (6, [1, 3])],
           "Un caso grande y luego otros más pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: crea la tabla (y los sectores) dentro de la función de cada caso.",
            "rte": "La tabla de un caso anterior tiene otro tamaño: créala en cada caso con (S + 1) × (V + 1)."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara la tabla y el vector de sectores dentro de la función de cada caso."], fin="\n")
    peq = []
    while len(peq) < 120:
        S = rng.randint(1, 5)
        peq.append(aleatorio(rng, rng.randint(1, 60), S, rng.choice([10, 20, 30])))
    prueba("Aleatorios pequeños", "aleatorio", peq,
           "120 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; hazlo a mano."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Revisa la recurrencia (misma fila al usar un sector) y el «Imposible»."])
    gr = [aleatorio(rng, rng.randint(1000, 50000), rng.randint(1, 100), 1000) for _ in range(6)] + \
         [aleatorio(rng, rng.randint(1000, 50000), rng.randint(2, 6), 1000) for _ in range(4)]
    prueba("Aleatorios grandes", "aleatorio", gr,
           "10 dianas con valores de hasta 50.000.",
           {"wa": "Falla en casos grandes: revisa el infinito y el tamaño de la tabla.",
            "tle": "Tu solución es lenta: debe ser O(S · V) por caso."},
           ["¿Calculas cada casilla una sola vez?",
            "Rellena la tabla con dos bucles: sectores por fuera y sumas por dentro."])
    maxi = [aleatorio(rng, 50000 - k, 100, 1000) for k in range(8)]
    prueba("Muchos casos de tamaño máximo", "rendimiento", maxi,
           "8 dianas de 100 sectores con V cerca de 50.000.",
           {"tle": "Tu solución es lenta para S = 100 y V = 50.000: debe ser O(S · V). Una recursión sin memoria (probar todos los dardos) no termina nunca.",
            "mle": "Gastas demasiada memoria: la tabla (S + 1) × (V + 1) de int ocupa unos 20 MB; no uses long long ni varias copias."},
           ["Si usas recursión, guarda cada resultado en la tabla la primera vez.",
            "Una tabla de int de 101 × 50.001 basta; no la copies al pasarla a funciones (usa referencias)."])
    for casos in (x[2] for x in P):
        for V, s in casos:
            assert 1 <= V <= 50000 and 1 <= len(s) <= 100 and s == sorted(set(s)) and all(1 <= p <= 1000 for p in s)
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(c) for c in casos) + fin,
                   salida="".join(resuelve(*c) + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas, fin in P]


VARIANTES = [
    Variante("sin espacio tras los dos puntos", [("cout << dardos[S][V] << ':';", "cout << dardos[S][V] << ':';  bool pr = true;"),
                                                 ("else { cout << ' ' << p[i]; j -= p[i]; }", "else { if (!pr) cout << ' '; pr = false; cout << p[i]; j -= p[i]; }")], prueba=1, v="pe"),
    Variante("bucle con eof()", [("bool resuelveCaso() {\n    int V, S;\n    cin >> V >> S;\n    if (!cin)  // fin de la entrada\n        return false;",
                                  "bool resuelveCaso() {\n    if (cin.eof()) return false;\n    int V = 0, S = 0;\n    cin >> V >> S;")], prueba=4, v="wa"),
    Variante("sectores usados una sola vez (0/1)", [("dardos[i][j] = min(dardos[i][j], dardos[i][j - p[i]] + 1);", "dardos[i][j] = min(dardos[i][j], dardos[i - 1][j - p[i]] + 1);")], prueba=6, v="wa"),
    Variante("al reconstruir cambia de sector tras usarlo", [("else { cout << ' ' << p[i]; j -= p[i]; }", "else { cout << ' ' << p[i]; j -= p[i]; --i; }")], prueba=6, v="rte"),
    Variante("infinito = INT_MAX en int, sin EntInf (la suma desborda)",
             [("#include <vector>", "#include <vector>\n#include <climits>"),
              ("Matriz<EntInf> dardos(S + 1, V + 1, Infinito);", "Matriz<int> dardos(S + 1, V + 1, INT_MAX);"),
              ("if (dardos[S][V] == Infinito)", "if (dardos[S][V] == INT_MAX)")], prueba=7, v="rte"),
    Variante("escribe IMPOSIBLE", [('cout << "Imposible\\n";', 'cout << "IMPOSIBLE\\n";')], prueba=7, v="wa"),
    Variante("voraz: el sector más alto que cabe",
             [("bool resuelveCaso() {\n    int V, S;\n    cin >> V >> S;\n    if (!cin)  // fin de la entrada\n        return false;",
               "bool resuelveCaso() {\n    int V, S;\n    cin >> V >> S;\n    if (!cin) return false;\n"
               "    { vector<int> q(S); for (int& x : q) cin >> x; vector<int> u; int r = V;\n"
               "      for (int k = S - 1; k >= 0; --k) while (q[k] <= r) { u.push_back(q[k]); r -= q[k]; }\n"
               "      if (r) cout << \"Imposible\\n\"; else { cout << u.size() << ':'; for (int x : u) cout << ' ' << x; cout << '\\n'; }\n"
               "      return true; }")], prueba=8, v="wa"),
    Variante("recursión sin memoria",
             [("bool resuelveCaso() {",
               "#include <climits>\nint rec(const vector<int>& p, int j) {\n    if (j == 0) return 0;\n    int m = INT_MAX;\n"
               "    for (size_t k = 1; k < p.size(); ++k) if (p[k] <= j) { int r = rec(p, j - p[k]); if (r != INT_MAX) m = min(m, r + 1); }\n    return m;\n}\n"
               "bool resuelveCaso() {\n    { int V, S; cin >> V >> S; if (!cin) return false; vector<int> p(S + 1); for (int i = 1; i <= S; ++i) cin >> p[i];\n"
               "      int r = rec(p, V); if (r == INT_MAX) { cout << \"Imposible\\n\"; return true; }\n"
               "      cout << r << ':'; int j = V; while (j > 0) for (int i = S; i >= 1; --i) if (p[i] <= j && rec(p, j - p[i]) == r - 1) { cout << ' ' << p[i]; j -= p[i]; --r; break; }\n"
               "      cout << '\\n'; return true; }")], prueba=9, v="tle"),
]
