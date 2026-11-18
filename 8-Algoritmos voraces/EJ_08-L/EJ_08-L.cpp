#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <functional>

using namespace std;

/*
    Planificacion de conferencias

    N conferencias (1 <= N <= 250.000), cada una con su hora de comienzo y de fin (enteros
    0..10^9, comienzo < fin). Dos conferencias que se solapan no pueden ir en la misma sala;
    una que empieza justo cuando acaba otra NO se solapa con ella. Escribir el minimo numero R
    de salas y una asignacion valida: la sala (1..R) de cada conferencia en el orden de entrada.
*/

/*
    PLANTEAMIENTO (voraz)
    Se recorren las conferencias por hora de COMIENZO. Para cada una:
      - si alguna sala ya esta libre (su ultima conferencia acabo como muy tarde cuando empieza
        esta), se reutiliza;
      - si no, se abre una sala nueva.
    Para saber rapido si hay alguna sala libre basta mirar la que queda libre ANTES: una cola
    de prioridad de minimos con (hora en que queda libre, numero de sala).

    Por que es optimo: solo se abre una sala nueva cuando todas las abiertas estan ocupadas en
    el instante en que empieza la conferencia. En ese instante hay tantas conferencias a la vez
    como salas abiertas mas una, asi que ninguna planificacion puede usar menos.

    Las conferencias se ordenan por indices para poder escribir la sala de cada una en el orden
    de la entrada.

    Coste: O(N log N) por caso.
*/

void resuelveCaso() {
    int N;
    cin >> N;
    vector<int> ini(N), fin(N);
    for (int i = 0; i < N; ++i) cin >> ini[i] >> fin[i];

    vector<int> orden(N);
    for (int i = 0; i < N; ++i) orden[i] = i;
    sort(orden.begin(), orden.end(), [&](int a, int b) { return ini[a] < ini[b]; });

    using Libre = pair<int, int>;      // (hora en que la sala queda libre, sala)
    priority_queue<Libre, vector<Libre>, greater<Libre>> salas;
    vector<int> sala(N);
    int numSalas = 0;
    for (int c : orden) {
        if (!salas.empty() && salas.top().first <= ini[c]) {
            sala[c] = salas.top().second;      // reutilizar la que queda libre antes
            salas.pop();
        } else {
            sala[c] = ++numSalas;              // todas ocupadas: sala nueva
        }
        salas.push({fin[c], sala[c]});
    }

    cout << numSalas << '\n';
    for (int i = 0; i < N; ++i) cout << sala[i] << (i + 1 < N ? ' ' : '\n');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
