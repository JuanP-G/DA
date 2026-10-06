#include <iostream>
#include <vector>
#include "Grafo.h"

using namespace std;

/*
    Arboles libres

    Vertices --> 1 <= V <= 10.000
    Aristas  --> 0 <= A <= 100.000
    Vertices numerados de 0 a V-1, sin lazos ni aristas repetidas
    Entrada: V en una linea y A en la siguiente --> justo lo que lee Grafo(cin)
*/

/*
    PLANTEAMIENTO
    Arbol libre = grafo ACICLICO y CONEXO.

    Propiedad clave de los arboles: un grafo con V vertices es un arbol
    si cumple DOS de estas tres cosas (y entonces cumple la tercera):
        - es conexo
        - es aciclico
        - tiene exactamente V-1 aristas
    Asi que no hace falta buscar ciclos: basta con mirar que A == V-1
    y que un recorrido (DFS) desde cualquier vertice llega a los V.

    Coste: O(V + A) por caso (el DFS visita cada vertice y arista una vez).

    Nota: el dfs recursivo puede llegar a profundidad V (hasta 10.000).
    Un caso enorme podria desbordar la pila.
*/

class ArbolLibre {
public:
    ArbolLibre(Grafo const& g) : visit(g.V(), false), alcanzados(0) {
        dfs(g, 0);   // V >= 1, asi que el vertice 0 siempre existe
        bool conexo = (alcanzados == g.V());
		// un grafo es un arbol libre si es conexo y tiene V-1 aristas
        arbol = conexo && g.A() == g.V() - 1;
    }

    bool esArbol() const { return arbol; }

private:
    vector<bool> visit;   // visit[v] = el dfs ya ha pasado por v
    int alcanzados;       // cuantos vertices ha visitado el dfs
    bool arbol;

    // recorrido en profundidad: marca v y sigue por los adyacentes sin visitar
    void dfs(Grafo const& g, int v) {
        visit[v] = true;
        ++alcanzados;
		//recorre todos los adyacentes a v
        for (int w : g.ady(v))
			//si w no ha sido visitado, lo visita
            if (!visit[w]) dfs(g, w);
    }
};

void resuelveCaso() {
    Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)

    ArbolLibre al(g);
    cout << (al.esArbol() ? "SI" : "NO") << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}