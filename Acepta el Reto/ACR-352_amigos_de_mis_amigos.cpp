// =====================================================================
// Acepta el Reto #352 - Los amigos de mis amigos son mis amigos
// https://aceptaelreto.com/problem/statement.php?id=352
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 4-Grafos no dirigidos/EJ_04-2/EJ_04-2.cpp
// (no la edites a mano: se vuelve a generar).
// =====================================================================

#include <iostream>
#include <vector>
#include <algorithm>
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
    Los amigos de mis amigos son mis amigos

    Personas --> 1 <= N <= 20.000
    Parejas  --> 0 <= M <= 200.000
    Personas numeradas de 1 a N --> Grafo(cin, 1) les resta 1 (vertices 0..N-1)
    Una pareja puede repetirse --> no pasa nada: el dfs no visita dos veces
*/

/*
    PLANTEAMIENTO
    Modelo: cada persona es un vertice y cada amistad una arista.
    "Los amigos de mis amigos son mis amigos" significa que dos personas
    estan en el mismo grupo si hay un CAMINO entre ellas en el grafo.
    Es decir, un grupo de amigos = una COMPONENTE CONEXA.

    Lo que piden: el tamano de la componente conexa mas grande.
    Para cada vertice no visitado lanzo un dfs que devuelve cuantos
    vertices ha visitado (el tamano de esa componente) y me quedo
    con el maximo.

    Coste: O(N + M) por caso.

    Nota: el dfs recursivo puede llegar a profundidad N (hasta 20.000).
    En el juez no da problemas, pero en Visual Studio (pila de 1MB)
    un caso enorme podria desbordar la pila --> ver EJ_04-L, que usa BFS.
*/

class MaximaCompConexa {
public:
	// construye el objeto y calcula el tamano de la mayor componente conexa
    MaximaCompConexa(Grafo const& g) : visit(g.V(), false), maxim(0) {
        for (int v = 0; v < g.V(); ++v) {
            if (!visit[v]) {   // v empieza una componente nueva
                int tam = dfs(g, v);
                maxim = max(maxim, tam);
            }
        }
    }

    int maximo() const { return maxim; }

private:
    vector<bool> visit;   // visit[v] = ya contado en alguna componente
    int maxim;            // tamano de la mayor componente encontrada

    // devuelve el numero de vertices de la componente de v que aun no se habian visitado
    int dfs(Grafo const& g, int v) {
        visit[v] = true;
        int tam = 1;   // el propio v
        for (int w : g.ady(v))
            if (!visit[w]) tam += dfs(g, w);
        return tam;
    }
};

void resuelveCaso() {
    Grafo g(cin, 1);   // lee N, M y las M amistades (de 1 a N)

    MaximaCompConexa mcc(g);
    cout << mcc.maximo() << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
