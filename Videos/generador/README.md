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
