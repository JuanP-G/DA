#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <utility>
#include <functional>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    Cual es el mejor camino?

    Ciudad con N intersecciones (2 <= N <= 20.000) y C calles (0 <= C <= 100.000) de
    longitud 1..5.000, de doble sentido. Para cada una de K <= 10 consultas (origen y
    destino distintos) escribir la distancia minima y SI si algun camino de esa distancia
    usa ademas el MENOR NUMERO DE CALLES posible entre los dos puntos (NO si no), o
    SIN CAMINO. Tras cada caso, una linea con ---. La entrada termina al acabarse el fichero.
*/

/*
    PLANTEAMIENTO
    Dos cosas distintas desde el origen:

      1. Menor numero de calles posible (sin mirar la longitud): un recorrido en anchura.
            calles[v] = menor numero de calles de origen a v
      2. Distancia minima, y entre los caminos de esa distancia, el de MENOS calles:
         Dijkstra donde la prioridad es una pareja (distancia, calles) comparada en ese orden.
            dist[v]   = distancia minima
            pasos[v]  = menos calles entre los caminos de distancia dist[v]

    Respuesta de la consulta: distancia dist[destino] y SI si pasos[destino] == calles[destino]
    (el mejor camino en distancia tambien es de los de menos calles), NO si pasos > calles.

    - Con la pareja, al sumar una calle (c, 1) el orden lexicografico se conserva, asi que
      Dijkstra sigue siendo correcto.
    - Doble sentido: dos aristas dirigidas por calle.
    - Hasta 10 consultas con origenes distintos: se repiten los dos recorridos por consulta.

    Coste: O(K * C log N) por caso.
*/

using Par = pair<int, int>;                   // (distancia, calles)

void resuelveCaso(int N) {
    int C;
    cin >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, d;
        cin >> u >> v >> d;
        --u; --v;
        g.ponArista({u, v, d});
        g.ponArista({v, u, d});
    }

    const int INF = numeric_limits<int>::max();
    int K; cin >> K;
    while (K--) {
        int origen, destino;
        cin >> origen >> destino;
        --origen; --destino;

        // Dijkstra con prioridad (distancia, calles)
        vector<Par> mejor(N, {INF, INF});
        IndexPQ<Par> pq(N);
        mejor[origen] = {0, 0};
        pq.push(origen, mejor[origen]);
        while (!pq.empty()) {
            int v = pq.top().elem; pq.pop();
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                Par nuevo = {mejor[v].first + a.valor(), mejor[v].second + 1};
                if (nuevo < mejor[w]) {
                    mejor[w] = nuevo;
                    pq.update(w, nuevo);
                }
            }
        }

        if (mejor[destino].first == INF) {
            cout << "SIN CAMINO\n";
            continue;
        }

        // Anchura: menor numero de calles posible, sin mirar la longitud
        vector<int> calles(N, -1);
        queue<int> cola;
        calles[origen] = 0;
        cola.push(origen);
        while (!cola.empty() && calles[destino] == -1) {
            int v = cola.front(); cola.pop();
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                if (calles[w] == -1) { calles[w] = calles[v] + 1; cola.push(w); }
            }
        }

        cout << mejor[destino].first << (mejor[destino].second == calles[destino] ? " SI\n" : " NO\n");
    }
    cout << "---\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    while (cin >> N) resuelveCaso(N);         // la entrada acaba con el fichero

    return 0;
}
