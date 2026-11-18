// =====================================================================
// Acepta el Reto #341 - Reina del super
// https://aceptaelreto.com/problem/statement.php?id=341
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-3/EJ_02-3.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - la entrada termina al acabarse el fichero (no hay caso `0 0`)
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
#include <utility>
using namespace std;

/*@ <answer>

 Reina del super

 N cajas y una fila unica de C clientes con su tiempo de atencion. Decir en que caja acabara
 Ismael, que va detras del ultimo. La entrada acaba con un caso con 0 cajas.

 PLANTEAMIENTO
 Cola de minimos de pares (instante en que la caja queda libre, numero de caja): el pair se compara
 primero por instante y luego por caja, que es justo el desempate del enunciado. Cada cliente saca
 la cima, le suma su tiempo y la vuelve a meter. Al final, la cima es la caja de Ismael.

 Coste: O(N + C log N) por caso.

 Cajas --> 1 <= N <= 250.000
 Clientes --> 1 <= C <= 250.000
 Tiempo de atencion --> 1 <= T <= 100
 Instante maximo: 500.000 * 100 = 50.000.000 --> cabe en int

 @ </answer> */


// ================================================================
// Escribe el codigo completo de tu solucion aqui debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int cajas;
    if (!(cin >> cajas)) return false;
	// si no hay cajas, no hay caso que resolver
    if (cajas == 0) return false;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;

    for (int i = 1; i <= cajas; ++i) {
		//genero los pares (tiempo, id) de los cajeros y los meto en la cola
        cola.push(pair<int, int>(0, i));
	}

    int clientes;
    cin >> clientes;
	//Simulo la llegada de los clientes, y voy actualizando el tiempo de cada cajero
    for (int i = 0; i < clientes; ++i) {
        int tiempo;
        cin >> tiempo;
        pair<int, int> cajero = cola.top(); cola.pop();
        cajero.first += tiempo;
        cola.push(cajero);
    }
	cout << cola.top().second << '\n'; // cajero que le tocara a Ismael (el acosador)
	return true;
}

//@ </answer>
//  Lo que se escriba dejado de esta linea ya no forma parte de la solucion.

int main() {
    while (resuelveCaso());
    return 0;
}
