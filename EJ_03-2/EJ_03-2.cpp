#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <functional>
#include "IndexPQ.h"

using namespace std;

using Par = pair<int, string>;   // (puntos, nombre)

struct Mejor {
	bool operator()(Par const& a, Par const& b) const {
		if (a.first != b.first) return a.first > b.first;   // más puntos va antes
		return a.second < b.second;                          // empate: nombre menor va antes
	}
};

bool resolverCaso() {
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
int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	while (resolverCaso());
	return 0;
}