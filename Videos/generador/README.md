# Generador de los vídeos de los temas 4, 5 y 6

Cada `v04_X.py` es el guion de un vídeo: una lista de diapositivas, cada una con su frase de narración. Las trazas de ejecución salen de **simular el mismo algoritmo del `.cpp`** (mismo orden de adyacentes que `Grafo.h`). El código que aparece en pantalla se lee del `.cpp` real, con sus números de línea.

`vidlib.py` dibuja las diapositivas (Pillow), genera la voz (Kokoro, offline; o Piper, la voz antigua) y monta el vídeo con ffmpeg: H.264 + audio AAC + pista de subtítulos en castellano.

## Voz

Desde el vídeo 05-0 se usa **Kokoro** (`pip install kokoro-onnx`), mucho más natural que la voz Piper `es-mls_10246-low` de los vídeos anteriores. Modelos: `kokoro-v1.0.onnx` y `voices-v1.0.bin` de las [releases de kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0).

```bash
export KOKORO_MODEL=/ruta/kokoro-v1.0.onnx KOKORO_VOICES=/ruta/voices-v1.0.bin
export KOKORO_VOICE=ef_dora      # o em_alex (masculina)
```

Sin `KOKORO_MODEL` se usa Piper (`PIPER_MODEL`), como antes.

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


## Vídeo de teoría del tema 6

`v06_teoria.py` genera `../06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4` (con capítulos y subtítulos): relaciones de equivalencia dinámicas, búsqueda rápida, unión rápida, unión por tamaños y compresión de caminos, la autoevaluación 6.1 paso a paso, los ejercicios 06-1 a 06-5, `GrafoValorado.h`, la propiedad del corte, y Kruskal y Prim sobre un grafo de 6 vértices.

- Los ejercicios del tema 6 aún no tienen `.cpp`, así que las trazas salen de **simular los algoritmos en el propio guion** (los resultados coinciden con los ejemplos de los enunciados). El código que se ve en pantalla es el de `Estructuras de datos/ConjuntosDisjuntos.h` y `GrafoValorado.h`.
- Para unión por tamaños se sigue el criterio de desempate de las transparencias (en empate, la raíz de `b` cuelga de la de `a`); la cabecera hace lo contrario y el vídeo lo advierte.

```bash
export KOKORO_MODEL=/ruta/kokoro-v1.0.onnx KOKORO_VOICES=/ruta/voices-v1.0.bin KOKORO_VOICE=ef_dora
python v06_teoria.py --preview   # solo las imágenes
python v06_teoria.py             # genera el mp4 (varios minutos: sintetiza la voz de cada diapositiva)
```
