#include <iostream>
#include <vector>
#include <queue>
#include <utility> //pair
#include <climits>
#include "Pila.h"       // la implementación con vector dinámico
using namespace std;

/*
Pilas           --> 1 <= N <= 100.000       (10^5)
Comics por pila --> 1 <= K <= 100
Identificador   --> 1 <= id <= 100.000.000  (10^8)
Total comics    --> suma de K <= 1.000.000  (10^6)
Puesto (salida) --> 1 <= puesto <= 1.000.000
Todo cabe en int.
*/

bool resuelveCaso() {
    int n;
    if (!(cin >> n)) return false;

    // cola de MÍNIMOS de (identificador, nº de pila)
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;

    vector<Pila<int>> pilas(n);
    int mejor = INT_MAX;

    for (int i = 0; i < n; ++i) {
        int nComics;
        cin >> nComics;
        for (int j = 0; j < nComics; ++j) {
            int id;
            cin >> id;
            pilas[i].apila(id);              // del fondo a la cima: orden correcto
            if (id < mejor) mejor = id;
        }
        cola.push({ pilas[i].cima(), i });     // la cima de esta pila entra en juego
    }

    int puesto = 1;
    while (cola.top().first != mejor) {
        int p = cola.top().second;
        cola.pop();
        pilas[p].desapila();                 // ese cliente se lleva la cima
        if (!pilas[p].esVacia())             // si queda algo, asoma el siguiente
            cola.push({ pilas[p].cima(), p });
        ++puesto;
    }

    cout << puesto << '\n';
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}