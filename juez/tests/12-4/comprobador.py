"""Comprobador de 12-4 «Mejor no llevar muchas monedas»: vale CUALQUIER pago con el mínimo de monedas.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/12-4.js en el navegador (el verificador comprueba que coinciden).
"""


def _casos(entrada):
    d = iter(map(int, entrada.split()))
    r = []
    for _ in range(next(d)):
        n = next(d)
        v = [next(d) for _ in range(n)]
        c = [next(d) for _ in range(n)]
        r.append((v, c, next(d)))
    return r


def _entero(s):
    return 0 < len(s) <= 7 and all(c in "0123456789" for c in s)


def comprobar(entrada, esperada, obtenida):
    casos = _casos(entrada)
    e = esperada.replace("\r", "").split("\n")
    o = [x.rstrip() for x in obtenida.replace("\r", "").split("\n")]
    while o and o[-1] == "":
        o.pop()
    n, mias = len(casos), len(o)
    formato = None
    if mias > n:
        return {"linea": n + 1, "esperada": None, "obtenida": o[n], "total": n, "lineas_tuyas": mias,
                "motivo": "escribes líneas de más: una por caso"}
    o += [""] * (n - len(o))
    for k, (v, c, P) in enumerate(casos):
        def fallo(motivo):
            return {"linea": k + 1, "esperada": e[k], "obtenida": o[k], "total": n,
                    "lineas_tuyas": mias, "motivo": motivo}
        x, bien = o[k].split(), e[k].split()
        if bien[0] == "NO":
            if x != ["NO"]:
                return fallo("el precio no se puede pagar de forma exacta: hay que escribir NO")
        else:
            if not x or x[0] != "SI":
                return fallo("el precio sí se puede pagar: la línea debe empezar por SI")
            if len(x) != len(v) + 1 or not all(_entero(s) for s in x[1:]):
                return fallo(f"después de SI van {len(v)} números, uno por tipo de moneda")
            u = [int(s) for s in x[1:]]
            if any(a > b for a, b in zip(u, c)):
                return fallo("usas más monedas de un tipo de las que hay")
            if sum(a * b for a, b in zip(u, v)) != P:
                return fallo(f"esas monedas no suman {P}")
            minimo = sum(int(s) for s in bien[1:])
            if sum(u) != minimo:
                return fallo(f"se puede pagar con {minimo} monedas y usas {sum(u)}")
        if o[k] != " ".join(x) and formato is None:
            formato = fallo("la respuesta es correcta, pero separa con un solo espacio")
    if formato is not None:
        formato["pe"] = True
    return formato
