# Plantillas del juez

Las tres plantillas de la asignatura. Todas tienen la misma forma: la solución va entre `//@ <answer>` y `//@ </answer>`, y el comentario general (cómo se resuelve y su coste) en el bloque `/*@ <answer> ... @ </answer> */`. El `main` no se toca: fuera del juez (`#ifndef DOMJUDGE`) lee de `casos.txt`.

| Plantilla | Cuándo | `resuelveCaso` | Fin de la entrada |
|---|---|---|---|
| [1 · Número de casos](1.NumeroCasos.cpp) | La entrada **empieza con el número de casos** | `void` | El `main` hace `numCasos` llamadas |
| [2 · Centinela](2.Centinela.cpp) | Un **valor especial** marca el final (p. ej. `0 0`) | `bool` | `if (es el centinela) return false;` |
| [3 · Casos ilimitados](3.CasosIlimitados.cpp) | No hay número de casos ni centinela: **hasta el final del fichero** | `bool` | `if (!cin) return false;` tras leer el primer dato |

Cómo saber cuál: mira la sección **Entrada** del enunciado.
- «La entrada comienza con el número de casos de prueba…» → **1**.
- «La entrada termina con una línea con …» → **2**.
- Nada de eso («la entrada está formada por una serie de casos…») → **3**.

Ojo: el enunciado manda. En 07-5 el juez de la asignatura da el número de casos aunque en Acepta el Reto el mismo problema se lee hasta el final del fichero.
