#include <iostream>
#include <vector>
#include <queue>
#include <functional>
#include "Digrafo.h"

using namespace std;

/*
    MasterHash

    N elaboraciones (1..100.000) y A anotaciones (0..200.000) "X Y": la elaboracion X hace
    falta para la Y. La elaboracion S se ha quemado y P es el plato que se quiere hacer.
    El plato se puede hacer si no necesita S (ni directa ni indirectamente, y P != S) y las
    anotaciones de lo que necesita no tienen ciclos. Escribir NO, o SI seguido de un orden
    valido de las elaboraciones necesarias que acabe en P.
*/

/*
    PLANTEAMIENTO (digrafos: alcanzabilidad en el inverso + orden topologico)
    1. Lo que hace falta para P son los vertices desde los que se llega a P. En el grafo
       INVERSO son los alcanzables desde P: un recorrido (BFS o DFS) desde P en g.inverso().
    2. Si S esta entre ellos (incluido S == P), el plato no se puede hacer: NO.
    3. Orden topologico SOLO de esos vertices (algoritmo de Kahn): se cuentan sus aristas de
       entrada dentro del conjunto y se van sacando los que no tienen ninguna pendiente. Si no
       salen todos, hay un ciclo entre las elaboraciones necesarias: NO.
       Un ciclo en elaboraciones que P no necesita no importa.
    Como todos los vertices del conjunto llegan a P, P sale el ultimo. Se usa una cola de
    prioridad de minimos para que, entre las disponibles, salga siempre la de menor numero
    (asi el orden es el del ejemplo: SI 2 3 4 5).

    Coste: O(N + A log N) por caso.
*/

void resuelveCaso() {
    int N, A, S, P;
    cin >> N >> A >> S >> P;
    --S; --P;
    Digrafo g(N);
    for (int i = 0; i < A; ++i) {
        int x, y;
        cin >> x >> y;
        g.ponArista(x - 1, y - 1);
    }

    // 1. elaboraciones necesarias: alcanzables desde P en el inverso
    Digrafo inv = g.inverso();
    vector<bool> necesaria(N, false);
    vector<int> pila = {P};
    necesaria[P] = true;
    while (!pila.empty()) {
        int v = pila.back(); pila.pop_back();
        for (int w : inv.ady(v))
            if (!necesaria[w]) { necesaria[w] = true; pila.push_back(w); }
    }

    // 2. ¿depende del sofrito?
    if (necesaria[S]) { cout << "NO\n"; return; }

    // 3. orden topologico de las necesarias (Kahn)
    vector<int> entrada(N, 0);
    int total = 0;
    for (int v = 0; v < N; ++v) {
        if (!necesaria[v]) continue;
        ++total;
        for (int w : g.ady(v))
            if (necesaria[w]) ++entrada[w];
    }
    priority_queue<int, vector<int>, greater<int>> libres;
    for (int v = 0; v < N; ++v)
        if (necesaria[v] && entrada[v] == 0) libres.push(v);

    vector<int> orden;
    while (!libres.empty()) {
        int v = libres.top(); libres.pop();
        orden.push_back(v);
        for (int w : g.ady(v))
            if (necesaria[w] && --entrada[w] == 0) libres.push(w);
    }

    if ((int)orden.size() < total) { cout << "NO\n"; return; }   // hay un ciclo
    cout << "SI";
    for (int v : orden) cout << ' ' << v + 1;
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
