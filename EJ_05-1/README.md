# EJ 05-1 · Juego de Transformación Modular

📄 [Enunciado](<../Ejercicios juez/5-Grafos dirigidos/prob-Juego de Transformación Modular.pdf>) · 💻 [Solución](EJ_05-1.cpp) · 🎬 [Vídeo](../Videos/05-1_transformacion_modular.mp4)

## Qué piden
Con N operaciones `x ← (aᵢ·x + bᵢ) mod M`, el mínimo de jugadas para pasar de `S` a `T` (o `-1`).

## Cómo se plantea
Un **`Digrafo`** (`Digrafo.h`): los vértices son los números `0 … M-1` y cada operación da una arista `x → (aᵢ·x + bᵢ) mod M`. Mínimo de jugadas = camino más corto de `S` a `T` ⇒ **BFS** desde `S`.

0. Se construye el grafo: para cada `x` y cada operación, `g.ponArista(x, (a·x+b) % M)`.
1. `dist[S] = 0` y `S` a la cola.
2. Se saca `x`; si es `T`, ya tiene su distancia mínima y se para.
3. Para cada sucesor `y` en `g.ady(x)`: si `dist[y] == -1`, `dist[y] = dist[x] + 1` y `y` entra en la cola.
4. Respuesta: `dist[T]` (queda en `-1` si no se alcanza).

## Por qué así
- **Construir el grafo cuesta:** con `M = 10.000` y `N = 100` son un millón de aristas por caso. Alternativa sin `Digrafo`: calcular el vecino al vuelo dentro del BFS (más rápido, pero no usa la estructura de la asignatura).
- **Es dirigido:** que `x → y` no implica que `y → x`.
- **`S == T` ⇒ 0**, sin tratarlo aparte (`dist[S] = 0`). Con `M = 1` solo existe el 0.
- `a·x + b < 10⁸`, cabe en un `int`.
- Se quitan las operaciones repetidas (mismos `a` y `b` módulo `M`) porque no añaden aristas.

## Traza del ejemplo 2 (`M=5, S=1, T=0`, operaciones `2x+1` y `3x+1`)
```text
saca 1:  2·1+1 = 3 (nuevo, d=1)    3·1+1 = 4 (nuevo, d=1)
saca 3:  2·3+1 = 2 (nuevo, d=2)    3·3+1 = 0 (nuevo, d=2)
saca 4:  4 y 3, ya visitados
saca 2:  0 y 2, ya visitados
saca 0 = T  ⇒  2
```
Ejemplo 3 (`M=10, S=2, T=1`, `2x`): solo se recorre 2→4→8→6→2, al 1 no llega nadie ⇒ **-1**.

## Coste
**O(M · N)** por caso: construir el `Digrafo` (M·N aristas) y el BFS (que puede cortar al llegar a `T`). En el peor caso adversarial con el máximo de casos, la versión con `Digrafo` tarda ~3 s en las pruebas (la versión sin construir el grafo, ~1,7 s); con casos normales es mucho menos.
