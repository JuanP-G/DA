#include <iostream>
#include <vector>
#include <limits>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    Navegando sin teclado

    N paginas web (2 <= N <= 3000). Se empieza en la 1 y se quiere llegar a la N.
    Cada pagina tiene un tiempo de CARGA y cada enlace (v -> w) un tiempo de
    LOCALIZAR Y PULSAR. Minimo tiempo total contando la carga de TODAS las paginas
    visitadas (tambien la 1 y la N). Si no se puede llegar: IMPOSIBLE.
*/

/*
    PLANTEAMIENTO
    Digrafo valorado (los enlaces tienen sentido) y caminos de coste minimo: Dijkstra.
    Hay DOS tipos de coste: el de los enlaces (en las aristas) y el de carga (en los
    vertices). Truco: el tiempo de carga de una pagina se paga siempre que se LLEGA a ella,
    asi que se suma al valor de la arista que entra:

        coste de la arista v -> w  =  tiempo del enlace  +  carga[w]

    Lo unico que queda fuera es la carga de la pagina de partida, que se paga siempre:
    dist[origen] = carga[origen] (en lugar de 0).

    Dijkstra necesita valores >= 0: todos los tiempos estan entre 0 y 10.000. Perfecto.

    El mayor coste posible es 3000 paginas * (10.000 + 10.000) = 6 * 10^7: cabe en int.

    Coste: O(M log N) por caso.
*/

void resuelveCaso() {
    int N, M;
    cin >> N;
    vector<int> carga(N);
    for (int& c : carga) cin >> c;

    DigrafoValorado<int> g(N);
    cin >> M;
    for (int i = 0; i < M; ++i) {
        int v, w, t;
        cin >> v >> w >> t;
        --v; --w;                                   // paginas desde 1
        g.ponArista({v, w, t + carga[w]});          // enlace + carga de la pagina a la que llega
    }

    // Dijkstra desde la pagina 0 (la "1" del enunciado)
    const int INF = numeric_limits<int>::max();
    vector<int> dist(N, INF);
    IndexPQ<int> pq(N);
    dist[0] = carga[0];                             // la primera pagina tambien se carga
    pq.push(0, dist[0]);
    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        if (v == N - 1) break;                      // ya es definitiva la distancia al destino
        for (auto a : g.ady(v)) {
            int w = a.hasta();
            if (dist[w] > dist[v] + a.valor()) {    // relajacion
                dist[w] = dist[v] + a.valor();
                pq.update(w, dist[w]);
            }
        }
    }

    if (dist[N - 1] == INF) cout << "IMPOSIBLE\n";
    else cout << dist[N - 1] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
