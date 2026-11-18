# EJ 11-1 · El cazatesoros

📄 Enunciado: en el juez de la asignatura (`Ej11-1`) · 💻 [Solución](EJ_11-1.cpp)

## Qué piden
Una botella de T segundos de aire (1..10.000) y N cofres (1..100), cada uno con su profundidad p (1..500) y su oro (1..10.000). Bajar a p cuesta p segundos y subir cuesta 2p, y en cada inmersión se sube **un solo cofre**. Hay que escribir el **máximo oro**, cuántos cofres hay que coger y **cuáles** (profundidad y oro como en la entrada), y después `---`. Vale cualquier solución óptima, con los cofres en cualquier orden.

## Cómo se plantea
Es la **mochila 0/1**: cada cofre es un objeto de **peso 3p** (segundos) y **valor** su oro, con capacidad T.

```text
oro(i, j) = máximo oro con los cofres 1..i y j segundos

oro(0, j) = 0
oro(i, j) = oro(i−1, j)                                     si 3·p_i > j
          = max(oro(i−1, j), oro(i−1, j − 3·p_i) + o_i)     si no
```

**Reconstrucción** desde `(N, T)` hacia atrás: si `oro(i, j) ≠ oro(i−1, j)`, el cofre i se ha cogido y se pasa a `(i−1, j − 3·p_i)`. Se marcan los cofres cogidos y se escriben en el orden de la entrada.

## Traza del ejemplo 2 (T = 200)
```text
cofre  (25,4)  (50,5)  (40,4)  (10,2)  (70,10)
tiempo   75     150     120      30     210  ← no cabe nunca
voraz por oro: (50,5) + (10,2) = 7  en 180 s
óptimo:        (25,4) + (40,4) = 8  en 195 s
```
Coger primero el más valioso que cabe no es lo mejor: hace falta la tabla.

## Por qué así
- **Tabla entera:** con una sola fila se sabe el oro máximo, pero no qué cofres lo dan.
- **Coste:** O(N·T) en tiempo y en espacio (como mucho 10⁶ casillas).

## Ojo con
- Si no cabe ningún cofre (ejemplo 3) se escribe `0`, `0` y `---`.
- En el ejemplo 4 hay dos soluciones de 11 monedas: esta solución escribe `12 7` y `8 4`, y el enunciado `10 5` y `10 6`. El juez acepta las dos.
