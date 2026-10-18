#include <iostream>
#include <vector>
#include <algorithm>
#include "GrafoValorado.h"
#include "ConjuntosDisjuntos.h"

using namespace std;

/*
    La selva de Tarzan

    N arboles (1 <= N <= 10.000) y M saltos posibles (0 <= M <= 100.000);
    cada salto une dos arboles y exige una cuerda de AL MENOS cierta longitud
    (hasta 1.000.000). Tarzan lleva una sola cuerda y quiere poder ir de cualquier
    arbol a cualquier otro. Longitud MINIMA de cuerda, o "Imposible".
    La entrada es una secuencia de selvas (hasta el final del fichero).
*/

/*
    PLANTEAMIENTO
    Grafo valorado no dirigido: arboles = vertices, saltos = aristas,
    longitud minima del salto = valor.

    Con una cuerda de longitud L se pueden hacer todos los saltos de valor <= L.
    Se busca el menor L tal que las aristas de valor <= L conecten todo el grafo.

    Eso es lo que hace KRUSKAL: mete aristas de menor a mayor, y cuando mete una de
    valor L es porque ya estan todas las mas cortas. La respuesta es el valor de la
    ULTIMA arista que Kruskal acepta (la que deja todos los arboles conectados):
    la arista mas pesada de un ARM.

    Diferencia con 06-3: no se suman los costes, se guarda el valor de la ultima.

    Si al terminar quedan varios conjuntos --> "Imposible".
    Con N = 1 no se acepta ninguna arista y ya hay un solo conjunto --> 0.

    Coste: O(N + M log M).
*/

bool resuelveCaso() {
    GrafoValorado<int> g(cin, 1);   // N, M y M saltos; arboles numerados desde 1
    if (!cin) return false;         // fin de la entrada

    vector<Arista<int>> saltos = g.aristas();
    sort(saltos.begin(), saltos.end());   // por longitud creciente

    ConjuntosDisjuntos cd(g.V());
    int ultima = 0;
    for (auto const& s : saltos) {
        if (cd.num_cjtos() == 1) break;
        int u = s.uno(), v = s.otro(u);
        if (!cd.unidos(u, v)) {
            cd.unir(u, v);
            ultima = s.valor();
        }
    }

    if (cd.num_cjtos() == 1) cout << ultima << '\n';
    else cout << "Imposible\n";
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());

    return 0;
}
