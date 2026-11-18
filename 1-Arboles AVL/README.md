# Árboles AVL (tema 1) · resumen

🎬 Vídeo: [`01-0_arboles_avl_teoria.mp4`](../Videos/01-0_arboles_avl_teoria.mp4)

## Árboles binarios de búsqueda
En cada nodo, todo lo del subárbol izquierdo es **menor** y todo lo del derecho **mayor**. Buscar, insertar y borrar bajan un nivel por comparación, así que cuestan **lo que la altura**. El recorrido en **inorden** da los elementos ordenados.

El problema es que, si se insertan en orden (1, 2, 3, 4, 5), el árbol degenera en una lista y todo cuesta `O(n)`.

## La condición AVL
En **cada nodo**, las alturas de los dos hijos difieren **como mucho en 1**. Cada nodo guarda su altura (el vacío tiene altura 0). Con eso la altura es `O(log n)`.

## Rotaciones
| Desequilibrio | Arreglo |
|---|---|
| izquierda-izquierda | rotación a la **derecha** (`rotaDer`) |
| derecha-derecha | rotación a la **izquierda** (`rotaIzq`) |
| izquierda-derecha | izquierda en el hijo y derecha en el nodo (`rotaIzqDer`) |
| derecha-izquierda | derecha en el hijo e izquierda en el nodo (`rotaDerIzq`) |

Cada rotación cambia unos pocos punteros y recalcula dos alturas: `O(1)`.

**Insertar:** se baja como en un ABB, se inserta como hoja, al volver de la recursión se recalculan alturas y se arregla el primer nodo desequilibrado. **Borrar** es parecido, pero puede necesitar rotaciones en varios niveles.

## En el curso
[`TreeSet_AVL_plantilla.h`](../Estructuras%20de%20datos/TreeSet_AVL_plantilla.h): `insert`, `contains` y `erase` en `O(log n)`; `size` y `empty` en `O(1)`.

| Ejercicio | Idea |
|---|---|
| [01-1](EJ_01-1/README.md) | comprobar si es AVL con una recursión en postorden que devuelve altura, mínimo y máximo |
| [01-2](EJ_01-2/README.md) | k-ésimo en `O(log n)` con un atributo nuevo (`tami`) que se mantiene al insertar y al rotar |
