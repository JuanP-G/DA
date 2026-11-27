# EJ 12-1 · El carpintero Ebanisto

📄 [Enunciado](<../Enunciados/prob-El carpintero Ebanisto.pdf>) · 💻 [Solución](EJ_12-1.cpp) · 🎬 [Vídeo](<../../Videos/12-1_el_carpintero_ebanisto.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Un tablón de longitud L (10..1.000.000) con N marcas (1..500), dadas en orden creciente. Cortar un trozo de madera en dos cuesta **el doble de su longitud**. Hay que escribir el **mínimo esfuerzo** para hacer todos los cortes, eligiendo bien el orden.

## Recurrencias (formato de examen)

Puntos $p_0 = 0$, $p_1 < \dots < p_N$ las marcas y $p_{N+1} = L$. Para $0 \le i < j \le N+1$:

- $\text{esfuerzo}(i, j)$: mínimo esfuerzo para hacer todos los cortes que hay entre $p_i$ y $p_j$ en el trozo que va de $p_i$ a $p_j$.

**Casos base**

$$
\text{esfuerzo}(i, i+1) = 0 \qquad \text{(trozo sin marcas dentro)}
$$

**Recurrencia** ($j - i \ge 2$)

$$
\text{esfuerzo}(i, j) = 2\,(p_j - p_i) + \min_{i < k < j} \big(\text{esfuerzo}(i, k) + \text{esfuerzo}(k, j)\big)
$$

El primer corte del trozo cuesta $2\,(p_j - p_i)$ se haga por la marca que se haga. Si se hace por la marca $k$, quedan dos trozos independientes, $(i, k)$ y $(k, j)$.

**Llamada inicial / respuesta:** $\text{esfuerzo}(0, N+1)$.

**Implementación:** tabla $(N+2) \times (N+2)$ rellenada **por longitud de intervalo creciente** ($j - i = 2, 3, \dots, N+1$): así $(i, k)$ y $(k, j)$ ya están calculados. Coste $O(N^3)$ en tiempo y $O(N^2)$ en espacio por caso.

## Cómo se plantea
```text
p = 0, c1, ..., cN, L
esfuerzo[i][i+1] = 0
para d = 2 .. N+1:                 ← longitud del intervalo, j − i
    para i = 0 .. N+1−d:
        j = i + d
        esfuerzo[i][j] = 2·(p[j] − p[i]) + min_{i<k<j} (esfuerzo[i][k] + esfuerzo[k][j])
respuesta: esfuerzo[0][N+1]
```

## Traza del ejemplo 1 (L = 10, marcas 3, 6, 8)
```text
p = 0 3 6 8 10
d = 2:  (0,2) = 2·6 + 0 = 12     (1,3) = 2·5 + 0 = 10     (2,4) = 2·4 + 0 = 8
d = 3:  (0,3) = 16 + min(0 + 10, 12 + 0) = 26
        (1,4) = 14 + min(0 + 8, 10 + 0)  = 22
d = 4:  (0,4) = 20 + min( k=1: 0 + 22,  k=2: 12 + 8,  k=3: 26 + 0 ) = 20 + 20 = 40
→ 40   (primero por el 6, luego el 3 y el 8)
```

## Por qué así
- **No vale un voraz** (cortar por la marca más centrada, o en orden): el ejemplo del enunciado ya muestra que el orden 3, 6, 8 cuesta 42 y el óptimo, 40.
- **El coste del primer corte no depende de $k$:** por eso sale de la minimización y la recurrencia es la típica de «partir un intervalo» (como el producto de matrices encadenadas).
- **Por longitud creciente:** cada intervalo solo necesita intervalos más cortos.

## Ojo con
- El esfuerzo es **el doble** de la longitud del trozo que se corta, no la longitud.
- Los extremos 0 y L cuentan como puntos: sin ellos falta el primer corte.
- Probar todos los órdenes de corte (N!) o la recursión sin memoria no termina con N = 500.
