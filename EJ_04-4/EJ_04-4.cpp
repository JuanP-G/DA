#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <unordered_map>
#include "Grafo.h"

using namespace std;

/*
    Los numeros de Bacon

    Peliculas         --> 1 <= P <= 5.000
    Actores distintos --> como mucho 100.000
    Consultas         --> 1 <= N <= 100.000 (siempre actores que existen)
    Los nombres son una sola palabra --> se leen con cin >> string
*/

/*
    PLANTEAMIENTO
    El numero de Bacon de un actor es la longitud del camino MAS CORTO
    hasta KevinBacon, donde cada paso es "han salido en la misma pelicula".
    Camino mas corto sin pesos --> BFS desde KevinBacon (una sola vez,
    y luego cada consulta es mirar dist[actor]).

    1) Los actores vienen por nombre --> unordered_map nombre -> numero
       de vertice, para poder usar Grafo (que trabaja con 0..V-1).

    2) Como construir el grafo. Lo directo seria unir con una arista cada
       par de actores de la misma pelicula, pero una pelicula con k actores
       daria k*(k-1)/2 aristas (con 100.000 actores, imposible).
       Truco: meter tambien las PELICULAS como vertices:
            actor --- pelicula --- actor
       Asi una pelicula de k actores son solo k aristas. Pero ahora pasar
       de un actor a otro cuesta 2 aristas (actor-peli-actor), asi que
            numero de Bacon = dist / 2

    3) Grafo necesita saber V al crearlo, y no sabemos cuantos actores hay
       hasta leer todas las peliculas: primero guardo los repartos y
       despues construyo el grafo con V = actores + peliculas.
       Vertices: 0..actores-1 son actores, actores+p es la pelicula p.

    4) Si KevinBacon no sale en ninguna pelicula, todos son INF.

    Coste: O(V + A) para el BFS, con V <= 105.000 y A = suma de repartos.
*/

const string BACON = "KevinBacon";

class CaminosBFS {
public:
    CaminosBFS(Grafo const& g, int origen) : dist(g.V(), -1) {
        bfs(g, origen);
    }

    bool hayCamino(int v) const { return dist[v] != -1; }
    int distancia(int v) const { return dist[v]; }

private:
    vector<int> dist;   // dist[v] = aristas desde el origen (-1 = inalcanzable)

    void bfs(Grafo const& g, int origen) {
        queue<int> q;
        dist[origen] = 0;
        q.push(origen);
        while (!q.empty()) {
            int v = q.front(); q.pop();
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
    int peliculas; cin >> peliculas;

    unordered_map<string, int> id;           // nombre del actor -> vertice
    vector<vector<int>> reparto(peliculas);  // reparto[p] = actores de la pelicula p

    for (int p = 0; p < peliculas; ++p) {
        string titulo; int k;
        cin >> titulo >> k;   // el titulo no se usa para nada
        for (int i = 0; i < k; ++i) {
            string actor; cin >> actor;
            auto it = id.find(actor);
            if (it == id.end()) {   // actor nuevo: le doy el siguiente numero
                int nuevo = id.size();
                id[actor] = nuevo;
                reparto[p].push_back(nuevo);
            }
            else reparto[p].push_back(it->second);
        }
    }

    // ya sabemos cuantos actores hay --> construimos el grafo actor-pelicula
    int actores = id.size();
    Grafo g(actores + peliculas);
    for (int p = 0; p < peliculas; ++p)
        for (int a : reparto[p])
            g.ponArista(a, actores + p);

    // un unico BFS desde Kevin Bacon (si esta en la base de datos)
    auto itBacon = id.find(BACON);
    bool hayBacon = (itBacon != id.end());
    CaminosBFS caminos(g, hayBacon ? itBacon->second : 0);   // si no esta, el BFS da igual

    int consultas; cin >> consultas;
    for (int i = 0; i < consultas; ++i) {
        string actor; cin >> actor;
        int v = id[actor];
        cout << actor << ' ';
        if (hayBacon && caminos.hayCamino(v)) cout << caminos.distancia(v) / 2 << '\n';
        else cout << "INF\n";
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