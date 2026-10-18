# EJ 07-1 · Navegando sin teclado

📄 [Enunciado](<../Enunciados/prob-Navegando sin teclado.pdf>) · 💻 [Solución](EJ_07-1.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#318 · Navegando sin teclado](https://aceptaelreto.com/problem/statement.php?id=318) — *casi el mismo problema*. Misma historia, pero allí los límites son menores (hasta 1.000 páginas; aquí 3.000 páginas y 30.000 enlaces) y no hay número de casos: se lee hasta el final del fichero.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-318_navegando_sin_teclado.cpp`](<../../Acepta el Reto/ACR-318_navegando_sin_teclado.cpp>)
<!-- acr:fin -->

## Qué piden
N páginas web (2 ≤ N ≤ 3.000); se empieza en la **1** y se quiere llegar a la **N** usando solo los enlaces. Cada página tarda un tiempo en **cargar** y cada enlace tarda un tiempo en **localizarse y pulsarse**. Hay que escribir el tiempo mínimo contando la carga de **todas** las páginas visitadas (también la 1 y la N) y los enlaces pulsados, o `IMPOSIBLE`.

## Cómo se plantea
Es un **camino de coste mínimo en un digrafo valorado** (los enlaces tienen sentido): Dijkstra. La dificultad es que hay **dos tipos de coste**, el de los enlaces (en las aristas) y el de carga (en los vértices), y el campus pregunta justo eso.

**Truco:** el tiempo de carga de una página se paga **cada vez que se llega a ella**. Se suma al valor de la arista que entra:

```text
coste de la arista v → w  =  tiempo del enlace  +  carga[w]
dist[origen]              =  carga[origen]          (la primera página también se carga)
```

Así todo el coste queda en las aristas y vale Dijkstra tal cual. Todos los valores son ≥ 0 (entre 0 y 10.000), que es lo que exige el algoritmo.

## Dijkstra paso a paso
1. `dist[v] = ∞` para todos; `dist[0] = carga[0]`; se mete el 0 en la cola `IndexPQ`.
2. Mientras haya cola: se saca el vértice `v` de menor `dist` (su distancia ya es definitiva) y se **relajan** sus aristas: si `dist[v] + valor < dist[w]`, se actualiza `dist[w]` y se hace `pq.update(w, dist[w])`.
3. Se puede parar al sacar la página `N − 1`.
4. Resultado: `dist[N-1]`, o `IMPOSIBLE` si sigue en ∞.

## Traza del ejemplo 1
Cargas: 1→10, 2→5, 3→15, 4→8. Aristas con la carga del destino sumada:

```text
1→2: 10+5 = 15     1→3: 20+15 = 35     1→4: 100+8 = 108     2→4: 20+8 = 28     3→4: 20+8 = 28

dist[1] = 10
saca 1:  dist[2] = 25   dist[3] = 45   dist[4] = 118
saca 2:  dist[4] = min(118, 25+28 = 53) = 53
saca 3:  45 + 28 = 73 > 53, no mejora
saca 4:  fin  →  53
```
El segundo caso no tiene ningún enlace hacia la página 4: `dist[4]` queda en ∞ ⇒ `IMPOSIBLE`.

## Por qué así
- **Sin tocar el grafo de enlaces**: basta construir las aristas con `t + carga[w]`; la carga de la página inicial va en `dist[0]`.
- **Valores**: el mayor coste posible es 3.000 páginas · (10.000 + 10.000) = 6 · 10⁷, cabe en `int`.
- **Enlaces repetidos**: el enunciado garantiza que solo viene el más rápido entre dos páginas.
- **Coste**: O(M log N) por caso (Dijkstra con cola de prioridad variable).

## Ojo con
- Las páginas van **numeradas desde 1**: restar 1 al leer.
- Sumar la carga de la **página 1 y de la N**: la 1 en `dist[0]`, la N al llegar a ella (va dentro de la arista).
- Hay **varios casos**: reiniciar los vectores en cada uno (se declaran dentro de `resuelveCaso`).
