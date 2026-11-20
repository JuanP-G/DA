"""03-5 · Tridente de temas candentes: juez con pruebas pensadas para cada error típico."""
import heapq
import pathlib
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-5/EJ_03-5.cpp",
    "cabeceras": ["3-Colas de prioridad variable (Heapsort)/EJ_03-5/IndexPQ.h"],
    "limite_ms": 4000,
    "fallo": ["return a.ultimoC > b.ultimoC;", "return a.ultimoC < b.ultimoC;"],
}


def tridente(eventos):
    """Solucionador independiente: diccionarios de citas y último C + montículo con borrado perezoso
    (cada entrada lleva la versión del tema; las desfasadas se descartan al consultar)."""
    citas, ultimo, version, monti, out = {}, {}, {}, [], []
    for t, e in enumerate(eventos):
        if e == "TC":
            podio = []
            while monti and len(podio) < 3:
                c, u, v, tema = heapq.heappop(monti)
                if version[tema] == v:
                    podio.append((c, u, v, tema))
            podio = [x for x in podio if -x[0] > 0]
            for k, (_, _, _, tema) in enumerate(podio, 1):
                out.append(f"{k} {tema}")
            for x in podio:
                heapq.heappush(monti, x)
        else:
            tipo, tema, n = e
            if tipo == "C":
                citas[tema] = citas.get(tema, 0) + n
                ultimo[tema] = t
            else:
                citas[tema] -= n
            version[tema] = version.get(tema, 0) + 1
            if citas[tema] > 0:
                heapq.heappush(monti, (-citas[tema], -ultimo[tema], version[tema], tema))
    out.append("---")
    return out


def caso_a_texto(eventos):
    return f"{len(eventos)}\n" + "".join("TC\n" if e == "TC" else f"{e[0]} {e[1]} {e[2]}\n" for e in eventos)


def ev(*lineas):
    res = []
    for l in lineas:
        if l == "TC":
            res.append("TC")
        else:
            a, b, c = l.split()
            res.append((a, b, int(c)))
    return res


def aleatorio(r, temas, n, maxC, p_tc=.25):
    """Eventos válidos: las E nunca quitan más citas de las vigentes."""
    citas, evs = {}, []
    while len(evs) < n:
        x = r.random()
        if x < p_tc:
            evs.append("TC")
        elif x < p_tc + .25 and any(citas.values()):
            tema = r.choice([t for t in citas if citas[t] > 0])
            k = r.randint(1, citas[tema])
            citas[tema] -= k
            evs.append(("E", tema, k))
        else:
            tema = r.choice(temas)
            k = r.randint(1, maxC)
            citas[tema] = citas.get(tema, 0) + k
            evs.append(("C", tema, k))
    return evs


def nombre_base26(k, largo):
    s = ""
    for _ in range(largo):
        s += chr(97 + k % 26)
        k //= 26
    return s


TEMAS = ["quickSort", "mergeSort", "heapSort", "burbuja", "IndexPQ", "AVL", "Dijkstra", "Prim", "Kruskal", "DFS"]


