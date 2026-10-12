// =====================================================================
// Acepta el Reto #351 - Unidad Curiosa de Monitorizacion
// https://aceptaelreto.com/problem/statement.php?id=351
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-2/EJ_02-2.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - el separador de cada caso es `----` (cuatro guiones)
// =====================================================================

#include <iostream>
#include <queue>
#include <vector>
using namespace std;

struct Envio {
    long long t;      // instante del proximo envio
    int id;           // identificador del usuario
    int periodo;      // cada cuanto le toca

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
        cola.push({ (long long)p, id, p });   // primer envio en t = p
    }

    int K;
    cin >> K;
    for (int i = 0; i < K; ++i) {
        Envio e = cola.top(); cola.pop();
        cout << e.id << '\n';
        e.t += e.periodo;                   // modifico mi copia
        cola.push(e);
    }
    cout << "----\n";
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}
