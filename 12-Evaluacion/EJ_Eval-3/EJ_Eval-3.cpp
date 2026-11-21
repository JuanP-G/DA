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

 Cine romantico a raudales

 N peliculas (1..300.000) con dia D, hora HH:MM y duracion (1..10^6 minutos). Entre una
 pelicula y la siguiente hacen falta 10 minutos libres. Maximo de minutos viendo peliculas.

 PLANTEAMIENTO (programacion dinamica sobre intervalos ordenados + busqueda binaria)
 Cada pelicula es un intervalo en minutos absolutos: empieza en (D-1)*1440 + HH*60 + MM y
 acaba en inicio + duracion. Se ordenan por inicio.
     minutos(i) = maximo de minutos viendo peliculas elegidas entre la i y las siguientes
     minutos(N) = 0
     minutos(i) = max( minutos(i+1),                      // no ver la i
                       duracion_i + minutos(sig(i)) )      // verla
 sig(i) = la primera pelicula que empieza en fin_i + 10 o despues (lower_bound: estan
 ordenadas por inicio). Respuesta: minutos(0).
 No vale un voraz: no se maximiza el numero de peliculas sino el tiempo (ejemplo 2).
 Las peliculas vistas no se solapan: el total es como mucho 100.000*1440 + 10^6, que cabe
 en int; se usa long long para los minutos absolutos por comodidad.

 Coste: O(N log N) por caso; espacio O(N).

 @ </answer> */

// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

struct Pelicula {
    long long ini, fin;
};

bool operator<(Pelicula const& a, Pelicula const& b) { return a.ini < b.ini; }

void resuelveCaso() {
    int N;
    cin >> N;
    vector<Pelicula> p(N);
    for (int i = 0; i < N; ++i) {
        long long d, dur;
        int hh, mm;
        char dos;
        cin >> d >> hh >> dos >> mm >> dur;
        p[i].ini = (d - 1) * 1440 + hh * 60 + mm;
        p[i].fin = p[i].ini + dur;
    }
    sort(p.begin(), p.end());
    vector<long long> inicios(N);
    for (int i = 0; i < N; ++i) inicios[i] = p[i].ini;

    vector<long long> minutos(N + 1, 0);         // minutos[i]: lo mejor desde la pelicula i
    for (int i = N - 1; i >= 0; --i) {
        int sig = lower_bound(inicios.begin(), inicios.end(), p[i].fin + 10) - inicios.begin();
        minutos[i] = max(minutos[i + 1], (p[i].fin - p[i].ini) + minutos[sig]);
    }
    cout << minutos[0] << '\n';
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
