"""11-2 · Aibofobia: juez con pruebas pensadas para cada error típico.

El enunciado admite CUALQUIER palíndromo con el mínimo de letras añadidas: el comprobador
(juez/ejercicios/comprobadores/11-2.py y .js) mira que el número sea el mínimo y que la palabra
escrita sea un palíndromo de minúsculas con n + k letras que contenga la palabra dada como
subsecuencia (es decir, que se obtenga AÑADIENDO letras). ALTERNATIVA da otro palíndromo válido
(desempata hacia el otro extremo) y el verificador comprueba que se acepta.

El solucionador es propio: subsecuencia palindrómica más larga lps(i, j) (letras que se quedan)
y reconstrucción desde ella; faltan = n − lps. Validado contra fuerza bruta en miles de palabras.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-2/EJ_11-2.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["reverse(der.begin(), der.end());", ";"],
}


def resuelve(s, derecha_en_empate=False):
    """(letras añadidas, palíndromo)."""
    n = len(s)
    # lps[i][j] = longitud de la subsecuencia palindrómica más larga de s[i..j]
    lps = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        fila, sig = lps[i], lps[i + 1] if i + 1 < n else None
        fila[i] = 1
        si = s[i]
        for j in range(i + 1, n):
            if si == s[j]:
                fila[j] = (sig[j - 1] if j - 1 >= i + 1 else 0) + 2
            else:
                a, b = sig[j], fila[j - 1]
                fila[j] = a if a > b else b
    izq, der = [], []
    i, j = 0, n - 1

    def L(a, b):
        return lps[a][b] if a <= b else 0
    while i <= j:
        if i == j:
            izq.append(s[i])
            break
        if s[i] == s[j]:
            izq.append(s[i]); der.append(s[i]); i += 1; j -= 1
        else:
            quita_i, quita_j = L(i + 1, j), L(i, j - 1)
            if quita_i > quita_j or (quita_i == quita_j and not derecha_en_empate):
                izq.append(s[i]); der.append(s[i]); i += 1
            else:
                izq.append(s[j]); der.append(s[j]); j -= 1
    pal = "".join(izq) + "".join(reversed(der))
    return len(pal) - n, pal


def linea(s, alt=False):
    k, pal = resuelve(s, alt)
    return f"{k} {pal}\n"


def palabra(rng, n, letras="abcdefghijklmnopqrstuvwxyz"):
    return "".join(rng.choice(letras) for _ in range(n))


def pruebas():
    rng = random.Random(1102)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(c + "\n" for c in casos),
                        salida="".join(linea(c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    VARIOS = "Vale cualquier palíndromo con el mínimo de letras añadidas."
    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado (roda)", "enunciado", ["roda"],
           "roda: cuatro letras distintas, hay que añadir 3 (adoroda, rodador...). " + VARIOS,
           {"wa": "Falla el primer ejemplo: revisa la recurrencia faltan(i, j) y que escribes el número, un espacio y el palíndromo.",
            "pe": "Los datos están bien pero no el formato: el número y el palíndromo van en la MISMA línea, separados por un espacio."},
           ["Con cuatro letras distintas solo una puede quedarse sola en el centro.",
            "faltan(i, j) = faltan(i+1, j−1) si s[i] = s[j]; si no, 1 + min(faltan(i+1, j), faltan(i, j−1)).",
            "Escribe «3 adoroda» (o cualquier otro palíndromo de 7 letras que contenga roda)."])
    prueba("Ejemplo 2 del enunciado (amad)", "enunciado", ["amad"],
           "amad: basta con una d al principio (damad).",
           {"wa": "Sale más de 1: en «amad» hay que emparejar la d (añadiéndola al principio) y aprovechar que «ama» ya es palíndromo."},
           ["¿Qué queda si emparejas la d del final con una d nueva al principio?",
            "Cuando los extremos son distintos hay que probar las DOS opciones y quedarse con la mejor."])
    prueba("Ejemplo 3 del enunciado (reconor)", "enunciado", ["reconor"],
           "reconor: hay que insertar dos letras EN MEDIO (reconocer), no solo por los extremos.",
           {"wa": "Las letras se pueden añadir en cualquier posición: si solo añades por un extremo (o buscas el palíndromo contiguo más largo) no sale 2."},
           ["r, o, n, o, r ya forman un palíndromo aunque no sean letras seguidas.",
            "Es la subsecuencia palindrómica más larga, no la subcadena: faltan = n − (letras que se quedan)."])
    prueba("Ejemplo 4 del enunciado (reconocer)", "enunciado", ["reconocer"],
           "reconocer ya es un palíndromo: se escribe «0 reconocer».",
           {"wa": "Si la palabra ya es un palíndromo no se añade nada: «0» y la propia palabra."},
           ["¿Qué vale faltan(i, j) cuando s[i] = s[j] en todos los pasos?",
            "Con extremos iguales se emparejan entre sí y no se añade ninguna letra."])

    # ------------------------------------------------------------------ trampas
    prueba("Formato: número y palíndromo en la misma línea", "trampa", ["aa", "xxxx"],
           "Dos palabras que ya son palíndromos: «0 aa» y «0 xxxx».",
           {"wa": "Mira el «Por qué»: hay que escribir el número de letras añadidas, un espacio y el palíndromo, todo en una línea por palabra.",
            "pe": "El número y el palíndromo van en la misma línea, separados por un solo espacio."},
           ["La salida de «aa» es exactamente «0 aa».",
            "Escribe primero el número, luego un espacio y luego el palíndromo, y un salto de línea."])
    prueba("Una sola letra", "trampa", ["a"],
           "Una palabra de una letra ya es un palíndromo: «0 a».",
           {"wa": "Escribes la letra del centro dos veces: cuando i = j, esa letra va UNA sola vez (en la mitad izquierda o en el centro).",
            "rte": "Con una sola letra te sales de la tabla: el caso base es faltan(i, j) = 0 si i ≥ j; no mires faltan(i+1, j−1) con j < i+1."},
           ["¿Qué escribe tu programa para «a»?",
            "En la reconstrucción, si i == j la letra se pone una sola vez y se termina."])
    prueba("Ya es un palíndromo impar", "trampa", ["aba", "aabaa", "xyx"],
           "Palabras que ya son palíndromos de longitud impar: no se añade nada.",
           {"wa": "Añades letras a algo que ya es palíndromo: si s[i] = s[j], faltan(i, j) = faltan(i+1, j−1) (las dos letras se emparejan entre sí)."},
           ["En «aba» la a del principio y la del final se emparejan entre sí.",
            "Revisa el caso s[i] = s[j]: el intervalo que queda es (i+1, j−1), no (i+1, j)."])
    prueba("Dos letras distintas", "trampa", ["ab"],
           "«ab»: hay que añadir 1 letra (aba o bab).",
           {"wa": "Con dos letras distintas basta con añadir una: faltan(i, j) = 1 + min(...), no 2 + min(...). Cada letra sin pareja necesita UNA copia."},
           ["Añadiendo una a al final de «ab» sale «aba».",
            "Si los extremos son distintos, se añade UNA copia de uno de ellos: 1 + min(faltan(i+1, j), faltan(i, j−1))."])
    prueba("La mitad derecha va al revés", "trampa", ["abc"],
           "«abc»: se añaden 2 letras (abcba, cbabc...).",
           {"wa": "Tu palabra no es un palíndromo: si construyes la mitad derecha de fuera hacia dentro, al final hay que darle la vuelta."},
           ["Escribe a mano tus dos mitades para «abc»: ¿en qué orden quedan las letras de la derecha?",
            "La mitad derecha se va construyendo desde el final de la palabra: hay que invertirla antes de juntarla con la izquierda."])
    prueba("Elegir el extremo que menos letras necesita", "trampa", ["aab"],
           "«aab»: lo mejor es emparejar la b (baab), con una sola letra.",
           {"wa": "Tu palabra tiene letras de más: al reconstruir, cuando los extremos son distintos hay que seguir por el lado con MENOS letras que añadir (el que dio el mínimo en la tabla)."},
           ["¿Cuántas letras faltan para «ab» y cuántas para «aa»?",
            "Si faltan(i+1, j) ≤ faltan(i, j−1), empareja s[i]; si no, empareja s[j]."])
    prueba("Subsecuencia, no subcadena", "trampa", ["abca", "abcda"],
           "En «abca» las dos a se emparejan aunque no estén juntas: basta con 1 letra (abcba).",
           {"wa": "Sale más de lo debido: las letras que se quedan no tienen por qué ser contiguas (es la subsecuencia palindrómica más larga, no la subcadena)."},
           ["En «abca» se aprovechan las dos a de los extremos.",
            "Usa la recurrencia por intervalos: si s[i] = s[j], se emparejan y queda (i+1, j−1)."])
    prueba("Todas las letras distintas", "trampa", ["abcdefghijklmnopqrstuvwxyz"],
           "Las 26 letras distintas: hay que añadir 25.",
           {"wa": "Con todas las letras distintas solo una se queda sin copia: n − 1 letras añadidas."},
           ["¿Cuántas letras pueden quedarse sin pareja en un palíndromo?",
            "Comprueba que tu palíndromo tiene 51 letras y contiene la palabra."])
    prueba("Letras iguales separadas", "trampa", ["abab", "baab", "abcab"],
           "Palabras en las que hay que decidir qué letras iguales se emparejan.",
           {"wa": "Algún palíndromo no es mínimo o no contiene la palabra: revisa la recurrencia y que la reconstrucción sigue las decisiones de la tabla."},
           ["En «abab» basta con una letra: «ababa» o «babab».",
            "La reconstrucción debe seguir exactamente las decisiones que dan el mínimo de la tabla."])
    casos = ["abcdefghij", "a", "racecar", "ab", "aab", "zz", "xyz", "abcba", "q", "roda"]
    prueba("Varios casos seguidos", "trampa", casos,
           "Una palabra larga seguida de otras cortas: nada de una palabra debe pasar a la siguiente.",
           {"wa": "La primera palabra sale bien y las siguientes no: algo no se reinicia (las mitades del palíndromo o la tabla).",
            "rte": "Una tabla del caso anterior con otro tamaño: créala dentro de cada caso con el tamaño de la palabra."},
           ["¿Vacías las cadenas de las dos mitades antes de cada palabra?",
            "Declara la tabla y las cadenas dentro de resuelveCaso."])

    prueba("Palabras de una y dos letras", "borde", ["z", "zz", "zy", "yz"],
           "Las palabras más cortas posibles: «0 z», «0 zz» y dos de dos letras distintas que necesitan una más.",
           {"wa": "Falla con palabras mínimas: revisa el caso base (faltan = 0 si i ≥ j) y la letra del centro, que va una sola vez.",
            "rte": "Con una o dos letras te sales de la tabla: no mires faltan(i+1, j−1) cuando j − i < 2."},
           ["Prueba tu programa con «z» y con «zy».",
            "Con dos letras iguales faltan 0; con dos distintas, 1."])

    # ------------------------------------------------------------------ aleatorios
    casos = [palabra(rng, rng.randint(1, 10), rng.choice(["ab", "abc", "abcdefghijklmnopqrstuvwxyz"])) for _ in range(300)]
    prueba("Palabras cortas al azar", "aleatorio", casos,
           "300 palabras de hasta 10 letras, muchas con pocas letras distintas (muchas soluciones). " + VARIOS,
           {"wa": "Alguna palabra falla: busca cuál es en la entrada y resuélvela a mano (son cortas)."},
           ["El «Por qué» te dice si el número no es el mínimo o si la palabra no es un palíndromo que contenga la dada.",
            "Comprueba el orden de cálculo de la tabla: faltan(i, j) necesita intervalos MÁS CORTOS ya calculados."])
    casos = [palabra(rng, rng.randint(11, 18), rng.choice(["ab", "abcd", "abcdefghijklmnopqrstuvwxyz"])) for _ in range(60)]
    prueba("Palabras medianas al azar", "aleatorio", casos,
           "60 palabras de 11 a 18 letras.",
           {"wa": "Alguna palabra mediana falla: revisa el orden de cálculo (por longitudes crecientes) y la reconstrucción."},
           ["Si las cortas salen bien y estas no, mira los índices de la tabla.",
            "Rellena por d = j − i creciente: d = 1, 2, …, n − 1."])

    # ------------------------------------------------------------------ rendimiento
    prueba("Palabra de 1.000 letras", "rendimiento", [palabra(rng, 1000)],
           "Una palabra del tamaño máximo con letras al azar.",
           {"tle": "Recursión sin memoria (exponencial): guarda faltan(i, j) en una tabla n × n.",
            "mle": "¿Guardas un palíndromo (string) en cada casilla de la tabla? Guarda solo números y reconstruye al final.",
            "rte": "Con 1.000 letras se rompe: revisa el tamaño de la tabla (n × n) y los índices."},
           ["¿Cuántas veces calculas el mismo faltan(i, j)?",
            "Una tabla de enteros n × n (10⁶ casillas) rellena por longitudes crecientes: O(n²)."])
    casos = [palabra(rng, 1000, rng.choice(["ab", "abcdefghijklmnopqrstuvwxyz"])) for _ in range(15)] + ["a" * 1000]
    prueba("16 palabras de 1.000 letras", "rendimiento", casos,
           "Muchas palabras del tamaño máximo (incluida una de mil «a»): mide el coste O(n²) por palabra.",
           {"tle": "Debe costar O(n²) por palabra. ¿Concatenas strings en cada casilla, usas map en vez de una tabla o pasas la palabra por valor en una recursión?",
            "mle": "No guardes strings en la tabla: solo números, y reconstruye el palíndromo al final."},
           ["10⁶ casillas por palabra son pocas; si tarda, algo repite trabajo o copia strings.",
            "Reconstruye el palíndromo una sola vez, recorriendo la tabla desde (0, n − 1)."])
    return P


RECURSIVA = """int f(string const& s, int i, int j) {
    if (i >= j) return 0;
    if (s[i] == s[j]) return f(s, i + 1, j - 1);
    return 1 + min(f(s, i + 1, j), f(s, i, j - 1));
}

