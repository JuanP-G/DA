"""03-2 · 12 points go to…: juez con pruebas pensadas para cada error típico."""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-2/EJ_03-2.cpp",
    "cabeceras": ["3-Colas de prioridad variable (Heapsort)/EJ_03-2/IndexPQ.h"],
    "limite_ms": 4000,
    "fallo": ["return a.second < b.second;", "return a.second > b.second;"],
}


def votacion(eventos):
    """Solucionador independiente: diccionario de puntos + montículo con borrado perezoso.
    eventos: lista de "?" o (nombre, puntos). Devuelve las líneas de salida del caso."""
    puntos, monti, out = {}, [], []
    for e in eventos:
        if e == "?":
            while True:
                p, nombre = monti[0]
                if puntos[nombre] == -p:
                    break
                heapq.heappop(monti)          # entrada antigua de ese país
            out.append(f"{nombre} {-p}")
        else:
            nombre, x = e
            puntos[nombre] = puntos.get(nombre, 0) + x
            heapq.heappush(monti, (-puntos[nombre], nombre))
    out.append("---")
    return out


def caso_a_texto(eventos):
    return f"{len(eventos)}\n" + "".join("?\n" if e == "?" else f"{e[0]} {e[1]}\n" for e in eventos)


def ev(*lineas):
    """ev("Spain 12", "?", ...) -> lista de eventos."""
    res = []
    for l in lineas:
        if l == "?":
            res.append("?")
        else:
            n, x = l.split()
            res.append((n, int(x)))
    return res


def aleatorio(r, paises, n, rango, p_consulta=.35):
    nombres = r.sample(paises, r.randint(1, min(len(paises), 6)))
    evs = [(r.choice(nombres), r.randint(-rango, rango))]
    while len(evs) < n:
        evs.append("?" if r.random() < p_consulta else (r.choice(nombres), r.randint(-rango, rango)))
    return evs


def nombre_base26(k, largo):
    s = ""
    for _ in range(largo):
        s += chr(97 + k % 26)
        k //= 26
    return s


PAISES = ["Spain", "Italy", "France", "Germany", "Sweden", "Norway", "Ukraine", "UK", "Malta",
          "Israel", "Austria", "Albania", "Armenia", "Serbia", "Croatia", "Cyprus"]


