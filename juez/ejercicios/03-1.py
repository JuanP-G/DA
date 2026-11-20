"""03-1 · Volando drones: juez con pruebas pensadas para cada error típico."""
import heapq
import pathlib
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-1/EJ_03-1.cpp",
    "cabeceras": ["3-Colas de prioridad variable (Heapsort)/EJ_03-1/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["if (p1.prioridad > 0) sobran1V.push_back({ p1.elem, p1.prioridad });",
              "if (p1.prioridad > 0) cola1V.push(p1.elem, p1.prioridad);"],
}


def sabados(N, nueve, uno):
    """Solucionador independiente: dos montículos de máximos (heapq con signo cambiado)."""
    a = [-x for x in nueve]
    b = [-x for x in uno]
    heapq.heapify(a)
    heapq.heapify(b)
    res = []
    while a and b:
        total, vuelven_a, vuelven_b = 0, [], []
        for _ in range(N):
            if not a or not b:
                break
            x, y = -heapq.heappop(a), -heapq.heappop(b)
            t = min(x, y)
            total += t
            if x > t:
                vuelven_a.append(x - t)
            if y > t:
                vuelven_b.append(y - t)
        for x in vuelven_a:
            heapq.heappush(a, -x)
        for y in vuelven_b:
            heapq.heappush(b, -y)
        res.append(total)
    return res


def caso_a_texto(c):
    N, nueve, uno = c
    return f"{N} {len(nueve)} {len(uno)}\n" + " ".join(map(str, nueve)) + "\n" + " ".join(map(str, uno)) + "\n"


def aleatorio(r, maxN, maxP, maxH):
    return (r.randint(1, maxN), [r.randint(1, maxH) for _ in range(r.randint(1, maxP))],
            [r.randint(1, maxH) for _ in range(r.randint(1, maxP))])


