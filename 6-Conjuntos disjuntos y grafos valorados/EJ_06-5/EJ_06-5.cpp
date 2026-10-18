#include <iostream>
#include <vector>
#include <algorithm>
#include "GrafoValorado.h"
#include "ConjuntosDisjuntos.h"

using namespace std;

/*
    Las minas del emperador Trajano

    N camaras (1 <= N <= 20.000) y M galerias (0 <= M <= 200.000) que se recorren en
    los dos sentidos y tardan cierto tiempo (hasta 1.000.000 s) en recorrerse.
    Palencia Jones va de la camara 'origen' a la camara 'destino' aguantando la
    respiracion en cada galeria. Tiempo MAXIMO que tendra que aguantar (de camara
    en camara) por el camino que menos le exija, o "IMPOSIBLE".
*/

/*
    PLANTEAMIENTO
    Grafo valorado no dirigido. No se minimiza la SUMA de un camino sino su arista
    MAS LARGA (se descansa en cada camara): hay que encontrar el camino cuya galeria
    mas larga sea lo mas corta posible ("camino de cuello de botella", minimax).

    Con un limite T se puede usar cualquier galeria de tiempo <= T. El menor T que
    conecta origen y destino se encuentra con KRUSKAL: se anaden aristas de menor a
    mayor y se PARA en cuanto origen y destino estan unidos (unidos(origen, destino)).
    La respuesta es el valor de la arista que lo consigue.

    Casos:
      origen == destino  --> 0  (no hay que bucear)
      nunca se unen      --> IMPOSIBLE

    Coste: O(N + M log M).
*/

void resuelveCaso() {
    GrafoValorado<int> g(cin, 1);   // N, M y M galerias; camaras numeradas desde 1
    int origen, destino;
    cin >> origen >> destino;
    --origen; --destino;

    vector<Arista<int>> galerias = g.aristas();
    sort(galerias.begin(), galerias.end());   // por tiempo creciente

    ConjuntosDisjuntos cd(g.V());
    int aguante = 0;
    for (auto const& a : galerias) {
        if (cd.unidos(origen, destino)) break;
        int u = a.uno(), v = a.otro(u);
        if (!cd.unidos(u, v)) {
            cd.unir(u, v);
            aguante = a.valor();
        }
    }

    if (cd.unidos(origen, destino)) cout << aguante << '\n';
    else cout << "IMPOSIBLE\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
