"""
Vídeos ANIMADOS (desde los temas 8-11).

Igual que vidlib, pero cada segmento es una ESCENA que se dibuja fotograma a fotograma
(30 fps) en vez de una imagen fija. Así los objetos se mueven, cambian de color y aparecen
justo cuando la voz lo dice.

    Escena(narracion, dibuja, extra=0.5, titulo=None)

    dibuja(f) recibe un objeto Fotograma con:
        f.s      -> un vidlib.Slide nuevo (fondo ya pintado) sobre el que dibujar
        f.t      -> segundos desde el principio de la escena
        f.T      -> duración total de la escena
        f.c(k)   -> segundo en que EMPIEZA la frase k de la narración (0, 1, 2, ...)
        f.p(t0, d) -> progreso suavizado 0..1 entre t0 y t0 + d (para animar)
        f.lin(t0, d) -> lo mismo pero lineal

Cada escena se codifica en su propio mp4 (mismos ajustes en todas) y al final se juntan con
el concat demuxer sin recodificar; después se añaden la voz y los subtítulos.
"""
import os
import subprocess
import tempfile
import wave
from pathlib import Path

from PIL import Image

import vidlib
from vidlib import Slide, C, W, H, _split_sub, _texto_sub, _wrap2, _srt_time
import hashlib
import json
import shutil

_CACHE = Path(os.environ.get("TTS_CACHE", "/tmp/tts_cache"))


def _tts(texto, wav):
    """vidlib._tts con caché en disco (la misma frase no se sintetiza dos veces)."""
    clave = hashlib.md5((os.environ.get("KOKORO_VOICE", "") + texto).encode()).hexdigest()
    cw, cj = _CACHE / f"{clave}.wav", _CACHE / f"{clave}.json"
    if not (cw.exists() and cj.exists()):
        _CACHE.mkdir(parents=True, exist_ok=True)
        a, frases = vidlib._tts(texto, cw)
        cj.write_text(json.dumps([a, frases]))
    shutil.copy(cw, wav)
    a, frases = json.loads(cj.read_text())
    return a, [tuple(x) for x in frases]

FPS = 30


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def mix(c1, c2, u):
    c1 = C.get(c1, c1) if isinstance(c1, str) else c1
    c2 = C.get(c2, c2) if isinstance(c2, str) else c2
    u = max(0.0, min(1.0, u))
    return tuple(int(round(a + (b - a) * u)) for a, b in zip(c1, c2))


class Fotograma:
    def __init__(self, t, T, cues):
        self.t, self.T, self._cues = t, T, cues
        self.s = Slide()

    def c(self, k):
        if k < 0:
            k += len(self._cues)
        return self._cues[min(k, len(self._cues) - 1)] if self._cues else 0.0

    def p(self, t0, d=0.6):
        return ease((self.t - t0) / d) if d > 0 else float(self.t >= t0)

    def lin(self, t0, d):
        return max(0.0, min(1.0, (self.t - t0) / d)) if d > 0 else float(self.t >= t0)

    def __getattr__(self, k):            # atajos: f.d, f.img
        return getattr(self.s, k)


class Escena:
    def __init__(self, narracion, dibuja, extra=0.5, titulo=None, dmin=0):
        self.narracion, self.dibuja, self.extra, self.titulo, self.dmin = narracion, dibuja, extra, titulo, dmin


def _encoder(path):
    return subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", str(FPS), str(path)], stdin=subprocess.PIPE)


def preview(escenas, carpeta, tiempos=(0.5,), solo=None):
    """Dibuja fotogramas sueltos con los tiempos reales de la voz (sin codificar vídeo).
    tiempos: fracciones de la escena, 'fin', o ('c', k, dt) = dt segundos tras empezar la frase k."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="prev_"))
    for i, e in enumerate(escenas):
        if solo is not None and i not in solo:
            continue
        cues, T = [], max(e.dmin, 6.0)
        if e.narracion:
            a, frases = _tts(e.narracion, tmp / f"a{i}.wav")
            cues = [ini for _, ini, _ in frases]
            T = max(e.dmin, a + e.extra)
        lista = list(tiempos) + [("c", k, 1.5) for k in range(len(cues))]
        for j, tt in enumerate(lista):
            if tt == "fin":
                t = T - 0.05
            elif isinstance(tt, tuple):
                t = min(T - 0.05, cues[tt[1]] + tt[2])
            else:
                t = tt * T
            f = Fotograma(t, T, cues)
            e.dibuja(f)
            f.s.img.save(carpeta / f"e{i:02}_{j:02}.png")


def build(escenas, out_mp4, capitulos=True):
    out_mp4 = Path(out_mp4)
    tmp = Path(tempfile.mkdtemp(prefix="anim_"))
    trozos, audios, subs, caps = [], [], [], []
    t_global, sr = 0.0, 16000
    for i, e in enumerate(escenas):
        if e.titulo and capitulos:
            caps.append((t_global, e.titulo))
        cues, dur, wav = [], e.dmin, None
        if e.narracion:
            wav = tmp / f"a{i:03}.wav"
            a, frases = _tts(e.narracion, wav)
            with wave.open(str(wav), "rb") as wf:
                sr = wf.getframerate()
            cues = [ini for _, ini, _ in frases]
            dur = max(dur, a + e.extra)
            for fr, ini, fin in frases:
                chunks = _split_sub(_texto_sub(fr))
                total = sum(len(c) for c in chunks)
                tt = t_global + ini
                for c in chunks:
                    d = (fin - ini) * len(c) / total
                    subs.append((tt, tt + d, _wrap2(c)))
                    tt += d
        n = max(1, round(dur * FPS))
        dur = n / FPS
        tmpmp4 = tmp / f"v{i:03}.part.mp4"
        enc = _encoder(tmpmp4)
        for k in range(n):
            f = Fotograma(k / FPS, dur, cues)
            e.dibuja(f)
            enc.stdin.write(f.s.img.tobytes())
        enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg falló en la escena {i}")
        final = tmp / f"v{i:03}.mp4"
        tmpmp4.rename(final)
        trozos.append(final)
        audios.append((wav, dur))
        t_global += dur
        print(f"  escena {i + 1}/{len(escenas)}: {dur:.1f}s", flush=True)

    full = tmp / "audio.wav"
    with wave.open(str(full), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(sr)
        for wav, dur in audios:
            nm = int(round(dur * sr))
            data = b""
            if wav:
                with wave.open(str(wav), "rb") as wf:
                    data = wf.readframes(wf.getnframes())
            data = data[: nm * 2]
            out.writeframes(data + b"\x00\x00" * (nm - len(data) // 2))

    lst = tmp / "lista.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in trozos))
    srt = tmp / "subs.srt"
    with open(srt, "w", encoding="utf-8") as f:
        for k, (a, b, s) in enumerate(subs, 1):
            f.write(f"{k}\n{_srt_time(a)} --> {_srt_time(b)}\n{s}\n\n")
    meta = tmp / "meta.txt"
    with open(meta, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        for k, (a, tit) in enumerate(caps):
            b = caps[k + 1][0] if k + 1 < len(caps) else t_global
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a * 1000)}\nEND={int(b * 1000)}\ntitle={tit}\n")

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    tmpout = out_mp4.with_name(out_mp4.stem + ".part.mp4")
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-i", str(full), "-i", str(srt), "-i", str(meta),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map_chapters", "3",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-ar", "44100",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=spa",
        "-movflags", "+faststart", "-shortest", str(tmpout)], check=True)
    tmpout.rename(out_mp4)
    return t_global
