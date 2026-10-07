#!/usr/bin/env python3
"""
Construye la web del repositorio en sitio/_site/ (HTML estático, sin servidor).

    pip install markdown
    python3 sitio/construir.py

Qué usa (todo sale del propio repositorio, así que la web se actualiza sola):
  · README.md            -> tablas de cada tema (nº, título, PDF, solución, vídeo, idea)
  · EJ_0T-N/             -> carpetas de ejercicios no listadas en el README (se añaden igualmente)
  · EJ_*/README.md       -> explicación de cada ejercicio
  · Videos/*.mp4, Ejercicios juez/**.pdf, Estructuras de datos/*.h
  · Visualizaciones/*.html -> herramientas interactivas (se copian a herramientas/)

Solo se enlazan los ficheros que existen de verdad.
"""
import html, json, os, pathlib, posixpath, re, shutil, subprocess, sys
from datetime import datetime, timezone
from urllib.parse import quote, unquote

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("Falta el paquete 'markdown': pip install markdown")

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
OUT = AQUI / "_site"

TEMAS = {
    1: dict(nombre="Árboles AVL", resumen="Conjuntos sobre árboles binarios de búsqueda equilibrados: altura O(log n), rotaciones y k-ésimo elemento.", herr="tema1-avl.html", cab=["TreeSet_AVL_plantilla.h", "bintree.h"]),
    2: dict(nombre="Colas de prioridad", resumen="Montículo binario: siempre a mano el mínimo (o el máximo) con push y pop en O(log n).", herr="tema2-cola-prioridad.html", cab=["Pila.h"]),
    3: dict(nombre="Colas de prioridad variable (IndexPQ)", resumen="Montículo con tabla de posiciones para cambiar la prioridad de un elemento ya insertado.", herr="tema3-indexpq.html", cab=["IndexPQ.h"]),
    4: dict(nombre="Grafos no dirigidos", resumen="Listas de adyacencia, DFS para componentes y colores, BFS para distancias mínimas.", herr="tema4-grafo.html", cab=["Grafo.h"]),
    5: dict(nombre="Grafos dirigidos", resumen="Digrafos: BFS dirigido, orden topológico (postorden inverso) y detección de ciclos.", herr="tema5-digrafo.html", cab=["Digrafo.h"]),
}
HERRAMIENTAS = [
    ("tema1-avl.html", "Tema 1", "Árbol AVL", "Inserta, borra y pide el k-ésimo; mira el factor de equilibrio y cada rotación."),
    ("tema2-cola-prioridad.html", "Tema 2", "Cola de prioridad", "El montículo como árbol y como array: flotar, hundir y heapify."),
    ("tema3-indexpq.html", "Tema 3", "IndexPQ", "Montículo con tabla de posiciones y update paso a paso."),
    ("tema4-grafo.html", "Tema 4", "Grafo", "Construye un grafo y ejecuta DFS, BFS y bipartito sobre el código real."),
    ("tema5-digrafo.html", "Tema 5", "Digrafo", "BFS, orden topológico con ciclos e inverso() paso a paso."),
]
COPIAR = set()   # rutas relativas (posix) de ficheros del repo que hay que copiar a _site


def esc(s):
    return html.escape(str(s), quote=True)


def existe(rel):
    return (RAIZ / rel).is_file()


def href_sitio(rel, desde_ej=False):
    """Ruta del fichero en el sitio (mismo diseño de carpetas que el repo)."""
    COPIAR.add(rel)
    return ("../" if desde_ej else "") + quote(rel)


# ---------------------------------------------------------------- README
def celdas(linea):
    partes = [c.strip() for c in linea.strip().strip("|").split("|")]
    return partes


