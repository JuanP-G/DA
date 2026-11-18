
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <functional>
using namespace std;

#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 12 points go to…

 Eventos: sumar o restar puntos a un país, o preguntar (?) quién va primero y con cuántos puntos
 (empate -> nombre menor). La entrada acaba con el fichero.

 PLANTEAMIENTO
 IndexPQ<pair<int,string>, Mejor>: índice = número del país (unordered_map nombre -> índice),
 prioridad = (puntos, nombre). En cada cambio, update(idx, nuevos puntos): sube o baja en el
 montículo. En cada ?, top() da el líder.

 Coste: O(log P) por evento, con P el número de países.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

using Par = pair<int, string>;   // (puntos, nombre)

struct Mejor {
	bool operator()(Par const& a, Par const& b) const {
		if (a.first != b.first) return a.first > b.first;   // más puntos va antes
		return a.second < b.second;                          // empate: nombre menor va antes
	}
};

bool resuelveCaso() {
	//Numero de eventos que se van a realizar
	int n;
	if (!(cin >> n)) return false;

	IndexPQ<Par, Mejor> pq(n);
	unordered_map<string, int> indice; // nombre -> índice en la cola
	int siguiente = 0;
		
	for (int i = 0; i < n; ++i) {
		string nombre;
		cin >> nombre;

		if (nombre == "?") {
			auto const& lider = pq.top().prioridad;
			cout << lider.second << " " << lider.first << "\n";
		}
		else {
			int puntos;
			cin >> puntos;

			int idx, actuales;

			auto it = indice.find(nombre);
			if (it == indice.end()) {          // país nuevo
				idx = siguiente++;
				indice[nombre] = idx;
				actuales = 0;
			}
			else {                              // país que ya estaba en la cola
				idx = it->second;
				actuales = pq.priority(idx).first;
			}

			pq.update(idx, { actuales + puntos, nombre });
		}

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
