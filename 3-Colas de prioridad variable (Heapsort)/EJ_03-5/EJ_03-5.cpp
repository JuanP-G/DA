
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 Tridente de temas candentes

 Eventos: C tema n (n citas nuevas), E tema n (expiran n) y TC (escribir los 3 temas con más citas
 vigentes; empate -> el de C más reciente; los de 0 citas no salen). Acaba con el fichero.

 PLANTEAMIENTO
 IndexPQ<Prio, Mejor> con índice = número de tema y prioridad = (citas, instante del último C).
 C y E hacen update. TC saca hasta 3 cimas con citas > 0, las escribe y las vuelve a meter.

 Coste: O(log T) por evento, con T el número de temas.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

struct Prio {
    int citas;     // citas vigentes del tema
    int ultimoC;   // instante (numero de evento) de su ultimo C
};

struct Mejor {
    bool operator()(Prio const& a, Prio const& b) const {
        if (a.citas != b.citas) return a.citas > b.citas;  // mas citas va antes
        return a.ultimoC > b.ultimoC;                      // empate: el mas reciente
    }
};

bool resuelveCaso() {
    int n;
    if (!(cin >> n)) return false;

    IndexPQ<Prio, Mejor> pq(n);
    unordered_map<string, int> indice;   // tema -> indice
    vector<string> nombre;               // indice -> tema

    for (int t = 0; t < n; ++t) {
        string tipo;
        cin >> tipo;
        if (tipo == "TC") {
            vector<IndexPQ<Prio, Mejor>::Par> podio;
            while (podio.size() < 3 && !pq.empty()
                && pq.top().prioridad.citas > 0) {
                podio.push_back(pq.top());
                pq.pop();
            }
            for (int k = 0; k < (int)podio.size(); ++k)
                cout << k + 1 << ' ' << nombre[podio[k].elem] << '\n';
            for (auto const& p : podio) pq.push(p.elem, p.prioridad);
        }
        else {
            string tema; int m;
            cin >> tema >> m;
            int idx;
            auto it = indice.find(tema);
            if (it == indice.end()) {            // tema nuevo
                idx = nombre.size();
                indice[tema] = idx;
                nombre.push_back(tema);
                pq.push(idx, { 0, -1 });
            }
            else idx = it->second;
            Prio p = pq.priority(idx);
            if (tipo == "C") { p.citas += m; p.ultimoC = t; }
            else p.citas -= m;
            pq.update(idx, p);
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
