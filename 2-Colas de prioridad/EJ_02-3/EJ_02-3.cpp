
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

 Reina del súper

 N cajas y una fila única de C clientes con su tiempo de atención. Decir en qué caja acabará
 Ismael, que va detrás del último. La entrada acaba con un caso con 0 cajas.

 PLANTEAMIENTO
 Cola de mínimos de pares (instante en que la caja queda libre, número de caja): el pair se compara
 primero por instante y luego por caja, que es justo el desempate del enunciado. Cada cliente saca
 la cima, le suma su tiempo y la vuelve a meter. Al final, la cima es la caja de Ismael.

 Coste: O(N + C log N) por caso.

 Cajas --> 1 ≤ 𝘕 ≤ 𝟤𝟧𝟢.𝟢𝟢0
 Clientes --> 1 ≤ C ≤ 𝟤𝟧𝟢.𝟢𝟢0
 Tiempo de atencion --> 1 ≤ T ≤ 1𝟢0
 Instante maximo: 500.000 * 100 = 50.000.000 --> cabe en int

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int cajas;
    cin >> cajas;
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
