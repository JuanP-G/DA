# EJ Eval-1 · MasterHash

📄 Enunciado: en el juez de la asignatura (`Eval-1`) · 💻 [Solución](EJ_Eval-1.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N elaboraciones (1..100.000) y A anotaciones (0..200.000) de la forma `X Y`: la elaboración X hace falta para la Y. La elaboración **S se ha quemado** y **P es el plato** que se quiere hacer (pueden coincidir). El plato se puede hacer si **no necesita S** (ni directa ni indirectamente) y las anotaciones de lo que necesita **no tienen ciclos**. Hay que escribir `NO`, o `SI` seguido de un orden válido de las elaboraciones necesarias que acabe en P.

## Cómo se plantea
Es un problema de **digrafos** (tema 5) en tres pasos:
1. **Qué hace falta para P:** los vértices desde los que se llega a P. En el grafo **inverso** son los alcanzables desde P, con un recorrido desde P en `g.inverso()`.
2. **¿Necesita el sofrito?** Si S está entre ellos (incluido `S == P`): `NO`.
3. **Orden topológico solo de esos vértices** (algoritmo de Kahn): se cuentan las aristas de entrada dentro del conjunto y se van sacando los que no tienen ninguna pendiente. Si no salen todos, hay un ciclo entre las elaboraciones necesarias: `NO`.

Como todos los vértices del conjunto llegan a P, **P sale el último**. Se usa una cola de prioridad de mínimos para que salga siempre la disponible de menor número, que da el orden del ejemplo.

## Traza del ejemplo 1 (S = 1, P = 5)
```text
aristas: 2→4 3→4 4→5 5→6 6→7 7→6 1→7
necesarias para 5 (inverso desde 5): 5, 4, 2, 3       S = 1 no está ✓
entradas dentro del conjunto: 2:0  3:0  4:2  5:1
Kahn: 2 → 3 → 4 → 5                                      → SI 2 3 4 5
```
El ciclo 6 ↔ 7 no importa: 5 no necesita ni el 6 ni el 7.

En el ejemplo 2, el 5 necesita el 2, que es el quemado: `NO`. En el ejemplo 3, el 4 necesita el 3, y entre el 2 y el 3 hay un ciclo: `NO`.

## Por qué así
- **El inverso** convierte «quién llega a P» en «a quién llega P», que es un recorrido normal.
- **Kahn en vez de DFS:** detecta el ciclo (no salen todos) y da el orden a la vez.
- **Coste:** O(N + A log N) por caso.

## Ojo con
- Un ciclo **fuera** de lo que necesita P no hace imposible el plato.
- Si `S == P` el plato está quemado: `NO`.
