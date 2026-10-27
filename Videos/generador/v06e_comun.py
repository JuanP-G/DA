"""Piezas comunes de los vídeos de los ejercicios 06-3, 06-4 y 06-5 (Kruskal con conjuntos disjuntos).

Los tres son el mismo esqueleto: aristas por valor creciente, `unidos(u, v)` para descartar ciclos y `unir`.
Solo cambia (a) cuándo se para y (b) qué se guarda: la suma (06-3), el valor de la última (06-4)
o el valor de la que une origen y destino (06-5).
"""
from vidlib import Slide, C
from v06_teoria import wgraph, PAL

TEMA = "Tema 6 · Conjuntos disjuntos y grafos valorados"


def sim(ej, modo):
    """
    ej: dict(n, E=[(a, b, valor)] con vértices desde 1, pos={v: (x, y)}, org, dst).
    modo: 'sum' (06-3), 'ult' (06-4), 'par' (06-5).
    Devuelve (pasos, final). Cada paso: k, d ('une' | 'ciclo' | 'para'), tot, ult, el, grupos.
    """
    n, E = ej["n"], ej["E"]
    p = list(range(n + 1))

    def f(x):
        while p[x] != x:
            x = p[x]
        return x

    def grupos():
        g = {}
        for v in range(1, n + 1):
            g.setdefault(f(v), []).append(v)
        return sorted(g.values(), key=lambda m: m[0])

    def para(el):
        if modo == "sum":
            return el == n - 1
        if modo == "ult":
            return len(grupos()) == 1
        return f(ej["org"]) == f(ej["dst"])

    pasos, tot, ult, el = [], 0, 0, 0
    for k in sorted(range(len(E)), key=lambda k: (E[k][2], k)):
        if para(el):
            pasos.append(dict(k=k, d="para", tot=tot, ult=ult, el=el, grupos=grupos()))
            break
        a, b, c = E[k]
        if f(a) != f(b):
            p[f(a)] = f(b)
            tot += c
            ult = c
            el += 1
            d = "une"
        else:
            d = "ciclo"
        pasos.append(dict(k=k, d=d, tot=tot, ult=ult, el=el, grupos=grupos()))
    return pasos, dict(ok=para(el), tot=tot, ult=ult, el=el, grupos=grupos())


def colores_grupos(grupos):
    return {v: PAL[gi % len(PAL)] for gi, g in enumerate(grupos) if len(g) > 1 for v in g}


def dibuja(s, ej, pasos, hasta, k_actual=None, grupos=None):
    """Grafo con las aristas decididas en pasos[:hasta]; la actual en dorado; los nodos se colorean por grupo."""
    pos, E = ej["pos"], ej["E"]
    es = {}
    for st in pasos[:hasta]:
        a, b, c = E[st["k"]]
        es[(a, b)] = {"une": ("green", 7), "ciclo": ("muted", 3), "para": ("red", 4)}[st["d"]]
    if k_actual is not None:
        a, b, c = E[k_actual]
        es[(a, b)] = ("gold", 8)
    if grupos is None:
        grupos = [[v] for v in range(1, ej["n"] + 1)] if hasta == 0 else pasos[hasta - 1]["grupos"]
    col = colores_grupos(grupos)
    ns = {v: (col.get(v, "node"), "node_t", None) for v in pos}
    for key in ("org", "dst"):
        if key in ej:
            v = ej[key]
            ns[v] = (ns[v][0], "node_t", "blue" if key == "org" else "red")
    wgraph(s, pos, E, es=es, ns=ns, r=24, lsize=22)


def grupos_txt(grupos):
    return "  ".join("{" + ",".join(map(str, g)) + "}" for g in grupos)