def pruebas():
    r = random.Random(32)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [ev("Spain 12", "Italy 10", "?", "France 18", "Spain -5", "?"),
            ev("Germany 8", "France 8", "?", "Spain 12", "?", "Spain 8", "Italy 22", "?", "Italy -7", "?")],
           "Los dos casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: lectura de los eventos, el comparador o el formato «nombre puntos».",
            "pe": "Los datos están bien pero no el formato: cada respuesta es «nombre», un espacio y los puntos, en su propia línea; y «---» al final de cada caso.",
            "rte": "Se rompe con el ejemplo: ¿consultas la prioridad de un país que aún no está en la cola? Un país nuevo empieza con 0 puntos."},
           ["Sigue el segundo caso a mano: tras «Italy -7» Italia baja a 15 y España, con 20, vuelve a mandar.",
            "Cada «?» escribe «nombre puntos» y cada caso termina con una línea «---».",
            "La entrada no dice cuántos casos hay: lee hasta que falle la lectura de N (plantilla de casos ilimitados)."])
    prueba("Caso sin ninguna consulta", "borde",
           [ev("Spain 3", "Italy 5", "Spain -1"), ev("Malta 1", "?")],
           "Un caso sin «?»: solo se escribe la línea «---».",
           {"wa": "Aunque un caso no tenga consultas, hay que escribir su «---». Revisa que lo escribes siempre al acabar los N eventos.",
            "pe": "Revisa las líneas en blanco: un caso sin consultas da solo «---», sin líneas vacías."},
           ["La salida del primer caso es una sola línea: «---».",
            "Escribe «---» después del bucle de eventos, pase lo que pase dentro."])
    prueba("Un solo país", "borde",
           [ev("Spain 7", "?"), ev("Malta 5", "?", "Malta -2", "?", "?")],
           "Casos con un único país que cambia de puntos.",
           {"wa": "Con un solo país, el líder es siempre él con sus puntos actuales. Revisa que actualizas la puntuación al restar.",
            "rte": "Con un solo país te sales: revisa el tamaño de la cola y los índices de los países."},
           ["Malta pasa de 5 a 3: las respuestas son «Malta 5», «Malta 3», «Malta 3».",
            "Cada evento cambia los puntos del país que nombra; la consulta mira los puntos ACTUALES."])
    prueba("Los puntos se acumulan", "trampa",
           [ev("Spain 5", "Spain 3", "Italy 7", "?")],
           "Cada evento suma (o resta) a lo que ya tenía el país; no sustituye sus puntos.",
           {"wa": "Estás guardando los puntos del último evento en vez de sumarlos a los que ya tenía el país."},
           ["España tiene 5 + 3 = 8 puntos e Italia 7: el líder es «Spain 8».",
            "La nueva prioridad es (puntos actuales + incremento): consulta los actuales con priority(idx) antes del update."])
    prueba("Empate: gana el nombre menor (llega después)", "trampa",
           [ev("Spain 10", "France 10", "?")],
           "Dos países empatados a puntos: manda el de nombre lexicográficamente menor, aunque haya llegado después.",
           {"wa": "En los empates tu comparador no elige el nombre menor (o elige el que llegó antes). Con puntos iguales debe ir antes el nombre más pequeño."},
           ["España y Francia empatan a 10: manda «France 10» porque «France» < «Spain».",
            "El comparador debe ser: más puntos antes; si empatan, nombre menor antes (a.nombre < b.nombre)."])
    prueba("Empate: gana el nombre menor (llega antes)", "trampa",
           [ev("Austria 10", "Spain 10", "?")],
           "Empate en el que el país de nombre menor ya iba primero: el recién llegado no le quita la cabeza.",
           {"wa": "En los empates gana el último que ha cambiado: tu comparador no mira el nombre (o usa ≥ con los puntos). Con puntos iguales manda el nombre menor."},
           ["Austria y España empatan a 10: sigue mandando «Austria 10».",
            "Si el comparador solo mira los puntos (o usa >=), al flotar un empatado se coloca por encima. Añade el nombre como desempate."])
    prueba("El líder pierde puntos y deja de serlo", "trampa",
           [ev("Spain 20", "Italy 15", "Spain -10", "?")],
           "El que iba primero recibe una sanción y otro país pasa a mandar sin haber recibido nada.",
           {"wa": "Cuando el líder pierde puntos no lo bajas en la cola: guardas al líder aparte y solo lo cambias cuando alguien le supera, o tu montículo flota pero no hunde."},
           ["España baja a 10 e Italia, con 15, pasa a mandar: «Italy 15».",
            "El líder puede dejar de serlo sin que nadie le supere: hay que recolocarlo (hundirlo) al bajar sus puntos.",
            "Con IndexPQ, update(idx, nuevaPrioridad) ya flota o hunde según haga falta; no guardes el líder en una variable aparte."])
    prueba("El líder pierde puntos y empata", "trampa",
           [ev("Spain 20", "Italy 10", "Spain -10", "?")],
           "El líder baja justo hasta empatar con otro de nombre menor: al hundirse, el desempate decide.",
           {"wa": "Al bajar el líder hasta empatar, el desempate por nombre no se aplica: el comparador debe usar el nombre también al hundir."},
           ["España baja a 10 y empata con Italia: manda «Italy 10» («Italy» < «Spain»).",
            "Revisa que el mismo comparador (puntos y luego nombre) se usa en todas las comparaciones del montículo."])
    prueba("El líder pierde puntos pero sigue mandando", "trampa",
           [ev("Spain 20", "Italy 5", "Spain -10", "?")],
           "El líder baja pero sigue por delante: hay que escribir sus puntos actuales, no los antiguos.",
           {"wa": "Escribes una puntuación antigua del líder: si guardas copias en un montículo, la del principio puede estar desfasada."},
           ["España baja de 20 a 10 y sigue por delante de Italia (5): «Spain 10».",
            "La consulta debe dar los puntos actuales del líder: con IndexPQ, top().prioridad está siempre al día si haces update."])
    prueba("Todos con puntos negativos", "trampa",
           [ev("Spain -5", "Italy -3", "?", "France -100", "?")],
           "Los países pueden ir en negativo: el líder es el menos negativo.",
           {"wa": "Con puntuaciones negativas el líder no sale bien: ¿empiezas el máximo en 0 o descartas los países con puntos negativos?",
            "rte": "Con puntuaciones negativas no encuentras líder y consultas algo que no existe."},
           ["Italia, con −3, va por delante de España (−5): «Italy -3».",
            "Un país que entra en la cola sigue en ella aunque sus puntos sean negativos o cero."])
    prueba("Un país con 0 puntos puede mandar", "trampa",
           [ev("Spain 3", "Spain -3", "Italy -2", "?")],
           "España vuelve a 0 puntos y sigue en la clasificación: va por delante de Italia (−2).",
           {"wa": "Quitas de la clasificación a los países que vuelven a 0, pero siguen participando (no es como el tridente de temas)."},
           ["España tiene 0 e Italia −2: «Spain 0».",
            "No saques a nadie de la cola: aquí ningún país desaparece."])
    prueba("Comparación estándar de cadenas", "trampa",
           [ev("albania 7", "Zambia 7", "?", "Macedonia 9", "MacedoniaNorte 9", "?")],
           "En los empates se compara con el orden estándar de string: mayúsculas antes que minúsculas, y un prefijo antes que la palabra larga.",
           {"wa": "Tu comparación de nombres no es la estándar: «Zambia» < «albania» (las mayúsculas van antes) y «Macedonia» < «MacedoniaNorte»."},
           ["En C++, «Z» (90) va antes que «a» (97): manda «Zambia 7».",
            "Compara los nombres con < de string directamente; no los pases a minúsculas ni compares solo la primera letra."])
    prueba("Varios casos seguidos", "trampa",
           [ev("Spain 50", "Italy 40", "?"), ev("Italy 10", "Spain 5", "?"), ev("France 1", "?"), ev("Spain -1", "?")],
           "Los mismos países aparecen en casos distintos: cada caso empieza con todos a 0.",
           {"wa": "Algo se arrastra de un caso a otro: el mapa nombre → índice o la cola deben crearse dentro de resuelveCaso.",
            "rte": "Usas en un caso un índice o una cola de un caso anterior: el mapa nombre → número de país debe vaciarse en cada caso."},
           ["En el segundo caso España tiene 5 puntos, no 55: manda «Italy 10».",
            "Declara la cola, el mapa y el contador de países dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, PAISES, r.randint(2, 15), 10) for _ in range(40)],
           "40 casos pequeños al azar con pocos países.",
           {"wa": "Hay algún caso concreto que no tratas: busca qué consulta falla y sigue los puntos de cada país hasta ahí.",
            "rte": "Algún caso pequeño hace que consultes algo que no existe."},
           ["Cuenta los «---» de la salida esperada hasta la línea que falla para saber qué caso es.",
            "Apunta en una tabla los puntos de cada país evento a evento."])
    prueba("Aleatorios con muchos empates", "aleatorio",
           [aleatorio(r, PAISES[:6], r.randint(5, 30), 1, .4) for _ in range(40)],
           "Puntos de −1 a 1 con pocos países: hay empates continuamente.",
           {"wa": "Con muchos empates falla el desempate por nombre en algún momento: suele ser al bajar (hundir) o al subir (flotar) un país empatado."},
           ["Busca la primera consulta que falla y mira qué países empataban en ese momento.",
            "El comparador debe ser el mismo en todas partes: puntos y, si empatan, nombre."])
    prueba("Aleatorios con muchos países", "aleatorio",
           [aleatorio(r, [nombre_base26(k, 3) for k in range(400)], 300, 100, .3) for _ in range(5)]
           + [[(nombre_base26(k, 3), r.randint(-100, 100)) for k in range(150)] + ["?"] for _ in range(3)],
           "Casos de unos cientos de eventos y países: el montículo tiene varios niveles.",
           {"wa": "Con muchos países algo falla al recolocarlos: revisa que tras cada cambio el país sube o baja lo que haga falta."},
           ["Si las pequeñas salen bien, el fallo aparece cuando el montículo es profundo: flotar/hundir más de un nivel.",
            "Usa update de la IndexPQ: flota si ha mejorado y hunde si ha empeorado."])
    # rendimiento: 60.000 países y 95.000 consultas
    nombres = [nombre_base26(k, 4) for k in r.sample(range(26 ** 4), 60000)]
    grande = [(n, r.randint(-100, 100)) for n in nombres]
    for _ in range(190000):
        grande.append("?" if r.random() < .5 else (r.choice(nombres), r.randint(-100, 100)))
    prueba("Muchos países y muchas consultas", "rendimiento", [grande],
           "250.000 eventos con 60.000 países y unas 95.000 consultas.",
           {"tle": "Cada consulta (o cada búsqueda de un país) recorre todos los países: O(países) por evento es demasiado. Con IndexPQ la consulta es O(1) y el cambio O(log n).",
            "mle": "Gastas demasiada memoria: ¿guardas una copia por evento en vez de una entrada por país?"},
           ["Con 60.000 países y 95.000 consultas, recorrerlos todos en cada «?» son 5,7·10⁹ comparaciones.",
            "Para encontrar el índice de un país usa un unordered_map<string,int> (no busques en un vector).",
            "La consulta es top() de la IndexPQ: O(1). Cada cambio, update: O(log n)."])
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(c) for c in casos),
                   salida="".join(l + "\n" for c in casos for l in votacion(c)),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("desempate al revés (nombre mayor)", [("return a.second < b.second;", "return a.second > b.second;")], prueba=5, v="wa"),
    Variante("sustituye los puntos en vez de sumarlos", [("pq.update(idx, { actuales + puntos, nombre });", "pq.update(idx, { puntos, nombre });")], prueba=4, v="wa"),
    Variante("comparador sin desempate (>=)",
             [("if (a.first != b.first) return a.first > b.first;", "return a.first >= b.first;")], prueba=6, v="wa"),
    Variante("guarda el líder aparte (no baja al perder puntos)",
             [("int siguiente = 0;", "int siguiente = 0;\n\tstring lnombre; int lpuntos = 0;"),
              ("auto const& lider = pq.top().prioridad;\n\t\t\tcout << lider.second << \" \" << lider.first << \"\\n\";",
               "cout << lnombre << \" \" << lpuntos << \"\\n\";"),
              ("pq.update(idx, { actuales + puntos, nombre });",
               "Par np{ actuales + puntos, nombre };\n\t\t\tif (lnombre.empty() || lnombre == nombre || Mejor()(np, Par{ lpuntos, lnombre })) { lnombre = nombre; lpuntos = np.first; }\n\t\t\tpq.update(idx, np);")],
             prueba=7, v="wa"),
    Variante("nombre y puntos en líneas distintas", [("cout << lider.second << \" \" << lider.first", "cout << lider.second << \"\\n\" << lider.first")], prueba=1, v="pe"),
    Variante("olvida la línea ---", [("cout << \"---\\n\";", "")], prueba=2, v="wa"),
    Variante("el mapa de países no se vacía entre casos",
             [("unordered_map<string, int> indice;", "static unordered_map<string, int> indice;")], prueba=13, v="rte"),
    Variante("busca el líder recorriendo todos los países",
             [("auto const& lider = pq.top().prioridad;",
               "Par lider = pq.priority(0);\n\t\t\tfor (int k = 1; k < siguiente; ++k) if (Mejor()(pq.priority(k), lider)) lider = pq.priority(k);")],
             prueba=17, v="tle"),
]
