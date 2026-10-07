# EJ 05-3 · Ordenando tareas

📄 [Enunciado](<../Ejercicios juez/5-Grafos dirigidos/prob-Ordenando tareas.pdf>) · 💻 [Solución](EJ_05-3.cpp) · 🎬 [Vídeo](../Videos/05-3_ordenando_tareas.mp4)

## Qué piden
Un orden de las tareas que respete todas las dependencias «A antes que B», o `Imposible`.

## Cómo se plantea
**Grafo dirigido:** cada tarea es un vértice y «A antes que B» es la arista `A → B`. Un orden válido es un **orden topológico**, que existe si y solo si el grafo **no tiene ciclos**.

**Orden topológico = postorden inverso de un DFS.** Cuando el DFS termina un vértice `v`, ya han terminado todos sus sucesores, así que `v` va antes que ellos: se van guardando los vértices al terminar y se le da la vuelta a la lista.

**Ciclos en el mismo DFS**, con tres estados por vértice:

| Estado | Significado |
|:--:|---|
| 0 | sin visitar |
| 1 | en la pila (se está explorando) |
| 2 | terminado |

Si desde `v` se ve un vecino `w` en estado 1, `w` es un antecesor de `v` y `v → w` cierra un ciclo ⇒ `Imposible`. Ver un vecino en estado 2 es normal.

## Por qué así
- **Hay muchos órdenes válidos** y el problema acepta cualquiera (el programa da `7 1 2 4 3 5 6` en el ejemplo, el enunciado `1 2 7 3 4 5 6`).
- Alternativa: **algoritmo de Kahn** (ir quitando los vértices sin dependencias pendientes); detecta el ciclo si se queda sin poder quitar todos.
- La recursión llega como mucho a N = 10.000 niveles: no hay problema de pila.
- Usa `Digrafo.h` (copia en esta carpeta; ver nota en `Estructuras de datos/`).

## Traza del ejemplo 1
```text
DFS(1) → 2 → 3 → 5 → 6      termina 6, 5, 3     post = 6 5 3
        2 → 4 (5 ya terminado) termina 4, 2, 1  post = 6 5 3 4 2 1
DFS(7) (4 ya terminado)       termina 7         post = 6 5 3 4 2 1 7
al revés:  7 1 2 4 3 5 6
```
Ejemplo 2 (`1→2`, `2→1`): DFS(1) → 2, y desde 2 se ve el 1 **en la pila** ⇒ `Imposible`.

## Coste
**O(N + M)**.
