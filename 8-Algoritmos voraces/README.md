# Algoritmos voraces (temas 8 y 9) · resumen

🎬 Vídeo: [`08-0_algoritmos_voraces_teoria.mp4`](../Videos/08-0_algoritmos_voraces_teoria.mp4)

## La idea
Un algoritmo voraz construye la solución paso a paso y en cada paso coge **la opción que mejor parece ahora**, sin volver atrás. Es rápido y sencillo, pero **no siempre acierta**: con monedas de 1, 3 y 4, para devolver 6 coge 4 + 1 + 1 (tres monedas) cuando 3 + 3 son dos.

## La receta
1. **Criterio**: qué se coge primero. Casi siempre, ordenar por algo.
2. **Probar**: buscar contraejemplos pequeños para descartar las ideas que fallan.
3. **Demostrar**: normalmente con un **argumento de intercambio**. Se compara la voraz con una solución óptima cualquiera y, en la primera diferencia, se cambia lo del óptimo por lo que eligió la voraz: si sigue siendo válida y no es peor, repitiendo se llega a la voraz sin empeorar.
4. **Programar**: suele ser `sort` + un bucle, `O(N log N)`.

## Patrones de los ejercicios
| Patrón | Criterio | Ejercicios |
|---|---|---|
| Selección de actividades | ordenar por **fin** y coger lo compatible | [08-4](EJ_08-4/README.md) |
| Pinchar puntos o intervalos | cada parche/pasadizo lo más a la derecha posible | [08-1](EJ_08-1/README.md), [09-1](../9-Algoritmos%20voraces%20II/EJ_09-1/README.md) |
| Cubrir un intervalo | de lo que no deja hueco, lo que llega más lejos | [09-2](../9-Algoritmos%20voraces%20II/EJ_09-2/README.md) |
| Emparejar (dar lo justo / extremos) | el más pequeño que sirve; débil con fuerte, dos punteros | [08-2](EJ_08-2/README.md), [09-3](../9-Algoritmos%20voraces%20II/EJ_09-3/README.md), [09-4](../9-Algoritmos%20voraces%20II/EJ_09-4/README.md) |
| Con cola de prioridad | reutilizar lo que queda libre antes | [08-L](EJ_08-L/README.md) |
| Voraz + otra técnica | contar por tallas; Dijkstra y ordenar diferencias | [08-3](EJ_08-3/README.md), [09-L](../9-Algoritmos%20voraces%20II/EJ_09-L/README.md) |

Kruskal, Prim (tema 6) y Dijkstra (tema 7) también son voraces: una elección local que nunca se deshace, cada una con su demostración.

## Voraz frente a programación dinámica
| Voraz | Programación dinámica |
|---|---|
| una sola elección por paso, sin volver atrás | prueba todas las opciones y guarda subproblemas |
| `O(N log N)` típico | tabla, `O(N·M)` típico |
| hay que demostrar que es óptimo | correcta por la recurrencia |
