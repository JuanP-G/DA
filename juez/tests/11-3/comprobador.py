"""Comprobador de 11-3 «La colecta de primavera»: vale CUALQUIER reparto óptimo.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/11-3.js en el navegador (el verificador comprueba que coinciden).
Por cada caso se espera: el beneficio máximo (un número) y una línea con V enteros entre 0 y 4 (las
cajas de cada vecino) que sumen como mucho C y den, con la tabla de precios de la entrada, ese beneficio.
"""
import re

_ENTERO = re.compile(r"-?[0-9]+")


def _lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def _casos(entrada):
    v = entrada.split()
    p = 0

    def sig():
        nonlocal p
        p += 1
        return int(v[p - 1])
    for _ in range(sig()):
        V, C = sig(), sig()
        pago = [[0] * V for _ in range(5)]
        for k in range(1, 5):
            for i in range(V):
                pago[k][i] = sig()
        yield V, C, pago


def _numeros(linea, cuantos):
    t = linea.split()
    if len(t) != cuantos or not all(_ENTERO.fullmatch(x) for x in t):
        return None
    return [int(x) for x in t]


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    ie = io = 0
    formato = None

    def fallo(motivo, esp):
        return {"linea": io + 1, "esperada": esp, "obtenida": o[io] if io < len(o) else None,
                "total": len(e), "lineas_tuyas": len(o), "motivo": motivo}

    for V, C, pago in _casos(entrada):
        mejor = int(e[ie])
        if io >= len(o):
            return fallo("tu salida acaba antes", e[ie])
        x = _numeros(o[io], 1)
        if x is None:
            return fallo("en esta línea va el beneficio máximo (un solo número)", e[ie])
        if x[0] != mejor:
            return fallo(f"el beneficio máximo es {mejor} y escribes {x[0]}", e[ie])
        if o[io] != str(x[0]) and formato is None:
            formato = fallo("el beneficio es correcto, pero la línea debe tener solo el número", e[ie])
        io += 1
        if io >= len(o):
            return fallo("tu salida acaba antes: falta la línea con las cajas de cada vecino", e[ie + 1])
        x = _numeros(o[io], V)
        if x is None:
            return fallo(f"en esta línea van {V} enteros: las cajas que se venden a cada vecino", e[ie + 1])
        if any(c < 0 or c > 4 for c in x):
            return fallo("a cada vecino se le venden entre 0 y 4 cajas", e[ie + 1])
        if sum(x) > C:
            return fallo(f"vendes {sum(x)} cajas y solo hay {C}", e[ie + 1])
        ganancia = sum(pago[c][i] for i, c in enumerate(x) if c)
        if ganancia != mejor:
            return fallo(f"con ese reparto se recaudan {ganancia} y el máximo es {mejor}", e[ie + 1])
        if o[io] != " ".join(str(c) for c in x) and formato is None:
            formato = fallo("el reparto es correcto, pero los números deben ir separados por un solo espacio", e[ie + 1])
        io += 1
        ie += 2
    if io < len(o):
        return fallo("escribes líneas de más", None)
    if formato is not None:
        formato["pe"] = True
    return formato


def _reparte(entrada, obtenida):
    """Las mismas palabras como las pide el enunciado (1 + V por caso), o None si no encajan."""
    tok = obtenida.split()
    k, out = 0, []
    for V, C, pago in _casos(entrada):
        if k + 1 + V > len(tok):
            return None
        out.append(tok[k])
        out.append(" ".join(tok[k + 1:k + 1 + V]))
        k += 1 + V
    return "\n".join(out) + "\n" if k == len(tok) else None


def comprobar(entrada, esperada, obtenida):
    d = _comprobar(entrada, esperada, obtenida)
    if d is None or d.get("pe"):
        return d
    r = _reparte(entrada, obtenida)
    if r is not None and _comprobar(entrada, esperada, r) is None:
        d = dict(d)
        d["pe"] = True
        d["motivo"] = "tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado"
    return d
