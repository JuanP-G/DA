# EJ 07-3 · RapidEats con ruta

📄 [Enunciado](<../Enunciados/prob-RapidEats.pdf>) · 💻 [Solución](EJ_07-3.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#813 · RapidEats](https://aceptaelreto.com/problem/statement.php?id=813) — *casi el mismo problema*. Allí solo se pide el **tiempo mínimo** de cada pedido (sin la ruta: `30` en vez de `30: 1 -> 3`) y no hay número de casos (se lee hasta el final del fichero); el resto es igual.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-813_rapideats.cpp`](<../../Acepta el Reto/ACR-813_rapideats.cpp>)
<!-- acr:fin -->

## Qué piden
Ciudad con N puntos (2 ≤ N ≤ 20.000) y C tramos de calle (cada uno con un tiempo de 1 a 500) que se recorren **en ambos sentidos**; puede haber varios tramos entre los mismos dos puntos. Para cada uno de K ≤ 10 pedidos (origen, destino) hay que escribir el tiempo mínimo y **la ruta** que lo consigue:

```text
40: 4 -> 3 -> 1       (o NO LLEGA)
```
y, tras cada caso, una línea `---`. Si hay varias rutas con el mismo tiempo, vale cualquiera.

## Cómo se plantea
**Dijkstra directo** (sin trucos) más **recuperar el camino** con el vector que guarda cómo se llegó a cada vértice. En las transparencias es `ulti[w]`, la última arista del camino mínimo hasta `w`; aquí basta guardar el vértice anterior (`ulti[w] = v` en cada relajación que mejora).

Para escribir la ruta se **retrocede** desde el destino hasta el origen:

```text
camino = []
v = destino
mientras v != origen:  camino.push_front(v);  v = ulti[v]
camino.push_front(origen)
```
Como se retrocede, los vértices se meten **por delante** (en un `deque`, o se invierte el vector al final).

## Traza del ejemplo 1, pedido 4 → 1
Tramos: 1-2 (15), 1-3 (30), 2-3 (20), 4-3 (10).
```text
sale 4 (0):   dist[3] = 10, ulti[3] = 4
sale 3 (10):  dist[1] = 40, ulti[1] = 3     dist[2] = 30, ulti[2] = 3
sale 2 (30):  1 por 2 costaría 30 + 15 = 45 > 40, no mejora
sale 1 (40):  fin
retroceder desde 1:  ulti[1] = 3,  ulti[3] = 4  →  4 -> 3 -> 1,  tiempo 40
```

## Por qué así
- **Tramos de doble sentido:** cada tramo se añade como **dos aristas dirigidas**. Los tramos repetidos no molestan: Dijkstra se queda con el más rápido.
- **Un Dijkstra por pedido:** los K ≤ 10 pedidos pueden tener orígenes distintos. El grafo se construye **una vez** por caso y se ejecuta Dijkstra K veces (si varios pedidos compartieran origen se podría reutilizar).
- **NO LLEGA:** `dist[destino]` queda en ∞.
- **Parada anticipada:** al sacar el destino de la cola su distancia ya es definitiva.
- **Coste:** O(K · C log N) por caso.

## Ojo con
- Imprimir `---` **después de cada caso**, aunque todos los pedidos sean `NO LLEGA`.
- El formato es `tiempo: a -> b -> c`: dos puntos pegados al tiempo y flechas con espacios.
- Los puntos van numerados desde 1: restar 1 al leer y sumar 1 al escribir.
