
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
using namespace std;

/*@ <answer>

 La ley D'Hondt

 Repartir N escaños entre C candidaturas por el método D'Hondt y escribir los escaños de cada una
 en el orden de la entrada. La entrada acaba con un caso 0 0.

 PLANTEAMIENTO
 Cola de máximos de candidaturas ordenada por coeficiente votos / (1 + escaños), después por votos
 y después por orden de entrada. N veces: se saca la cima, se le suma un escaño y vuelve a entrar.

 Coste: O(C + N log C) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

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
