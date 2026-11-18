# Colas de prioridad variable · IndexPQ (tema 3) · resumen

🎬 Vídeo: [`03-0_indexpq_teoria.mp4`](../Videos/03-0_indexpq_teoria.mp4)

## Para qué
A veces la prioridad de un elemento **cambia cuando ya está en la cola** (votos que suben y bajan, distancias de Dijkstra). `priority_queue` no sabe dónde está cada elemento; meter copias repetidas funciona, pero la cola crece y hay que saltarse las viejas. La [`IndexPQ`](../Estructuras%20de%20datos/IndexPQ.h) permite **`update(e, p)` en `O(log n)`**.

## Cómo es por dentro
- Los elementos son enteros **0 … N−1**, cada uno con su prioridad.
- `array`: el montículo de pares `{elem, prioridad}`, desde la posición 1.
- `posiciones[e]`: en qué posición del array está `e` (**0 = no está**).

`update(e, p)` encuentra `e` en `O(1)` gracias a `posiciones`, cambia su prioridad y lo **flota** si ha mejorado o lo **hunde** si ha empeorado; cada intercambio actualiza `posiciones`.

## Operaciones
| Operación | Qué hace | Coste |
|---|---|---|
| `IndexPQ<T, Comparator> pq(N)` | cola para los elementos 0 … N−1 | `O(N)` |
| `pq.push(e, p)` | meter `e` (error si ya está) | `O(log n)` |
| `pq.update(e, p)` | cambiar la prioridad; si no está, lo mete | `O(log n)` |
| `pq.top()` | `Par { elem, prioridad }` del primero | `O(1)` |
| `pq.pop()` | sacar el primero | `O(log n)` |
| `pq.priority(e)` | prioridad actual de `e` | `O(1)` |

## El comparador
`antes(a, b)` es cierto si `a` debe salir antes que `b`. Por defecto `less` (mínimos); `greater<int>` da máximos; con `pair` se desempata solo; con un `struct` con `operator()` se puede ordenar por cualquier criterio (03-2: puntos y nombre).

## En los ejercicios
| Uso | Ejercicios |
|---|---|
| Prioridades que cambian (`update`) | [03-2](EJ_03-2/README.md), [03-5](EJ_03-5/README.md), [03-L](EJ_03-L/README.md) |
| La próxima aparición de cada elemento | [03-3](EJ_03-3/README.md) |
| Como montículo normal (`push`, `top`, `pop`) | [03-1](EJ_03-1/README.md), [03-4](EJ_03-4/README.md) (mediana con dos montículos) |

Será la pieza clave de **Prim** (tema 6) y **Dijkstra** (tema 7).
