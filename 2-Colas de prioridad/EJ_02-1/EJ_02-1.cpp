
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

 Lo que cuesta sumar

 Sumar N números con el mínimo esfuerzo total, sabiendo que sumar a + b cuesta a + b.
 La entrada acaba con un caso con N = 0.

 PLANTEAMIENTO (voraz, como Huffman)
 Cola de prioridad de mínimos con los N números. Mientras quede más de uno, se sacan los dos
 menores, se suma su suma al esfuerzo y se mete el resultado. long long: el esfuerzo crece mucho.

 Coste: O(N log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

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
