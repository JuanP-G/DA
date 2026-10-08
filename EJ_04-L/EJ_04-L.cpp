#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <queue>
#include "Grafo.h"

#include <iostream>

/*
    Peaje a la sombra

    Intersecciones --> 3 <= N <= 20.000   (numeradas de 1 a N)
    Calles         --> 2 <= C <= 200.000  (sin lazos ni repetidas, grafo conexo)
    Casa de Alex A, casa de Lucas L y trabajo T (los tres distintos)
    Entrada: N C A L T y despues las C aristas (vertices 0..N-1)
*/

/*
    PLANTEAMIENTO
    Cada tramo de calle cuesta 1 euro, pero si Alex y Lucas van JUNTOS por un
    tramo solo lo paga uno. Asi que lo que hay que minimizar es el numero de
    tramos DISTINTOS que se recorren entre los dos.

    La forma de los caminos es siempre una "Y":
        A ---\
              m --- T      (de A y de L hasta m cada uno por su lado,
        L ---/              y de m hasta T juntos)
    Si se encuentran en el cruce m, el coste es
        dist(A, m) + dist(L, m) + dist(m, T)
    (el trozo m-T se paga una sola vez).

    Para cada m el mejor coste es esa suma con caminos MINIMOS, y la
    respuesta es el minimo sobre TODOS los vertices m.
    Casos extremos incluidos sin tratarlos aparte:
        m = T  --> cada uno va solo hasta el trabajo
        m = A  --> Lucas pasa por casa de Alex y siguen juntos (idem m = L)

    Necesito las tres distancias (dA, dL, dT) --> un BFS desde A, otro
    desde L y otro desde T.

    Coste: 3 BFS, O(N + C) en total.
*/

using namespace std;

class CaminosBFS {
public:
    CaminosBFS(Grafo const& g, int origen) : dist(g.V(), -1) {
        bfs(g, origen);
    }

    int distancia(int v) const { return dist[v]; }

private:
    vector<int> dist;   // dist[v] = saltos desde el origen (-1 = no alcanzado)
    int alcanzados;     // vertices a distancia <= ttl (incluido el origen)

    void bfs(Grafo const& g, int origen) {
        queue<int> q;
        dist[origen] = 0;
        q.push(origen);
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (int w : g.ady(v)) {
                if (dist[w] == -1) {        // primera vez que llegamos --> camino mas corto
                    dist[w] = dist[v] + 1;
                    q.push(w);
                }
            }
        }
    }
};

void resolverCaso() {
    int n, c, a, l, t;
    cin >> n >> c >> a >> l >> t;
	--a; --l; --t;   // -1: el grafo empieza en 0

	Grafo g(n);
    for (int i = 0; i < c; ++i) {
        int u, v; cin >> u >> v;
        g.ponArista(u - 1, v - 1);   // -1: el grafo empieza en 0   
    }

    CaminosBFS dA(g, a), dL(g, l), dT(g, t);   // distancias desde Alex, Lucas y el trabajo

    int mejor = dA.distancia(t) + dL.distancia(t);   // cada uno solo (caso m = T)
    for (int m = 0; m < n; ++m) {
        int coste = dA.distancia(m) + dL.distancia(m) + dT.distancia(m);
        mejor = min(mejor, coste);
    }
        
	cout << mejor << '\n';
}

int main(){
    ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int casos; cin >> casos;    
    while (casos--) resolverCaso();
    return 0;
}