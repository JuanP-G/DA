#include <iostream>
#include <vector>
#include <algorithm>
#include "GrafoValorado.h"
#include "ConjuntosDisjuntos.h"

using namespace std;

/*
    Recorriendo el archipielago en bicicleta

    I islas (1 <= I <= 10.000) y P puentes presupuestados (0 <= P <= 100.000),
    cada uno une dos islas y tiene un coste (1..100.000).
    Elegir puentes para poder ir de cualquier isla a cualquier otra con coste
    total MINIMO. Si no hay puentes suficientes: "No hay puentes suficientes".
*/

/*
    PLANTEAMIENTO
    Arbol de recubrimiento de coste minimo (ARM) de un grafo valorado:
    islas = vertices, puentes = aristas, coste = valor.
    Un ARM conecta todos los vertices con V - 1 aristas y suma minima.

    Algoritmo de KRUSKAL:
      1. Ordenar los puentes por coste creciente.
      2. Particion de las islas: al principio cada una esta sola.
      3. Para cada puente en ese orden:
            si sus dos islas YA estan unidas  --> cerraria un ciclo: se descarta
            si no                             --> se construye: unir y sumar coste.
      4. Si se han elegido I - 1 puentes, la suma es la respuesta;
         si no, el grafo no es conexo --> "No hay puentes suficientes".

    Por que funciona (propiedad del corte): el puente mas barato que cruza de un
    grupo de islas al resto pertenece a algun ARM. Cuando Kruskal llega a un puente
    que une dos conjuntos distintos, es el mas barato que sale de uno de ellos.

    Con I = 1 no hace falta ningun puente: 0.

    Coste: ordenar O(P log P) + particion O(I + P lg* I) --> O(I + P log P).
*/

void resuelveCaso() {
    GrafoValorado<int> g(cin, 1);   // I, P y P puentes; islas numeradas desde 1

    vector<Arista<int>> puentes = g.aristas();
    sort(puentes.begin(), puentes.end());   // por coste creciente (operator< de Arista)

    ConjuntosDisjuntos cd(g.V());
    long long coste = 0;
    int elegidos = 0;
    for (auto const& p : puentes) {
        if (elegidos == g.V() - 1) break;
        int u = p.uno(), v = p.otro(u);
        if (!cd.unidos(u, v)) {
            cd.unir(u, v);
            coste += p.valor();
            ++elegidos;
        }
    }

    if (elegidos == g.V() - 1) cout << coste << '\n';
    else cout << "No hay puentes suficientes\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
