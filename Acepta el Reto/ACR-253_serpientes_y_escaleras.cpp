// =====================================================================
// Acepta el Reto #253 - Haciendo trampas en Serpientes y Escaleras
// https://aceptaelreto.com/problem/statement.php?id=253
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 5-Grafos dirigidos/EJ_05-5/EJ_05-5.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - la entrada termina con la linea `0 0 0 0`
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
    Haciendo trampas en Serpientes y Escaleras

    Tablero  --> N x N casillas (2 <= N <= 100), numeradas de 1 a N*N
    Dado     --> caras de 1 a K (K <= N), y podemos ELEGIR la cara
    S serpientes y E escaleras: "origen destino"
    Salida: minimo numero de tiradas para llegar de la casilla 1 a la N*N
*/

/*
    PLANTEAMIENTO
    Grafo DIRIGIDO: un vertice por casilla (casilla c --> vertice c - 1).
    Desde la casilla v, una tirada d (1..K) lleva a v + d, y si ahi empieza
    una serpiente o una escalera, la ficha acaba en su otro extremo:

        v --> destino(v + d)      para d = 1..K,  v + d <= N*N

    destino[c] = c, salvo en el origen de una serpiente o escalera.
    Cada arista es UNA tirada, asi que el minimo de tiradas es el camino
    mas corto (en aristas) de 0 a N*N - 1 --> BFS.

    * Da igual que la numeracion del tablero vaya en zigzag: solo importa
      el numero de cada casilla.
    * Las serpientes y las escaleras se tratan igual (un salto obligatorio).
    * El enunciado garantiza que la ultima casilla es alcanzable.
    * BFS parando al sacar la ultima casilla.

    Coste: O(N^2 * K) por caso (N^2 vertices, K aristas cada uno).
*/

class Tiradas {
public:
	// minimo de tiradas desde s a v (-1 si no se llega)
    Tiradas(Digrafo const& g, int s) : dist(g.V(), -1) {
        bfs(g, s);
    }
    int distancia(int v) const { return dist[v]; }

private:
    vector<int> dist;   // dist[v] = minimo de tiradas de s a v (-1 si no se llega)

    void bfs(Digrafo const& g, int s) {
        int fin = g.V() - 1;
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            if (v == fin) return;          // ya tenemos su distancia minima
            for (int w : g.ady(v)) {
                if (dist[w] == -1) {
                    dist[w] = dist[v] + 1;
                    q.push(w);
                }
            }
        }
    }
};

bool resuelveCaso() {
    int N, K, S, E;
    if (!(cin >> N >> K >> S >> E) || N == 0) return false;

	// Generamos el grafo con N*N vertices (casillas)
    int casillas = N * N;
    Digrafo g(casillas);

	// destino[c] = casilla a la que se llega desde c (c - 1 en el grafo)
    vector<int> destino(casillas);
    for (int c = 0; c < casillas; ++c) destino[c] = c;
    for (int i = 0; i < S + E; ++i) {      // serpientes y escaleras: igual
        int a, b; cin >> a >> b;
        destino[a - 1] = b - 1;
    }

	//Ahora generamos las aristas
    for (int v = 0; v < casillas; ++v)
		// desde la casilla v, tirando un d (1..K) se llega a destino[v + d]
        for (int d = 1; d <= K && v + d < casillas; ++d)
            g.ponArista(v, destino[v + d]);   // tirar un d desde v

    Tiradas t(g, 0);
    cout << t.distancia(casillas - 1) << '\n';
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());

    return 0;
}
