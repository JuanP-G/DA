#include <iostream>
#include <vector>
#include "GrafoValorado.h"

using namespace std;

/*
    Camiones de reparto

    V intersecciones (2 <= V <= 10.000) y E calles de doble sentido (0 <= E <= 100.000),
    cada una con la anchura MAXIMA que puede tener un camion para pasar por ella.
    K <= 10 consultas (origen, destino, anchura del camion): SI/NO segun pueda ir.
*/

/*
    PLANTEAMIENTO
    Grafo valorado no dirigido: intersecciones = vertices, calles = aristas,
    anchura maxima = valor de la arista.

    Cada consulta es una pregunta de alcanzabilidad CON FILTRO:
        hay un camino origen --> destino que use solo aristas con valor >= anchura?

    Un recorrido (DFS) desde el origen que ignora las aristas demasiado estrechas lo
    responde. La comparacion es >= : un camion de anchura 15 cabe justo por una calle
    de anchura maxima 15 (el fragmento de las transparencias usa <, que es otra cosa).

    Se repite para cada consulta (el filtro cambia con la anchura), con un vector
    de visitados nuevo cada vez.

    Coste: O(K * (V + E)). La recursion baja como mucho V = 10.000 niveles.
*/

class Alcanzables {
public:
    // vertices alcanzables desde origen usando solo aristas con valor >= ancho
    Alcanzables(GrafoValorado<int> const& g, int origen, int ancho)
        : visitado(g.V(), false), ancho(ancho) {
        dfs(g, origen);
    }

    bool alcanzable(int v) const { return visitado[v]; }

private:
    vector<bool> visitado;
    int ancho;

    void dfs(GrafoValorado<int> const& g, int v) {
        visitado[v] = true;
        for (auto a : g.ady(v)) {
            int w = a.otro(v);
            if (a.valor() >= ancho && !visitado[w]) dfs(g, w);
        }
    }
};

void resuelveCaso() {
	// lee el grafo
    GrafoValorado<int> g(cin, 1);   // V, E y E calles; intersecciones numeradas desde 1

    int k; cin >> k;
    while (k--) {
        int origen, destino, ancho;
        cin >> origen >> destino >> ancho;

		// vertices alcanzables desde origen usando solo aristas con valor >= ancho
        Alcanzables a(g, origen - 1, ancho);
        cout << (a.alcanzable(destino - 1) ? "SI" : "NO") << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
