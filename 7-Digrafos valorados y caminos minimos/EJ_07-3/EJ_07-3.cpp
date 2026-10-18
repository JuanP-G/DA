#include <iostream>
#include <vector>
#include <deque>
#include <limits>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    RapidEats con ruta

    Ciudad con N puntos (2 <= N <= 20.000) y C tramos de calle (0 <= C <= 100.000), cada
    uno con una duracion 1..500. Los tramos se recorren en ambos sentidos y puede haber
    varios entre los mismos dos puntos. Para cada uno de K pedidos (K <= 10), de un origen
    a un destino, escribir el tiempo minimo y el camino:

        30: 1 -> 3                (o NO LLEGA si no hay camino)

    Despues de cada caso, una linea con ---.
*/

/*
    PLANTEAMIENTO
    Caminos de coste minimo con Dijkstra, pero ahora tambien hay que decir POR DONDE se va.
    Para eso sirve ulti[w] (la ultima arista del camino mas corto hasta w, que se actualiza
    en cada relajacion): se recorre hacia atras desde el destino hasta el origen.

        ulti[destino] = (a -> destino);  ulti[a] = (b -> a);  ... hasta llegar al origen

    y se escribe al reves (se van metiendo los vertices por delante en un deque).

    - Tramos de doble sentido: dos aristas dirigidas por cada tramo (los tramos repetidos
      no molestan: Dijkstra se queda con el mas rapido).
    - Hay hasta 10 pedidos con origenes distintos, asi que se ejecuta Dijkstra UNA VEZ POR
      PEDIDO (el grafo se construye una sola vez por caso).
    - Si hay varios caminos con el mismo tiempo vale cualquiera.

    Coste: O(K * C log N) por caso.
*/

void resuelveCaso() {
    int N, C;
    cin >> N >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, t;
        cin >> u >> v >> t;
        --u; --v;
        g.ponArista({u, v, t});
        g.ponArista({v, u, t});
    }

    const int INF = numeric_limits<int>::max();
    int K; cin >> K;
    while (K--) {
        int origen, destino;
        cin >> origen >> destino;
        --origen; --destino;

        // Dijkstra desde el origen del pedido
        vector<int> dist(N, INF);
        vector<int> ulti(N, -1);          // vertice anterior en el camino minimo
        IndexPQ<int> pq(N);
        dist[origen] = 0;
        pq.push(origen, 0);
        while (!pq.empty()) {
            int v = pq.top().elem; pq.pop();
            if (v == destino) break;      // la distancia al destino ya es definitiva
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                if (dist[w] > dist[v] + a.valor()) {
                    dist[w] = dist[v] + a.valor();
                    ulti[w] = v;
                    pq.update(w, dist[w]);
                }
            }
        }

        if (dist[destino] == INF) {
            cout << "NO LLEGA\n";
        } else {
            deque<int> camino;            // se reconstruye hacia atras desde el destino
            for (int v = destino; v != origen; v = ulti[v]) camino.push_front(v);
            camino.push_front(origen);

            cout << dist[destino] << ":";
            for (size_t i = 0; i < camino.size(); ++i)
                cout << (i == 0 ? " " : " -> ") << camino[i] + 1;
            cout << '\n';
        }
    }
    cout << "---\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