void resuelveCaso() {"""

VARIANTES = [
    Variante("número y palíndromo en líneas distintas", [("cout << faltan[0][n - 1] << ' ' << izq + der", "cout << faltan[0][n - 1] << '\\n' << izq + der")], prueba=1, v="pe"),
    Variante("solo escribe el número", [("cout << faltan[0][n - 1] << ' ' << izq + der << '\\n';", "cout << faltan[0][n - 1] << '\\n';")], prueba=5, v="wa"),
    Variante("la letra del centro dos veces", [("if (i == j) { izq += s[i]; ++i; }", "if (i == j) { izq += s[i]; der += s[i]; ++i; }")], prueba=6, v="wa"),
    Variante("extremos iguales: (i+1, j)", [("faltan[i][j] = (d >= 2) ? faltan[i + 1][j - 1] : 0;", "faltan[i][j] = (d >= 2) ? faltan[i + 1][j] : 0;")], prueba=7, v="wa"),
    Variante("cuenta 2 letras por cada extremo distinto", [("else faltan[i][j] = 1 + min(", "else faltan[i][j] = 2 + min(")], prueba=8, v="wa"),
    Variante("no da la vuelta a la mitad derecha", [("reverse(der.begin(), der.end());", "")], prueba=9, v="wa"),
    Variante("sigue el extremo peor al reconstruir", [("else if (faltan[i + 1][j] <= faltan[i][j - 1])", "else if (faltan[i + 1][j] > faltan[i][j - 1])")], prueba=10, v="wa"),
    Variante("rellena la tabla por filas (i creciente)",
             [("for (int d = 1; d < n; ++d) {              // d = j - i\n        for (int i = 0; i + d < n; ++i) {\n            int j = i + d;",
               "for (int i = 0; i < n; ++i) {\n        for (int j = i + 1; j < n; ++j) {\n            int d = j - i;")],
             prueba=[9, 10, 11, 12, 13], v="wa"),
    Variante("mitades sin vaciar entre casos", [("string izq, der;", "static string izq, der;")], prueba=14, v="wa"),
    Variante("recursión sin memoria",
             [("void resuelveCaso() {", RECURSIVA),
              ("            if (s[i] == s[j]) faltan[i][j] = (d >= 2) ? faltan[i + 1][j - 1] : 0;\n            else faltan[i][j] = 1 + min(faltan[i + 1][j], faltan[i][j - 1]);",
               "            faltan[i][j] = f(s, i, j);")],
             prueba=[18, 19], v="tle"),
]


# ---------------------------------------------------------------- respuesta alternativa
def ALTERNATIVA(entrada):
    """Otro palíndromo válido: en caso de empate se empareja el extremo derecho."""
    t = entrada.split()
    return "".join(linea(s, True) for s in t[1:1 + int(t[0])])
