# EJ 01-1 · ¿Es un árbol AVL?

📄 [Enunciado](<../Enunciados/prob-¿Es un árbol AVL_.pdf>) · 💻 [Solución](<EJ 01-1.cpp>)

## Qué piden
Dado un árbol binario de enteros (en preorden, con `-1` como árbol vacío), decidir si es **AVL**: de búsqueda (estricto) y con alturas de los hijos que difieren como mucho en 1 en todo nodo.

## Cómo se plantea
**No se construye el árbol:** la función recursiva `leerAVL(altura, minimo, maximo)` lee el subárbol de la entrada a la vez que lo comprueba. Como la entrada viene en preorden (raíz, izquierdo, derecho), basta con leer la raíz y llamarse dos veces.

Cada llamada **devuelve** si el subárbol es AVL y **deja en los parámetros por referencia**:

| Parámetro | Vacío (`-1`) | Nodo `valor` |
|---|---|---|
| `altura` | 0 | `max(altIzq, altDer) + 1` |
| `minimo` | `INT_MAX` (centinela) | `min(minIzq, valor)` |
| `maximo` | `INT_MIN` (centinela) | `max(maxDer, valor)` |

Un nodo es AVL si:
1. los dos hijos son AVL (`izqOK && derOK`),
2. `|altIzq − altDer| ≤ 1`,
3. `maxIzq < valor < minDer` (todo el izquierdo es menor y todo el derecho mayor).

## Por qué así
- **Postorden implícito:** para decidir sobre un nodo hacen falta la altura, el mínimo y el máximo de sus hijos, así que primero se resuelven los hijos y después el nodo.
- **Comparar con el mínimo/máximo del subárbol, no con el hijo:** comparar solo con los hijos directos no basta (un nieto puede romper el orden). Por eso se propagan min y max.
- **Centinelas en el vacío:** con `INT_MIN`/`INT_MAX` las comparaciones `maxIzq < valor` y `valor < minDer` son ciertas sin casos especiales. Funciona porque los valores son no negativos; un nodo que valiera `INT_MAX` sin hijo derecho daría un falso `NO`.
- **Se lee siempre el árbol entero**, aunque ya se sepa que no es AVL: las dos llamadas se hacen antes de combinar, así que la entrada del siguiente caso queda bien posicionada.
- Si el subárbol no es de búsqueda, `minimo`/`maximo` pueden no ser los reales (solo miran un lado), pero da igual: el resultado ya es `false`.
- Al final del fichero hay una versión alternativa comentada que devuelve un `struct Info` en lugar de usar parámetros por referencia.

## Traza del ejemplo
```text
Caso 1: 2 1 -1 -1 3 -1 4 -1 -1
  nodo 1: alt=1 min=1 max=1                         ok
  nodo 4: alt=1 min=4 max=4                         ok
  nodo 3: altIzq=0 altDer=1, minDer=4 > 3           ok  (alt=2)
  nodo 2: altIzq=1 altDer=2, maxIzq=1 < 2 < minDer=3 ok → SI
Caso 2: 1 -1 3 2 -1 -1 4 -1 -1
  nodo 3: altIzq=1 altDer=1                         ok  (alt=2)
  nodo 1: altIzq=0 altDer=2 → diferencia 2          NO
Caso 3: 4 1 -1 -1 3 -1 2 -1 -1
  nodo 3: hijo derecho 2, minDer=2 no es > 3        NO
  nodo 4: hereda el fallo                           → NO
```

## Coste
**O(N)** por caso, siendo N el número de nodos: cada nodo se lee y se procesa una sola vez con trabajo constante. Memoria **O(h)** por la pila de recursión.
