#include <iostream>
#include <vector>
#include <algorithm>
#include "Grafo.h"

using namespace std;

/*
    Los amigos de mis amigos son mis amigos

    Personas --> 1 <= N <= 20.000
    Parejas  --> 0 <= M <= 200.000
    Personas numeradas de 1 a N --> Grafo(cin, 1) les resta 1 (vertices 0..N-1)
    Una pareja puede repetirse --> no pasa nada: el dfs no visita dos veces
*/

/*
    PLANTEAMIENTO
    Modelo: cada persona es un vertice y cada amistad una arista.
    "Los amigos de mis amigos son mis amigos" significa que dos personas
    estan en el mismo grupo si hay un CAMINO entre ellas en el grafo.
    Es decir, un grupo de amigos = una COMPONENTE CONEXA.

    Lo que piden: el tamano de la componente conexa mas grande.
    Para cada vertice no visitado lanzo un dfs que devuelve cuantos
    vertices ha visitado (el tamano de esa componente) y me quedo
    con el maximo.

    Coste: O(N + M) por caso.

    Nota: el dfs recursivo puede llegar a profundidad N (hasta 20.000).
    En el juez no da problemas, pero en Visual Studio (pila de 1MB)
    un caso enorme podria desbordar la pila --> ver EJ_04-L, que usa BFS.
*/

class MaximaCompConexa {
public:
	// construye el objeto y calcula el tamano de la mayor componente conexa
    MaximaCompConexa(Grafo const& g) : visit(g.V(), false), maxim(0) {
        for (int v = 0; v < g.V(); ++v) {
            if (!visit[v]) {   // v empieza una componente nueva
                int tam = dfs(g, v);
                maxim = max(maxim, tam);
            }
        }
    }

    int maximo() const { return maxim; }

private:
    vector<bool> visit;   // visit[v] = ya contado en alguna componente
    int maxim;            // tamano de la mayor componente encontrada

    // devuelve el numero de vertices de la componente de v que aun no se habian visitado
    int dfs(Grafo const& g, int v) {
        visit[v] = true;
        int tam = 1;   // el propio v
        for (int w : g.ady(v))
            if (!visit[w]) tam += dfs(g, w);
        return tam;
    }
};

void resuelveCaso() {
    Grafo g(cin, 1);   // lee N, M y las M amistades (de 1 a N)

    MaximaCompConexa mcc(g);
    cout << mcc.maximo() << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}