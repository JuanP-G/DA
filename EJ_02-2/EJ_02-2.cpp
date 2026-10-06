#include <iostream>
#include <queue>
#include <vector>
using namespace std;

struct Envio {
    long long t;      // instante del próximo envío
    int id;           // identificador del usuario
    int periodo;      // cada cuánto le toca

    // primero por tiempo, y a igualdad, por id
    bool operator>(const Envio& o) const {
        if (t != o.t) return t > o.t;
        return id > o.id;
    }
};

bool resuelveCaso() {
    int n;
    cin >> n;
    if (n == 0) return false;

    priority_queue<Envio, vector<Envio>, greater<Envio>> cola;

    for (int i = 0; i < n; ++i) {
        int id, p;
        cin >> id >> p;
        cola.push({ (long long)p, id, p });   // primer envío en t = p
    }

    int K;
    cin >> K;
    for (int i = 0; i < K; ++i) {
        Envio e = cola.top(); cola.pop();
        cout << e.id << '\n';
        e.t += e.periodo;                   // modifico mi copia
        cola.push(e);
    }
    cout << "---\n";
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}