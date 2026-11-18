#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/*
    ¡En primera linea de playa!

    N edificios (1 <= N <= 100.000), cada uno con su extremo occidental W y oriental E (W < E,
    enteros 0..10^9). Un pasadizo de 1 metro de ancho sirve a un edificio si queda COMPLETAMENTE
    debajo de el: el pasadizo del metro [x, x + 1] sirve al edificio [W, E] si W <= x y x + 1 <= E.
    Escribir el minimo numero de pasadizos para servir a todos los edificios.
*/

/*
    PLANTEAMIENTO (voraz: puntos que pinchan intervalos)
    Se ordenan los edificios por su extremo ORIENTAL. El edificio que acaba antes necesita un
    pasadizo; lo mejor es ponerlo lo mas al este posible dentro de el, en el metro [E - 1, E]:
    asi sirve tambien a todos los edificios que empiezan como muy tarde en E - 1.

    Recorriendo en ese orden, un edificio ya esta servido por el ultimo pasadizo (en [x, x + 1])
    si W <= x (su E es >= que el del edificio que lo coloco, asi que x + 1 <= E). Si no, se pone
    un pasadizo nuevo en su metro mas oriental.

    Ojo: dos edificios que solo se tocan en un punto ([1, 4] y [4, 8]) no comparten ningun metro.

    Coste: O(N log N) por caso.
*/

void resuelveCaso() {
    int N;
    cin >> N;
    vector<pair<int, int>> edif(N);        // (E, W) para ordenar por el extremo oriental
    for (auto& e : edif) cin >> e.second >> e.first;
    sort(edif.begin(), edif.end());

    int pasadizos = 0;
    long long x = -1;                      // el ultimo pasadizo ocupa el metro [x, x + 1]
    for (auto const& [E, W] : edif) {
        if (pasadizos == 0 || W > x) {
            ++pasadizos;
            x = E - 1;
        }
    }
    cout << pasadizos << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
