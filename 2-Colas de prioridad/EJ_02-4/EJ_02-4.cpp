#include <iostream>
#include <vector>
#include <queue>

using namespace std;

struct Candidatura {
    long long votos;
    int escanios;
    int orden;   // posicion en la entrada, para desempatar y para la salida

    // "tiene menos prioridad que o": compara votos/(1+escanios) sin dividir
    bool operator<(const Candidatura& o) const {
        long long izq = votos * (1 + o.escanios);
        long long der = o.votos * (1 + escanios);
        if (izq != der) return izq < der;              // menor coeficiente
        if (votos != o.votos) return votos < o.votos;  // menos votos
        return orden > o.orden;                        // aparece despues
    }
};

bool resuelveCaso() {
    int candidaturas, escanios;
	cin >> candidaturas >> escanios;

	// caso de finalizacion
    if (candidaturas == 0 && escanios == 0) return false;

	priority_queue<Candidatura> cola;

	//procesamos todas las candidaturas y las metemos en la cola de maximos
    for(int i = 0; i < candidaturas; ++i) {
        long long votos;
        cin >> votos;
		// el primer coeficiente es el numero de votos
		Candidatura c = { votos, 0, i };
        cola.push(c);
	}

	// asignamos los escanios a las candidaturas con mayor coeficiente
    for (int i = 0; i < escanios; ++i) {
        Candidatura c = cola.top(); cola.pop();
        ++c.escanios;
		cola.push(c);
    }

	//escribimos los resultados en orden de entrada
    vector<int> res(candidaturas);
    while (!cola.empty()) {
        res[cola.top().orden] = cola.top().escanios;
        cola.pop();
    }
    for (int i = 0; i < candidaturas; ++i)
        cout << (i > 0 ? " " : "") << res[i];
    cout << '\n';

    return true;
}   

int main()
{
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}