// =====================================================================
// Acepta el Reto #319 - La maquina calculadora
// https://aceptaelreto.com/problem/statement.php?id=319
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 5-Grafos dirigidos/EJ_05-1/EJ_05-1.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
// =====================================================================

#include <iostream>
#include <vector>
#include <queue>
// ---------- Digrafo.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/*
 * Implementacion de grafos dirigidos (digrafos).
 * Copyright (c) 2020  Alberto Verdejo
 *
 */

#ifndef DIGRAFO_H_
#define DIGRAFO_H_

#include <iostream>
#include <stdexcept>
#include <vector>

using Adys = std::vector<int>;  // lista de adyacentes a un vertice

class Digrafo {

    int _V;   // numero de vertices
    int _A;  // numero de aristas
    std::vector<Adys> _ady;   // vector de listas de adyacentes

public:

    /** Crea un grafo dirigido con V vertices */
    Digrafo(int V) : _V(V), _A(0), _ady(_V) {}

    /**
     * Crea un grafo dirigido a partir de los datos en el flujo de entrada (si puede).
     * primer es el indice del primer vertice del grafo en el entrada.
     */
    Digrafo(std::istream& flujo, int primer = 0) : _A(0) {
        flujo >> _V;
        if (!flujo) return;
        _ady.resize(_V);
        int E, v, w;
        flujo >> E;
        while (E--) {
            flujo >> v >> w;
            ponArista(v - primer, w - primer);
        }
    }

    /** Devuelve el numero de vertices del grafo */
    int V() const { return _V; }

    /** Devuelve el numero de aristas del grafo */
    int A() const { return _A; }

    /**
     * Anade la arista dirigida v-w al grafo.
     * @throws domain_error si algun vertice no existe
     */
    void ponArista(int v, int w) {
        if (v < 0 || v >= _V || w < 0 || w >= _V)
            throw std::domain_error("Vertice inexistente");
        ++_A;
        _ady[v].push_back(w);
    }


    /** Comprueba si hay arista de u a v. */
    bool hayArista(int u, int v) const {
        for (int w : _ady[u])
            if (w == v) return true;
        return false;
    }


    /**
     * Devuelve la lista de adyacencia de v.
     * @throws domain_error si v no existe
     */
    Adys const& ady(int v) const {
        if (v < 0 || v >= _V)
            throw std::domain_error("Vertice inexistente");
        return _ady[v];
    }


    /** Devuelve el grafo dirigido inverso. */
    Digrafo inverso() const {
        Digrafo inv(_V);
        for (int v = 0; v < _V; ++v) {
            for (int w : _ady[v]) {
                inv.ponArista(w, v);
            }
        }
        return inv;
    }


    /** Muestra el grafo en el stream de salida o (para depurar) */
    void print(std::ostream& o = std::cout) const {
        o << _V << " vertices, " << _A << " aristas\n";
        for (int v = 0; v < _V; ++v) {
            o << v << ": ";
            for (int w : _ady[v]) {
                o << w << " ";
            }
            o << "\n";
        }
    }

};

/** Para mostrar grafos por la salida estandar */
inline std::ostream& operator<<(std::ostream& o, Digrafo const& g) {
    g.print(o);
    return o;
}


#endif /* DIGRAFO_H_ */
// ---------- fin de Digrafo.h ----------

using namespace std;

/*
    La maquina calculadora

    Marcador de 4 digitos --> numeros 0..9.999
    Botones: +1, *2 y /3, todo modulo 10.000 y la division es entera
    Casos de prueba --> como mucho 2.000, cada uno con (inicial, final)
*/

/*
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
*/

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

void resuelveCaso(Digrafo const& g) {
    int inicial, final_;
    cin >> inicial >> final_;

    MaquinaCalculadora mc(g, inicial, final_);
    cout << mc.minimoPulsaciones() << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Digrafo g = construyeMaquina();   // una sola vez para todos los casos

    while (cin >> ws && cin.peek() != EOF) resuelveCaso(g);

    return 0;
}
