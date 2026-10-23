#include <iostream>
#include <vector>
#include <limits>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    Repartiendo paquetes

    Comarca con N casas (1 <= N <= 100.000) y C conexiones DIRIGIDAS (1 <= C <= 200.000) con
    esfuerzo 1..10.000 (puede haber varias entre el mismo par e incluso de una casa a ella
    misma). La oficina esta en la casa O y hay P paquetes con sus casas destino (una casa
    puede recibir varios). El repartidor lleva un paquete cada vez: va de la oficina al
    destino y VUELVE a la oficina. Escribir el esfuerzo minimo total, o Imposible.
*/

/*
    PLANTEAMIENTO
    El orden de reparto no importa: cada paquete cuesta lo mismo (ida + vuelta) y los
    viajes son independientes. Para el paquete que va a la casa d:

        coste = dist(O -> d)  +  dist(d -> O)

    - dist(O -> d): un Dijkstra desde O en el grafo.
    - dist(d -> O): un Dijkstra desde O en el grafo INVERSO (con todas las aristas dadas
      la vuelta), porque un camino de d a O es un camino de O a d en el inverso.
      Asi bastan DOS Dijkstra para todos los paquetes, en vez de uno por paquete.

    Se suman los costes de los P paquetes (una casa repetida se suma varias veces). Si para
    algun destino alguna de las dos distancias es infinita, el reparto es Imposible.

    Coste: O(C log N) por caso + O(P).
*/

vector<long long> dijkstra(DigrafoValorado<int> const& g, int origen) {
    const long long INF = numeric_limits<long long>::max();
    vector<long long> dist(g.V(), INF);
    IndexPQ<long long> pq(g.V());
    dist[origen] = 0;
    pq.push(origen, 0);
    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        for (auto a : g.ady(v)) {
            int w = a.hasta();
            if (dist[w] > dist[v] + a.valor()) {
                dist[w] = dist[v] + a.valor();
                pq.update(w, dist[w]);
            }
        }
    }
    return dist;
}

void resuelveCaso() {
    int N, C;
    cin >> N >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, e;
        cin >> u >> v >> e;
        g.ponArista({u - 1, v - 1, e});
    }
    int oficina, P;
    cin >> oficina >> P;
    --oficina;

    const long long INF = numeric_limits<long long>::max();
    vector<long long> ida = dijkstra(g, oficina);
    vector<long long> vuelta = dijkstra(g.inverso(), oficina);

    long long total = 0;
    bool posible = true;
    while (P--) {
        int d; cin >> d; --d;
        if (ida[d] == INF || vuelta[d] == INF) posible = false;
        else total += ida[d] + vuelta[d];
    }

    if (posible) cout << total << '\n';
    else cout << "Imposible\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
