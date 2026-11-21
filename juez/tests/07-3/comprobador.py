"""Comprobador de 07-3 «RapidEats con ruta»: vale CUALQUIER camino de tiempo mínimo.

Cada pedido escribe «T: o -> ... -> d» (o NO LLEGA) y tras cada caso «---». El tiempo debe ser el
mínimo (el de la salida esperada) y el camino tiene que existir, ir de o a d y sumar ese tiempo.
comprobar(entrada, esperada, obtenida) -> None si es correcta, o un dict con la primera línea mala:
{linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace comprobadores/07-3.js.
"""
import re

_FORMA = re.compile(r"^(\d+): (\d+(?: -> \d+)*)$")


def _lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def _casos(entrada):
    """Por cada caso: (tramos {(a,b): tiempo mínimo}, [(origen, destino), ...])."""
    v = entrada.split()
    p = 0
    def sig():
        nonlocal p
        p += 1
        return int(v[p - 1])
    for _ in range(sig()):
        n, c = sig(), sig()
        tramos = {}
        for _ in range(c):
            a, b, t = sig(), sig(), sig()
            for k in ((a, b), (b, a)):
                tramos[k] = min(t, tramos.get(k, t))
        yield tramos, [(sig(), sig()) for _ in range(sig())]


def _revisa(tramos, o, d, esperada, linea):
    if esperada == "NO LLEGA":
        return "no hay ningún camino de un punto al otro: hay que escribir NO LLEGA"
    if linea == "NO LLEGA":
        return f"escribes NO LLEGA, pero sí hay camino de {o} a {d}"
    norm = re.sub(r"\s*->\s*", " -> ", re.sub(r"\s*:\s*", ": ", " ".join(linea.split()), count=1))
    m = _FORMA.match(norm)
    if not m:
        return "el formato debe ser «tiempo: origen -> ... -> destino»"
    tiempo = int(m.group(1))
    camino = [int(x) for x in m.group(2).split(" -> ")]
    minimo = int(esperada.split(":")[0])
    if tiempo != minimo:
        return f"el tiempo mínimo es {minimo} y escribes {tiempo}"
    if camino[0] != o:
        return f"el camino debe empezar en el origen ({o}) y empieza en {camino[0]}"
    if camino[-1] != d:
        return f"el camino debe acabar en el destino ({d}) y acaba en {camino[-1]}"
    suma = 0
    for a, b in zip(camino, camino[1:]):
        if (a, b) not in tramos:
            return f"no hay ningún tramo entre {a} y {b}"
        suma += tramos[(a, b)]
    if suma != minimo:
        return f"tu camino tarda {suma}, no {minimo}: no es un camino mínimo"
    if norm != linea:
        return ("PE", "el camino es correcto, pero el formato no es exacto: «tiempo: a -> b -> c», "
                "con un espacio tras los dos puntos y alrededor de cada ->")
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    i = 0
    for tramos, pedidos in _casos(entrada):
        for ped in pedidos + [None]:                   # None = la línea «---» tras el caso
            org, dst = ped if ped else (None, None)
            x = e[i]
            y = o[i] if i < len(o) else None
            d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
            i += 1
            if y is None:
                d["motivo"] = "tu salida acaba antes"
                return d
            if y == x:
                continue
            if org is None:
                d["motivo"] = "tras los pedidos de cada caso va una línea con ---"
                return d
            motivo = _revisa(tramos, org, dst, x, y)
            if isinstance(motivo, tuple):
                d["motivo"], d["pe"] = motivo[1], True
                return d
            if motivo:
                d["motivo"] = motivo
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
