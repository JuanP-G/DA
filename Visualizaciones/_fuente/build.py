#!/usr/bin/env python3
"""
Genera las páginas finales a partir de los fragmentos de _fuente/.

  python3 build.py            -> escribe ../<nombre>.html (páginas autónomas para abrir en el navegador / GitHub Pages)
                                 y _artifact/<nombre>.html (mismo contenido sin <html>/<head>, listo para publicar como artifact)

Un fragmento (<nombre>.frag.html) contiene: <title>, <style> propio, el <body> de la página y un <script> con el
marcador /*SHARED_JS*/ donde se inserta shared.js. El marcador /*SHARED_CSS*/ dentro del <style> inserta shared.css.
"""
import pathlib, re, sys

AQUI = pathlib.Path(__file__).parent
CSS = (AQUI / "shared.css").read_text(encoding="utf-8")
JS = (AQUI / "shared.js").read_text(encoding="utf-8")
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">'

def main():
    out_art = AQUI / "_artifact"
    out_art.mkdir(exist_ok=True)
    for frag in sorted(AQUI.glob("*.frag.html")):
        nombre = frag.name.replace(".frag.html", "")
        s = frag.read_text(encoding="utf-8").replace("/*SHARED_CSS*/", CSS).replace("/*SHARED_JS*/", JS)
        title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
        cuerpo = re.sub(r"<title>.*?</title>", "", s, count=1, flags=re.S)
        (out_art / f"{nombre}.html").write_text(f"<title>{title}</title>\n{FONTS}\n{cuerpo}", encoding="utf-8")
        pagina = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  f'<title>{title}</title>\n{FONTS}\n</head>\n<body>\n{cuerpo}\n</body>\n</html>\n')
        (AQUI.parent / f"{nombre}.html").write_text(pagina, encoding="utf-8")
        print("ok", nombre, len(pagina) // 1024, "KB")

if __name__ == "__main__":
    main()
