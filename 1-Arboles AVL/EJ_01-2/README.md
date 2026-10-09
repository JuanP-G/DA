# EJ 01-2 · Encontrar el k-ésimo elemento en un árbol AVL

📄 [Enunciado](<../Enunciados/prob-Encontrar el k-ésimo elemento en un árbol AVL.pdf>) · 💻 [Solución](<EJ 01-2.cpp>) · [TreeSet_AVL_plantilla.h](TreeSet_AVL_plantilla.h)

## Qué piden
Añadir a `Set` (conjunto con árbol AVL) la operación `kesimo(k)`, que devuelve el k-ésimo menor elemento en **tiempo logarítmico**, o lanza excepción si no existe (se escribe `??`).

## Cómo se plantea
**Atributo nuevo `tami`** en cada nodo = tamaño del hijo izquierdo + 1, es decir, la posición de la raíz dentro de su subárbol. Hay que mantenerlo en tres sitios del `.h`:

| Dónde | Cambio |
|---|---|
| `inserta` | si se insertó por la **izquierda** (`crece`), `a->tami += 1`; por la derecha no cambia |
| `rotaDer(r2)` | `r1` sube: `r2` pierde a `r1` y su izquierdo → `r2->tami -= r1->tami` |
| `rotaIzq(r1)` | `r2` sube: gana a `r1` y todo su izquierdo → `r2->tami += r1->tami` |

Las rotaciones dobles son composición de simples, así que no necesitan nada más.

**`kesimo(k, a)`** baja desde la raíz:
1. `a == nullptr` → `out_of_range` (k no existe).
2. `k == a->tami` → es la raíz.
3. `k < a->tami` → buscar el mismo `k` en el izquierdo.
4. `k > a->tami` → buscar `k − a->tami` en el derecho (se saltan la raíz y todo el izquierdo).

`main` inserta los N valores, y para cada consulta escribe `kesimo(k)` o `??` si salta la excepción.

## Por qué así
- **Por qué no recorrer en inorden:** funcionaría, pero cuesta O(k), lineal en el peor caso. Con `tami` cada paso descarta un subárbol entero.
- **Repetidos:** `inserta` devuelve `false` si el valor ya está, así que `tami` no se toca; por eso el conjunto puede tener menos de N elementos y aparecen `??`.
- **`k` fuera de rango** (k > tamaño o k ≤ 0) acaba siempre en `nullptr` y lanza la excepción, sin comprobar el tamaño aparte.
- En `inserta`, `crece` significa «se ha insertado algo» (no «ha crecido la altura»), por eso sirve para decidir si sumar 1 a `tami`.
- El enunciado permite ignorar el borrado. `borra` sí ajusta `tami` en su propio camino, pero `borraMin` no, así que `erase` deja `tami` incoherente cuando el nodo borrado tiene dos hijos. No afecta a este problema (no se borra).
- `comprueba()` es una función de depuración que verifica alturas, equilibrio y `tami`. El `#include "bintree.h"` del `.cpp` no se usa.

## Traza del ejemplo
Caso 2 (`16 8 4 4 32`, consultas `2 4 5`), nodos como `elem|tami`:
```text
insert 16:  16|1
insert 8:   8|1 ← 16|2
insert 4:   8|2, 16|3; desequilibrio → rotaDer: 16|3 − 8|2 = 16|1  →  4|1 ← 8|2 → 16|1
insert 4:   repetido, no cambia nada
insert 32:  4|1 ← 8|2 → 16|1 → 32|1
kesimo(2): 8|2 → k == tami                                   → 8
kesimo(4): 8|2 → der k=2 → 16|1 → der k=1 → 32|1             → 32
kesimo(5): 8|2 → k=3 → 16|1 → k=2 → 32|1 → k=1 → nullptr     → ??
```
Casos 1 y 3: `15 25` y `7`, como en la salida de ejemplo.

## Coste
**O(log N)** por `kesimo` e `insert`: ambos bajan un solo camino de un árbol AVL, cuya altura es logarítmica, y actualizar `tami` es O(1) por nodo. Total por caso: **O((N + M) log N)**.
