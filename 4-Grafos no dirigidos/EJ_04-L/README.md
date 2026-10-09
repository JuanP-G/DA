# EJ 04-L · Peaje a la sombra

📄 [Enunciado](<../Enunciados/prob-Peaje a la sombra.pdf>) · 💻 [Solución](EJ_04-L.cpp) · 🎬 [Vídeo](../../Videos/04-L_peaje_a_la_sombra.mp4)

## Qué piden
Álex y Lucas salen de casas distintas hacia el mismo trabajo. Cada tramo de calle cuesta 1 € y, si van juntos por un tramo, lo paga solo uno. Hay que dar el **mínimo de tramos distintos** que recorren entre los dos.

## Cómo se plantea
Si se encuentran en un cruce `m`, los caminos tienen forma de **Y**: cada uno va solo hasta `m` y desde `m` siguen juntos hasta el trabajo.

```text
Álex  ---\
          m --- trabajo
Lucas ---/
```

El coste es `dist(Álex, m) + dist(Lucas, m) + dist(m, trabajo)`: el trozo común se cuenta una sola vez.

1. Tres **BFS**: desde Álex (`dA`), desde Lucas (`dL`) y desde el trabajo (`dT`). Como las calles son de doble sentido, `dist(m, trabajo) = dT[m]`.
2. Se prueban **todos** los vértices `m` y se queda el menor `dA[m] + dL[m] + dT[m]`.

## Por qué así
- **Para un `m` fijo** lo mejor es usar caminos mínimos, así que solo cuentan esas tres distancias.
- **No hay que tratar casos aparte:** `m = trabajo` es «cada uno va solo» y `m = casa de Álex` (o de Lucas) es «uno pasa por la casa del otro y siguen juntos». El mínimo sobre todos los `m` los incluye.
- **Cada uno por su camino mínimo no basta:** en el ejemplo 1 darían 3 + 2 = 5, pero quedando en el cruce 2 se paga 1 + 1 + 2 = 4.
- Un BFS es suficiente porque el grafo no tiene pesos.

## Traza del ejemplo 1 (`A = 1`, `L = 3`, `T = 6`)
```text
vértice   dA  dL  dT   suma
   1       0   2   3     5
   2       1   1   2     4   ← mínimo
   3       2   0   2     4   ← también (Álex pasa por casa de Lucas)
   4       3   1   1     5
   5       2   2   1     5
   6       3   2   0     5
```
Respuesta **4**. En el ejemplo 2 (`4 3 4 1 3`, una línea) el mínimo sale en `m = 3`, el propio trabajo: 1 + 2 + 0 = **3**.

## Coste
**O(N + C)** por caso (tres BFS y una pasada por los vértices). Las sumas valen como mucho `3·N`, caben en un `int`.
