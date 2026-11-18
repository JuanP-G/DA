#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

/*
    Construyendo dianas

    Un valor V (1..50.000) y una diana con S sectores (1..100) de puntuaciones distintas en orden
    creciente (1..1.000). Cada sector se puede usar las veces que haga falta. Escribir el minimo
    numero de dardos para sumar V y las puntuaciones usadas ("4: 25 25 25 25"), o Imposible.
    La entrada acaba con el fichero.
*/

/*
    PLANTEAMIENTO (programacion dinamica: problema del cambio con monedas ilimitadas)
        dardos(i, j) = minimo numero de dardos para sumar j usando los sectores 1..i

        dardos(0, 0) = 0        dardos(0, j) = INF  si j > 0
        dardos(i, j) = dardos(i - 1, j)                              si p_i > j
                     = min(dardos(i - 1, j), dardos(i, j - p_i) + 1) si p_i <= j
    En la segunda opcion se queda en la fila i porque el sector i se puede volver a usar.

    Se guarda la tabla entera para reconstruir la solucion desde (S, V) hacia atras:
      - si dardos(i, j) == dardos(i - 1, j), el sector i no hace falta: se sube a la fila i - 1;
      - si no, se ha usado el sector i: se apunta y se pasa a (i, j - p_i).
    Asi salen las puntuaciones de mayor a menor, como en el ejemplo.

    Coste: O(S * V) en tiempo y en espacio por caso.
*/

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int V, S;
    while (cin >> V >> S) {
        vector<int> p(S + 1);
        for (int i = 1; i <= S; ++i) cin >> p[i];

        const int INF = INT_MAX;
        vector<vector<int>> dardos(S + 1, vector<int>(V + 1, INF));
        dardos[0][0] = 0;
        for (int i = 1; i <= S; ++i) {
            dardos[i][0] = 0;
            for (int j = 1; j <= V; ++j) {
                dardos[i][j] = dardos[i - 1][j];
                if (p[i] <= j && dardos[i][j - p[i]] != INF)
                    dardos[i][j] = min(dardos[i][j], dardos[i][j - p[i]] + 1);
            }
        }

        if (dardos[S][V] == INF) { cout << "Imposible\n"; continue; }

        cout << dardos[S][V] << ':';
        int i = S, j = V;
        while (j > 0) {
            if (dardos[i][j] == dardos[i - 1][j]) --i;   // el sector i no se usa
            else { cout << ' ' << p[i]; j -= p[i]; }     // se usa el sector i
        }
        cout << '\n';
    }
    return 0;
}
