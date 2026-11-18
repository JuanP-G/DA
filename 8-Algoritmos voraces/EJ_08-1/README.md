# EJ 08-1 · Agujeros en la manguera

📄 Enunciado: en el juez de la asignatura (`Ej08-1`) · 💻 [Solución](EJ_08-1.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una manguera con N agujeros (1 ≤ N ≤ 100.000) en posiciones 1..10⁹, dadas **en orden no decreciente** (puede haber varios en la misma posición), y parches de longitud L. Un parche tapa todos los agujeros que estén a distancia ≤ L entre sí, y los parches se pueden solapar. Hay que escribir el **mínimo número de parches**.

## Cómo se plantea
Voraz: el agujero más a la izquierda que siga sin tapar tiene que quedar en algún parche, y lo mejor es **empezar el parche justo en él**, porque así llega lo más lejos posible, hasta `p + L`.

```text
fin = -1, parches = 0
para cada agujero p (ya vienen ordenados):
    si p > fin:  parches++,  fin = p + L      // agujero sin tapar: parche nuevo desde él
```

**Por qué es óptimo:** cualquier solución tiene un parche que cubre el primer agujero `p`, y ese parche no pasa de `p + L`. El nuestro empieza en `p`, así que tapa todo lo que tapa el suyo a la derecha de `p`, y a la izquierda no queda nada por tapar. Se puede cambiar su parche por el nuestro sin empeorar, y repetir el argumento con el resto.

## Traza del ejemplo 3 (L = 10)
```text
agujeros: 3 8 8 9 20 45 55 90
3  > -1  → parche [3, 13]     tapa 3, 8, 8, 9
20 > 13  → parche [20, 30]
45 > 30  → parche [45, 55]    tapa 45 y 55 (justo en el borde)
90 > 55  → parche [90, 100]                       total = 4
```

## Por qué así
- **Ya vienen ordenados:** no hace falta ordenar, el recorrido es O(N).
- **`p > fin` estricto:** un agujero justo en `p + L` está tapado (el 55 del ejemplo).
- **`long long` en `fin`:** `p + L` puede pasar un poco de 10⁹ (cabría en `int`, pero así no hay dudas).

## Ojo con
- Agujeros repetidos en la misma posición: los tapa el mismo parche, no cuentan dos veces.
- La suma de N de todos los casos llega a 1.000.000: con el `cin` de la plantilla tarda unas décimas, suficiente.
