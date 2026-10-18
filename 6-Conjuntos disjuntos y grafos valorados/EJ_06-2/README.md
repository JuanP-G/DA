# EJ 06-2 · Camiones de reparto

📄 [Enunciado](<../Enunciados/prob-Camiones de reparto.pdf>) · 💻 Solución en código: *pendiente* (esta carpeta solo trae la explicación y `GrafoValorado.h`)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#646 · Camiones de reparto](https://aceptaelreto.com/problem/statement.php?id=646) — *mismo problema*. Mismo enunciado, pero allí no hay número de casos: se lee hasta el final del fichero.
<!-- acr:fin -->

## Qué piden
Una ciudad con V intersecciones y E calles de doble sentido; cada calle tiene una **anchura máxima**. Para cada una de las K consultas `(origen, destino, anchura del camión)`: `SI` si el camión puede ir del origen al destino **usando solo calles por las que cabe**, `NO` si no.

## Cómo se plantea
**Grafo valorado no dirigido:** intersecciones = vértices, calles = aristas, anchura máxima = valor de la arista.

La pregunta de cada consulta es una pregunta de **alcanzabilidad con filtro**:

> ¿Hay un camino de `origen` a `destino` que use solo aristas con `valor ≥ anchura del camión`?

Un recorrido (DFS o BFS) desde `origen` que **ignora las aristas demasiado estrechas** responde a eso:

```text
dfs(v):  marcar v
         para cada arista a de ady(v):
             si a.valor() >= ancho  y  w = a.otro(v) no está marcado:  dfs(w)
```

Al terminar, la respuesta es `visitado[destino] ? SI : NO`.

Hay que repetirlo **para cada consulta** (el filtro cambia con la anchura), borrando antes las marcas.

## Por qué así
- **La comparación es `>=`**: un camión de anchura 15 cabe «justo» por una calle cuya anchura máxima es 15 (lo dice el enunciado). Con `>` fallaría el ejemplo 3. *(El fragmento de recorrido con umbral de las transparencias usa `<`; para este enunciado la condición correcta es `>=`, así que no lo copies tal cual.)*
- **`GrafoValorado<int> g(cin, 1)`** lee directamente «V, E y E aristas» con vértices numerados desde 1 (el segundo parámetro, `primer`, los pasa a base 0). Las consultas se leen aparte con `cin`.
- **Calles repetidas** entre las mismas dos intersecciones: no molestan, el recorrido las ve como dos aristas más.
- **Origen ≠ destino** está garantizado, pero aunque no lo estuviera la respuesta sería `SI` (basta con estar allí).
- La recursión baja como mucho V = 10.000 niveles: no hay problema de pila (si se prefiere, un BFS con cola lo evita).

## Traza del ejemplo (V = 5, E = 5)
```text
aristas:  1-2 (10)   1-3 (30)   2-4 (20)   3-4 (15)   4-5 (12)

Consulta 1→5, camión 8      todas las aristas valen (≥ 8)        → 1,2,3,4,5 alcanzado   SI
Consulta 1→4, camión 12     descarta 1-2 (10)                    → 1-3-4                 SI
Consulta 1→4, camión 15     descarta 1-2 (10) y 4-5 (12)         → 1-3-4 (15 ≥ 15)       SI
Consulta 2→5, camión 15     solo valen 1-3, 2-4, 3-4             → desde 2: 4, 3, 1
                            la 4-5 (12) no vale ⇒ no se llega a 5                        NO
```

## Coste
Cada consulta es un recorrido completo: O(V + E). Con K ≤ 10 consultas por caso: **O(K · (V + E))**, es decir ~10 · 110.000 operaciones. Espacio O(V + E).

## Otra forma de verlo (más potente)
Si K fuera enorme (miles de consultas) repetir el recorrido sería lento. Entonces se usa lo que se verá en 06-3, 06-4 y 06-5: el **árbol de recubrimiento de coste *máximo*** (Kruskal con las aristas de mayor a menor): la anchura más grande con la que se puede viajar entre dos intersecciones es la **arista más estrecha del camino que las une en ese árbol**. Aquí, con K ≤ 10, no hace falta.

## Ojo con
- Reiniciar el vector de visitados **en cada consulta**.
- La anchura de cada calle es la anchura **máxima** que admite: el camión cabe si su anchura es **menor o igual**.
- Los casos son varios: la primera línea de la entrada indica cuántos.
