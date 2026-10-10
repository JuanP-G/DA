# EJ 02-L · Cinemáticas digitales

📄 [Enunciado](<../Enunciados/prob-Cinemáticas digitales.pdf>) · 💻 [Solución](EJ_02-L.cpp)

*Ejercicio de laboratorio.*

## Qué piden
R escenas llegan en orden (minuto de envío, duración) a S estaciones idénticas; calcular el **tiempo máximo** que alguna escena pasa **en la cola de espera** antes de empezar a renderizarse.

## Cómo se plantea
Es el mismo esquema que [Reina del súper](../EJ_02-3/README.md): cada escena, en orden, va a la estación que **antes queda libre**. Aquí no importa *qué* estación es, solo *cuándo* se libera.

- Cola de **mínimos** de `long long` con el instante en que se libera cada estación:
  `priority_queue<long long, vector<long long>, greater<long long>>`.
- Al principio hay S ceros (todas libres en el instante 0).

Para cada escena `(minuto, tiempo)`:
1. `libre = top()`, `pop()`: la estación que antes queda libre.
2. `inicio = max(libre, minuto)`: no puede empezar antes de enviarse ni antes de que la estación acabe.
3. `maxT = max(maxT, inicio − minuto)`: lo que ha esperado.
4. `push(inicio + tiempo)`: esa estación queda ocupada hasta entonces.

## Por qué así
- **El `max(libre, minuto)` es la clave:** si la estación ya estaba libre cuando llega la escena, la espera es 0; olvidarlo da esperas negativas o estaciones «que empiezan en el pasado».
- **Basta la estación que antes se libera:** como los envíos vienen ordenados por minuto, ninguna escena posterior puede adelantar a esta.
- Los enteros de la cola no llevan número de estación porque todas son idénticas: no hay desempate que hacer.
- **`long long`:** con 2·10⁶ escenas, los instantes de fin acumulan duraciones y pueden pasar de 2³¹ (el enunciado no acota las duraciones).
- La entrada acaba con fin de fichero (`if (!(cin >> escenas >> estaciones))`).
- **Error típico:** la cola sin `greater<>` daría la estación que **más tarde** se libera.

## Traza del ejemplo
```text
Caso 1: S = 2                                  cola = {0, 0}
  (0,30):  libre 0,  empieza 0,  espera 0,  fin 30   cola = {0, 30}
  (5,20):  libre 0,  empieza 5,  espera 0,  fin 25   cola = {25, 30}
  (10,15): libre 25, empieza 25, espera 15, fin 40   cola = {30, 40}
  (15,10): libre 30, empieza 30, espera 15, fin 40   cola = {40, 40}
  máximo = 15
Caso 3: S = 2
  (0,50) y (0,60) ocupan las dos estaciones         cola = {50, 60}
  (10,5):  libre 50, empieza 50, espera 40, fin 55   cola = {55, 60}
  (25,5):  libre 55, empieza 55, espera 30, fin 60   cola = {60, 60}
  máximo = 40
```
En el caso 2 hay 5 estaciones para 3 escenas: nadie espera → **0**.

## Coste
**O((S + R) log S)** por caso: S inserciones iniciales y, por cada escena, un `pop` y un `push` en una cola de tamaño S.
