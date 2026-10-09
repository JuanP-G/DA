#include <iostream>
#include <queue>
#include <vector>
using namespace std;

bool resuelveCaso() {
    int N;
    cin >> N;
    if (N == 0) return false;

    // cola de prioridad de MÍNIMOS
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