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
    12: dict(nombre="Pruebas evaluativas", resumen="Problemas de las pruebas evaluativas de la asignatura.", herr="", cab=[]),
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
        if re.match(r"##\s+Pruebas evaluativas\b", linea):
            tema = EVAL; continue
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
const CTL=/^(if|else|for|while|do|switch|case|default|return|break|continue|throw|try|catch|goto)$/;
const TY=/^(Set|Grafo|Digrafo|IndexPQ|Par|vector|queue|stack|string|priority_queue|pair|map|set|cin|cout|endl|std|Adys|size_t|BinTree|Pila|istream|ostream)$/;
const TOK=/(\/\/.*$)|(\/\*[\s\S]*?\*\/)|("[^"]*")|(#\w+)|(\b\d+\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)/g;
function esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function paint(src){let h='',m;TOK.lastIndex=0;while((m=TOK.exec(src))){const t=m[0];
 if(m[1]||m[2])h+='<span class="c">'+esc(t)+'</span>';else if(m[3])h+='<span class="s">'+esc(t)+'</span>';else if(m[4])h+='<span class="k">'+esc(t)+'</span>';
 else if(m[5])h+='<span class="n">'+t+'</span>';else if(m[6]&&CTL.test(t))h+='<span class="kc">'+t+'</span>';else if(m[6]&&KW.test(t))h+='<span class="k">'+t+'</span>';else if(m[6]&&(TY.test(t)||/^[A-Z][a-z]\w*$/.test(t)&&!/^\s*\(/.test(src.slice(TOK.lastIndex))))h+='<span class="t">'+t+'</span>';else if(m[6]&&/^\s*\(/.test(src.slice(TOK.lastIndex)))h+='<span class="fn">'+t+'</span>';else h+=esc(t)}return h}
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
function hasTab(id){return !!document.querySelector('[data-tab="'+id+'"]')}
function show(id,scroll){if(!hasTab(id)||!document.getElementById('p-'+id))return;
 document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id==='p-'+id));
 document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('on',b.dataset.tab===id));
 document.querySelectorAll('.pane:not(.on) video').forEach(v=>v.pause());
 if(scroll)document.querySelector('.tabs').scrollIntoView({block:'start'})}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{show(b.dataset.tab);try{history.replaceState(null,'','#'+b.dataset.tab)}catch(e){}});
