# EJ 07-4 · La conferencia de paz

📄 [Enunciado](<../Enunciados/prob-La conferencia de paz.pdf>) · 💻 [Solución](EJ_07-4.cpp)

## Qué piden
N aldeas (3 ≤ N ≤ 100.000) unidas por caminos de **doble sentido** con longitud 1..1.000 (el grafo es conexo). Unas aldeas son de los **galos**, otras de los **romanos** y el resto son **neutrales**. Hay que elegir una aldea **neutral** tal que la distancia a la aldea gala **más cercana** y la distancia a la romana **más cercana** se diferencien lo **menos** posible. Si hay empate, la de índice menor. Se escribe el índice de la aldea y esa diferencia.

## Cómo se plantea
Dos **Dijkstra con varios orígenes a la vez**: se meten **todas** las aldeas del bando en la cola con distancia 0.

```text
dGalos[v]   = distancia de v a la aldea gala más cercana
dRomanos[v] = distancia de v a la aldea romana más cercana
```
Es lo mismo que añadir un vértice falso unido con coste 0 a todas las aldeas del bando y hacer Dijkstra desde él, pero sin construirlo. Después se recorren las aldeas neutrales **en orden creciente** y nos quedamos con la de menor `|dGalos − dRomanos|`; con `<` estricto gana la primera, que es la de índice menor.

## Traza del ejemplo 2
Caminos: 1-2 (3), 2-3 (5), 3-4 (4), 4-5 (2), 5-6 (1). Galos = {1, 5}, romanos = {3}.
```text
aldea         1   2   3   4   5   6
dGalos        0   3   6   2   0   1        (a la 3, por la 5 y la 4: 2 + 4 = 6)
dRomanos      8   5   0   4   6   7
neutral?      -   sí  -   sí  -   sí
|diferencia|      2       2       6
```
Empatan la 2 y la 4 con diferencia 2; gana la de índice menor: **2 2**.

## Por qué así
- **Cualquier aldea sirve de paso:** el camino más corto puede atravesar aldeas de cualquier bando.
- **Un Dijkstra por bando, no por aldea:** con varios orígenes a la vez basta uno para cada bando.
- **Solo neutrales:** las aldeas de los bandos se saltan al elegir (pero sí se usan en los caminos).
- **Coste:** O(C log N) por caso (dos Dijkstra). Las distancias son ≤ 10⁸, caben en `int`.

## Ojo con
- Doble sentido: dos aristas dirigidas por camino.
- Las aldeas vienen numeradas desde 1: restar 1 al leer y sumar 1 al escribir.
- Las dos últimas líneas del caso empiezan por **el número de aldeas** del bando (galos primero).
