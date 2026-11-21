"""Comprobador de 05-3 «Ordenando tareas»: vale CUALQUIER orden que respete las dependencias.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/05-3.js en el navegador (el verificador comprueba que coinciden).
"""


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
        n, m = sig(), sig()
        yield n, [(sig(), sig()) for _ in range(m)]


def _revisa(n, deps, linea):
    """Motivo por el que «linea» no es un orden válido de las tareas 1..n, o None."""
    t = linea.split()
    if t == ["Imposible"]:
        return "escribes Imposible, pero sí se pueden ordenar las tareas"
    if not all(x.lstrip("-").isdigit() for x in t):
        return "la línea debería tener solo números de tarea (o Imposible)"
    t = [int(x) for x in t]
    if len(t) != n:
        return f"hay {n} tareas y escribes {len(t)} números"
    pos = {}
    for i, x in enumerate(t):
        if not 1 <= x <= n:
            return f"la tarea {x} no existe (van de 1 a {n})"
        if x in pos:
            return f"la tarea {x} aparece dos veces"
        pos[x] = i
    for a, b in deps:
        if pos[a] > pos[b]:
            return f"la tarea {a} debe ir antes que la {b}, y en tu orden va después"
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    for i, (n, deps) in enumerate(_casos(entrada)):
        x = e[i]
        y = o[i] if i < len(o) else None
        d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
        if y is None:
            d["motivo"] = "tu salida acaba antes"
            return d
        if y == x:
            continue
        if x == "Imposible":
            d["motivo"] = "hay un ciclo de dependencias: la respuesta es Imposible"
            return d
        motivo = _revisa(n, deps, y)
        if motivo:
            d["motivo"] = motivo
            return d
        if y != " ".join(y.split()):
            d["motivo"] = "el orden es válido, pero los números deben ir separados por un solo espacio"
            d["pe"] = True
            return d
    if len(o) > len(e):
        return {"linea": len(e) + 1, "esperada": None, "obtenida": o[len(e)], "total": len(e),
                "lineas_tuyas": len(o), "motivo": "escribes líneas de más"}
    return None


def comprobar(entrada, esperada, obtenida):
    d = _comprobar(entrada, esperada, obtenida)
    if d is None or d.get("pe"):
        return d
    # ¿Los mismos datos con otro reparto en líneas? Se reparten tus palabras como en la salida
    # esperada y, si así es correcta, es un error de presentación.
    cuentas = [len(l.split()) for l in _lineas(esperada)]
    pal = obtenida.split()
    if len(pal) == sum(cuentas):
        nuevas, k = [], 0
        for c in cuentas:
            nuevas.append(" ".join(pal[k:k + c]))
            k += c
        if _comprobar(entrada, esperada, "\n".join(nuevas) + "\n") is None:
            d = dict(d)
            d["pe"] = True
            d["motivo"] = "tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado"
    return d
