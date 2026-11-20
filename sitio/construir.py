#!/usr/bin/env python3
"""
Construye la web del repositorio en sitio/_site/ (HTML estático, sin servidor).

    pip install markdown
    python3 sitio/construir.py

Qué usa (todo sale del propio repositorio, así que la web se actualiza sola):
  · README.md            -> tablas de cada tema (nº, título, PDF, solución, vídeo, idea)
  · <tema>/EJ_0T-N/     -> carpetas de ejercicios no listadas en el README (se añaden igualmente)
  · <tema>/EJ_*/README.md -> explicación de cada ejercicio
  · Videos/*.mp4, <tema>/Enunciados/*.pdf, Estructuras de datos/*.h
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
    6: dict(nombre="Conjuntos disjuntos y grafos valorados", resumen="Particiones que solo se unen, grafos con valores en las aristas y árbol de recubrimiento de coste mínimo (Kruskal y Prim).", herr="tema6-kruskal.html", cab=["ConjuntosDisjuntos.h", "GrafoValorado.h"]),
    7: dict(nombre="Dígrafos valorados y caminos mínimos", resumen="Dígrafos con costes en las aristas y el algoritmo de Dijkstra: distancias mínimas, contar caminos y reconstruir rutas.", herr="tema7-dijkstra.html", cab=["DigrafoValorado.h", "IndexPQ.h"]),
    8: dict(nombre="Algoritmos voraces", resumen="Elegir en cada paso lo que parece mejor sin volver atrás: intervalos, emparejamientos y por qué la elección es óptima.", herr="", cab=[]),
    9: dict(nombre="Algoritmos voraces II", resumen="Más voraces: pinchar y cubrir intervalos, emparejar extremos de un vector ordenado y voraces sobre Dijkstra.", herr="", cab=[]),
    10: dict(nombre="Programación dinámica", resumen="Recurrencias con subproblemas repetidos rellenadas en tablas: mochila, cambio de monedas y caminos en cuadrículas.", herr="", cab=[]),
    11: dict(nombre="Programación dinámica II", resumen="Programación dinámica con reconstrucción de la solución: mochila 0/1 y palíndromos sobre intervalos.", herr="", cab=[]),
    12: dict(nombre="Problemas de evaluación", resumen="Problemas de evaluación de la asignatura.", herr="", cab=[]),
}
HERRAMIENTAS = [
    ("tema1-avl.html", "Tema 1", "Árbol AVL", "Inserta, borra y pide el k-ésimo; mira el factor de equilibrio y cada rotación."),
    ("tema2-cola-prioridad.html", "Tema 2", "Cola de prioridad", "El montículo como árbol y como array: flotar, hundir y heapify."),
    ("tema3-indexpq.html", "Tema 3", "IndexPQ", "Montículo con tabla de posiciones y update paso a paso."),
    ("tema4-grafo.html", "Tema 4", "Grafo", "Construye un grafo y ejecuta DFS, BFS y bipartito sobre el código real."),
    ("tema5-digrafo.html", "Tema 5", "Digrafo", "BFS, orden topológico con ciclos e inverso() paso a paso."),
    ("tema6-kruskal.html", "Tema 6", "Conjuntos disjuntos y ARM", "Las cuatro implementaciones de conjuntos disjuntos y Kruskal / Prim paso a paso."),
    ("tema7-dijkstra.html", "Tema 7", "Dijkstra", "Relajación de aristas, Dijkstra con cola y con vector, ulti[] y contar caminos mínimos."),
]
ESTILO = AQUI / "estilo"
ESTILO_BASE = (ESTILO / "apuntes.css").read_text(encoding="utf-8")
TEMA_INI = (ESTILO / "tema-inicial.js").read_text(encoding="utf-8")
TEMA_JS = (ESTILO / "apuntes.js").read_text(encoding="utf-8")
SPRITE = (ESTILO / "iconos.html").read_text(encoding="utf-8")
ICON_RE = re.compile(r"@@i:(\w+)@@")
GLIFOS = {"📄": "pdf", "💻": "code", "🧩": "tool", "🔗": "link", "📥": "download", "🎬": "video", "📘": "book", "⚠": "warn", "⬇": "download", "↗": "external"}
GLIFO_RE = re.compile("(" + "|".join(GLIFOS) + ")\ufe0f?")
PALETAS = (ESTILO / "paletas.css").read_text(encoding="utf-8")
GLOSSY = (ESTILO / "glossy.css").read_text(encoding="utf-8")
DA_CSS = (ESTILO / "da.css").read_text(encoding="utf-8")
PROGRESO_JS = (ESTILO / "progreso.js").read_text(encoding="utf-8")
PORTAL_URL = os.environ.get("PORTAL_URL", "https://studia-one-flax.vercel.app")   # URL del portal; si está vacía no se enseña el enlace
BLOQUES = [("Estructuras de datos", [1, 2, 3], "var(--s1)"), ("Grafos", [4, 5, 6, 7], "var(--s2)"), ("Algoritmos voraces", [8, 9], "var(--s3)"),
           ("Programación dinámica", [10, 11], "var(--s4)"), ("Evaluación", [12], "var(--muted)")]
DECO = ('<div class="deco" aria-hidden="true"><svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice"><defs>'
        '<linearGradient id="dg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c5cff" stop-opacity=".55"/><stop offset="1" stop-color="#4f6bff" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="dg2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6d5cff" stop-opacity=".5"/><stop offset="1" stop-color="#2a3cff" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="dg3" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3b6bff" stop-opacity=".28"/><stop offset="1" stop-color="#3b6bff" stop-opacity="0"/></radialGradient></defs>'
        '<path d="M0 0H470C360 130 190 150 0 380Z" fill="url(#dg1)"/><path d="M1440 0V760C1330 540 1220 300 1010 0Z" fill="url(#dg2)"/>'
        '<ellipse cx="260" cy="860" rx="520" ry="260" fill="url(#dg3)"/>'
        '<path d="M0 560C260 520 420 640 640 900" fill="none" stroke="#9a8cff" stroke-opacity=".09" stroke-width="2"/>'
        '<path d="M820 0C980 180 1200 220 1440 300" fill="none" stroke="#9a8cff" stroke-opacity=".08" stroke-width="2"/></svg></div>')
SITE_URL = os.environ.get("SITE_URL", "https://studia-one-flax.vercel.app").rstrip("/")   # dominio donde vive la web (StudIA); DA cuelga de «/da/»
BASE_DA = SITE_URL + "/da/"
MEDIA_BASE = os.environ.get("MEDIA_BASE", "")   # si se indica (p. ej. https://juanp-g.github.io/DA/), los vídeos se sirven desde ahí en vez de pasar por el proxy
PAGINAS = []   # rutas de todas las páginas, para el sitemap
COPIAR = set()   # rutas relativas (posix) de ficheros del repo que hay que copiar a _site


def _icono(m):
    return f'<svg class="i" aria-hidden="true"><use href="#i-{m.group(1)}"/></svg>'


def es_teoria(e):
    return re.search(r"-0$", e["id"]) is not None


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
        m = re.match(r"##\s+Tema\s+(\d+)\b", linea)
        if m:
            tema = int(m.group(1)); continue
        if linea.startswith("## "):
            tema = None; continue
        if tema is None or not linea.startswith("|"):
            continue
        c = celdas(linea)
        if len(c) < 6 or not re.match(r"^(\d\d|Eval)-\w+$", c[0]):
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
    conocidos = {posixpath.dirname(s[1]) for e in ej for s in e["sols"]}
    for d in sorted(RAIZ.glob("[0-9]*-*/EJ_*")):   # <tema>/EJ_TT-N
        if not d.is_dir() or d.relative_to(RAIZ).as_posix() in conocidos:
            continue
        m = re.match(r"EJ_(\d\d|Eval)-(\w+)$", d.name)
        mt = re.match(r"(\d+)-", d.parent.name)
        cpp = sorted(p for p in d.glob("*.cpp"))
        if not m or not mt or int(mt.group(1)) not in TEMAS or not cpp:
            continue
        id_ = f"{m.group(1)}-{m.group(2)}"
        v = sorted((RAIZ / "Videos").glob(f"{id_}_*.mp4"))
        ej.append(dict(tema=int(mt.group(1)), id=id_, titulo=f"Ejercicio {id_}", idea="(añadido automáticamente: falta su fila en el README)",
                       pdf=None, sols=[("Solución", c.relative_to(RAIZ).as_posix()) for c in cpp],
                       readme=(d / "README.md").relative_to(RAIZ).as_posix() if (d / "README.md").exists() else None,
                       video=v[0].relative_to(RAIZ).as_posix() if v else None))
    return ej


# ---------------------------------------------------------------- páginas
CSS_VIEJO = """
body{font-size:15px;line-height:1.55}
.tag{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft);padding:3px 9px;border-radius:4px;display:inline-block}
.hero .tag,.ejhead .tag{align-self:flex-start}
.hero{padding-block:34px 18px;display:flex;flex-direction:column;gap:10px}
h1{font-size:clamp(1.7rem,4vw,2.5rem);letter-spacing:-.02em}
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
.btn:hover{border-color:var(--blue)}.btn.on,.btn.prim{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
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
.crumbs{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:.86rem;color:var(--muted);padding-top:16px}
.crumbs a{color:var(--muted);text-decoration:none}.crumbs a:hover{color:var(--blue)}.crumbs .back{font-weight:600;color:var(--ink);margin-right:6px}
.tabs .btn .cnt{font-size:.75rem;color:var(--muted);margin-left:4px}.tabs .btn.off{opacity:.55}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}.bar .grow{flex:1}
.bar .hint{font-size:.85rem;color:var(--muted)}
.acr{background:var(--green-soft);border:1px solid var(--line);border-left:4px solid var(--green);border-radius:10px;padding:10px 14px;margin:0 0 12px;font-size:.92rem;line-height:1.5}.acr.rel{background:var(--blue-soft);border-left-color:var(--blue)}.acr b{display:block;margin-bottom:2px}.acr a{font-weight:600}
.nada{background:var(--panel);border:1px dashed var(--line);border-radius:12px;padding:26px;color:var(--muted);text-align:center}
.vid{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:14px;align-items:start}@media(max-width:860px){.vid{grid-template-columns:minmax(0,1fr)}}
.caps{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px;max-height:60vh;overflow:auto}
.caps b{display:block;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:2px 4px 6px}
.caps button{all:unset;display:flex;gap:10px;width:100%;box-sizing:border-box;padding:6px 8px;border-radius:8px;cursor:pointer;font-size:.9rem}
.caps button:hover,.caps button.on{background:var(--panel2)}.caps button span{font-family:var(--mono);color:var(--accent);font-size:.82rem}
.pager{display:flex;justify-content:space-between;gap:10px;margin-top:22px;flex-wrap:wrap}
.vlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:12px}
a.vcard{display:flex;flex-direction:column;gap:4px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:inherit}
a.vcard:hover{border-color:var(--green)}a.vcard .n{font-family:var(--mono);font-size:.75rem;color:var(--green)}a.vcard .d{font-size:.84rem;color:var(--muted)}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:8px 14px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .2s;pointer-events:none}.toast.on{opacity:1}
"""
CSS = ESTILO_BASE + PALETAS + GLOSSY + CSS_VIEJO + DA_CSS
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800&display=swap">'

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
 const box=document.createElement('div');box.className='codebox';if(pre.id)box.id=pre.id;box.dataset.src=src;
 const head=document.createElement('div');head.className='fname';head.innerHTML='<span>'+esc(name)+'</span>';
 box.appendChild(head);
 src.split('\n').forEach((l,i)=>{const d=document.createElement('div');d.className='ln';d.innerHTML='<i>'+(i+1)+'</i><span>'+paint(l)+'</span>';box.appendChild(d)});
 pre.replaceWith(box)});
"""

