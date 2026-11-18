
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 La batalla por las audiencias

 Audiencias iniciales de C canales y actualizaciones por minuto. Decir cuántos minutos ha sido líder
 cada canal en [0, D), de más a menos (empate -> canal menor).

 PLANTEAMIENTO
 IndexPQ de máximos con índice = canal y prioridad = (audiencia, canal). En cada actualización, el
 líder actual suma los minutos desde la anterior y después se aplican los cambios con update. Al
 final el líder suma el último tramo; se ordena y se escriben los que tienen minutos.

 Coste: O((C + U) log C + C log C), con U el número de cambios de audiencia.

 1ª linea

 Duracion D (minutos de la franja) -->  1 ≤ D ≤ 10^9
 Numero C de canales --> 1 ≤ C ≤ 2*10^5
 Numerp N de actualizciones --> 1 ≤ N ≤ min(D − 1, 2*10^5)
 --------------------------------------
 2ªlinea

 C numeros de las audiencias en el minuto 0
 N lineas con las actualizaciones de audiencia
 ---------------------------------------
 xª linea
 minuto de la actualizacion --> 1 ≤ m ≤ D − 1
 numero de canales que cambian de audiencia
 ck es el canal que cambia de audiencia y ek es la nueva audiencia del canal ck

 D (duracion en minutos)   --> 1 <= D <= 10^9
 C (canales, del 1 al C)   --> 1 <= C <= 2*10^5
 N (actualizaciones)       --> 0 <= N <= min(D-1, 2*10^5)
 audiencias                --> 0 .. 10^6

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

struct Canales {
    int audiencia;
	int canal;

    bool operator>(Canales const& otro) const {
        if (audiencia != otro.audiencia) return audiencia > otro.audiencia;
        return canal < otro.canal; // En caso de empate, el canal con menor número es más prioritario
	}
};

void resuelveCaso() {
	int duracion, canales, actualizaciones;
    cin >> duracion >> canales >> actualizaciones;

	//Creamos e  inicializamos la cola de prioridad con los canales y sus audiencias iniciales
    // canales del 1 al C → hace falta sitio para el indice C (el 0 no se usa)
    IndexPQ<Canales, greater<Canales>> pq(canales + 1);
    //Ahora creamos el vector donde guardaremos los tiempo de audiencia maxima de cada canal
    vector<Canales> tiempos(canales);
    for(int i = 1; i <= canales; ++i) {
        int audiencia;
        cin >> audiencia;
        pq.push(i, {audiencia, i});
		//Inicializamos el vector de tiempos de maxima audiencia a 0
		tiempos[i - 1] = { 0, i }; //en este caso son minutos y canal
	}

	
	int tiempoAnterior = 0;
	//Ahora procesamos las actualizaciones de audiencia, actualizando la audiencia de cada canal y guardando el tiempo de maxima audiencia de cada canal
    for (int i = 0; i < actualizaciones; ++i) {
		int tiempoActual, canalesCambio;
        cin >> tiempoActual >> canalesCambio;

        // el lider hasta ahora suma los minutos transcurridos
		Canales lider = pq.top().prioridad;
		tiempos[lider.canal - 1].audiencia += tiempoActual - tiempoAnterior;

		//Ahora actualizamos las audiencias de los canales que han cambiado
        for (int j = 0; j < canalesCambio; ++j) {
			int canal, audiencia;
            cin >> canal >> audiencia;
			pq.update(canal, { audiencia, canal });
        }
		tiempoAnterior = tiempoActual;
    }

	//Ultimo tramo de la franja
    tiempos[pq.top().prioridad.canal - 1].audiencia += duracion - tiempoAnterior; //en realidad es el tiempo

    
	//Ordenamos el vector de mayor a menor audiencia y en caso de empate, por el canal con menor número
	std::sort(tiempos.begin(), tiempos.end(), greater<Canales>());
	//Y ahora los mostramos por pantalla
    for(vector<int>::size_type i = 0; i < tiempos.size(); ++i) {
        if (tiempos[i].audiencia > 0)
            cout << tiempos[i].canal << ' ' << tiempos[i].audiencia << '\n';
    }
    cout << "---\n";
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
