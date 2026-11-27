# EJ 12-4 · Mejor no llevar muchas monedas

📄 [Enunciado](<../Enunciados/prob-Mejor no llevar muchas monedas.pdf>) · 💻 [Solución](EJ_12-4.cpp) · 🎬 [Vídeo](<../../Videos/12-4_mejor_no_llevar_muchas_monedas.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
`N` tipos de moneda (1..100); del tipo $i$ hay $c_i$ monedas de valor $v_i$ (1..1.000). Pagar **exactamente** el precio $P$ (1..10.000) con el **menor número de monedas**. Se escribe `SI` y cuántas de cada tipo, o `NO`.

## Recurrencia (formato de examen)

- $\text{monedas}(i, j)$: mínimo número de monedas para pagar $j$ usando los tipos $1..i$ ($0 \le i \le N$, $0 \le j \le P$).

**Casos base**

$$
\text{monedas}(0, 0) = 0, \qquad \text{monedas}(0, j) = +\infty \quad (j > 0)
$$

**Recurrencia** ($1 \le i \le N$)

$$
\text{monedas}(i, j) = \min_{\substack{0 \le k \le c_i \\ k\, v_i \le j}} \big(\text{monedas}(i-1,\ j - k\, v_i) + k\big)
$$

**Llamada inicial / respuesta:** $\text{monedas}(N, P)$; si vale $+\infty$, `NO`.

**Reconstrucción:** desde $(N, P)$, para $i = N, \dots, 1$ se busca el $k$ con $\text{monedas}(i-1, j - k v_i) + k = \text{monedas}(i, j)$, se apunta y se sigue en $j - k v_i$.

**Coste:** $O\big(P \cdot \sum_i \min(c_i, P / v_i)\big)$ en tiempo y $O(N P)$ en espacio (hace falta la tabla entera para reconstruir).

## Cómo se plantea
Es el problema del cambio de las transparencias con una diferencia: **no hay monedas ilimitadas**. Para cada tipo se decide cuántas usar, de 0 a las que haya.

## Traza del ejemplo 3 (valores 15 10 5, dos de cada, precio 20)
```text
j:                  0   5  10  15  20
solo la de 15       0   -   -   1   -
añadiendo la de 10  0   -   1   1   2   (10 + 10)
añadiendo la de 5   0   1   1   1   2   (empata 15 + 5, no mejora)
```
Cualquier solución con 2 monedas vale: `SI 0 2 0` o `SI 1 0 1`.

## Por qué así
- **Voraz no:** coger siempre la moneda mayor puede fallar. Con 15, 10, 10 para pagar 20, la de 15 deja 5 imposible.
- **La fila «anterior» es obligatoria:** usar `monedas(i, j − v)` (la misma fila) supondría monedas ilimitadas.
- **Reconstruir con la tabla:** no hace falta guardar las decisiones aparte.

## Ojo con
- $+\infty + k$ no puede desbordar: por eso se usa `EntInf` ([`EnterosInf.h`](EnterosInf.h)).
- La salida lleva **un número por tipo**, en el orden de la entrada, también los ceros.
- En el peor caso (100 tipos de valor 1) son unos $10^9$ pasos muy sencillos: entra en tiempo, pero conviene compilar con optimización.
