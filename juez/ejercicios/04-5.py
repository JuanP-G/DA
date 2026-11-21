"""04-5 · ¡Las noticias vuelan!: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso «N M» (1 ≤ N, M ≤ 100.000) y M grupos, cada uno «k u1 ... uk»
(0 ≤ k ≤ N, usuarios distintos de 1 a N). La suma de N y la de los tamaños de grupo de todos los
casos no pasan de 1.000.000. Salida: por caso, una línea con N números: el i-ésimo es cuántos
usuarios acaban sabiendo la noticia si empieza el usuario i (el tamaño de su componente conexa).
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-5/EJ_04-5.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-5/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["for (int j = 1; j < k; ++j) {", "for (int j = 2; j < k; ++j) {"],
}


# ---------------------------------------------------------------- solucionador independiente
def respuestas(N, grupos):
    """Conjuntos disjuntos por tamaño (sin construir ningún grafo)."""
    padre = list(range(N + 1))
    tam = [1] * (N + 1)

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for g in grupos:
        for u in g[1:]:
            a, b = raiz(g[0]), raiz(u)
            if a != b:
                if tam[a] < tam[b]:
                    a, b = b, a
                padre[b] = a
                tam[a] += tam[b]
    return [tam[raiz(i)] for i in range(1, N + 1)]


def caso_a_texto(caso):
    N, grupos = caso
    return f"{N} {len(grupos)}\n" + "".join(" ".join(map(str, [len(g)] + list(g))) + "\n" for g in grupos)


# ---------------------------------------------------------------- generadores
def aleatorio_pequeno(rng):
    N = rng.randint(1, 10)
    grupos = []
    for _ in range(rng.randint(1, 6)):
        k = rng.choice([0, 1, 1, 2, 2, 3, 4, N])
        grupos.append(rng.sample(range(1, N + 1), min(k, N)))
    return (N, grupos)


def pruebas():
    rng = random.Random(45)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(7, [[2, 5, 4], [], [1, 2], [1], [6, 7]]), (4, [[1], [3]])],
           "Los dos casos del PDF: grupos que se solapan, un grupo vacío, grupos de un solo usuario y un usuario sin grupo.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: que los usuarios van de 1 a N, que los grupos vacíos («0») no tienen ningún número detrás y que la respuesta es el tamaño de toda la componente.",
            "pe": "Los números están bien pero el formato no: los N números de cada caso van en una sola línea, separados por espacios."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "El usuario 5 no comparte grupo con el 1, pero la noticia le llega a través del 2: su respuesta es 4.",
            "La respuesta de i es el tamaño de la componente conexa de i en el grafo «comparten algún grupo»."])
    prueba("Un solo usuario", "borde", [(1, [[1], []])],
           "N = 1: la noticia solo la conoce él (1).",
           {"wa": "Con un solo usuario la respuesta es 1: quien empieza la noticia también la conoce."},
           ["¿Qué escribe tu programa con un único usuario?",
            "Cuenta también al usuario que empieza la noticia."])
    prueba("Todos los grupos vacíos", "borde", [(5, [[], [], []])],
           "Tres grupos vacíos: nadie es amigo de nadie (1 1 1 1 1).",
           {"wa": "Un grupo vacío no conecta a nadie: cada usuario se queda con la noticia (1)."},
           ["Con grupos «0», ¿lees algún número de más?",
            "Si k = 0, no hay ningún usuario que leer en esa línea."])
    prueba("Todos en el mismo grupo", "borde", [(6, [[3, 1, 6, 2, 5, 4]])],
           "Un grupo con los N usuarios: todas las respuestas son N.",
           {"wa": "Si todos están en el mismo grupo, todos son amigos de todos: la noticia llega a los 6."},
           ["Todas las respuestas deben ser 6.",
            "Basta unir a cada usuario del grupo con el primero: así quedan todos en la misma componente."])
    prueba("Un grupo vacío entre otros", "trampa", [(3, [[], [1, 3]])],
           "Un grupo vacío seguido de otro: el «0» no va seguido de ningún usuario.",
           {"wa": "Con k = 0 lees un usuario que no existe (el número de la línea siguiente) y todo se descoloca. Si el grupo está vacío no hay nada más que leer."},
           ["Las respuestas son «2 1 2»: el grupo {1, 3} junta a 1 y 3.",
            "¿Lees el primer usuario del grupo antes de comprobar que k > 0?",
            "Pon la lectura del primer usuario dentro de un if (k > 0)."])
    prueba("La noticia salta de grupo en grupo", "trampa", [(4, [[1, 2], [2, 3], [3, 4]])],
           "Grupos {1, 2}, {2, 3} y {3, 4}: la noticia que empieza en 1 llega a los cuatro.",
           {"wa": "No basta con contar a los compañeros de grupo: los amigos de tus amigos también se enteran. La respuesta es el tamaño de toda la componente conexa."},
           ["1 y 4 no comparten ningún grupo, pero la noticia pasa por 2 y 3.",
            "La respuesta de i no es «1 + compañeros de sus grupos», sino cuántos usuarios alcanza un recorrido desde i.",
            "Construye el grafo, recorre cada componente una vez y guarda su tamaño."])
    prueba("Dos grupos con los mismos usuarios", "trampa", [(3, [[1, 2, 3], [3, 2, 1]])],
           "Los mismos tres usuarios en dos grupos: siguen siendo 3, no 5.",
           {"wa": "Un usuario que está con otro en dos grupos no cuenta doble. Cuenta usuarios distintos alcanzados, no suma tamaños de grupos."},
           ["Las respuestas son «3 3 3».",
            "Marca a cada usuario al visitarlo y cuéntalo una sola vez."])
    prueba("Grupos de un solo usuario", "trampa", [(3, [[2], [1], [3], [2]])],
           "Grupos con un único miembro: no ponen a nadie en contacto (1 1 1).",
           {"wa": "Un grupo de un solo usuario no crea ninguna amistad. Revisa el bucle que une a los miembros (empieza en el segundo).",
            "rte": "Con k = 1 no hay segundo usuario: revisa los índices del bucle del grupo."},
           ["Todas las respuestas son 1.",
            "Une el primero con los usuarios 2.º, 3.º... del grupo: con k = 1 no hay ninguna arista."])
    prueba("El usuario N también cuenta", "trampa", [(3, [[3, 1]])],
           "Los usuarios van de 1 a N y el usuario N aparece en un grupo.",
           {"rte": "Los usuarios van de 1 a N: con un grafo de N vértices hay que restar 1 al leerlos (el N sería el vértice N, que no existe)."},
           ["El usuario 3 existe cuando N = 3.",
            "Resta 1 a cada usuario al poner las aristas (o crea N + 1 vértices y no uses el 0)."])
    prueba("Usuarios sin grupo intercalados", "trampa", [(8, [[2, 7], [7, 4], [], [8, 6]])],
           "Los usuarios 1, 3 y 5 no están en ningún grupo; los demás forman {2, 4, 7} y {6, 8}.",
           {"wa": "Un usuario que no aparece en ningún grupo tiene respuesta 1, y hay que escribirla en su sitio: N números, en orden de usuario."},
           ["La respuesta es «1 3 1 3 1 2 3 2».",
            "Escribe una respuesta para cada usuario de 1 a N, aparezca o no en algún grupo."])
    prueba("Grupos que se unen al final", "trampa", [(5, [[1, 2], [3, 4], [5], [2, 3]])],
           "{1, 2} y {3, 4} quedan unidos por el último grupo {2, 3}.",
           {"wa": "Si das una etiqueta de grupo a cada usuario según lees, un grupo que une dos componentes ya formadas obliga a fusionarlas. Es más sencillo construir el grafo y recorrerlo al final."},
           ["Las respuestas son «4 4 4 4 1».",
            "Construye primero el grafo con todos los grupos y recorre las componentes después de leerlo todo."])
    prueba("Varios casos seguidos", "trampa",
           [(6, [[6, 1, 2, 3, 4, 5, 6]]), (5, [[1, 2]]), (3, [[]]), (2, [[2, 1]])],
           "Un caso con todos juntos seguido de otros más pequeños: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: las componentes, sus tamaños o el grafo están declarados fuera de la función de cada caso (o son static)."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo y los vectores de componentes y tamaños dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(60)],
           "60 casos pequeños al azar, con grupos vacíos, de uno y de todos.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja sus grupos."},
           ["Busca el caso de la línea que falla y dibuja quién comparte grupo con quién.",
            "Calcula a mano las componentes y comprueba tu salida usuario a usuario."])
    # ---- grandes
    N = 100000
    todos = list(range(1, N + 1))
    rng.shuffle(todos)
    prueba("Un grupo con todos los usuarios", "rendimiento", [(N, [todos])],
           "Un grupo de 100.000 usuarios: unir cada par serían 5.000 millones de aristas.",
           {"mle": "Unir todos los pares de un grupo de k usuarios son k·(k − 1)/2 aristas. Basta unir a todos con el primero (k − 1 aristas).",
            "tle": "O unes todos los pares del grupo o haces un recorrido por usuario: las dos cosas son cuadráticas."},
           ["¿Cuántas aristas pones para un grupo de k usuarios?",
            "Solo importa quién está conectado con quién: une a cada usuario del grupo con el primero.",
            "Y recorre cada componente una vez, guardando su tamaño, en lugar de un recorrido por usuario."])
    sueltos = [[u] for u in range(1, N + 1, 2)] + [[] for _ in range(N // 2)]
    prueba("100.000 usuarios sueltos", "rendimiento", [(N, sueltos)],
           "100.000 usuarios sin amigos: 100.000 componentes de tamaño 1.",
           {"tle": "Algo cuesta O(N) por cada componente o por cada usuario: un recorrido completo por usuario, reiniciar un vector entero o copiar el grafo al empezar cada componente.",
            "mle": "Revisa que no copias el grafo al llamar a la función de recorrido."},
           ["Con 100.000 componentes, lo que hagas al empezar cada una debe costar O(1) más su tamaño.",
            "Pasa el grafo por referencia (Grafo const&) a la función de recorrido.",
            "Haz un único recorrido por componente y guarda en comp[v] su número y en tam[c] su tamaño."])
    cadena = [[todos[i], todos[i + 1]] for i in range(N - 1)]
    prueba("Cadena de 100.000 usuarios", "rendimiento", [(N, cadena)],
           "99.999 grupos de dos encadenados: una única componente muy «larga».",
           {"tle": "Algo se repite de más: ¿un recorrido por usuario?",
            "rte": "Si usas un DFS recursivo, la cadena tiene 100.000 niveles. En el juez hay pila de sobra, pero en tu ordenador puede desbordarse: un BFS con cola lo evita."},
           ["Un solo recorrido para toda la componente basta.",
            "Para contar una componente da igual el orden: un BFS con cola no tiene problemas de pila."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(" ".join(map(str, respuestas(*c))) + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("un número por línea", [("cout << tc.tamano(v) << ' ';", "cout << tc.tamano(v) << '\\n';")], prueba=1, v="pe"),
    Variante("lee un usuario aunque el grupo esté vacío", [("if (k != 0) {", "{")], prueba=5, v="wa"),
    Variante("cuenta solo a los compañeros de grupo",
             [("Grafo g(usuarios);", "Grafo g(usuarios); vector<int> amigos(usuarios, 0);"),
              ("int primero; cin >> primero;", "int primero; cin >> primero; amigos[primero - 1] += k - 1;"),
              ("g.ponArista(primero - 1, otro - 1);", "g.ponArista(primero - 1, otro - 1); amigos[otro - 1] += k - 1;"),
              ("cout << tc.tamano(v) << ' ';", "cout << 1 + amigos[v] << ' ';")], prueba=6, v="wa"),
    Variante("no resta 1 a los usuarios", [("g.ponArista(primero - 1, otro - 1);", "g.ponArista(primero, otro);")], prueba=9, v="rte"),
    Variante("componentes calculadas solo en el primer caso", [("TamComponentes tc(g);", "static TamComponentes tc(g);")], prueba=12, v="wa"),
    Variante("une todos los pares de cada grupo",
             [("int primero; cin >> primero;", "int primero; cin >> primero; vector<int> miembros{primero};"),
              ("g.ponArista(primero - 1, otro - 1);", "for (int x : miembros) g.ponArista(x - 1, otro - 1); miembros.push_back(otro);")], prueba=14, v="mle"),
    Variante("un recorrido por usuario",
             [("    TamComponentes tc(g);\n    for (int v = 0; v < usuarios; ++v)\n        cout << tc.tamano(v) << ' ';",
               "    for (int v = 0; v < usuarios; ++v) { TamComponentes tc(g); cout << tc.tamano(v) << ' '; }")], prueba=[14, 15, 16], v="tle"),
    Variante("copia el grafo en cada recorrido", [("int bfs(Grafo const& g, int origen, int c) {", "int bfs(Grafo g, int origen, int c) {")], prueba=15, v="tle"),
]
