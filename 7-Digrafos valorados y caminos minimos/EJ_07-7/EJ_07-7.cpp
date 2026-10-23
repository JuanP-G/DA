#include <iostream>
#include <vector>
#include <limits>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    Ratones en un laberinto

    Laberinto con N celdas (1 <= N <= 100.000) y P pasadizos DIRIGIDOS (0 <= P <= 200.000)
    con tiempo 1..10.000 (pueden repetirse y haber bucles). Hay un raton en cada celda
    menos en la salida S y todos van por el camino mas rapido hacia S. Cuantos ratones
    llegan a S en como mucho T segundos?
*/

/*
    PLANTEAMIENTO
    Hay que conocer, para CADA celda, el tiempo minimo hasta S. Un Dijkstra normal da las
    distancias DESDE un origen; aqui queremos las distancias HACIA un destino:

        camino de a a S en el grafo  ==  camino de S a a en el grafo INVERSO

    Asi que un solo Dijkstra desde S en el grafo inverso da dist[a] = tiempo del raton de a.
    Se cuentan las celdas a != S con dist[a] <= T (el "como mucho" incluye el igual).
    Las celdas sin camino a S se quedan en infinito y no cuentan.

    Coste: O(P log N) por caso.
*/

void resuelveCaso() {
    int N, S, T, P;
    cin >> N >> S >> T >> P;
    --S;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < P; ++i) {
        int a, b, t;
        cin >> a >> b >> t;
        g.ponArista({a - 1, b - 1, t});
    }
    DigrafoValorado<int> inv = g.inverso();   // tiempos de cada celda HASTA la salida

    const int INF = numeric_limits<int>::max();
    vector<int> dist(N, INF);
    IndexPQ<int> pq(N);
    dist[S] = 0;
    pq.push(S, 0);
    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        if (dist[v] > T) break;               // el resto ya no llega a tiempo
        for (auto a : inv.ady(v)) {
            int w = a.hasta();
            if (dist[w] > dist[v] + a.valor()) {
                dist[w] = dist[v] + a.valor();
                pq.update(w, dist[w]);
            }
        }
    }

    int ratones = 0;
    for (int v = 0; v < N; ++v)
        if (v != S && dist[v] <= T) ++ratones;
    cout << ratones << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
