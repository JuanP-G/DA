# EJ 09-L · Necesitamos agua

📄 [Enunciado](<../Enunciados/prob-Necesitamos agua.pdf>) · 💻 [Solución](EJ_09-L.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una isla con N puntos (N par, 2..200.000): la desalinizadora norte es el **1**, la sur es el **N** y los N − 2 restantes son pueblos. Hay M carreteras de doble sentido con su coste (1..100.000), y el grafo es conexo. A cada pueblo le llega un camión que sale de una planta, va al pueblo y **vuelve**. Exactamente la **mitad** de los pueblos se sirven desde el norte y la otra mitad desde el sur. Hay que escribir el **coste mínimo total**.

## Cómo se plantea
Dos piezas:
1. **Dijkstra dos veces:** `dN[v]` = distancia mínima desde el 1, y `dS[v]` = distancia mínima desde el N. El camión de `v` cuesta `2·dN[v]` desde el norte o `2·dS[v]` desde el sur.
2. **Voraz para el reparto:** si todos fueran al sur costaría `2·Σ dS`. Pasar el pueblo `v` al norte cambia el coste en `2·(dN[v] − dS[v])`. Hay que pasar exactamente `(N − 2)/2` pueblos, así que se pasan los de **menor diferencia** (los que más ahorran yendo al norte, o los que menos pierden).

```text
total = Σ dS[v]
dif   = [ dN[v] − dS[v] para cada pueblo ]
ordenar dif y sumar las (N − 2)/2 primeras
respuesta = 2 · total
```

## Traza del ejemplo 2
```text
pueblo   dN    dS    dN − dS
  2      15   105     −90
  3      20   100     −80
  4       5   100     −95
  5      20   100     −80
todos al sur: 105 + 100 + 100 + 100 = 405
dos al norte: las diferencias −95 (pueblo 4) y −90 (pueblo 2)  → 405 − 185 = 220
respuesta = 2 · 220 = 440
```
Los cuatro pueblos están más cerca del norte, pero el norte solo tiene camiones para dos.

## Por qué así
- **Por qué vale ordenar diferencias:** el coste total es `Σ dS + Σ_{v al norte} (dN[v] − dS[v])`. El primer término no depende del reparto, así que solo hay que minimizar la suma de `(N − 2)/2` diferencias: las más pequeñas.
- **`GrafoValorado` + `IndexPQ`:** el Dijkstra del tema 7 sobre un grafo no dirigido (`a.otro(v)` en vez de `a.hasta()`).
- **`long long`:** una distancia puede llegar a 100.000 × 200.000.
- **Coste:** O(M log N) por los Dijkstra + O(N log N) por ordenar.

## Ojo con
- Las plantas no son pueblos: se suman los puntos `2..N−1`.
- Con N = 2 no hay pueblos y el coste es 0.
