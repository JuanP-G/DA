
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>

using namespace std;

#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 Multitarea

 N tareas únicas [c, f) y M periódicas (se repiten cada p minutos). Decir si dos se solapan dentro
 de [0, T): SI o NO.

 PLANTEAMIENTO (barrido por comienzo)
 IndexPQ<pair<int,int>> de mínimos: índice = tarea, prioridad = (ini, fin) de su próxima aparición.
 Se van sacando por orden de comienzo guardando el fin de la última: si una empieza antes, hay
 conflicto. Una periódica no se saca: update a su siguiente aparición (ini + p, fin + p).

 Coste: O(k log (N + M)), con k el número de apariciones antes de T o del primer conflicto.

 N --> tareas unicas
 M --> tareasperiodicas
 T --> minutos donde saber si hay conflictos

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
	int N, M, T;
	cin >> N >> M >> T;

	IndexPQ<pair<int, int>> cola(N + M);   // prioridad = (ini, fin)
	vector<int> periodo(N + M, 0);        // 0 --> tarea única
	// 1..N --> Tareas unicas
	for (int i = 0; i < N; i++) {
		int ini, fin;
		cin >> ini >> fin;
		cola.push(i, { ini, fin });
	}

	// n..M+N --> Tareas periódicas
	for (int i = N; i < N + M; i++) {
		int ini, fin, p;
		cin >> ini >> fin >> p;
		cola.push(i, { ini, fin });
		periodo[i] = p;
	}

	int tiempoActual = 0;
	bool hayConflictos = false;
	while (!hayConflictos && !cola.empty() && cola.top().prioridad.first < T) {
		auto tarea = cola.top();
		int elem = tarea.elem;
		int ini = tarea.prioridad.first;
		int fin = tarea.prioridad.second;

		if (ini < tiempoActual) hayConflictos = true;
		else {
			tiempoActual = fin;
			if (periodo[elem] != 0)
				cola.update(elem, { ini + periodo[elem], fin + periodo[elem] });
			else
				cola.pop();
		}
	}

	cout << (hayConflictos ? "SI" : "NO") << "\n";
}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   int numCasos;
   std::cin >> numCasos;
   for (int i = 0; i < numCasos; ++i)
      resuelveCaso();

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
