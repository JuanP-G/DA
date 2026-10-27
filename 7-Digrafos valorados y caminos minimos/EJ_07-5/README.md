# EJ 07-5 · ¿Cuál es el mejor camino?

📄 [Enunciado](<../Enunciados/prob-¿Cuál es el mejor camino_.pdf>) · 💻 [Solución](EJ_07-5.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#504 · ¿Cuál es el mejor camino?](https://aceptaelreto.com/problem/statement.php?id=504) — *casi el mismo problema*. Mismo enunciado, pero allí no hay número de casos (se lee hasta el final del fichero) y el separador tras cada caso es `----` (cuatro guiones) en vez de `---`.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-504_cual_es_el_mejor_camino.cpp`](<../../Acepta el Reto/ACR-504_cual_es_el_mejor_camino.cpp>)
<!-- acr:fin -->

## Qué piden
Ciudad con N intersecciones (2 ≤ N ≤ 20.000) y C calles de doble sentido con longitud 1..5.000. Para cada una de K ≤ 10 consultas (origen y destino distintos) hay que escribir la **distancia mínima** seguida de:
- `SI` si algún camino de esa distancia usa además el **menor número de calles** posible entre los dos puntos,
- `NO` si no,
- `SIN CAMINO` (sin distancia) si no se puede llegar.

Después de cada caso, una línea `---`. La primera línea de la entrada es el **número de casos**; cada caso empieza con su N.

## Cómo se plantea
Hay que comparar **dos** cosas desde el origen:

1. **Menor número de calles posible**, sin mirar la longitud → recorrido en **anchura** (`calles[v]`).
2. **Distancia mínima** y, entre los caminos que la consiguen, el de **menos calles** → **Dijkstra** con prioridad una pareja `(distancia, calles)` comparada en ese orden (`pasos[v]`).

Respuesta: la distancia, y `SI` si `pasos[destino] == calles[destino]` (el camino más corto en distancia **también** es de los de menos calles), `NO` si `pasos > calles`.

## Traza del ejemplo 1, consulta 1 → 5
```text
Dijkstra con (distancia, calles):   1→2→3→5 = (27, 3)      1→4→5 = (30, 2)
  mejor (distancia, calles) hasta 5 = (27, 3)               ← gana la distancia
Anchura:  menos calles de 1 a 5 = 2   (1→4→5)
3 calles ≠ 2 calles  →  27 NO
```
Consulta 6 → 5: `6→7→5` mide 19 con 2 calles y `6→4→5` mide 20 con 2; menos calles posibles = 2 ⇒ **19 SI**.

## Por qué así
- **La pareja conserva el orden:** al recorrer una calle se suma `(c, 1)`; sumar lo mismo a dos parejas no cambia cuál es menor en orden lexicográfico, así que Dijkstra sigue siendo correcto.
- **Entre caminos de igual distancia** ganan los de menos calles; así `pasos[v]` es el *mínimo* número de calles *de entre los caminos más cortos*, que es lo que se compara.
- **Parar en cuanto el destino llega a la cabeza de la cola:** `while (!pq.empty() && pq.top().elem != destino)`. Las calles miden ≥ 1, así que todo lo que salga después tiene distancia estrictamente mayor y no puede mejorar el `(distancia, calles)` del destino: ya es definitivo. Así no se explora el resto del grafo.
- **Doble sentido:** dos aristas dirigidas por calle; las calles repetidas no molestan.
- **Hasta 10 consultas con orígenes distintos:** se repiten los dos recorridos por consulta (el grafo se construye una vez por caso).
- **Coste:** O(K · C log N) por caso.

## Ojo con
- **Número de casos:** la primera línea del juez de la asignatura es T, y después van los T casos (`cin >> casos; while (casos--) resuelveCaso();`, y N se lee dentro del caso). Si se lee con `while (cin >> N)` y el fichero trae algo más al final, la lectura falla a medias, `K` queda sin inicializar y el programa termina con *run-error*. En Acepta el Reto, en cambio, no hay número de casos y se lee hasta el final del fichero.
- Imprimir `---` **después de cada caso**, también si todas las consultas son `SIN CAMINO`.
- `SIN CAMINO` va solo, sin distancia.
- Intersecciones desde 1: restar 1 al leer.
