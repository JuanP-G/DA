#include <iostream>
#include <vector>
#include <queue>
#include "Grafo.h"

using namespace std;

/*
    Un nodo muy muy lejano

    Nodos      --> 1 <= N <= 10.000   (numerados de 1 a N)
    Conexiones --> 0 <= C <= 50.000   (sin repetidas ni lazos)
    Consultas  --> 1 <= K <= 10
    TTL        --> 0 <= TTL <= 20.000
    Entrada: N C y las C aristas --> Grafo(cin, 1) (vertices 0..N-1)
*/

/*
    PLANTEAMIENTO
    Cada vez que el mensaje salta de un nodo a un vecino gasta 1 de TTL.
    Por tanto, un nodo w recibe el mensaje si y solo si se puede llegar
    a el desde el origen con COMO MUCHO TTL saltos:
        alcanzable(w)  <=>  distancia(origen, w) <= TTL
    (en el ejemplo, desde 6 con TTL 2 llegan los que estan a 1 o 2 aristas)

    Distancia en numero de aristas en un grafo sin pesos --> BFS
    (recorrido en ANCHURA): visita los vertices por orden de distancia,
    asi que la primera vez que llega a un vertice lo hace por el camino
    mas corto. Un dfs NO sirve: puede llegar primero por un camino largo.

    Ademas el BFS se puede cortar: un vertice a distancia TTL ya no reenvia.
    Respuesta = N - (vertices alcanzados).

    Coste: O(N + C) por consulta, como mucho 10 consultas por red.
*/

class NodosAlcanzables {
public:
    NodosAlcanzables(Grafo const& g, int origen, int ttl) : dist(g.V(), -1), alcanzados(0) {
        bfs(g, origen, ttl);
    }

    int inalcanzables() const { return (int)dist.size() - alcanzados; }

private:
    vector<int> dist;   // dist[v] = saltos desde el origen (-1 = no alcanzado)
    int alcanzados;     // vertices a distancia <= ttl (incluido el origen)

    void bfs(Grafo const& g, int origen, int ttl) {
        queue<int> q;
        dist[origen] = 0;
        ++alcanzados;
        q.push(origen);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            // aqui el TTL llega a 0: no se reenvia
            if (dist[v] != ttl) {   
                for (int w : g.ady(v)) {
                    if (dist[w] == -1) {        // primera vez que llegamos --> camino mas corto
                        dist[w] = dist[v] + 1;
                        ++alcanzados;
                        q.push(w);
                    }
                }
            }
        }
    }
};

void resuelveCaso() {
    Grafo g(cin, 1);   // lee N, C y las C conexiones (de 1 a N)

    int consultas; cin >> consultas;
    for (int i = 0; i < consultas; ++i) {
        int origen, ttl;
        cin >> origen >> ttl;
        NodosAlcanzables na(g, origen - 1, ttl);   // -1: el grafo empieza en 0
        cout << na.inalcanzables() << '\n';
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