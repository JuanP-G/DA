"""
Librería mínima para generar los vídeos explicativos.

Cada vídeo es una lista de "segmentos": una imagen fija (1280x720) más una
frase de narración. La duración de cada segmento la marca su audio. Al final
se juntan con ffmpeg: vídeo H.264 + audio AAC + pista de subtítulos.

Voz: Piper (TTS offline). Ruta del modelo en la variable PIPER_MODEL.
"""
import os
import re
import subprocess
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 24

_FD = "/usr/share/fonts/truetype/dejavu/"
_fonts = {}


def font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _fonts:
        name = ("DejaVuSansMono" if mono else "DejaVuSans") + ("-Bold" if bold else "") + ".ttf"
        _fonts[key] = ImageFont.truetype(_FD + name, size)
    return _fonts[key]


# Paleta (la misma familia de colores que los vídeos del tema 3)
C = dict(
    top=(14, 30, 62), bot=(34, 78, 130),
    panel=(10, 22, 48), border=(46, 70, 115),
    text=(234, 240, 248), muted=(150, 172, 205), dim=(95, 115, 150),
    gold=(255, 206, 92), gold_d=(120, 95, 30),
    blue=(92, 192, 255), blue_d=(25, 70, 110),
    red=(255, 118, 108), red_d=(110, 40, 40),
    green=(112, 222, 152), green_d=(30, 90, 60),
    purple=(196, 150, 255), purple_d=(70, 50, 110),
    node=(207, 216, 230), node_t=(18, 28, 48),
    kw=(255, 121, 198), num=(189, 147, 249), com=(110, 135, 170), typ=(139, 233, 253),
)

_bg = None


def background():
    global _bg
    if _bg is None:
        img = Image.new("RGB", (W, H))
        px = img.load()
        for y in range(H):
            t = y / (H - 1)
            col = tuple(int(C["top"][i] * (1 - t) + C["bot"][i] * t) for i in range(3))
            for x in range(W):
                px[x, y] = col
        _bg = img
    return _bg.copy()


