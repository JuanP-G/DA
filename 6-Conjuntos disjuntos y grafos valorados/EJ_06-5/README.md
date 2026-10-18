# EJ 06-5 · Las minas del emperador Trajano

📄 [Enunciado](<../Enunciados/prob-Las minas del emperador Trajano.pdf>) · 💻 Solución en código: *pendiente* (esta carpeta solo trae la explicación, `GrafoValorado.h` y `ConjuntosDisjuntos.h`)

## Qué piden
Una mina con N cámaras y M galerías (de doble sentido) que hay que recorrer buceando; cada galería tarda un número de segundos. En las cámaras se puede descansar. Desde la cámara de entrada hasta la del tesoro, hay que elegir el camino que **minimice el tiempo máximo que se aguanta la respiración de una vez**, es decir, la galería **más larga** del camino. Escribir ese tiempo, `0` si entrada y tesoro son la misma cámara, o `IMPOSIBLE` si no hay camino.

## Cómo se plantea
Grafo valorado no dirigido: cámaras = vértices, galerías = aristas, tiempo = valor.

> De todos los caminos de `origen` a `destino`, cada uno tiene una arista máxima. Queremos **el camino cuya arista máxima sea la menor posible** (camino *minimax*).

Es el mismo razonamiento que en 06-4, pero ahora **no hace falta conectar todo el grafo, solo estas dos cámaras**:

> Con aristas de valor ≤ T, ¿están `origen` y `destino` en la misma componente? El menor T para el que la respuesta es sí, es la solución.

**Algoritmo (Kruskal con parada temprana)**

1. Si `origen == destino` ⇒ escribir `0` (no hay que bucear).
2. Ordenar las galerías por tiempo creciente. Crear `ConjuntosDisjuntos cd(N)`.
3. Para cada galería `(u, v, t)` en orden:
   - `cd.unir(u, v)`,
   - si ahora `cd.unidos(origen, destino)` ⇒ la respuesta es `t`, **parar**.
4. Si se acaban las galerías sin conseguirlo ⇒ `IMPOSIBLE`.

(Unir también las que ya estaban unidas no hace daño: `unir` no hace nada en ese caso.)

## Por qué funciona
Kruskal añade las galerías en orden de tiempo. La **primera vez** que `origen` y `destino` quedan conectados es porque la galería recién añadida, de tiempo `t`, completa un camino cuyas galerías valen todas ≤ `t`. Antes de ella, con todas las galerías de tiempo menor (o igual, ya vistas), no estaban conectados ⇒ **ningún** camino puede tener su galería máxima por debajo de `t`.

Dicho con el ARM: el camino que mejor evita las galerías largas es el **camino único entre las dos cámaras dentro del árbol de recubrimiento mínimo**.

## Comparación de los tres problemas de Kruskal

| Problema | Pregunta | Qué se guarda | Cuándo se para |
|---|---|---|---|
| 06-3 Archipiélago | coste mínimo para conectar **todo** | **suma** de las aristas aceptadas | al aceptar V − 1 (o se acaban) |
| 06-4 Tarzán | cuerda mínima para conectar **todo** | **última** arista aceptada (la mayor) | cuando queda 1 componente |
| 06-5 Trajano | aguante mínimo entre **dos** cámaras | la arista que las conecta | cuando `unidos(origen, destino)` |

## Por qué así
- **Es un camino con *máximo*, no con *suma*:** no es un problema de caminos mínimos (Dijkstra, que se verá más adelante). Aquí cuentan las galerías largas, no el tiempo total de buceo. Con el mapa del ejemplo 1 se ve: la galería directa 1→4 tarda 10 s; el rodeo 1→2→4 tarda 2 + 5 = 7 s en total pero el máximo es 5 ⇒ la respuesta es 5.
- **Entrada:** hay número de casos. La línea final de cada caso trae `origen destino`, después de las M galerías (el grafo se lee con `GrafoValorado<int> g(cin, 1)` y **luego** se leen origen y destino). Si prefieres no construir el grafo, lee las aristas a un vector.
- **Límites:** N ≤ 20.000, M ≤ 200.000 por caso, y las sumas de N y de M no pasan de 10⁶ ⇒ ordenar es O(M log M), sobrado. Como puede haber muchos casos, la partición se crea con tamaño N en cada caso (no un array enorme fijo que haya que reiniciar entero).
- **Sin galerías repetidas ni bucles** (lo asegura el enunciado), pero el algoritmo tampoco se rompería con ellas.

## Traza del ejemplo 1 (4 cámaras; entrada en 1, tesoro en 4)
```text
Galerías ordenadas:  1-2 (2)   2-4 (5)   1-3 (6)   4-1 (10)

1-2 (2)   unir → {1,2}   {3} {4}        ¿1 y 4 unidos? no
2-4 (5)   unir → {1,2,4} {3}            ¿1 y 4 unidos? sí  → respuesta 5
```
Resultado: **5**.

Ejemplo 2 (N = 1, origen = destino = 1): **0**.
Ejemplo 3 (N = 2, M = 0, de 1 a 2): no hay galerías ⇒ **IMPOSIBLE**.

## Coste
**O(N + M log M)**; en el peor caso se miran todas las galerías.

## Ojo con
- Comprobar `origen == destino` **antes** del bucle: si no, con M = 0 el bucle no se ejecuta y saldría `IMPOSIBLE` en vez de `0`; y con M > 0 se escribiría el tiempo de la primera galería en lugar de `0`.
- Mensaje exacto: `IMPOSIBLE` (mayúsculas), distinto del `Imposible` del 06-4.
- Escribir el **tiempo de una galería** (un máximo), no la suma de las que forman el camino.