def enlaces(celda):
    return [(m.group(1), unquote(m.group(2))) for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", celda)]


def leer_readme():
    ej = []
    p = RAIZ / "README.md"
    if not p.exists():
        return ej
    tema = None
    for linea in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"##\s+Tema\s+(\d)\b", linea)
        if m:
            tema = int(m.group(1)); continue
        if linea.startswith("## "):
            tema = None; continue
        if tema is None or not linea.startswith("|"):
            continue
        c = celdas(linea)
        if len(c) < 6 or not re.match(r"^\d\d-\w+$", c[0]):
            continue
        e = dict(tema=tema, id=c[0], titulo=re.sub(r"`", "", c[1]), idea=c[5], pdf=None, sols=[], readme=None, video=None)
        for etq, ruta in enlaces(c[2]):
            if existe(ruta): e["pdf"] = ruta
        for etq, ruta in enlaces(c[3]):
            if not existe(ruta): continue
            if "Explicación" in etq: e["readme"] = ruta
            else: e["sols"].append((re.sub(r"^💻\s*", "", etq), ruta))
        for etq, ruta in enlaces(c[4]):
            if existe(ruta): e["video"] = ruta
        ej.append(e)
    return ej


def descubrir(ej):
    """Carpetas EJ_0T-N que no aparecen en el README."""
    conocidos = {s[1].split("/")[0] for e in ej for s in e["sols"]}
    for d in sorted(RAIZ.glob("EJ_0[1-9]-*")):
        if not d.is_dir() or d.name in conocidos:
            continue
        m = re.match(r"EJ_0(\d)-(\w+)", d.name)
        cpp = sorted(p for p in d.glob("*.cpp"))
        if not cpp:
            continue
        id_ = f"0{m.group(1)}-{m.group(2)}"
        v = sorted((RAIZ / "Videos").glob(f"{id_}_*.mp4"))
        ej.append(dict(tema=int(m.group(1)), id=id_, titulo=f"Ejercicio {id_}", idea="(añadido automáticamente: falta su fila en el README)",
                       pdf=None, sols=[("Solución", c.relative_to(RAIZ).as_posix()) for c in cpp],
                       readme=(d / "README.md").relative_to(RAIZ).as_posix() if (d / "README.md").exists() else None,
                       video=v[0].relative_to(RAIZ).as_posix() if v else None))
    return ej