class Slide:
    def __init__(self, title=None, corner=None):
        self.img = background()
        self.d = ImageDraw.Draw(self.img)
        if title:
            self.d.text((40, 26), title, font=font(30, True), fill=C["text"])
        if corner:
            self.d.text((W - 40, 34), corner, font=font(18), fill=C["muted"], anchor="ra")

    # ---------- texto ----------
    def text(self, xy, s, size=24, color="text", bold=False, anchor="la", mono=False):
        self.d.text(xy, s, font=font(size, bold, mono), fill=C.get(color, color), anchor=anchor)

    def wrap(self, x, y, w, s, size=24, color="text", bold=False, gap=8, center=False):
        f = font(size, bold)
        words, lines, cur = s.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.d.textlength(t, font=f) <= w:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        for ln in lines:
            if center:
                self.d.text((x + w / 2, y), ln, font=f, fill=C.get(color, color), anchor="ma")
            else:
                self.d.text((x, y), ln, font=f, fill=C.get(color, color))
            y += size + gap
        return y

    def caption(self, s, y=640):
        """Frase corta centrada en la parte de abajo."""
        self.wrap(80, y, W - 160, s, size=22, color="text", center=True)

    def bullets(self, x, y, w, items, size=24, gap=18, mark="•", color="text"):
        for it in items:
            col = color
            if isinstance(it, tuple):
                it, col = it
            self.d.text((x, y), mark, font=font(size, True), fill=C["gold"])
            y = self.wrap(x + 30, y, w - 30, it, size=size, color=col) + gap
        return y

    def box(self, x, y, w, h, title=None, fill="panel", border="border", r=14):
        self.d.rounded_rectangle((x, y, x + w, y + h), r, fill=C.get(fill, fill), outline=C.get(border, border), width=2)
        if title:
            self.d.text((x + 16, y + 10), title, font=font(16), fill=C["muted"])

    def pill(self, x, y, s, fill="gold", color="node_t", size=20, padx=14, pady=7, bold=True):
        f = font(size, bold)
        w = self.d.textlength(s, font=f)
        self.d.rounded_rectangle((x, y, x + w + 2 * padx, y + size + 2 * pady), (size + 2 * pady) // 2,
                                 fill=C.get(fill, fill))
        self.d.text((x + padx, y + pady - 1), s, font=f, fill=C.get(color, color))
        return x + w + 2 * padx

    # ---------- grafo ----------
    def graph(self, pos, edges, ns=None, es=None, r=24, labels=None, under=None, over=None, lsize=None):
        """
        pos:   {v: (x, y)}
        edges: [(a, b)]
        ns:    {v: (relleno, color_texto, aro)}  estilo de nodo
        es:    {(a, b): (color, grosor)}         estilo de arista
        under: {v: texto pequeño debajo del nodo}  (p.ej. distancias)
        over:  {v: texto pequeño encima del nodo}
        """
        ns, es = ns or {}, es or {}
        for a, b in edges:
            st = es.get((a, b)) or es.get((b, a)) or ("dim", 3)
            self.d.line((pos[a], pos[b]), fill=C.get(st[0], st[0]), width=st[1])
        for v, (x, y) in pos.items():
            fill, tcol, ring = ns.get(v, ("node", "node_t", None))
            if ring:
                self.d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), outline=C.get(ring, ring), width=4)
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=C.get(fill, fill))
            lab = str(v) if labels is None else labels[v]
            self.d.text((x, y), lab, font=font(lsize or (20 if len(lab) < 3 else 15), True),
                        fill=C.get(tcol, tcol), anchor="mm")
            if under and v in under:
                self.d.text((x + r * 0.75, y + r * 0.6), under[v], font=font(17, True), fill=C["gold"], anchor="la")
            if over and v in over:
                self.d.text((x, y - r - 10), over[v], font=font(16), fill=C["muted"], anchor="md")

    # ---------- grafo dirigido ----------
    def dgraph(self, pos, edges, ns=None, es=None, r=24, labels=None, under=None, elabels=None, lsize=None):
        """
        Como graph(), pero con flechas.
        edges:   [(a, b)]  la arista va de a a b (a == b dibuja un lazo)
        elabels: {(a, b): (texto, color)}  texto junto a la flecha (p.ej. la operación)
        Si existen a->b y b->a se dibujan paralelas, separadas, para que se vean las dos.
        """
        import math
        ns, es, elabels = ns or {}, es or {}, elabels or {}
        todas = set(edges)
        for a, b in edges:
            col, wd = es.get((a, b), ("dim", 3))
            col = C.get(col, col)
            if a == b:
                x, y = pos[a]
                self.d.ellipse((x - 15, y - r - 24, x + 15, y - r + 4), outline=col, width=wd)
                self.d.polygon([(x + 10, y - r + 6), (x + 2, y - r - 6), (x + 17, y - r - 5)], fill=col)
                if (a, b) in elabels:
                    t, tc = elabels[(a, b)]
                    self.d.text((x + 24, y - r - 18), t, font=font(15, True), fill=C.get(tc, tc), anchor="lm")
                continue
            (x1, y1), (x2, y2) = pos[a], pos[b]
            L = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            nx, ny = -uy, ux
            off = 9 if (b, a) in todas else 0
            sx, sy = x1 + ux * r + nx * off, y1 + uy * r + ny * off
            ex, ey = x2 - ux * (r + 3) + nx * off, y2 - uy * (r + 3) + ny * off
            self.d.line((sx, sy, ex - ux * 10, ey - uy * 10), fill=col, width=wd)
            self.d.polygon([(ex, ey), (ex - ux * 16 + nx * 7, ey - uy * 16 + ny * 7),
                            (ex - ux * 16 - nx * 7, ey - uy * 16 - ny * 7)], fill=col)
            if (a, b) in elabels:
                t, tc = elabels[(a, b)]
                mx, my = (sx + ex) / 2 + nx * (14 + off), (sy + ey) / 2 + ny * (14 + off)
                self.d.text((mx, my), t, font=font(15, True), fill=C.get(tc, tc), anchor="mm")
        for v, (x, y) in pos.items():
            fill, tcol, ring = ns.get(v, ("node", "node_t", None))
            if ring:
                self.d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), outline=C.get(ring, ring), width=4)
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=C.get(fill, fill))
            lab = str(v) if labels is None else labels[v]
            self.d.text((x, y), lab, font=font(lsize or (20 if len(lab) < 3 else 15), True),
                        fill=C.get(tcol, tcol), anchor="mm")
            if under and v in under:
                self.d.text((x + r * 0.75, y + r * 0.6), under[v], font=font(17, True), fill=C["gold"], anchor="la")

    # ---------- bitmap ----------
    def grid(self, x, y, bitmap, cell, fills=None, labels=None, rings=(), lsize=None, links=(), linkcol="gold", esquina=False):
        """
        Dibuja un bitmap ('#' negro, '-' blanco) como cuadrícula.
        fills:  {(i, j): color}  para pintar píxeles (p.ej. por mancha)
        labels: {(i, j): texto}  texto dentro del píxel
        rings:  píxeles con borde destacado
        links:  [((i, j), (i2, j2))] segmentos entre centros (las aristas del grafo)
        """
        fills, labels = fills or {}, labels or {}
        for i, fila in enumerate(bitmap):
            for j, ch in enumerate(fila):
                x0, y0 = x + j * cell, y + i * cell
                col = fills.get((i, j), (14, 16, 24) if ch == "#" else (222, 228, 238))
                self.d.rectangle((x0 + 1, y0 + 1, x0 + cell - 2, y0 + cell - 2), fill=C.get(col, col) if isinstance(col, str) else col)
        for (a, b) in links:
            p = (x + a[1] * cell + cell / 2, y + a[0] * cell + cell / 2)
            q = (x + b[1] * cell + cell / 2, y + b[0] * cell + cell / 2)
            self.d.line((p, q), fill=C.get(linkcol, linkcol), width=3)
            for c in (p, q):
                self.d.ellipse((c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4), fill=C.get(linkcol, linkcol))
        for (i, j) in rings:
            x0, y0 = x + j * cell, y + i * cell
            self.d.rectangle((x0 - 1, y0 - 1, x0 + cell, y0 + cell), outline=C["red"], width=4)
        for (i, j), t in labels.items():
            ch = bitmap[i][j]
            dark = (i, j) in fills or ch == "#"
            col = C["node_t"] if (i, j) in fills else (C["text"] if dark else (70, 80, 100))
            if esquina:   # número pequeño arriba a la izquierda, para que no lo tapen las aristas
                self.d.text((x + j * cell + 4, y + i * cell + 3), str(t),
                            font=font(lsize or max(9, cell // 4)), fill=(150, 165, 190) if dark else (70, 80, 100), anchor="la")
            else:
                self.d.text((x + j * cell + cell / 2, y + i * cell + cell / 2), str(t),
                            font=font(lsize or max(10, cell // 3), True), fill=col, anchor="mm")

    # ---------- código ----------
    def code(self, x, y, w, h, lines, hl=(), title=None, size=15):
        self.box(x, y, w, h, title)
        top = 38 if title else 14
        lh = min(size + 6, (h - top - 8) // max(1, len(lines)))   # si no cabe, letra más pequeña
        size = lh - 6
        f = font(size, mono=True)
        yy = y + top
        for n, s in lines:
            if n in hl:
                self.d.rectangle((x + 4, yy - 2, x + w - 4, yy + lh - 3), fill=(78, 66, 30))
                self.d.rectangle((x + 4, yy - 2, x + 8, yy + lh - 3), fill=C["gold"])
            self.d.text((x + 14, yy), f"{n:>3}", font=f, fill=C["dim"])
            self._code_line(x + 54, yy, s, f, n in hl)
            yy += lh

    _tok = re.compile(r"(//.*$)|(\"[^\"]*\"|'[^']*')|(\b\d+\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)")
    _kws = {"for", "if", "else", "while", "return", "continue", "const", "class", "public", "private",
            "auto", "void", "bool", "int", "true", "false"}
    _types = {"Grafo", "vector", "queue", "string", "unordered_map", "Adys"}

    def _code_line(self, x, y, s, f, hot):
        for m in self._tok.finditer(s):
            t = m.group(0)
            if m.group(1):
                col = C["com"]
            elif m.group(2):
                col = (241, 250, 140)
            elif m.group(3):
                col = C["num"]
            elif m.group(4) and t in self._kws:
                col = C["kw"]
            elif m.group(4) and t in self._types:
                col = C["typ"]
            else:
                col = (255, 255, 255) if hot else (210, 222, 240)
            self.d.text((x, y), t, font=f, fill=col)
            x += self.d.textlength(t, font=f)

    # ---------- estructuras ----------
    def cells(self, x, y, label, vals, idx=True, hl=None, cw=44, size=18, colors=None, first=0):
        """Vector dibujado como fila de casillas, con índices debajo."""
        hl = hl or {}
        colors = colors or {}
        self.d.text((x, y + 8), label, font=font(17, True), fill=C["muted"])
        x0 = x + max(110, int(self.d.textlength(label, font=font(17, True))) + 16)
        for i, v in enumerate(vals):
            cx = x0 + i * (cw + 4)
            fill = colors.get(i, (24, 42, 78))
            self.d.rounded_rectangle((cx, y, cx + cw, y + 36), 7, fill=C.get(fill, fill),
                                     outline=C["gold"] if i in hl else C["border"], width=3 if i in hl else 1)
            self.d.text((cx + cw / 2, y + 18), str(v), font=font(size, True), fill=C["text"], anchor="mm")
            if idx:
                self.d.text((cx + cw / 2, y + 42), str(i + first), font=font(13), fill=C["dim"], anchor="ma")
        return x0

    def queue_row(self, x, y, label, vals, size=18):
        self.d.text((x, y + 8), label, font=font(17, True), fill=C["muted"])
        cx = x + 110
        if not vals:
            self.d.text((cx, y + 8), "vacía", font=font(17), fill=C["dim"])
        for v in vals:
            s = str(v)
            w = max(40, self.d.textlength(s, font=font(size, True)) + 20)
            self.d.rounded_rectangle((cx, y, cx + w, y + 36), 7, fill=C["blue_d"], outline=C["blue"], width=2)
            self.d.text((cx + w / 2, y + 18), s, font=font(size, True), fill=C["text"], anchor="mm")
            cx += w + 6


def code_lines(cpp_path, first, last, maxc=60, skip=()):
    """
    Devuelve [(número de línea, texto)] del .cpp real, para que el vídeo enseñe el código de verdad.
    Si una línea no cabe en el panel se le quita el comentario final y, si aun así no cabe, se recorta.
    """
    src = Path(cpp_path).read_text(encoding="utf-8").splitlines()
    out = []
    for i in range(first, last + 1):
        if any(a <= i <= b for a, b in skip):
            continue
        s = src[i - 1].replace("\t", "    ").rstrip()
        if len(s) > maxc and "//" in s and not s.lstrip().startswith("//"):
            s = s[: s.index("//")].rstrip()
        if len(s) > maxc:
            s = s[: maxc - 1] + "…"
        out.append((i, s))
    return out


def find_line(cpp_path, needle, start=1):
    src = Path(cpp_path).read_text(encoding="utf-8").splitlines()
    for i in range(start, len(src) + 1):
        if needle in src[i - 1]:
            return i
    raise ValueError(f"no encuentro {needle!r} en {cpp_path}")


# ---------------------------------------------------------------------------
# voz y montaje
# ---------------------------------------------------------------------------
_voice = None


def _acorta_silencios(a, sr, th=300, maxsil=0.3):
    """Deja en maxsil segundos cualquier silencio interno más largo."""
    import array
    win = int(0.02 * sr)
    bloques = [a[i:i + win] for i in range(0, len(a), win)]
    out, run = array.array("h"), 0
    for b in bloques:
        if max((abs(x) for x in b), default=0) < th:
            run += 1
            if run * 0.02 > maxsil:
                continue
        else:
            run = 0
        out.extend(b)
    return out


def _tts(text, out_wav, gap=0.22):
    """
    Sintetiza la narración frase a frase, recortando el silencio que Piper deja
    al final de cada una. Devuelve (duración total, [(frase, inicio, fin)]).
    """
    global _voice
    import array
    from piper import PiperVoice, SynthesisConfig
    if _voice is None:
        _voice = PiperVoice.load(os.environ["PIPER_MODEL"])
    sr = _voice.config.sample_rate
    # poco ruido = voz estable (con los valores por defecto el modelo mete pausas y balbuceos)
    cfg = SynthesisConfig(noise_scale=0.3, noise_w_scale=0.1, length_scale=1.0)
    frases = [f for f in re.split(r"(?<=[.:;?!])\s+", text.strip()) if f]
    pcm, tiempos, t = array.array("h"), [], 0.0
    for f in frases:
        a = array.array("h")
        for ch in _voice.synthesize(f, syn_config=cfg):
            a.frombytes(ch.audio_int16_bytes)
        a = _acorta_silencios(a, sr)
        # recorte de silencios al principio y al final
        th = 400
        i = next((k for k, x in enumerate(a) if abs(x) > th), 0)
        j = len(a) - next((k for k, x in enumerate(reversed(a)) if abs(x) > th), 0)
        a = a[max(0, i - int(0.03 * sr)): min(len(a), j + int(0.08 * sr))]
        d = len(a) / sr
        tiempos.append((f, t, t + d))
        pcm.extend(a)
        pcm.extend([0] * int(gap * sr))
        t += d + gap
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    return len(pcm) / sr, tiempos


def _srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


# la narración deletrea siglas y letras para que la voz las lea bien; en los subtítulos se escriben normal
_SUBS = [(r"\bT T L\b", "TTL"), (r"\bB F S\b", "BFS"), (r"\bD F S\b", "DFS"), (r"unordered map", "unordered_map"),
         (r"\buve\b", "V"), (r"\bka\b", "k"), (r"\bene\b", "N"), (r"\bpe\b", "p"), (r"\bV más a\b", "V más A"),
         (r"\bT A D\b", "TAD"), (r"\bD A G\b", "DAG"), (r"\bE M T\b", "EMT"), (r"poner gemelas", "ponGemelas"),
         (r"push front", "push_front"), (r"Page Rank", "PageRank")]


def _texto_sub(s):
    for a, b in _SUBS:
        s = re.sub(a, b, s)
    return s


def _split_sub(text, maxlen=58):
    """Parte una frase larga en trozos de subtítulo (por signos de puntuación o palabras)."""
    parts = re.split(r"(?<=[.:;?!])\s+", text.strip())
    out = []
    for p in parts:
        while len(p) > maxlen * 2:
            cut = p.rfind(" ", 0, maxlen * 2)
            cut = cut if cut > 0 else maxlen * 2
            out.append(p[:cut])
            p = p[cut:].strip()
        out.append(p)
    return [o for o in out if o]


def _wrap2(s, maxlen=58):
    if len(s) <= maxlen:
        return s
    cut = s.rfind(" ", 0, len(s) // 2 + 8)
    return s[:cut] + "\n" + s[cut + 1:]


def build(segments, out_mp4, pause=0.35, chapters=None):
    """
    segments: lista de (Slide o Image, narración o None, duración mínima)
    chapters: opcional, {índice de segmento: título}; se guardan como capítulos del mp4
    """
    out_mp4 = Path(out_mp4)
    tmp = Path(tempfile.mkdtemp(prefix="vid_"))
    concat_v, concat_a, subs = [], [], []
    t = 0.0
    sr = None
    cap_t = []
    for i, (sl, narr, dmin) in enumerate(segments):
        if chapters and i in chapters:
            cap_t.append((t, chapters[i]))
        img = sl.img if isinstance(sl, Slide) else sl
        png = tmp / f"s{i:03}.png"
        img.save(png)
        dur = dmin or 0
        if narr:
            wav = tmp / f"a{i:03}.wav"
            a, frases = _tts(narr, wav)
            with wave.open(str(wav), "rb") as wf:
                sr = wf.getframerate()
            dur = max(dur, a + pause)
            concat_a.append((wav, dur))
            # un subtítulo por frase (las muy largas se parten en proporción a sus caracteres)
            for f, ini, fin in frases:
                chunks = _split_sub(_texto_sub(f))
                total = sum(len(c) for c in chunks)
                tt = t + ini
                for c in chunks:
                    d = (fin - ini) * len(c) / total
                    subs.append((tt, tt + d, _wrap2(c)))
                    tt += d
        else:
            concat_a.append((None, dur))
        # redondeo a frames para que audio y vídeo no se desfasen
        dur = round(dur * FPS) / FPS
        concat_a[-1] = (concat_a[-1][0], dur)
        concat_v.append((png, dur))
        t += dur

    sr = sr or 16000
    # audio: cada trozo se rellena con silencio hasta su duración
    full = tmp / "audio.wav"
    with wave.open(str(full), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sr)
        for wav, dur in concat_a:
            n = int(round(dur * sr))
            data = b""
            if wav:
                with wave.open(str(wav), "rb") as wf:
                    data = wf.readframes(wf.getnframes())
            data = data[: n * 2]
            out.writeframes(data + b"\x00\x00" * (n - len(data) // 2))

    lst = tmp / "video.txt"
    with open(lst, "w") as f:
        for png, dur in concat_v:
            f.write(f"file '{png}'\nduration {dur:.4f}\n")
        f.write(f"file '{concat_v[-1][0]}'\n")

    srt = tmp / "subs.srt"
    with open(srt, "w", encoding="utf-8") as f:
        for k, (a, b, s) in enumerate(subs, 1):
            f.write(f"{k}\n{_srt_time(a)} --> {_srt_time(b)}\n{s}\n\n")

    meta = tmp / "meta.txt"
    with open(meta, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        for k, (a, titulo) in enumerate(cap_t):
            b = cap_t[k + 1][0] if k + 1 < len(cap_t) else t
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a * 1000)}\nEND={int(b * 1000)}\ntitle={titulo}\n")
    if cap_t:
        print("capítulos:")
        for a, titulo in cap_t:
            print(f"  {int(a // 60):02}:{int(a % 60):02}  {titulo}")

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-i", str(full), "-i", str(srt), "-i", str(meta),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map_chapters", "3",
        "-vf", f"fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "96k", "-ar", "44100",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=spa",
        "-movflags", "+faststart", "-shortest",
        str(out_mp4),
    ], check=True)
    return t


# ---------------------------------------------------------------------------
# plantillas de diapositiva
# ---------------------------------------------------------------------------
def portada(nombre, codigo, subtitulo="Tema 4 · Grafos no dirigidos"):
    s = Slide()
    s.text((W / 2, 250), codigo, size=26, color="gold", bold=True, anchor="mm")
    s.text((W / 2, 320), nombre, size=58, bold=True, anchor="mm")
    s.text((W / 2, 395), subtitulo, size=24, color="muted", anchor="mm")
    s.d.line((W / 2 - 140, 440, W / 2 + 140, 440), fill=C["gold"], width=3)
    return s


def ideas(title, items, corner=None, size=26, y=120, note=None):
    s = Slide(title, corner)
    yy = s.bullets(70, y, W - 140, items, size=size, gap=22)
    if note:
        s.box(70, max(yy + 10, 520), W - 140, 110, fill=(30, 52, 90), border="gold")
        s.wrap(96, max(yy + 10, 520) + 22, W - 200, note, size=24, color="text")
    return s


def cierre(nombre, puntos):
    s = Slide("Resumen", nombre)
    s.bullets(70, 130, W - 140, puntos, size=26, gap=24)
    return s
