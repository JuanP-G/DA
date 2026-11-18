# EJ 10-1 · La cuerda de la cometa

📄 Enunciado: en el juez de la asignatura (`Ej10-1`) · 💻 [Solución](EJ_10-1.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N cordeles (1..1.000), cada uno con su longitud y su coste (1..1.000), y una longitud L (1..1.000). Cada cordel se usa **como mucho una vez** y el orden de unión no importa. Si se puede formar exactamente L, hay que escribir `SI` y tres respuestas por separado: el **número de formas**, el **mínimo número de cordeles** y el **mínimo coste**. Si no se puede, `NO`.

## Recurrencias (formato de examen)

Cordeles numerados $1..N$, con longitud $l_i$ y coste $c_i$. Para $0 \le i \le N$ y $0 \le j \le L$ se definen tres funciones sobre «los cordeles $1..i$ y la longitud $j$»:

- $\text{formas}(i, j)$: número de formas de sumar exactamente $j$ con los cordeles $1..i$.
- $\text{cordeles}(i, j)$: mínimo número de cordeles para sumar exactamente $j$ con los cordeles $1..i$.
- $\text{coste}(i, j)$: mínimo coste para sumar exactamente $j$ con los cordeles $1..i$.

**Casos base**

$$
\text{formas}(i, 0) = 1 \qquad \text{cordeles}(i, 0) = 0 \qquad \text{coste}(i, 0) = 0 \qquad \forall\, i \ge 0
$$

$$
\text{formas}(0, j) = 0 \qquad \text{cordeles}(0, j) = +\infty \qquad \text{coste}(0, j) = +\infty \qquad \forall\, j > 0
$$

**Recurrencias** ($1 \le i \le N$, $1 \le j \le L$)

$$
\text{formas}(i, j) =
\begin{cases}
\text{formas}(i-1, j) & \text{si } l_i > j \\
\text{formas}(i-1, j) + \text{formas}(i-1,\ j - l_i) & \text{si } l_i \le j
\end{cases}
$$

$$
\text{cordeles}(i, j) =
\begin{cases}
\text{cordeles}(i-1, j) & \text{si } l_i > j \\
\min\big(\text{cordeles}(i-1, j),\ \text{cordeles}(i-1,\ j - l_i) + 1\big) & \text{si } l_i \le j
\end{cases}
$$

$$
\text{coste}(i, j) =
\begin{cases}
\text{coste}(i-1, j) & \text{si } l_i > j \\
\min\big(\text{coste}(i-1, j),\ \text{coste}(i-1,\ j - l_i) + c_i\big) & \text{si } l_i \le j
\end{cases}
$$

En cada caso: o **no se usa** el cordel $i$ (fila $i-1$, misma longitud), o **se usa** y queda por sumar $j - l_i$ con los anteriores (fila $i-1$: cada cordel solo una vez).

**Llamada inicial / respuesta:** si $\text{formas}(N, L) = 0$ se escribe `NO`; si no, `SI` $\text{formas}(N, L)$ $\text{cordeles}(N, L)$ $\text{coste}(N, L)$.

**Implementación:** la fila $i$ solo depende de la $i-1$, así que basta un vector por función recorriendo $j$ **de $L$ hacia abajo** (así $j - l_i$ aún tiene el valor de la fila $i-1$). Coste $O(N \cdot L)$ en tiempo y $O(L)$ en espacio.

## Cómo se plantea
Programación dinámica tipo **mochila 0/1 con suma exacta**: tres tablas sobre las longitudes `j = 0..L`, añadiendo los cordeles uno a uno.

```text
formas[j]   = nº de subconjuntos que suman j          formas[0] = 1
cordeles[j] = mínimo nº de cordeles para sumar j      cordeles[0] = 0   (INF si no se puede)
coste[j]    = mínimo coste para sumar j               coste[0] = 0      (INF si no se puede)

al añadir el cordel (l, c), para j = L, L−1, …, l:
    formas[j]   += formas[j − l]
    cordeles[j]  = min(cordeles[j], cordeles[j − l] + 1)
    coste[j]     = min(coste[j],    coste[j − l] + c)
```

Se recorre `j` **de mayor a menor** para que cada cordel se use una sola vez: `j − l` todavía tiene el valor de antes de añadir este cordel. De menor a mayor sería la versión con cordeles ilimitados.

## Traza del ejemplo 4 (L = 10)
```text
cordeles: (10, 50)  (5, 10)  (5, 10)
tras (10,50):  formas[10] = 1   cordeles[10] = 1   coste[10] = 50
tras (5,10):   formas[5]  = 1
tras (5,10):   formas[10] += formas[5] → 2
               cordeles[10] = min(1, 1 + 1) = 1      coste[10] = min(50, 10 + 10) = 20
→ SI 2 1 20
```
La forma con menos cordeles no es la más barata: cada pregunta se responde por separado.

## Por qué así
- **Una sola pasada para las tres preguntas:** las tres recurrencias tienen la misma forma y se rellenan a la vez.
- **`long long` en `formas`:** el enunciado garantiza como mucho 10¹⁸ formas para cualquier longitud.
- **Coste:** O(N·L) en tiempo y O(L) en espacio.

## Ojo con
- Cordeles con la misma longitud **son distintos** (en el ejemplo 3, tres cordeles de 1 dan 3 formas de hacer 2).
- Si `formas[j − l] == 0` no hay que tocar nada: así `INF + 1` nunca se calcula.
