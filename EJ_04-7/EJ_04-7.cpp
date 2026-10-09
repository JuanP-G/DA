#include <iostream>
#include <vector>
#include "Grafo.h"

using namespace std;

/*
    Grafo bipartito

    Vertices --> 1 <= V <= 100
    Aristas  --> A (vertices de 0 a V-1, sin lazos ni repetidas)
    Entrada: V en una linea y A en la siguiente --> justo lo que lee Grafo(cin)
*/

/*
    PLANTEAMIENTO
    Bipartito = se puede colorear con 2 colores sin que una arista
    una dos vertices del mismo color.

    Idea: el color de un vertice OBLIGA el color de sus vecinos (el contrario).
    Asi que hago un dfs coloreando: al vertice de partida le doy un color
    cualquiera y a cada vecino nuevo el color contrario al de su padre.
    Si encuentro una arista v-w con w ya visitado y del MISMO color que v,
    hay conflicto --> no es bipartito (hay un ciclo de longitud impar).

    OJO: el grafo puede no ser conexo, asi que hay que lanzar el dfs desde
    cada vertice no visitado (cada componente se colorea por separado).

    Coste: O(V + A) por caso.
*/

class Bipartito {
public:
    Bipartito(Grafo const& g) : visit(g.V(), false), color(g.V(), false), bipar(true) {
        for (int v = 0; v < g.V() && bipar; ++v) {
            if (!visit[v]) {   // nueva componente: su primer vertice puede ir de cualquier color
                color[v] = false;
                dfs(g, v);
            }
        }
    }

    bool esBipartito() const { return bipar; }

private:
    vector<bool> visit;   // visit[v] = v ya tiene color asignado
    vector<bool> color;   // los dos colores: false / true
    bool bipar;

    void dfs(Grafo const& g, int v) {
        visit[v] = true;
        for (int w : g.ady(v)) {
            if (!bipar) return;   // ya sabemos la respuesta, no seguimos
            if (!visit[w]) {
                color[w] = !color[v];   // el vecino lleva el color contrario
                dfs(g, w);
            }
            else if (color[w] == color[v]) bipar = false;   // arista entre iguales
        }
    }
};

void resuelveCaso() {
    Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)

    Bipartito b(g);
    cout << (b.esBipartito() ? "SI" : "NO") << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}