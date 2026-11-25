# EJ 11-4 · Seis grados de separación

📄 [Enunciado](../Enunciados/prob-Seis%20grados%20de%20separaci%C3%B3n.pdf) · 💻 [Solución](EJ_11-4.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una red de `P` personas (hasta 500) con `R` relaciones directas (hasta 10.000) dadas por **nombres**. El **grado de separación** de dos personas es el mínimo de relaciones que las unen; el de la red, el **máximo** de todos los pares. Si algún par no está conectado se escribe `DESCONECTADA`.

## Recurrencia (formato de examen) · Floyd-Warshall

Personas $1..P$. Para $0 \le k \le P$:

$$
\text{dist}(k, i, j) = \text{mínimo de relaciones entre } i \text{ y } j \text{ pasando como intermedias solo por las personas } 1..k
$$

**Casos base**

$$
\text{dist}(0, i, j) =
\begin{cases}
0 & \text{si } i = j \\
1 & \text{si } i \text{ y } j \text{ se conocen} \\
\infty & \text{en otro caso}
\end{cases}
$$

**Recurrencia** ($1 \le k \le P$)

$$
\text{dist}(k, i, j) = \min\big(\text{dist}(k-1, i, j),\ \text{dist}(k-1, i, k) + \text{dist}(k-1, k, j)\big)
$$

**Llamada inicial / respuesta:** se calcula $\text{dist}(P, \cdot, \cdot)$ y

$$
\text{grado} = \max_{i, j} \text{dist}(P, i, j) \qquad \text{(si algún valor es } \infty \text{: DESCONECTADA)}
$$

**Implementación:** una **sola matriz** que se va mejorando con $k = 1, \dots, P$ (el paso $k$ no cambia ni la fila ni la columna $k$, así que se puede hacer «en el sitio»). Coste $O(P^3)$ en tiempo y $O(P^2)$ en espacio.

## Cómo se plantea
1. Los nombres se pasan a números `0..P−1` con un `unordered_map`, en el orden en que aparecen.
2. La matriz empieza con 0 en la diagonal, 1 donde hay relación y «infinito» en el resto.
3. Para cada intermedio `k`, para cada par `(i, j)`: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
4. La respuesta es el mayor valor de la matriz; si hay un infinito, `DESCONECTADA`.

```text
para k en 0..P−1:
    para i en 0..P−1:
        si dist[i][k] es infinito: seguir
        para j en 0..P−1:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

## Traza del ejemplo 1
```text
Marta–Mario, Mario–Roberto, Roberto–Raquel, Mario–Raquel
Marta→Roberto: Marta–Mario–Roberto = 2      Marta→Raquel = 2      el resto = 1
el máximo es 2 → grado de separación 2
```

## Por qué así
- **Distancias entre todos los pares** de un grafo no valorado: se puede hacer con un BFS desde cada vértice (`O(P·(P+R))`) o con Floyd-Warshall. Aquí se usa Floyd por ser el algoritmo de programación dinámica del tema: el subproblema es «menor camino pasando solo por los `k` primeros».
- **Con `P = 500`** son `1,25·10⁸` operaciones simples por caso, que cabe sobradamente en tiempo.

## Ojo con
- **Personas sin ninguna relación:** no aparecen en la lista de relaciones, pero cuentan en `P`. La matriz es de `P × P`, así que quien no aparece se queda con distancia infinita a todos y la red sale desconectada (ejemplo 3: cinco personas, solo cuatro nombres).
- Una red de **una sola persona** no tiene pares: su grado es 0.
- Una relación puede repetirse o aparecer en los dos órdenes; no importa, la arista es la misma.