COMUN_JS = r"""
function toast(t){const e=document.getElementById('toast');if(!e)return;e.textContent=t;e.classList.add('on');clearTimeout(e._t);e._t=setTimeout(()=>e.classList.remove('on'),1600)}
function copiar(txt,btn){const ok=()=>{toast('Copiado al portapapeles');if(btn){const o=btn.innerHTML;btn.textContent='¡Copiado!';setTimeout(()=>btn.innerHTML=o,1400)}};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(ok).catch(()=>viejo())}else viejo();
 function viejo(){const t=document.createElement('textarea');t.value=txt;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();try{document.execCommand('copy');ok()}catch(e){toast('No se ha podido copiar')}t.remove()}}
// «Volver»: si se llegó desde esta misma web, vuelve exactamente a donde estabas; si no, a la página indicada
document.querySelectorAll('[data-back]').forEach(a=>a.addEventListener('click',ev=>{
 let mismo=false;try{mismo=document.referrer&&new URL(document.referrer).origin===location.origin&&history.length>1}catch(e){}
 if(mismo){ev.preventDefault();history.back()}}));
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{const el=document.getElementById(b.dataset.copy);copiar(el.dataset.src!==undefined?el.dataset.src:el.textContent,b)}));
"""

TABS_JS = r"""
// Pestañas: cada una tiene su #ancla. Cambiar de pestaña no llena el historial (replaceState),
// así que «Atrás» del navegador te devuelve a la página anterior y no a la pestaña anterior.
function show(id,scroll){if(!document.getElementById('p-'+id))return;
 document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id==='p-'+id));
 document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('on',b.dataset.tab===id));
 document.querySelectorAll('.pane:not(.on) video').forEach(v=>v.pause());
 if(scroll)document.querySelector('.tabs').scrollIntoView({block:'start'})}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{show(b.dataset.tab);try{history.replaceState(null,'','#'+b.dataset.tab)}catch(e){}});
document.querySelectorAll('[data-sub]').forEach(b=>b.onclick=()=>{const g=b.dataset.group;document.querySelectorAll('[data-group="'+g+'"]').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-subpane^="'+g+'"]').forEach(p=>p.style.display=p.dataset.subpane===b.dataset.sub?'block':'none')});
window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
const ini=location.hash.slice(1);show(document.getElementById('p-'+ini)?ini:(document.querySelector('[data-tab].pref')||document.querySelector('[data-tab]')).dataset.tab);
// capítulos del vídeo
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{const v=document.querySelector('#p-video video');v.currentTime=+b.dataset.t;v.play()});
const vv=document.querySelector('#p-video video');if(vv){vv.addEventListener('timeupdate',()=>{let cur=null;document.querySelectorAll('[data-t]').forEach(b=>{if(+b.dataset.t<=vv.currentTime+0.3)cur=b});document.querySelectorAll('[data-t]').forEach(b=>b.classList.toggle('on',b===cur))})}
// «Descargar todo»: zip generado en el navegador con los ficheros del ejercicio
const zb=document.getElementById('zip');
if(zb)zb.onclick=async()=>{const lista=JSON.parse(zb.dataset.files),nombre=zb.dataset.name;
 if(typeof JSZip==='undefined'){toast('No se ha podido cargar el compresor; descarga los ficheros por separado');return}
 const z=new JSZip(),txt=zb.innerHTML;zb.disabled=true;
 try{let i=0;for(const [url,ruta] of lista){zb.textContent='Preparando… '+(++i)+'/'+lista.length;const r=await fetch(url);if(!r.ok)throw new Error(url);z.file(nombre+'/'+ruta,await r.blob(),{binary:true})}
  zb.textContent='Comprimiendo…';const blob=await z.generateAsync({type:'blob',compression:'STORE'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=nombre+'.zip';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},2000);toast('Descarga lista')}
 catch(e){toast('No se ha podido generar el zip')}finally{zb.disabled=false;zb.innerHTML=txt}};
"""

KATEX = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" '
         'onload="renderMathInElement(document.body,{delimiters:[{left:\'\\\\[\',right:\'\\\\]\',display:true},'
         '{left:\'\\\\(\',right:\'\\\\)\',display:false}]})"></script>'
         '<style>.math{overflow-x:auto;overflow-y:hidden;padding:.2em 0}</style>')
JSZIP = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js" defer></script>'


def pagina(titulo, cuerpo, prefijo="", extra_js="", desc="", head="", ruta=None):
    portal = f'<a href="{esc(PORTAL_URL)}/#asignaturas">Asignaturas</a>' if PORTAL_URL else ""
    nav = (f'<header class="nav"><div class="nav-pill"><a class="brand" href="{prefijo}index.html" aria-label="Diseño de Algoritmos, inicio"><img src="{prefijo}estilo/marca/mark.png" alt="" width="201" height="242"><b>StudIA</b><span class="subj">DA</span></a>'
           f'<nav aria-label="Principal">{portal}<a class="keep" href="{prefijo}index.html#temas">Temas</a><a href="{prefijo}index.html#herramientas">Herramientas</a>'
           f'<a href="{prefijo}index.html#estructuras">Estructuras</a><a class="keep" href="{prefijo}videos.html">Vídeos</a></nav>'
           f'<button id="tema" class="icon-btn" type="button" aria-label="Cambiar tema claro/oscuro"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg></button></div></header>')
    iconos = (f'<link rel="icon" href="{prefijo}estilo/marca/favicon.ico" sizes="any"><link rel="icon" href="{prefijo}estilo/marca/favicon-32.png" type="image/png" sizes="32x32">'
              f'<link rel="apple-touch-icon" href="{prefijo}estilo/marca/apple-touch-icon.png"><meta name="theme-color" content="#080a1c">')
    seo = ""
    if ruta is not None:
        PAGINAS.append(ruta)
        canon = BASE_DA + quote(ruta)
        seo = (f'<link rel="canonical" href="{esc(canon)}"><meta property="og:type" content="website"><meta property="og:site_name" content="StudIA"><meta property="og:locale" content="es_ES">'
               f'<meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(canon)}">'
               f'<meta property="og:image" content="{SITE_URL}/assets/marca/og.png"><meta name="twitter:card" content="summary_large_image">')
    pag = (f'<!doctype html><html lang="es" data-paleta="premium" data-estilo="glossy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}">{iconos}{seo}{FONTS}<script>{TEMA_INI}</script><style>{CSS}</style>{head}{KATEX if 'class="math"' in cuerpo else ""}</head><body>{DECO}{SPRITE}{nav}{cuerpo}<div class="toast" id="toast"></div><script>{TEMA_JS}{COMUN_JS}{PROGRESO_JS}{extra_js}</script></body></html>')
    pag = GLIFO_RE.sub(lambda m: f'@@i:{GLIFOS[m.group(1)]}@@', pag)
    return ICON_RE.sub(_icono, pag)


