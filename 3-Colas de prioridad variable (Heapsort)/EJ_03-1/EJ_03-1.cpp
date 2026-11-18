
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <functional>
using namespace std;

#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 Volando drones

 Cada sábado se monta en cada dron la pila de 9 V y la de 1,5 V más cargadas que queden. Escribir
 las horas de vuelo totales de cada sábado mientras quede alguna pila de cada tipo.
 La entrada acaba con el fichero.

 PLANTEAMIENTO
 Dos colas de máximos (IndexPQ, índice = número de pila, prioridad = horas que le quedan). Cada
 sábado, para cada dron se saca la mejor pila de cada tipo; vuela min(h9, h1) horas y se resta a
 las dos. Las que aún tienen carga se apartan y vuelven a la cola al acabar el sábado.

 Coste: O(P log P) por sábado, con P el número de pilas.

 drones    --> 1 <= N <= 100.000 (10^5)
 pila 9V/1.5V --> 1 <= pila <= 200.000 (2*10^5)

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso(){
	int drones;
	if (!(cin >> drones)) return false;

	int pila9V, pila1V; 
	cin >> pila9V >> pila1V; // no se usan, solo para leer la entrada


	//creo la cola maximos de las pilas de 9V
	IndexPQ<int, greater<int>> cola9V(pila9V); //greater<int> para que sea maximos
	for(int i = 0; i < pila9V; ++i) {
		int horas;
		cin >> horas;
		cola9V.push(i, horas);
	}

	//creo la cola maximos de las pilas de 1.5V
	IndexPQ<int, greater<int>> cola1V(pila1V); //greater<int> para que sea maximos
	for(int i = 0; i < pila1V; ++i) {
		int horas;
		cin >> horas;
		cola1V.push(i, horas);
	}

	//Si no hay drones no puedo volar, devolvemos 0
	if(drones <= 0) {
		cout << "0\n";
		return true;
	}

	//puedo volar el finde si tengo al menos 1 pila de cada tipo y al menos 1 drone
	//2 pilas por drone, 1 de cada tipo
	bool primero = true;
	while (!cola1V.empty() && !cola9V.empty()) {
		int horasFinde = 0;
		vector<pair<int, int>> sobran9V, sobran1V; //para guardar las pilas usadas y devolverlas a la cola

		//cogemos un drone y le metemos 1 pila de cada tipo hasta quedarnos sin drones o pilas
		int contador = 0;
		while (contador < drones && !cola9V.empty() && !cola1V.empty()) {
			//auto = IndexPQ<int, greater<int>>::Par
			auto p9 = cola9V.top();   cola9V.pop();
			auto p1 = cola1V.top();   cola1V.pop();
			// p9.elem, p9.prioridad, p1.elem, p1.prioridad

			int tiempo = min(p9.prioridad, p1.prioridad); //tiempo que puedo volar ese drone
			horasFinde += tiempo;
			p9.prioridad -= tiempo; //restamos el tiempo volado a la pila de 9V
			p1.prioridad -= tiempo; //restamos el tiempo volado a la pila de 1.5V
			if (p9.prioridad > 0) sobran9V.push_back({ p9.elem, p9.prioridad }); //si sobra tiempo de la pila de 9V la guardamos para devolverla a la cola
			if (p1.prioridad > 0) sobran1V.push_back({ p1.elem, p1.prioridad }); //si sobra tiempo de la pila de 1.5V la guardamos para devolverla a la cola

			++contador;
		}
		
		for (auto& s : sobran9V) cola9V.push(s.first, s.second); //devolvemos las pilas de 9V sobrantes a la cola
		for (auto& s : sobran1V) cola1V.push(s.first, s.second); //devolvemos las pilas de 1.5V sobrantes a la cola

		if (!primero) cout << ' '; //si no es el primer caso, ponemos un espacio
		cout << horasFinde; //devolvemos las horas voladas ese finde
		primero = false;
	}
	cout << '\n';
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
