#include <iostream>
#include <vector>
#include "Digrafo.h"

using namespace std;

/*
    Sistema de inecuaciones

    Variables    --> 1 <= N <= 10.000 (x1 .. xN)
    Inecuaciones --> 0 <= M <= 100.000, de la forma xi < xj (pueden repetirse)
    Salida: "SI v1 ... vN" con valores que cumplen todas, o "NO"
*/

/*
    PLANTEAMIENTO
    Grafo DIRIGIDO: un vertice por variable y una arista i --> j por cada
    inecuacion xi < xj ("xi tiene que ir antes, con un valor menor, que xj").

    - Si hay un CICLO  x1 < x2 < ... < x1  es imposible  --> NO.
    - Si no hay ciclos (DAG), hay un ORDEN TOPOLOGICO: todas las aristas van
      de un vertice a otro posterior. Dando a cada variable su POSICION en ese
      orden (1, 2, ..., N), toda arista i --> j cumple pos(i) < pos(j). --> SI.

    Orden topologico y ciclos en el mismo DFS (como en 05-3), con 3 estados:
        0 = sin visitar,  1 = en la pila,  2 = terminado
    Vecino en estado 1 --> ciclo. Orden topologico = postorden inverso.

    * Cualquier asignacion valida vale (el ejemplo da otra distinta).
    * Las variables sueltas tambien tienen posicion, asi que reciben valor.
    * Inecuaciones repetidas: aristas repetidas, no molestan.
    * Profundidad de la recursion <= N = 10.000.

    Coste: O(N + M) por caso.
*/

class Inecuaciones {
public:
    Inecuaciones(Digrafo const& g) : estado(g.V(), 0), valor(g.V()), hayCiclo(false) {
        for (int v = 0; v < g.V() && !hayCiclo; ++v)
            if (estado[v] == 0) dfs(g, v);
        // post esta en postorden: al reves es el orden topologico
        int n = (int)post.size();
        for (int i = 0; i < n; ++i)
            valor[post[i]] = n - i;        // posicion en el orden topologico (1..N)
    }

    bool posible() const { return !hayCiclo; }
    int valorDe(int v) const { return valor[v]; }

private:
    vector<int> estado;   // 0 = sin visitar, 1 = en la pila, 2 = terminado
    vector<int> post;     // vertices en el orden en que el DFS los termina
    vector<int> valor;    // valor asignado a cada variable
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
    // El constructor lee N, M y las M inecuaciones "i j" (xi < xj --> arista i --> j);
    // el 1 indica que las variables vienen numeradas desde 1 (resta 1 a cada vertice).
    Digrafo g(cin, 1);
    int n = g.V();

    Inecuaciones sis(g);
    if (!sis.posible()) {
        cout << "NO\n";
    }
    else {
        cout << "SI";
        for (int v = 0; v < n; ++v) cout << ' ' << sis.valorDe(v);
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
