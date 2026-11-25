# EJ 11-5 · Las vacas pensantes

📄 [Enunciado](../Enunciados/prob-Las%20vacas%20pensantes.pdf) · 💻 [Solución](EJ_11-5.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una hilera de `N` cubos (hasta 1.000) con cantidades **distintas** de comida. Dos vacas se alternan; en su turno cada una come uno de los **dos extremos** y lo retira. Empieza **nuestra vaca**; la otra (Devoradora) **siempre coge el extremo mayor**. Se escribe lo máximo que puede comer nuestra vaca.

## Recurrencia (formato de examen)

Cubos $a_1, \dots, a_N$. Para $1 \le i, j \le N$ (cubos que quedan: $a_i \dots a_j$):

$$
\text{come}(i, j) = \text{máximo que come nuestra vaca con los cubos } i..j \text{ cuando le toca a ella}
$$

Y, auxiliar, lo que le queda **después de su jugada**, cuando le toca a Devoradora (que **sabemos** lo que hará):

$$
\text{despues}(l, r) =
\begin{cases}
0 & \text{si } l > r \\
\text{come}(l+1, r) & \text{si } a_l > a_r \quad (\text{Devoradora se come } a_l) \\
\text{come}(l, r-1) & \text{si } a_l < a_r \quad (\text{Devoradora se come } a_r)
\end{cases}
$$

**Caso base**

$$
\text{come}(i, j) = 0 \qquad \text{si } i > j
$$

**Recurrencia** ($i \le j$)

$$
\text{come}(i, j) = \max\Big( a_i + \text{despues}(i+1, j),\ \ a_j + \text{despues}(i, j-1) \Big)
$$

**Llamada inicial / respuesta:** $\text{come}(1, N)$.

**Orden de cálculo:** cada intervalo depende de otros **más cortos**, así que se rellena por longitudes crecientes ($1, 2, \dots, N$). Coste $O(N^2)$ en tiempo y en espacio.

## Cómo se plantea
Es el típico juego de las monedas en los extremos, pero con una diferencia que lo simplifica: **el rival no es óptimo, es voraz**. Por eso no hace falta un `min` (rival inteligente) sino que su jugada está **determinada**:

```text
come(i, j) = max( a[i] + despues(i+1, j),  a[j] + despues(i, j−1) )

despues(l, r):   si a[l] > a[r]  →  come(l+1, r)
                 si no           →  come(l, r−1)
```
Como las cantidades son todas distintas, nunca hay empate que desempatar.

## Traza del ejemplo 2 (`2 4 15 5`)
```text
empezar por el 5:  Devoradora come el 15 (mayor de 2…15) → quedan 2 4 → ella coge el 4 → 5 + 4 = 9
empezar por el 2:  Devoradora come el 5 (mayor de 4 y 5) → quedan 4 15 → ella coge el 15 → 2 + 15 = 17
come(1, 4) = 17
```
Lo voraz («coge el mayor extremo») daría 9: hay que **mirar lo que deja** para el rival.

## Por qué así
- **No es voraz para nosotros:** coger siempre el extremo mayor falla (ejemplo 2). Hay que comparar las dos jugadas con la tabla.
- **Intervalos que quedan:** tras dos jugadas siempre quedan los cubos de un intervalo `i..j` contiguo, por eso basta una tabla de `N × N`.
- **Memoria:** `N = 1.000` son un millón de enteros, sin problema.

## Ojo con
- Devoradora se mueve **entre** nuestras jugadas: cada paso de la recurrencia incluye nuestro turno **y** el suyo, así que se pasa de `(i, j)` a un intervalo con **dos cubos menos** (o uno si ya no quedan más).
- Con un solo cubo (`i = j`), `despues` de un intervalo vacío es 0 y `come(i, i) = a_i`.
