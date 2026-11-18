
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <queue>
#include <vector>
using namespace std;

/*@ <answer>

 Unidad Curiosa de Monitorización

 Usuarios con un periodo de envío. Escribir a quién van los K primeros envíos; si coinciden en el
 tiempo, primero el de identificador menor. Tras cada caso, ---. Acaba con un caso con n = 0.

 PLANTEAMIENTO (simulación por eventos)
 Cola de mínimos de Envio(t, id, periodo) ordenada por (t, id). Cada usuario entra con t = periodo.
 K veces: se saca la cima, se escribe su id y vuelve a entrar con t + periodo.

 Coste: O((n + K) log n) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

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

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   while (resuelveCaso());

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
