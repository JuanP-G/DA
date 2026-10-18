# EJ 06-4 · La selva de Tarzán

📄 [Enunciado](<../Enunciados/prob-La selva de Tarzán.pdf>) · 💻 Solución en código: *pendiente* (esta carpeta solo trae la explicación, `GrafoValorado.h` y `ConjuntosDisjuntos.h`)

## Qué piden
N árboles y M saltos posibles; cada salto entre dos árboles exige una **cuerda de al menos cierta longitud**. Tarzán lleva **una sola cuerda** y quiere poder llegar de cualquier árbol a cualquier otro. ¿Cuál es la **longitud mínima** de cuerda que lo permite? Si aunque la cuerda fuese infinita no se puede, `Imposible`.

## Cómo se plantea
Grafo valorado no dirigido: árboles = vértices, saltos = aristas, longitud mínima del salto = valor.

Con una cuerda de longitud `L` se pueden hacer **todos los saltos de valor ≤ L**. La pregunta es:

> ¿Cuál es el menor `L` tal que las aristas de valor ≤ L conectan todo el grafo?

Eso es lo que hace **Kruskal**: va metiendo aristas de menor a mayor, y cada vez que mete una arista de valor `L` es porque ya están todas las más cortas. **La longitud buscada es el valor de la última arista que Kruskal acepta**, la que deja todos los árboles conectados.

**Algoritmo**

1. Ordenar los saltos por longitud creciente. Crear `ConjuntosDisjuntos cd(N)`.
2. Para cada salto `(u, v, L)` en orden: si `!cd.unidos(u, v)` ⇒ `cd.unir(u, v)` y `ultima = L`.
3. Al terminar (o cuando `cd.num_cjtos() == 1`):
   - si `num_cjtos() == 1` ⇒ escribir `ultima`,
   - si no ⇒ `Imposible`.

Con N = 1 no se acepta ninguna arista y `num_cjtos()` ya es 1 ⇒ la respuesta es `0` (inicializar `ultima = 0`).

## Por qué funciona
- **Menos que `ultima` no basta:** justo antes de añadir la última arista aceptada, con todas las aristas de valor menor, quedaban al menos dos componentes (si no, Kruskal habría terminado antes). Con una cuerda más corta que `ultima` solo se tienen aristas que ya se habían probado ⇒ sigue sin conectar.
- **`ultima` sí basta:** lo aceptado forma un árbol de recubrimiento, y todas sus aristas valen ≤ `ultima`.
- Es el **valor de la arista más pesada de un ARM**. Es un resultado general: el ARM además de minimizar la *suma*, minimiza la arista *máxima* («árbol de cuello de botella»).

## Diferencia con 06-3
Es casi el mismo código, pero **no se suman los costes**: se guarda el valor de la última arista aceptada (el máximo del ARM). La pregunta cambia de «cuánto cuesta todo» a «cuál es el salto más largo que me obliga a llevar la cuerda».

## Por qué así
- **Aristas que sobran** (largas, o repetidas, o entre árboles ya conectados) simplemente se descartan con `unidos`; no hay que tratarlas aparte.
- **Entrada:** no hay número de casos; se leen selvas **hasta el final del fichero** (`while (cin >> N >> M)`). Para el grafo, `GrafoValorado<int> g(N)` y `ponArista({u - 1, v - 1, L})` M veces, o leer las aristas directamente a un vector (el grafo no es imprescindible: solo hace falta la lista de aristas ordenada).
- **Longitudes** hasta 10⁶: caben en `int`.
- Hasta 10.000 árboles y 100.000 saltos: ordenar es O(M log M), muy holgado.

## Traza del ejemplo 1 (4 árboles, 4 saltos)
```text
Ordenados:  1-2 (5)   3-1 (7)   2-4 (8)   2-3 (10)

1-2 (5)   distintos → unir    {1,2} {3} {4}      ultima = 5
3-1 (7)   distintos → unir    {1,2,3} {4}        ultima = 7
2-4 (8)   distintos → unir    {1,2,3,4}          ultima = 8   ← un solo conjunto
2-3 (10)  (no hace falta: ya conectado)
```
Resultado: **8** (el salto de 10 nunca se necesita).

Ejemplo 2 (N = 1, M = 0): un solo árbol ⇒ **0**.
Ejemplo 3 (N = 4; saltos 1-2 y 4-3): quedan dos componentes `{1,2}` y `{3,4}` ⇒ **Imposible**.

## Coste
**O(N + M log M)** (ordenar las aristas; la partición es casi lineal).

## Ojo con
- No sumar: se escribe una **longitud**, no un coste total.
- Distinguir «un solo árbol» (`0`) de «no se puede» (`Imposible`) mirando `num_cjtos()`, no si hubo aristas.
- La palabra es `Imposible` (con minúscula salvo la inicial), distinta del `IMPOSIBLE` del 06-5.
