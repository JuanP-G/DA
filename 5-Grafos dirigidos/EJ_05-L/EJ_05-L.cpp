#include <iostream>
#include <vector>
#include "Digrafo.h"

using namespace std;

/*
    El Necronomicon de la informatica

    Programa oscuro de L instrucciones (1 <= L <= 10.000):
        A    --> aritmetica o asignacion (pasa a la siguiente)
        J N  --> salta a la instruccion N
        C N  --> salta a la N O pasa a la siguiente (no se puede predecir)
    Empieza en la 1 y termina al llegar detras de la ultima.
    Salida: SIEMPRE (todas las ejecuciones terminan), NUNCA (ninguna termina)
            o A VECES (unas si y otras no).
*/

/*
    PLANTEAMIENTO
    Digrafo con L + 1 vertices: la instruccion i es el vertice i - 1 y el vertice L
    es "el programa ha terminado". Cada ejecucion posible es un camino desde el 0:

        A       -->  arista  i - 1 --> i
        J N     -->  arista  i - 1 --> N - 1
        C N     -->  las DOS aristas  i - 1 --> i  y  i - 1 --> N - 1

    Todos los vertices tienen sucesores salvo el final, asi que un camino
    solo se acaba al llegar al vertice L; si no, sigue para siempre.
    Un unico DFS desde el 0 responde a todo:

    * NUNCA:    el vertice L NO es alcanzable desde el 0.
    * SIEMPRE:  no hay ningun CICLO alcanzable desde el 0 (sin ciclos todos los
                caminos son finitos y acaban en L, y L si es alcanzable).
    * A VECES:  L es alcanzable y ademas hay un ciclo alcanzable (se puede dar
                vueltas al ciclo para siempre o salir hacia L).

    Un salto hacia atras NO es un ciclo si no se puede volver a el (ejemplo 2).
    Los ciclos que no se alcanzan desde la instruccion 1 no cuentan.

    Coste: O(L) por caso (cada instruccion aporta como mucho 2 aristas).
*/

class ProgramaOscuro {
public:
    ProgramaOscuro(Digrafo const& g) : estado(g.V(), 0), hayCiclo(false) {
        dfs(g, 0);                          // solo lo que se alcanza desde la instruccion 1
        alcanzaFin = (estado[g.V() - 1] != 0);
    }
    bool terminaAlgunaVez() const { return alcanzaFin; }
    bool puedeNoTerminar() const { return hayCiclo; }

private:
    vector<int> estado;    // 0 sin visitar, 1 en la pila (camino actual), 2 terminado
    bool hayCiclo;
    bool alcanzaFin;

    void dfs(Digrafo const& g, int v) {
        estado[v] = 1;
        for (int w : g.ady(v)) {
            if (estado[w] == 1) hayCiclo = true;      // vuelve a un vertice de la pila
            else if (estado[w] == 0) dfs(g, w);
        }
        estado[v] = 2;
    }
};

void resuelveCaso() {
    int L;
    cin >> L;
    Digrafo g(L + 1);                       // vertice L: el programa ha terminado
    for (int i = 0; i < L; ++i) {           // instruccion i + 1  <-->  vertice i
        char tipo;
        cin >> tipo;
        if (tipo == 'A') {
            g.ponArista(i, i + 1);
        } else {
            int destino;
            cin >> destino;
            g.ponArista(i, destino - 1);    // el salto
            if (tipo == 'C') g.ponArista(i, i + 1);   // y, si es condicional, seguir
        }
    }

    ProgramaOscuro p(g);
    if (!p.terminaAlgunaVez()) cout << "NUNCA\n";
    else if (!p.puedeNoTerminar()) cout << "SIEMPRE\n";
    else cout << "A VECES\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