def limpiar_readme(txt):
    """Quita lo que la página del ejercicio ya muestra por su cuenta: título, fila Enunciado/Solución/Vídeo y caja de Acepta el Reto."""
    txt = re.sub(r"<!--\s*acr:inicio\s*-->.*?<!--\s*acr:fin\s*-->\n?", "", txt, flags=re.S)
    txt = re.sub(r"\A\s*# [^\n]*\n", "", txt, count=1)
    lineas = txt.split("\n")
    for i, l in enumerate(lineas[:8]):   # la fila es «📄 [Enunciado](…) · 💻 [Solución](…) · 🎬 [Vídeo](…)»: solo enlaces
        if re.match(r"^\s*[^\w\s\[]*\s*\[(Enunciado|Soluci[oó]n|V[ií]deo)[^\]]*\]\(", l, re.I):
            del lineas[i]
            break
    return "\n".join(lineas).lstrip("\n")


def render_md(ruta_rel):
    base = posixpath.dirname(ruta_rel)
    txt = limpiar_readme((RAIZ / ruta_rel).read_text(encoding="utf-8"))
    # fórmulas: $$...$$ (bloque) y $...$ (en línea) se apartan antes de markdown y las pinta KaTeX
    formulas = []

    def guarda(m, bloque):
        formulas.append((bloque, m.group(1)))
        return f"@@FORMULA{len(formulas) - 1}@@"
    txt = re.sub(r"\$\$(.+?)\$\$", lambda m: guarda(m, True), txt, flags=re.S)
    txt = re.sub(r"(?<![\\$])\$([^$\n]+?)\$", lambda m: guarda(m, False), txt)
    h = markdown.markdown(txt, extensions=["tables", "fenced_code"])

    def pon(m):
        bloque, f = formulas[int(m.group(1))]
        return (f'<div class="math">\\[{esc(f)}\\]</div>' if bloque else f'<span class="math">\\({esc(f)}\\)</span>')
    h = re.sub(r"<p>@@FORMULA(\d+)@@</p>", pon, h)
    h = re.sub(r"@@FORMULA(\d+)@@", pon, h)

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


def leer_texto(rel):
    """Lee un fuente en UTF-8 o, si lo guardó así Visual Studio, en Windows-1252."""
    b = (RAIZ / rel).read_bytes()
    try:
        return b.decode("utf-8-sig")
    except UnicodeDecodeError:
        return b.decode("cp1252", errors="replace")


def tam_legible(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}".replace(".", ",")
        n /= 1024


def media_video(rel):
    """Subtítulos (.vtt) y capítulos del mp4, si hay ffmpeg/ffprobe. Devuelve (ruta_vtt|None, [(seg, título)])."""
    vtt, caps = None, []
    src = RAIZ / rel
    destino = OUT / (rel[:-4] + ".vtt")
    if shutil.which("ffmpeg"):
        destino.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map", "0:s:0", str(destino)], capture_output=True)
        if r.returncode == 0 and destino.exists() and destino.stat().st_size > 10:
            vtt = rel[:-4] + ".vtt"
    if shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-of", "json", str(src)], capture_output=True, text=True)
        try:
            caps = [(float(c["start_time"]), c.get("tags", {}).get("title", "")) for c in json.loads(r.stdout).get("chapters", [])]
        except Exception:
            caps = []
    return vtt, caps


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02}"


def descargar(rel, texto, extra=""):
    return f'<a class="btn" href="{href_sitio(rel, True)}" download="{esc(posixpath.basename(rel))}"{extra}>{texto}</a>'


ACR_ETQ = {"igual": "Mismo problema", "parecido": "Casi el mismo problema", "relacionado": "Problema relacionado (misma técnica)"}


def cargar_acepta():
    """Equivalentes en Acepta el Reto (herramientas/acepta_el_reto.json)."""
    p = RAIZ / "herramientas" / "acepta_el_reto.json"
    if not p.exists():
        return []
    try:
        return [x for x in json.loads(p.read_text(encoding="utf-8"))["ejercicios"] if x.get("tipo") != "ninguno"]
    except (ValueError, KeyError):
        return []


ACEPTA = cargar_acepta()


def acepta_de(e):
    for x in ACEPTA:
        if x["id"] == e["id"] and (not x.get("titulo_contiene") or x["titulo_contiene"].lower() in e["titulo"].lower()):
            return x
    return None


def acepta_url(x):
    return f"https://aceptaelreto.com/problem/statement.php?id={x['num']}"


sys.path.insert(0, str(RAIZ / "herramientas"))
try:
    from para_acepta import EJERCICIOS as ACR_GENERADOS   # qué problemas tienen versión lista para enviar
except Exception:                                           # la web no debe romperse por esto
    ACR_GENERADOS = {}


def acepta_fichero(x, e):
    """Ruta (relativa al repo) de la versión lista para enviar de este ejercicio, si existe."""
    g = ACR_GENERADOS.get(x["num"])
    if not g or x["tipo"] == "relacionado" or not e["sols"] or posixpath.dirname(g["fuente"]) != posixpath.dirname(e["sols"][0][1]):
        return None
    rel = f"Acepta el Reto/ACR-{x['num']}_{g['slug']}.cpp"
    return rel if existe(rel) else None


def acepta_caja(x, fichero=None):
    cab = "Para practicar lo mismo en Acepta el Reto" if x["tipo"] == "relacionado" else "Pruébalo en Acepta el Reto, sin necesidad del juez de la asignatura"
    envio = ""
    if fichero:
        txt = leer_texto(fichero)
        envio = (f'<div class="bar" style="margin:8px 0 0"><button class="btn prim" data-copy="acr-src">@@i:copy@@ Copiar código para Acepta el Reto</button>'
                 f'{descargar(fichero, "@@i:download@@ Descargar " + esc(posixpath.basename(fichero)))}'
                 f'<span class="hint">un solo fichero, con las cabeceras dentro y su formato de entrada · {txt.count(chr(10)) + 1} líneas</span></div>'
                 f'<script type="text/plain" id="acr-src">{esc(txt)}</script>')
    return (f'<div class="acr{" rel" if x["tipo"] == "relacionado" else ""}"><b>@@i:link@@ {cab}</b>'
            f'<a href="{acepta_url(x)}" target="_blank" rel="noopener">#{x["num"]} · {esc(x["problema"])} ↗</a> · {ACR_ETQ[x["tipo"]]}. {esc(x.get("nota", ""))}{envio}</div>')


