"""Vídeo de teoría · Tema 2 · Colas de prioridad y montículos (animado)."""
from vidlib import C, W, H, font
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo, arbol, arbol_anim

TEMA = "Tema 2 · Colas de prioridad"


def etq(e, p):
    return str(p)


def vector(f, arr, y=560, u=1.0, marca=None, base=1):
    """El montículo como array (posiciones desde 1)."""
    n = len(arr)
    x0 = 640 - n * 80 / 2
    for i, (e, p) in enumerate(arr):
        x = x0 + i * 80 + 40
        caja(f, x, y, p, c="gold" if marca and i in marca else "blue", u=u, w=70, h=54, tam=24, borde=4 if marca and i in marca else 2)
        texto(f, (x, y + 44), str(i + base), 16, "muted", u, anchor="mm")


def construye(vals):
    m = Monticulo(lambda a, b: a < b)
    for k, v in enumerate(vals):
        m.push(k, v)
    return m


BASE = [3, 5, 8, 9, 7, 10]


def e_portada(f):
    def dib(f):
        m = construye([1, 4, 2])
        arbol(f, m.copia(), 960, 270, 220, etq, u=f.p(0.3, 0.8), r=30)
    portada(f, "Teoría", "Colas de prioridad", TEMA, dib)


def e_tad(f):
    texto(f, (640, 70), "cola de prioridad: sale siempre el MÁS prioritario", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    ops = [("push(x)", "meter un elemento"), ("top()", "consultar el más prioritario"), ("pop()", "sacarlo"), ("empty(), size()", "")]
    for k, (o, d) in enumerate(ops):
        if f.t >= f.c(1):
            u = aparece(f, f.c(1) + 0.3 * k)
            texto(f, (380, 180 + 70 * k), o, 28, "blue", u, mono=True)
            texto(f, (680, 180 + 70 * k), d, 24, "text", u)
    if f.t >= f.c(2):
        etiqueta(f, (640, 540), "urgencias, cajas de súper, eventos en el tiempo, voraces…", 24, "text", aparece(f, f.c(2)))


def e_ingenuas(f):
    texto(f, (640, 70), "¿con qué se implementa?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    filas = [("vector desordenado", "push O(1)", "top / pop O(n)", "red"),
             ("vector ordenado", "push O(n)", "top / pop O(1)", "red"),
             ("montículo", "push O(log n)", "top O(1) · pop O(log n)", "green")]
    for k, (n, a, b, c) in enumerate(filas):
        if f.t >= f.c(k + 1):
            u = aparece(f, f.c(k + 1))
            y = 200 + 110 * k
            caja(f, 330, y, n, c=c, u=u, w=330, h=64, tam=24)
            texto(f, (560, y), a, 26, c, u, mono=True, anchor="lm")
            texto(f, (820, y), b, 26, c, u, mono=True, anchor="lm")


def e_monticulo(f):
    m = construye(BASE)
    arbol(f, m.copia(), 640, 150, 640, etq, u=aparece(f, f.c(0)), r=34, tam=22)
    texto(f, (640, 60), "montículo de mínimos", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 400), "árbol completo: todos los niveles llenos salvo el último, de izquierda a derecha", 22, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 460), "cada padre ≤ sus hijos  →  el mínimo está en la raíz", 22, "green", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        vector(f, m.copia(), 560, aparece(f, f.c(3)))
        etiqueta(f, (640, 670), "se guarda en un vector: hijos de i en 2i y 2i+1, padre en i/2", 22, "gold", aparece(f, f.c(3) + 0.3))


