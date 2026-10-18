# EJ 07-2 · Camino al cole

📄 [Enunciado](<../Enunciados/prob-Camino al cole.pdf>) · 💻 [Solución](EJ_07-2.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#358 · Camino al cole](https://aceptaelreto.com/problem/statement.php?id=358) — *casi el mismo problema*. Misma historia, pero allí los límites son distintos (hasta 10.000 intersecciones y 100.000 calles de hasta 100.000 de longitud; aquí 100.000, 200.000 y 10.000) y no hay número de casos: se lee hasta el final del fichero.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-358_camino_al_cole.cpp`](<../../Acepta el Reto/ACR-358_camino_al_cole.cpp>)
<!-- acr:fin -->

## Qué piden
Pueblo con N intersecciones (1 ≤ N ≤ 100.000) y C calles con una longitud. Lucas va de la intersección **1** a la **N** y no respeta el sentido de circulación: las calles se recorren **en ambos sentidos**. ¿De cuántas formas distintas puede ir recorriendo **exactamente la distancia mínima**? (`0` si no hay camino; el resultado es siempre menor que 2³¹.)

## Cómo se plantea
Se adapta **Dijkstra para contar caminos mínimos**, no solo medirlos. Además de `dist[]` hay un vector `formas[]`:

> `formas[v]` = número de caminos de longitud mínima desde la intersección 1 hasta `v`.

Al **relajar** la arista `v → w` de valor `c` (cuando `v` ya está tratado):

| Situación | Qué significa | Qué hacer |
|---|---|---|
| `dist[v] + c < dist[w]` | camino **más corto** que todos los vistos hasta `w` | `dist[w] = dist[v] + c`, `formas[w] = formas[v]` (los anteriores ya no valen), `pq.update` |
| `dist[v] + c == dist[w]` | **otra** forma igual de buena de llegar a `w` | `formas[w] += formas[v]` |
| `dist[v] + c > dist[w]` | no sirve | nada |

Inicio: `dist[0] = 0` y `formas[0] = 1` (hay una forma de estar en casa: no moverse). El resultado es `formas[N-1]`.

## Por qué `formas[v]` es definitivo al sacar `v` de la cola
Todos los caminos mínimos hasta `v` llegan por algún vecino `u` con `dist[u] < dist[v]` (las calles miden ≥ 1, así que la distancia estrictamente crece). Esos `u` se han sacado antes de la cola y ya han **sumado su aportación** a `formas[v]`. Con calles de longitud 0 esto fallaría, pero aquí son ≥ 1.

## Traza del ejemplo 1 (7 intersecciones, 4 formas)
```text
            dist  formas
1             0      1
2 (vía 1)     5      1
3 (vía 1)     7      1
4 (vía 2)    15      1     luego vía 3: 7 + 8 = 15 = dist[4]  →  formas[4] = 1 + 1 = 2   (1-2-4 y 1-3-4)
6 (vía 4)    26      2
5 (vía 4)    27      2
7 (vía 4)    40      2     al sacar el 4 (dist 15): 15 + 25 = 40
7 (vía 5)    40      4     al sacar el 5 (dist 27): 27 + 13 = 40 = dist[7]  →  formas[7] += formas[5] = 2
                           (la vía 6 daría 26 + 30 = 56 > 40: no sirve)
```
Salida: **4**. Segundo caso: no se llega a la intersección 4 ⇒ `0`. Tercer caso: N = 1 ⇒ `1`.

## Por qué así
- **Calles de doble sentido:** se añaden **dos aristas dirigidas** por calle en el `DigrafoValorado` (`v → w` y `w → v`).
- **N = 1:** casa y colegio coinciden; `formas[0] = 1` ya da la respuesta.
- **Tipo de `formas`:** la respuesta final es < 2³¹, pero el número de caminos de *otros* vértices puede ser enorme. Con `unsigned long long` el desbordamiento está definido (módulo 2⁶⁴) y no estropea la respuesta, que es pequeña y por tanto exacta.
- **Coste:** O(C log N) por caso, el de Dijkstra; contar no añade nada.

## Ojo con
- Si el vecino ya tiene la **misma** distancia, hay que **sumar**, no ignorar: ese es el caso nuevo respecto a Dijkstra normal.
- Si se encuentra un camino **más corto**, el contador se **sustituye**, no se suma.
