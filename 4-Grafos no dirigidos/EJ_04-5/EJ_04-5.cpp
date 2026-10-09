#include <iostream>
#include <vector>
#include <queue>
#include "Grafo.h"

using namespace std;

/*
    ¡Las noticias vuelan!

    Usuarios --> 1 <= N <= 100.000   (numerados de 1 a N)
    Grupos   --> 1 <= M <= 100.000   (cada uno con 0..N usuarios distintos)
    Suma de N de todos los casos <= 1.000.000, y lo mismo la suma de tamanos de grupo
*/

/*
    PLANTEAMIENTO
    Modelo: cada usuario es un vertice; dos usuarios estan unidos si
    comparten grupo. La noticia se extiende hasta que no queda ningun
    amigo sin enterarse --> llega a TODA la componente conexa del que
    la empieza (y solo a ella).
    Respuesta para el usuario i = tamano de la componente conexa de i.

    1) Construir el grafo. Lo directo es unir todos los pares de cada grupo,
       pero un grupo de k usuarios daria k*(k-1)/2 aristas (con k = 100.000
       son 5.000 millones). Truco: solo importa QUIEN esta conectado con
       quien, no por cuantas aristas, asi que basta unir a todos los del
       grupo con el primero (una "estrella"): k-1 aristas y el grupo sigue
       quedando en una sola componente.

    2) Recorrer cada componente una vez (no un recorrido por usuario, que
       seria cuadratico): para cada vertice sin visitar, recorro su
       componente, guardo en comp[v] su numero y en tam[] su tamano.
       Despues la respuesta de v es tam[comp[v]].

    3) Uso BFS (iterativo) en lugar de un dfs recursivo: una componente
       puede tener 100.000 vertices y la recursion tan profunda podria
       desbordar la pila. Para contar una componente da igual el orden.

    Coste: O(N + suma de tamanos de grupo) por caso.
*/

class TamComponentes {
public:
    TamComponentes(Grafo const& g) : comp(g.V(), -1) {
        for (int v = 0; v < g.V(); ++v) {
            if (comp[v] == -1) {   // v no pertenece aun a ninguna componente
                int c = tam.size();
				// recorro la componente de v, la marco con c y guardo su tamano
                tam.push_back(bfs(g, v, c));
            }
        }
    }

    // numero de usuarios en la componente de v
    int tamano(int v) const { return tam[comp[v]]; }

private:
    vector<int> comp;   // comp[v] = numero de componente de v (-1 = sin visitar)
    vector<int> tam;    // tam[c]  = numero de vertices de la componente c

    // marca con c todos los vertices de la componente de origen y devuelve cuantos son
    int bfs(Grafo const& g, int origen, int c) {
		// BFS iterativo
        queue<int> q;
        comp[origen] = c;
		// origen es el primer vertice de la componente c
        q.push(origen);
        int cuantos = 1;
		// recorro todos los vertices de la componente, marcandolos con c y contando cuantos son
        while (!q.empty()) {
            int v = q.front(); q.pop();
			// recorro todos los vecinos de v
            for (int w : g.ady(v)) {
                if (comp[w] == -1) {
                    comp[w] = c;
                    ++cuantos;
                    q.push(w);
                }
            }
        }
        return cuantos;
    }
};

void resuelveCaso() {
    int usuarios, grupos;
    cin >> usuarios >> grupos;

	// Construir el grafo: cada usuario es un vertice
    Grafo g(usuarios);
    for (int i = 0; i < grupos; ++i) {
        int k; cin >> k;
		// si el grupo tiene algun usuario, leo el primero y luego los demas
        if (k != 0) {
            int primero; cin >> primero;
            for (int j = 1; j < k; ++j) {
                int otro; cin >> otro;
                g.ponArista(primero - 1, otro - 1);   // estrella: todos con el primero
            }
        }
    }

	// recorrer las componentes conexas y contar su tamano
    TamComponentes tc(g);
    for (int v = 0; v < usuarios; ++v)
        cout << tc.tamano(v) << ' ';
	cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}