# EJ 02-6 · Coleccionando cómics

📄 [Enunciado](<../Enunciados/prob-Coleccionando cómics.pdf>) · 💻 [Solución](EJ_02-6.cpp)

## Qué piden
Hay N pilas de cómics y cada cliente se lleva **el menor identificador entre las cimas**. ¿Qué puesto de la fila hay que ocupar para llevarse **el menor de toda la tienda**?

## Cómo se plantea
Se **simula** la venta: en cada turno hace falta el mínimo de las N cimas, y tras cada compra cambia una sola cima. Eso es una **cola de prioridad de mínimos** con un elemento por pila.

- Cada pila se guarda en una `Pila<int>` ([`Pila.h`](Pila.h), la implementación con vector dinámico del curso), apilando de izquierda a derecha: el último número leído queda en la cima, como dice el enunciado.
- Mientras se lee, se calcula `mejor`, el identificador mínimo de todo el caso: es el cómic que queremos.
- Cola de **mínimos** de pares `(identificador de la cima, número de pila)`:
  `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>>`.

Bucle principal (con `puesto = 1`):
1. Si la cima de la cola es `mejor`, ese es nuestro turno: se escribe `puesto`.
2. Si no, el cliente actual se lleva ese cómic: `pop()`, `desapila()` en su pila y, **si la pila no se ha vaciado**, se mete en la cola su nueva cima.
3. `++puesto` y se repite.

## Por qué así
- **Cada pila aporta a la cola solo su cima**, que es lo único que un cliente puede comprar. Guardar el número de pila en el `pair` permite saber de dónde reponer.
- **El bucle siempre termina:** `mejor` es el menor de todos, así que en cuanto asome en alguna cima será el mínimo de la cola; y nunca se lo lleva otro, porque antes de que asome todo lo que se vende está encima de él o en otras pilas.
- **Pilas que se agotan** (caso 3 del ejemplo): simplemente no se vuelve a meter nada de ellas.
- Los identificadores son distintos, así que no hay empates; el segundo campo del `pair` nunca decide.
- **Error típico:** `priority_queue<pair<int,int>>` sin `greater<>` es de máximos y daría el cómic **peor** de las cimas.
- Todo cabe en `int` (ids ≤ 10⁸, puestos ≤ 10⁶). La entrada acaba con fin de fichero (`if (!(cin >> n))`).

## Traza del ejemplo
```text
Caso 1: pila 0 = [5 2 3 1 | 20]   pila 1 = [9 12 44 13 4 7 | 8]   mejor = 1
  cola = {(8,1), (20,0)}
  puesto 1: se lleva 8  (pila 1) -> asoma 7    cola = {(7,1), (20,0)}
  puesto 2: se lleva 7  (pila 1) -> asoma 4    cola = {(4,1), (20,0)}
  puesto 3: se lleva 4  (pila 1) -> asoma 13   cola = {(13,1), (20,0)}
  puesto 4: se lleva 13 (pila 1) -> asoma 44   cola = {(20,0), (44,1)}
  puesto 5: se lleva 20 (pila 0) -> asoma 1    cola = {(1,0), (44,1)}
  puesto 6: la cima es 1 = mejor  -> 6
Caso 3: se venden 3, 4, 7, 9 (las pilas 0 y 1 se agotan) -> 5
```

## Coste
**O(T log N)**, siendo T ≤ 10⁶ el total de cómics: cada cómic entra y sale de la cola como mucho una vez, y la cola nunca tiene más de N elementos (más O(T) de la lectura).
