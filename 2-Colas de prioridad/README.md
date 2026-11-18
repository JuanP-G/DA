# Colas de prioridad (tema 2) · resumen

🎬 Vídeo: [`02-0_colas_de_prioridad_teoria.mp4`](../Videos/02-0_colas_de_prioridad_teoria.mp4)

## El TAD
Siempre sale el elemento **más prioritario**: `push(x)`, `top()`, `pop()`, `empty()`, `size()`.

| Implementación | push | top | pop |
|---|---|---|---|
| vector desordenado | `O(1)` | `O(n)` | `O(n)` |
| vector ordenado | `O(n)` | `O(1)` | `O(1)` |
| **montículo** | `O(log n)` | `O(1)` | `O(log n)` |

## El montículo
Árbol binario **completo** (todos los niveles llenos salvo el último, que se llena de izquierda a derecha) en el que **cada padre es ≤ que sus hijos** (montículo de mínimos): el mínimo está en la raíz. Se guarda en un **vector**: con posiciones desde 1, los hijos de `i` están en `2i` y `2i+1`, y el padre en `i/2`.

- **push**: se pone al final y **flota** (se intercambia con su padre mientras sea menor).
- **pop**: el último pasa a la raíz y se **hunde** (se intercambia con su hijo menor mientras haga falta).
- **heapify**: convertir un vector en montículo hundiendo desde la mitad hacia atrás, `O(n)`.
- **heapsort**: heapify + sacar `n` veces la raíz, `O(n log n)` sin memoria extra.

## `std::priority_queue`
| Declaración | Qué hace |
|---|---|
| `priority_queue<int>` | de **máximos** (por defecto) |
| `priority_queue<int, vector<int>, greater<int>>` | de mínimos |
| con `pair` | compara `first` y luego `second` (desempate gratis) |
| con un `struct` y `operator<` | sale primero el **mayor** |

No deja cambiar la prioridad de un elemento que ya está dentro: para eso está la [IndexPQ](../3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/README.md).

## Patrones de los ejercicios
| Patrón | Ejercicios |
|---|---|
| Simulación por eventos (cajas, estaciones, envíos) | [02-2](EJ_02-2/README.md), [02-3](EJ_02-3/README.md), [02-L](EJ_02-L/README.md) |
| Prioridad con desempate | [02-4](EJ_02-4/README.md), [02-5](EJ_02-5/README.md) |
| Voraz: siempre los menores | [02-1](EJ_02-1/README.md) |
| Mezclar varias secuencias | [02-6](EJ_02-6/README.md) |