def e_push(f):
    m = construye(BASE)
    a = m.copia()
    m2 = construye(BASE)
    m2.a.append((99, 2))
    m2.pos[99] = len(m2.a) - 1
    b = m2.copia()             # 2 al final, sin flotar
    m2._flota(len(m2.a) - 1)
    c = m2.copia()             # ya flotado
    texto(f, (640, 60), "push(2): al final, y FLOTA mientras sea menor que su padre", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t < f.c(1):
        arbol(f, a, 640, 150, 640, etq, r=34, tam=22)
        vector(f, a)
    elif f.t < f.c(2):
        arbol_anim(f, a, b, f.lin(f.c(1), 0.8), 640, 150, 640, etq, r=34, tam=22, marca_elem=99)
        vector(f, b, marca={len(b) - 1})
    else:
        arbol_anim(f, b, c, f.lin(f.c(2), 2.0), 640, 150, 640, etq, r=34, tam=22, marca_elem=99)
        vector(f, c if f.t >= f.c(2) + 2.0 else b, marca={0} if f.t >= f.c(2) + 2.0 else {len(b) - 1})
    if f.t >= f.c(3):
        etiqueta(f, (640, 660), "sube como mucho la altura: O(log n)", 24, "green", aparece(f, f.c(3)))


def e_pop(f):
    m = construye(BASE)
    a = m.copia()
    m.pop()
    c = m.copia()
    # estado intermedio: el último en la raíz, sin hundir
    b = [a[-1]] + a[1:-1]
    texto(f, (640, 60), "pop(): el último pasa a la raíz y se HUNDE con su hijo menor", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t < f.c(1):
        arbol(f, a, 640, 150, 640, etq, r=34, tam=22, marca={0})
        vector(f, a, marca={0})
    elif f.t < f.c(2):
        arbol_anim(f, a[1:], b, f.lin(f.c(1), 0.8), 640, 150, 640, etq, r=34, tam=22, marca_elem=a[-1][0])
        vector(f, b, marca={0})
    else:
        arbol_anim(f, b, c, f.lin(f.c(2), 2.0), 640, 150, 640, etq, r=34, tam=22, marca_elem=a[-1][0])
        vector(f, c)
    if f.t >= f.c(3):
        etiqueta(f, (640, 660), "baja como mucho la altura: O(log n)", 24, "green", aparece(f, f.c(3)))


def e_heapsort(f):
    texto(f, (640, 70), "Dos usos más del montículo", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        caja(f, 640, 170, "heapify", c="blue", u=u, w=240, h=60, tam=26)
        texto(f, (640, 230), "vector → montículo, hundiendo desde la mitad hacia atrás: O(n)", 24, "text", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        caja(f, 640, 320, "heapsort", c="green", u=u, w=240, h=60, tam=26)
        texto(f, (640, 380), "heapify + sacar n veces la raíz al final: O(n log n), sin memoria extra", 24, "text", u, anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 480), "sacar k veces: los k menores en O(n + k log n)", 24, "muted", aparece(f, f.c(3)))


def e_stl(f):
    f.box(60, 110, 1160, 470, "std::priority_queue")
    lineas = [("priority_queue<int> q;", "de MÁXIMOS por defecto", "text"),
              ("priority_queue<int, vector<int>, greater<int>> q;", "de mínimos", "text"),
              ("priority_queue<pair<int,int>, …, greater<…>> q;", "pares: compara first y luego second", "text"),
              ("struct X { bool operator<(X const&) const; };", "el MAYOR sale primero", "gold")]
    for k, (c, d, col) in enumerate(lineas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (100, 180 + 100 * k), c, 22, "blue", u, mono=True, fondo=C["panel"])
            texto(f, (100, 214 + 100 * k), d, 20, col, u, fondo=C["panel"])
    if f.t >= f.c(4):
        etiqueta(f, (640, 640), "no deja cambiar la prioridad de un elemento: para eso, la IndexPQ (tema 3)", 22, "text", aparece(f, f.c(4)))


PATR = [("Simulación por eventos", "cajas, estaciones, envíos", "02-2 · 02-3 · 02-L", C["blue"]),
        ("Prioridad con desempate", "gravedad, coeficiente D'Hondt", "02-4 · 02-5", NARANJA),
        ("Voraz: siempre los menores", "sumar con mínimo esfuerzo", "02-1", C["green"]),
        ("Mezclar varias secuencias", "las cimas de varias pilas", "02-6", C["purple"])]


def e_patrones(f):
    texto(f, (640, 50), "Patrones de los ejercicios", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (t, d, e, c) in enumerate(PATR):
        if f.t < f.c(k + 1):
            continue
        u = aparece(f, f.c(k + 1))
        x = 40 + (k % 2) * 610
        y = 110 + (k // 2) * 250
        f.d.rounded_rectangle((x, y, x + 590, y + 220), 16, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        f.d.text((x + 24, y + 40), t, font=font(28, True), fill=mix(C["bot"], c, u), anchor="lm")
        f.d.text((x + 24, y + 110), d, font=font(24), fill=mix(C["bot"], C["text"], u), anchor="lm")
        f.d.text((x + 24, y + 170), e, font=font(22, True), fill=mix(C["bot"], C["muted"], u), anchor="lm")


def e_cierre(f):
    cierre(f, "Colas de prioridad", [
        "push, top y pop: sale siempre el más prioritario",
        "montículo: árbol completo guardado en un vector",
        "flotar al insertar, hundir al sacar: O(log n)",
        "priority_queue: máximos por defecto; greater para mínimos",
    ])


ESC = [
    Escena("Colas de prioridad y montículos: tener siempre a mano el elemento más importante.", e_portada, titulo="Portada", extra=1.0),
    Escena("Una cola de prioridad es una colección de la que siempre sale el elemento más prioritario. "
           "Tiene tres operaciones: push mete un elemento, top consulta el más prioritario y pop lo saca. "
           "Aparece en urgencias, en las cajas del súper, al simular eventos en el tiempo y en muchos algoritmos voraces.",
           e_tad, titulo="La cola de prioridad", extra=1.5),
    Escena("¿Cómo se implementa? "
           "Con un vector desordenado, meter es rápido pero buscar el mejor cuesta ene. "
           "Con un vector ordenado, al revés: meter cuesta ene. "
           "Con un montículo, todo cuesta como mucho un logaritmo.",
           e_ingenuas, titulo="Implementaciones", extra=1.5),
    Escena("Un montículo de mínimos es un árbol binario. "
           "Es completo: todos los niveles están llenos menos el último, que se rellena de izquierda a derecha. "
           "Y cada padre es menor o igual que sus hijos, así que el mínimo está en la raíz. "
           "Como es completo, se guarda en un vector: los hijos de la posición i están en dos i y dos i más uno, y el padre en i entre dos.",
           e_monticulo, titulo="El montículo", extra=1.5),
    Escena("Para insertar el dos, se pone al final del vector, en el primer hueco del último nivel. "
           "Queda debajo del ocho, que es mayor, así que no se cumple la propiedad. "
           "Flota: se intercambia con su padre mientras sea menor, y llega hasta la raíz. "
           "Como mucho sube la altura del árbol: logaritmo de ene.",
           e_push, titulo="push: flotar", extra=1.5),
    Escena("Para sacar el mínimo, la raíz, se pone en su lugar el último elemento. "
           "Ahora la raíz es el diez, que es mayor que sus hijos. "
           "Se hunde: se intercambia con el menor de sus hijos mientras haga falta. "
           "También cuesta logaritmo de ene.",
           e_pop, titulo="pop: hundir", extra=1.5),
    Escena("El montículo tiene dos usos más. "
           "Heapify convierte un vector cualquiera en montículo hundiendo los nodos desde la mitad hacia atrás, en tiempo lineal. "
           "Heapsort hace heapify y luego saca ene veces la raíz, dejando el vector ordenado sin memoria extra, en ene log ene. "
           "Y sacar ka veces da los ka menores.",
           e_heapsort, titulo="Heapify y heapsort", extra=1.5),
    Escena("En C más más usamos la priority queue de la librería, que por defecto es de máximos. "
           "Con greater se convierte en una de mínimos. "
           "Con pares, compara el primer campo y luego el segundo, lo que sirve para desempatar. "
           "Y con un struct propio, se define el operador menor, y sale primero el mayor. "
           "Lo que no permite es cambiar la prioridad de algo que ya está dentro: para eso está la IndexPQ del tema tres.",
           e_stl, titulo="priority_queue", extra=2.0),
    Escena("En los ejercicios salen cuatro patrones. "
           "Simular eventos en el tiempo, como cajas, estaciones o envíos. "
           "Prioridades con desempate, como la gravedad o el coeficiente de Hondt. "
           "Voraces que cogen siempre los menores, como sumar con mínimo esfuerzo. "
           "Y mezclar varias secuencias, como las cimas de las pilas de cómics.",
           e_patrones, titulo="Patrones", extra=2.0),
    Escena("Resumiendo: una cola de prioridad saca siempre el más prioritario; el montículo la implementa en un vector, flotando al insertar y hundiendo al sacar, en tiempo logarítmico.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-0", "../02-0_colas_de_prioridad_teoria.mp4", "02-0")
