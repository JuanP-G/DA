#include <iostream>
#include <vector>
#include <algorithm>
#include "Digrafo.h"

using namespace std;

/*
    Ordenando tareas

    Tareas      --> 1 <= N <= 10.000   (numeradas de 1 a N)
    Dependencias --> 0 <= M <= 100.000, "A antes que B" (A != B)
    Salida: un orden valido (cualquiera) o Imposible
*/

/*
    PLANTEAMIENTO
    Grafo DIRIGIDO: una arista A --> B significa "A tiene que hacerse antes que B".
    Un orden valido de las tareas es un ORDEN TOPOLOGICO del grafo; existe
    si y solo si el grafo NO tiene ciclos (si no, ninguna tarea del ciclo
    puede empezar: Imposible).

    Orden topologico con DFS:
        orden topologico = postorden inverso
    Cuando el DFS termina un vertice v, ya ha terminado todo lo que depende
    de v (sus sucesores), asi que v va ANTES que todos ellos: basta ir
    metiendo los vertices en una lista al terminar y darle la vuelta al final.

    Deteccion de ciclos en el mismo DFS: cada vertice tiene 3 estados
        0 = sin visitar,  1 = en la pila del DFS (se esta explorando),  2 = terminado
    Si desde v veo un vecino w en estado 1, w es un ANTECESOR de v en el
    recorrido y v --> w cierra un ciclo --> Imposible.
    (Ver un vecino en estado 2 es normal: ya terminado, no hay ciclo.)

    * Hay muchos ordenes validos; el problema acepta cualquiera.
    * Profundidad de la recursion <= N = 10.000, no hay problema de pila.

    Coste: O(N + M).
*/

class OrdenTopologico {
public:
    OrdenTopologico(Digrafo const& g) : estado(g.V(), 0), hayCiclo(false) {
        for (int v = 0; v < g.V() && !hayCiclo; ++v)
            if (estado[v] == 0) dfs(g, v);
        reverse(post.begin(), post.end());   // postorden inverso = orden topologico
    }

    bool posible() const { return !hayCiclo; }
    vector<int> const& orden() const { return post; }

private:
    vector<int> estado;   // 0 = sin visitar, 1 = en la pila, 2 = terminado
    vector<int> post;     // vertices en el orden en que el DFS los termina
    bool hayCiclo;

    void dfs(Digrafo const& g, int v) {
        estado[v] = 1;
        for (int w : g.ady(v)) {
            if (hayCiclo) return;
            if (estado[w] == 1) hayCiclo = true;        // w sigue en la pila: ciclo
            else if (estado[w] == 0) dfs(g, w);
        }
        estado[v] = 2;
        post.push_back(v);
    }
};

void resuelveCaso() {
    int n, m;
    cin >> n >> m;
    Digrafo g(n);
    for (int i = 0; i < m; ++i) {
        int a, b; cin >> a >> b;
        g.ponArista(a - 1, b - 1);   // a antes que b
    }

    OrdenTopologico ot(g);
    if (!ot.posible()) {
        cout << "Imposible\n";
    }
    else {
        bool primero = true;
        for (int v : ot.orden()) {
            if (!primero) cout << ' ';
            cout << v + 1;
            primero = false;
        }
        cout << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
