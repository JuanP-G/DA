# EJ 05-2 · La máquina calculadora

📄 [Enunciado](<../Enunciados/prob-La máquina calculadora.pdf>) · 💻 [Solución](EJ_05-2.cpp) · 🎬 [Vídeo](../../Videos/05-2_maquina_calculadora.mp4)

## Qué piden
Marcador de 4 dígitos con botones `+1`, `×2` y `÷3` (módulo 10.000, división entera): mínimo de pulsaciones de un número inicial a uno final.

## Cómo se plantea
Un **`Digrafo`** de 10.000 vértices (los números 0…9.999), tres aristas de salida por vértice, que se construye **una sola vez** al empezar el programa (es el mismo para todos los casos):

```text
x → (x + 1) % 10000      x → (x * 2) % 10000      x → x / 3
```

Mínimo de pulsaciones = camino más corto ⇒ **BFS** desde el inicial sobre `g.ady(x)`, parando al sacar el final.

## Por qué así
- **Dirigido:** 5.000 → 0 con `×2`, pero desde 0 no se llega a 5.000 con un botón.
- **Lazos:** en el 0, `×2` y `÷3` dan 0 otra vez; no pasa nada, ya está visitado.
- **Siempre hay camino:** con `+1` se llega a cualquier número.
- **inicial == final ⇒ 0** (`dist[inicial] = 0`).
- El grafo no depende del caso: se construye una vez (30.000 aristas) y cada caso solo hace su BFS.

## Traza del ejemplo 3 (`9999 → 6666`)
```text
saca 9999:  +1 → 0   ×2 → 9998   ÷3 → 3333        (d=1)
saca 0:     +1 → 1 (nuevo)  ×2, ÷3 → 0 (visto)    (d=2)
saca 9998:  ×2 → 9996  ÷3 → 3332                  (d=2)
saca 3333:  +1 → 3334  ×2 → 6666  ÷3 → 1111       (d=2)
...         salen 1, 9996, 3332, 3334 y por fin 6666 = final  ⇒  2   (÷3 y ×2)
```

## Coste
Construir el grafo: **O(10.000)** una vez. Cada caso: **O(10.000)** (3 sucesores por vértice), ~3·10⁴ operaciones; unas 6·10⁷ con los 2.000 casos.