document.querySelectorAll('[data-sub]').forEach(b=>b.onclick=()=>{const g=b.dataset.group;document.querySelectorAll('[data-group="'+g+'"]').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-subpane^="'+g+'"]').forEach(p=>p.style.display=p.dataset.subpane===b.dataset.sub?'block':'none')});
window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
const ini=location.hash.slice(1);show(hasTab(ini)?ini:(document.querySelector('[data-tab].pref')||document.querySelector('[data-tab]')).dataset.tab);
// aviso de la guía: desaparece cuando ya la has visto
(function(){var g=document.querySelector('[data-guia]');if(!g)return;try{if(localStorage.getItem('studia-da-guia'))g.hidden=true}catch(e){}g.addEventListener('click',function(){try{localStorage.setItem('studia-da-guia','1')}catch(e){}})})();
// lista de ejercicios del tema: abierta en escritorio, plegada en móvil
(function(){var d=document.querySelector('[data-det]');if(d&&window.innerWidth>960)d.open=true})();
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


EVAL = 12   # las pruebas evaluativas se guardan como «tema 12», pero en la web no llevan número


def tema_corto(t):
    """«Tema 4» o «Pruebas evaluativas»."""
    return "Pruebas evaluativas" if t == EVAL else f"Tema {t}"


def tema_largo(t, nombre):
    """«Tema 4 · Grafos no dirigidos» o «Pruebas evaluativas»."""
    return "Pruebas evaluativas" if t == EVAL else f"Tema {t} · {nombre}"


def pagina(titulo, cuerpo, prefijo="", extra_js="", desc="", head="", ruta=None):
    portal = f'<a href="{esc(PORTAL_URL)}/#asignaturas">Asignaturas</a>' if PORTAL_URL else ""
    marca = f'href="{prefijo}../" aria-label="StudIA, portal de asignaturas"' if PORTAL_URL else f'href="{prefijo}index.html" aria-label="Diseño de Algoritmos, inicio"'
    nav = (f'<header class="nav"><div class="nav-pill"><a class="brand" {marca}><img src="{prefijo}estilo/marca/mark.png" alt="" width="201" height="242"><b>StudIA</b><span class="subj">DA</span></a>'
           f'<nav aria-label="Principal">{portal}<a class="keep" href="{prefijo}index.html#temas">Temas</a><a href="{prefijo}laboratorio.html">Laboratorio</a>'
           f'<a class="keep" href="{prefijo}videos.html">Vídeos</a><a href="{prefijo}guia.html">Guía</a></nav>'
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


ACT = ' aria-current="page"'
CHEV_L = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
CHEV_R = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'


def pagina_ejercicio(e, slug, ant=None, sig=None, ctx=None):
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

    # 4 · Vídeo (bloque principal, fuera de las pestañas)
    p_vid = ""
    if e["video"]:
        vurl = href_sitio(e["video"], True)
        if MEDIA_BASE:
            vurl = MEDIA_BASE + quote(e["video"])
        vtt, caps = media_video(e["video"])
        track = f'<track kind="subtitles" srclang="es" label="Español" src="{(MEDIA_BASE + quote(vtt)) if MEDIA_BASE else "../" + quote(vtt)}">' if vtt else ""
        lista_caps = ("<div class='caps'><b>Capítulos</b>" + "".join(f'<button data-t="{t:.2f}"><span>{mmss(t)}</span>{esc(ti)}</button>' for t, ti in caps) + "</div>") if caps else ""
        p_vid = (f'<section class="evideo{" conc" if caps else ""}" id="video" aria-label="Vídeo del ejercicio"><div id="p-video" class="{"vid" if caps else "vid1"}">'
                 f'<video controls preload="metadata" playsinline{" crossorigin=anonymous" if MEDIA_BASE else ""} src="{vurl}">{track}Tu navegador no puede reproducir el vídeo: <a href="{vurl}">descárgalo</a>.</video>{lista_caps}</div>'
                 f'<div class="vlinks"><a class="xl" href="{vurl}" download="{esc(posixpath.basename(e["video"]))}">@@i:download@@ Descargar vídeo · {tam_legible((RAIZ / e["video"]).stat().st_size)}</a></div></section>')
        ficheros_zip.append((vurl, "video.mp4"))

    tabs = [("enunciado", "@@i:pdf@@ Enunciado", bool(e["pdf"]), p_enun),
            ("explicacion", "@@i:book@@ Explicación", bool(e["readme"]), p_exp), ("codigo", "@@i:code@@ Código", bool(codigos), p_cod)]
    hay_juez = slug in JUECES
    if hay_juez:
        p_juez = (f'<div class="dj-host" data-manifest="../juez/{slug}/manifest.json" '
                  f'data-wasm="{esc(os.environ.get("JUEZ_WASM_BASE", "https://binji.github.io/wasm-clang/"))}" '
                  f'data-servidor="{esc(os.environ.get("JUEZ_SERVIDOR", ""))}"><p class="hint">Cargando el juez…</p></div>')
        tabs.append(("probar", "@@i:check@@ Probar", True, p_juez))
    if e["readme"]:
        pref = "explicacion"
    elif codigos:
        pref = "codigo"
    else:
        pref = "enunciado"
    botones = "".join(f'<button class="btn{"" if hay else " off"}{" pref" if i == pref else ""}" data-tab="{i}">{t}</button>' for i, t, hay, _ in tabs)
    panes = "".join(f'<div class="pane" id="p-{i}">{c}</div>' for i, _, _, c in tabs)

    acc = []   # extras discretos, a la derecha de las pestañas
    if acr:
        acc.append(f'<a class="xl" href="{acepta_url(acr)}" target="_blank" rel="noopener">@@i:link@@ Acepta el Reto #{acr["num"]}</a>')
    contenido_zip = ", ".join(x for x, ok in (("enunciado", e["pdf"]), ("código", codigos), ("explicación", e["readme"]), ("vídeo", e["video"]), ("versión para Acepta el Reto", acr_fich)) if ok)
    if ficheros_zip:
        acc.append(f'<button class="xl" id="zip" data-name="{esc(e["id"] + " " + e["titulo"])}" data-files="{esc(json.dumps(ficheros_zip, ensure_ascii=False))}" title="El zip incluye: {esc(contenido_zip)}">@@i:download@@ Descargar todo .zip</button>')

    # --- barra lateral: volver, progreso del tema, apuntes y herramienta destacados, lista de ejercicios ---
    ctx = ctx or []
    hermanos = [(s_, x) for s_, x in ctx if not es_teoria(x)]
    apuntes = next(((s_, x) for s_, x in ctx if es_teoria(x)), None)
    ids = ",".join(s_ for s_, _ in hermanos)
    color = color_de(tema)
    tarjetas = []
    if apuntes:
        cur = " cur" if apuntes[0] == slug else ""
        tarjetas.append(f'<a class="arow main{cur}" href="{apuntes[0]}.html"><span class="pic">@@i:book@@</span><span class="at"><b>Apuntes del tema</b><small>Teoría explicada paso a paso</small></span>@@i:arrow@@</a>')
    if herr and (RAIZ / "Visualizaciones" / herr).exists():
        tarjetas.append(f'<a class="arow main alt" href="{url_herr(herr, "../")}"><span class="pic">@@i:tool@@</span><span class="at"><b>Herramienta interactiva</b><small>Prueba el algoritmo paso a paso</small></span>@@i:arrow@@</a>')
    items = ""
    for s_, x in hermanos:
        actual = s_ == slug
        items += (f'<a class="el{" actual" if actual else ""}" href="{s_}.html" data-st="{s_}"{ACT if actual else ""}><span class="dot">@@i:check@@</span>'
                  f'<span class="et"><b>{esc(x["id"])}</b>{esc(x["titulo"])}</span></a>')
    lateral = (f'<aside class="eside"><a class="volver" href="../tema/{tema}.html">{CHEV_L}<span>Volver al tema</span></a>'
               f'<div class="etema"><small>{tema_corto(tema)}</small><b>{esc(TEMAS[tema]["nombre"])}</b></div>'
               f'<div class="sbox prog-box" data-ids="{ids}" style="--c:{color}"><div class="ph"><small>Tu progreso</small><b data-pct>0%</b></div><div class="prog"><i data-bar></i></div>'
               f'<span class="pt" data-hechos>0 de {len(hermanos)} hechos</span></div>'
               + (f'<div class="atarj">{"".join(tarjetas)}</div>' if tarjetas else "")
               + (f'<details class="elist" data-det><summary>Ejercicios del tema</summary><div class="elin">{items}</div></details>' if items else "")
               + '</aside>')

    # --- cierre: anterior / marcar como hecho y seguir ---
    teoria_pag = es_teoria(e)
    prev_b = (f'<a class="enav prev" href="{ant[0]}.html"><span class="ar">{CHEV_L}</span><span class="tx"><small>Anterior</small>{esc(ant[1])}</span></a>' if ant else "<span></span>")
    if sig:
        etq = "Siguiente" if teoria_pag else "Marcar como hecho y seguir"
        done = "" if teoria_pag else f' data-done-go="{slug}"'
        next_b = f'<a class="enav next"{done} href="{sig[0]}.html"><span class="tx"><small>{etq}</small>{esc(sig[1])}</span><span class="ar">{CHEV_R}</span></a>'
    else:
        next_b = f'<a class="enav next" href="../tema/{tema}.html"><span class="tx"><small>Has llegado al final</small>Volver al tema {tema}</span><span class="ar">{CHEV_R}</span></a>'
    cierre = f'<div class="ecierre">{prev_b}{next_b}</div>'

    aviso = (f'<a class="guiab" href="../guia.html" data-guia><b>¿Primera vez aquí?</b><span>Guía de 1 minuto: qué es cada cosa y por dónde empezar</span><em>Ver la guía →</em></a>')
    etq_ej = ("Teoría" if teoria_pag else "Ejercicio") + " " + esc(e["id"])
    cuerpo = (f'<div class="wrap"><div class="elay">{lateral}<main class="emain">{aviso}'
              f'<div class="ejhead"><span class="eyebrow">{etq_ej}</span>'
              f'<div class="ejtit"><h1>{esc(e["titulo"])}</h1>'
              f'<button class="btn okb-ej" data-ok="{slug}" aria-pressed="false">@@i:check@@ <span class="lab">Marcar como hecho</span></button></div>'
              f'<p class="lede">{md_inline(e["idea"])}</p></div>'
              f'{p_vid}'
              f'<div class="tabsbar"><div class="tabs">{botones}</div><div class="xls">{"".join(acc)}</div></div>{panes}{cierre}</main></div></div>{teoria_panel(tema, "../")}')
    return pagina(f'{e["id"]} {e["titulo"]} | Diseño de Algoritmos UCM', cuerpo, "../", HIGHLIGHT_JS + TABS_JS + (TEORIA_JS if TEORIA.get(tema) else "") + (JUEZ_JS if hay_juez else ""), e["idea"],
                  JSZIP + ('<link rel="stylesheet" href="../juez/juez.css">' if hay_juez else ""), ruta=f"ej/{slug}.html")


def pagina_guia(n_temas, n_ej, n_herr, n_vid):
    pasos = [
        ("1", "Mira la teoría", "El vídeo del tema explica la idea general. Los apuntes la dejan resumida por escrito.", ""),
        ("2", "Juega con el algoritmo", f"La herramienta interactiva del tema te deja ver paso a paso qué hace el algoritmo (temas con herramienta: {n_herr}).", ""),
        ("3", "Haz los ejercicios en orden", "Lee el enunciado, inténtalo tú y, cuando te atasques, mira el vídeo y compara con la explicación y el código.", ""),
        ("4", "Márcalo y sigue", "Pulsa «Marcar como hecho» al terminar. La barra del tema te muestra cuánto llevas.", " ok"),
    ]
    dentro = [
        ("Vídeo", "El ejercicio resuelto y explicado. Es lo más útil para entenderlo."),
        ("Enunciado", "El PDF original del juez, con los casos de ejemplo."),
        ("Explicación", "Qué piden, cómo se plantea, por qué así y cuánto cuesta."),
        ("Código", "La solución en C++ lista para copiar o descargar, con sus cabeceras."),
    ]
    donde = [
        ("index.html#temas", "Temas", f"Los {n_temas} temas con sus ejercicios, vídeo y apuntes. Empieza aquí."),
        ("index.html#herramientas", "Herramientas", f"Las {n_herr} herramientas interactivas para ver los algoritmos funcionando."),
        ("laboratorio.html", "Laboratorio", "Estructuras de datos: simulador paso a paso, código .h, coste de cada operación y ejercicios."),
        ("videos.html", "Vídeos", f"Todos los vídeos juntos ({n_vid} en total), por si quieres verlos de seguido."),
    ]
    h_pasos = "".join(f'<div class="gp"><span class="gn{ok}">{n}</span><b>{esc(t)}</b><span>{esc(d)}</span></div>' for n, t, d, ok in pasos)
    h_dentro = "".join(f'<div class="gd"><b>{esc(t)}</b><span>{esc(d)}</span></div>' for t, d in dentro)
    h_donde = "".join(f'<a href="{u}"><b>{esc(t)}</b><span>{esc(d)}</span></a>' for u, t, d in donde)
    cuerpo = (f'<div class="wrap guia"><a class="volver" href="index.html">{CHEV_L}<span>Volver a Diseño de Algoritmos</span></a>'
              f'<header><span class="eyebrow">Guía · 1 minuto</span><h1>Cómo usar esta web</h1>'
              f'<p class="lede">Hay {n_temas} temas y {n_ej} ejercicios, cada uno con su vídeo, su explicación y su código. Esta guía te dice qué es cada cosa y por dónde empezar para no perderte.</p></header>'
              f'<section><h2>La ruta recomendada para cada tema</h2><div class="gpasos">{h_pasos}</div></section>'
              f'<section><h2>Qué hay dentro de cada ejercicio</h2><div class="gdentro">{h_dentro}</div></section>'
              f'<section><h2>Dónde está cada cosa</h2><div class="gdonde">{h_donde}</div></section>'
              f'<section class="gcta"><div><b>Tu progreso se guarda en este navegador</b><span>No hace falta cuenta. Si cambias de ordenador o borras los datos del navegador, empezará de cero.</span></div>'
              f'<a class="btn prim" href="tema/1.html">Empezar por el Tema 1 →</a></section></div>')
    return pagina("Cómo usar esta web | Diseño de Algoritmos UCM", cuerpo, "", "", "Guía de 1 minuto de Diseño de Algoritmos UCM: la ruta recomendada, qué hay en cada ejercicio y dónde está cada cosa.", ruta="guia.html")


def pagina_cabecera(nombre):
    rel = f"Estructuras de datos/{nombre}"
    herr = next((TEMAS[t]["herr"] for t in TEMAS if nombre in TEMAS[t]["cab"]), None)
    extra = f'<a class="btn" href="{url_herr(herr, "../")}">@@i:tool@@ Herramienta interactiva</a>' if herr and (RAIZ / "Visualizaciones" / herr).exists() else ""
    txt = leer_texto(rel)
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../laboratorio.html">← Volver</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../laboratorio.html">Laboratorio</a>›<span>{esc(nombre)}</span></div>'
              f'<div class="ejhead"><span class="tag">Estructura de datos</span><h1>{esc(nombre)}</h1>'
              f'<div class="acc"><button class="btn" data-copy="src0">@@i:copy@@ Copiar código</button>{descargar(rel, "@@i:download@@ Descargar " + esc(nombre))}{extra}</div></div>'
              f'<pre data-code="{esc(nombre)}" id="src0">{esc(txt)}</pre></div>')
    return pagina(f"{nombre} | Estructuras de datos de DA", cuerpo, "../", HIGHLIGHT_JS, f"Código de {nombre}, la cabecera de la asignatura de Diseño de Algoritmos, con visor, copiar y descargar.", ruta=f"estructuras/{nombre}.html")


# ----------------------------------------------------------------------------------------------------------------
#  LABORATORIO: una página por estructura con pestañas (Visualizar · Código · Operaciones y coste · Ejercicios)
# ----------------------------------------------------------------------------------------------------------------
LABS = {
    "tema4-grafo.html": dict(
        slug="grafo", titulo="Grafo", cab="Grafo.h",
        lede="Un grafo no dirigido guarda, para cada vértice, la lista de sus adyacentes. Aquí lo ves funcionar paso a paso, construyes el tuyo, lees su código y practicas con los ejercicios.",
        ops=[
            ("Grafo(V)", "Crea un grafo con V vértices y ninguna arista", "O(V)", "Hay que crear V listas de adyacentes vacías (una por vértice). No depende de las aristas, solo de cuántos vértices pidas."),
            ("ponArista(v, w)", "Añade la arista v–w", "O(1)", "Solo hace dos <code>push_back</code>: uno en la lista de v y otro en la de w, y sube <code>_A</code>. No recorre nada del grafo, así que tarda lo mismo con 10 vértices que con un millón."),
            ("ady(v)", "Devuelve los adyacentes de v", "O(1)", "Devuelve una referencia a la lista que ya está guardada: no la copia ni busca nada. Ojo: <b>recorrerla</b> sí cuesta O(grado de v)."),
            ("V() / A()", "Número de vértices / aristas", "O(1)", "Son dos enteros que la clase guarda al construir el grafo y actualiza en <code>ponArista</code>. Leerlos es instantáneo."),
            ("¿Existe la arista v–w?", "Comprobarlo recorriendo ady(v)", "O(grado(v))", "Hay que mirar la lista de adyacentes de v hasta encontrar w. En el peor caso v está unido con todos los demás, y la lista tiene V − 1 elementos."),
            ("DFS / BFS completo", "Recorrer todo el grafo", "O(V + A)", "Cada vértice se visita una sola vez (V). Al visitarlo se recorre su lista de adyacentes, y entre todos los vértices se recorren 2·A adyacentes (cada arista aparece en dos listas). Total: V + A. Con una matriz de adyacencia sería V², porque habría que mirar una fila entera por cada vértice."),
            ("Componentes conexas", "DFS desde cada vértice sin visitar", "O(V + A)", "Es un recorrido completo: lanzas un DFS cada vez que encuentras un vértice sin visitar, pero ningún vértice ni arista se procesa dos veces."),
            ("Camino mínimo (BFS)", "Distancia en aristas desde un origen", "O(V + A)", "BFS procesa cada vértice una vez y mira cada lista una vez. La cola garantiza que se llega a cada vértice por el camino con menos aristas."),
            ("Bipartito", "Colorear con 2 colores con DFS", "O(V + A)", "Es otro recorrido completo: al visitar cada arista se comprueba si los dos extremos tienen el mismo color. No hay trabajo extra por encima de V + A."),
        ]),
    "tema1-avl.html": dict(
        slug="avl", titulo="Árbol AVL", cab="TreeSet_AVL_plantilla.h", nota="El <b>coste</b> dice cómo crece el tiempo al crecer el árbol. <b>n</b> es el número de elementos. Abre cualquier fila para ver el razonamiento.",
        lede="Un árbol binario de búsqueda que se reequilibra solo con rotaciones. Inserta, borra y pide el k-ésimo elemento: ves el factor de equilibrio de cada nodo y cada rotación.",
        ops=[
            ("insertar(x)", "Añade x en su sitio y reequilibra", "O(log n)", "Bajas desde la raíz comparando (una rama por nivel) y al volver arriba corriges el equilibrio con como mucho una rotación simple o doble. Como el AVL garantiza altura ≤ 1,44·log₂(n+2), todo ello es logarítmico."),
            ("borrar(x)", "Quita x y reequilibra", "O(log n)", "Buscar x y su sucesor cuesta una bajada. Al volver, puede hacer falta una rotación en cada nivel del camino, y son O(log n) niveles con O(1) cada rotación."),
            ("buscar / contiene(x)", "Dice si x está", "O(log n)", "Es una búsqueda binaria en el árbol: en cada nodo descartas un subárbol entero. Un AVL nunca se degenera en lista, así que la altura es log n."),
            ("k-ésimo(k)", "El elemento en posición k del orden", "O(log n)", "Cada nodo guarda cuántos elementos hay en su subárbol. Con ese tamaño decides en cada nivel si el k-ésimo está a la izquierda, es el nodo actual o está a la derecha: una sola bajada."),
            ("Rotación", "Reordena 3 nodos para bajar la altura", "O(1)", "Solo cambia un puñado de punteros (y recalcula altura/tamaño de dos nodos). No recorre nada del árbol."),
            ("Recorrido en inorden", "Todos los elementos ordenados", "O(n)", "Visitas cada nodo una vez. No se puede ir más rápido: hay que producir n resultados."),
        ]),
    "tema2-cola-prioridad.html": dict(
        slug="cola-prioridad", titulo="Cola de prioridad", cab=None, nota="El <b>coste</b> dice cómo crece el tiempo al crecer la cola. <b>n</b> es el número de elementos. Abre cualquier fila para ver el razonamiento.",
        lede="Un montículo binario guardado en un vector. Siempre tienes a mano el mínimo (o el máximo): mira cómo flota cada push y cómo se hunde tras cada pop.",
        ops=[
            ("push(x)", "Añade x al final y lo hace flotar", "O(log n)", "Se coloca en la primera posición libre del vector y, mientras sea mejor que su padre, intercambia con él. Como el árbol es completo tiene altura log n, así que sube como mucho log n niveles."),
            ("top()", "Mira el mejor elemento", "O(1)", "Está siempre en la posición 1 del vector (la raíz). No hay que buscar nada."),
            ("pop()", "Quita el mejor y reordena", "O(log n)", "Se mueve el último elemento a la raíz y se hunde intercambiándolo con su mejor hijo. Baja como mucho log n niveles."),
            ("size() / empty()", "Cuántos elementos hay", "O(1)", "Es el tamaño del vector menos uno (la posición 0 no se usa). Leerlo es instantáneo."),
            ("Construir con n elementos", "Heapify: hundir desde la mitad hacia atrás", "O(n)", "Parece O(n log n) pero no lo es: la mitad de los nodos son hojas y no se hunden, un cuarto se hunde 1 nivel, un octavo 2 niveles… La suma Σ n/2^k · k es lineal."),
            ("Heapsort", "Ordenar haciendo n pops", "O(n log n)", "Construir el montículo cuesta O(n) y después hay n pops de O(log n) cada uno."),
        ]),
    "tema3-indexpq.html": dict(
        slug="indexpq", titulo="IndexPQ", cab="IndexPQ.h", nota="El <b>coste</b> dice cómo crece el tiempo al crecer la cola. <b>n</b> es el número de elementos. Abre cualquier fila para ver el razonamiento.",
        lede="Un montículo con una tabla de posiciones: sabes dónde está cada elemento, así que puedes cambiar su prioridad sin recorrer nada. Es la pieza clave de Dijkstra y Prim.",
        ops=[
            ("push(e, p)", "Inserta e con prioridad p", "O(log n)", "Se añade al final, se anota su posición en la tabla y se hace flotar. La tabla se actualiza en cada intercambio, que cuesta O(1)."),
            ("update(e, p)", "Cambia la prioridad de e", "O(log n)", "Aquí está la gracia: la tabla de posiciones te dice dónde está e en O(1). Después solo hay que flotarlo (o hundirlo) y eso son log n niveles. Sin la tabla habría que buscarlo antes: O(n)."),
            ("top() / prioridad", "Mejor elemento y su prioridad", "O(1)", "El mejor está en la raíz y su prioridad se lee directamente del vector."),
            ("pop()", "Quita el mejor", "O(log n)", "Se baja el último a la raíz y se hunde. Cada intercambio actualiza la tabla de posiciones en O(1)."),
            ("size() / empty()", "Cuántos elementos hay", "O(1)", "Es el tamaño del vector menos uno."),
        ]),
    "tema6-kruskal.html|lab": dict(
        slug="conjuntos-disjuntos", titulo="Conjuntos disjuntos", cab="ConjuntosDisjuntos.h", extra=["ConjuntosDisjuntos_variantes.h"],
        desc="Particiones que solo se unen: las cuatro implementaciones, de la más lenta a la del juez.",
        nota="El <b>coste</b> dice cómo crece el tiempo. <b>n</b> es el número de elementos. Abre cualquier fila para ver el razonamiento.",
        lede="Una partición que solo sabe juntar conjuntos. Compara sus cuatro implementaciones (búsqueda rápida, unión rápida, por tamaños y con compresión de caminos) y mira cómo cambian los árboles.",
        ops=[
            ("buscar(a)", "Representante del conjunto de a", "O(α(n)) ≈ O(1)", "Con unión por tamaños el árbol tiene altura log n; con compresión de caminos cada búsqueda aplana el camino recorrido. Juntas dan un coste amortizado α(n) (inversa de Ackermann), que en la práctica es menor que 5."),
            ("unir(a, b)", "Fusiona los conjuntos de a y b", "O(α(n)) ≈ O(1)", "Son dos búsquedas más colgar la raíz pequeña de la grande. Lo único caro son las búsquedas."),
            ("unidos(a, b)", "¿Están en el mismo conjunto?", "O(α(n)) ≈ O(1)", "Dos búsquedas y comparar representantes."),
            ("cardinal(a) / num_cjtos()", "Tamaño del conjunto / cuántos hay", "O(α(n)) / O(1)", "El tamaño se guarda en la raíz (hay que buscarla); el número de conjuntos es un contador."),
            ("Versión «búsqueda rápida»", "Vector id[] con el conjunto de cada uno", "buscar O(1), unir O(n)", "Buscar es leer id[a]. Pero unir obliga a recorrer todo el vector para renombrar un conjunto."),
            ("Versión «unión rápida»", "Un árbol por conjunto, sin equilibrar", "unir O(1)*, buscar O(n)", "Unir cuelga una raíz de otra. Pero sin control de la altura el árbol puede degenerar en una lista y buscar recorre hasta n nodos. (*tras buscar las raíces)."),
            ("Por tamaños", "Colgar siempre el árbol pequeño del grande", "O(log n)", "Cada vez que un elemento baja un nivel, su conjunto al menos se duplica. Como no puede duplicarse más de log n veces, la altura es ≤ log n."),
        ]),
    "tema6-kruskal.html|graf": dict(
        slug="grafo-valorado", titulo="Grafo valorado: Kruskal y Prim", cab="GrafoValorado.h", extra=["GrafoValorado_algoritmos.h"],
        desc="Grafos con valores en las aristas y árbol de recubrimiento de coste mínimo (Kruskal y Prim).",
        nota="El <b>coste</b> dice cómo crece el tiempo. <b>V</b> y <b>A</b> son los vértices y aristas del grafo. Abre cualquier fila para ver el razonamiento.",
        lede="Un grafo no dirigido con valores en las aristas. Construye el tuyo y ejecuta Kruskal o Prim para ver cómo se forma el árbol de recubrimiento de coste mínimo.",
        ops=[
            ("GrafoValorado(V)", "Crea un grafo con V vértices y sin aristas", "O(V)", "Crea V listas de adyacentes vacías."),
            ("ponArista({v, w, c})", "Añade una arista con valor c", "O(1)", "Una sola arista compartida que se guarda en la lista de v y en la de w: dos push_back."),
            ("ady(v)", "Aristas incidentes en v", "O(1)", "Devuelve la lista ya guardada. Recorrerla cuesta O(grado de v)."),
            ("aristas()", "Todas las aristas, cada una una vez", "O(V + A)", "Recorre todas las listas y se queda con cada arista una sola vez (la ve dos veces, una por extremo)."),
            ("Kruskal", "Ordenar aristas y unir sin formar ciclos", "O(A log A)", "Ordenar las aristas domina: A log A. Después hay A comprobaciones/uniones casi constantes gracias a los conjuntos disjuntos."),
            ("Prim", "Crecer el árbol con una cola de prioridad", "O(A log V)", "Cada arista puede provocar un update/push en la cola (log V) y hay A aristas."),
            ("¿Es único el ARM?", "Solo si los valores son distintos", "—", "Si hay aristas con el mismo valor puede haber varios árboles de coste mínimo; el coste total es el mismo."),
        ]),
    "tema7-dijkstra.html": dict(
        slug="dijkstra", titulo="Dijkstra", cab="DigrafoValorado.h", nota="El <b>coste</b> dice cómo crece el tiempo. <b>V</b> y <b>A</b> son los vértices y aristas del dígrafo. Abre cualquier fila para ver el razonamiento.",
        lede="Caminos mínimos desde un origen en un dígrafo con costes. Ves la cola de prioridad, las distancias que se van fijando y cómo se reconstruye la ruta.",
        ops=[
            ("ponArista(v, w, c)", "Añade la arista v→w con coste c", "O(1)", "Un push_back en la lista de v. No recorre nada."),
            ("ady(v)", "Aristas que salen de v", "O(1)", "Devuelve la lista ya guardada. Recorrerla cuesta O(grado de salida)."),
            ("Dijkstra completo", "Distancias mínimas desde el origen", "O(A log V)", "Cada vértice sale una vez de la cola (V pops de log V) y cada arista se relaja una vez, y relajar puede ser un update de la IndexPQ (log V). Total: (V + A)·log V, que es O(A log V) si todos los vértices son alcanzables."),
            ("Reconstruir el camino", "Seguir los predecesores hasta el origen", "O(V)", "Se sigue el vector de predecesores de destino a origen: como mucho V pasos."),
            ("Contar caminos mínimos", "Contador junto a cada distancia", "O(A log V)", "Es el mismo Dijkstra con un contador extra que se actualiza en cada relajación: no añade coste asintótico."),
            ("Con pesos negativos", "No funciona", "—", "Dijkstra fija la distancia de un vértice al sacarlo de la cola porque asume que ningún camino posterior puede mejorarla, y con pesos negativos eso es falso. Para ellos hace falta Bellman-Ford."),
        ]),
    "tema5-digrafo.html": dict(
        slug="digrafo", titulo="Digrafo", cab="Digrafo.h",
        lede="En un grafo dirigido cada arista v→w tiene sentido. Construye uno, mira cómo se rellenan las listas de sucesores y ejecuta BFS, orden topológico o inverso() sobre el código real.",
        ops=[
            ("Digrafo(V)", "Crea un digrafo con V vértices y ninguna arista", "O(V)", "Hay que crear V listas de sucesores vacías. No depende de las aristas."),
            ("ponArista(v, w)", "Añade la arista v→w", "O(1)", "Un único <code>push_back</code>: w entra solo en la lista de v. No se recorre nada, así que el coste es constante."),
            ("ady(v)", "Devuelve los sucesores de v", "O(1)", "Devuelve una referencia a la lista guardada, sin copiarla. Recorrerla cuesta O(grado de salida de v)."),
            ("V() / A()", "Número de vértices / aristas", "O(1)", "Dos enteros que la clase mantiene al día. Aquí cada arista se guarda una vez, así que la suma de las longitudes de las listas es exactamente <code>_A</code>."),
            ("inverso()", "Crea el digrafo con todas las aristas invertidas", "O(V + A)", "Hay que recorrer todas las listas (V listas y A elementos en total) y meter cada arista v→w como w→v en el nuevo digrafo. Cada arista se toca una sola vez."),
            ("BFS", "Distancias desde un origen", "O(V + A)", "Cada vértice entra una vez en la cola y se recorre su lista de sucesores una vez. Solo se llega a los vértices alcanzables desde el origen."),
            ("Orden topológico", "DFS y postorden inverso", "O(V + A)", "Es un DFS completo: cada vértice y cada arista se procesan una vez. El orden sale de apilar los vértices cuando terminan; si aparece una arista hacia un vértice aún «en proceso», hay un ciclo."),
            ("Detectar ciclos", "DFS con tres estados", "O(V + A)", "El mismo DFS del orden topológico: marcar cada vértice como sin visitar, en proceso o terminado no añade trabajo por encima de V + A."),
        ]),
}


def url_herr(herr, pre=""):
    """Dirección de la herramienta: la página del laboratorio si existe, y si no la herramienta suelta."""
    k = next((k for k in LABS if k.split("|")[0] == herr), None)
    return f"{pre}lab/{LABS[k]['slug']}.html" if k else f"{pre}herramientas/{herr}"


def pagina_lab(herr, lab, tema, info, lista_ej, slugs, descr_herr, otros=(), vista=""):
    rel = f"Estructuras de datos/{lab['cab']}" if lab["cab"] else None
    txt = leer_texto(rel) if rel else ""
    nota = lab.get("nota", "El <b>coste</b> dice cómo crece el tiempo al crecer el grafo. <b>V</b> es el número de vértices y <b>A</b> el de aristas. Abre cualquier fila para ver el razonamiento.")
    filas = []
    for i, e in lista_ej:
        if es_teoria(e):
            continue
        filas.append(f'<a class="labej" data-st="{slugs[i]}" href="../ej/{slugs[i]}.html"><span class="tk" aria-hidden="true">@@i:check@@</span><b>{esc(e["id"])}</b><span class="t">{esc(e["titulo"])}</span><span class="e">Hecho</span></a>')
    ops = "".join(f'<details class="op"><summary><code>{o[0]}</code><span class="q">{o[1]}</span><b class="c">{o[2]}</b><i>¿Por qué?</i></summary><div class="why"><b>Por qué: </b>{o[3]}</div></details>' for o in lab["ops"])
    tabs = [("vis", "Visualizar")] + ([("cod", f"Código<span class=\"fn\"> ({lab['cab']})</span>")] if rel else []) + [("ops", "Operaciones y coste"), ("ej", "Ejercicios")]
    botones = "".join(f'<button class="btn{" pref" if i == "vis" else ""}" data-tab="{i}">{t}</button>' for i, t in tabs)
    panes = (f'<div class="pane" id="p-vis"><iframe id="labframe" class="labframe" src="../herramientas/{herr}?embed=1{("&vista=" + vista) if vista else ""}" title="Simulador de {esc(lab["titulo"])}" loading="eager"></iframe></div>'
             + (f'<div class="pane" id="p-cod"><pre data-code="{esc(lab["cab"])}" id="src0">{esc(txt)}</pre></div>' if rel else '') +
             f'<div class="pane" id="p-ops"><p class="lede">{nota}</p><div class="ops">{ops}</div></div>'
             f'<div class="pane" id="p-ej"><p class="lede">Ejercicios del juez que usan esta estructura. Se marcan en verde cuando los das por hechos.</p><div class="labejs">{"".join(filas)}</div></div>')
    cuerpo = (f'<div class="wrap lab"><div class="crumbs"><a class="back" href="../laboratorio.html">← Laboratorio</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../laboratorio.html">Laboratorio</a>›<span>{esc(lab["titulo"])}</span></div>'
              f'<div class="ejhead"><span class="tag">Tema {tema} · Estructura de datos</span><h1>{esc(lab["titulo"])}</h1><p class="lede">{lab["lede"]}</p>'
              f'<div class="acc">' + (f'<button class="btn" data-copy="src0">@@i:copy@@ Copiar código</button>{descargar(rel, "@@i:download@@ Descargar " + esc(lab["cab"]))}' if rel else '')
              + "".join(f'<a class="btn" href="../estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>' for c in otros) + f'<a class="btn" href="../tema/{tema}.html">@@i:book@@ Ver el tema {tema}</a></div></div>'
              f'<div class="tabsbar"><div class="tabs">{botones}</div></div>{panes}</div>')
    js = HIGHLIGHT_JS + TABS_JS + LAB_JS
    return pagina(f"{lab['titulo']} · Laboratorio | Diseño de Algoritmos UCM", cuerpo, "../", js,
                  f"Laboratorio de {lab['titulo']}: simulador paso a paso, código C++, coste de cada operación y ejercicios.", ruta=f"lab/{lab['slug']}.html")


LAB_JS = r"""
// el simulador (iframe) avisa de su alto; así no hay doble barra de desplazamiento
(function(){var f=document.getElementById('labframe');if(!f)return;
 window.addEventListener('message',function(e){if(e.source!==f.contentWindow||!e.data||e.data.tipo!=='da-lab-alto')return;if(e.data.alto>200)f.style.height=(e.data.alto+4)+'px'});
 (function(){var t=document.querySelector('.lab .tabs');if(!t)return;var ind=document.createElement('span');ind.className='ind';t.appendChild(ind);
 function mv(){var b=t.querySelector('.btn.on');if(!b||!b.offsetWidth){t.classList.add('sin-ind');return}t.classList.remove('sin-ind');ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)';if(t.scrollWidth>t.clientWidth){var l=b.offsetLeft-(t.clientWidth-b.offsetWidth)/2;if(t.scrollTo)t.scrollTo({left:l,behavior:t.classList.contains('listo')?'smooth':'auto'})}}
 mv();setTimeout(function(){mv();setTimeout(function(){t.classList.add('listo')},30)},50);window.addEventListener('resize',mv);window.addEventListener('hashchange',function(){requestAnimationFrame(mv)});if(document.fonts&&document.fonts.ready)document.fonts.ready.then(mv);
 t.querySelectorAll('.btn').forEach(function(b){b.addEventListener('click',function(){requestAnimationFrame(mv)})})})();
document.querySelectorAll('[data-tab]').forEach(function(b){b.addEventListener('click',function(){if(b.dataset.tab==='vis')setTimeout(function(){try{f.contentWindow.postMessage({tipo:'da-lab-medir'},'*')}catch(x){}},60)})});
})();
"""


def cabs_por_tema(cabs):
    """Cada cabecera .h pertenece a un tema: el primero que la lista (o el de su cabecera base, p. ej. Grafo_algoritmos.h -> Grafo.h)."""
    res = {t: [] for t in TEMAS}
    for c in cabs:
        base = c.split("_")[0].replace(".h", "") + ".h"
        dueno = next((t for t in TEMAS if c in TEMAS[t]["cab"]), None) or next((t for t in TEMAS if base in TEMAS[t]["cab"]), None)
        if dueno:
            res[dueno].append(c)
    return res


def pagina_laboratorio(temas_lab, n_ej_por_tema):
    """Catálogo: una tarjeta por tema con estructura (simulador + sus cabeceras + ejercicios)."""
    tarjetas = []
    for t, titulo, url, cab_main, otros, desc, lab_ok in temas_lab:
        n = n_ej_por_tema.get(t, 0)
        chips_h = "".join(f'<a class="chip" href="estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>' for c in ([cab_main] if cab_main else []) + otros)
        tarjetas.append(f'<div class="labcard" data-f="t{t}"><span class="top"><b class="tm">Tema {t} · {esc(TEMAS[t]["nombre"])}</b></span>'
                        f'<a class="nm" href="{url}">{esc(titulo)}<span class="go">{"Abrir laboratorio" if lab_ok else "Abrir simulador"} @@i:arrow@@</span></a>'
                        f'<span class="ds">{esc(desc)}</span><span class="bt">{chips_h}<a class="chip" href="tema/{t}.html">{plural(n, "ejercicio", "ejercicios")}</a></span></div>')
    filtros = [("all", "Todo"), ("t1", "Temas 1-3"), ("t4", "Temas 4-5"), ("t6", "Temas 6-7")]
    chips = "".join(f'<button class="btn{" on" if k == "all" else ""}" data-lf="{k}">{t}</button>' for k, t in filtros)
    cuerpo = (f'<div class="wrap lab"><div class="crumbs"><a class="back" href="index.html">← Volver</a><a href="index.html">Inicio</a>›<span>Laboratorio</span></div>'
              f'<div class="hero"><p class="eyebrow">Laboratorio</p><h1>Estructuras de datos y simuladores</h1>'
              f'<p class="lede">Cada estructura pertenece a un tema: aquí tienes su simulador paso a paso, el código de la asignatura, el coste de cada operación y los ejercicios de ese tema.</p></div>'
              f'<div class="labfil" role="group" aria-label="Filtrar por tema">{chips}</div><div class="labgrid" id="labgrid">{"".join(tarjetas)}</div></div>')
    js = r"""
var fb=document.querySelectorAll('[data-lf]');
function filtra(k){fb.forEach(function(b){b.classList.toggle('on',b.dataset.lf===k)});
 document.querySelectorAll('.labcard').forEach(function(c){var t=+c.dataset.f.slice(1);
  var ok=k==='all'||(k==='t1'&&t<=3)||(k==='t4'&&t>=4&&t<=5)||(k==='t6'&&t>=6&&t<=7);c.style.display=ok?'':'none'})}
fb.forEach(function(b){b.onclick=function(){filtra(b.dataset.lf)}});
"""
    return pagina("Laboratorio: estructuras de datos y simuladores | Diseño de Algoritmos UCM", cuerpo, "", js,
                  "Laboratorio de estructuras de datos de Diseño de Algoritmos: simuladores paso a paso, código C++, coste de las operaciones y ejercicios.", ruta="laboratorio.html")


def datos_videos(ej, slugs):
    """Datos de cada vídeo para la página: duración, miniatura, subtítulos y capítulos (si hay ffmpeg)."""
    out = []
    pdir = OUT / "Videos" / "posters"
    for i, e in enumerate(ej):
        if not e["video"]:
            continue
        src = RAIZ / e["video"]
        dur = 0.0
        if shutil.which("ffprobe"):
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True)
            try:
                dur = float(r.stdout.strip())
            except ValueError:
                dur = 0.0
        poster = ""
        if shutil.which("ffmpeg") and dur:
            pdir.mkdir(parents=True, exist_ok=True)
            p = pdir / f"{slugs[i]}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(4, dur * 0.2)), "-i", str(src), "-frames:v", "1", "-vf", "scale=360:-2", "-q:v", "6", str(p)], capture_output=True)
            if p.exists() and p.stat().st_size > 200:
                poster = f"Videos/posters/{slugs[i]}.jpg"
        vtt, caps = media_video(e["video"])
        out.append(dict(s=slugs[i], id=e["id"], t=e["titulo"], tema=e["tema"], tn=TEMAS[e["tema"]]["nombre"], d=round(dur), v=quote(e["video"]),
                        vtt=quote(vtt) if vtt else "", caps=[[round(c[0]), c[1]] for c in caps], p=poster, teoria=es_teoria(e), idea=re.sub(r"`", "", e["idea"])))
    return out


