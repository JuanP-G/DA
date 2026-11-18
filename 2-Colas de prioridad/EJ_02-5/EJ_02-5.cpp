
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

 Ordenando a los pacientes en urgencias

 Eventos: I nombre gravedad (ingreso) y A (atender). En cada A escribir el paciente más grave y,
 a igualdad, el que más lleva esperando. Tras cada caso, ---. Acaba con un caso con 0 eventos.

 PLANTEAMIENTO
 Cola de máximos de Paciente(nombre, gravedad, orden de llegada): operator< da menos prioridad al
 de menor gravedad y, si empatan, al que llegó después. I hace push; A escribe top() y hace pop().

 Coste: O(n log n) por caso.

 Casos --> 1 <= N <= 200.000  (2*10^5)
 Gravedad --> 1 <= N <= 1.000.000   (10^0)
 I (Ingreso) --> Los nombres son strings de 1 a 20 caracteres, sin espacios
 A (Atencion) --> No hay atencion si no hay pacientes

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

struct Paciente {
    string nombre;
    int gravedad;
    int orden; // orden de llegada

	// primero por gravedad, y a igualdad, por orden de llegada
    bool operator<(const Paciente& o) const {
        if (gravedad != o.gravedad) return gravedad < o.gravedad;
        return orden > o.orden;
	}
};

bool resuelveCaso() {
    int casos;
    if(!(cin >> casos) || casos == 0) return false;
    priority_queue<Paciente> cola;

    for (int i = 0; i < casos; ++i) {
        char tipo;
		cin >> tipo;
        if (tipo == 'I') {
            string nombre;
			cin >> nombre;
			int gravedad;
            cin >> gravedad;
            cola.push({ nombre, gravedad, i });
        }
        else if (tipo == 'A') {
            if (!cola.empty()) {
                cout << cola.top().nombre << '\n';
                cola.pop();
            }
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