# ---------------------------------------------------------------- páginas
CSS = """
:root{--bg:#f3f4f8;--panel:#fff;--panel2:#eceef4;--ink:#1a2133;--muted:#5d667b;--line:#d9deea;--accent:#b86e00;--accent-soft:#fbeccd;--blue:#1f6fb8;--blue-soft:#d9eafa;--green:#1e7f57;--green-soft:#d6f1e4;--code-bg:#121a2b;--code-ink:#dce4f5;--code-dim:#6f7b95;--kw:#ff79c6;--ty:#8be9fd;--nu:#bd93f9;--co:#7e8aa8;--st:#f1fa8c;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1424;--panel:#151d31;--panel2:#1c2640;--ink:#e7ecf7;--muted:#94a0ba;--line:#2a3556;--accent:#f5a623;--accent-soft:#3a2c0c;--blue:#58b2f2;--blue-soft:#14304a;--green:#4fd1a0;--green-soft:#123a2c;--code-bg:#0a0f1c;color-scheme:dark}}
:root[data-theme=dark]{--bg:#0e1424;--panel:#151d31;--panel2:#1c2640;--ink:#e7ecf7;--muted:#94a0ba;--line:#2a3556;--accent:#f5a623;--accent-soft:#3a2c0c;--blue:#58b2f2;--blue-soft:#14304a;--green:#4fd1a0;--green-soft:#123a2c;--code-bg:#0a0f1c;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55}
a{color:var(--blue)}code{font-family:var(--mono);font-size:.9em;background:var(--panel2);padding:1px 5px;border-radius:4px}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
.nav{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;gap:6px 14px;align-items:center;flex-wrap:wrap;padding-block:9px}
.nav b{font-family:var(--mono);font-size:.82rem;letter-spacing:.06em;margin-right:auto;white-space:nowrap}
.nav a{font-size:.88rem;text-decoration:none;color:var(--muted);padding:3px 8px;border-radius:6px}.nav a:hover{background:var(--panel2);color:var(--ink)}
.tag{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft);padding:3px 9px;border-radius:4px;display:inline-block}
.hero .tag,.ejhead .tag{align-self:flex-start}
.hero{padding-block:34px 18px;display:flex;flex-direction:column;gap:10px}
h1{font-size:clamp(1.7rem,4vw,2.5rem);line-height:1.15;letter-spacing:-.02em;margin:0;text-wrap:balance}
h2{font-size:1.45rem;margin:0 0 4px;letter-spacing:-.01em}.lede{color:var(--muted);max-width:68ch;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:8px 22px;font-family:var(--mono);font-size:.85rem;color:var(--muted)}.stats b{color:var(--ink);font-size:1.15rem}
.search{font:inherit;width:100%;max-width:420px;padding:9px 12px;border:1px solid var(--line);border-radius:9px;background:var(--panel);color:var(--ink)}
section.bloque{padding-block:22px 6px}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin-top:12px}
a.tool{display:flex;flex-direction:column;gap:4px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:inherit}
a.tool:hover{border-color:var(--accent)}a.tool .n{font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}a.tool b{font-size:1.05rem}a.tool span.d{font-size:.86rem;color:var(--muted)}
.tema{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin-top:14px}
.tema header{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:baseline;justify-content:space-between;margin-bottom:8px}
.tema header p{margin:0;color:var(--muted);flex-basis:100%;max-width:70ch;font-size:.92rem}
.lista{display:flex;flex-direction:column}
.fila{display:grid;grid-template-columns:3.6rem minmax(0,1.3fr) minmax(0,1.7fr) auto;gap:4px 14px;align-items:center;padding:9px 2px;border-top:1px solid var(--line)}
.fila .id{font-family:var(--mono);font-weight:600;color:var(--accent)}.fila .t a{font-weight:600;color:var(--ink);text-decoration:none}.fila .t a:hover{color:var(--blue)}
.fila .i{color:var(--muted);font-size:.88rem}.chips{display:flex;flex-wrap:wrap;gap:5px;justify-content:flex-end}
.chip{font-size:.78rem;padding:2px 9px;border-radius:999px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);text-decoration:none;white-space:nowrap}.chip:hover{border-color:var(--blue);color:var(--blue)}
.chip.v{background:var(--green-soft);border-color:var(--green);color:var(--green)}.chip.p{background:var(--blue-soft);border-color:var(--blue);color:var(--blue)}
@media(max-width:760px){.fila{grid-template-columns:3.2rem minmax(0,1fr)}.fila .i{grid-column:2}.chips{grid-column:1/-1;justify-content:flex-start}}
.cabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
footer{color:var(--muted);font-size:.82rem;padding-block:30px 40px}
.vacio{display:none;color:var(--muted);padding:20px 0}
/* página de ejercicio */
.ejhead{padding-block:22px 8px;display:flex;flex-direction:column;gap:8px}.ejhead .acc{display:flex;flex-wrap:wrap;gap:8px}
.btn{font:inherit;font-size:.9rem;font-weight:500;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:7px 13px;text-decoration:none;cursor:pointer;display:inline-block}
.btn:hover{border-color:var(--blue)}.btn.on{background:var(--accent);border-color:var(--accent);color:#fff}
:root[data-theme=dark] .btn.on{color:#1b1400}@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .btn.on{color:#1b1400}}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 12px}.pane{display:none}.pane.on{display:block}
.md{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:6px 20px 16px;overflow-x:auto}.md h1{font-size:1.5rem;margin-top:16px}.md h2{font-size:1.2rem;margin-top:20px}
.md pre{background:var(--code-bg);color:var(--code-ink);padding:12px 14px;border-radius:10px;overflow-x:auto;font-size:12.5px;line-height:1.5}.md pre code{background:none;padding:0;color:inherit}
.md table{border-collapse:collapse;font-size:.9rem}.md th,.md td{border-bottom:1px solid var(--line);padding:5px 9px;text-align:left}
.codebox{background:var(--code-bg);color:var(--code-ink);border-radius:10px;padding:10px 0;overflow-x:auto;font-family:var(--mono);font-size:12.5px;line-height:1.55}
.codebox .fname{padding:0 14px 6px;color:var(--code-dim);font-size:11.5px;display:flex;gap:12px;align-items:center}.codebox .fname button{margin-left:auto}
.ln{display:flex;white-space:pre;padding-right:14px}.ln i{font-style:normal;width:3em;text-align:right;padding-right:12px;color:var(--code-dim);flex:none;user-select:none}
.k{color:var(--kw)}.t{color:var(--ty)}.n{color:var(--nu)}.c{color:var(--co)}.s{color:var(--st)}
.sub{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
video{width:100%;max-width:960px;border-radius:10px;background:#000}iframe.pdf{width:100%;height:78vh;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
.herr{margin-top:12px}
"""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">'

