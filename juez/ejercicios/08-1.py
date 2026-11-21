"""08-1 · Agujeros en la manguera: juez con pruebas pensadas para cada error típico.

El solucionador (parche que empieza en el primer agujero sin tapar) se ha validado contra fuerza
bruta (probar todos los conjuntos de comienzos de parche) en miles de casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "8-Algoritmos voraces/EJ_08-1/EJ_08-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["if (p > finParche) {", "if (p >= finParche) {"],
}


def parches(L, pos):
    n, hasta = 0, None
    for p in pos:
        if hasta is None or p > hasta:
            n += 1
            hasta = p + L
    return n


def caso_a_texto(c):
    L, pos = c
    return f"{len(pos)} {L}\n" + " ".join(map(str, pos)) + "\n"


def al_azar(rng, n, L, tope):
    return (L, sorted(rng.randint(1, tope) for _ in range(n)))


def pruebas():
    rng = random.Random(801)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{parches(*c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [(2, [1, 6, 10]), (5, [1, 7, 10]), (10, [3, 8, 8, 9, 20, 45, 55, 90])],
           "Los tres casos del PDF, incluido un agujero justo en el borde del parche (el 55).",
           {"wa": "Si falla hasta el ejemplo, revisa la idea básica: cada parche nuevo empieza en el primer agujero que sigue sin tapar y llega hasta esa posición más L.",
            "pe": "Los números están bien pero el formato no: un número por línea, uno por caso."},
           ["Sigue a mano el tercer caso: el primer parche va de 3 a 13, el segundo empieza en 20…",
            "Recuerda que la línea del caso trae primero N (agujeros) y después L (longitud del parche).",
            "Guarda hasta dónde llega el último parche; si un agujero queda más allá, pon un parche nuevo que empiece en él."])

    # ------------------------------------------------------------------ borde
    prueba("Un solo agujero", "borde", [(5, [7])],
           "N = 1: hace falta exactamente un parche.",
           {"wa": "Con un único agujero la respuesta es 1. Si sale 0, cuentas los parches al «cerrarlos» y te olvidas del último; si sale 2, cuentas uno de más al empezar."},
           ["¿Qué escribe tu programa con «1 5» y el agujero 7?",
            "Si cuentas el parche cuando encuentras un agujero fuera del anterior, el primero también cuenta: inicializa para que el primer agujero siempre abra parche."])
    prueba("Todos los agujeros en la misma posición", "borde", [(1, [1000000000] * 6)],
           "Seis agujeros en la posición 10⁹: un solo parche los tapa todos.",
           {"wa": "Los agujeros repetidos están en el mismo sitio: un parche los tapa a la vez. ¿Cuentas un parche por agujero o comparas con < en vez de con ≤?"},
           ["Un parche que empieza en p tapa todo lo que hay en [p, p + L], y p está dentro.",
            "Abre parche nuevo solo si el agujero está ESTRICTAMENTE más allá de donde llega el último parche."])

    # ------------------------------------------------------------------ trampas
    prueba("Los parches no van en posiciones fijas", "trampa", [(3, [2, 4])],
           "Agujeros en 2 y 4 con L = 3: un parche de 2 a 5 los tapa (1 parche). No hay que dividir la manguera en tramos fijos [0, L), [L, 2L)…",
           {"wa": "Sale 2: repartes la manguera en tramos fijos (p / L) en vez de colocar cada parche donde empieza el primer agujero sin tapar."},
           ["Un parche se puede colocar en cualquier sitio, no solo en múltiplos de L.",
            "Empieza cada parche justo en el primer agujero que queda sin tapar."])
    prueba("Agujero justo en el extremo del parche", "trampa", [(3, [1, 4])],
           "Agujeros en 1 y 4 con parches de 3: el parche de 1 a 4 tapa los dos (el borde cuenta).",
           {"wa": "Sale 2: no tapas el agujero que queda justo en el borde. Un parche de longitud L que empieza en p llega hasta p + L INCLUIDO (en el ejemplo, el 55 lo tapa el parche de 45)."},
           ["¿Hasta dónde llega un parche de longitud 3 colocado en la posición 1?",
            "Llega hasta 1 + 3 = 4, incluido: si dos agujeros están a distancia L, basta un parche.",
            "Abre parche nuevo solo cuando p > finParche (no ≥), con finParche = inicio + L (no inicio + L - 1)."])
    prueba("Parches de longitud 1", "trampa", [(1, [1, 2, 4, 5])],
           "Agujeros en 1, 2, 4 y 5 con L = 1: un parche tapa el 1 y el 2, y otro el 4 y el 5 (2 parches).",
           {"wa": "Con L = 1 un parche en p tapa p y p + 1. Si sale 4, el parche no llega a su extremo (usas ≥ al comparar o restas 1 al calcular dónde acaba)."},
           ["Un parche de longitud 1 en la posición 1 tapa el 1 y el 2.",
            "La distancia entre el primer y el último agujero que tapa un parche puede ser L, no L - 1."])
    prueba("Un hueco de L + 1 ya no cabe", "trampa", [(5, [1, 7])],
           "Agujeros en 1 y 7 con L = 5: el parche de 1 llega a 6 y el 7 necesita otro (2 parches).",
           {"wa": "Sale 1: tu parche llega más lejos de la cuenta. Un parche que empieza en p acaba en p + L, no en p + L + 1."},
           ["El parche de longitud 5 colocado en 1 va de 1 a 6.",
            "Revisa la cuenta del final del parche: inicio + L, exactamente."])
    prueba("Huecos pequeños encadenados", "trampa", [(2, [1, 3, 5, 7, 9])],
           "Agujeros cada 2 con L = 2: cada parche tapa dos agujeros seguidos y hacen falta 3, aunque ningún hueco sea mayor que L.",
           {"wa": "Sale 1: comparas cada agujero con el ANTERIOR y no con el comienzo del parche. Los huecos pequeños se van acumulando: el parche que empieza en 1 no llega al 5."},
           ["¿Puede un parche de longitud 2 tapar a la vez los agujeros 1 y 5?",
            "Lo que importa es la distancia al agujero donde EMPIEZA el parche, no al agujero anterior.",
            "Guarda hasta dónde llega el parche actual (inicio + L) y no lo muevas hasta abrir uno nuevo."])
    prueba("Mucho espacio vacío entre agujeros", "trampa", [(10, [1, 500, 1000])],
           "Tres agujeros muy separados: 3 parches. No se trata de cubrir toda la manguera de punta a punta.",
           {"wa": "Solo hay que tapar los agujeros, no el tramo entero entre el primero y el último: cada agujero aislado necesita un parche."},
           ["¿Cuántos parches de longitud 10 hacen falta para tapar el 1, el 500 y el 1000?",
            "No dividas la longitud total entre L: recorre los agujeros uno a uno."])
    prueba("Repetidos justo después de un parche", "trampa", [(2, [1, 3, 3, 4, 4, 4, 6])],
           "Agujeros 1 3 3 | 4 4 4 6 con L = 2: el primer parche tapa 1 y los dos 3; el segundo, los tres 4 y el 6 (2 parches).",
           {"wa": "Los agujeros repetidos están en el mismo sitio. ¿Abres un parche por cada agujero repetido, o tratas los iguales como si estuvieran separados?"},
           ["Varios agujeros en la misma posición los tapa el mismo parche.",
            "Compara cada agujero con el final del parche actual; los repetidos no cambian nada."])
    prueba("Posiciones cerca de 10⁹", "borde", [(1000, [999998000, 999999000, 999999500, 1000000000])],
           "Posiciones grandes con L = 1000: el parche de 999.998.000 llega justo al 999.999.000; 2 parches.",
           {"wa": "Con posiciones grandes algo se estropea: ¿lees en un tipo demasiado pequeño o inicializas el final del parche con un valor que no sirve?"},
           ["Las posiciones llegan hasta 10⁹: caben en un int, y p + L también (≈ 10⁹ + 1000 < 2³¹).",
            "Inicializa el final del último parche con un valor menor que cualquier posición (por ejemplo -1)."])
    prueba("Varios casos seguidos", "trampa",
           [(1000, [999990000, 1000000000]), (3, [1, 2, 5]), (1, [7]), (5, [1, 7, 10]), (2, [1, 3, 5, 7, 9])],
           "Un caso con posiciones enormes seguido de otros pequeños: nada del caso anterior debe quedar.",
           {"wa": "El primer caso sale bien y los siguientes no: el contador de parches o el final del último parche no se reinician en cada caso."},
           ["Si en el segundo caso salen 0 parches o parches de más, mira qué variables viven fuera de resuelveCaso.",
            "Declara el contador y el final del parche dentro de la función de cada caso (y sin static)."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 8), rng.randint(1, 6), rng.choice([10, 20, 40])) for _ in range(150)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "150 casos de hasta 8 agujeros, con repetidos y distancias justo en L.",
           {"wa": "Algún caso falla: localiza la línea, busca ese caso en la entrada y colócalo a mano sobre una recta."},
           ["La línea que falla es el número de caso.",
            "Revisa el borde (≤) y que comparas con el inicio del parche, no con el agujero anterior."])
    casos = [al_azar(rng, rng.randint(100, 2000), rng.randint(1, 1000), rng.choice([10 ** 4, 10 ** 6, 10 ** 9])) for _ in range(40)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "40 casos de 100 a 2.000 agujeros con L y posiciones variadas.",
           {"wa": "Algún caso mediano falla: el error aparece solo en algunas configuraciones. Prueba los casos pequeños al azar primero."},
           ["Compara con un caso pequeño parecido que hagas a mano.",
            "Revisa que el final del parche se calcula desde el agujero donde empieza."])

    # ------------------------------------------------------------------ rendimiento
    casos = []
    for _ in range(10):
        casos.append((1, sorted(rng.randint(1, 9) for _ in range(100000))))
    prueba("10 casos de 100.000 agujeros", "rendimiento", casos,
           "La suma de N llega a 10⁶: la solución debe ser O(N) por caso.",
           {"tle": "Algo cuesta O(N²): ¿borras agujeros del principio del vector (erase(begin())) o vuelves a recorrer desde el principio por cada parche?",
            "wa": "Con muchos agujeros repetidos falla: revisa cómo tratas posiciones iguales."},
           ["Las posiciones ya vienen ordenadas: no hace falta ordenar ni borrar nada.",
            "Un único recorrido de izquierda a derecha basta.",
            "Borrar el primer elemento de un vector mueve todos los demás: evítalo y usa un índice."])
    pos = []
    x = 1
    for _ in range(100000):
        x += rng.randint(0, 19000)
        pos.append(x)
    prueba("100.000 agujeros por toda la manguera", "rendimiento", [(1000, pos)],
           "Un caso grande con posiciones hasta casi 10⁹.",
           {"tle": "Debe ser O(N): un solo recorrido por los agujeros.",
            "wa": "En el caso grande falla: revisa el tipo de las posiciones y el borde del parche."},
           ["No vuelvas atrás en el vector: cada agujero se mira una vez.",
            "Lee con cin normal; un único bucle basta."])
    return P


VARIANTES = [
    Variante("el borde del parche no cuenta (≥)", [("if (p > finParche) {", "if (p >= finParche) {")], prueba=[5, 6], v="wa"),
    Variante("el parche tapa L - 1", [("finParche = (long long)p + L;", "finParche = (long long)p + L - 1;")], prueba=[5, 6], v="wa"),
    Variante("el parche tapa L + 1", [("finParche = (long long)p + L;", "finParche = (long long)p + L + 1;")], prueba=7, v="wa"),
    Variante("compara con el agujero anterior",
             [("            finParche = (long long)p + L;\n        }", "        }\n        finParche = (long long)p + L;")], prueba=8, v="wa"),
    Variante("tramos fijos de longitud L",
             [("        if (p > finParche) {           // agujero sin tapar: parche nuevo que empieza en el\n            ++parches;\n            finParche = (long long)p + L;",
               "        if (p / L > finParche) {\n            ++parches;\n            finParche = p / L;")], prueba=4, v="wa"),
    Variante("contador sin reiniciar", [("int parches = 0;", "static int parches = 0;")], prueba=12, v="wa"),
    Variante("final del parche sin reiniciar", [("long long finParche = -1;", "static long long finParche = -1;")], prueba=12, v="wa"),
    Variante("borra del principio del vector",
             [("for (int p : pos) {\n        if (p > finParche) {", "while (!pos.empty()) {\n        int p = pos.front(); pos.erase(pos.begin());\n        if (p > finParche) {")],
             prueba=15, v="tle"),
    Variante("un número por caso separado por espacios", [("cout << parches << '\\n';", "cout << parches << ' ';")], prueba=1, v="pe"),
]
