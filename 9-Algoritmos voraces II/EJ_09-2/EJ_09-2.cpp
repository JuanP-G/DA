#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/*
    El alienigena infiltrado

    Intervalo [C, F) y N trabajos (0 <= N <= 200.000), cada uno con su intervalo [c, f).
    Escribir el minimo numero de trabajos que cubren todo [C, F) (en cada instante hay al menos
    uno en marcha), o Imposible.
*/

/*
    PLANTEAMIENTO (voraz: cubrir un intervalo)
    Se ordenan los trabajos por comienzo. 'cubierto' es hasta donde llega lo ya cubierto
    (al principio, C). Mientras cubierto < F:
      - entre los trabajos que empiezan como muy tarde en 'cubierto' (asi no dejan hueco),
        se elige el que acaba MAS TARDE;
      - si ninguno pasa de 'cubierto', hay un hueco: Imposible;
      - si no, cubierto = ese final y se cuenta un trabajo mas.

    Por que es optimo: cualquier solucion necesita un trabajo que cubra el instante 'cubierto';
    ese trabajo empieza como muy tarde ahi, asi que el elegido llega al menos igual de lejos.

    Como los trabajos se recorren una sola vez con un indice que solo avanza, el coste es
    O(N log N) por caso (la ordenacion).
*/

void resuelveCaso() {
    long long C, F;
    int N;
    cin >> C >> F >> N;
    vector<pair<long long, long long>> trab(N);
    for (auto& t : trab) cin >> t.first >> t.second;
    sort(trab.begin(), trab.end());

    long long cubierto = C;
    int usados = 0, i = 0;
    bool posible = true;
    while (cubierto < F) {
        long long masLejos = cubierto;
        while (i < N && trab[i].first <= cubierto) {
            masLejos = max(masLejos, trab[i].second);
            ++i;
        }
        if (masLejos == cubierto) { posible = false; break; }   // hueco sin cubrir
        cubierto = masLejos;
        ++usados;
    }

    if (posible) cout << usados << '\n';
    else cout << "Imposible\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
