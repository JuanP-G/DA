# Acepta el Reto: versiones listas para enviar

Acepta el Reto ([aceptaelreto.com](https://aceptaelreto.com)) es un juez público: se registra uno y puede enviar su solución sin pasar por el de la asignatura. Solo admite **un fichero `.cpp`**, así que `#include "Grafo.h"` no compila allí. Los ficheros de esta carpeta son las soluciones del repo con:

1. las cabeceras propias (`Grafo.h`, `Digrafo.h`, `IndexPQ.h`) copiadas dentro, y
2. la lectura de la entrada y la salida cambiadas al formato de Acepta el Reto cuando difiere del de la asignatura.

**Cómo usarlos:** abre el que corresponda, copia **todo** su contenido y pégalo en la página de envío del problema (lenguaje C++).

> No los edites a mano: se regeneran con `python3 herramientas/para_acepta.py` (añade `--probar` para compilarlos y ejecutarlos con las pruebas de [`pruebas/`](pruebas)). Si cambias una solución, vuelve a ejecutar el script.

| Ejercicio | Problema en Acepta el Reto | Fichero | Qué cambia respecto a la asignatura |
|:--:|---|---|---|
| 01-1 | [#303 · ¿Es un árbol AVL?](https://aceptaelreto.com/problem/statement.php?id=303) | [`ACR-303_es_un_arbol_AVL.cpp`](ACR-303_es_un_arbol_AVL.cpp) | nada: el formato ya coincide |
| 02-1 | [#289 · Lo que cuesta sumar](https://aceptaelreto.com/problem/statement.php?id=289) | [`ACR-289_lo_que_cuesta_sumar.cpp`](ACR-289_lo_que_cuesta_sumar.cpp) | nada: el formato ya coincide |
| 02-2 | [#351 · Unidad Curiosa de Monitorización](https://aceptaelreto.com/problem/statement.php?id=351) | [`ACR-351_unidad_curiosa_de_monitorizacion.cpp`](ACR-351_unidad_curiosa_de_monitorizacion.cpp) | el separador de cada caso es `----` (cuatro guiones) |
| 02-3 | [#341 · Reina del súper](https://aceptaelreto.com/problem/statement.php?id=341) | [`ACR-341_reina_del_super.cpp`](ACR-341_reina_del_super.cpp) | la entrada termina al acabarse el fichero (no hay caso `0 0`) |
| 02-5 | [#311 · Ordenando a los pacientes en urgencias](https://aceptaelreto.com/problem/statement.php?id=311) | [`ACR-311_pacientes_en_urgencias.cpp`](ACR-311_pacientes_en_urgencias.cpp) | el separador de cada caso es `----` (cuatro guiones) |
| 03-1 | [#505 · Volando drones](https://aceptaelreto.com/problem/statement.php?id=505) | [`ACR-505_volando_drones.cpp`](ACR-505_volando_drones.cpp) | solo se copian las cabeceras (el formato ya coincide) |
| 03-3 | [#649 · Multitarea](https://aceptaelreto.com/problem/statement.php?id=649) | [`ACR-649_multitarea.cpp`](ACR-649_multitarea.cpp) | no hay número de casos: se lee hasta el final del fichero; los instantes llegan hasta 10^9: `long long` |
| 03-4 | [#271 · Pájaros en vuelo](https://aceptaelreto.com/problem/statement.php?id=271) | [`ACR-271_pajaros_en_vuelo.cpp`](ACR-271_pajaros_en_vuelo.cpp) | nada: el formato ya coincide |
| 04-1 | [#307 · Árboles libres](https://aceptaelreto.com/problem/statement.php?id=307) | [`ACR-307_arboles_libres.cpp`](ACR-307_arboles_libres.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 04-2 | [#352 · Los amigos de mis amigos son mis amigos](https://aceptaelreto.com/problem/statement.php?id=352) | [`ACR-352_amigos_de_mis_amigos.cpp`](ACR-352_amigos_de_mis_amigos.cpp) | solo se copian las cabeceras (el formato ya coincide) |
| 04-7 | [#279 · Grafo bipartito](https://aceptaelreto.com/problem/statement.php?id=279) | [`ACR-279_grafo_bipartito.cpp`](ACR-279_grafo_bipartito.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 05-1 | [#319 · La máquina calculadora](https://aceptaelreto.com/problem/statement.php?id=319) | [`ACR-319_maquina_calculadora.cpp`](ACR-319_maquina_calculadora.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 05-5 | [#253 · Haciendo trampas en Serpientes y Escaleras](https://aceptaelreto.com/problem/statement.php?id=253) | [`ACR-253_serpientes_y_escaleras.cpp`](ACR-253_serpientes_y_escaleras.cpp) | la entrada termina con la línea `0 0 0 0` |
| 06-1 | [#288 · Petroleros hundidos](https://aceptaelreto.com/problem/statement.php?id=288) | [`ACR-288_petroleros_hundidos.cpp`](ACR-288_petroleros_hundidos.cpp) | no hay número de casos: se lee hasta el final del fichero (el mar va como espacio en blanco: la solución solo mira dónde hay `#`); el mar va como espacios en blanco, así que cada fila se lee entera con `getline`; las filas llevan espacios: no sirve `cin >> fila`; una fila puede venir recortada |
| 06-2 | [#646 · Camiones de reparto](https://aceptaelreto.com/problem/statement.php?id=646) | [`ACR-646_camiones_de_reparto.cpp`](ACR-646_camiones_de_reparto.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 06-3 | [#645 · Recorriendo el archipiélago en bicicleta](https://aceptaelreto.com/problem/statement.php?id=645) | [`ACR-645_archipielago_en_bicicleta.cpp`](ACR-645_archipielago_en_bicicleta.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 07-1 | [#318 · Navegando sin teclado](https://aceptaelreto.com/problem/statement.php?id=318) | [`ACR-318_navegando_sin_teclado.cpp`](ACR-318_navegando_sin_teclado.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 07-2 | [#358 · Camino al cole](https://aceptaelreto.com/problem/statement.php?id=358) | [`ACR-358_camino_al_cole.cpp`](ACR-358_camino_al_cole.cpp) | no hay número de casos: se lee hasta el final del fichero |
| 07-3 | [#813 · RapidEats](https://aceptaelreto.com/problem/statement.php?id=813) | [`ACR-813_rapideats.cpp`](ACR-813_rapideats.cpp) | no hay número de casos: se lee hasta el final del fichero; allí solo se pide el tiempo mínimo de cada pedido (sin la ruta): se escribe `30` en vez de `30: 1 -> 3` |
| 07-5 | [#504 · ¿Cuál es el mejor camino?](https://aceptaelreto.com/problem/statement.php?id=504) | [`ACR-504_cual_es_el_mejor_camino.cpp`](ACR-504_cual_es_el_mejor_camino.cpp) | el separador de cada caso es `----` (cuatro guiones) |
| 07-7 | [#601 · Ratones en un laberinto](https://aceptaelreto.com/problem/statement.php?id=601) | [`ACR-601_ratones_en_un_laberinto.cpp`](ACR-601_ratones_en_un_laberinto.cpp) | no hay número de casos: se lee hasta el final del fichero |

Las versiones de `pruebas/` son los ejemplos de los enunciados (los de Acepta el Reto y los de la asignatura, en el formato de Acepta el Reto).