VIDEOS_JS = r"""
const V=__DATA__;
const $=s=>document.querySelector(s);
const fmt=d=>d>=3600?Math.floor(d/3600)+':'+String(Math.floor(d%3600/60)).padStart(2,'0')+':'+String(d%60).padStart(2,'0'):Math.floor(d/60)+':'+String(d%60).padStart(2,'0');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const KEY='studia-da-vistos';
let vistos={};try{vistos=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(vistos))}catch(e){}};
const byT={};V.forEach(v=>(byT[v.tema]=byT[v.tema]||[]).push(v));
const idx=s=>V.findIndex(v=>v.s===s);
const thumb=v=>'<span class="thumb">'+(v.p?'<img loading="lazy" src="'+v.p+'" alt="" onerror="this.remove()">':'')+'<span class="ok" aria-hidden="true">✓</span><span class="pl"><i>▶</i></span><span class="dur">'+fmt(v.d)+'</span></span>';
const root=$('#vroot');
function menu(){
 document.title='Vídeos de Diseño de Algoritmos UCM | StudIA';clearInterval(window._nxt);document.body.classList.remove('cine-on');$('.vv').classList.remove('ensala');
 const sig=V.find(v=>!vistos[v.s]),hay=Object.keys(vistos).length;
 const sec=Object.keys(byT).map(t=>{const xs=byT[t],teo=xs.find(x=>x.teoria),res=xs.filter(x=>x!==teo),n=xs.filter(x=>vistos[x.s]).length,min=Math.round(xs.reduce((a,x)=>a+x.d,0)/60);
  return '<section class="vtema"><div class="vth"><h2><span>Tema '+t+'</span>'+esc(xs[0].tn)+'</h2><small>'+n+'/'+xs.length+' vistos · '+min+' min</small></div><div class="vprog"><i style="width:'+(n/xs.length*100)+'%"></i></div>'
  +'<div class="vrow">'+(teo?'<a class="vcard teo'+(vistos[teo.s]?' vist':'')+'" href="#'+teo.s+'">'+thumb(teo)+'<span class="etq">Resumen del tema</span><b>'+esc(teo.t)+'</b></a>':'<div></div>')
  +'<div class="vsc">'+res.map(x=>'<a class="vcard ej'+(vistos[x.s]?' vist':'')+'" href="#'+x.s+'">'+thumb(x)+'<span class="etq">Ejercicio '+esc(x.id)+'</span><b>'+esc(x.t)+'</b></a>').join('')+'</div></div></section>'}).join('');
 root.className='vmenu';
 root.innerHTML='<div class="hero"><span class="tag">Vídeos</span><h1>Vídeos explicativos</h1><p class="lede">Un bloque por tema: el <b class="ct">resumen del tema</b> y, al lado, el <b class="ce">vídeo de cada ejercicio</b>. '+V.length+' vídeos, '+Math.round(V.reduce((a,v)=>a+v.d,0)/60)+' minutos.</p></div>'
 +(sig?'<a class="vcont" href="#'+sig.s+'">'+thumb(sig)+'<div><span class="etq">'+(hay?'Continuar':'Empezar por aquí')+'</span><b>'+esc(sig.id)+' · '+esc(sig.t)+'</b><small>Tema '+sig.tema+' · '+esc(sig.tn)+'</small></div><span class="go">Ver →</span></a>':'')+sec;
}
function sala(s){
 const sv=p=>'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+p+'</svg>';
 const SP='<path d="M4 9.5v5h3.5L12 18.5v-13L7.5 9.5z" fill="currentColor"/>';
 const I={play:sv('<path d="M7 4.5v15l12-7.5z" fill="currentColor" stroke="none"/>'),pause:sv('<rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor" stroke="none"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor" stroke="none"/>'),
  vol:sv(SP+'<path d="M15.5 9a4 4 0 010 6M18 6.5a8 8 0 010 11"/>'),vol1:sv(SP+'<path d="M15.5 9a4 4 0 010 6"/>'),mute:sv(SP+'<path d="M16 9.5l5 5M21 9.5l-5 5"/>'),
  more:sv('<circle cx="12" cy="5" r="1.6" fill="currentColor"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/><circle cx="12" cy="19" r="1.6" fill="currentColor"/>'),
  fs:sv('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>'),fso:sv('<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/>')};
 clearInterval(window._nxt);document.body.classList.remove('cine-on');
 const i=idx(s),v=V[i];if(!v){location.hash='';return}
 document.title=v.id+' · '+v.t+' | Vídeos StudIA';
 const q=(window._q||'').toLowerCase(),sg=V[i+1];
 const lista=Object.keys(byT).map(t=>{const xs=byT[t].filter(x=>!q||(x.id+' '+x.t+' '+x.idea).toLowerCase().includes(q));if(!xs.length)return'';const n=byT[t].filter(x=>vistos[x.s]).length;
  return '<details '+(q||t==v.tema?'open':'')+'><summary><span>Tema '+t+' · '+esc(byT[t][0].tn)+'</span><small>'+n+'/'+byT[t].length+'</small></summary>'+xs.map(x=>'<a class="it'+(x.s===s?' act':'')+(vistos[x.s]?' vist':'')+(x.teoria?' teo':' ej')+'" href="#'+x.s+'">'+thumb(x)+'<div><b>'+esc(x.id)+' · '+esc(x.t)+'</b><span>'+(x.teoria?'Resumen del tema':'Ejercicio')+'</span></div></a>').join('')+'</details>'}).join('');
 root.className='vsala';$('.vv').classList.add('ensala');
 root.innerHTML='<div class="vtop"><a class="vback" href="#">← Todos los vídeos</a></div><div class="sala"><div class="main"><div class="pw" id="pw"><video id="vid" preload="metadata" playsinline'+(v.p?' poster="'+v.p+'"':'')+' src="'+v.v+'">'+(v.vtt?'<track kind="subtitles" srclang="es" label="Español" src="'+v.vtt+'">':'')+'</video>'
 +'<div class="vc" id="vc"><button type="button" class="ic" id="pp" aria-label="Reproducir">'+I.play+'</button><span class="vol"><button class="ic" id="mu" type="button" aria-label="Silenciar">'+I.vol+'</button><input type="range" id="vl" min="0" max="1" step="0.02" value="1" aria-label="Volumen"></span><span class="tm" id="tm">0:00 / 0:00</span><input type="range" id="sk" min="0" max="1000" value="0" aria-label="Progreso"><div class="mn"><button class="ic" id="mb" type="button" aria-label="Más opciones">'+I.more+'</button><div class="pop" id="pop" hidden><div class="r"><span>Velocidad</span><div class="spd">'+[.75,1,1.25,1.5,2].map(x=>'<button type="button" data-v="'+x+'"'+(x===1?' class="on"':'')+'>'+x+'×</button>').join('')+'</div></div>'+(v.vtt?'<label class="r"><span>Subtítulos</span><input type="checkbox" id="cc" checked></label>':'')+'<label class="r"><span>Pasar al siguiente</span><input type="checkbox" id="auto" '+(window._auto===false?'':'checked')+'></label></div></div><button class="ic" id="fs" type="button" aria-label="Pantalla completa">'+I.fs+'</button></div>'
 +'<button class="xit" id="xit" type="button">✕ Salir de pantalla completa</button>'
 +(sg?'<div class="nx" id="nx" hidden><span>Siguiente en <b id="cd">5</b> s</span><b class="nt">'+esc(sg.id)+' · '+esc(sg.t)+'</b><div><button class="btn go" id="nxgo" type="button">Ver ahora</button><button class="btn ghost" id="nxno" type="button">Cancelar</button></div></div>':'')+'</div>'
 +'<div class="info"><span class="etq '+(v.teoria?'teo':'ej')+'">'+(v.teoria?'Resumen del tema '+v.tema:'Ejercicio '+esc(v.id))+' · '+esc(v.tn)+'</span><h2>'+esc(v.t)+'</h2><p>'+esc(v.idea)+'</p>'
 +(v.caps.length?'<div class="caps" role="group" aria-label="Capítulos">'+v.caps.map(c=>'<button class="cap" type="button" data-t="'+c[0]+'"><i>'+fmt(c[0])+'</i>'+esc(c[1])+'</button>').join('')+'</div>':'')
 +'<div class="ctl"><div class="seg"><button class="btn nav" id="prev" type="button"'+(i?'':' disabled')+'>← Anterior</button><button class="btn nav" id="next" type="button"'+(sg?'':' disabled')+'>Siguiente →</button></div>'
 +''
 +'<span class="sp"></span><button class="btn act" id="mk" type="button">'+(vistos[s]?'✓ Visto':'Marcar como visto')+'</button>'
 +'<a class="btn lnk '+(v.teoria?'teo':'ej')+'" href="'+(v.teoria?'tema/'+v.tema+'.html':'ej/'+v.s+'.html')+'">'+(v.teoria?'Ver el tema '+v.tema:'Ver el ejercicio')+' →</a></div></div></div>'
 +'<aside class="side"><input id="q" type="search" placeholder="Buscar vídeo…" value="'+esc(window._q||'')+'" aria-label="Buscar vídeo">'+lista+'</aside></div>';
 const vid=$('#vid'),pw=$('#pw'),nx=$('#nx');
 const stop=()=>{clearInterval(window._nxt);if(nx)nx.hidden=true};
 vid.onended=()=>{vistos[s]=1;save();if(sg&&$('#auto').checked){let n=5;$('#cd').textContent=n;nx.hidden=false;window._nxt=setInterval(()=>{n--;$('#cd').textContent=n;if(n<=0){clearInterval(window._nxt);location.hash=sg.s}},1000)}};
 vid.onplay=stop;vid.onseeking=stop;
 if(nx){$('#nxgo').onclick=()=>{clearInterval(window._nxt);location.hash=sg.s};$('#nxno').onclick=stop}
 vid.play().catch(()=>{});
 const caps=[...document.querySelectorAll('.cap')];
 caps.forEach(b=>b.onclick=()=>{vid.currentTime=+b.dataset.t;vid.play()});
 const marca=()=>{let cur=null;caps.forEach(b=>{if(+b.dataset.t<=vid.currentTime+.3)cur=b});caps.forEach(b=>b.classList.toggle('on',b===cur))};
 vid.ontimeupdate=marca;vid.onseeked=marca;marca();
 $('#prev').onclick=()=>{if(i)location.hash=V[i-1].s};$('#next').onclick=()=>{if(sg)location.hash=sg.s};
 $('#auto').onchange=e=>{window._auto=e.target.checked};
 const fsi=()=>{$('#fs').innerHTML=(document.fullscreenElement||pw.classList.contains('cine'))?I.fso:I.fs};
 const cine=on=>{pw.classList.toggle('cine',on);document.body.classList.toggle('cine-on',on);fsi()};
 document.addEventListener('fullscreenchange',fsi);
 const toggleFs=()=>{
  if(document.fullscreenElement){document.exitFullscreen();return}
  if(pw.classList.contains('cine')){cine(false);return}
  const f=pw.requestFullscreen||pw.webkitRequestFullscreen;
  if(!f){cine(true);return}
  try{const p=f.call(pw);if(p&&p.catch)p.catch(()=>cine(true))}catch(e){cine(true)}
  setTimeout(()=>{if(!document.fullscreenElement&&!pw.classList.contains('cine'))cine(true)},350)};
 $('#fs').onclick=toggleFs;
 const pp=$('#pp'),sk=$('#sk'),tm=$('#tm'),mu=$('#mu'),pop=$('#pop');
 const ff=t=>{t=Math.floor(t||0);return Math.floor(t/60)+':'+String(t%60).padStart(2,'0')};
 const upd=()=>{const d=vid.duration||0;sk.value=d?vid.currentTime/d*1000:0;tm.textContent=ff(vid.currentTime)+' / '+ff(d)};
 const est=()=>{pp.innerHTML=vid.paused?I.play:I.pause;pp.setAttribute('aria-label',vid.paused?'Reproducir':'Pausar');pw.classList.toggle('paused',vid.paused)};
 ['timeupdate','loadedmetadata','durationchange'].forEach(n=>vid.addEventListener(n,upd));
 ['play','pause','ended'].forEach(n=>vid.addEventListener(n,est));est();upd();
 const tgl=()=>vid.paused?vid.play():vid.pause();
 pp.onclick=tgl;vid.onclick=tgl;
 sk.oninput=()=>{if(vid.duration)vid.currentTime=sk.value/1000*vid.duration};
 const vl=$('#vl');
 const vi=()=>{const m=vid.muted||vid.volume===0;mu.innerHTML=m?I.mute:vid.volume<.5?I.vol1:I.vol;vl.value=m?0:vid.volume;window._vol=vid.volume;window._mut=vid.muted};
 if(window._vol!=null){vid.volume=window._vol;vid.muted=!!window._mut}
 vid.addEventListener('volumechange',vi);vi();
 mu.onclick=()=>{if(vid.muted||vid.volume===0){vid.muted=false;if(vid.volume===0)vid.volume=.5}else vid.muted=true};
 vl.oninput=()=>{vid.volume=+vl.value;vid.muted=vid.volume===0};
 $('#mb').onclick=e=>{e.stopPropagation();pop.hidden=!pop.hidden};
 document.onclick=e=>{if(!e.target.closest('.mn'))pop.hidden=true};
 pop.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{vid.playbackRate=+b.dataset.v;pop.querySelectorAll('[data-v]').forEach(x=>x.classList.toggle('on',x===b))});
 const tt=vid.textTracks[0];if(tt)tt.mode='showing';
 const cc=$('#cc');if(cc)cc.onchange=()=>{tt.mode=cc.checked?'showing':'hidden'};$('#xit').onclick=()=>cine(false);vid.ondblclick=toggleFs;
 window._key=e=>{if(e.target.closest('input,textarea'))return;if(e.key==='f'||e.key==='F')toggleFs();else if(e.key==='m'||e.key==='M')mu.click();else if(e.key==='k'||(e.key===' '&&!e.target.closest('button'))){e.preventDefault();tgl()}else if(e.key==='ArrowRight')vid.currentTime+=5;else if(e.key==='ArrowLeft')vid.currentTime-=5;else if(e.key==='Escape'&&pw.classList.contains('cine'))cine(false)};
 $('#mk').onclick=()=>{vistos[s]?delete vistos[s]:vistos[s]=1;save();const t=vid.currentTime;sala(s);$('#vid').currentTime=t;$('#vid').pause()};
 const qi=$('#q');qi.oninput=()=>{window._q=qi.value;const p=qi.selectionStart,t=vid.currentTime,pl=!vid.paused;sala(s);const n=$('#q');n.focus();n.setSelectionRange(p,p);$('#vid').currentTime=t;if(!pl)$('#vid').pause()};
 window.scrollTo({top:0});
}
function ruta(){const h=decodeURIComponent(location.hash.slice(1));if(h&&idx(h)>=0)sala(h);else menu()}
window.addEventListener('hashchange',ruta);document.addEventListener('keydown',e=>{if(window._key&&$('#vid'))window._key(e)});ruta();
"""


