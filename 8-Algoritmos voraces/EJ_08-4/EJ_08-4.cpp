
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

/*@ <answer>

 Maraton de cine de terror
 
 N peliculas (1 <= N <= 500.000), cada una con el dia D (1..100.000), la hora de comienzo
 HH:MM y la duracion en minutos (1..1.000.000). Entre pelicula y pelicula hacen falta 10
 minutos libres. Escribir el maximo numero de peliculas que se pueden ver enteras.

 PLANTEAMIENTO (voraz: seleccion de actividades)
 Cada pelicula es un intervalo de tiempo en minutos absolutos:
     inicio = (D * 24 + HH) * 60 + MM,   fin = inicio + duracion
 Los 10 minutos de descanso se suman al final: una pelicula se puede ver despues de otra si
     inicio >= finAnterior + 10
 
 Se ordenan las peliculas por hora de FIN y se va cogiendo cada una que sea compatible con
 la ultima elegida. Elegir la que acaba antes deja el maximo tiempo libre para las demas:
 cualquier solucion optima se puede cambiar para que empiece por ella sin perder peliculas.
 
 Coste: O(N log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

struct Peli {
    long long inicio, fin;
};

void resuelveCaso() {
    int N;
    cin >> N;
    vector<Peli> pelis(N);
    for (Peli& p : pelis) {
        long long dia, hh, mm, dur;
        char dosPuntos;
        cin >> dia >> hh >> dosPuntos >> mm >> dur;
        p.inicio = (dia * 24 + hh) * 60 + mm;
        p.fin = p.inicio + dur;
    }
    sort(pelis.begin(), pelis.end(), [](Peli const& a, Peli const& b) { return a.fin < b.fin; });

    const int DESCANSO = 10;
    int vistas = 0;
    long long libreDesde = -DESCANSO;  // la primera pelicula siempre se puede ver
    for (Peli const& p : pelis) {
        if (p.inicio >= libreDesde) {
            ++vistas;
            libreDesde = p.fin + DESCANSO;
        }
    }
    cout << vistas << '\n';
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
