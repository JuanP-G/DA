
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

 Cinemáticas digitales

 R escenas llegan en orden (minuto de envío, duración) a S estaciones iguales. Escribir el tiempo
 máximo que alguna escena espera antes de empezar. La entrada acaba con el fichero.

 PLANTEAMIENTO
 Cola de mínimos con el instante en que queda libre cada estación (al principio S ceros). Para cada
 escena: libre = top, inicio = max(libre, minuto), espera = inicio - minuto, y la estación queda
 ocupada hasta inicio + duración.

 Coste: O(S + R log S) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

//escenas de renderizado --> 𝟣 <= 𝘙 <= 𝟤.𝟢𝟢𝟢.𝟢𝟢0
//estaciones de renderizado--> 𝟣 <= 𝘛 <= 𝟣𝟢𝟢.𝟢𝟢0
bool resuelveCaso() {
	int escenas, estaciones;
	if (!(cin >> escenas >> estaciones)) return false;

	// cola de minimos de instantes de liberacion de estaciones
    priority_queue<long long, vector<long long>, greater<long long>> cola;
    for (int i = 0; i < estaciones; ++i)
        cola.push(0);        // todas libres en el instante 0

    long long maxT = 0;

    for (int i = 0; i < escenas; ++i) {
        long long minuto, tiempo;
		cin >> minuto >> tiempo;

		//cogemos la estacion que se liberara antes
        long long libre = cola.top(); cola.pop();
		// queremos entrar en el instante minuto, pero la estacion puede estar ocupada hasta libre
        long long inicio = max(libre, minuto);
		// ponemos el tiempo maximo de espera
		maxT = max(maxT, inicio - minuto);
		//volvemos a meter en la cola el instante en que se liberara la estacion
        cola.push(inicio + tiempo);
    }
    
    //sacammos el tiempo maximo de espera
	cout << maxT << '\n';
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