def pruebas():
    r = random.Random(35)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [ev("C quickSort 31", "C mergeSort 40", "C burbuja 17", "C quickSort 8", "TC", "C heapSort 19",
               "C burbuja 1", "E mergeSort 6", "TC"),
            ev("C Hulk 1000", "C Ironman 3000", "E Hulk 1000", "C Superman 3000", "TC")],
           "Los dos casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura de los eventos (TC no lleva argumentos), el comparador o el formato «puesto tema».",
            "pe": "Los datos están bien pero no el formato: cada puesto en su línea, «número espacio tema», y «---» al final de cada caso."},
           ["En el segundo caso Hulk se queda a 0 y no sale; Superman e Ironman empatan y va antes Superman (su C es más reciente).",
            "Cada puesto se escribe como «1 tema», «2 tema», «3 tema» en líneas distintas; cada caso acaba con «---».",
            "La entrada no dice cuántos casos hay: lee hasta que falle la lectura de n (plantilla de casos ilimitados)."])
    prueba("TC sin ningún tema", "borde",
           [ev("TC"), ev("TC", "C a 1", "TC")],
           "Una consulta cuando aún no hay temas: no se escribe ningún puesto.",
           {"wa": "Con la cola vacía no hay que escribir nada para esa consulta (solo el «---» del final del caso).",
            "rte": "Consultas la cima de una cola vacía: comprueba que no está vacía antes de top()."},
           ["El primer caso solo tiene un TC: su salida es solo «---».",
            "En el bucle del podio comprueba antes que nada que la cola no está vacía."])
    prueba("Menos de tres temas", "borde",
           [ev("C uno 5", "TC"), ev("C uno 5", "C dos 7", "TC")],
           "Con uno o dos temas el podio tiene solo esos puestos.",
           {"wa": "Con menos de tres temas escribes puestos de más (o de menos): el podio se corta cuando se acaban los temas.",
            "rte": "Con menos de tres temas sacas de una cola vacía al buscar el tercero."},
           ["Con un único tema la salida es «1 uno» y «---».",
            "Saca como mucho 3, pero para antes si la cola se queda vacía."])
    prueba("Caso sin ninguna consulta", "borde",
           [ev("C a 3", "E a 1"), ev("C b 1", "TC")],
           "Un caso sin TC: solo se escribe la línea «---».",
           {"wa": "Aunque un caso no tenga consultas, hay que escribir su «---» al final.",
            "pe": "Un caso sin consultas da solo «---», sin líneas en blanco."},
           ["La salida del primer caso es una sola línea: «---».",
            "Escribe «---» después del bucle de eventos, pase lo que pase dentro."])
    prueba("Empate: va antes el C más reciente", "trampa",
           [ev("C A 5", "C B 5", "TC")],
           "Dos temas con las mismas citas: va primero el que recibió su último C más tarde.",
           {"wa": "En los empates no eliges el C más reciente: el desempate debe poner antes el tema con el último C posterior (instante mayor)."},
           ["A y B tienen 5 citas; el C de B llegó después: «1 B», «2 A».",
            "Guarda en la prioridad el instante (número de evento) del último C y, si las citas empatan, va antes el mayor."])
    prueba("Empate: cuenta el último C, no el primero", "trampa",
           [ev("C A 2", "C B 5", "C A 3", "TC")],
           "A apareció antes que B, pero su último C es más reciente: en el empate va primero A.",
           {"wa": "Desempatas por cuándo apareció el tema por primera vez (o por su índice). Hay que actualizar el instante en CADA C."},
           ["A y B tienen 5 citas; el último C de A (evento 3) es posterior al de B (evento 2): «1 A», «2 B».",
            "En cada evento C, además de sumar las citas, actualiza el instante del último C."])
    prueba("Una E no cuenta como reciente", "trampa",
           [ev("C B 6", "C A 5", "E B 1", "TC")],
           "Las expiraciones no cambian el instante del último C.",
           {"wa": "Una expiración (E) está actualizando el instante del desempate: solo los eventos C cuentan como «tendencia reciente»."},
           ["B baja a 5 y empata con A; el último C de A es posterior al de B: «1 A», «2 B».",
            "Con E solo se restan citas; el instante del último C se queda como estaba."])
    prueba("Temas que se quedan a 0 no salen", "trampa",
           [ev("C A 3", "E A 3", "TC", "C B 2", "TC")],
           "Un tema cuyas citas expiran todas desaparece del podio.",
           {"wa": "Escribes temas con 0 citas: al montar el podio para en cuanto la cima tenga 0 citas."},
           ["Tras «E A 3», A tiene 0 citas: el primer TC no escribe nada y el segundo solo «1 B».",
            "Si la cima tiene 0 citas, todos los demás también: deja de sacar."])
    prueba("El podio no se pierde entre consultas", "trampa",
           [ev("C B 2", "C A 3", "TC", "C A 1", "TC", "TC")],
           "Para ver el podio se sacan temas de la cola: hay que volver a meterlos después.",
           {"wa": "Tras un TC, los temas del podio desaparecen de la cola: hay que volver a meterlos (push) al acabar la consulta.",
            "rte": "Tras un TC, un tema del podio ya no está en la cola y al consultar o cambiar su prioridad salta una excepción. Hay que volver a meterlos."},
           ["Después del primer TC, A y B deben seguir en la cola: «C A 1» la sube a 4.",
            "Guarda en un vector los que sacas para el podio y, tras escribirlos, vuelve a hacer push de todos."])
    prueba("Más de tres temas: solo los tres primeros", "trampa",
           [ev("C a 1", "C b 2", "C c 3", "C d 4", "C e 5", "TC")],
           "Con cinco temas el podio tiene exactamente tres puestos.",
           {"wa": "Escribes más (o menos) de tres puestos: el podio se corta en el tercero."},
           ["La salida es «1 e», «2 d», «3 c» y «---».",
            "La condición del bucle del podio es «menos de 3 sacados» (< 3, no ≤ 3)."])
    prueba("Más citas va antes aunque el C sea antiguo", "trampa",
           [ev("C A 10", "C B 1", "TC")],
           "El criterio principal son las citas; la recencia solo desempata.",
           {"wa": "Ordenas primero por recencia: el criterio principal son las citas y el último C solo sirve para desempatar."},
           ["A tiene 10 citas y B 1: «1 A», «2 B», aunque el C de B sea más reciente.",
            "Comparador: si las citas son distintas, gana la mayor; solo si empatan, el C más reciente."])
    prueba("Una expiración baja al líder", "trampa",
           [ev("C A 10", "C B 8", "C D 6", "E A 5", "TC")],
           "El tema que va primero pierde citas y baja hasta el tercer puesto.",
           {"wa": "Cuando un tema pierde citas no baja en la cola: hay que hundirlo (update de la IndexPQ lo hace)."},
           ["A baja a 5: «1 B», «2 D», «3 A».",
            "Usa update(idx, nuevaPrioridad): flota si mejora y hunde si empeora."])
    prueba("Un tema que vuelve tras quedarse a 0", "trampa",
           [ev("C A 3", "E A 3", "C B 1", "C A 1", "TC")],
           "Un tema a 0 que vuelve a recibir citas reaparece, con su nuevo último C.",
           {"wa": "Un tema que se quedó a 0 no vuelve bien: debe seguir en la cola (o volver a ella) con sus citas y su último C actualizados.",
            "rte": "Al volver a citar un tema que se quedó a 0 consultas un elemento que ya no está en la cola."},
           ["A vuelve con 1 cita y empata con B; el C de A es más reciente: «1 A», «2 B».",
            "No saques de la cola los temas que se quedan a 0: basta con no escribirlos."])
    prueba("Varios casos seguidos", "trampa",
           [ev("C A 50", "C B 40", "TC"), ev("C B 1", "C A 2", "TC"), ev("TC"), ev("C C 7", "TC")],
           "Los mismos temas aparecen en casos distintos: cada caso empieza sin temas ni citas.",
           {"wa": "Algo se arrastra de un caso a otro: el mapa tema → índice, el vector de nombres o la cola deben crearse dentro de resuelveCaso.",
            "rte": "Usas en un caso el índice de un tema de un caso anterior: el mapa tema → índice debe vaciarse en cada caso."},
           ["En el segundo caso A tiene 2 citas y B 1, no 52 y 41.",
            "Declara la cola, el mapa y el vector de nombres dentro de la función de cada caso."])
    prueba("Muchas citas", "borde",
           [ev("C grande 1000000000", "C grande 500000000", "C otro 1499999999", "TC", "E grande 1", "TC")],
           "Citas que suman 1,5·10⁹: caben en int, y los empates se siguen resolviendo bien.",
           {"wa": "Con números grandes algo se corta o el empate falla: revisa el tipo de las citas (int basta aquí)."},
           ["«grande» tiene 1.500.000.000 citas y «otro» 1.499.999.999: primero «grande»; tras la E empatan y va antes «otro» (su C es más reciente).",
            "Lee las citas en int o long long, no en short."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, TEMAS[:5], r.randint(1, 15), 3) for _ in range(40)],
           "40 casos pequeños al azar, con citas pequeñas (muchos empates).",
           {"wa": "Hay algún caso concreto que no tratas: busca la consulta que falla y apunta citas y último C de cada tema hasta ahí.",
            "rte": "Algún caso pequeño hace que consultes un tema que no está en la cola."},
           ["Cuenta los «---» de la salida esperada hasta la línea que falla para saber qué caso es.",
            "Haz una tabla: tema, citas vigentes e instante de su último C."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, [nombre_base26(k, 3) for k in range(300)], 2000, 50, .1) for _ in range(5)],
           "Casos de 2000 eventos con cientos de temas.",
           {"wa": "Con muchos temas algo falla al recolocarlos o al devolver el podio a la cola."},
           ["Si las pequeñas salen bien, revisa que tras cada TC los temas vuelven a la cola con su prioridad intacta.",
            "Comprueba que E y C usan update y que el desempate es el mismo en todas las comparaciones."])
    nombres = [nombre_base26(k, 4) for k in r.sample(range(26 ** 4), 60000)]
    grande = [("C", t, r.randint(1, 1000)) for t in nombres]
    resto = aleatorio(r, nombres, 150000, 1000, .3)
    prueba("Muchos temas y muchas consultas", "rendimiento", [grande + resto],
           "210.000 eventos con 60.000 temas y unas 45.000 consultas TC.",
           {"tle": "Cada TC (o cada búsqueda de un tema) recorre todos los temas: O(temas) por evento es demasiado. Con IndexPQ cada TC son 3 pop y 3 push.",
            "mle": "Gastas demasiada memoria: guarda una entrada por tema, no una por evento."},
           ["Con 60.000 temas y 45.000 TC, recorrerlos todos en cada consulta son 2,7·10⁹ comparaciones.",
            "Para encontrar el índice de un tema usa un unordered_map<string,int>.",
            "En cada TC saca como mucho 3 cimas, escríbelas y vuelve a meterlas: O(log n)."])
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(c) for c in casos),
                   salida="".join(l + "\n" for c in casos for l in tridente(c)),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_SOL = (pathlib.Path(__file__).resolve().parent.parent.parent / CONFIG["solucion"]).read_bytes().decode("utf-8", "replace")
