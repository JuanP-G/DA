# EJ 07-7 · Ratones en un laberinto

📄 [Enunciado](<../Enunciados/prob-Ratones en un laberinto.pdf>) · 💻 [Solución](EJ_07-7.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#601 · Ratones en un laberinto](https://aceptaelreto.com/problem/statement.php?id=601) — *casi el mismo problema*. Allí los límites son menores (hasta 10.000 celdas y 100.000 pasadizos; aquí 100.000 y 200.000) y no hay número de casos: se lee hasta el final del fichero.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-601_ratones_en_un_laberinto.cpp`](<../../Acepta el Reto/ACR-601_ratones_en_un_laberinto.cpp>)
<!-- acr:fin -->

## Qué piden
Laberinto con N celdas (1 ≤ N ≤ 100.000) y P pasadizos **dirigidos** (0 ≤ P ≤ 200.000) con un tiempo 1..10.000 (pueden repetirse y haber bucles). Hay un ratón en cada celda **menos en la salida S** y todos van por el camino más rápido hacia S. ¿Cuántos ratones llegan a S en **como mucho** T segundos?

## Cómo se plantea
Hay que saber, para **cada** celda, el tiempo mínimo **hasta** S. Un Dijkstra normal da las distancias *desde* un origen, y aquí queremos las distancias *hacia* un destino. Truco:

```text
camino de a a S en el grafo   ==   camino de S a a en el grafo INVERSO
```
Un solo Dijkstra desde S en el **grafo inverso** da `dist[a]` = tiempo del ratón de `a`. Se cuentan las celdas `a ≠ S` con `dist[a] ≤ T` (el «como mucho» incluye el igual). Las celdas que no llegan quedan en infinito y no cuentan.

## Traza del ejemplo 1 (S = 5, T = 20)
Pasadizos: 1→2 (5), 1→4 (10), 2→4 (7), 3→4 (15), 4→5 (10).
```text
Grafo inverso desde 5:   5 → 4 (10)
                         4 → 1 (10 + 10 = 20)   4 → 2 (10 + 7 = 17)   4 → 3 (10 + 15 = 25)
dist:   celda 4 = 10,   celda 2 = 17,   celda 1 = 20,   celda 3 = 25
dist ≤ 20:  celdas 4, 2 y 1   →  3 ratones      (la 3 tarda 25 y no llega)
```

## Por qué así
- **Un solo Dijkstra** (en el inverso) en lugar de uno por ratón: en el peor caso serían N ejecuciones.
- **Parada anticipada:** al sacar una celda con `dist > T` todas las siguientes de la cola tampoco llegan, así que se puede parar.
- **Ratón en la salida:** no se cuenta (no hay ratón en S).
- **Bucles y pasadizos repetidos:** no molestan.
- **Coste:** O(P log N) por caso.

## Ojo con
- Sentido de los pasadizos: «A B t» es de A a B. Para el inverso se usa `g.inverso()`.
- `≤ T`, no `< T` (en el ejemplo, el ratón de la celda 1 llega justo a los 20 s y cuenta).
- Celdas desde 1: restar 1 al leer.
