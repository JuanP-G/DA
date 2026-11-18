# EJ 08-3 · Comienza la temporada

📄 Enunciado: en el juez de la asignatura (`Ej08-3`) · 💻 [Solución](EJ_08-3.cpp)

## Qué piden
N jugadores y M equipaciones (1 ≤ N, M ≤ 100.000), cada uno con una talla entre 1 y 100. Un jugador puede usar una equipación **de su talla o de una talla más**. Hay que escribir el **mínimo número de equipaciones que comprar** para que jueguen todos.

## Cómo se plantea
Solo hay 100 tallas, así que se **cuentan** jugadores y equipaciones de cada talla. Después, voraz recorriendo las tallas **de menor a mayor**. Los jugadores de talla `t`:
1. usan primero las equipaciones de **su talla** (los de talla `t − 1` ya están atendidos, así que nadie más las quiere);
2. si faltan, usan las de **talla `t + 1`**, que se descuentan para los jugadores de esa talla;
3. los que sigan sin equipación son las que hay que comprar.

**Por qué es óptimo:** una equipación de talla `t + 1` la pueden usar los de talla `t` o los de `t + 1`. Si se la queda uno de talla `t`, el de talla `t + 1` todavía puede usar una de `t + 2`. El de talla `t`, en cambio, no tiene otra opción. Dársela al de talla `t` nunca empeora.

## Traza del ejemplo 2
```text
jugadores:     10 ×1   12 ×1   13 ×1
equipaciones:  11 ×1   12 ×1   14 ×1   15 ×1
t = 10: de su talla 0, de la 11 → 1 ✓
t = 12: de su talla 1 ✓
t = 13: de su talla 0, de la 14 → 1 ✓                    comprar = 0
```

## Por qué así
- **Contar en vez de ordenar:** con tallas 1..100 cada caso es O(N + M + 100).
- **El vector tiene hueco para la talla 101:** los de talla 100 miran `equipaciones[101]`, que vale 0.

## Ojo con
- Las equipaciones **más pequeñas** no sirven (en el ejemplo 1, la de talla 10 no la puede usar nadie de talla 12).
