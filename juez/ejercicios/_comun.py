"""Utilidades comunes de los generadores de pruebas del juez (juez/ejercicios/<id>.py).

Cada ejercicio es un módulo con:

    CONFIG = {
        "solucion": "4-Grafos no dirigidos/EJ_04-3/EJ_04-3.cpp",   # ruta desde la raíz del repo
        "cabeceras": ["4-Grafos no dirigidos/EJ_04-3/Grafo.h"],      # se copian junto al código
        "limite_ms": 3000,                                           # CPU por prueba (ver LEEME)
        "fallo": ["texto de la solución", "texto con un fallo"],     # demo «con un fallo» de la web
    }

    def pruebas():            # lista de Prueba(...) en orden: de lo más simple a lo más grande
        ...

    VARIANTES = [             # soluciones con fallos típicos: el verificador comprueba que se detectan
        Variante("nombre", [("texto original", "texto con el fallo"), ...], prueba=9, v="wa"),
        ...
    ]

La salida esperada de cada prueba la calcula un solucionador INDEPENDIENTE escrito en el módulo
(en Python, sin mirar la solución del repo). Así, si la solución del repo pasa todas las pruebas,
las dos implementaciones coinciden en todo.
"""
import random

TIPOS = ("enunciado", "borde", "trampa", "aleatorio", "rendimiento")
VEREDICTOS = ("wa", "pe", "tle", "mle", "rte", "ole")


class Prueba(dict):
    """Una prueba = un fichero .in/.out.

    nombre     corto y concreto («Final de una fila y principio de la siguiente»)
    tipo       enunciado | borde | trampa | aleatorio | rendimiento
    entrada    texto completo de la entrada (con el número de casos, centinela... si lo hay)
    salida     texto esperado (lo calcula el solucionador independiente)
    casos      cuántos casos hay en la entrada (1 si el formato no tiene casos)
    comprueba  qué mira esta prueba, en una frase, para el alumno
    si         {veredicto: qué suele significar fallarla así}; al menos el más probable
    pistas     de menos a más directa (2-4); la última casi dice cómo arreglarlo
    """

    def __init__(self, nombre, tipo, entrada, salida, casos, comprueba, si, pistas):
        assert tipo in TIPOS, tipo
        assert isinstance(si, dict) and si and all(k in VEREDICTOS for k in si), si
        assert pistas and all(isinstance(p, str) and p for p in pistas), pistas
        assert entrada.endswith("\n") and salida.endswith("\n") or salida == "", nombre
        super().__init__(nombre=nombre, tipo=tipo, entrada=entrada, salida=salida, casos=casos,
                         comprueba=comprueba, si=si, pistas=list(pistas))


class Variante(dict):
    """Solución con un fallo típico, para comprobar que el juez lo detecta y lo explica bien.

    cambios  [(texto que existe en la solución, texto que lo sustituye), ...]
    prueba   número de prueba (o lista de números válidos) que la guía debe señalar
    v        veredicto que debe tener esa prueba (wa, pe, tle, mle, rte, ole)
    """

    def __init__(self, nombre, cambios, prueba, v):
        assert v in VEREDICTOS, v
        super().__init__(nombre=nombre, cambios=[list(c) for c in cambios],
                         prueba=prueba if isinstance(prueba, list) else [prueba], v=v)


def rng(semilla):
    """Generador aleatorio con semilla fija: las pruebas salen siempre iguales."""
    return random.Random(semilla)


def lineas(*filas):
    """Une filas (cada una lista de valores o texto) en un texto con salto de línea final."""
    out = []
    for f in filas:
        out.append(" ".join(map(str, f)) if isinstance(f, (list, tuple)) else str(f))
    return "\n".join(out) + "\n"
