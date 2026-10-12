// =====================================================================
// Acepta el Reto #289 - Lo que cuesta sumar
// https://aceptaelreto.com/problem/statement.php?id=289
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-1/EJ_02-1.cpp
// (no la edites a mano: se vuelve a generar).
// =====================================================================

#include <iostream>
#include <queue>
#include <vector>
using namespace std;

bool resuelveCaso() {
    int N;
    cin >> N;
    if (N == 0) return false;

    // cola de prioridad de MINIMOS
    priority_queue<long long, vector<long long>, greater<long long>> cola;
    for (int i = 0; i < N; ++i) {
        int x; cin >> x;
        cola.push(x);
    }

    long long esfuerzo = 0;
    while (cola.size() > 1) {
        long long a = cola.top(); cola.pop();
        long long b = cola.top(); cola.pop();
        esfuerzo += a + b;   // actualizar esfuerzo
        cola.push(a + b);   // devolver el resultado a la cola
    }

    cout << esfuerzo << '\n';
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}
