#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "Grafo.h"

using namespace std;

/*
    Deteccion de manchas negras

    Filas, columnas --> 1 <= F, C <= 1.000
    Suma de F*C de todos los casos <= 4.000.000
    Ninguna mancha tiene mas de 50.000 pixeles
    '#' = pixel negro, '-' = pixel blanco
*/

/*
    PLANTEAMIENTO
    Modelo: cada pixel es un vertice. El pixel (i, j) es el vertice i*C + j
    (fila por fila, como se guarda una matriz en un vector).
    Dos pixeles NEGROS vecinos en horizontal o vertical se unen con una arista.
    Las diagonales NO cuentan (el enunciado lo avisa con las dos manchas que
    se tocan por una esquina).

    Una mancha = una COMPONENTE CONEXA formada por pixeles negros.
    Lo que piden: cuantas componentes hay (contando solo pixeles negros)
    y el tamano de la mayor --> igual que EJ_04-2, pero ademas contando.

    Para poner las aristas basta mirar, desde cada pixel negro, el de su
    DERECHA y el de ABAJO: la arista con el de la izquierda y el de arriba
    ya la puso ese otro pixel (si no, cada arista saldria dos veces).

    Los pixeles blancos quedan como vertices sueltos y el recorrido los salta.

    Coste: O(F*C) por caso (como mucho 2 aristas por pixel).
    El dfs recursivo baja como mucho 50.000 niveles (el tamano maximo de una
    mancha, que el enunciado garantiza justo para esto).
*/

class Manchas {
public:
    Manchas(Grafo const& g, vector<bool> const& negro) : visit(g.V(), false), num(0), maxim(0) {
        for (int v = 0; v < g.V(); ++v) {
            if (negro[v] && !visit[v]) {   // pixel negro sin mancha: empieza una nueva
                ++num;
                int tam = dfs(g, v);
                maxim = max(maxim, tam);
            }
        }
    }

    int numero() const { return num; }
    int mayor() const { return maxim; }

private:
    vector<bool> visit;   // visit[v] = el pixel v ya esta en alguna mancha
    int num;              // numero de manchas encontradas
    int maxim;            // tamano de la mayor

    // devuelve cuantos pixeles de la mancha de v se visitan desde v
    int dfs(Grafo const& g, int v) {
        visit[v] = true;
        int tam = 1;
        for (int w : g.ady(v))
            if (!visit[w]) tam += dfs(g, w);
        return tam;
    }
};

void resuelveCaso() {
    int F, C;
    cin >> F >> C;


    vector<string> bitmap(F);
    for (int i = 0; i < F; ++i) {
        cin >> bitmap[i];
    }

    Grafo g(F * C);
    vector<bool> negro(F * C, false);
    //Recorremos toda la matriz de caracteres para generar el nuevo grafo de pixeles negros
    for (int i = 0; i < F; ++i) {
        for (int j = 0; j < C; ++j) {
            //Si es un pixel negro la añadimos
            if (bitmap[i][j] == '#') {
                int v = i * C + j;
                negro[v] = true;
                //Miramos sus cercanas (derecha y abajo para no repetir como esta arriba explicado)
                if (j + 1 < C && bitmap[i][j + 1] == '#') g.ponArista(v, v + 1);   // derecha
                if (i + 1 < F && bitmap[i + 1][j] == '#') g.ponArista(v, v + C);   // abajo
            }
        }
    }

    Manchas m(g, negro);
    cout << m.numero() << ' ' << m.mayor() << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
