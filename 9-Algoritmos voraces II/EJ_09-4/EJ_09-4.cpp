#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/*
    El telesilla

    Sillas de dos plazas que soportan un peso maximo P (1..10^9) y N usuarios (1 <= N <= 500.000)
    con pesos entre 1 y P. Escribir el minimo numero de viajes (sillas) para subir a todos.
*/

/*
    PLANTEAMIENTO (voraz: emparejar extremos)
    Se ordenan los pesos y se mira el mas pesado (j) que queda por subir:
      - si cabe con el mas ligero (i), suben juntos;
      - si no, el mas pesado no cabe con nadie y sube solo.
    En los dos casos se gasta un viaje.

    Por que es optimo: al mas pesado le conviene ir con el mas ligero; si en una solucion optima
    va con otro (o solo), cambiar su pareja por el mas ligero sigue siendo valido y no anade
    viajes.

    Coste: O(N log N) por caso.
*/

void resuelveCaso() {
    long long P;
    int N;
    cin >> P >> N;
    vector<long long> peso(N);
    for (long long& p : peso) cin >> p;
    sort(peso.begin(), peso.end());

    int viajes = 0;
    int i = 0, j = N - 1;
    while (i <= j) {
        if (i < j && peso[i] + peso[j] <= P) ++i;   // el mas ligero sube con el mas pesado
        --j;                                         // el mas pesado sube (solo o acompanado)
        ++viajes;
    }
    cout << viajes << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