HIGHLIGHT_JS = r"""
const KW=/^(for|if|else|while|return|const|class|struct|public|private|protected|void|bool|int|long|double|char|auto|true|false|template|typename|using|namespace|throw|new|delete|break|continue|static|nullptr|include|define|ifndef|endif|inline|unsigned|operator|switch|case|default|do)$/;
const TY=/^(Set|Grafo|Digrafo|IndexPQ|Par|vector|queue|stack|string|priority_queue|pair|map|set|cin|cout|endl|std|Adys|size_t|BinTree|Pila|istream|ostream)$/;
const TOK=/(\/\/.*$)|(\/\*[\s\S]*?\*\/)|("[^"]*")|(#\w+)|(\b\d+\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)/g;
function esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function paint(src){let h='',m;TOK.lastIndex=0;while((m=TOK.exec(src))){const t=m[0];
 if(m[1]||m[2])h+='<span class="c">'+esc(t)+'</span>';else if(m[3])h+='<span class="s">'+esc(t)+'</span>';else if(m[4])h+='<span class="k">'+esc(t)+'</span>';
 else if(m[5])h+='<span class="n">'+t+'</span>';else if(m[6]&&KW.test(t))h+='<span class="k">'+t+'</span>';else if(m[6]&&TY.test(t))h+='<span class="t">'+t+'</span>';else h+=esc(t)}return h}
document.querySelectorAll('pre[data-code]').forEach(pre=>{
 const name=pre.dataset.code,src=pre.textContent.replace(/\n$/,'');
 const box=document.createElement('div');box.className='codebox';
 const head=document.createElement('div');head.className='fname';head.innerHTML='<span>'+esc(name)+'</span>';
 const b=document.createElement('button');b.className='btn';b.textContent='Copiar';b.onclick=()=>{(navigator.clipboard?navigator.clipboard.writeText(src):Promise.reject()).then(()=>{b.textContent='¡Copiado!';setTimeout(()=>b.textContent='Copiar',1500)}).catch(()=>{const r=document.createRange();r.selectNodeContents(box);getSelection().removeAllRanges();getSelection().addRange(r)})};
 head.appendChild(b);box.appendChild(head);
 src.split('\n').forEach((l,i)=>{const d=document.createElement('div');d.className='ln';d.innerHTML='<i>'+(i+1)+'</i><span>'+paint(l)+'</span>';box.appendChild(d)});
 pre.replaceWith(box)});
"""

TABS_JS = r"""
function show(id){document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id===id));document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('on',b.dataset.tab===id));
 document.querySelectorAll('.sub-pane').forEach(p=>{});}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{show(b.dataset.tab);try{history.replaceState(null,'','#'+b.dataset.tab)}catch(e){}});
document.querySelectorAll('[data-sub]').forEach(b=>b.onclick=()=>{const g=b.dataset.group;document.querySelectorAll('[data-group="'+g+'"]').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-subpane^="'+g+'"]').forEach(p=>p.style.display=p.dataset.subpane===b.dataset.sub?'block':'none')});
const h=location.hash.slice(1);show(document.getElementById(h)?h:document.querySelector('.pane').id);
"""


def pagina(titulo, cuerpo, prefijo="", extra_js="", desc=""):
    nav = (f'<nav class="nav"><div class="wrap"><b>DA · DISEÑO DE ALGORITMOS</b>'
           f'<a href="{prefijo}index.html">Inicio</a><a href="{prefijo}index.html#herramientas">Herramientas</a>'
           + "".join(f'<a href="{prefijo}index.html#tema{t}">Tema {t}</a>' for t in TEMAS)
           + f'<a href="{prefijo}index.html#estructuras">Estructuras</a></div></nav>')
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}">{FONTS}<style>{CSS}</style></head><body>{nav}{cuerpo}<script>{extra_js}</script></body></html>')


