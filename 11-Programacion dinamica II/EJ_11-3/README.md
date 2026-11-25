# EJ 11-3 · La colecta de primavera

📄 [Enunciado](../Enunciados/prob-La%20colecta%20de%20primavera.pdf) · 💻 [Solución](EJ_11-3.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
`V` vecinos (hasta 1.000) y `C` cajas de galletas (0 a 4·V). Cada vecino pagaría una cantidad distinta por 1, 2, 3 o 4 cajas (por 0, nada). Se reparten **como mucho `C` cajas**, **como mucho 4 a cada vecino**, para **recaudar lo máximo**. Se escribe el beneficio y cuántas cajas se vende a cada vecino (vale cualquier reparto óptimo).

## Recurrencia (formato de examen)

Vecinos $1..V$; $\text{pago}(i, k)$ = lo que paga el vecino $i$ por $k$ cajas ($1 \le k \le 4$), con $\text{pago}(i, 0) = 0$.

$$
\text{dinero}(i, j) = \text{máxima recaudación con los vecinos } 1..i \text{ y como mucho } j \text{ cajas}
$$

**Casos base**

$$
\text{dinero}(0, j) = 0 \qquad 0 \le j \le C
$$

**Recurrencia** ($1 \le i \le V$, $0 \le j \le C$)

$$
\text{dinero}(i, j) = \max_{0 \le k \le \min(4,\, j)} \Big( \text{dinero}(i-1,\ j-k) + \text{pago}(i, k) \Big)
$$

**Llamada inicial / respuesta:** $\text{dinero}(V, C)$.

**Reconstrucción** desde $(V, C)$ con $i = V, V-1, \dots, 1$: se busca un $k$ con $\text{dinero}(i, j) = \text{dinero}(i-1, j-k) + \text{pago}(i, k)$; ese es el número de cajas del vecino $i$ y se pasa a $(i-1, j-k)$.

**Coste:** $O(V \cdot C \cdot 4)$ en tiempo y $O(V \cdot C)$ en espacio (tabla entera para reconstruir; unos 4 millones de casillas como mucho).

## Cómo se plantea
Es una **mochila con grupos**: cada vecino es un grupo del que hay que elegir **una** opción (0, 1, 2, 3 o 4 cajas, cada una con su «peso» en cajas y su «valor» en dinero). Como la capacidad es «como mucho `C`», `dinero(0, j) = 0` para todo `j` y no hace falta un valor especial para «sobran cajas».

```text
dinero[0][j] = 0
para cada vecino i, para cada j de 0 a C:
    dinero[i][j] = max sobre k de 0 a min(4, j) de  dinero[i−1][j−k] + pago[i][k]
```

Después se reconstruye hacia atrás eligiendo en cada vecino el `k` que explica el valor de la tabla.

## Traza del ejemplo 1 (3 vecinos, 5 cajas)
```text
pago   vecino1: 10  5  6  7      vecino2: 0 100 100 100      vecino3: 5 4 4 4
 (1, 2, 3 y 4 cajas)

vecino 1 → 1 caja (10)      vecino 3 → 1 caja (5)
vecino 2 → 2 cajas (100)    total = 10 + 100 + 5 = 115, sobra 1 caja
```
La salida `1 2 1` (o `1 3 1`) vale; con 2 o 3 cajas el vecino 2 paga lo mismo, así que cualquiera es óptima.

## Por qué así
- **No es voraz:** repartir cajas al que más paga por caja no sirve, porque cada vecino tiene una tabla de precios distinta (hay quien solo paga por lotes de 2 y quien paga más por una sola).
- **Mirar solo `k` hasta 4** hace la transición `O(1)` y el total `O(V·C)`.

## Ojo con
- **No hay que vender todas las cajas:** el tercer ejemplo (un vecino que paga menos cuantas más cajas compra) deja 3 cajas sin vender.
- Hay varias respuestas válidas; el juez acepta cualquier reparto con el beneficio máximo (y como mucho `C` cajas).
- Las cuatro líneas de entrada son **por número de cajas** (1, 2, 3, 4), cada una con los `V` vecinos; no por vecino. En el código se guardan como `pago[i][k]`.