def pagina_ejercicio(e, slug, ant=None, sig=None):
    carpeta = posixpath.dirname(e["sols"][0][1]) if e["sols"] else (posixpath.dirname(e["readme"]) if e["readme"] else None)   # sin código aún: la carpeta del README
    # código: soluciones del README + .h de la carpeta
    codigos, vistos = [], set()
    for etq, r in e["sols"]:
        if r.endswith((".cpp", ".h")) and r not in vistos:
            codigos.append(r); vistos.add(r)
    if carpeta and carpeta != "Estructuras de datos":
        candidatos = sorted((RAIZ / carpeta).glob("*.h"))
    elif carpeta:   # ficheros sueltos de «Estructuras de datos» (05-0): solo las cabeceras que incluyen
        incl = set()
        for r in list(codigos):
            incl |= set(re.findall(r'#include\s+"([^"]+)"', leer_texto(r)))
        candidatos = sorted(RAIZ / carpeta / h for h in incl if (RAIZ / carpeta / h).exists())
    else:
        candidatos = []
    for p in candidatos:
        r = p.relative_to(RAIZ).as_posix()
        if r not in vistos:
            codigos.append(r); vistos.add(r)
    herr = TEMAS[e["tema"]]["herr"]
    tema = e["tema"]
    ficheros_zip = []   # (url relativa a la página, ruta dentro del zip)

    acr = acepta_de(e)
    # 1 · Enunciado
    if e["pdf"]:
        pdf = href_sitio(e["pdf"], True)
        p_enun = (f'<div class="bar">{descargar(e["pdf"], "@@i:download@@ Descargar PDF")}<a class="btn" href="{pdf}" target="_blank" rel="noopener">@@i:external@@ Abrir en otra pestaña</a>'
                  f'<span class="hint">{tam_legible((RAIZ / e["pdf"]).stat().st_size)}</span></div>'
                  f'<iframe class="pdf" src="{pdf}" title="Enunciado {esc(e["id"])}"></iframe>'
                  f'<p class="hint" style="color:var(--muted);font-size:.85rem">¿No se ve? En el móvil los PDF no se muestran dentro de la página: usa «Abrir en otra pestaña» o «Descargar PDF».</p>')
        ficheros_zip.append((pdf, "enunciado.pdf"))
    else:
        p_enun = '<div class="nada">Este ejercicio no tiene enunciado en PDF.</div>'

    acr_fich = acepta_fichero(acr, e) if acr else None
    if acr:
        p_enun = acepta_caja(acr, acr_fich) + p_enun
        if acr_fich:
            ficheros_zip.append((href_sitio(acr_fich, True), "acepta_el_reto/" + posixpath.basename(acr_fich)))

    # 2 · Código
    if codigos:
        subs = "".join(f'<button class="btn{" on" if i == 0 else ""}" data-sub="c{i}" data-group="c">{esc(posixpath.basename(r))}</button>' for i, r in enumerate(codigos))
        cods = []
        for i, r in enumerate(codigos):
            txt = leer_texto(r)
            nombre = posixpath.basename(r)
            tipo = "solución" if r.endswith(".cpp") else "estructura de datos"
            cods.append(f'<div data-subpane="c{i}" style="display:{"block" if i == 0 else "none"}"><div class="bar"><button class="btn" data-copy="src{i}">@@i:copy@@ Copiar código</button>'
                        f'{descargar(r, "@@i:download@@ Descargar " + esc(nombre))}<span class="hint">{tipo} · {txt.count(chr(10)) + 1} líneas</span></div>'
                        f'<pre data-code="{esc(nombre)}" id="src{i}">{esc(txt)}</pre></div>')
            ficheros_zip.append((href_sitio(r, True), ("codigo/" if r.endswith(".cpp") else "estructuras/") + nombre))
        p_cod = f'<div class="sub">{subs if len(codigos) > 1 else ""}</div>{"".join(cods)}'
    else:
        p_cod = '<div class="nada">Todavía no hay código para este ejercicio.</div>'

    # 3 · Explicación
    if e["readme"]:
        crudo = (RAIZ / e["readme"]).read_text(encoding="utf-8")
        p_exp = (f'<div class="bar"><button class="btn" data-copy="md-src">@@i:copy@@ Copiar (Markdown)</button>{descargar(e["readme"], "@@i:download@@ Descargar .md", "")}</div>'
                 f'<div class="md">{render_md(e["readme"])}</div><script type="text/plain" id="md-src">{esc(crudo)}</script>')
        ficheros_zip.append((href_sitio(e["readme"], True), "explicacion.md"))
    else:
        p_exp = '<div class="nada">Todavía no hay explicación escrita para este ejercicio.</div>'

    # 4 · Vídeo
    if e["video"]:
        vurl = href_sitio(e["video"], True)
        if MEDIA_BASE:
            vurl = MEDIA_BASE + quote(e["video"])
        vtt, caps = media_video(e["video"])
        track = f'<track kind="subtitles" srclang="es" label="Español" src="{(MEDIA_BASE + quote(vtt)) if MEDIA_BASE else "../" + quote(vtt)}">' if vtt else ""
        lista_caps = ("<div class='caps'><b>Capítulos</b>" + "".join(f'<button data-t="{t:.2f}"><span>{mmss(t)}</span>{esc(ti)}</button>' for t, ti in caps) + "</div>") if caps else ""
        p_vid = (f'<div class="bar">{descargar(e["video"], "@@i:download@@ Descargar vídeo")}<span class="hint">{tam_legible((RAIZ / e["video"]).stat().st_size)} · subtítulos con el botón CC del reproductor</span></div>'
                 f'<div class="{"vid" if caps else ""}"><video controls preload="metadata" playsinline{" crossorigin=anonymous" if MEDIA_BASE else ""} src="{vurl}">{track}Tu navegador no puede reproducir el vídeo: <a href="{vurl}">descárgalo</a>.</video>{lista_caps}</div>')
        ficheros_zip.append((vurl, "video.mp4"))
    else:
        p_vid = '<div class="nada">Este ejercicio todavía no tiene vídeo.</div>'

    tabs = [("enunciado", "@@i:pdf@@ Enunciado", bool(e["pdf"]), p_enun), ("video", "@@i:video@@ Vídeo", bool(e["video"]), p_vid),
            ("explicacion", "@@i:book@@ Explicación", bool(e["readme"]), p_exp), ("codigo", "@@i:code@@ Código", bool(codigos), p_cod)]
    hay_juez = slug in JUECES
    if hay_juez:
        p_juez = (f'<div class="dj-host" data-manifest="../juez/{slug}/manifest.json" '
                  f'data-wasm="{esc(os.environ.get("JUEZ_WASM_BASE", "https://binji.github.io/wasm-clang/"))}" '
                  f'data-servidor="{esc(os.environ.get("JUEZ_SERVIDOR", ""))}"><p class="hint">Cargando el juez…</p></div>')
        tabs.append(("probar", "@@i:check@@ Probar", True, p_juez))
    pref = "video" if e["video"] else ("explicacion" if e["readme"] else ("codigo" if codigos else "enunciado"))
    botones = "".join(f'<button class="btn{"" if hay else " off"}{" pref" if i == pref else ""}" data-tab="{i}">{t}</button>' for i, t, hay, _ in tabs)
    panes = "".join(f'<div class="pane" id="p-{i}">{c}</div>' for i, _, _, c in tabs)

    acc = []   # extras discretos, a la derecha de las pestañas
    if acr:
        acc.append(f'<a class="xl" href="{acepta_url(acr)}" target="_blank" rel="noopener">@@i:link@@ Acepta el Reto #{acr["num"]}</a>')
    if herr and (RAIZ / "Visualizaciones" / herr).exists():
        acc.append(f'<a class="xl" href="../herramientas/{herr}">@@i:tool@@ Herramienta del tema</a>')
    contenido_zip = ", ".join(x for x, ok in (("enunciado", e["pdf"]), ("código", codigos), ("explicación", e["readme"]), ("vídeo", e["video"]), ("versión para Acepta el Reto", acr_fich)) if ok)

    if ficheros_zip:
        acc.append(f'<button class="xl" id="zip" data-name="{esc(e["id"] + " " + e["titulo"])}" data-files="{esc(json.dumps(ficheros_zip, ensure_ascii=False))}" title="El zip incluye: {esc(contenido_zip)}">@@i:download@@ Descargar todo .zip</button>')
    pager = '<div class="pager">' + (f'<a class="btn" href="{ant[0]}.html">← {esc(ant[1])}</a>' if ant else "<span></span>") + \
            (f'<a class="btn" href="{sig[0]}.html">{esc(sig[1])} →</a>' if sig else "<span></span>") + "</div>"
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../tema/{tema}.html" data-back>← Volver</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../tema/{tema}.html">Tema {tema}</a>›<span>{esc(e["id"])}</span></div>'
              f'<div class="ejhead"><a class="tag" href="../tema/{tema}.html">Tema {tema} · {esc(TEMAS[tema]["nombre"])}</a>'
              f'<div class="ejtit"><h1>{esc(e["id"])} · {esc(e["titulo"])}</h1>'
              f'<button class="btn okb-ej" data-ok="{slug}" aria-pressed="false">@@i:check@@ <span class="lab">Marcar como hecho</span></button></div>'
              f'<p class="lede">{md_inline(e["idea"])}</p>'
              f'</div><div class="tabsbar"><div class="tabs">{botones}</div><div class="xls">{"".join(acc)}</div></div>{panes}{pager}</div>{teoria_panel(tema, "../")}')
    return pagina(f'{e["id"]} {e["titulo"]} | Diseño de Algoritmos UCM', cuerpo, "../",
                  HIGHLIGHT_JS + TABS_JS + (TEORIA_JS if TEORIA.get(tema) else "") + (JUEZ_JS if hay_juez else ""), e["idea"],
                  JSZIP + ('<link rel="stylesheet" href="../juez/juez.css">' if hay_juez else ""), ruta=f"ej/{slug}.html")


def pagina_cabecera(nombre):
    rel = f"Estructuras de datos/{nombre}"
    herr = next((TEMAS[t]["herr"] for t in TEMAS if nombre in TEMAS[t]["cab"]), None)
    extra = f'<a class="btn" href="../herramientas/{herr}">@@i:tool@@ Herramienta interactiva</a>' if herr and (RAIZ / "Visualizaciones" / herr).exists() else ""
    txt = leer_texto(rel)
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../index.html#estructuras" data-back>← Volver</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../index.html#estructuras">Estructuras</a>›<span>{esc(nombre)}</span></div>'
              f'<div class="ejhead"><span class="tag">Estructura de datos</span><h1>{esc(nombre)}</h1>'
              f'<div class="acc"><button class="btn" data-copy="src0">@@i:copy@@ Copiar código</button>{descargar(rel, "@@i:download@@ Descargar " + esc(nombre))}{extra}</div></div>'
              f'<pre data-code="{esc(nombre)}" id="src0">{esc(txt)}</pre></div>')
    return pagina(f"{nombre} | Estructuras de datos de DA", cuerpo, "../", HIGHLIGHT_JS, f"Código de {nombre}, la cabecera de la asignatura de Diseño de Algoritmos, con visor, copiar y descargar.", ruta=f"estructuras/{nombre}.html")