def render_md(ruta_rel):
    base = posixpath.dirname(ruta_rel)
    txt = (RAIZ / ruta_rel).read_text(encoding="utf-8")
    h = markdown.markdown(txt, extensions=["tables", "fenced_code"])

    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|data:)", val):
            return m.group(0)
        rel = posixpath.normpath(posixpath.join(base, unquote(val.split("#")[0])))
        if rel.startswith("..") or not existe(rel):
            return m.group(0)
        return f'{attr}="{href_sitio(rel, True)}"'
    h = re.sub(r'(href|src)="([^"]+)"', fix, h)
    # el bloque ```text ... ``` -> <pre><code>; se deja tal cual
    return h


def pagina_ejercicio(e, slug):
    carpeta = None
    for _, r in e["sols"]:
        carpeta = posixpath.dirname(r); break
    # ficheros de código: soluciones del README + .h de la carpeta
    codigos = []
    vistos = set()
    for etq, r in e["sols"]:
        if r.endswith((".cpp", ".h")) and r not in vistos:
            codigos.append((etq, r)); vistos.add(r)
    if carpeta:
        for p in sorted((RAIZ / carpeta).glob("*.h")):
            r = p.relative_to(RAIZ).as_posix()
            if r not in vistos:
                codigos.append((p.name, r)); vistos.add(r)
    tab = []; panes = []
    acc = []
    herr = TEMAS[e["tema"]]["herr"]
    if e["pdf"]:
        acc.append(f'<a class="btn" href="{href_sitio(e["pdf"], True)}">📄 Enunciado (PDF)</a>')
    if e["video"]:
        acc.append(f'<a class="btn" href="#video">🎬 Vídeo</a>')
    if (RAIZ / "Visualizaciones" / herr).exists():
        acc.append(f'<a class="btn" href="../herramientas/{herr}">🧩 Herramienta interactiva</a>')
    if e["readme"]:
        tab.append(("explicacion", "📘 Explicación"))
        panes.append(f'<div class="pane" id="explicacion"><div class="md">{render_md(e["readme"])}</div></div>')
    if codigos:
        tab.append(("codigo", "💻 Código"))
        subs = "".join(f'<button class="btn{" on" if i == 0 else ""}" data-sub="c{i}" data-group="c">{esc(posixpath.basename(r))}</button>' for i, (_, r) in enumerate(codigos))
        cods = "".join(
            f'<div data-subpane="c{i}" style="display:{"block" if i == 0 else "none"}"><pre data-code="{esc(posixpath.basename(r))}">{esc((RAIZ / r).read_text(encoding="utf-8", errors="replace"))}</pre></div>'
            for i, (_, r) in enumerate(codigos))
        panes.append(f'<div class="pane" id="codigo"><div class="sub">{subs if len(codigos) > 1 else ""}</div>{cods}</div>')
    if e["pdf"]:
        tab.append(("enunciado", "📄 Enunciado"))
        panes.append(f'<div class="pane" id="enunciado"><iframe class="pdf" src="{href_sitio(e["pdf"], True)}" title="Enunciado"></iframe><p class="i" style="color:var(--muted)">¿No se ve? <a href="{href_sitio(e["pdf"], True)}">Abre el PDF</a>.</p></div>')
    if e["video"]:
        tab.append(("video", "🎬 Vídeo"))
        panes.append(f'<div class="pane" id="video"><video controls preload="metadata" src="{href_sitio(e["video"], True)}"></video></div>')
    if not panes:
        tab.append(("vacio", "Sin contenido")); panes.append('<div class="pane" id="vacio"><p>Todavía no hay material para este ejercicio.</p></div>')
    cuerpo = (f'<div class="wrap"><div class="ejhead"><span class="tag">Tema {e["tema"]} · {esc(TEMAS[e["tema"]]["nombre"])}</span>'
              f'<h1>{esc(e["id"])} · {esc(e["titulo"])}</h1><p class="lede">{esc(e["idea"])}</p><div class="acc">{"".join(acc)}</div></div>'
              f'<div class="tabs">{"".join(f"<button class=btn data-tab={i}>{esc(t)}</button>" for i, t in tab)}</div>{"".join(panes)}</div>')
    return pagina(f'{e["id"]} {e["titulo"]}', cuerpo, "../", HIGHLIGHT_JS + TABS_JS, e["idea"])


