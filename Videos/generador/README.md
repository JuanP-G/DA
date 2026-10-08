# Generador de los vídeos de los temas 4 y 5

Cada `v04_X.py` es el guion de un vídeo: una lista de diapositivas, cada una con su frase de narración. Las trazas de ejecución salen de **simular el mismo algoritmo del `.cpp`** (mismo orden de adyacentes que `Grafo.h`). El código que aparece en pantalla se lee del `.cpp` real, con sus números de línea.

`vidlib.py` dibuja las diapositivas (Pillow), genera la voz (Piper, offline) y monta el vídeo con ffmpeg: H.264 + audio AAC + pista de subtítulos en castellano.

## Requisitos

- Python 3 con `pillow` y `piper-tts` (`pip install pillow piper-tts`)
- `ffmpeg`
- Una voz de Piper en castellano, por ejemplo `es-mls_10246-low` ([releases de Piper](https://github.com/rhasspy/piper/releases/tag/v0.0.2), fichero `voice-es-mls_10246-low.tar.gz`)

## Uso

```bash
cd Videos/generador
export PIPER_MODEL=/ruta/a/es-mls_10246-low.onnx
python v04_1.py --preview   # solo las imágenes, en preview/ (para revisar el diseño)
python v04_1.py             # genera ../04-1_arboles_libres.mp4
```

## Vídeo de teoría del tema 5

`v05_teoria.py` genera `../05-0_grafos_dirigidos_teoria.mp4` (≈ 23 min, con capítulos y subtítulos): conceptos de grafos dirigidos, TAD `Digrafo`, DFS, BFS, la máquina calculadora (grafo implícito), el grafo de autobuses de la EMT, orden topológico, detección de ciclos y, como extra, componentes fuertemente conexas.

- El código que sale en pantalla se lee de `Estructuras de datos/Digrafo_algoritmos.h` (y `Digrafo.h`, `Digrafo_implicito_calculadora.cpp`); `Digrafo_demo.cpp` comprueba que las trazas simuladas coinciden con la ejecución real.
- `material/emt_ejemplo.cpp` es el ejemplo de `grafoEMT.zip`; `material/emt_resultado.txt` guarda lo que imprime (BFS: 6 paradas; DFS: 2.032).
- `build()` de `vidlib.py` admite ahora `chapters={índice de diapositiva: título}`.

```bash
export PIPER_MODEL=/ruta/a/es-mls_10246-low.onnx
python v05_teoria.py --preview   # solo las imágenes
python v05_teoria.py             # genera el mp4 (tarda unos minutos)
```