def slide_paso(titulo, corner, ej, modo, pasos, i, nombre_ej, etiqueta_arista):
    """Una diapositiva por arista: lista ordenada a la izquierda, grafo a la derecha."""
    st = pasos[i]
    E = ej["E"]
    a, b, c = E[st["k"]]
    s = Slide(titulo, corner)
    s.box(24, 84, 600, 520, f"{etiqueta_arista} ordenadas por valor")
    orden = sorted(range(len(E)), key=lambda k: (E[k][2], k))
    for j, k in enumerate(orden):
        x, y, cc = E[k]
        marca = ""
        if j < i:
            marca = {"une": "  ✓", "ciclo": "  ✗ ciclo", "para": ""}[pasos[j]["d"]]
        col = ("red" if st["d"] == "para" else "gold") if k == st["k"] else ("muted" if j > i else "text")
        s.text((56, 132 + j * 40), f"{x}–{y}  ({cc}){marca}", size=24, mono=True, color=col)
    y0 = 132 + len(E) * 40 + 14
    if modo == "sum":
        s.text((56, y0), f"coste = {st['tot']}", size=26, bold=True, color="gold")
        s.text((56, y0 + 40), f"elegidos = {st['el']} de {ej['n'] - 1}", size=22, color="muted")
    elif modo == "ult":
        s.text((56, y0), f"última = {st['ult']}", size=26, bold=True, color="gold")
        s.text((56, y0 + 40), f"conjuntos = {len(st['grupos'])}", size=22, color="muted")
    else:
        s.text((56, y0), f"aguante = {st['ult']}", size=26, bold=True, color="gold")
        unidos = any(ej["org"] in g and ej["dst"] in g for g in st["grupos"])
        s.text((56, y0 + 40), f"¿{ej['org']} y {ej['dst']} unidos?  {'sí' if unidos else 'no'}", size=22, color="muted")
    s.box(644, 84, 612, 520, nombre_ej)
    if st["d"] == "para":     # la arista que ya no se mira, en rojo
        dibuja(s, ej, pasos, i + 1, None, grupos=pasos[i - 1]["grupos"] if i else None)
    else:
        dibuja(s, ej, pasos, i, st["k"], grupos=pasos[i - 1]["grupos"] if i else None)
    s.text((664, 560), "grupos: " + grupos_txt(pasos[i - 1]["grupos"] if i else [[v] for v in range(1, ej["n"] + 1)]),
           size=18, color="muted", mono=True)
    return s


def slide_final(titulo, corner, ej, modo, pasos, fin, nombre_ej, caption, resultado, detalle):
    s = Slide(titulo, corner)
    s.box(24, 84, 600, 520, "resultado")
    s.text((56, 140), f"conjuntos que quedan: {len(fin['grupos'])}", size=26, color="muted")
    s.text((56, 186), grupos_txt(fin["grupos"]), size=26, mono=True)
    s.text((56, 270), detalle, size=24, mono=True)
    s.text((56, 350), resultado, size=48 if len(resultado) < 12 else 27, bold=True, color="gold")
    s.box(644, 84, 612, 520, nombre_ej)
    dibuja(s, ej, pasos, len(pasos), None, grupos=fin["grupos"])
    s.caption(caption, y=626)
    return s


def narra(ej, modo, pasos, i, nombre):
    """Narración de una arista en función del modo."""
    st = pasos[i]
    a, b, c = ej["E"][st["k"]]
    if st["d"] == "une":
        extra = {"sum": f"Se construye y sumamos su coste: llevamos {st['tot']}.",
                 "ult": f"Se une, y apuntamos {c} como última longitud.",
                 "par": f"Se une, y apuntamos {c} como el tiempo que hay que aguantar."}[modo]
        return f"{nombre} {a} y {b}, valor {c}: están en conjuntos distintos. {extra}"
    if st["d"] == "ciclo":
        return f"{nombre} {a} y {b}, valor {c}: ya están unidos, cerraría un ciclo. Se descarta."
    return {"sum": f"Ya tenemos {ej['n'] - 1} elementos, uno menos que vértices: el árbol está completo. Paramos sin mirar el resto.",
            "ult": "Ya queda un solo conjunto: todo está conectado. Paramos; las aristas que faltan no hacen falta.",
            "par": f"Origen y destino ya están unidos: paramos. Las aristas que quedan son aún más largas."}[modo]


def pinta_preview(segs, prefijo):
    import os
    os.makedirs("preview", exist_ok=True)
    for i, (sl, _, _) in enumerate(segs):
        sl.img.save(f"preview/{prefijo}_{i:02}.png")
    print(len(segs), "diapositivas")
