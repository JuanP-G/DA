#include <iostream>
#include <vector>
#include <functional> //greater
#include "IndexPQ.h"

using namespace std;
/*
drones	--> 1 <= N <= 100.000 (10^5)
pila 9V/1.5V --> 1 <= pila <= 200.000 (2*10^5)
*/

bool resolverCaso(){
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

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	while (resolverCaso());
	return 0;
}