_i = _SOL.index("vector<IndexPQ<Prio, Mejor>::Par> podio;")
_PODIO = _SOL[_i:_SOL.index("pq.push(p.elem, p.prioridad);", _i) + len("pq.push(p.elem, p.prioridad);")]
_PODIO_LINEAL = """vector<int> usados;
            for (int k = 0; k < 3; ++k) {
                int mejor = -1;
                for (int i = 0; i < (int)nombre.size(); ++i) {
                    bool ya = false;
                    for (int u : usados) if (u == i) ya = true;
                    if (ya || pq.priority(i).citas <= 0) continue;
                    if (mejor == -1 || Mejor()(pq.priority(i), pq.priority(mejor))) mejor = i;
                }
                if (mejor == -1) break;
                usados.push_back(mejor);
                cout << k + 1 << ' ' << nombre[mejor] << '\\n';
            }"""

VARIANTES = [
    Variante("desempate por el C más antiguo", [("return a.ultimoC > b.ultimoC;", "return a.ultimoC < b.ultimoC;")], prueba=5, v="wa"),
    Variante("guarda solo el primer C",
             [("if (tipo == \"C\") { p.citas += m; p.ultimoC = t; }", "if (tipo == \"C\") { p.citas += m; if (p.ultimoC < 0) p.ultimoC = t; }")],
             prueba=6, v="wa"),
    Variante("la E también cuenta como reciente", [("else p.citas -= m;", "else { p.citas -= m; p.ultimoC = t; }")], prueba=7, v="wa"),
    Variante("escribe temas con 0 citas", [("&& pq.top().prioridad.citas > 0", "")], prueba=8, v="wa"),
    Variante("no devuelve el podio a la cola", [("for (auto const& p : podio) pq.push(p.elem, p.prioridad);", "")], prueba=9, v="rte"),
    Variante("podio de cuatro (≤ 3)", [("podio.size() < 3", "podio.size() <= 3")], prueba=10, v="wa"),
    Variante("criterios en orden inverso (recencia primero)",
             [("if (a.citas != b.citas) return a.citas > b.citas;", "if (a.ultimoC != b.ultimoC) return a.ultimoC > b.ultimoC;"),
              ("return a.ultimoC > b.ultimoC;                      // empate", "return a.citas > b.citas;                      // empate")],
             prueba=11, v="wa"),
    Variante("el mapa de temas no se vacía entre casos",
             [("unordered_map<string, int> indice;", "static unordered_map<string, int> indice;")], prueba=14, v="rte"),
    Variante("olvida la línea ---", [("cout << \"---\\n\";", "")], prueba=[2, 4], v="wa"),
    Variante("puesto y tema en líneas distintas", [("cout << k + 1 << ' ' << nombre", "cout << k + 1 << '\\n' << nombre")], prueba=1, v="pe"),
    Variante("busca el podio recorriendo todos los temas", [(_PODIO, _PODIO_LINEAL)], prueba=18, v="tle"),
]
