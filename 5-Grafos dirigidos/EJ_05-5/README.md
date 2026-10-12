# EJ 05-5 · Haciendo trampas en Serpientes y Escaleras

📄 [Enunciado](<../Enunciados/prob-Haciendo trampas en Serpientes y Escaleras.pdf>) · 💻 [Solución](EJ_05-5.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#253 · Haciendo trampas en Serpientes y Escaleras](https://aceptaelreto.com/problem/statement.php?id=253) — *mismo problema*. Mismo enunciado, pero allí la entrada termina con la línea «0 0 0 0» en vez de empezar con el número de casos: cambia el bucle de lectura.
<!-- acr:fin -->

## Qué piden
Con un dado trucado (eliges la cara, de 1 a K), el **mínimo número de tiradas** para ir de la casilla 1 a la N².

## Cómo se plantea
**Digrafo** de N² vértices (casilla `c` → vértice `c − 1`). Si en `c` empieza una serpiente o una escalera, `destino[c]` es su otro extremo; si no, `destino[c] = c`. Desde cada casilla `v`:

```text
v → destino[v + d]        para d = 1 … K   (sin pasarse de N²)
```

Cada arista es **una tirada**, así que el mínimo de tiradas es el camino con menos aristas ⇒ **BFS** desde 0, parando al sacar N² − 1.

## Por qué así
- **El zigzag del tablero no importa:** solo cuenta el número de cada casilla.
- **Serpientes y escaleras son lo mismo** para el grafo: un salto obligatorio al caer en la casilla.
- Es **dirigido**: de 6 se sube a 47, pero de 47 no se baja a 6.
- No hace falta tratar aparte caer en una serpiente: el BFS ya prefiere otra tirada si es mejor (ejemplo 2).
- El enunciado garantiza que la meta es alcanzable.

## Traza del ejemplo 2 (`N=4, K=2`, escalera 3→12, serpiente 14→2)
```text
d=0: 1
d=1: 2, 12          (tirar un 2 desde 1: casilla 3, escalera a la 12)
d=2: 13, 14→2 (ya visto)
d=3: 15
d=4: 16             ⇒ 4
```
Ejemplo 1: `1 → 6 (escalera a 47) → 51 (escalera a 94) → 100` ⇒ 3.

## Coste
**O(N² · K)** por caso: N² vértices con K aristas cada uno.