def pagina_videos(ej, slugs):
    datos = datos_videos(ej, slugs)
    n_min = round(sum(v["d"] for v in datos) / 60)
    cuerpo = (f'<div class="wrap vv"><div class="crumbs"><a class="back" href="index.html" data-back>← Volver</a><a href="index.html">Inicio</a>›<span>Vídeos</span></div>'
              f'<div id="vroot"><noscript>Esta página necesita JavaScript para listar los {len(datos)} vídeos ({n_min} min).</noscript></div></div>')
    js = VIDEOS_JS.replace("__DATA__", json.dumps(datos, ensure_ascii=False).replace("</", "<\\/"))
    return pagina("Vídeos de Diseño de Algoritmos UCM | StudIA", cuerpo, "", js,
                  "Vídeos paso a paso de todos los ejercicios de Diseño de Algoritmos de la FDI UCM, con subtítulos y capítulos.", ruta="videos.html")


def volver_herr(t):
    """Botón fijo de las herramientas: siempre al menú del tema (nunca a «atrás», que podía caer en los apuntes)."""
    return (f'<a href="../tema/{t}.html" class="volver-tema" '
            'style="position:fixed;left:12px;bottom:12px;z-index:99;font:600 14px system-ui,sans-serif;background:#151d31;color:#e7ecf7;border:1px solid #2a3556;'
            f'padding:9px 16px;border-radius:999px;text-decoration:none;box-shadow:0 8px 22px rgba(0,0,0,.35)">← Volver al tema {t}</a>') if t else (
            '<a href="../index.html#herramientas" class="volver-tema" '
            'style="position:fixed;left:12px;bottom:12px;z-index:99;font:600 14px system-ui,sans-serif;background:#151d31;color:#e7ecf7;border:1px solid #2a3556;'
            'padding:9px 16px;border-radius:999px;text-decoration:none;box-shadow:0 8px 22px rgba(0,0,0,.35)">← Volver a la web</a>')


