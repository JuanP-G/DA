#include <iostream>
#include "IndexPQ.h"

using namespace std;

/*
	N --> tareas unicas
	M --> tareasperiodicas
	T --> minutos donde saber si hay conflictos
*/
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

int main() {

	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int casos; cin >> casos;
	for (int i = 0; i < casos; i++)
		resuelveCaso();

	return 0;
}