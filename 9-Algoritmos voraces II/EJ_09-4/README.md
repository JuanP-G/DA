# EJ 09-4 · El telesilla

📄 Enunciado: en el juez de la asignatura (`Ej09-4`) · 💻 [Solución](EJ_09-4.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Sillas de dos plazas que soportan un peso máximo P y N usuarios (1 ≤ N ≤ 500.000) con pesos entre 1 y P. Hay que escribir el **mínimo número de viajes** (sillas) para subir a todos.

## Cómo se plantea
Voraz emparejando **extremos** del vector ordenado. Se mira el más pesado (`j`) que queda:
- si cabe con el más ligero (`i`), suben juntos;
- si no, el más pesado no cabe con nadie y sube solo.

En los dos casos se gasta un viaje.

```text
ordenar; i = 0, j = N − 1
mientras i <= j:
    si i < j y peso[i] + peso[j] <= P:  i++     // el más ligero sube con él
    j--, viajes++
```

## Traza del ejemplo 2 (P = 30)
```text
8 10 12 16 20
20 + 8  = 28 ✓  (1 viaje)
16 + 10 = 26 ✓  (2 viajes)
12 solo         (3 viajes)
```

## Por qué así
- **Intercambio:** si en una solución óptima el más pesado no va con el más ligero, cambiar su pareja por el más ligero sigue cabiendo y no añade viajes.
- Es el mismo esquema que [09-3](../EJ_09-3/README.md) pero al revés: allí se busca **llegar** a un mínimo, aquí **no pasar** de un máximo.
- **Coste:** O(N log N) por caso.

## Ojo con
- `long long`: dos pesos de hasta 10⁹ suman más de lo que cabe en `int`.
- La condición `i < j` evita emparejar a alguien consigo mismo cuando solo queda uno.
