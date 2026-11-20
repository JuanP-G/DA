"""02-5 · Ordenando a los pacientes en urgencias: juez con pruebas pensadas para cada error típico.

Formato: varios casos; cada uno «n» (n ≤ 200.000) y n eventos: «I nombre gravedad» (nombre sin
espacios de hasta 20 caracteres, 0 ≤ gravedad ≤ 10⁶) o «A». Nunca hay una A sin pacientes.
Acaba con n = 0. Salida: el nombre atendido en cada A y «---» al final de cada caso.
"""
import heapq
import random
import string
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-5/EJ_02-5.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["return orden > o.orden;", "return orden < o.orden;"],
}

MAXG = 1_000_000


def atender(eventos):
    """El más grave; a igualdad, el que llegó antes (contador de llegadas)."""
    h, out, llegada = [], [], 0
    for ev in eventos:
        if ev[0] == "I":
            heapq.heappush(h, (-ev[2], llegada, ev[1]))
            llegada += 1
        else:
            out.append(heapq.heappop(h)[2])
    return out


def ev_texto(ev):
    return f"I {ev[1]} {ev[2]}" if ev[0] == "I" else "A"


def texto_entrada(casos):
    return "".join(f"{len(c)}\n" + "".join(ev_texto(e) + "\n" for e in c) for c in casos) + "0\n"


def texto_salida(casos):
    return "".join("".join(x + "\n" for x in atender(c)) + "---\n" for c in casos)


def I(nombre, g):
    return ("I", nombre, g)


A = ("A",)


def nombre_al_azar(r, largo=None):
    largo = largo or r.randint(1, 8)
    return "".join(r.choice(string.ascii_letters) for _ in range(largo))


def caso_al_azar(r, n, maxg, pA=0.45, largo=None):
    ev, esperando = [], 0
    for _ in range(n):
        if esperando and r.random() < pA:
            ev.append(A)
            esperando -= 1
        else:
            ev.append(I(nombre_al_azar(r, largo), r.randint(0, maxg)))
            esperando += 1
    return ev


def nombre_corto(k):
    s = ""
    k += 1
    while k:
        k, d = divmod(k - 1, 26)
        s = chr(97 + d) + s
    return s


