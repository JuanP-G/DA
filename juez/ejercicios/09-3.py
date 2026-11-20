"""09-3 · Carreras de coches: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «N V» y una línea con N voltajes (0..10⁶; V entre 0 y 2·10⁶).
Salida: el máximo número de parejas de pilas cuya suma de voltajes es al menos V.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "9-Algoritmos voraces II/EJ_09-3/EJ_09-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["pilas[i] + pilas[j] >= V", "pilas[i] + pilas[j] > V"],
}


def resuelve(V, pilas):
    """Solucionador independiente: de la más fuerte a la más débil, cada pila fuerte se lleva la
    pila más débil (aún libre) con la que llega a V."""
    p = sorted(pilas)
    lo, hi, n = 0, len(p) - 1, 0
    while lo < hi:
        if p[lo] + p[hi] < V:
            lo += 1
        else:
            n += 1
            lo += 1
            hi -= 1
    return n


def caso_a_texto(c):
    V, pilas = c
    return f"{len(pilas)} {V}\n" + " ".join(map(str, pilas)) + "\n"


def aleatorio(rng, n, maxv):
    pilas = [rng.randint(0, maxv) for _ in range(n)]
    return (rng.randint(0, 2 * maxv), pilas)


def pruebas():
    rng = random.Random(903)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado", [(20, [8, 10, 12, 15]), (30, [20, 12, 7, 18, 2])],
           "Los dos ejemplos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la lectura (primero N y luego V), el criterio voraz y que escribes un número por caso."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "En el primer caso juntar las dos más potentes (15 y 12) deja solo un coche.",
            "Ordena las pilas y mira a la vez la más débil y la más fuerte."])
    prueba("Una sola pila", "trampa", [(20, [15])],
           "Con una sola pila no hay ningún coche, aunque su voltaje doble llegue a V.",
           {"wa": "Emparejas una pila consigo misma: cuando los dos índices se encuentran (i == j) ya no queda pareja."},
           ["Con N = 1 la respuesta es 0.",
            "El bucle debe seguir mientras i < j, no i ≤ j."])
    prueba("Voltaje mínimo 0", "borde", [(0, [0, 0, 0]), (0, [5, 0, 3, 9])],
           "Con V = 0 cualquier pareja sirve, incluso de pilas de 0 µV.",
           {"wa": "Con V = 0 todas las parejas valen: salen N / 2 coches. Revisa ≥ frente a > y el tratamiento de los voltajes 0."},
           ["0 + 0 ≥ 0: dos pilas gastadas también mueven el coche si V = 0.",
            "La condición es suma ≥ V."])
    prueba("La suma justa", "trampa", [(20, [5, 15])],
           "Dos pilas que suman exactamente V sirven.",
           {"wa": "Usas > en vez de ≥: el enunciado dice que deben sumar AL MENOS V."},
           ["5 + 15 = 20 = V: es un coche.",
            "Cambia la comparación a suma ≥ V."])
    prueba("Las dos más potentes juntas no", "trampa", [(20, [8, 10, 12, 15])],
           "Juntar las dos pilas más fuertes desperdicia voltaje.",
           {"wa": "Emparejas la más fuerte con la siguiente más fuerte. A la más fuerte le conviene la pila MÁS DÉBIL con la que llegue a V."},
           ["15 + 8 y 12 + 10 dan dos coches; 15 + 12 deja solo uno.",
            "Mira la más débil y la más fuerte: si juntas llegan, forman pareja."])
    prueba("Descartar la débil, no la fuerte", "trampa", [(15, [1, 10, 10])],
           "Si la más débil y la más fuerte no llegan, la que sobra es la débil.",
           {"wa": "Cuando la pareja (más débil, más fuerte) no llega, descartas la fuerte. Pero es la débil la que no sirve con nadie."},
           ["Aquí 10 + 10 forman un coche; la pila de 1 no sirve.",
            "Si débil + fuerte < V, la débil tampoco llegará con ninguna otra: descártala (avanza i)."])
    prueba("Emparejar mitad débil con mitad fuerte en orden", "trampa", [(20, [1, 2, 18, 19])],
           "Emparejar la i-ésima débil con la i-ésima fuerte (en el mismo orden) no es óptimo.",
           {"wa": "Emparejas las dos mitades en el mismo orden (la más débil con la más débil de la mitad fuerte). Hay que cruzarlas: la más débil con la más fuerte."},
           ["1 + 19 y 2 + 18 dan dos coches.",
            "Usa dos índices que avanzan desde los extremos hacia el centro."])
    prueba("Voltajes máximos", "borde", [(2000000, [1000000, 999999, 1000000]), (2000000, [999999, 999999])],
           "V en su máximo (2·10⁶) y pilas de 10⁶ µV.",
           {"wa": "Con los valores máximos algo falla: revisa los tipos y la comparación ≥."},
           ["Solo las dos pilas de 10⁶ llegan a 2·10⁶.",
            "2·10⁶ cabe en int sin problema; revisa la condición."])
    prueba("Número impar de pilas", "trampa", [(20, [10, 10, 10])],
           "Con tres pilas válidas, una se queda sin pareja.",
           {"wa": "Cuentas una pila sola como coche o te sales del vector al emparejar: cada coche necesita dos pilas distintas."},
           ["Sale un coche, no dos.",
            "Para cuando los índices se crucen o coincidan."])
    prueba("Pilas desordenadas", "trampa", [(20, [19, 1, 2, 18])],
           "Las pilas no vienen ordenadas en la entrada.",
           {"wa": "Parece que no ordenas las pilas antes de emparejarlas."},
           ["La entrada no está ordenada.",
            "Ordena el vector antes de usar los dos índices."])
    prueba("Ninguna pareja llega", "borde", [(100, [1, 2, 3, 49]), (1, [0, 0])],
           "Ninguna pareja alcanza V: 0 coches.",
           {"wa": "Si ninguna pareja llega debe salir 0."},
           ["49 + 3 < 100.",
            "Revisa que solo cuentas un coche cuando la suma llega a V."])
    prueba("Muchas pilas iguales", "trampa", [(20, [10] * 7), (21, [10] * 6)],
           "Pilas repetidas: con 10 + 10 ≥ 20 salen 3 coches; con V = 21 ninguno.",
           {"wa": "Algo falla con valores repetidos: revisa cómo mueves los índices."},
           ["7 pilas de 10 y V = 20: 3 coches.",
            "Con valores iguales no debe cambiar nada de tu bucle."])
    prueba("Varios casos seguidos", "trampa",
           [(10, [5, 5, 5, 5, 5, 5]), (100, [1, 2]), (7, [7, 0]), (3, [1, 1, 2, 2])],
           "Varios casos seguidos: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el contador o el vector no se reinician."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara el vector y el contador dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(rng, rng.randint(1, 9), rng.choice([10, 30, 1000000])) for _ in range(200)],
           "200 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Ordena sus pilas en papel y sigue los dos índices."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(rng, rng.randint(100, 2000), rng.choice([100, 1000000])) for _ in range(30)],
           "30 casos medianos.",
           {"wa": "Algo falla con más pilas: revisa qué haces cuando la pareja no llega."},
           ["Reduce el caso que falla quitando pilas mientras siga fallando.",
            "Si débil + fuerte llegan, pareja; si no, se descarta la débil."])
    prueba("300.000 pilas", "rendimiento", [aleatorio(rng, 300000, 1000000)],
           "El tamaño máximo de un caso: mide la eficiencia.",
           {"tle": "Tu solución es lenta para 300.000 pilas: debe ser O(N log N). ¿Buscas pareja para cada pila recorriendo las demás?"},
           ["Ordenar cuesta O(N log N); emparejar con dos índices es una sola pasada.",
            "Usa sort de la biblioteca, no una ordenación cuadrática.",
            "No borres elementos del medio de un vector: cuesta O(N) cada vez."])
    return [Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{resuelve(*c)}\n" for c in casos), casos=len(casos),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("empareja una pila consigo misma", [("while (i < j)", "while (i <= j)")], prueba=2, v="wa"),
    Variante("exige suma > V", [("pilas[i] + pilas[j] >= V", "pilas[i] + pilas[j] > V")], prueba=4, v="wa"),
    Variante("junta las dos más fuertes",
             [("if (pilas[i] + pilas[j] >= V) {", "if (pilas[j - 1] + pilas[j] >= V) {"),
              ("++coches;\n            ++i; --j;", "++coches;\n            j -= 2;")], prueba=5, v="wa"),
    Variante("descarta la fuerte", [("++i;                           // la mas debil", "--j;                           // la mas debil")], prueba=6, v="wa"),
    Variante("no ordena", [("sort(pilas.begin(), pilas.end());", "")], prueba=10, v="wa"),
    Variante("no reinicia entre casos", [("int coches = 0;", "static int coches = 0;")], prueba=13, v="wa"),
    Variante("ordenación cuadrática",
             [("sort(pilas.begin(), pilas.end());",
               "for (int a = 1; a < N; ++a) for (int b = a; b > 0 && pilas[b] < pilas[b - 1]; --b) swap(pilas[b], pilas[b - 1]);")],
             prueba=16, v="tle"),
]
