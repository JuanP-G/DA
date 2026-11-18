// =====================================================================
// Acepta el Reto #271 - Pajaros en vuelo
// https://aceptaelreto.com/problem/statement.php?id=271
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 3-Colas de prioridad variable (Heapsort)/EJ_03-4/EJ_03-4.cpp
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
#include <functional>
using namespace std;

/*@ <answer>

 Pajaros en vuelo

 Una bandada empieza con un pajaro y se le unen parejas. Tras cada pareja escribir la mediana de
 las edades. La entrada acaba con un caso 0 0.

 PLANTEAMIENTO (mediana con dos monticulos)
 lider = mediana; menores = cola de maximos con los mas jovenes; mayores = cola de minimos con los
 mas viejos, siempre del mismo tamano. Cada pajaro nuevo va a su lado; si un lado queda con dos
 mas, el lider pasa al lado pequeno y la cima del grande es el nuevo lider.

 Coste: O(log P) por pareja.

 @ </answer> */


// ================================================================
// Escribe el codigo completo de tu solucion aqui debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int primero, parejas;
    cin >> primero >> parejas;

    if (primero == 0 && parejas == 0) return false;

    priority_queue<int> menores;                             // max-heap
    priority_queue<int, vector<int>, greater<int>> mayores;  // min-heap
    int lider = primero;

    for (int i = 0; i < parejas; ++i) {
        for (int j = 0; j < 2; ++j) {
            int edad; cin >> edad;

            if (edad < lider) menores.push(edad);
            else mayores.push(edad);
        }
        if (menores.size() > mayores.size()) {
            mayores.push(lider);
            lider = menores.top(); menores.pop();
        }
        else if (mayores.size() > menores.size()) {
            menores.push(lider);
            lider = mayores.top(); mayores.pop();
        }
        cout << lider << (i + 1 < parejas ? ' ' : '\n');
    }
    return true;
}

//@ </answer>
//  Lo que se escriba dejado de esta linea ya no forma parte de la solucion.

int main() {
    while (resuelveCaso());
    return 0;
}