def pruebas():
    r = random.Random(311)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [[I("Luis", 1000), I("Eva", 2000), A, A],
            [I("Alberto", 4000), I("Pepe", 3000), A, I("Rosa", 2000), I("Laura", 5000), A, I("Sara", 3000), A, A],
            [I("Ana", 0)]],
           "Los tres casos del PDF (el último sin ninguna atención), terminados con el 0.",
           {"wa": "Si fallan hasta los ejemplos, revisa la base: en cada A sale el paciente MÁS GRAVE y, a igualdad, el que llegó antes; tras cada caso, una línea «---».",
            "pe": "Los nombres están bien pero no el formato: un nombre por línea y «---» al final de cada caso."},
           ["En el segundo caso, Pepe y Sara tienen 3000: sale antes Pepe porque llegó antes.",
            "El tercer caso no tiene ninguna A: su salida es solo «---».",
            "La entrada termina con n = 0: usa la plantilla de centinela."])
    prueba("Separador «---» y fin con n = 0", "trampa",
           [[I("Ana", 0)], [I("Bob", 5), A], [I("X", 3), I("Y", 4)]],
           "Casos con un solo paciente atendido o sin ninguna atención: solo se mira el formato de los separadores y el final.",
           {"wa": "Falla el formato de los separadores: tras CADA caso (aunque no haya atendido a nadie) va una línea con tres guiones «---» (no «----» como en Acepta el Reto), y tras el 0 final no se escribe nada.",
            "ole": "No te detienes al leer n = 0 y el programa sigue escribiendo.",
            "tle": "El bucle de casos no termina al leer n = 0."},
           ["Mira la primera línea de tu salida: el primer caso no atiende a nadie y debe escribir solo «---».",
            "Después del último caso no debe aparecer otro «---».",
            "«if (!(cin >> n) || n == 0) return false;» y, al final de cada caso, cout << \"---\\n\" siempre."])
    prueba("Primero el más grave", "trampa",
           [[I("Leve", 1), I("Grave", 5), A]],
           "Dos pacientes de gravedad distinta: se atiende al de gravedad MAYOR.",
           {"wa": "Atiendes al MENOS grave: el comparador está al revés. priority_queue pone arriba el «mayor» según operator<, así que operator< debe devolver true cuando this tiene menos gravedad que o."},
           ["Con gravedades 1 y 5, ¿a quién atiendes?",
            "priority_queue es de máximos con operator<: si quieres arriba al más grave, «menor» debe significar «menos grave».",
            "En operator<: if (gravedad != o.gravedad) return gravedad < o.gravedad;"])
    prueba("Empate: el que más tiempo lleva esperando", "trampa",
           [[I("Ana", 7), I("Luis", 7), I("Zoe", 7), A, A, A]],
           "Tres pacientes con la misma gravedad: se atienden en el orden en que llegaron (como una cola, no como una pila).",
           {"wa": "Con gravedades iguales no atiendes por orden de llegada: o no desempatas (la priority_queue no respeta el orden de inserción), o desempatas al revés (atiendes primero al último en llegar). El que más tiempo lleva esperando es el que llegó ANTES."},
           ["La salida debe ser Ana, Luis, Zoe.",
            "Guarda en cada paciente un número de llegada creciente y úsalo para desempatar.",
            "Tiene menos prioridad el que llegó después: en operator<, return orden > o.orden;"])
    prueba("No se desempata por nombre", "trampa",
           [[I("Zoe", 7), I("Ana", 7), I("Marta", 7), A, A, A]],
           "Misma gravedad y nombres que no llegan en orden alfabético: manda el orden de llegada, no el nombre.",
           {"wa": "Desempatas por nombre (orden alfabético). El enunciado dice que a igual gravedad va el que más tiempo lleva esperando: Zoe, Ana y Marta, en ese orden."},
           ["Aquí la salida es Zoe, Ana, Marta, aunque alfabéticamente sea al revés.",
            "Si tu Paciente no tiene un campo con el orden de llegada y comparas por nombre (o comparas un pair/tuple que incluye el nombre), cámbialo.",
            "Añade un campo orden (el número de evento, por ejemplo) y desempata solo con él."])
    prueba("El orden de llegada no es la posición en la cola", "trampa",
           [[I("P1", 9), I("P2", 9), I("Quique", 5), A, A, I("Rita", 5), A, A]],
           "Quique llega antes que Rita (ambos 5): tras atender a otros, Quique sigue teniendo preferencia.",
           {"wa": "Tu «orden de llegada» se repite o retrocede: si usas el tamaño de la cola (o un contador que reinicias al atender) como marca, un paciente que llega más tarde puede quedar marcado como más antiguo. Usa un contador que solo crezca."},
           ["Antes de llegar Rita la cola tiene 1 paciente (Quique): si la marca es el tamaño de la cola, Rita recibe una marca menor que la de Quique.",
            "La marca de llegada tiene que ser estrictamente creciente durante todo el caso.",
            "Usa el índice del evento i (o un contador que solo se incrementa en cada I)."])
    prueba("Empates con llegadas intercaladas", "trampa",
           [[I("A1", 3), I("B1", 3), A, I("C1", 3), I("D1", 4), A, A, I("E1", 3), A, A],
            [I("x", 10), I("y", 20), I("z", 10), A, I("w", 20), A, A, A]],
           "Pacientes empatados que llegan entre atenciones: el orden de llegada se mantiene aunque se vayan atendiendo otros.",
           {"wa": "Con llegadas y atenciones intercaladas los empates salen mal: revisa que la marca de llegada es creciente y que el desempate la usa a favor del más antiguo."},
           ["En el primer caso la salida es A1, D1, B1, C1, E1: D1 se cuela por ser más grave, pero entre los de gravedad 3 se respeta la llegada.",
            "Cada paciente conserva su marca de llegada aunque se atienda a otros entre medias."])
    prueba("Gravedades extremas (0 y 1.000.000)", "borde",
           [[I("Hipocondriaco", 0), I("Casi", MAXG), I("Otro", 0), A, A, A],
            [I("Uno", MAXG), I("Dos", MAXG), A, A]],
           "Gravedad 0 (válida, no es un final) y gravedad 1.000.000.",
           {"wa": "La gravedad 0 es un paciente normal (no marca ningún final) y 1.000.000 cabe en int. Revisa también el desempate entre los dos de gravedad 0."},
           ["El paciente de gravedad 0 se atiende igual que los demás, el último.",
            "No uses la gravedad 0 como valor especial."])
    prueba("Nombres largos y repetidos", "trampa",
           [[I("A" * 20, 5), I("B" * 20, 6), I("A" * 20, 7), A, A, A],
            [I("Pepe", 1), I("Pepe", 2), I("Pepe", 1), A, A, A]],
           "Nombres de 20 caracteres y pacientes distintos con el mismo nombre (el enunciado no lo prohíbe).",
           {"wa": "Dos pacientes pueden llamarse igual: no los identifiques por el nombre (por ejemplo, con un map de nombre a gravedad). Cada ingreso es un paciente distinto.",
            "rte": "Con nombres de 20 caracteres se rompe algo: ¿guardas el nombre en un char[20] (falta sitio para el '\\0')? Usa string."},
           ["Guarda cada paciente completo (nombre, gravedad, llegada) en la cola, aunque el nombre se repita.",
            "Usa string para el nombre, no un array de tamaño fijo."])
    prueba("Atender justo después de llegar", "borde",
           [[I("a", 5), A, I("b", 1), A, I("c", 9), A, I("d", 0), A]],
           "Cada paciente se atiende nada más llegar: la cola tiene siempre 0 o 1 elementos.",
           {"wa": "Con la cola casi siempre vacía no debería haber problema: revisa que haces pop() tras escribir el nombre.",
            "rte": "Haces top()/pop() de más: cada A atiende exactamente a un paciente."},
           ["La salida es a, b, c, d.",
            "Cada A: escribe top().nombre y haz pop(), una sola vez."])
    prueba("Varios casos seguidos", "trampa",
           [[I("Ana", 5), I("Bea", 9), I("Carla", 1), A],
            [I("Dani", 3), A],
            [I("Eva", 2), I("Fran", 2), A, A],
            [I("Gema", 0), A]],
           "Varios casos en los que quedan pacientes sin atender: no pasan al caso siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: los pacientes que quedan sin atender (o el contador de llegada) se arrastran al caso siguiente. La cola debe ser local a resuelveCaso.",
            "rte": "Algo del caso anterior se queda a medias: declara la cola dentro de resuelveCaso."},
           ["Al acabar el primer caso quedan Ana y Carla sin atender: en el segundo caso no existen.",
            "Declara la priority_queue (y el contador de llegada) dentro de resuelveCaso."])
    nombres = [nombre_al_azar(r, 6) for _ in range(50)]
    prueba("Cincuenta pacientes empatados", "trampa",
           [[I(x, 42) for x in nombres] + [A] * 50],
           "50 pacientes con la misma gravedad: deben salir exactamente en su orden de llegada.",
           {"wa": "Con muchos empates la priority_queue los desordena si el comparador no desempata por llegada: no es estable, el orden de inserción no se conserva."},
           ["La salida debe ser la lista de nombres en el mismo orden de la entrada.",
            "El desempate tiene que estar dentro del comparador."])
    casos = [caso_al_azar(r, r.randint(1, 14), r.choice([3, 10, MAXG])) for _ in range(250)]
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "250 casos pequeños al azar con muchas gravedades repetidas.",
           {"wa": "Algún caso concreto falla: cuenta los «---» anteriores a la línea que falla para saber qué caso es, y simúlalo a mano."},
           ["Localiza el caso por el número de «---» anteriores.",
            "Apunta la cola tras cada evento con (gravedad, llegada) de cada paciente."])
    casos = [caso_al_azar(r, r.randint(500, 5000), r.choice([20, MAXG]), r.choice([0.3, 0.5])) for _ in range(15)]
    prueba("Aleatorios medianos", "aleatorio", casos,
           "15 casos de hasta 5000 eventos.",
           {"wa": "Con casos medianos aparece un fallo que en los pequeños no: revisa el desempate por orden de llegada.",
            "tle": "Ya con casos medianos va lento: ¿buscas al más grave recorriendo a todos?"},
           ["Comprueba que el orden de llegada es un contador creciente.",
            "Cada evento debe costar O(log n)."])
    llegan = [I(nombre_corto(k), r.randint(0, MAXG)) for k in range(100000)]
    prueba("Grande: 100.000 ingresos y luego 100.000 atenciones", "rendimiento",
           [llegan + [A] * 100000],
           "200.000 eventos con la cola llena: mide la eficiencia (O(n log n)).",
           {"tle": "Buscar al más grave recorriendo la lista en cada A (o insertar en un vector ordenado) cuesta O(n²): usa una priority_queue.",
            "mle": "Gastas demasiada memoria con 100.000 pacientes: guarda solo nombre, gravedad y llegada."},
           ["¿Cuánto cuesta cada A? Hay 100.000 con 100.000 pacientes esperando.",
            "priority_queue: push y pop en O(log n)."])
    ev = []
    for k in range(160000):
        ev.append(I(nombre_corto(k), r.randint(0, 3)) if k < 80000 or k % 2 == 0 else A)
    prueba("Grande: muchísimos empates", "rendimiento",
           [ev],
           "160.000 eventos con solo cuatro gravedades posibles: casi todo se decide por orden de llegada.",
           {"tle": "Con tantos empates tu solución se vuelve lenta: el desempate debe estar en el comparador (O(1)), no en una búsqueda aparte.",
            "wa": "Con muchísimos empates el orden de llegada se pierde: revisa el desempate."},
           ["El comparador debe decidir en O(1): gravedad y, si empata, llegada.",
            "No recorras la cola buscando al más antiguo."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida=texto_salida(c), casos=len(c),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


VARIANTES = [
    Variante("separador de cuatro guiones (formato de Acepta el Reto)", [('cout << "---\\n";', 'cout << "----\\n";')],
             prueba=2, v="wa"),
    Variante("procesa el caso n = 0", [("if(!(cin >> casos) || casos == 0) return false;", "if(!(cin >> casos)) return false;")],
             prueba=2, v="wa"),
    Variante("atiende al menos grave", [("return gravedad < o.gravedad;", "return gravedad > o.gravedad;")], prueba=3, v="wa"),
    Variante("empate al revés (el último en llegar primero)", [("return orden > o.orden;", "return orden < o.orden;")],
             prueba=4, v="wa"),
    Variante("sin desempate por llegada", [("return orden > o.orden;", "return false;")], prueba=[4, 7, 12], v="wa"),
    Variante("desempata por nombre", [("return orden > o.orden;", "return nombre > o.nombre;")], prueba=5, v="wa"),
    Variante("marca de llegada = tamaño de la cola",
             [("cola.push({ nombre, gravedad, i });", "cola.push({ nombre, gravedad, (int)cola.size() });")], prueba=6, v="wa"),
    Variante("cola global que no se vacía entre casos",
             [("bool resuelveCaso() {", "priority_queue<Paciente> cola;\nbool resuelveCaso() {"),
              ("    priority_queue<Paciente> cola;\n", "")], prueba=11, v="wa"),
    Variante("formato: separador pegado al último nombre", [('cout << "---\\n";', 'cout << "--- ";')], prueba=1, v="pe"),
    Variante("busca al más grave recorriendo un vector (O(n²))",
             [("    priority_queue<Paciente> cola;\n", "    vector<Paciente> cola;\n"),
              ("cola.push({ nombre, gravedad, i });", "cola.push_back({ nombre, gravedad, i });"),
              ("""                cout << cola.top().nombre << '\\n';
                cola.pop();""", """                int m = 0;
                for (int j = 1; j < (int)cola.size(); ++j) if (cola[m] < cola[j]) m = j;
                cout << cola[m].nombre << '\\n';
                cola.erase(cola.begin() + m);""")], prueba=15, v="tle"),
]
