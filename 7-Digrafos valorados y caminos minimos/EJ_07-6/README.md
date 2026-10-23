# EJ 07-6 · Repartiendo paquetes

📄 [Enunciado](<../Enunciados/prob-Repartiendo paquetes.pdf>) · 💻 [Solución](EJ_07-6.cpp)

<!-- acr:inicio -->
🔗 **Para practicar lo mismo en Acepta el Reto:** [#292 · Repartiendo paquetes](https://aceptaelreto.com/problem/statement.php?id=292) — *problema relacionado*. No he podido leer la página de allí desde aquí: comprueba el formato de entrada y de salida (y los límites) antes de enviar.
<!-- acr:fin -->

## Qué piden
Comarca con N casas (1 ≤ N ≤ 100.000) y C conexiones **dirigidas** (1 ≤ C ≤ 200.000) con un esfuerzo 1..10.000 (puede haber varias entre el mismo par e incluso de una casa a ella misma). La oficina está en la casa O y hay P paquetes, cada uno con su casa destino (una casa puede recibir varios). El repartidor lleva **un paquete cada vez**: va de la oficina al destino y **vuelve** a la oficina. Se escribe el esfuerzo mínimo total, o `Imposible`.

## Cómo se plantea
El **orden de reparto no importa**: los viajes son independientes y cada paquete cuesta ida + vuelta. Para el paquete que va a la casa `d`:

```text
coste = dist(O → d)  +  dist(d → O)
```
- `dist(O → d)`: **un Dijkstra desde O** en el grafo.
- `dist(d → O)`: **un Dijkstra desde O en el grafo inverso** (con todas las aristas dadas la vuelta), porque un camino de `d` a `O` es un camino de `O` a `d` en el inverso.

Así bastan **dos** Dijkstra para los P paquetes, en vez de uno por paquete. Se suman los costes de todos los paquetes (una casa repetida se suma varias veces). Si para algún destino alguna de las dos distancias es infinita, el reparto es `Imposible`.

## Traza del ejemplo 1 (oficina en 1)
Conexiones: 1→2 (5), 2→3 (2), 3→1 (8), 1→4 (2), 4→1 (3). Paquetes a 2, 3 y 4.
```text
ida    desde 1:       d2 = 5     d3 = 5 + 2 = 7     d4 = 2
vuelta (inverso desde 1):  2→3→1 = 2 + 8 = 10    3→1 = 8    4→1 = 3
paquete a 2:  5 + 10 = 15
paquete a 3:  7 + 8  = 15
paquete a 4:  2 + 3  =  5                          total = 35
```
En el ejemplo 2 la casa 2 no tiene conexiones: `ida[2]` es infinito ⇒ `Imposible`.

## Por qué así
- **Grafo inverso en vez de P Dijkstra:** `g.inverso()` da las distancias *hacia* la oficina con una sola ejecución.
- **`long long`:** una casa muy lejana repetida muchas veces puede sumar mucho (el enunciado garantiza ≤ 10⁹, pero no cuesta nada).
- **Aristas repetidas y bucles:** no molestan en Dijkstra.
- **Una casa destino puede ser la oficina:** cuesta 0 + 0.
- **Coste:** O(C log N) por caso + O(P).

## Ojo con
- Las conexiones son **dirigidas**: aparecen dos veces si se pueden recorrer en ambos sentidos.
- La entrada de cada caso pone N y C en líneas distintas, y luego `O P` y la línea con los P destinos.
- Comprobar `Imposible` para **todos** los destinos antes de escribir nada.
