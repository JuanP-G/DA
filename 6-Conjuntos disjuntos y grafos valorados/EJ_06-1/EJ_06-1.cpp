#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <algorithm>
#include "ConjuntosDisjuntos.h"

using namespace std;

/*
    Petroleros hundidos

    Rejilla F x C (1 <= F, C <= 1.000), '-' mar y '#' petroleo
    Dos celdas negras son de la misma mancha si se llega de una a otra por celdas
    negras moviendose en 8 direcciones.
    Despues aparecen N (<= 100.000) celdas nuevas de petroleo, una a una.
    Salida: tamano de la mancha mas grande al principio y tras cada celda nueva.
*/

/*
    PLANTEAMIENTO
    Las celdas solo SE ANADEN, nunca se quitan: las manchas solo pueden crecer o
    fundirse, jamas partirse. Eso es exactamente lo que sabe hacer una particion
    de CONJUNTOS DISJUNTOS (solo sabe unir).

        elemento    = celda (i, j)  -->  numero i*C + j
        conjunto    = mancha
        unir(a, b)  = dos celdas negras vecinas (8 direcciones)
        cardinal(a) = tamano de la mancha de a

    anade(i, j): marca la celda como petroleo, la une con sus vecinas que ya sean
    petroleo y compara el tamano de SU mancha con el maximo. Como solo hay uniones,
    la unica mancha que puede haber cambiado es la de la celda nueva y el maximo
    nunca baja: no hace falta recorrer todos los conjuntos.

    La imagen inicial se procesa con la misma operacion: celda negra a celda negra.
    (Al llegar a una celda, las vecinas posteriores aun no estan marcadas, pero
    cuando se procesen ellas se uniran con esta: el resultado final es el mismo.)

    La rejilla es el grafo: no se construye ninguna lista de adyacencia.

    Coste: O(F*C + N) con la lg* de la particion practicamente constante.
*/

class Manchas {
public:
    Manchas(int filas, int columnas)
        : F(filas), C(columnas), petroleo(filas * columnas, false), cd(filas * columnas), mayor(0) {}

    // marca como petroleo la celda (i, j) (base 0) y actualiza la mancha mas grande
    void anade(int i, int j) {
        int celda = i * C + j;
        petroleo[celda] = true;
        for (int di = -1; di <= 1; ++di)
            for (int dj = -1; dj <= 1; ++dj) {
                if (di == 0 && dj == 0) continue;
                int a = i + di, b = j + dj;
                if (a < 0 || a >= F || b < 0 || b >= C) continue;
                if (petroleo[a * C + b]) cd.unir(celda, a * C + b);
            }
        mayor = max(mayor, cd.cardinal(celda));
    }

    int masGrande() const { return mayor; }

private:
    int F, C;
    vector<bool> petroleo;
    ConjuntosDisjuntos cd;
    int mayor;
};

void resuelveCaso() {
    int F, C;
    cin >> F >> C;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    Manchas m(F, C);
    string fila;
    for (int i = 0; i < F; ++i) {
        getline(cin, fila);
        for (int j = 0; j < C && j < (int)fila.size(); ++j)
            if (fila[j] == '#') m.anade(i, j);
    }

    cout << m.masGrande();
    int n; cin >> n;
    while (n--) {
        int f, c; cin >> f >> c;
        m.anade(f - 1, c - 1);
        cout << ' ' << m.masGrande();
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos; cin >> casos;
    while (casos--) resuelveCaso();

    return 0;
}
