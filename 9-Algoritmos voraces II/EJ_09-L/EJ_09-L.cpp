#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>
#include "GrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    Necesitamos agua

    Isla con N puntos (N par, 2..200.000): la desalinizadora norte es el 1, la sur es el N y los
    N - 2 restantes son pueblos. M carreteras de doble sentido con coste 1..100.000 (el grafo es
    conexo). Cada pueblo recibe un camion que sale de una planta, va al pueblo y VUELVE. La mitad
    de los pueblos se sirven desde el norte y la otra mitad desde el sur. Escribir el coste
    minimo total.
*/

/*
    PLANTEAMIENTO (Dijkstra + voraz)
    El camion de un pueblo v hace el camino minimo de ida y el de vuelta:
        coste(v) = 2 * dN[v]  si lo sirve el norte,   2 * dS[v]  si lo sirve el sur
    con dN y dS las distancias minimas desde 1 y desde N (dos Dijkstra).

    Si todos fueran al sur costaria  2 * suma(dS). Pasar el pueblo v al norte cambia el coste en
        2 * (dN[v] - dS[v])
    Hay que pasar exactamente (N - 2) / 2 pueblos al norte, asi que lo mejor es pasar los de
    MENOR diferencia dN[v] - dS[v] (los que mas ahorran yendo al norte, o los que menos pierden).
    Se ordenan las diferencias y se cogen las (N - 2) / 2 primeras.

    long long: una distancia puede llegar a 100.000 * 200.000.

    Coste: O(M log N) por caso (los Dijkstra) + O(N log N) (ordenar las diferencias).
*/

vector<long long> dijkstra(GrafoValorado<int> const& g, int origen) {
    const long long INF = numeric_limits<long long>::max();
    vector<long long> dist(g.V(), INF);
    IndexPQ<long long> pq(g.V());
    dist[origen] = 0;
    pq.push(origen, 0);
    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        for (auto a : g.ady(v)) {
            int w = a.otro(v);
            if (dist[w] > dist[v] + a.valor()) {
                dist[w] = dist[v] + a.valor();
                pq.update(w, dist[w]);
            }
        }
    }
    return dist;
}

void resuelveCaso() {
    int N, M;
    cin >> N >> M;
    GrafoValorado<int> g(N);
    for (int i = 0; i < M; ++i) {
        int u, v, c;
        cin >> u >> v >> c;
        g.ponArista({u - 1, v - 1, c});
    }

    vector<long long> dN = dijkstra(g, 0), dS = dijkstra(g, N - 1);

    long long total = 0;               // todos al sur...
    vector<long long> dif;             // ...y lo que cambia al pasar cada pueblo al norte
    for (int v = 1; v < N - 1; ++v) {
        total += dS[v];
        dif.push_back(dN[v] - dS[v]);
    }
    sort(dif.begin(), dif.end());
    for (int k = 0; k < (N - 2) / 2; ++k) total += dif[k];

    cout << 2 * total << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