def pruebas():
    r = random.Random(31)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(2, [5, 12, 7, 15], [10, 10]), (2, [5, 12, 7, 15], [20, 20, 2]),
            (20, [3, 3, 3], [25, 15, 10]), (1, [5, 9, 2, 6], [7, 3, 3, 1, 6, 4])],
           "Los cuatro casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (N, A, B y luego A horas de 9 V y B de 1,5 V), las colas o el bucle de sábados.",
            "pe": "Los números están bien pero no el formato: los totales de los sábados van en UNA línea por caso, separados por un espacio.",
            "tle": "El programa no termina: casi seguro el bucle de sábados no acaba nunca. ¿Vuelves a meter en la caja pilas gastadas (0 horas)? Un dron con una pila a 0 vuela 0 horas y nada cambia."},
           ["Haz a mano el segundo caso: el primer sábado vuelan 15 + 12 = 27 horas y el segundo 7 + 5 = 12.",
            "Cada caso es UNA línea con los totales de todos los sábados separados por espacios.",
            "La entrada no dice cuántos casos hay: lee hasta que falle la lectura de N (plantilla de casos ilimitados)."])
    prueba("Un dron y una pila de cada tipo", "borde",
           [(1, [5], [3]), (1, [4], [4]), (1, [2], [9])],
           "El mínimo: un dron, una pila de 9 V y una de 1,5 V; solo hay un sábado.",
           {"wa": "Con una pila de cada tipo el dron vuela min(h9, h1) horas una sola vez. Si sale otra cosa, revisa el mínimo y que paras cuando una caja queda vacía.",
            "rte": "Con una pila de cada tipo te sales: ¿consultas la cola vacía después del primer vuelo?",
            "tle": "Con una pila de cada tipo no termina: tras el primer vuelo una caja queda vacía y hay que parar."},
           ["Con 5 y 3 horas el dron vuela 3 y la pila de 9 V vuelve con 2, pero ya no hay pilas de 1,5 V: se acabó.",
            "El bucle de sábados sigue solo mientras las DOS cajas tienen pilas."])
    prueba("Más drones que parejas de pilas", "trampa",
           [(1000, [4, 2], [4, 2]), (5, [7], [2, 2, 2, 2])],
           "N es mayor que las pilas que hay: vuelan los drones que se puedan y el resto se queda en tierra.",
           {"rte": "Sacas pilas de una caja vacía: dentro del bucle de drones hay que comprobar también que quedan pilas de los dos tipos.",
            "wa": "Cuando hay menos parejas que drones, el sábado termina al vaciarse una caja, no al llegar a N drones."},
           ["En el primer caso hay 1000 drones pero solo 2 parejas de pilas: vuelan 2 drones y se acabó («6»).",
            "La condición del bucle de drones necesita tres cosas: quedan drones, quedan pilas de 9 V y quedan pilas de 1,5 V."])
    prueba("Todas las pilas iguales", "borde",
           [(2, [5, 5, 5, 5], [5, 5, 5, 5]), (3, [7, 7, 7], [7, 7, 7])],
           "Pilas que se agotan a la vez: no vuelve ninguna a la caja.",
           {"wa": "Si las dos pilas de un dron se agotan a la vez, ninguna vuelve. Revisa que solo devuelves las que tienen MÁS de 0 horas.",
            "tle": "Si vuelves a meter pilas con 0 horas, los drones vuelan 0 horas para siempre y el bucle no termina.",
            "ole": "Escribes sin parar: el bucle de sábados no termina porque vuelves a meter pilas gastadas (0 horas) y los drones vuelan 0 horas una y otra vez."},
           ["Con 4 y 4 pilas de 5 horas y 2 drones: dos sábados de 10 horas, «10 10».",
            "Una pila con 0 horas va al reciclaje: no la devuelvas a la caja."])
    prueba("Horas grandes (total de 10⁹)", "borde",
           [(1, [1000000000], [1000000000]), (2, [600000000, 400000000, 7], [500000000, 500000000])],
           "Pilas con muchísimas horas: el total de un sábado llega a 10⁹ y cabe justo en int.",
           {"wa": "Con valores grandes algo se corta: revisa que lees y sumas con int (o long long) y no con un tipo más pequeño."},
           ["El enunciado garantiza que cada total es como mucho 10⁹: int basta, pero no uses short ni float.",
            "Comprueba el segundo caso a mano: el primer sábado vuelan 500000000 + 400000000."])
    prueba("Las pilas sobrantes no vuelven el mismo sábado", "trampa",
           [(2, [10], [3, 3])],
           "Una pila que sobra se guarda al volver al club: ese mismo sábado ya no puede ir en otro dron.",
           {"wa": "Devuelves la pila sobrante a la caja en cuanto aterriza el dron, y otro dron la usa ese mismo sábado. Las sobrantes deben esperar al final del sábado."},
           ["Solo hay una pila de 9 V: el primer sábado vuela un único dron (3 horas), aunque haya dos. La respuesta es «3 3».",
            "Las pilas se colocan en el club antes de salir: cada pila va como mucho en un dron cada sábado.",
            "Guarda las sobrantes en un vector aparte y mételas en las colas cuando acabe el bucle de drones de ese sábado."])
    prueba("Se cogen las pilas más cargadas", "trampa",
           [(1, [2, 9], [5])],
           "Cada dron lleva la pila MÁS cargada de cada caja: hacen falta colas de máximos.",
           {"wa": "Estás cogiendo las pilas menos cargadas: la IndexPQ (o priority_queue) que usas es de mínimos. Con IndexPQ hace falta greater<int>."},
           ["El dron debe llevar la pila de 9 horas, no la de 2: vuela 5 horas y se acaba la única pila de 1,5 V.",
            "IndexPQ<int> por defecto saca el MENOR. Para sacar el mayor: IndexPQ<int, greater<int>>."])
    prueba("Solo vuelan N drones cada sábado", "trampa",
           [(2, [5, 5, 5], [5, 5, 5])],
           "Hay pilas para más drones de los que tenemos: cada sábado vuelan exactamente N.",
           {"wa": "Vuelan más drones de los que hay: o no limitas el bucle de drones a N, o el contador llega a N incluido (≤ en vez de <)."},
           ["Hay 3 parejas pero solo 2 drones: «10 5», no «15».",
            "Cuenta los drones que despegan: el bucle del sábado debe parar cuando el contador llegue a N (condición contador < N)."])
    prueba("La pila de 9 V que sobra vuelve con lo que le queda", "trampa",
           [(1, [10], [4, 4, 4])],
           "Tras volar, a la pila que sobra hay que restarle las horas voladas.",
           {"wa": "La pila sobrante vuelve a la caja con las horas que tenía al principio (o no vuelve): hay que restarle lo que ha volado el dron."},
           ["La pila de 9 V pasa de 10 a 6 y luego a 2: «4 4 2».",
            "Resta min(h9, h1) a LAS DOS pilas del dron, y la que quede con horas vuelve a su caja."])
    prueba("La pila de 1,5 V que sobra también vuelve", "trampa",
           [(1, [4, 4, 4], [10])],
           "La pila sobrante puede ser la de 1,5 V: también vuelve a su caja.",
           {"wa": "Solo devuelves a la caja las pilas de 9 V que sobran. Las de 1,5 V también pueden sobrar."},
           ["La pila de 1,5 V tiene 10 horas: vuela 4, 4 y 2 en tres sábados seguidos.",
            "Trata las dos cajas igual: las sobrantes de cualquiera de los dos tipos vuelven al final del sábado."])
    prueba("Un tipo de pila se acaba antes que el otro", "trampa",
           [(3, [1, 1, 1, 1, 1, 1, 1, 1], [9])],
           "Quedan muchas pilas de un tipo pero ninguna del otro: ya no se puede volar.",
           {"wa": "Sigues contando sábados cuando una caja está vacía, o paras demasiado pronto. Se vuela mientras queden pilas de LOS DOS tipos.",
            "pe": "Revisa los espacios: entre sábados un espacio, y al final del caso un salto de línea (sin espacio ni línea en blanco extra)."},
           ["La única pila de 1,5 V (9 horas) se gasta 1 hora cada sábado: nueve sábados de 1 hora.",
            "El bucle de sábados es «mientras ninguna de las dos colas esté vacía»."])
    prueba("Varios casos seguidos", "trampa",
           [(1, [9, 9, 9], [1]), (1, [2], [3]), (2, [5], [7, 7]), (3, [1, 2, 3], [3, 2, 1])],
           "Un caso que deja pilas sin usar seguido de otros: nada del caso anterior debe quedar en las cajas.",
           {"wa": "Algo se arrastra de un caso a otro: las colas, los vectores de sobrantes o los contadores deben crearse dentro de resuelveCaso.",
            "rte": "Una estructura de un caso anterior (con otro tamaño o con pilas que aún estaban dentro) se reutiliza en el siguiente.",
            "pe": "A partir del segundo caso hay un espacio de más al principio de la línea: la variable que controla el primer número debe reiniciarse en cada caso."},
           ["Tras el primer caso quedan dos pilas de 9 V con 9 horas: el segundo caso no debe verlas.",
            "Declara las colas, los vectores y los contadores dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio(r, 4, 7, 9) for _ in range(60)],
           "60 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: busca qué caso es (una línea por caso) y simúlalo a mano.",
            "rte": "Algún caso pequeño hace que consultes una caja vacía."},
           ["La línea que falla es el número del caso: búscalo en la entrada.",
            "Simula los sábados en papel con dos listas ordenadas de mayor a menor."])
    prueba("Aleatorios medianos", "aleatorio", [aleatorio(r, 30, 200, 1000) for _ in range(30)],
           "30 casos medianos al azar, con muchos drones y sábados.",
           {"wa": "Falla algún caso mediano: busca entre las pruebas pequeñas cuál falla también, es más fácil de seguir."},
           ["Si las pequeñas salen bien, revisa lo que solo pasa con muchos drones: límite de N, sobrantes que se repiten…",
            "Comprueba que cada pila va como mucho en un dron por sábado."])
    prueba("Un dron y 200.000 sábados", "rendimiento",
           [(1, [1000000], [5] * 200000)],
           "Un solo dron y 200.000 pilas pequeñas: hay 200.000 sábados, cada uno debe costar poco.",
           {"tle": "Haces demasiado trabajo cada sábado (ordenar las cajas, copiar las colas, recorrer todas las pilas…). Cada sábado debe costar O(drones · log P).",
            "ole": "Escribes demasiado: un número por sábado, en una sola línea."},
           ["Hay 200.000 sábados: si cada uno recorre las 200.000 pilas, son 4·10¹⁰ operaciones.",
            "No ordenes ni copies las cajas cada sábado: las colas de prioridad ya mantienen el orden.",
            "Dentro de un sábado solo se tocan las pilas que se usan: top/pop al montarlas y push de las sobrantes."])
    prueba("Tamaño máximo (1000 drones y 200.000 pilas por caja)", "rendimiento",
           [(1000, [r.randint(1, 999) for _ in range(200000)], [r.randint(1, 999) for _ in range(200000)])],
           "El tamaño máximo con pilas al azar: mide la eficiencia de sacar la pila más cargada.",
           {"tle": "Buscar la pila más cargada recorriendo todo el vector es O(P) por dron. Con una cola de prioridad es O(log P).",
            "mle": "Gastas demasiada memoria: dos colas de 200.000 enteros caben de sobra; ¿copias estructuras grandes en cada vuelo?"},
           ["Cuenta las operaciones: hay hasta 400.000 vuelos; cada uno debe costar O(log P).",
            "Usa una cola de máximos por tipo de pila (IndexPQ<int, greater<int>> o priority_queue<int>)."])
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(c) for c in casos),
                   salida="".join(" ".join(map(str, sabados(*c))) + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


# ---------------------------------------------------------------- variantes con fallos típicos

_SOL = (pathlib.Path(__file__).resolve().parent.parent.parent / CONFIG["solucion"]).read_bytes().decode("utf-8", "replace")


def _trozo(desde, hasta):
    """Texto de la solución desde `desde` hasta `hasta` (incluido)."""
    i = _SOL.index(desde)
    return _SOL[i:_SOL.index(hasta, i) + len(hasta)]


_ORDENA_CADA_SABADO = """vector<int> v9, v1;
	while (!cola9V.empty()) { v9.push_back(cola9V.top().prioridad); cola9V.pop(); }
	while (!cola1V.empty()) { v1.push_back(cola1V.top().prioridad); cola1V.pop(); }
	bool primero = true;
	while (!v9.empty() && !v1.empty()) {
		sort(v9.begin(), v9.end(), greater<int>());
		sort(v1.begin(), v1.end(), greater<int>());
		int horasFinde = 0, k = min((int)min(v9.size(), v1.size()), drones);
		vector<int> n9, n1;
		for (int i = 0; i < k; ++i) {
			int t = min(v9[i], v1[i]); horasFinde += t;
			if (v9[i] > t) n9.push_back(v9[i] - t);
			if (v1[i] > t) n1.push_back(v1[i] - t);
		}
		for (int i = k; i < (int)v9.size(); ++i) n9.push_back(v9[i]);
		for (int i = k; i < (int)v1.size(); ++i) n1.push_back(v1[i]);
		v9 = n9; v1 = n1;
		if (!primero) cout << ' ';
		cout << horasFinde;
		primero = false;
	}"""

VARIANTES = [
    Variante("devuelve la pila sobrante en el momento",
             [("if (p9.prioridad > 0) sobran9V.push_back({ p9.elem, p9.prioridad });",
               "if (p9.prioridad > 0) cola9V.push(p9.elem, p9.prioridad);"),
              ("if (p1.prioridad > 0) sobran1V.push_back({ p1.elem, p1.prioridad });",
               "if (p1.prioridad > 0) cola1V.push(p1.elem, p1.prioridad);")], prueba=6, v="wa"),
    Variante("colas de mínimos", [("IndexPQ<int, greater<int>> cola9V(pila9V);", "IndexPQ<int> cola9V(pila9V);"),
                                  ("IndexPQ<int, greater<int>> cola1V(pila1V);", "IndexPQ<int> cola1V(pila1V);")], prueba=7, v="wa"),
    Variante("no limita los drones a N", [("while (contador < drones && !cola9V.empty()", "while (!cola9V.empty()")], prueba=8, v="wa"),
    Variante("un dron de más (≤ N)", [("while (contador < drones && ", "while (contador <= drones && ")], prueba=8, v="wa"),
    Variante("no resta las horas a la pila de 9 V", [("p9.prioridad -= tiempo;", "")], prueba=9, v="wa"),
    Variante("no devuelve las pilas de 1,5 V", [("for (auto& s : sobran1V) cola1V.push(s.first, s.second);", "")], prueba=10, v="wa"),
    Variante("devuelve también las pilas gastadas", [("if (p9.prioridad > 0) sobran9V", "if (p9.prioridad >= 0) sobran9V"),
                                                    ("if (p1.prioridad > 0) sobran1V", "if (p1.prioridad >= 0) sobran1V")], prueba=4, v="ole"),
    Variante("no comprueba las cajas dentro del sábado",
             [("while (contador < drones && !cola9V.empty() && !cola1V.empty())", "while (contador < drones)")], prueba=3, v="rte"),
    Variante("un sábado por línea", [("if (!primero) cout << ' ';", "if (!primero) cout << '\\n';")], prueba=1, v="pe"),
    Variante("las cajas no se vacían entre casos",
             [("IndexPQ<int, greater<int>> cola9V(pila9V); //greater<int> para que sea maximos",
               "static IndexPQ<int, greater<int>> cola9V(2000000); static int b9 = 0; int base9 = b9; b9 += pila9V;"),
              ("cola9V.push(i, horas);", "cola9V.push(base9 + i, horas);")], prueba=12, v="wa"),
    Variante("ordena las cajas cada sábado",
             [(_trozo("bool primero = true;", "primero = false;\n\t}"), _ORDENA_CADA_SABADO),
              ("#include <functional>", "#include <functional>\n#include <algorithm>")], prueba=15, v="tle"),
]
