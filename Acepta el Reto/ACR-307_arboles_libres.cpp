// =====================================================================
// Acepta el Reto #307 - Arboles libres
// https://aceptaelreto.com/problem/statement.php?id=307
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 4-Grafos no dirigidos/EJ_04-1/EJ_04-1.cpp
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
    Arboles libres

    Vertices --> 1 <= V <= 10.000
    Aristas  --> 0 <= A <= 100.000
    Vertices numerados de 0 a V-1, sin lazos ni aristas repetidas
    Entrada: V en una linea y A en la siguiente --> justo lo que lee Grafo(cin)
*/

/*
    PLANTEAMIENTO
    Arbol libre = grafo ACICLICO y CONEXO.

    Propiedad clave de los arboles: un grafo con V vertices es un arbol
    si cumple DOS de estas tres cosas (y entonces cumple la tercera):
        - es conexo
        - es aciclico
        - tiene exactamente V-1 aristas
    Asi que no hace falta buscar ciclos: basta con mirar que A == V-1
    y que un recorrido (DFS) desde cualquier vertice llega a los V.

    Coste: O(V + A) por caso (el DFS visita cada vertice y arista una vez).

    Nota: el dfs recursivo puede llegar a profundidad V (hasta 10.000).
    Un caso enorme podria desbordar la pila.
*/

class ArbolLibre {
public:
    ArbolLibre(Grafo const& g) : visit(g.V(), false), alcanzados(0) {
        dfs(g, 0);   // V >= 1, asi que el vertice 0 siempre existe
        bool conexo = (alcanzados == g.V());
        // un grafo es un arbol libre si es conexo y tiene V-1 aristas
        arbol = conexo && g.A() == g.V() - 1;
    }

    bool esArbol() const { return arbol; }

private:
    vector<bool> visit;   // visit[v] = el dfs ya ha pasado por v
    int alcanzados;       // cuantos vertices ha visitado el dfs
    bool arbol;

    // recorrido en profundidad: marca v y sigue por los adyacentes sin visitar
    void dfs(Grafo const& g, int v) {
        visit[v] = true;
        ++alcanzados;
        //recorre todos los adyacentes a v
        for (int w : g.ady(v))
            //si w no ha sido visitado, lo visita
            if (!visit[w]) dfs(g, w);
    }
};

void resuelveCaso() {
    Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)

    ArbolLibre al(g);
    cout << (al.esArbol() ? "SI" : "NO") << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();

    return 0;
}
