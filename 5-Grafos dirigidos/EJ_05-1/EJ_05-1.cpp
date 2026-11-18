
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

#include "Digrafo.h"  // estructuras de datos de clase

/*@ <answer>

 La maquina calculadora

 Marcador de 4 digitos --> numeros 0..9.999
 Botones: +1, *2 y /3, todo modulo 10.000 y la division es entera
 Casos de prueba --> como mucho 2.000, cada uno con (inicial, final)

 PLANTEAMIENTO
 Grafo DIRIGIDO (clase Digrafo) con 10.000 vertices (lo que muestra el marcador):
     x --> (x + 1) mod 10000
     x --> (x * 2) mod 10000
     x --> x / 3                  (division entera)
 Minimo de pulsaciones = camino mas corto de inicial a final --> BFS.

 El grafo NO depende del caso (siempre es el mismo marcador): se construye
 UNA sola vez en main y se reutiliza en los 2.000 casos.

 Se ve que es dirigido: de 5.000 se llega a 0 con *2, pero de 0 no se llega
 a 5.000 con ningun boton directo.

 * En el 0, *2 y /3 dan 0: aristas que son lazos. No pasa nada, 0 ya
   esta visitado cuando se miran.
 * inicial == final --> 0 pulsaciones (dist[inicial] = 0).
 * Se corta el BFS al sacar el vertice final (el BFS ya le ha dado su
   distancia minima).
 * Siempre hay camino: con +1 se llega a cualquier numero.

 Coste: construir el grafo O(10.000) una vez; despues O(10.000 + 30.000)
 por caso, unas 8*10^7 operaciones como mucho con los 2.000 casos.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

const int MARCADOR = 10000;

class MaquinaCalculadora {
public:
    MaquinaCalculadora(Digrafo const& g, int inicial, int final_) : dist(g.V(), -1), pulsaciones(-1) {
        bfs(g, inicial, final_);
    }

    int minimoPulsaciones() const { return pulsaciones; }

private:
    vector<int> dist;   // dist[x] = pulsaciones minimas desde el inicial hasta x (-1 = sin visitar)
    int pulsaciones;

    void bfs(Digrafo const& g, int inicial, int final_) {
        queue<int> q;
        dist[inicial] = 0;

        q.push(inicial);
        while (!q.empty()) {
            int x = q.front(); q.pop();
            if (x == final_) { pulsaciones = dist[x]; return; }   // ya no hace falta seguir

            for (int y : g.ady(x)) {
                if (dist[y] == -1) {
                    dist[y] = dist[x] + 1;
                    q.push(y);
                }
            }
        }
    }
};

// el grafo de la maquina: cada numero tiene tres aristas, una por boton
Digrafo construyeMaquina() {
    Digrafo g(MARCADOR);
    for (int x = 0; x < MARCADOR; ++x) {
        g.ponArista(x, (x + 1) % MARCADOR);   // boton +1
        g.ponArista(x, (x * 2) % MARCADOR);   // boton *2
        g.ponArista(x, x / 3);                // boton /3 (division entera)
    }
    return g;
}

void resuelveCaso() {
    static const Digrafo g = construyeMaquina();   // se construye una sola vez, en la primera llamada
    int inicial, final_;
    cin >> inicial >> final_;

    MaquinaCalculadora mc(g, inicial, final_);
    cout << mc.minimoPulsaciones() << '\n';
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
