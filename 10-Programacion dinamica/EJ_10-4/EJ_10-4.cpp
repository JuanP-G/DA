#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/*
    ¿Por donde hay que subir?

    Tablero N x N (3 <= N <= 1.000) con numeros 1..10.000. Se empieza en una casilla de la ultima
    fila y se sube hasta la primera; en cada paso se va a una de las tres casillas de la fila de
    encima (en vertical o en diagonal) sin salirse. Escribir la suma maxima y la columna (1..N)
    de la ultima fila por la que hay que empezar (la de mas a la izquierda si hay varias).
*/

/*
    PLANTEAMIENTO (programacion dinamica)
        mejor(i, j) = suma maxima de un recorrido que empieza en (i, j) y sube hasta la fila 1

        mejor(1, j) = t(1, j)
        mejor(i, j) = t(i, j) + max( mejor(i - 1, j - 1), mejor(i - 1, j), mejor(i - 1, j + 1) )
                      (solo las columnas que existen)

    La respuesta es el maximo de mejor(N, j); con '>' estricto al recorrer j de izquierda a
    derecha, en caso de empate se queda la columna de mas a la izquierda.

    Se rellena fila a fila guardando solo la fila anterior.

    Coste: O(N^2) en tiempo y O(N) en espacio por caso (la suma maxima es <= 10^7: cabe en int).
*/

void resuelveCaso() {
    int N;
    cin >> N;
    vector<int> anterior(N), actual(N);
    for (int j = 0; j < N; ++j) cin >> anterior[j];           // fila 1
    for (int i = 1; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            int t;
            cin >> t;
            int mejorArriba = anterior[j];
            if (j > 0) mejorArriba = max(mejorArriba, anterior[j - 1]);
            if (j + 1 < N) mejorArriba = max(mejorArriba, anterior[j + 1]);
            actual[j] = t + mejorArriba;
        }
        swap(anterior, actual);
    }

    int col = 0;
    for (int j = 1; j < N; ++j)
        if (anterior[j] > anterior[col]) col = j;
    cout << anterior[col] << ' ' << col + 1 << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
