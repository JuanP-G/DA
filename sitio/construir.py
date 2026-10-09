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
    conocidos = {posixpath.dirname(s[1]) for e in ej for s in e["sols"]}
    for d in sorted(RAIZ.glob("*/EJ_0[1-9]-*")):   # <tema>/EJ_0T-N
        if not d.is_dir() or d.relative_to(RAIZ).as_posix() in conocidos:
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
.crumbs{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:.86rem;color:var(--muted);padding-top:16px}
.crumbs a{color:var(--muted);text-decoration:none}.crumbs a:hover{color:var(--blue)}.crumbs .back{font-weight:600;color:var(--ink);margin-right:6px}
.tabs .btn .cnt{font-size:.75rem;color:var(--muted);margin-left:4px}.tabs .btn.off{opacity:.55}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}.bar .grow{flex:1}
.bar .hint{font-size:.85rem;color:var(--muted)}
.btn.prim{background:var(--accent);border-color:var(--accent);color:#fff}:root[data-theme=dark] .btn.prim{color:#1b1400}@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .btn.prim{color:#1b1400}}
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
 const box=document.createElement('div');box.className='codebox';if(pre.id)box.id=pre.id;box.dataset.src=src;
 const head=document.createElement('div');head.className='fname';head.innerHTML='<span>'+esc(name)+'</span>';
 box.appendChild(head);
 src.split('\n').forEach((l,i)=>{const d=document.createElement('div');d.className='ln';d.innerHTML='<i>'+(i+1)+'</i><span>'+paint(l)+'</span>';box.appendChild(d)});
 pre.replaceWith(box)});
"""

COMUN_JS = r"""
function toast(t){const e=document.getElementById('toast');if(!e)return;e.textContent=t;e.classList.add('on');clearTimeout(e._t);e._t=setTimeout(()=>e.classList.remove('on'),1600)}
function copiar(txt,btn){const ok=()=>{toast('Copiado al portapapeles');if(btn){const o=btn.textContent;btn.textContent='¡Copiado!';setTimeout(()=>btn.textContent=o,1400)}};
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
 const z=new JSZip(),txt=zb.textContent;zb.disabled=true;
 try{let i=0;for(const [url,ruta] of lista){zb.textContent='Preparando… '+(++i)+'/'+lista.length;const r=await fetch(url);if(!r.ok)throw new Error(url);z.file(nombre+'/'+ruta,await r.blob(),{binary:true})}
  zb.textContent='Comprimiendo…';const blob=await z.generateAsync({type:'blob',compression:'STORE'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=nombre+'.zip';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},2000);toast('Descarga lista')}
 catch(e){toast('No se ha podido generar el zip')}finally{zb.disabled=false;zb.textContent=txt}};
