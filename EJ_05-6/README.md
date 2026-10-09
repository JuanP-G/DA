# EJ 05-6 · Sistema de inecuaciones

📄 [Enunciado](<../Ejercicios juez/5-Grafos dirigidos/prob-Sistema de inecuaciones.pdf>) · 💻 [Solución](EJ_05-6.cpp)

## Qué piden
Valores enteros para x1 … xN que cumplan todas las inecuaciones `xi < xj`, o `NO` si no existen.

## Cómo se plantea
**Digrafo:** un vértice por variable y una arista `i → j` por cada `xi < xj`. La entrada tiene justo el formato que lee el constructor `Digrafo(cin, 1)` (N, M y los pares; el `1` es porque las variables empiezan en 1), así que no hace falta añadir las aristas a mano.

- Si hay un **ciclo** (`x1 < x2 < … < x1`) es imposible ⇒ `NO`.
- Si es un **DAG**, existe un **orden topológico**: todas las aristas van hacia delante. Dando a cada variable su **posición** en ese orden (1, 2, …, N), cada arista `i → j` cumple `pos(i) < pos(j)` ⇒ `SI` y esas posiciones.

Ciclo y orden salen del **mismo DFS con tres estados** que en [05-3](../EJ_05-3/README.md): 0 sin visitar, 1 en la pila, 2 terminado; un vecino en estado 1 es un ciclo, y el orden es el postorden inverso.

## Por qué así
- **Cualquier asignación válida vale:** el programa da `SI 1 3 2 4` en el ejemplo 1, el enunciado `SI 2 5 3 7`.
- **Variables sueltas:** también tienen posición en el orden, así que reciben valor.
- **Inecuaciones repetidas:** aristas repetidas, no molestan.
- Es el mismo problema que 05-3 (tareas con precedencias) cambiando la salida: en vez del orden, la posición de cada uno.
- La recursión llega como mucho a N = 10.000 niveles.

## Traza del ejemplo 1
```text
aristas: 1→3  3→2  2→4  3→4  1→4
DFS(1) → 3 → 2 → 4      termina 4, 2, 3, 1      post = 4 2 3 1
orden topológico (al revés): 1 3 2 4
valores:  x1 = 1, x3 = 2, x2 = 3, x4 = 4   ⇒   SI 1 3 2 4
```
Ejemplo 2 (`x1 < x2`, `x2 < x1`): ciclo ⇒ `NO`.

## Coste
**O(N + M)** por caso.
