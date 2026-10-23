#include <iostream>
#include <vector>
#include <limits>
#include <cstdlib>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

using namespace std;

/*
    La conferencia de paz

    N aldeas (3 <= N <= 100.000) unidas por caminos de doble sentido con longitud 1..1.000
    (el grafo es conexo). Unas son de los galos, otras de los romanos y el resto neutrales.
    Hay que elegir una aldea NEUTRAL cuya distancia a la aldea gala mas cercana y cuya
    distancia a la romana mas cercana se diferencien lo MENOS posible. Si hay empate, la de
    indice menor. Salida: indice de la aldea y esa diferencia.
*/

/*
    PLANTEAMIENTO
    Dos Dijkstra con VARIAS ORIGENES a la vez (se meten todos con distancia 0):

        dGalos[v]    = distancia de v a la aldea gala mas cercana
        dRomanos[v]  = distancia de v a la aldea romana mas cercana

    Es lo mismo que anadir un vertice falso unido con coste 0 a todas las aldeas del bando
    y hacer Dijkstra desde el, pero sin construirlo.
    Despues se recorren las aldeas neutrales en orden creciente y nos quedamos con la de
    menor |dGalos - dRomanos| (con "<" estricto gana la primera, que es la de indice menor).

    - Todos pueden pasar por cualquier aldea (aunque sea de un bando): el camino mas corto
      puede atravesar aldeas galas, romanas o neutrales.
    - Camino de doble sentido: dos aristas dirigidas.

    Coste: O(C log N) por caso (dos Dijkstra).
*/

vector<int> distanciaMinima(DigrafoValorado<int> const& g, vector<int> const& origenes) {
    const int INF = numeric_limits<int>::max();
    vector<int> dist(g.V(), INF);
    IndexPQ<int> pq(g.V());
    for (int o : origenes) {
        dist[o] = 0;
        pq.update(o, 0);
    }
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
        int u, v, d;
        cin >> u >> v >> d;
        --u; --v;
        g.ponArista({u, v, d});
        g.ponArista({v, u, d});
    }

    vector<int> bando(N, 0);                  // 0 neutral, 1 galos, 2 romanos
    vector<int> galos, romanos;
    int n;
    cin >> n;
    while (n--) { int a; cin >> a; --a; galos.push_back(a); bando[a] = 1; }
    cin >> n;
    while (n--) { int a; cin >> a; --a; romanos.push_back(a); bando[a] = 2; }

    vector<int> dGalos = distanciaMinima(g, galos);
    vector<int> dRomanos = distanciaMinima(g, romanos);

    int mejor = -1, difMejor = numeric_limits<int>::max();
    for (int v = 0; v < N; ++v) {
        if (bando[v] != 0) continue;          // solo aldeas neutrales
        int dif = abs(dGalos[v] - dRomanos[v]);
        if (dif < difMejor) { difMejor = dif; mejor = v; }
    }
    cout << mejor + 1 << ' ' << difMejor << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