def pagina_videos(ej, slugs):
    bloques = []
    for t, info in TEMAS.items():
        cards = []
        for i, e in enumerate(ej):
            if e["tema"] == t and e["video"]:
                mb = tam_legible((RAIZ / e["video"]).stat().st_size)
                cards.append(f'<a class="vcard" href="ej/{slugs[i]}.html#video"><span class="n">▶ {esc(e["id"])} · {mb}</span><b>{esc(e["titulo"])}</b><span class="d">{md_inline(e["idea"])}</span></a>')
        if cards:
            bloques.append(f'<section class="bloque"><h2>Tema {t} · {esc(info["nombre"])}</h2><div class="vlist">{"".join(cards)}</div></section>')
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="index.html" data-back>← Volver</a><a href="index.html">Inicio</a>›<span>Vídeos</span></div>'
              f'<div class="hero"><span class="tag">Vídeos</span><h1>Vídeos explicativos</h1><p class="lede">Se ven aquí mismo, con subtítulos y, en los largos, capítulos. Cada uno abre la página de su ejercicio, donde también se puede descargar.</p></div>'
              f'{"".join(bloques)}</div>')
    return pagina("Vídeos de Diseño de Algoritmos UCM | StudIA", cuerpo, "", "", "Vídeos paso a paso de todos los ejercicios de Diseño de Algoritmos de la FDI UCM, con subtítulos.", ruta="videos.html")


VOLVER_HERR = ('<a href="../index.html#herramientas" onclick="try{if(document.referrer&&new URL(document.referrer).origin===location.origin&&history.length>1){history.back();return false}}catch(e){}" '
               'style="position:fixed;left:12px;bottom:12px;z-index:99;font:600 14px system-ui,sans-serif;background:#151d31;color:#e7ecf7;border:1px solid #2a3556;'
               'padding:9px 16px;border-radius:999px;text-decoration:none;box-shadow:0 8px 22px rgba(0,0,0,.35)">← Volver a la web</a>')


def chips(e, slug, pre=""):
    """Accesos rápidos de la fila: iconos con etiqueta accesible (en móvil y escritorio)."""
    c = []
    def mk(cls, icono, etq, ancla):
        c.append(f'<a class="mi {cls}" href="{pre}ej/{slug}.html#{ancla}" title="{etq}" aria-label="{etq}">@@i:{icono}@@<span>{etq}</span></a>')
    if e["pdf"]: mk("", "pdf", "Enunciado", "enunciado")
    if e["sols"]: mk("", "code", "Código", "codigo")
    if e["readme"]: mk("", "book", "Explicación", "explicacion")
    if e["video"]: mk("v", "video", "Vídeo", "video")
    return "".join(c)


def color_de(t):
    for _, ts, col in BLOQUES:
        if t in ts:
            return col
    return "var(--muted)"


