"""06-4 · La selva de Tarzán: juez con pruebas pensadas para cada error típico.

Entrada: selvas hasta el final del fichero; cada una «N M» y M saltos «árbol árbol longitud».
Salida: la longitud mínima de cuerda para ir de cualquier árbol a cualquier otro (la arista más
larga de un árbol de recubrimiento mínimo), o «Imposible».
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-4/EJ_06-4.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-4/GrafoValorado.h",
                  "6-Conjuntos disjuntos y grafos valorados/EJ_06-4/ConjuntosDisjuntos.h"],
    "limite_ms": 3000,
    "fallo": ["ultima = s.valor();", "ultima += s.valor();"],
}


def resuelve(N, saltos):
    """Solucionador independiente: añade saltos de menor a mayor hasta que todo queda conectado."""
    padre = list(range(N + 1))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    grupos, cuerda = N, 0
    for u, v, l in sorted(saltos, key=lambda s: s[2]):
        if grupos == 1:
            break
        a, b = raiz(u), raiz(v)
        if a != b:
            padre[a] = b
            grupos -= 1
            cuerda = l
    return (str(cuerda) if grupos == 1 else "Imposible") + "\n"


def caso_a_texto(N, saltos):
    return f"{N} {len(saltos)}\n" + "".join(f"{u} {v} {l}\n" for u, v, l in saltos)


def aleatorio(rng, N, M, lmax):
    saltos = []
    for _ in range(M if N > 1 else 0):
        u = rng.randint(1, N)
        v = rng.randint(1, N - 1)
        if v >= u:
            v += 1
        saltos.append((u, v, rng.randint(1, lmax)))
    return N, saltos


def grande(rng):
    """10.000 árboles y 100.000 saltos; el árbol 10.000 solo se alcanza con el salto más largo."""
    N = 10000
    saltos = [(k, rng.randint(1, k - 1), rng.randint(1, 999998)) for k in range(2, N)]
    while len(saltos) < 99999:
        u, v = rng.randint(1, N - 1), rng.randint(1, N - 1)
        if u != v:
            saltos.append((u, v, rng.randint(1, 999998)))
    saltos.append((rng.randint(1, N - 1), N, 1000000))
    rng.shuffle(saltos)
    return N, saltos


def cadena_profunda():
    """Para conjuntos disjuntos sin unión por tamaños ni compresión: los saltos «k k+1» forman
    una cadena de 9.999 árboles y luego muchos saltos que sobran entre árboles del principio."""
    N = 10000
    saltos = [(k, k + 1, k) for k in range(1, N - 1)]
    extra, m = [], 0
    while len(extra) < 85000:
        m += 1
        for a in range(1, m - 1):
            extra.append((a, m, 20000 + len(extra)))
    saltos += extra[:85000]
    saltos.append((N - 1, N, 1000000))
    return N, saltos


def pruebas():
    rng = random.Random(64)
    ej1 = (4, [(1, 2, 5), (2, 3, 10), (3, 1, 7), (2, 4, 8)])
    ej2 = (1, [])
    ej3 = (4, [(1, 2, 3), (4, 3, 5)])
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ej1],
           "El primer ejemplo del PDF: 4 árboles y 4 saltos; la cuerda debe medir 8.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la respuesta es el salto MÁS LARGO que hace falta, no la suma ni el mínimo.",
            "rte": "Se rompe con el ejemplo: revisa la lectura (la entrada no empieza con el número de casos: se lee hasta el final del fichero)."},
           ["Ejecútalo en tu ordenador con el ejemplo y compara.",
            "Con una cuerda de 8 se pueden hacer los saltos de 5, 7 y 8, que unen los 4 árboles.",
            "Es Kruskal: mete saltos de menor a mayor y quédate con la longitud del último que une dos grupos."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ej2],
           "El segundo ejemplo: un solo árbol y ningún salto; la cuerda mide 0.",
           {"wa": "Con un solo árbol no hace falta saltar: la respuesta es 0, no «Imposible»."},
           ["Con N = 1 ya se puede ir de cualquier árbol a cualquier otro.",
            "Comprueba «queda un solo grupo», no «he elegido algún salto»."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [ej3],
           "El tercer ejemplo: los saltos no llegan a todos los árboles («Imposible»).",
           {"wa": "Si los saltos no unen todos los árboles hay que escribir exactamente «Imposible» (con mayúscula inicial)."},
           ["Con los saltos 1–2 y 4–3 quedan dos grupos.",
            "Al acabar, si num_cjtos() > 1, escribe «Imposible»."])
    prueba("Dos árboles y un salto", "borde", [(2, [(2, 1, 1000000)]), (2, [(1, 2, 1)])],
           "La selva más pequeña que necesita cuerda.",
           {"wa": "Con dos árboles y un salto, la cuerda mide lo que ese salto."},
           ["Con dos árboles basta el único salto que hay.",
            "Revisa la condición de parada: hay que llegar a un solo grupo."])
    # --- Trampas. El orden importa: las primeras no deben fallar por los errores que buscan las siguientes.
    prueba("Árboles numerados desde 1", "trampa", [(2, [(2, 1, 7)])],
           "Saltos que tocan el árbol N: hay que pasar de 1..N a 0..N−1.",
           {"rte": "Usas el número de árbol tal cual: el árbol N se sale del grafo. Lee con GrafoValorado<int>(cin, 1) o resta 1 a cada árbol.",
            "wa": "Los árboles se desplazan: resta 1 a los dos árboles de cada salto."},
           ["El salto «2 1 7» toca el último árbol: ¿existe el vértice 2 en tu grafo?",
            "GrafoValorado<int>(cin, 1) resta 1 al leer: los vértices van de 0 a N − 1."])
    prueba("Un solo árbol", "trampa", [(1, []), (3, [(1, 2, 2), (2, 3, 6)])],
           "Con un árbol la cuerda mide 0 y es una respuesta válida, no «Imposible».",
           {"wa": "Usas «cuerda == 0» o «no he elegido ningún salto» como señal de imposible. Con N = 1 ya hay un solo grupo: la respuesta es 0."},
           ["¿Qué escribe tu programa con «1 0»? Debe ser «0».",
            "Decide con num_cjtos() == 1 (o con N − 1 saltos elegidos), no con el valor de la cuerda."])
    prueba("La cuerda es el salto más largo, no la suma", "trampa",
           [(3, [(1, 2, 4), (2, 3, 6)]), (4, [(1, 2, 1), (2, 3, 1), (3, 4, 1)])],
           "Tarzán usa la misma cuerda en cada salto: basta con que llegue al más largo.",
           {"wa": "Sumas las longitudes de los saltos (como en el archipiélago, 06-3). Aquí la cuerda tiene que llegar al salto más largo: es un máximo, no una suma."},
           ["En el primer caso, con una cuerda de 6 se hacen los saltos de 4 y de 6: la respuesta es 6, no 10.",
            "Guarda la longitud del último salto que Kruskal acepta (es el mayor de los aceptados)."])
    prueba("Un salto muy largo que no hace falta", "trampa",
           [(3, [(1, 2, 3), (2, 3, 4), (1, 3, 900)]), (4, [(1, 2, 5), (2, 3, 5), (3, 4, 5), (4, 1, 6), (1, 3, 1000000)])],
           "No vale la longitud del salto más largo de la selva: solo cuentan los que hacen falta.",
           {"wa": "Te quedas con el salto más largo de todos (o con el último que miras), aunque una dos árboles que ya estaban unidos. Solo cuenta el último salto ACEPTADO. También pasa si no ordenas los saltos de menor a mayor: el salto largo puede aceptarse antes que los cortos."},
           ["En el primer caso el salto de 900 sobra: 1 y 3 ya se unen por 1–2–3. La cuerda mide 4.",
            "Actualiza la cuerda solo dentro del «if (!unidos(u, v))», o para en cuanto quede un solo grupo."])
    prueba("Saltos en cualquier orden", "trampa",
           [(3, [(1, 2, 50), (1, 3, 40), (2, 3, 1)]), (4, [(1, 4, 9), (1, 2, 8), (2, 3, 2), (3, 4, 3)])],
           "Los saltos no vienen ordenados: hay que meterlos de menor a mayor longitud.",
           {"wa": "No ordenas los saltos por longitud creciente (o los ordenas al revés). Kruskal necesita mirarlos de más corto a más largo."},
           ["En el primer caso bastan los saltos de 1 y 40: la cuerda mide 40, no 50.",
            "Ordena las aristas: sort(v.begin(), v.end()) con Arista ya compara por valor."])
    prueba("Hay que unir todos los árboles, no solo el primero y el último", "trampa",
           [(3, [(1, 3, 1), (2, 3, 5)]), (5, [(1, 5, 2), (2, 3, 3), (3, 4, 4), (4, 5, 7)])],
           "Tarzán quiere ir de CUALQUIER árbol a cualquier otro: hay que conectarlos todos.",
           {"wa": "Paras cuando el árbol 1 y el N quedan unidos (eso es otro problema, el de las minas, 06-5). Aquí hay que seguir hasta que quede un solo grupo."},
           ["En el primer caso los árboles 1 y 3 se unen con 1, pero falta el 2: la cuerda mide 5.",
            "La condición de parada es num_cjtos() == 1."])
    prueba("Selva partida en dos con muchos saltos", "trampa",
           [(5, [(1, 2, 1), (2, 3, 2), (3, 1, 3), (4, 5, 4), (5, 4, 5)]), (4, [(1, 2, 1), (1, 3, 1), (2, 3, 1)])],
           "Hay más saltos que árboles, pero forman dos grupos separados: «Imposible».",
           {"wa": "Escribes una longitud aunque queden árboles inalcanzables: al acabar, comprueba que queda un solo grupo."},
           ["En el primer caso los árboles {1, 2, 3} y {4, 5} no se pueden unir con ninguna cuerda.",
            "Que haya M ≥ N − 1 saltos no garantiza nada: mira num_cjtos() al terminar."])
    prueba("Saltos repetidos entre los mismos árboles", "trampa",
           [(2, [(1, 2, 9), (2, 1, 4)]), (3, [(1, 2, 7), (2, 3, 8), (2, 1, 2), (3, 2, 3)])],
           "Puede haber varios saltos entre los mismos dos árboles con distinta longitud: vale el más corto.",
           {"wa": "Guardas un solo salto por par de árboles (el primero o el último que lees). Guárdalos todos: Kruskal se queda con el más corto y descarta los demás."},
           ["En el primer caso hay dos saltos entre 1 y 2 (9 y 4): la cuerda mide 4.",
            "Con listas de aristas no tienes que hacer nada especial: el más corto se mira antes."])
    prueba("Longitudes extremas", "borde",
           [(3, [(1, 2, 1000000), (2, 3, 1000000)]), (3, [(1, 2, 1), (2, 3, 1)])],
           "Saltos de longitud 1.000.000 y de longitud 1.",
           {"wa": "Con los valores extremos algo falla: ¿inicializas la cuerda o un máximo con un valor que no llega a 1.000.000?"},
           ["La cuerda puede medir 1.000.000.",
            "Si usas un valor «infinito», que sea mayor que 1.000.000."])
    prueba("Varias selvas seguidas", "trampa",
           [(4, [(1, 2, 70), (2, 3, 80), (3, 4, 90)]), (2, [(1, 2, 5)]), (1, []), (3, [(1, 2, 1)]), (2, [(2, 1, 6)])],
           "Una selva con cuerda larga seguida de otras pequeñas: nada de la anterior debe quedar.",
           {"wa": "Algo se arrastra de una selva a la siguiente: la cuerda o la partición se declaran fuera de la función de cada caso (o como static).",
            "rte": "Un vector de una selva anterior con otro tamaño: crea el grafo y los conjuntos disjuntos para cada selva."},
           ["Fíjate en la tercera selva (un solo árbol): debe salir 0, no la cuerda de la selva anterior.",
            "La cuerda tiene que empezar en 0 en cada selva."])
    casos_al = [aleatorio(rng, rng.randint(1, 7), rng.randint(0, 12), rng.choice([4, 20, 1000000])) for _ in range(100)]
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "100 selvas pequeñas al azar, con saltos repetidos y empates.",
           {"wa": "Hay alguna selva concreta que no tratas: la línea que falla es el número de selva; búscala y haz Kruskal a mano."},
           ["La línea que falla es el número de selva: búscala en la entrada.",
            "Ordena sus saltos a mano y ve aceptando los que unen grupos distintos."])
    prueba("Selva grande con un salto largo imprescindible", "rendimiento", [grande(rng)],
           "10.000 árboles y 100.000 saltos; el último árbol solo se alcanza con el salto más largo, así que hay que mirarlos todos.",
           {"tle": "Tu solución no es O(M log M): ¿llamas a g.aristas() (que crea un vector nuevo) dentro del bucle, o compruebas la conexión con un recorrido después de cada salto?",
            "mle": "Gastas demasiada memoria: no copies el vector de saltos ni uses matrices N × N."},
           ["Ordena los saltos UNA vez y recórrelos en ese orden.",
            "Para saber si ya está todo unido usa num_cjtos() (es O(1)), no un recorrido.",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    prueba("Cadena larga de árboles", "rendimiento", [cadena_profunda()],
           "Los saltos cortos forman una fila de 10.000 árboles y después hay muchos saltos que sobran entre árboles del principio.",
           {"tle": "Tus conjuntos disjuntos forman árboles muy altos: usa unión por tamaños y compresión de caminos (como ConjuntosDisjuntos.h).",
            "rte": "La búsqueda recursiva baja demasiado: con unión por tamaños la altura es como mucho log N."},
           ["Sin unión por tamaños, unir la fila árbol a árbol deja una cadena: buscar el representante cuesta N pasos.",
            "Usa la clase ConjuntosDisjuntos de la asignatura."])
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(*c) for c in casos),
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
    Variante("no resta 1 a los árboles", [("GrafoValorado<int> g(cin, 1);", "GrafoValorado<int> g(cin, 0);")], prueba=5, v="rte"),
    Variante("cuerda 0 como señal de imposible", [("if (cd.num_cjtos() == 1) cout << ultima << '\\n';", "if (ultima > 0) cout << ultima << '\\n';")], prueba=6, v="wa"),
    Variante("suma los saltos", [("ultima = s.valor();", "ultima += s.valor();")], prueba=7, v="wa"),
    Variante("no ordena los saltos", [("sort(saltos.begin(), saltos.end());", "")], prueba=[9, 8], v="wa"),
    Variante("salto más largo de todos", [("if (cd.num_cjtos() == 1) break;", "ultima = max(ultima, s.valor());")], prueba=8, v="wa"),
    Variante("para cuando se unen el 1 y el N", [("if (cd.num_cjtos() == 1) break;", "if (cd.unidos(0, g.V() - 1)) break;")], prueba=10, v="wa"),
    Variante("nunca escribe «Imposible»", [("if (cd.num_cjtos() == 1) cout << ultima << '\\n';\n    else cout << \"Imposible\\n\";", "cout << ultima << '\\n';")], prueba=11, v="wa"),
    Variante("cuerda acumulada entre selvas", [("int ultima = 0;", "static int ultima = 0;")], prueba=14, v="wa"),
    Variante("llama a g.aristas() en cada vuelta", [("for (auto const& s : saltos) {", "for (size_t k = 0; k < g.aristas().size(); ++k) {\n        auto const& s = saltos[k];")], prueba=16, v="tle"),
    Variante("conjuntos disjuntos sin optimizar", [('#include "ConjuntosDisjuntos.h"  // estructuras de datos de clase', INGENUA)], prueba=17, v="tle"),
]
