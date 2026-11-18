# EJ 09-2 · El alienígena infiltrado

📄 Enunciado: en el juez de la asignatura (`Ej09-2`) · 💻 [Solución](EJ_09-2.cpp)

## Qué piden
Un intervalo `[C, F)` y N trabajos (0 ≤ N ≤ 200.000), cada uno con su intervalo `[c, f)`. Hay que escribir el **mínimo número de trabajos** que cubren todo `[C, F)` (en cada instante al menos uno en marcha), o `Imposible`.

## Cómo se plantea
Voraz para **cubrir un intervalo**: se ordenan los trabajos por comienzo y `cubierto` dice hasta dónde llega lo ya cubierto (al principio `C`). Mientras `cubierto < F`:
- entre los trabajos que empiezan como muy tarde en `cubierto` (así no dejan hueco), se elige el que **acaba más tarde**;
- si ninguno pasa de `cubierto`, hay un hueco: `Imposible`;
- si no, `cubierto` pasa a ese final y se cuenta un trabajo más.

```text
cubierto = C, i = 0
mientras cubierto < F:
    masLejos = cubierto
    mientras i < N y c[i] <= cubierto:  masLejos = max(masLejos, f[i]),  i++
    si masLejos == cubierto: Imposible
    cubierto = masLejos,  usados++
```

## Traza del ejemplo 1 (`[1, 10)`)
```text
ordenados: [0,5) [2,8) [5,10) [7,11)
cubierto = 1:  empiezan ≤ 1: [0,5)          → cubierto = 5  (1 trabajo)
cubierto = 5:  empiezan ≤ 5: [2,8) [5,10)   → cubierto = 10 (2 trabajos)   fin
```
En el ejemplo 2 nadie cubre el instante 1 (`[0,1)` acaba y `[2,3)` empieza en el 2): `Imposible`.

## Por qué así
- **Elegir el que llega más lejos:** cualquier solución necesita un trabajo que cubra el instante `cubierto`. Ese trabajo empieza como muy tarde ahí, así que el elegido llega al menos igual de lejos.
- **El índice `i` nunca retrocede:** los trabajos ya mirados empiezan antes que `cubierto`, que solo crece. Coste O(N log N) por la ordenación.

## Ojo con
- Los intervalos son **semiabiertos**: `[0,5)` y `[5,10)` no dejan hueco entre ellos.
- Con N = 0 la respuesta es `Imposible` (C < F siempre).
