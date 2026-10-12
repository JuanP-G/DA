// =====================================================================
// Acepta el Reto #279 - Grafo bipartito
// https://aceptaelreto.com/problem/statement.php?id=279
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 4-Grafos no dirigidos/EJ_04-7/EJ_04-7.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
// =====================================================================

#include <iostream>
#include <vector>
// ---------- Grafo.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/*
 * Implementacion de grafos no dirigidos.
 * Copyright (c) 2020  Alberto Verdejo
 *
 */

#ifndef GRAFO_H_
#define GRAFO_H_

#include <iostream>
#include <vector>
#include <iostream>
#include <stdexcept>

using Adys = std::vector<int>;  // lista de adyacentes a un vertice

class Grafo {
private:
    int _V;  // numero de vertices
    int _A;  // numero de aristas
    std::vector<Adys> _ady;  // vector de listas de adyacentes
public:

    /** Crea un grafo con V vertices */
    Grafo(int V) : _V(V), _A(0), _ady(_V) {}

    /**
     * Crea un grafo a partir de los datos en el flujo de entrada (si puede).
     * primer es el indice del primer vertice del grafo en el entrada.
     */
    Grafo(std::istream& flujo, int primer = 0) : _A(0) {
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

    /** Devuelve el numero de vertices del grafo. */
    int V() const { return _V; }

    /** Devuelve el numero de aristas del grafo. */
    int A() const { return _A; }

    /**
     * Anade la arista v-w al grafo.
     * @throws domain_error si algun vertice no existe
     */
    void ponArista(int v, int w) {
        if (v < 0 || v >= _V || w < 0 || w >= _V)
            throw std::domain_error("Vertice inexistente");
        ++_A;
        _ady[v].push_back(w);
        _ady[w].push_back(v);
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
inline std::ostream& operator<<(std::ostream& o, Grafo const& g) {
    g.print(o);
    return o;
}

#endif /* GRAFO_H_ */
// ---------- fin de Grafo.h ----------

using namespace std;

/*
    Grafo bipartito

    Vertices --> 1 <= V <= 100
    Aristas  --> A (vertices de 0 a V-1, sin lazos ni repetidas)
    Entrada: V en una linea y A en la siguiente --> justo lo que lee Grafo(cin)
*/

/*
    PLANTEAMIENTO
    Bipartito = se puede colorear con 2 colores sin que una arista
    una dos vertices del mismo color.

    Idea: el color de un vertice OBLIGA el color de sus vecinos (el contrario).
    Asi que hago un dfs coloreando: al vertice de partida le doy un color
    cualquiera y a cada vecino nuevo el color contrario al de su padre.
    Si encuentro una arista v-w con w ya visitado y del MISMO color que v,
    hay conflicto --> no es bipartito (hay un ciclo de longitud impar).

    OJO: el grafo puede no ser conexo, asi que hay que lanzar el dfs desde
    cada vertice no visitado (cada componente se colorea por separado).

    Coste: O(V + A) por caso.
*/

class Bipartito {
public:
    Bipartito(Grafo const& g) : visit(g.V(), false), color(g.V(), false), bipar(true) {
        for (int v = 0; v < g.V() && bipar; ++v) {
            if (!visit[v]) {   // nueva componente: su primer vertice puede ir de cualquier color
                color[v] = false;
                dfs(g, v);
            }
        }
    }

    bool esBipartito() const { return bipar; }

private:
    vector<bool> visit;   // visit[v] = v ya tiene color asignado
    vector<bool> color;   // los dos colores: false / true
    bool bipar;

    void dfs(Grafo const& g, int v) {
        visit[v] = true;
        for (int w : g.ady(v)) {
            if (!bipar) return;   // ya sabemos la respuesta, no seguimos
            if (!visit[w]) {
                color[w] = !color[v];   // el vecino lleva el color contrario
                dfs(g, w);
            }
            else if (color[w] == color[v]) bipar = false;   // arista entre iguales
        }
    }
};

void resuelveCaso() {
    Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)

    Bipartito b(g);
    cout << (b.esBipartito() ? "SI" : "NO") << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();

    return 0;
}
