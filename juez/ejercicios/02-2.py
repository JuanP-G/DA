"""02-2 · Unidad Curiosa de Monitorización: juez con pruebas pensadas para cada error típico.

Formato: varios casos; cada uno «n», n líneas «identificador periodo» (10³ ≤ id ≤ 10⁹, distintos;
1 ≤ periodo ≤ 5.000; n ≤ 25.000) y «K» (1 ≤ K ≤ 100.000). Acaba con n = 0.
Salida: los K identificadores, uno por línea, y «---» tras cada caso.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-2/EJ_02-2.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["return id > o.id;", "return id < o.id;"],
}

MINID, MAXID = 1000, 10 ** 9
MAXP = 5000
MAXN = 25000
MAXK = 100000


def envios(usuarios, K):
    """Simulación por eventos: el próximo envío es el de menor (instante, identificador)."""
    h = [(p, i, p) for i, p in usuarios]
    heapq.heapify(h)
    res = []
    for _ in range(K):
        t, i, p = heapq.heappop(h)
        res.append(i)
        heapq.heappush(h, (t + p, i, p))
    return res


def texto_entrada(casos):
    out = []
    for usuarios, K in casos:
        out.append(f"{len(usuarios)}\n")
        out.extend(f"{i} {p}\n" for i, p in usuarios)
        out.append(f"{K}\n")
    out.append("0\n")
    return "".join(out)


def texto_salida(casos):
    return "".join("".join(f"{i}\n" for i in envios(u, K)) + "---\n" for u, K in casos)


def ids_distintos(r, n, lo=MINID, hi=MAXID):
    return r.sample(range(lo, hi + 1), n)


def pruebas():
    r = random.Random(351)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [([(1234, 300), (9000, 200)], 5), ([(1111, 100), (9999, 1000)], 9), ([(1000, 1)], 1)],
           "Los tres casos del PDF, con su «---» detrás de cada uno.",
           {"wa": "Si fallan hasta los ejemplos, revisa la base: cada usuario recibe su primer envío a los Periodo segundos y luego cada Periodo segundos; sale siempre el envío más próximo.",
            "pe": "Los identificadores están bien pero no el formato: uno por línea y una línea «---» tras cada caso."},
           ["Haz a mano el primer ejemplo: envíos en 200 (9000), 300 (1234), 400 (9000), 600 (empate: 1234 y luego 9000).",
            "Tras los K identificadores de cada caso va una línea con exactamente tres guiones.",
            "La entrada termina con n = 0: usa la plantilla de centinela."])
    prueba("Separador «---» y fin con n = 0", "trampa",
           [([(1000, 1)], 2), ([(123456789, 5000)], 1)],
           "Casos de un único usuario (no hay nada que ordenar): solo se mira el separador y que el 0 final no se procese.",
           {"wa": "Falla el formato de los separadores: tras cada caso va una línea con TRES guiones («---», no «----» como en Acepta el Reto), y tras el 0 final no se escribe nada (si sale un «---» de más al final, estás procesando el caso n = 0).",
            "ole": "No te detienes al leer n = 0 y el programa sigue escribiendo.",
            "tle": "El bucle de casos no termina al leer n = 0."},
           ["Compara las líneas de separación de tu salida con la esperada: ¿cuántos guiones tienen?",
            "Mira el final de tu salida: después del último caso no debe aparecer otro «---».",
            "«cin >> n; if (n == 0) return false;» antes de escribir nada; y al final de cada caso, cout << \"---\\n\"."])
    prueba("Un solo envío (K = 1)", "trampa",
           [([(7000, 10)], 1)],
           "Un usuario y K = 1: la salida es su identificador y el «---». Mira que se hacen exactamente K envíos.",
           {"wa": "No haces exactamente K envíos: con K = 1 debe salir un identificador (si no sale ninguno, el bucle da una vuelta de menos; si salen dos, una de más).",
            "pe": "Revisa que el identificador y el «---» van en líneas distintas."},
           ["Con K = 1 la salida es una línea con un identificador y otra con «---».",
            "Cuenta las vueltas de tu bucle de envíos cuando K = 1.",
            "El bucle de envíos debe ser for (int i = 0; i < K; ++i): K vueltas exactas."])
    prueba("Un solo usuario", "borde",
           [([(MAXID, MAXP)], 7)],
           "Un único usuario con el identificador y el periodo máximos: recibe todos los envíos.",
           {"wa": "Con un solo usuario todos los envíos son suyos: si sale otra cosa, revisa cómo lees el identificador (llega hasta 10⁹, cabe en int) y que lo vuelves a meter en la cola tras cada envío.",
            "rte": "Con un solo usuario la cola se queda vacía: después de sacar la cima hay que volver a meterla con su siguiente instante."},
           ["Con un solo usuario, después de cada envío la cola debe seguir teniendo un elemento.",
            "Saca la cima, escribe su id, súmale el periodo a su instante y vuelve a meterla."])
    prueba("Primero el envío más próximo", "trampa",
           [([(1000, 5), (2000, 7)], 1), ([(1500, 1), (2500, 9), (3000, 7)], 1), ([(4000, 3), (9000, 3000)], 1)],
           "Usuarios con periodos distintos y un solo envío: sale el usuario cuyo primer envío ocurre antes.",
           {"wa": "Sale primero el envío MÁS LEJANO: tu cola es de máximos. priority_queue usa operator< y pone arriba el mayor; para tener arriba el instante menor usa greater<> con operator> (o invierte la comparación)."},
           ["En el primer caso el 1000 recibe en t = 5 y el 2000 en t = 7: el primer envío es para el 1000.",
            "¿Qué elemento deja arriba tu priority_queue: el de instante menor o el de instante mayor?",
            "Define operator> comparando (t, id) y declara priority_queue<Envio, vector<Envio>, greater<Envio>>."])
    prueba("El primer envío llega a los Periodo segundos", "trampa",
           [([(1000, 10), (2000, 3)], 1), ([(3000, 4), (1000, 6), (2000, 5)], 1)],
           "El primer envío a cada usuario es en el instante Periodo, no en el 0.",
           {"wa": "Haces el primer envío en el instante 0 (y entonces salen todos a la vez, ordenados por id). El enunciado dice que el primero llega cuando han pasado Periodo segundos desde el registro."},
           ["En el primer caso el 2000 recibe en t = 3 y el 1000 no recibe nada hasta t = 10: el primer envío es para el 2000.",
            "¿Con qué instante metes a cada usuario en la cola al principio?",
            "Al registrar a un usuario, mételo con t = periodo, no con t = 0."])
    prueba("Los envíos se repiten cada Periodo", "trampa",
           [([(1000, 3), (2000, 4)], 5)],
           "Tras cada envío, el siguiente a ese usuario es Periodo segundos después del anterior.",
           {"wa": "El siguiente envío no se calcula bien: tras enviar en el instante t, el usuario vuelve a la cola con t + periodo (no con periodo a secas, ni con 2·t)."},
           ["Aquí se alternan: 3 (1000), 4 (2000), 6 (1000), 8 (2000), 9 (1000).",
            "Si siempre sale el mismo usuario, no estás acumulando su instante.",
            "Copia la cima, haz pop(), suma e.t += e.periodo y vuelve a hacer push(e)."])
    prueba("Empate: primero el identificador menor", "trampa",
           [([(9000, 100), (1234, 100)], 4), ([(5000, 3), (4000, 3), (3000, 3)], 6),
            ([(8888, 6), (7777, 4)], 4)],
           "Envíos simultáneos: se hacen en orden creciente de identificador, aunque en la entrada vengan al revés.",
           {"wa": "Los empates no salen por id creciente: o no desempatas (la priority_queue no respeta ningún orden entre iguales), o desempatas al revés, o por orden de entrada. A igual instante, va primero el identificador MENOR."},
           ["En el primer caso los dos reciben a la vez en t = 100: primero el 1234 y luego el 9000.",
            "El orden de la cola tiene que ser (instante, identificador): si los instantes son iguales, decide el id.",
            "En operator>: if (t != o.t) return t > o.t; return id > o.id;"])
    prueba("Desempate por identificador, no por periodo", "trampa",
           [([(2000, 2), (1000, 3)], 4)],
           "En t = 6 coinciden los dos: va antes el 1000 (id menor) aunque su periodo sea mayor.",
           {"wa": "En el empate de t = 6 escribes primero el 2000: desempatas por periodo (o por orden de entrada). El enunciado dice que a igual instante decide SOLO el identificador."},
           ["Envíos: 2 (2000), 3 (1000), 4 (2000) y en 6 coinciden los dos.",
            "El periodo no interviene en el orden: solo el instante y, a igualdad, el identificador."])
    ids = ids_distintos(r, 12, 1000, 1100)
    prueba("Muchos empates a la vez", "trampa",
           [([(i, 7) for i in ids], 36)],
           "Doce usuarios con el mismo periodo: en cada instante hay doce envíos simultáneos.",
           {"wa": "Con muchos empates seguidos la priority_queue los devuelve en cualquier orden si el comparador no desempata por id. Comprueba que el desempate está en el comparador, no en el orden de inserción."},
           ["Debe salir tres veces la lista de los doce identificadores ordenados de menor a mayor.",
            "La priority_queue no es estable: el orden entre elementos «iguales» para el comparador no está garantizado.",
            "Incluye el id en la comparación cuando los instantes coinciden."])
    prueba("Identificadores y periodos extremos", "borde",
           [([(MAXID, 1), (MINID, MAXP), (MAXID - 1, 1)], 12)],
           "Identificadores 1000 y 10⁹ y periodos 1 y 5000.",
           {"wa": "Con valores extremos algo se lee o se compara mal: el id llega a 10⁹ (cabe en int, pero no en short ni en float) y el periodo puede ser 1."},
           ["Comprueba que lees el id y el periodo en el orden correcto (primero el id).",
            "Usa int (o long long) para id y periodo; nada de float."])
    prueba("Periodo 1 frente a periodo 5000", "borde",
           [([(5555, MAXP), (4444, 1)], 5002)],
           "Un usuario recibe cada segundo y el otro solo en t = 5000, donde empatan.",
           {"wa": "En t = 5000 coinciden los dos: va antes el 4444. Revisa el desempate y que el usuario de periodo 5000 aparece en el envío 5001.",
            "tle": "Si simulas el tiempo segundo a segundo, con periodos grandes se hace eterno: salta directamente al próximo envío con la cola."},
           ["Los primeros 4999 envíos son del 4444; en t = 5000 reciben los dos (primero el 4444).",
            "Los envíos 5000, 5001 y 5002 son 4444, 5555 y 4444."])
    prueba("Varios casos seguidos", "trampa",
           [([(1000, 2), (2000, 3), (3000, 4)], 8), ([(9999, 1)], 3), ([(4000, 5), (1000, 5)], 2),
            ([(2000, 10)], 1)],
           "Varios casos uno tras otro: la cola debe empezar vacía en cada caso.",
           {"wa": "El primer caso sale bien y los siguientes no: la cola (o algo) se arrastra de un caso al siguiente. Al terminar un caso la cola NO queda vacía (siguen todos los usuarios), así que debe ser local a resuelveCaso.",
            "rte": "Algo del caso anterior se queda a medias: declara la cola dentro de resuelveCaso."},
           ["Al final de cada caso en la cola siguen todos los usuarios con sus próximos envíos.",
            "Si la cola es global, en el caso siguiente aparecen usuarios que no existen.",
            "Declara la priority_queue dentro de resuelveCaso."])
    casos = []
    for _ in range(250):
        n = r.randint(1, 6)
        ids = ids_distintos(r, n, *r.choice([(1000, 1020), (1000, 10 ** 9)]))
        casos.append(([(i, r.randint(1, r.choice([4, 10, 30]))) for i in ids], r.randint(1, 20)))
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "250 casos pequeños al azar, con periodos pequeños y muchos empates.",
           {"wa": "Algún caso concreto falla: cuenta los «---» de la salida esperada hasta la línea que falla para saber qué caso es, y hazlo a mano.",
            "rte": "Algún caso pequeño rompe el programa."},
           ["Localiza el caso por el número de «---» anteriores a la línea que falla.",
            "Apunta los instantes de envío de cada usuario y ordénalos por (instante, id)."])
    casos = []
    for _ in range(20):
        n = r.randint(50, 2000)
        ids = ids_distintos(r, n)
        casos.append(([(i, r.randint(1, r.choice([50, MAXP]))) for i in ids], r.randint(1000, 5000)))
    prueba("Aleatorios medianos", "aleatorio", casos,
           "20 casos de hasta 2000 usuarios y 5000 envíos.",
           {"wa": "Con casos medianos aparece un fallo que en los pequeños no: revisa el desempate y que cada usuario está una sola vez en la cola.",
            "tle": "Algo es más lento de la cuenta incluso con casos medianos."},
           ["Cada usuario debe estar exactamente una vez en la cola en todo momento.",
            "Comprueba que el comparador ordena por (instante, id)."])
    ids = ids_distintos(r, MAXN)
    prueba("Grande: 25.000 usuarios y 100.000 envíos", "rendimiento",
           [([(i, r.randint(1, MAXP)) for i in ids], MAXK)],
           "El tamaño máximo: mide la eficiencia (debe ser O((n + K) log n)).",
           {"tle": "Buscar el próximo envío recorriendo los n usuarios cuesta O(n·K) = 2,5·10⁹: usa una cola de prioridad, así cada envío cuesta O(log n).",
            "wa": "Con muchos usuarios falla algo que en los pequeños no: revisa el desempate por id."},
           ["¿Cuánto cuesta encontrar el próximo envío? Se hace K veces.",
            "Con una cola de prioridad con un elemento por usuario, cada envío es un pop y un push: O(log n)."])
    ids = ids_distintos(r, MAXN)
    prueba("Grande: 25.000 usuarios con el mismo periodo", "rendimiento",
           [([(i, MAXP) for i in ids], MAXK)],
           "25.000 envíos simultáneos en cada instante: todo el trabajo está en los empates.",
           {"tle": "Con todos los envíos empatados tu solución se vuelve lenta: ¿simulas el tiempo segundo a segundo, o recorres todos los usuarios en cada envío?",
            "wa": "Con 25.000 empates en cada instante el orden debe ser exactamente el de los identificadores crecientes."},
           ["Cada envío debe costar O(log n), haya o no empates.",
            "No avances el tiempo de uno en uno: la cima de la cola ya te dice cuál es el próximo instante."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida=texto_salida(c), casos=len(c),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


VARIANTES = [
    Variante("separador de cuatro guiones (formato de Acepta el Reto)", [('cout << "---\\n";', 'cout << "----\\n";')],
             prueba=2, v="wa"),
    Variante("hace K − 1 envíos", [("for (int i = 0; i < K; ++i) {", "for (int i = 1; i < K; ++i) {")], prueba=3, v="wa"),
    Variante("cola de máximos (operator< sin greater)",
             [("bool operator>(", "bool operator<("),
              ("if (t != o.t) return t > o.t;\n        return id > o.id;", "if (t != o.t) return t < o.t;\n        return id < o.id;"),
              ("priority_queue<Envio, vector<Envio>, greater<Envio>> cola;", "priority_queue<Envio> cola;")],
             prueba=5, v="wa"),
    Variante("primer envío en el instante 0", [("cola.push({ (long long)p, id, p });", "cola.push({ 0, id, p });")],
             prueba=6, v="wa"),
    Variante("no acumula el instante (vuelve con t = periodo)", [("e.t += e.periodo;", "e.t = e.periodo;")],
             prueba=7, v="wa"),
    Variante("sin desempate por id", [("return id > o.id;", "return false;")], prueba=8, v="wa"),
    Variante("desempate al revés (id mayor primero)", [("return id > o.id;", "return id < o.id;")], prueba=8, v="wa"),
    Variante("desempata primero por periodo",
             [("return id > o.id;", "if (periodo != o.periodo) return periodo > o.periodo;\n        return id > o.id;")],
             prueba=9, v="wa"),
    Variante("cola global que no se vacía entre casos",
             [("bool resuelveCaso() {", "priority_queue<Envio, vector<Envio>, greater<Envio>> cola;\nbool resuelveCaso() {"),
              ("    priority_queue<Envio, vector<Envio>, greater<Envio>> cola;\n\n", "\n")],
             prueba=13, v="wa"),
    Variante("busca el mínimo recorriendo todos los usuarios (O(n·K))",
             [("""    for (int i = 0; i < K; ++i) {
        Envio e = cola.top(); cola.pop();
        cout << e.id << '\\n';
        e.t += e.periodo;                   // modifico mi copia
        cola.push(e);
    }""", """    vector<Envio> v;
    while (!cola.empty()) { v.push_back(cola.top()); cola.pop(); }
    for (int i = 0; i < K; ++i) {
        int m = 0;
        for (int j = 1; j < (int)v.size(); ++j)
            if (v[m] > v[j]) m = j;
        cout << v[m].id << '\\n';
        v[m].t += v[m].periodo;
    }""")], prueba=16, v="tle"),
]
