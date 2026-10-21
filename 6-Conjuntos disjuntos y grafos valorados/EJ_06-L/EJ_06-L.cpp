#include <iostream>
#include <vector>
#include <algorithm>
#include "GrafoValorado.h"
#include "ConjuntosDisjuntos.h"

using namespace std;

/*
    Donde construimos los aeropuertos?

    N localidades (1 <= N <= 10.000), M carreteras posibles de doble sentido
    (0 <= M <= 100.000, puede haber varias entre el mismo par) con coste C, y
    un aeropuerto cuesta A. Cada localidad debe tener un aeropuerto o poder llegar
    por carretera a otra que lo tenga. Salida: coste minimo y numero de aeropuertos;
    si hay varias soluciones de coste minimo, la que tenga MAS aeropuertos.
*/

/*
    PLANTEAMIENTO
    Localidades = vertices, carreteras = aristas. Una solucion es un conjunto de
    carreteras que parte las localidades en grupos conexos, con UN aeropuerto por grupo:

        coste = (suma de las carreteras construidas) + A * (numero de grupos)

    Conectar dos grupos con una carretera de coste C ahorra un aeropuerto (A), asi que
    compensa si C < A. Por tanto:

    * Kruskal normal (carreteras por coste creciente, descartando las que cierran ciclo),
      pero SOLO se construyen las carreteras con C < A. Como van ordenadas, en cuanto
      una cuesta A o mas se puede parar: las siguientes cuestan aun mas.
    * Cada grupo que queda (cd.num_cjtos()) necesita su aeropuerto.

    EMPATE: una carretera con C == A cuesta lo mismo que el aeropuerto que ahorra, y el
    enunciado prefiere MAS aeropuertos ==> con C == A NO se construye (condicion estricta C < A).
    Con C < A el ahorro es real, asi que la solucion es unica en numero de aeropuertos.

    * Varias carreteras entre el mismo par: Kruskal se queda con la mas barata y descarta
      el resto como ciclo (las dos localidades ya estan unidas).
    * N = 1: ningun grupo mas, un aeropuerto: coste A, 1 aeropuerto.

    Coste: ordenar O(M log M) + conjuntos disjuntos O(N + M lg* N).
    Tamanos: el coste maximo es unos 10^4 * 10^5 + 10^4 * 10^5 = 2 * 10^9 (no cabe en
    un int con seguridad) --> long long.
*/

void resuelveCaso() {
    int N, M, A;
    cin >> N >> M >> A;

    GrafoValorado<int> g(N);
    for (int i = 0; i < M; ++i) {
        int x, y, c;
        cin >> x >> y >> c;
        g.ponArista({x - 1, y - 1, c});      // localidades desde 1
    }

    vector<Arista<int>> carreteras = g.aristas();
    sort(carreteras.begin(), carreteras.end());   // por coste creciente

    ConjuntosDisjuntos cd(N);
    long long coste = 0;
    for (auto const& c : carreteras) {
        if (c.valor() >= A) break;                // ya no compensa (y las siguientes aun menos)
        int u = c.uno(), v = c.otro(u);
        if (!cd.unidos(u, v)) {
            cd.unir(u, v);
            coste += c.valor();
        }
    }

    int aeropuertos = cd.num_cjtos();             // un aeropuerto por grupo
    coste += (long long)aeropuertos * A;
    cout << coste << ' ' << aeropuertos << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