def pagina_cabecera(nombre):
    rel = f"Estructuras de datos/{nombre}"
    herr = next((TEMAS[t]["herr"] for t in TEMAS if nombre in TEMAS[t]["cab"]), None)
    extra = f'<a class="btn" href="../herramientas/{herr}">🧩 Herramienta interactiva</a>' if herr and (RAIZ / "Visualizaciones" / herr).exists() else ""
    cuerpo = (f'<div class="wrap"><div class="ejhead"><span class="tag">Estructura de datos</span><h1>{esc(nombre)}</h1>'
              f'<div class="acc"><a class="btn" href="{href_sitio(rel, True)}" download>⬇ Descargar</a>{extra}</div></div>'
              f'<pre data-code="{esc(nombre)}">{esc((RAIZ / rel).read_text(encoding="utf-8", errors="replace"))}</pre></div>')
    return pagina(nombre, cuerpo, "../", HIGHLIGHT_JS)


def chips(e, slug):
    c = []
    if e["pdf"]: c.append(f'<a class="chip p" href="{href_sitio(e["pdf"])}">PDF</a>')
    c.append(f'<a class="chip" href="ej/{slug}.html#codigo">Código</a>' if e["sols"] else "")
    if e["readme"]: c.append(f'<a class="chip" href="ej/{slug}.html#explicacion">Explicación</a>')
    if e["video"]: c.append(f'<a class="chip v" href="ej/{slug}.html#video">Vídeo</a>')
    return "".join(c)


