# EJ 05-4 · Sumidero en un grafo dirigido

📄 [Enunciado](<../Enunciados/prob-Sumidero en un grafo dirigido.pdf>) · 💻 [Solución](EJ_05-4.cpp)

## Qué piden
Si el digrafo tiene un **sumidero** (grado de salida 0 y grado de entrada V − 1) y cuál es.

## Cómo se plantea
Con el `Digrafo` (se lee directamente con el constructor `Digrafo(cin)`, que ya trae V, A y las aristas desde 0):

| | cómo se calcula | coste |
|---|---|:--:|
| grado de salida de `v` | `g.ady(v).size()` | O(1) |
| grado de entrada de `v` | contar cuántas veces sale `v` en todas las listas | O(V + A) en total |

Se busca el vértice con salida 0 y entrada V − 1.

## Por qué así
- **Como mucho hay un sumidero:** si `s` y `t` lo fueran, existiría `t → s` y `t` no tendría salida 0.
- Como no hay lazos ni aristas repetidas, entrada V − 1 significa que **todos** los demás apuntan a `s`.
- **V = 1:** el único vértice tiene salida 0 y entrada 0 = V − 1 ⇒ `SI 0`.
- El digrafo no da el grado de entrada: hace falta recorrer las listas (o mirar `g.inverso().ady(v).size()`, que cuesta lo mismo).
- Curiosidad: con **matriz de adyacencia** hay un truco en O(V) (descartar un candidato por cada consulta); con listas no compensa, porque leer las aristas ya cuesta O(A).

## Traza del ejemplo 1
```text
aristas: 1→0  0→2  3→2  1→2
vértice:     0  1  2  3
salida:      1  2  0  1
entrada:     1  0  3  0      V − 1 = 3
sumidero: 2 (salida 0, entrada 3)   ⇒  SI 2
```
Ejemplo 2: el único vértice con salida 0 es el 3, con entrada 2 ≠ 3 ⇒ `NO`.

## Coste
**O(V + A)** por caso.
