// =====================================================================
// Acepta el Reto #289 - Lo que cuesta sumar
// https://aceptaelreto.com/problem/statement.php?id=289
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-1/EJ_02-1.cpp
// (no la edites a mano: se vuelve a generar).
// =====================================================================

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

 Sumar N numeros con el minimo esfuerzo total, sabiendo que sumar a + b cuesta a + b.
 La entrada acaba con un caso con N = 0.

 PLANTEAMIENTO (voraz, como Huffman)
 Cola de prioridad de minimos con los N numeros. Mientras quede mas de uno, se sacan los dos
 menores, se suma su suma al esfuerzo y se mete el resultado. long long: el esfuerzo crece mucho.

 Coste: O(N log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el codigo completo de tu solucion aqui debajo
// ================================================================
//@ <answer>

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

//@ </answer>
//  Lo que se escriba dejado de esta linea ya no forma parte de la solucion.

int main() {
    while (resuelveCaso());
    return 0;
}