def commit_info():
    sha = os.environ.get("GITHUB_SHA") or ""
    if not sha:
        try:
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        except Exception:
            sha = ""
    return sha[:7]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "ej").mkdir(parents=True); (OUT / "estructuras").mkdir()
    ej = descubrir(leer_readme())
    ej.sort(key=lambda e: (e["tema"], e["id"].replace("-L", "-99")))
    slugs, usados = {}, set()
    for i, e in enumerate(ej):
        s = e["id"].lower(); n = 2
        while s in usados:
            s = f'{e["id"].lower()}-{n}'; n += 1
        usados.add(s); slugs[i] = s
        (OUT / "ej" / f"{s}.html").write_text(pagina_ejercicio(e, s), encoding="utf-8")

    # estructuras de datos
    dir_est = RAIZ / "Estructuras de datos"
    cabs = sorted(p.name for p in dir_est.glob("*.h")) if dir_est.exists() else []
    for c in cabs:
        (OUT / "estructuras" / f"{c}.html").write_text(pagina_cabecera(c), encoding="utf-8")

    # herramientas
    herr_dir = RAIZ / "Visualizaciones"
    herr = [h for h in HERRAMIENTAS if (herr_dir / h[0]).exists()]
    if herr_dir.exists():
        (OUT / "herramientas").mkdir()
        for p in herr_dir.glob("*.html"):
            shutil.copy2(p, OUT / "herramientas" / p.name)

    # portada
    n_pdf = sum(1 for e in ej if e["pdf"]); n_vid = sum(1 for e in ej if e["video"]); n_sol = sum(1 for e in ej if e["sols"])
    tema_html = []
    for t, info in TEMAS.items():
        filas = []
        for i, e in enumerate(ej):
            if e["tema"] != t: continue
            busq = esc(f'{e["id"]} {e["titulo"]} {e["idea"]}'.lower())
            filas.append(f'<div class="fila" data-q="{busq}"><span class="id">{esc(e["id"])}</span><span class="t"><a href="ej/{slugs[i]}.html">{esc(e["titulo"])}</a></span>'
                         f'<span class="i">{md_inline(e["idea"])}</span><span class="chips">{chips(e, slugs[i])}</span></div>')
        if not filas: continue
        h = (f'<a class="chip" href="herramientas/{info["herr"]}">🧩 Herramienta interactiva</a>' if info["herr"] in [x[0] for x in herr] else "")
        tema_html.append(f'<section class="tema" id="tema{t}"><header><h2>Tema {t} · {esc(info["nombre"])}</h2>{h}<p>{esc(info["resumen"])}</p></header><div class="lista">{"".join(filas)}</div></section>')
    tools_html = "".join(f'<a class="tool" href="herramientas/{f}"><span class="n">{esc(a)}</span><b>{esc(b)}</b><span class="d">{esc(c)}</span></a>' for f, a, b, c in herr)
    est_html = "".join(f'<a class="chip" href="estructuras/{quote(c)}.html">{esc(c)}</a>' for c in cabs)
    sha = commit_info()
    ahora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    cuerpo = f"""<div class="wrap">
<div class="hero"><span class="tag">Universidad Complutense · Ingeniería Informática</span>
<h1>Diseño de Algoritmos: ejercicios, soluciones y herramientas</h1>
<p class="lede">Todos los problemas del juez con su enunciado, la solución en C++, la explicación del planteamiento, un vídeo paso a paso y herramientas interactivas para entender cada estructura de datos.</p>
<div class="stats"><span><b>{len(ej)}</b> ejercicios</span><span><b>{n_sol}</b> con solución</span><span><b>{n_pdf}</b> enunciados</span><span><b>{n_vid}</b> vídeos</span><span><b>{len(herr)}</b> herramientas</span></div>
<input class="search" id="q" type="search" placeholder="Buscar ejercicio (nombre, número, técnica…)" aria-label="Buscar ejercicio"></div>
<section class="bloque" id="herramientas"><h2>Herramientas interactivas</h2><p class="lede">Ejecutan la misma lógica que el C++ de la asignatura y resaltan el código línea a línea.</p><div class="tools">{tools_html}</div></section>
<div id="temas">{"".join(tema_html)}<p class="vacio" id="vacio">Ningún ejercicio coincide con la búsqueda.</p></div>
<section class="bloque" id="estructuras"><h2>Estructuras de datos</h2><p class="lede">Las cabeceras que da la asignatura, con visor de código.</p><div class="cabs">{est_html}</div></section>
<footer>Web generada automáticamente desde el repositorio{" · commit <code>" + esc(sha) + "</code>" if sha else ""} · {ahora}</footer></div>"""
    js = """const q=document.getElementById('q');q.oninput=()=>{const v=q.value.trim().toLowerCase();let any=0;
document.querySelectorAll('.tema').forEach(s=>{let vis=0;s.querySelectorAll('.fila').forEach(f=>{const ok=!v||f.dataset.q.includes(v);f.style.display=ok?'':'none';if(ok)vis++});s.style.display=vis?'':'none';any+=vis});
document.getElementById('vacio').style.display=any?'none':'block'}"""
    (OUT / "index.html").write_text(pagina("DA · Diseño de Algoritmos", cuerpo, "", js, "Ejercicios, soluciones, vídeos y herramientas interactivas de Diseño de Algoritmos"), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")

    # copiar ficheros referenciados + código de cada ejercicio
    for e in ej:
        if e["sols"]:
            for p in (RAIZ / posixpath.dirname(e["sols"][0][1])).glob("*"):
                if p.suffix in (".cpp", ".h"):
                    COPIAR.add(p.relative_to(RAIZ).as_posix())
    for c in cabs:
        COPIAR.add(f"Estructuras de datos/{c}")
    for rel in sorted(COPIAR):
        if existe(rel):
            d = OUT / rel; d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(RAIZ / rel, d)
    print(f"ok: {len(ej)} ejercicios, {n_vid} vídeos, {n_pdf} PDFs, {len(herr)} herramientas, {len(cabs)} cabeceras -> {OUT}")


def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


if __name__ == "__main__":
    main()
