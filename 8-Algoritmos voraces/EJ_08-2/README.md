# EJ 08-2 · ¡Nos invaden!

📄 Enunciado: en el juez de la asignatura (`Ej08-2`) · 💻 [Solución](EJ_08-2.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N ciudades invadidas (1 ≤ N ≤ 300.000), cada una con sus efectivos enemigos, y N equipos de defensa con sus efectivos. Se asigna **un equipo por ciudad**. La victoria está garantizada si el equipo tiene **al menos** tantos efectivos como el enemigo. Hay que escribir el **máximo número de victorias garantizadas**.

## Cómo se plantea
Voraz con los dos vectores **ordenados**:
- A la ciudad más fácil (la de menos enemigos) se le manda el **equipo más pequeño que la gana**. Uno más grande se desperdiciaría ahí y podría hacer falta en una ciudad más difícil.
- Un equipo que no gana a la ciudad más fácil no gana a ninguna, así que se descarta (se manda a una ciudad que se pierde de todas formas).

```text
ordenar enemigos y equipos
i = 0                                // ciudad más fácil sin defender
para cada equipo j (de menor a mayor):
    si equipos[j] >= enemigos[i]:  victorias++,  i++
```

## Traza del ejemplo 1
```text
enemigos: 20 30 40 80        equipos: 25 35 40 50
25 ≥ 20 ✓   35 ≥ 30 ✓   40 ≥ 40 ✓ (basta con igualar)   50 ≥ 80 ✗   → 3
```

## Por qué así
- **Intercambio:** si una solución óptima defiende la ciudad más fácil con un equipo mayor que el mínimo que la gana, intercambiar ese equipo con el mínimo sigue ganando las dos ciudades. Así siempre hay una solución óptima que coincide con la voraz.
- **Coste:** O(N log N) por las ordenaciones; el recorrido es lineal.

## Ojo con
- La condición es `>=`: con los mismos efectivos que el enemigo también se gana.