"""

JSZIP = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js" defer></script>'


def pagina(titulo, cuerpo, prefijo="", extra_js="", desc="", head=""):
    nav = (f'<nav class="nav"><div class="wrap"><b>DA · DISEÑO DE ALGORITMOS</b>'
           f'<a href="{prefijo}index.html">Inicio</a><a href="{prefijo}index.html#herramientas">Herramientas</a>'
           + "".join(f'<a href="{prefijo}index.html#tema{t}">Tema {t}</a>' for t in TEMAS)
           + f'<a href="{prefijo}index.html#estructuras">Estructuras</a><a href="{prefijo}videos.html">Vídeos</a></div></nav>')
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}">{FONTS}<style>{CSS}</style>{head}</head><body>{nav}{cuerpo}<div class="toast" id="toast"></div><script>{COMUN_JS}{extra_js}</script></body></html>')


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


def pagina_ejercicio(e, slug, ant=None, sig=None):
    carpeta = posixpath.dirname(e["sols"][0][1]) if e["sols"] else None
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

    # 1 · Enunciado
    if e["pdf"]:
        pdf = href_sitio(e["pdf"], True)
        p_enun = (f'<div class="bar">{descargar(e["pdf"], "⬇ Descargar PDF")}<a class="btn" href="{pdf}" target="_blank" rel="noopener">↗ Abrir en otra pestaña</a>'
                  f'<span class="hint">{tam_legible((RAIZ / e["pdf"]).stat().st_size)}</span></div>'
                  f'<iframe class="pdf" src="{pdf}" title="Enunciado {esc(e["id"])}"></iframe>'
                  f'<p class="hint" style="color:var(--muted);font-size:.85rem">¿No se ve? En el móvil los PDF no se muestran dentro de la página: usa «Abrir en otra pestaña» o «Descargar PDF».</p>')
        ficheros_zip.append((pdf, "enunciado.pdf"))
    else:
        p_enun = '<div class="nada">Este ejercicio no tiene enunciado en PDF.</div>'

    # 2 · Código
    if codigos:
        subs = "".join(f'<button class="btn{" on" if i == 0 else ""}" data-sub="c{i}" data-group="c">{esc(posixpath.basename(r))}</button>' for i, r in enumerate(codigos))
        cods = []
        for i, r in enumerate(codigos):
            txt = leer_texto(r)
            nombre = posixpath.basename(r)
            tipo = "solución" if r.endswith(".cpp") else "estructura de datos"
            cods.append(f'<div data-subpane="c{i}" style="display:{"block" if i == 0 else "none"}"><div class="bar"><button class="btn" data-copy="src{i}">⧉ Copiar código</button>'
                        f'{descargar(r, "⬇ Descargar " + esc(nombre))}<span class="hint">{tipo} · {txt.count(chr(10)) + 1} líneas</span></div>'
                        f'<pre data-code="{esc(nombre)}" id="src{i}">{esc(txt)}</pre></div>')
            ficheros_zip.append((href_sitio(r, True), ("codigo/" if r.endswith(".cpp") else "estructuras/") + nombre))
        p_cod = f'<div class="sub">{subs if len(codigos) > 1 else ""}</div>{"".join(cods)}'
    else:
        p_cod = '<div class="nada">Todavía no hay código para este ejercicio.</div>'

    # 3 · Explicación
    if e["readme"]:
        crudo = (RAIZ / e["readme"]).read_text(encoding="utf-8")
        p_exp = (f'<div class="bar"><button class="btn" data-copy="md-src">⧉ Copiar (Markdown)</button>{descargar(e["readme"], "⬇ Descargar .md", "")}</div>'
                 f'<div class="md">{render_md(e["readme"])}</div><script type="text/plain" id="md-src">{esc(crudo)}</script>')
        ficheros_zip.append((href_sitio(e["readme"], True), "explicacion.md"))
    else:
        p_exp = '<div class="nada">Todavía no hay explicación escrita para este ejercicio.</div>'

    # 4 · Vídeo
    if e["video"]:
        vurl = href_sitio(e["video"], True)
        vtt, caps = media_video(e["video"])
        track = f'<track kind="subtitles" srclang="es" label="Español" src="../{quote(vtt)}" default>' if vtt else ""
        lista_caps = ("<div class='caps'><b>Capítulos</b>" + "".join(f'<button data-t="{t:.2f}"><span>{mmss(t)}</span>{esc(ti)}</button>' for t, ti in caps) + "</div>") if caps else ""
        p_vid = (f'<div class="bar">{descargar(e["video"], "⬇ Descargar vídeo")}<span class="hint">{tam_legible((RAIZ / e["video"]).stat().st_size)} · subtítulos con el botón CC del reproductor</span></div>'
                 f'<div class="{"vid" if caps else ""}"><video controls preload="metadata" playsinline src="{vurl}">{track}Tu navegador no puede reproducir el vídeo: <a href="{vurl}">descárgalo</a>.</video>{lista_caps}</div>')
        ficheros_zip.append((vurl, "video.mp4"))
    else:
        p_vid = '<div class="nada">Este ejercicio todavía no tiene vídeo.</div>'

    tabs = [("enunciado", "📄 Enunciado", bool(e["pdf"]), p_enun), ("codigo", "💻 Código", bool(codigos), p_cod),
            ("explicacion", "📘 Explicación", bool(e["readme"]), p_exp), ("video", "🎬 Vídeo", bool(e["video"]), p_vid)]
    pref = "explicacion" if e["readme"] else ("codigo" if codigos else "enunciado")
    botones = "".join(f'<button class="btn{"" if hay else " off"}{" pref" if i == pref else ""}" data-tab="{i}">{t}</button>' for i, t, hay, _ in tabs)
    panes = "".join(f'<div class="pane" id="p-{i}">{c}</div>' for i, _, _, c in tabs)

    acc = []
    if ficheros_zip:
        total = 0
        for url, _ in ficheros_zip:
            pass
        acc.append(f'<button class="btn prim" id="zip" data-name="{esc(e["id"] + " " + e["titulo"])}" data-files="{esc(json.dumps(ficheros_zip, ensure_ascii=False))}">⬇ Descargar todo (.zip)</button>')
    if (RAIZ / "Visualizaciones" / herr).exists():
        acc.append(f'<a class="btn" href="../herramientas/{herr}">🧩 Herramienta interactiva del tema</a>')
    contenido_zip = ", ".join(x for x, ok in (("enunciado", e["pdf"]), ("código", codigos), ("explicación", e["readme"]), ("vídeo", e["video"])) if ok)

    pager = '<div class="pager">' + (f'<a class="btn" href="{ant[0]}.html">← {esc(ant[1])}</a>' if ant else "<span></span>") + \
            (f'<a class="btn" href="{sig[0]}.html">{esc(sig[1])} →</a>' if sig else "<span></span>") + "</div>"
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../index.html#tema{tema}" data-back>← Volver</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../index.html#tema{tema}">Tema {tema}</a>›<span>{esc(e["id"])}</span></div>'
              f'<div class="ejhead"><span class="tag">Tema {tema} · {esc(TEMAS[tema]["nombre"])}</span>'
              f'<h1>{esc(e["id"])} · {esc(e["titulo"])}</h1><p class="lede">{md_inline(e["idea"])}</p>'
              f'<div class="acc">{"".join(acc)}</div>'
              + (f'<p class="hint" style="margin:0;color:var(--muted);font-size:.85rem">El zip incluye: {contenido_zip}.</p>' if ficheros_zip else "")
              + f'</div><div class="tabs">{botones}</div>{panes}{pager}</div>')
    return pagina(f'{e["id"]} {e["titulo"]}', cuerpo, "../", HIGHLIGHT_JS + TABS_JS, e["idea"], JSZIP)


def pagina_cabecera(nombre):
    rel = f"Estructuras de datos/{nombre}"
    herr = next((TEMAS[t]["herr"] for t in TEMAS if nombre in TEMAS[t]["cab"]), None)
    extra = f'<a class="btn" href="../herramientas/{herr}">🧩 Herramienta interactiva</a>' if herr and (RAIZ / "Visualizaciones" / herr).exists() else ""
    txt = leer_texto(rel)
    cuerpo = (f'<div class="wrap"><div class="crumbs"><a class="back" href="../index.html#estructuras" data-back>← Volver</a>'
              f'<a href="../index.html">Inicio</a>›<a href="../index.html#estructuras">Estructuras</a>›<span>{esc(nombre)}</span></div>'
              f'<div class="ejhead"><span class="tag">Estructura de datos</span><h1>{esc(nombre)}</h1>'
              f'<div class="acc"><button class="btn" data-copy="src0">⧉ Copiar código</button>{descargar(rel, "⬇ Descargar " + esc(nombre))}{extra}</div></div>'
              f'<pre data-code="{esc(nombre)}" id="src0">{esc(txt)}</pre></div>')
    return pagina(nombre, cuerpo, "../", HIGHLIGHT_JS)


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
    return pagina("Vídeos · DA", cuerpo, "", "")


VOLVER_HERR = ('<a href="../index.html#herramientas" onclick="try{if(document.referrer&&new URL(document.referrer).origin===location.origin&&history.length>1){history.back();return false}}catch(e){}" '
               'style="position:fixed;left:12px;bottom:12px;z-index:99;font:600 14px system-ui,sans-serif;background:#151d31;color:#e7ecf7;border:1px solid #2a3556;'
               'padding:8px 12px;border-radius:9px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25)">← Volver a la web</a>')


def chips(e, slug):
    c = []
    if e["pdf"]: c.append(f'<a class="chip p" href="ej/{slug}.html#enunciado">Enunciado</a>')
    if e["sols"]: c.append(f'<a class="chip" href="ej/{slug}.html#codigo">Código</a>')
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
<section class="bloque" id="estructuras"><h2>Estructuras de datos</h2><p class="lede">Las cabeceras que da la asignatura, con visor de código, copiar y descargar.</p><div class="cabs">{est_html}</div></section>
<section class="bloque" id="videos"><h2>Vídeos</h2><p class="lede">{n_vid} vídeos explicativos que se ven aquí mismo, con subtítulos. <a href="videos.html">Ver todos los vídeos →</a></p></section>
<footer>Web generada automáticamente desde el repositorio{" · commit <code>" + esc(sha) + "</code>" if sha else ""} · {ahora}</footer></div>"""
    js = """const q=document.getElementById('q');function filtra(){const v=q.value.trim().toLowerCase();let any=0;
document.querySelectorAll('.tema').forEach(s=>{let vis=0;s.querySelectorAll('.fila').forEach(f=>{const ok=!v||f.dataset.q.includes(v);f.style.display=ok?'':'none';if(ok)vis++});s.style.display=vis?'':'none';any+=vis});
document.getElementById('vacio').style.display=any?'none':'block';try{sessionStorage.setItem('q',q.value)}catch(e){}}
q.oninput=filtra;window.addEventListener('pageshow',()=>{try{const g=sessionStorage.getItem('q');if(g&&!q.value){q.value=g}}catch(e){}if(q.value)filtra()});"""
    (OUT / "index.html").write_text(pagina("DA · Diseño de Algoritmos", cuerpo, "", js, "Ejercicios, soluciones, vídeos y herramientas interactivas de Diseño de Algoritmos"), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")

    # copiar ficheros referenciados + código de cada ejercicio
    for e in ej:
        if e["readme"]: COPIAR.add(e["readme"])
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
