#include <iostream>
#include <vector>
#include <queue>
#include "Digrafo.h"

using namespace std;

/*
    Haciendo trampas en Serpientes y Escaleras

    Tablero  --> N x N casillas (2 <= N <= 100), numeradas de 1 a N*N
    Dado     --> caras de 1 a K (K <= N), y podemos ELEGIR la cara
    S serpientes y E escaleras: "origen destino"
    Salida: minimo numero de tiradas para llegar de la casilla 1 a la N*N
*/

/*
    PLANTEAMIENTO
    Grafo DIRIGIDO: un vertice por casilla (casilla c --> vertice c - 1).
    Desde la casilla v, una tirada d (1..K) lleva a v + d, y si ahi empieza
    una serpiente o una escalera, la ficha acaba en su otro extremo:

        v --> destino(v + d)      para d = 1..K,  v + d <= N*N

    destino[c] = c, salvo en el origen de una serpiente o escalera.
    Cada arista es UNA tirada, asi que el minimo de tiradas es el camino
    mas corto (en aristas) de 0 a N*N - 1 --> BFS.

    * Da igual que la numeracion del tablero vaya en zigzag: solo importa
      el numero de cada casilla.
    * Las serpientes y las escaleras se tratan igual (un salto obligatorio).
    * El enunciado garantiza que la ultima casilla es alcanzable.
    * BFS parando al sacar la ultima casilla.

    Coste: O(N^2 * K) por caso (N^2 vertices, K aristas cada uno).
*/

class Tiradas {
public:
    Tiradas(Digrafo const& g, int s) : dist(g.V(), -1) {
        bfs(g, s);
    }
    int distancia(int v) const { return dist[v]; }

private:
    vector<int> dist;   // dist[v] = minimo de tiradas de s a v (-1 si no se llega)

    void bfs(Digrafo const& g, int s) {
        int fin = g.V() - 1;
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            if (v == fin) return;          // ya tenemos su distancia minima
            for (int w : g.ady(v)) {
                if (dist[w] == -1) {
                    dist[w] = dist[v] + 1;
                    q.push(w);
                }
            }
        }
    }
};

void resuelveCaso() {
    int n, k, s, e;
    cin >> n >> k >> s >> e;
    int casillas = n * n;

    vector<int> destino(casillas);
    for (int c = 0; c < casillas; ++c) destino[c] = c;
    for (int i = 0; i < s + e; ++i) {      // serpientes y escaleras: igual
        int a, b; cin >> a >> b;
        destino[a - 1] = b - 1;
    }

    Digrafo g(casillas);
    for (int v = 0; v < casillas; ++v)
        for (int d = 1; d <= k && v + d < casillas; ++d)
            g.ponArista(v, destino[v + d]);   // tirar un d desde v

    Tiradas t(g, 0);
    cout << t.distancia(casillas - 1) << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
