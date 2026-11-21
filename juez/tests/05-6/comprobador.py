"""Comprobador de 05-6 «Sistema de inecuaciones»: vale CUALQUIER asignación que cumpla todo.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/05-6.js en el navegador (el verificador comprueba que coinciden).
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


def _revisa(n, ineq, linea):
    t = linea.split()
    if t == ["NO"]:
        return "escribes NO, pero el sistema sí tiene solución"
    if not t or t[0] != "SI":
        return "la línea debe empezar por SI (o ser NO)"
    vals = t[1:]
    if not all(x.lstrip("-").isdigit() and x.lstrip("-") for x in vals):
        return "después de SI solo puede haber números enteros"
    vals = [int(x) for x in vals]
    if len(vals) != n:
        return f"hay {n} variables y escribes {len(vals)} valores"
    for i, j in ineq:
        if not vals[i - 1] < vals[j - 1]:
            return f"no se cumple x{i} < x{j}: le das {vals[i - 1]} a x{i} y {vals[j - 1]} a x{j}"
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    for i, (n, ineq) in enumerate(_casos(entrada)):
        x = e[i]
        y = o[i] if i < len(o) else None
        d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
        if y is None:
            d["motivo"] = "tu salida acaba antes"
            return d
        if y == x:
            continue
        if x == "NO":
            d["motivo"] = "hay un ciclo de inecuaciones: la respuesta es NO"
            return d
        motivo = _revisa(n, ineq, y)
        if motivo:
            d["motivo"] = motivo
            return d
        if y != " ".join(y.split()):
            d["motivo"] = "la asignación es válida, pero los valores deben ir separados por un solo espacio"
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
