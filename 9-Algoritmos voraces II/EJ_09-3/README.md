# EJ 09-3 · Carreras de coches

📄 [Enunciado](<../Enunciados/prob-Carreras de coches.pdf>) · 💻 [Solución](EJ_09-3.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N pilas (1 ≤ N ≤ 300.000) con su voltaje (0..10⁶) y un voltaje mínimo V. Cada coche necesita **dos pilas cuyos voltajes sumen al menos V**. Hay que escribir el **máximo número de coches** que pueden funcionar a la vez.

## Cómo se plantea
Voraz emparejando los **extremos** del vector ordenado. Se miran la pila más débil (`i`) y la más fuerte (`j`):
- si juntas llegan a V, forman un coche: la más débil que acompaña bien a la más fuerte es la mejor pareja para ella, y las potentes quedan para las demás;
- si no llegan, la más débil **no sirve con ninguna** (ni con la más fuerte llega) y se descarta.

```text
ordenar; i = 0, j = N − 1
mientras i < j:
    si pilas[i] + pilas[j] >= V:  coches++, i++, j--
    si no:                        i++
```

## Traza del ejemplo 1 (V = 20)
```text
8 10 12 15
8 + 15 = 23 ≥ 20 ✓      10 + 12 = 22 ≥ 20 ✓            → 2 coches
```
Juntar las dos más potentes (15 + 12) dejaría 8 + 10 = 18: un solo coche.

## Por qué así
- **Intercambio:** si en una solución óptima la más débil útil va con otra pila, cambiar su pareja por la más fuerte sigue funcionando (la más fuerte suma aún más) y la pila liberada puede ocupar el sitio que dejó la más fuerte.
- **Coste:** O(N log N) por caso.

## Ojo con
- La condición es «al menos V» (`>=`).
- Con V = 0 cualquier pareja vale: N / 2 coches.
