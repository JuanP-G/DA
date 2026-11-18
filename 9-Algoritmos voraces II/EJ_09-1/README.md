# EJ 09-1 · ¡En primera línea de playa!

📄 Enunciado: en el juez de la asignatura (`Ej09-1`) · 💻 [Solución](EJ_09-1.cpp)

## Qué piden
N edificios (1 ≤ N ≤ 100.000), cada uno con su extremo occidental W y oriental E (enteros 0..10⁹). Un pasadizo de **1 metro de ancho** le sirve a un edificio si queda **completamente debajo** de él: el pasadizo del metro `[x, x+1]` sirve a `[W, E]` si `W ≤ x` y `x + 1 ≤ E`. Hay que escribir el **mínimo número de pasadizos** para que todos los edificios tengan uno.

## Cómo se plantea
Es el problema de «pinchar» intervalos con el mínimo número de puntos. Voraz:
- Se ordenan los edificios por su extremo **oriental**.
- El que acaba antes necesita un pasadizo, y lo mejor es ponerlo **lo más al este posible** dentro de él, en el metro `[E − 1, E]`. Así sirve también a todos los que empiezan como muy tarde en `E − 1`.
- Recorriendo en ese orden, un edificio ya está servido si `W ≤ x` (su E es mayor o igual, así que `x + 1 ≤ E`). Si no, se pone un pasadizo nuevo en su metro más oriental.

## Traza del ejemplo 1
```text
ordenados por E:  [1,4]  [2,10]  [6,15]  [12,20]
[1,4]   → pasadizo en [3,4]
[2,10]  → 2 ≤ 3 ✓
[6,15]  → 6 > 3 → pasadizo en [14,15]
[12,20] → 12 ≤ 14 ✓                         total = 2
```

## Por qué así
- **El metro más oriental:** cualquier pasadizo que sirva al edificio que acaba antes está en `[x, x+1]` con `x ≤ E − 1`. Moverlo a `E − 1` sigue sirviéndole y no deja de servir a ningún otro que acabe más tarde.
- **Coste:** O(N log N) por caso.

## Ojo con
- **Tocarse en un punto no basta:** `[1,4]` y `[4,8]` no comparten ningún metro (ejemplo 2), por eso se compara `W ≤ E − 1` y no `W ≤ E`.
