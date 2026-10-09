#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include "Digrafo.h"

using namespace std;

/*
    Juego de Transformacion Modular

    Modulo        --> 1 <= M <= 10.000
    Inicio/Objetivo --> 0 <= S, T < M
    Operaciones   --> 1 <= N <= 100, cada una x --> (a*x + b) mod M, 0 <= a, b < 10.000
    Casos de prueba --> como mucho 500
*/

/*
    PLANTEAMIENTO
    Grafo DIRIGIDO (clase Digrafo):
        vertices: los numeros 0..M-1 (el valor actual de x)
        aristas:  x --> (a_i * x + b_i) mod M, una por cada operacion i
    Minimo numero de jugadas = camino mas corto (en aristas) de S a T
    --> BFS desde S. Si T no se alcanza, -1.

    Construir el grafo: para cada x y cada operacion, ponArista(x, (a*x+b) % M).
    Son como mucho M*N = 1.000.000 de aristas por caso (unos 4 MB).

    * La direccion importa: x --> y no implica y --> x (no se puede "deshacer"
      una operacion), por eso Digrafo y no Grafo.
    * a*x + b cabe en un int: como mucho 9.999 * 9.999 + 9.999 < 10^8.
    * Si S == T la respuesta es 0 (el BFS lo da solo: dist[S] = 0).
      Tambien con M = 1: el unico numero es el 0.
    * Se corta el BFS en cuanto se saca T, y las operaciones repetidas
      (mismo a y mismo b modulo M) se quitan antes: no aportan aristas nuevas.

    Coste: construir el grafo O(M * N) y BFS O(M + A) = O(M * N) por caso.
*/

class TransformacionModular {
public:
    TransformacionModular(Digrafo const& g, int s, int t) : dist(g.V(), -1) {
        bfs(g, s, t);
    }

    // minimo de jugadas para llegar a t desde el inicio (-1 si no se puede)
    int jugadas(int t) const { return dist[t]; }

private:
    vector<int> dist;   // dist[x] = jugadas minimas desde S hasta x (-1 = no alcanzable)

    void bfs(Digrafo const& g, int s, int t) {
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int x = q.front(); q.pop();
            if (x == t) return;               // t ya tiene su distancia minima
            for (int y : g.ady(x)) {
                if (dist[y] == -1) {
                    dist[y] = dist[x] + 1;
                    q.push(y);
                }
            }
        }
    }
};

void resuelveCaso() {
    int m, s, t, n;
    cin >> m >> s >> t >> n;
    vector<pair<int, int>> ops(n);
    for (auto& op : ops) {
        cin >> op.first >> op.second;
        op.first %= m;                    // lo que cuenta es a y b modulo M
        op.second %= m;
    }
    sort(ops.begin(), ops.end());
    ops.erase(unique(ops.begin(), ops.end()), ops.end());   // quita operaciones repetidas

    Digrafo g(m);
    for (int x = 0; x < m; ++x)
        for (auto const& op : ops)
            g.ponArista(x, (op.first * x + op.second) % m);   // x --> resultado de la operacion

    TransformacionModular tm(g, s, t);
    cout << tm.jugadas(t) << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