SIN_SUBRAYADO = ('<style>a.back,a.btn,.btn,a.card,.volver-tema,.foot a{text-decoration:none!important}'
                 'a.back:hover,a.btn:hover,.btn:hover,.volver-tema:hover{text-decoration:none!important}</style>')


def limpiar_herr(h, t):
    h = re.sub(r"\s*\(A\. Verdejo[^)]*\)", "", h)
    h = h.replace("</head>", SIN_SUBRAYADO + "</head>", 1)
    h = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + volver_herr(t), h, count=1)
    return h


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
    n_juez = sum(1 for i, _ in lista if slugs[i] in JUECES)
    juez = (f'<span class="chip">@@i:check@@ Juez en {n_juez}/{n}</span>' if n_juez
            else '<span class="chip mute">@@i:check@@ Juez pronto</span>')
    return (f'<a class="tcard" href="tema/{t}.html" data-ids="{ids}" data-tema="{t}" style="--b:{color_de(t)}">'
            f'<div class="th"><div><span class="n">{"✎" if t == EVAL else f"{t:02d}"}</span><b>{esc(info["nombre"])}</b></div><span class="est" data-est>Sin empezar</span></div>'
            f'<div class="met"><div class="sol"><div class="l"><span>Con solución</span><b>{n_sol}/{n}</b></div><div class="prog"><i style="width:{pct_sol}%"></i></div></div>'
            f'<div><div class="l"><span>Tu progreso</span><b data-txt>0/{n} · 0%</b></div><div class="prog"><i data-bar></i></div></div></div>'
            f'<div class="tcf"><span class="chip">@@i:code@@ {plural(n, "ejercicio", "ejercicios")}</span>{herr}{vid}{juez}</div></a>')


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
            f'<aside class="teo-panel" id="teoPanel" aria-label="Teoría · {tema_corto(t)}" hidden><div class="teo-bar"><b>Teoría · {tema_corto(t)}</b>'
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
        acc.append(f'<a class="btn" href="{url_herr(info["herr"], "../")}">@@i:tool@@ Herramienta interactiva</a>')
    for c in info["cab"]:
        if c in cabs:
            acc.append(f'<a class="btn" href="../estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>')
    bloque = next((b[0] for b in BLOQUES if t in b[1]), "")
    prev_t = t - 1 if t - 1 in nombres_temas else None
    next_t = t + 1 if t + 1 in nombres_temas else None
    pager = ('<div class="pager">' + (f'<a class="btn" href="{prev_t}.html">← {esc(tema_largo(prev_t, nombres_temas[prev_t]))}</a>' if prev_t else "<span></span>")
             + (f'<a class="btn" href="{next_t}.html">{esc(tema_largo(next_t, nombres_temas[next_t]))} →</a>' if next_t else "<span></span>") + "</div>")
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
        principales.append(f'<a class="arow main" href="../ej/{s_}.html"><span class="pic">@@i:book@@</span><span class="at"><b>Apuntes del tema</b><small>Teoría explicada paso a paso</small></span>@@i:arrow@@</a>')
    if herr_ok:
        principales.append(f'<a class="arow main alt" href="{url_herr(info["herr"], "../")}"><span class="pic">@@i:tool@@</span><span class="at"><b>Herramienta interactiva</b><small>Prueba el algoritmo paso a paso</small></span>@@i:arrow@@</a>')
    for k, (r, nom, tam) in enumerate(docs):
        pdfs.append(f'<div class="arow"><span class="pic">@@i:pdf@@</span><span class="at"><b>{esc(nom)}</b><small>PDF · {tam_legible(tam)}</small></span>'
                    f'<button class="mb" type="button" data-teo="{k}" title="Abrir aquí" aria-label="Abrir {esc(nom)} aquí">@@i:book@@</button>'
                    f'<a class="mb" href="{url_teoria(t, r, "../")}" download title="Descargar" aria-label="Descargar {esc(nom)}">@@i:download@@</a></div>')
    aprender = principales + pdfs
    pdfsec = (f'<section class="pdfsec" id="teoria-pdf" aria-label="Teoría en PDF"><div class="mh"><h2>Teoría en PDF <span class="cnt">{len(pdfs)}</span></h2></div><div class="alist">{"".join(pdfs)}</div></section>' if pdfs else "")
    recursos = [f'<a class="chip" href="../estructuras/{quote(c)}.html">@@i:code@@ {esc(c)}</a>' for c in info["cab"] if c in cabs]
    lateral = (f'<aside class="tside">'
               f'<div class="sbox prog-box" data-ids="{ids}" style="--c:{color}"><div class="ph"><small>Tu progreso</small><b data-pct>0%</b></div><div class="prog"><i data-bar></i></div>'
               f'<span class="pt" data-hechos>0 de {n} hechos</span><a class="btn prim sig" data-sig href="#ejercicios">Empezar con {esc(lista[0][1]["id"]) if lista else ""} →</a></div>'
               + (f'<details class="sbox aprende" data-aprende><summary><h2>Aprende</h2></summary><div class="alist main">{"".join(principales)}</div>{('<h3 class="sub">PDFs de teoría</h3><div class="alist">' + "".join(pdfs) + '</div>') if pdfs else ""}</details>' if aprender else '')
               + (f'<div class="sbox"><h2>Plantillas y código</h2><div class="rec">{"".join(recursos)}</div></div>' if recursos else '')
               + '</aside>')
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../index.html#temas" data-back>← Volver</a><a href="../index.html">Inicio</a>›<a href="../index.html#temas">{esc(bloque)}</a>›<span>{tema_corto(t)}</span></div>'
              f'<div class="thead" data-ids="{ids}"><div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center"><span class="tag">{esc(bloque)}</span><span class="est" data-est>Sin empezar</span></div>'
              f'<h1>{esc(tema_largo(t, info["nombre"]))}</h1><p class="lede">{esc(info["resumen"])}</p></div>'
              f'<div class="tlay">{lateral}<main class="tmain">{vhero}{pdfsec}<div class="mh" id="ejercicios"><h2>Ejercicios <span class="cnt">{n}</span></h2>'
              f'<div class="filters"><button class="chip on" data-f="todos">Todos</button><button class="chip" data-f="pend">Pendientes</button><button class="chip" data-f="hechos">Hechos</button><button class="chip" data-fv>@@i:video@@ Con vídeo</button></div></div>'
              f'<div id="p-ejercicios">{"".join(filas)}<p class="vacio" id="sin">Ningún ejercicio coincide con el filtro.</p></div>'
              f'<p class="notas">Tests del profe y propios: próximamente.</p></main></div>{pager}</div>{teoria_panel(t, "../")}')
    titulo = f'{tema_largo(t, info["nombre"])} | Diseño de Algoritmos UCM'
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
    ctx_tema = {}
    for i, e in enumerate(ej):
        ctx_tema.setdefault(e["tema"], []).append((slugs[i], e))
    for i, e in enumerate(ej):
        ant = (slugs[i - 1], f'{ej[i - 1]["id"]} · {ej[i - 1]["titulo"]}') if i > 0 else None
        sig = (slugs[i + 1], f'{ej[i + 1]["id"]} · {ej[i + 1]["titulo"]}') if i + 1 < len(ej) else None
        (OUT / "ej" / f"{slugs[i]}.html").write_text(pagina_ejercicio(e, slugs[i], ant, sig, ctx_tema[e["tema"]]), encoding="utf-8", newline="\n")
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
            t_herr = next((t for t in TEMAS if TEMAS[t]["herr"] == p.name), None)
            h = limpiar_herr(h, t_herr)
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

    # laboratorio
    (OUT / "lab").mkdir()
    n_ej_tema = {t: sum(1 for _, e in por_tema[t] if not es_teoria(e)) for t in TEMAS}
    cpt = cabs_por_tema(cabs)
    temas_lab = []
    herr_dict = {x[0]: x for x in herr}
    for f, a_, b_, c_ in herr:
        t_ = next((t for t in TEMAS if TEMAS[t]["herr"] == f), None)
        if t_ is None or not por_tema.get(t_):
            continue
        claves = [k for k in LABS if k.split("|")[0] == f]
        if not claves:
            temas_lab.append((t_, b_, f"herramientas/{f}", None, [c for c in cpt[t_]], c_, False))
            continue
        for k in claves:
            lab = LABS[k]
            vista = k.split("|")[1] if "|" in k else ""
            otros = lab["extra"] if "extra" in lab else [c for c in cpt[t_] if c != lab["cab"]]
            (OUT / "lab" / f"{lab['slug']}.html").write_text(pagina_lab(f, lab, t_, TEMAS[t_], por_tema[t_], slugs, c_, otros, vista), encoding="utf-8", newline="\n")
            temas_lab.append((t_, lab["titulo"], f"lab/{lab['slug']}.html", lab["cab"], otros, lab.get("desc", c_), True))
    (OUT / "laboratorio.html").write_text(pagina_laboratorio(temas_lab, n_ej_tema), encoding="utf-8", newline="\n")

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
    tools_html = "".join(f'<a class="tool" href="{url_herr(f)}"><span class="n">{esc(a)}</span><b>{esc(b)}</b><span class="d">{esc(c)}</span></a>' for f, a, b, c in herr)
    est_html = "".join(f'<a class="chip" href="estructuras/{quote(c)}.html">{esc(c)}</a>' for c in cabs)
    sha = commit_info()
    ahora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    n_temas = sum(1 for t in TEMAS if por_tema.get(t))
    cuerpo = f"""<div class="wrap">
<div class="hero"><p class="eyebrow">FDI UCM · Informática · Computadores · Software</p>
<h1>Diseño de Algoritmos: ejercicios resueltos, vídeos y herramientas</h1>
<p class="lede">Todos los problemas del juez con su enunciado, la solución en C++, la explicación del planteamiento, el vídeo paso a paso de cada uno y herramientas interactivas para entender cada estructura de datos.</p>
<label class="search">@@i:arrow@@<input id="q" type="search" placeholder="Buscar ejercicio (nombre, número, técnica…)" aria-label="Buscar ejercicio"><kbd>/</kbd></label>
<a class="guiab" href="guia.html"><b>¿Primera vez aquí?</b><span>Guía de 1 minuto: qué es cada cosa y por dónde empezar</span><em>Ver la guía →</em></a></div>
<div class="acc"><a class="accb lab" href="laboratorio.html"><b>Laboratorio</b><span>{len(LABS)} simuladores paso a paso con código y coste</span><em>Abrir →</em></a><a class="accb vid" href="videos.html"><b>Vídeos</b><span>{n_vid} vídeos paso a paso, con subtítulos</span><em>Ver →</em></a></div>
<div class="sm" data-resumen>
<div class="box hi"><small>Tu progreso</small><b data-r="pct">0%</b><span data-r="txt"></span><div class="prog"><i data-r="bar"></i></div></div>
<div class="box"><small>Temas completados</small><b><u data-r="comp">0</u><em> / {n_temas}</em></b><span data-r="curso">0 en curso</span></div>
<div class="box"><small>Con solución</small><b>{round(n_sol / len(solo_ej) * 100)}%</b><span>{n_sol} de {len(solo_ej)} ejercicios</span></div>
<div class="box"><small>Tests</small><b>0</b><span>del profe y propios · pronto</span></div></div>
<section id="resultados" hidden><h2 id="res-t" style="margin-bottom:12px"></h2><div id="res-l"></div><p class="vacio" id="vacio">Ningún ejercicio coincide con la búsqueda.</p></section>
<div id="temas">{"".join(bloques_html)}</div>
<section class="bloque" id="laboratorio"><h2>Laboratorio</h2><p class="lede">Cada estructura de datos con su simulador paso a paso, el código de la asignatura, el coste de cada operación y ejercicios.</p><div class="tools">{tools_html}</div><p style="margin-top:12px"><a class="btn primary" href="laboratorio.html">Abrir el laboratorio →</a></p></section>
<section class="bloque" id="videos"><h2>Vídeos</h2><p class="lede">Un vídeo paso a paso por cada ejercicio y por cada tema ({n_vid} en total), que se ven aquí mismo, con subtítulos.</p><p><a class="btn primary" href="videos.html">Ver todos los vídeos →</a></p></section>
<footer>Material de estudio independiente, no afiliado a la UCM</footer></div>"""
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
    (OUT / "guia.html").write_text(pagina_guia(n_temas, len(solo_ej), len(herr), n_vid), encoding="utf-8", newline="\n")
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
                  f'<a href="../index.html">Inicio</a>›<a href="../tema/{e["tema"]}.html">{tema_corto(e["tema"])}</a>›<span>{esc(ej_id)} · probar</span></div>'
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