def plural(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


def tarjeta_tema(t, info, lista, slugs, hay_herr):
    """Tarjeta de la portada: soluciones disponibles, progreso personal (lo pinta progreso.js) y tests."""
    teo = [x for x in lista if es_teoria(x[1])]
    lista = [x for x in lista if not es_teoria(x[1])]
    n = len(lista)
    n_sol = sum(1 for _, e in lista if e["sols"]); n_vid = sum(1 for _, e in lista if e["video"])
    ids = ",".join(slugs[i] for i, _ in lista)
    pct_sol = round(n_sol / n * 100) if n else 0
    herr = '<span class="chip">@@i:tool@@ Herramienta</span>' if hay_herr else ""
    herr += '<span class="chip p">@@i:book@@ Teoría</span>' if teo else ""
    vid = f'<span class="chip v">@@i:video@@ {plural(n_vid, "vídeo", "vídeos")}</span>' if n_vid else ""
    return (f'<a class="tcard" href="tema/{t}.html" data-ids="{ids}" data-tema="{t}" style="--b:{color_de(t)}">'
            f'<div class="th"><div><span class="n">{t:02d}</span><b>{esc(info["nombre"])}</b></div><span class="est" data-est>Sin empezar</span></div>'
            f'<div class="met"><div class="sol"><div class="l"><span>Con solución</span><b>{n_sol}/{n}</b></div><div class="prog"><i style="width:{pct_sol}%"></i></div></div>'
            f'<div><div class="l"><span>Tu progreso</span><b data-txt>0/{n} · 0%</b></div><div class="prog"><i data-bar></i></div></div></div>'
            f'<div class="tcf"><span class="chip">@@i:code@@ {plural(n, "ejercicio", "ejercicios")}</span>{herr}{vid}<span class="chip mute">@@i:check@@ Tests pronto</span></div></a>')


FILTRO_JS = r"""
(function(){var f={f:'todos',v:false};
function hechos(){try{return JSON.parse(localStorage.getItem('studia-da-hechos')||'{}')}catch(e){return{}}}
function ap(){var h=hechos(),filas=document.querySelectorAll('#p-ejercicios .exr'),vis=0;
 filas.forEach(function(r){var b=r.querySelector('[data-ok]');if(!b){r.style.display='';return}var k=b.dataset.ok,d=!!h[k];var ok=(f.f==='todos'||(f.f==='hechos'?d:!d))&&(!f.v||r.dataset.v==='1');r.style.display=ok?'':'none';if(ok)vis++});
 var n=document.getElementById('sin');if(n)n.style.display=vis?'none':'block'}
document.querySelectorAll('[data-f]').forEach(function(b){b.onclick=function(){f.f=b.dataset.f;document.querySelectorAll('[data-f]').forEach(function(x){x.classList.toggle('on',x===b)});ap()}});
var fv=document.querySelector('[data-fv]');if(fv)fv.onclick=function(){f.v=!f.v;fv.classList.toggle('on',f.v);ap()};
(function(){var d=document.querySelector('[data-aprende]');if(d&&window.innerWidth>960)d.open=true})();
document.querySelectorAll('[data-vt]').forEach(function(b){b.onclick=function(){var v=document.querySelector('.vhero video');v.currentTime=+b.dataset.vt;v.play()}});
(function(){var v=document.querySelector('.vhero video');if(!v)return;v.addEventListener('timeupdate',function(){var cur=null,bs=document.querySelectorAll('[data-vt]');bs.forEach(function(b){if(+b.dataset.vt<=v.currentTime+.3)cur=b});bs.forEach(function(b){b.classList.toggle('on',b===cur)})})})();
function sig(){var a=document.querySelector('[data-sig]');if(!a)return;var h=hechos(),n=null,hay=false;
 document.querySelectorAll('#p-ejercicios .exr [data-ok]').forEach(function(b){hay=hay||!!h[b.dataset.ok];if(!n&&!h[b.dataset.ok])n=b.closest('.exr')});
 if(!n){a.textContent='¡Tema completado!';a.removeAttribute('href');return}
 a.href=n.querySelector('.t a').getAttribute('href');a.textContent=(hay?'Continuar con ':'Empezar con ')+n.querySelector('.id').textContent+' →'}
document.addEventListener('click',function(){setTimeout(function(){ap();sig()},0)});window.addEventListener('storage',function(){ap();sig()});window.addEventListener('pageshow',function(){ap();sig()});ap();sig()})();
"""



# ---------- Teoría en PDF (carpeta Teoria/ del repo) ----------
def teoria_pdfs():
    """{tema: [(ruta_relativa, nombre_legible, bytes)]}. El tema sale del primer número
    de la ruta (Teoria/tema6/Kruskal.pdf, Teoria/6/..., Teoria/Tema6_Kruskal.pdf)."""
    res = {}
    base = RAIZ / "Teoria"
    if not base.is_dir():
        return res
    for f in sorted(base.rglob("*.pdf"), key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", x.name)]):
        rel = f.relative_to(base)
        m = re.search(r"(\d+)", "/".join(rel.parts[:-1])) or re.search(r"(\d+)", rel.name)
        if not m:
            continue
        nombre = re.sub(r"^((tema\s*)?\d+\s*[-_.:]*\s*)", "", f.stem, flags=re.I).replace("_", " ").strip() or f.stem
        res.setdefault(int(m.group(1)), []).append((f.relative_to(RAIZ).as_posix(), nombre, f.stat().st_size))
    return res

TEORIA = {}

def url_teoria(t, rel, prefijo):
    return f'{prefijo}teoria/{t}/{quote(posixpath.basename(rel))}'

def teoria_cards(t, prefijo):
    docs = TEORIA.get(t)
    if not docs:
        return ""
    cards = "".join(
        f'<div class="pcard"><span class="pic">@@i:pdf@@</span><div><b>{esc(n)}</b><small>PDF · {tam_legible(b)}</small></div>'
        f'<div class="acc"><button class="btn primary" type="button" data-teo="{i}">@@i:book@@ Abrir aquí</button>'
        f'<a class="btn" href="{url_teoria(t, r, prefijo)}" download>@@i:download@@ Descargar</a></div></div>'
        for i, (r, n, b) in enumerate(docs))
    return f'<section class="teoria-bloque" aria-label="Teoría del tema"><h2>Teoría del tema</h2><div class="pcards">{cards}</div></section>'

def teoria_panel(t, prefijo):
    """Botón flotante + panel lateral con visor PDF; disponible en el tema y en cada ejercicio."""
    docs = TEORIA.get(t)
    if not docs:
        return ""
    opts = "".join(f'<option value="{esc(url_teoria(t, r, prefijo))}">{esc(n)}</option>' for r, n, b in docs)
    return (f'<button class="btn primary teo-fab" type="button" id="teoAbrir" aria-controls="teoPanel" aria-expanded="false">@@i:book@@ Teoría</button>'
            f'<aside class="teo-panel" id="teoPanel" aria-label="Teoría del tema {t}" hidden><div class="teo-bar"><b>Teoría · Tema {t}</b>'
            f'<select id="teoSel" aria-label="Documento">{opts}</select>'
            f'<a class="btn mini" id="teoTab" target="_blank" rel="noopener" href="#">Abrir en pestaña</a>'
            f'<button class="btn mini" type="button" id="teoCerrar">Cerrar</button></div>'
            f'<iframe id="teoFrame" title="Visor de PDF" loading="lazy"></iframe></aside>')

TEORIA_JS = r"""
(function(){var b=document.getElementById('teoAbrir');if(!b)return;
var P=document.getElementById('teoPanel'),S=document.getElementById('teoSel'),F=document.getElementById('teoFrame'),T=document.getElementById('teoTab');
function key(){return 'studia-da-teoria-'+location.pathname.replace(/[^0-9]/g,'').slice(0,0)+(document.title.match(/Tema (\d+)/)||[0,''])[1]}
function cargar(){F.src=S.value+'#view=FitH';T.href=S.value}
function abrir(i){if(typeof i==='number')S.selectedIndex=i;P.hidden=false;document.body.classList.add('teo-on');b.setAttribute('aria-expanded','true');cargar();try{localStorage.setItem('studia-da-teo-open','1')}catch(e){}}
function cerrar(){P.hidden=true;document.body.classList.remove('teo-on');b.setAttribute('aria-expanded','false');F.removeAttribute('src');try{localStorage.removeItem('studia-da-teo-open')}catch(e){}}
b.onclick=function(){P.hidden?abrir():cerrar()};
document.getElementById('teoCerrar').onclick=cerrar;S.onchange=cargar;
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!P.hidden)cerrar()});
document.querySelectorAll('[data-teo]').forEach(function(x){x.onclick=function(){abrir(+x.dataset.teo)}});
})();
"""


def pagina_tema(t, info, lista, slugs, cabs, herr_ok, nombres_temas):
    color = color_de(t)
    teo = [x for x in lista if es_teoria(x[1])]
    lista = [x for x in lista if not es_teoria(x[1])]
    n = len(lista)
    n_sol = sum(1 for _, e in lista if e["sols"])
    ids = ",".join(slugs[i] for i, _ in lista)
    filas = []
    for i, e in lista:
        s_ = slugs[i]
        filas.append(f'<div class="exr" data-v="{1 if e["video"] else 0}" style="--c:{color}"><button class="okb" data-ok="{s_}" aria-label="Marcar {esc(e["id"])} como hecho" aria-pressed="false">@@i:check@@</button>'
                     f'<span class="id">{esc(e["id"])}</span><span class="t"><a href="../ej/{s_}.html">{esc(e["titulo"])}</a>'
                     f'<span class="idea">{md_inline(e["idea"])}</span></span><span class="chips">{chips(e, s_, "../")}</span></div>')
    acc = []
    if herr_ok:
        acc.append(f'<a class="btn" href="../herramientas/{info["herr"]}">@@i:tool@@ Herramienta interactiva</a>')
    for c in info["cab"]:
        if c in cabs:
            acc.append(f'<a class="btn" href="../estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>')
    bloque = next((b[0] for b in BLOQUES if t in b[1]), "")
    prev_t = t - 1 if t - 1 in nombres_temas else None
    next_t = t + 1 if t + 1 in nombres_temas else None
    pager = ('<div class="pager">' + (f'<a class="btn" href="{prev_t}.html">← Tema {prev_t} · {esc(nombres_temas[prev_t])}</a>' if prev_t else "<span></span>")
             + (f'<a class="btn" href="{next_t}.html">Tema {next_t} · {esc(nombres_temas[next_t])} →</a>' if next_t else "<span></span>") + "</div>")
    # --- Vídeo del tema: lo más útil para entender el tema, va arriba del todo ---
    vhero = ""
    tv = next((e for _, e in teo if e["video"]), None)
    if tv:
        vurl = (MEDIA_BASE + quote(tv["video"])) if MEDIA_BASE else "../" + quote(tv["video"])
        vtt, caps = media_video(tv["video"])
        track = f'<track kind="subtitles" srclang="es" label="Español" src="{(MEDIA_BASE + quote(vtt)) if MEDIA_BASE else "../" + quote(vtt)}">' if vtt else ""
        lista_caps = ("<div class='vcaps'><b>Capítulos</b>" + "".join(f'<button type="button" data-vt="{t:.2f}"><span>{mmss(t)}</span>{esc(ti)}</button>' for t, ti in caps) + "</div>") if caps else ""
        vhero = (f'<section class="vhero" id="video-tema" aria-label="Vídeo del tema"><div class="vh"><span class="vtag">@@i:video@@ Empieza por aquí</span><h2>Vídeo del tema</h2>'
                 f'</div>'
                 f'<div class="vbody{" conc" if caps else ""}"><video controls preload="metadata" playsinline{" crossorigin=anonymous" if MEDIA_BASE else ""} src="{vurl}">{track}Tu navegador no puede reproducir el vídeo: <a href="{vurl}">descárgalo</a>.</video>{lista_caps}</div></section>')
    # --- Barra lateral: progreso, aprender (teoría, vídeo, herramienta) y recursos ---
    docs = TEORIA.get(t) or []
    principales, pdfs = [], []
    for i, e in teo:
        s_ = slugs[i]
        principales.append(f'<a class="arow main" href="../ej/{s_}.html"><span class="pic">@@i:book@@</span><span class="at"><b>Apuntes del tema</b><small>Explicación escrita paso a paso</small></span>@@i:arrow@@</a>')
    if herr_ok:
        principales.append(f'<a class="arow main" href="../herramientas/{info["herr"]}"><span class="pic">@@i:tool@@</span><span class="at"><b>Herramienta interactiva</b><small>Pruébalo paso a paso</small></span>@@i:arrow@@</a>')
    for k, (r, nom, tam) in enumerate(docs):
        pdfs.append(f'<div class="arow"><span class="pic">@@i:pdf@@</span><span class="at"><b>{esc(nom)}</b><small>PDF · {tam_legible(tam)}</small></span>'
                    f'<button class="mb" type="button" data-teo="{k}" title="Abrir aquí" aria-label="Abrir {esc(nom)} aquí">@@i:book@@</button>'
                    f'<a class="mb" href="{url_teoria(t, r, "../")}" download title="Descargar" aria-label="Descargar {esc(nom)}">@@i:download@@</a></div>')
    aprender = principales + pdfs
    recursos = [f'<a class="chip" href="../estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>' for c in info["cab"] if c in cabs]
    lateral = (f'<aside class="tside">'
               f'<div class="sbox prog-box" data-ids="{ids}" style="--c:{color}"><div class="ph"><small>Tu progreso</small><b data-pct>0%</b></div><div class="prog"><i data-bar></i></div>'
               f'<span class="pt" data-hechos>0 de {n} hechos</span><a class="btn prim sig" data-sig href="#ejercicios">Empezar con {esc(lista[0][1]["id"]) if lista else ""} →</a></div>'
               + (f'<details class="sbox aprende" data-aprende><summary><h2>Aprende</h2></summary><div class="alist main">{"".join(principales)}</div>{('<h3 class="sub">PDFs de teoría</h3><div class="alist">' + "".join(pdfs) + '</div>') if pdfs else ""}</details>' if aprender else '')
               + (f'<div class="sbox"><h2>Plantillas y código</h2><div class="rec">{"".join(recursos)}</div></div>' if recursos else '')
               + '</aside>')
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../index.html#temas" data-back>← Volver</a><a href="../index.html">Inicio</a>›<a href="../index.html#temas">{esc(bloque)}</a>›<span>Tema {t}</span></div>'
              f'<div class="thead" data-ids="{ids}"><div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center"><span class="tag">{esc(bloque)}</span><span class="est" data-est>Sin empezar</span></div>'
              f'<h1>Tema {t} · {esc(info["nombre"])}</h1><p class="lede">{esc(info["resumen"])}</p></div>'
              f'<div class="tlay">{lateral}<main class="tmain">{vhero}<div class="mh" id="ejercicios"><h2>Ejercicios <span class="cnt">{n}</span></h2>'
              f'<div class="filters"><button class="chip on" data-f="todos">Todos</button><button class="chip" data-f="pend">Pendientes</button><button class="chip" data-f="hechos">Hechos</button><button class="chip" data-fv>@@i:video@@ Con vídeo</button></div></div>'
              f'<div id="p-ejercicios">{"".join(filas)}<p class="vacio" id="sin">Ningún ejercicio coincide con el filtro.</p></div>'
              f'<p class="notas">Tests del profe y propios: próximamente.</p></main></div>{pager}</div>{teoria_panel(t, "../")}')
    titulo = f'Tema {t} · {info["nombre"]} | Diseño de Algoritmos UCM'
    desc = f'{info["resumen"]} Ejercicios de Diseño de Algoritmos de la FDI UCM resueltos en C++ con explicación.'
    return pagina(titulo, cuerpo, "../", FILTRO_JS + (TEORIA_JS if TEORIA.get(t) else ""), desc, ruta=f"tema/{t}.html")



def commit_info():
    sha = os.environ.get("GITHUB_SHA") or ""
    if not sha:
        try:
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        except Exception:
            sha = ""
    return sha[:7]


JUECES = set()   # slugs de los ejercicios con juez (pestaña «Probar»)

JUEZ_JS = r"""
// Pestaña «Probar»: el juez se carga solo cuando se abre (no pesa en el resto de la página).
(function(){const host=document.querySelector('.dj-host');if(!host)return;let hecho=false;
 const cargar=s=>new Promise((ok,ko)=>{const e=document.createElement('script');e.src=s;e.onload=ok;e.onerror=ko;document.head.appendChild(e)});
 function montar(){if(hecho)return;hecho=true;
  cargar('../juez/diagnostico.js').then(()=>cargar('../juez/juez.js'))
   .then(()=>DAJuez.mount(host,{manifest:host.dataset.manifest,wasmBase:host.dataset.wasm,servidor:host.dataset.servidor}))
   .catch(()=>{host.textContent='No se ha podido cargar el juez. Recarga la página.'})}
 document.querySelectorAll('[data-tab="probar"]').forEach(b=>b.addEventListener('click',montar));
 if(location.hash==='#probar')montar();
 window.addEventListener('hashchange',()=>{if(location.hash==='#probar')montar()});})();
"""


def main():
    global TEORIA, JUECES
    TEORIA = teoria_pdfs()
    JUECES = {k.lower() for k in config_juez()}
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
    for i, e in enumerate(ej):
        ant = (slugs[i - 1], f'{ej[i - 1]["id"]} {ej[i - 1]["titulo"]}') if i > 0 else None
        sig = (slugs[i + 1], f'{ej[i + 1]["id"]} {ej[i + 1]["titulo"]}') if i + 1 < len(ej) else None
        (OUT / "ej" / f"{slugs[i]}.html").write_text(pagina_ejercicio(e, slugs[i], ant, sig), encoding="utf-8")
    (OUT / "videos.html").write_text(pagina_videos(ej, slugs), encoding="utf-8")

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
            h = p.read_text(encoding="utf-8")
            h = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + VOLVER_HERR, h, count=1)
            (OUT / "herramientas" / p.name).write_text(h, encoding="utf-8")

    # páginas de tema
    (OUT / "tema").mkdir()
    herr_nombres = {x[0] for x in herr}
    nombres_temas = {t: info["nombre"] for t, info in TEMAS.items()}
    por_tema = {t: [(i, e) for i, e in enumerate(ej) if e["tema"] == t] for t in TEMAS}
    for t, info in TEMAS.items():
        if por_tema[t]:
            (OUT / "tema" / f"{t}.html").write_text(pagina_tema(t, info, por_tema[t], slugs, cabs, info["herr"] in herr_nombres, nombres_temas), encoding="utf-8")
    shutil.copytree(ESTILO / "marca", OUT / "estilo" / "marca")

    # portada
    solo_ej = [e for e in ej if not es_teoria(e)]
    n_pdf = sum(1 for e in ej if e["pdf"]); n_vid = sum(1 for e in ej if e["video"]); n_sol = sum(1 for e in solo_ej if e["sols"])
    todos_ids = ",".join(slugs[i] for i in range(len(ej)))
    bloques_html = []
    for nombre_b, temas_b, col in BLOQUES:
        tarjetas, ids_b = [], []
        for t in temas_b:
            if not por_tema.get(t):
                continue
            tarjetas.append(tarjeta_tema(t, TEMAS[t], por_tema[t], slugs, TEMAS[t]["herr"] in herr_nombres))
            ids_b += [slugs[i] for i, _ in por_tema[t]]
        if tarjetas:
            bloques_html.append(f'<section class="blk"><div class="bh" data-ids="{",".join(ids_b)}" style="--c:{col}"><h2><i></i>{esc(nombre_b)}</h2><span class="m" data-txt>0/{len(ids_b)} hechos · 0%</span><div class="prog"><i data-bar></i></div></div><div class="grid">{"".join(tarjetas)}</div></section>')
    tools_html = "".join(f'<a class="tool" href="herramientas/{f}"><span class="n">{esc(a)}</span><b>{esc(b)}</b><span class="d">{esc(c)}</span></a>' for f, a, b, c in herr)
    est_html = "".join(f'<a class="chip" href="estructuras/{quote(c)}.html">{esc(c)}</a>' for c in cabs)
    sha = commit_info()
    ahora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    n_temas = sum(1 for t in TEMAS if por_tema.get(t))
    cuerpo = f"""<div class="wrap">
<div class="hero"><p class="eyebrow">FDI UCM · Informática · Computadores · Software</p>
<h1>Diseño de Algoritmos: ejercicios resueltos, vídeos y herramientas</h1>
<p class="lede">Todos los problemas del juez con su enunciado, la solución en C++, la explicación del planteamiento, el vídeo paso a paso de cada uno y herramientas interactivas para entender cada estructura de datos.</p>
<label class="search">@@i:arrow@@<input id="q" type="search" placeholder="Buscar ejercicio (nombre, número, técnica…)" aria-label="Buscar ejercicio"><kbd>/</kbd></label></div>
<div class="sm" data-resumen>
<div class="box hi"><small>Tu progreso</small><b data-r="pct">0%</b><span data-r="txt"></span><div class="prog"><i data-r="bar"></i></div></div>
<div class="box"><small>Temas completados</small><b><u data-r="comp">0</u><em> / {n_temas}</em></b><span data-r="curso">0 en curso</span></div>
<div class="box"><small>Con solución</small><b>{round(n_sol / len(solo_ej) * 100)}%</b><span>{n_sol} de {len(solo_ej)} ejercicios</span></div>
<div class="box"><small>Tests</small><b>0</b><span>del profe y propios · pronto</span></div></div>
<section id="resultados" hidden><h2 id="res-t" style="margin-bottom:12px"></h2><div id="res-l"></div><p class="vacio" id="vacio">Ningún ejercicio coincide con la búsqueda.</p></section>
<div id="temas">{"".join(bloques_html)}</div>
<section class="bloque" id="herramientas"><h2>Herramientas interactivas</h2><p class="lede">Ejecutan la misma lógica que el C++ de la asignatura y resaltan el código línea a línea.</p><div class="tools">{tools_html}</div></section>
<section class="bloque" id="estructuras"><h2>Estructuras de datos</h2><p class="lede">Las cabeceras que da la asignatura, con visor de código, copiar y descargar.</p><div class="cabs">{est_html}</div></section>
<section class="bloque" id="videos"><h2>Vídeos</h2><p class="lede">Un vídeo paso a paso por cada ejercicio y por cada tema ({n_vid} en total), que se ven aquí mismo, con subtítulos.</p><p><a class="btn primary" href="videos.html">Ver todos los vídeos →</a></p></section>
<footer>Material de estudio independiente, no afiliado a la UCM{" · commit <code>" + esc(sha) + "</code>" if sha else ""} · actualizado {ahora}</footer></div>"""
    datos = json.dumps([{"s": slugs[i], "i": e["id"], "t": e["titulo"], "d": re.sub(r"`", "", e["idea"]), "k": color_de(e["tema"]),
                         "h": 1 if es_teoria(e) else 0, "v": 1 if e["video"] else 0, "c": 1 if e["sols"] else 0, "e": 1 if e["readme"] else 0, "p": 1 if e["pdf"] else 0} for i, e in enumerate(ej)], ensure_ascii=False)
    js = ("const EJ=" + datos.replace("</", "<\\/") + r""";
const q=document.getElementById('q');
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function fila(x){const ch=[];if(x.p)ch.push('<a class="chip p" href="ej/'+x.s+'.html#enunciado">Enunciado</a>');if(x.c)ch.push('<a class="chip" href="ej/'+x.s+'.html#codigo">Código</a>');if(x.e)ch.push('<a class="chip" href="ej/'+x.s+'.html#explicacion">Explicación</a>');if(x.v)ch.push('<a class="chip v" href="ej/'+x.s+'.html#video">Vídeo</a>');
 const ok=x.h?'<span class="okb th0" aria-hidden="true"><svg class="i"><use href="#i-book"/></svg></span>':'<button class="okb" data-ok="'+x.s+'" aria-label="Marcar '+esc(x.i)+' como hecho" aria-pressed="false"><svg class="i" aria-hidden="true"><use href="#i-check"/></svg></button>';
 return '<div class="exr'+(x.h?' teoria':'')+'" style="--c:'+x.k+'">'+ok+'<span class="id">'+(x.h?'Teoría':esc(x.i))+'</span><span class="t"><a href="ej/'+x.s+'.html">'+esc(x.t)+'</a></span><span class="idea">'+esc(x.d)+'</span><span class="chips">'+ch.join('')+'</span></div>'}
function filtra(){const v=q.value.trim().toLowerCase(),r=document.getElementById('resultados'),t=document.getElementById('temas');
 try{sessionStorage.setItem('q',q.value)}catch(e){}
 if(!v){r.hidden=true;t.hidden=false;return}
 const l=EJ.filter(x=>(x.i+' '+x.t+' '+x.d).toLowerCase().includes(v));
 document.getElementById('res-t').textContent=l.length+(l.length==1?' resultado':' resultados')+' para «'+q.value.trim()+'»';
 document.getElementById('res-l').innerHTML=l.map(fila).join('');document.getElementById('vacio').style.display=l.length?'none':'block';
 r.hidden=false;t.hidden=true;if(window.pintarProgreso)window.pintarProgreso()}
q.oninput=filtra;
document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus()}});
window.addEventListener('pageshow',()=>{try{const g=sessionStorage.getItem('q');if(g&&!q.value){q.value=g}}catch(e){}if(q.value)filtra()});""")
    (OUT / "index.html").write_text(pagina("Diseño de Algoritmos UCM: ejercicios resueltos, vídeos y herramientas | StudIA", cuerpo, "", js,
                                           "Ejercicios de Diseño de Algoritmos de la FDI UCM resueltos en C++, con explicación, vídeo paso a paso de cada uno y visualizadores de AVL, grafos y Dijkstra.", ruta=""), encoding="utf-8")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for r in dict.fromkeys(PAGINAS):
        sm.append(f"  <url><loc>{esc(BASE_DA + quote(r))}</loc><lastmod>{hoy}</lastmod></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("")

    # copiar ficheros referenciados + código de cada ejercicio
    for e in ej:
        if e["readme"]: COPIAR.add(e["readme"])
        if e["sols"] or e["readme"]:
            for p in (RAIZ / posixpath.dirname((e["sols"][0][1] if e["sols"] else e["readme"]))).glob("*"):
                if p.suffix in (".cpp", ".h"):
                    COPIAR.add(p.relative_to(RAIZ).as_posix())
    for c in cabs:
        COPIAR.add(f"Estructuras de datos/{c}")
    for t_, docs in TEORIA.items():
        for r_, _n, _b in docs:
            d = OUT / 'teoria' / str(t_) / posixpath.basename(r_); d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(RAIZ / r_, d)
    for rel in sorted(COPIAR):
        if existe(rel):
            d = OUT / rel; d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(RAIZ / rel, d)
    n_juez = generar_juez(ej, slugs)
    print(f"ok: {len(ej)} ejercicios, {n_vid} vídeos, {n_pdf} PDFs, {len(herr)} herramientas, {len(cabs)} cabeceras, {n_juez} jueces -> {OUT}")


def escribe_lf(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def config_juez():
    """Configuración de los jueces: juez/juez.json (antigua) + juez/tests/<id>/config.json (una por
    ejercicio, la escribe herramientas/generar_tests_juez.py). La clave es el slug de la página."""
    cfg = {}
    p = RAIZ / "juez" / "juez.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    for c in sorted((RAIZ / "juez" / "tests").glob("*/config.json")):
        cfg[c.parent.name] = json.loads(c.read_text(encoding="utf-8"))
    return cfg


def sin_planteamiento(codigo):
    """Las soluciones traen, tras «Nombre y Apellidos», un comentario /*@ <answer> ... */ con el
    planteamiento completo. En la plantilla del juez se deja solo su primera línea (el título):
    el planteamiento lo dan las pistas, de una en una."""
    bloques = list(re.finditer(r"/\*@ <answer>.*?@ </answer> \*/", codigo, flags=re.S))
    for m in reversed(bloques[1:]):
        lineas_ = [l.strip() for l in m.group(0).splitlines()[1:-1] if l.strip()]
        titulo = lineas_[0] if lineas_ else ""
        codigo = codigo[:m.start()] + f"/*\n {titulo}\n*/" + codigo[m.end():]
    return codigo


def generar_juez(ej, slugs=None):
    """Juez en el navegador (prototipo). Lee juez/juez.json y juez/tests/<ej>/N.in|N.out.
    Genera _site/juez/<ej>.html (página independiente) y _site/juez/<ej>/ (manifest, tests, cabeceras).
    El componente (sitio/juez/juez.js) no toca la página de ejercicio: se encaja donde se quiera."""
    cfg = config_juez()
    if not cfg:
        return 0
    por_slug = {slugs[i]: e for i, e in enumerate(ej)} if slugs else {e["id"].lower(): e for e in ej}
    wasm_base = os.environ.get("JUEZ_WASM_BASE", "https://binji.github.io/wasm-clang/")
    servidor = os.environ.get("JUEZ_SERVIDOR", "")   # URL del servidor del juez (Raspberry Pi); vacío = solo navegador
    shutil.copytree(AQUI / "juez", OUT / "juez")
    for ej_id, c in cfg.items():
        e = por_slug.get(ej_id.lower())
        if e is None:
            print(f"aviso: juez {ej_id} sin ejercicio en la web")
            continue
        d = OUT / "juez" / ej_id
        sol = leer_texto(c["solucion"])
        if c.get("plantilla"):           # plantilla propia (p. ej. 01-2: la clase sin tami ni kesimo)
            plantilla = leer_texto(c["plantilla"])
        else:
            vacio = "//@ <answer>\n\n    // Escribe aquí tu solución\n\n//@ </answer>"
            plantilla = re.sub(r"//@ <answer>.*?//@ </answer>", lambda m: vacio, sol, count=1, flags=re.S)
        plantilla = sin_planteamiento(plantilla)
        escribe_lf(d / "solucion.cpp", sol)
        a, b = c["fallo"]
        assert a in sol, f"juez {ej_id}: no encuentro «{a}» para fabricar el fallo de demostración"
        escribe_lf(d / "fallo.cpp", sol.replace(a, b, 1))
        cab = []
        for rel in c.get("cabeceras", []):
            nombre = posixpath.basename(rel)
            escribe_lf(d / nombre, leer_texto(rel))
            cab.append({"nombre": nombre, "url": nombre})
        tests = []
        meta_p = RAIZ / "juez" / "tests" / ej_id / "pruebas.json"   # qué comprueba cada prueba, pistas...
        meta = {m["n"]: m for m in json.loads(meta_p.read_text(encoding="utf-8"))} if meta_p.exists() else {}
        for p in sorted((RAIZ / "juez" / "tests" / ej_id).glob("*.in"), key=lambda p: int(p.stem)):
            n = p.stem
            escribe_lf(d / f"{n}.in", leer_texto(p.relative_to(RAIZ).as_posix()))
            escribe_lf(d / f"{n}.out", leer_texto(p.with_suffix(".out").relative_to(RAIZ).as_posix()))
            nombre_p = p.with_suffix(".txt")
            t = {"n": int(n), "nombre": nombre_p.read_text(encoding="utf-8").strip() if nombre_p.exists() else "",
                 "in": f"{n}.in", "out": f"{n}.out", "bytes": p.stat().st_size}
            t.update({k: v for k, v in meta.get(int(n), {}).items() if k != "n"})
            tests.append(t)
        manifest = {"id": ej_id, "titulo": e["titulo"], "limite_ms": c.get("limite_ms", 3000), "plantilla": plantilla,
                    "cabeceras": cab, "tests": tests,
                    "demo": {"solucion": "solucion.cpp", "fallo": "fallo.cpp"}}
        comp = RAIZ / "juez" / "tests" / ej_id / "comprobador.js"
        if c.get("comprobador") and comp.exists():    # admite varias respuestas: se comprueba, no se compara
            escribe_lf(d / "comprobador.js", comp.read_text(encoding="utf-8"))
            manifest["comprobador"] = "comprobador.js"
        escribe_lf(d / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
        cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../ej/{ej_id.lower()}.html">← Volver al ejercicio</a>'
                  f'<a href="../index.html">Inicio</a>›<a href="../tema/{e["tema"]}.html">Tema {e["tema"]}</a>›<span>{esc(ej_id)} · probar</span></div>'
                  f'<div class="ejhead"><span class="tag">Prototipo del juez</span><h1>{esc(ej_id)} · {esc(e["titulo"])}</h1>'
                  f'<p class="lede">Pega o escribe tu solución y comprueba si pasa las {len(tests)} pruebas de este ejercicio.</p></div>'
                  f'<div id="juez"></div></div>'
                  f'<script src="diagnostico.js"></script><script src="juez.js"></script><script>DAJuez.mount(document.getElementById("juez"),{{manifest:"{ej_id}/manifest.json",wasmBase:{json.dumps(wasm_base)},servidor:{json.dumps(servidor)}}})</script>')
        pag = pagina(f"Probar {ej_id} {e['titulo']} | Diseño de Algoritmos UCM", cuerpo, "../", "", "Prototipo del juez en el navegador.",
                     '<meta name="robots" content="noindex"><link rel="stylesheet" href="juez.css">')
        escribe_lf(OUT / "juez" / f"{ej_id}.html", pag)
    return len(cfg)


def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


if __name__ == "__main__":
    main()
