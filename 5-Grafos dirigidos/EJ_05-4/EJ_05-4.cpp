#include <iostream>
#include <vector>
#include "Digrafo.h"

using namespace std;

/*
    Sumidero en un grafo dirigido

    Vertices --> 1 <= V <= 10.000
    Aristas  --> 0 <= A <= 100.000 (sin lazos ni repetidas)
    Salida: "SI s" si s es sumidero, "NO" si no hay ninguno
*/

/*
    PLANTEAMIENTO
    s es sumidero <=> grado de salida 0  Y  grado de entrada V - 1
    (como no hay aristas repetidas ni lazos, entrada V - 1 significa
    que TODOS los demas vertices tienen una arista hacia s).

    - grado de salida de v  = g.ady(v).size()
    - grado de entrada de v = cuantas veces aparece v en las listas
      de adyacentes (un recorrido de todas las listas, O(V + A))

    * Como mucho hay UN sumidero: si s y t lo fueran, habria arista t --> s,
      y entonces t no tendria grado de salida 0.
    * V = 1: el unico vertice tiene salida 0 y entrada 0 = V - 1 --> SI 0.

    Coste: O(V + A) por caso.
*/

int sumidero(Digrafo const& g) {
    vector<int> entrada(g.V(), 0);
    for (int v = 0; v < g.V(); ++v)
        for (int w : g.ady(v))
            ++entrada[w];                  // arista v --> w: una mas de entrada a w

    for (int v = 0; v < g.V(); ++v)
        if (g.ady(v).empty() && entrada[v] == g.V() - 1)
            return v;
    return -1;
}

bool resuelveCaso() {
    Digrafo g(cin);                        // lee V, A y las aristas (vertices desde 0)
    if (!cin) return false;

    int s = sumidero(g);
    if (s == -1) cout << "NO\n";
    else cout << "SI " << s << '\n';
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());

    return 0;
}
