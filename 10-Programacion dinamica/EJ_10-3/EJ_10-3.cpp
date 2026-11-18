#include <iostream>
#include <vector>
#include <string>

using namespace std;

/*
    Esquivando las obras en los cruces

    Ciudad de N calles este-oeste y M calles norte-sur (1 <= N, M <= 50); cada cruce es '.'
    (libre) o 'X' (obras). Contar los caminos MAS CORTOS de la esquina noroeste (0, 0) a la
    sureste (N - 1, M - 1) que no pasan por obras (el resultado es siempre < 10^9).
*/

/*
    PLANTEAMIENTO (programacion dinamica: contar caminos en una cuadricula)
    Un camino de longitud minima solo avanza hacia el sur o hacia el este, asi que a un cruce
    (i, j) solo se llega desde el de arriba (i - 1, j) o desde el de la izquierda (i, j - 1):

        caminos(0, 0) = 1
        caminos(i, j) = 0                                      si (i, j) tiene obras
                      = caminos(i - 1, j) + caminos(i, j - 1)  si no (fuera de la ciudad vale 0)

    Se rellena por filas con un solo vector: caminos[j] ya tiene el valor de la fila de arriba
    y caminos[j - 1] el de la izquierda en la fila actual.

    Coste: O(N * M) en tiempo y O(M) en espacio por caso.
*/

void resuelveCaso() {
    int N, M;
    cin >> N >> M;
    vector<long long> caminos(M, 0);
    caminos[0] = 1;                       // la esquina noroeste nunca tiene obras
    for (int i = 0; i < N; ++i) {
        string fila;
        cin >> fila;
        for (int j = 0; j < M; ++j) {
            if (fila[j] == 'X') caminos[j] = 0;
            else if (j > 0) caminos[j] += caminos[j - 1];   // arriba + izquierda
        }
    }
    cout << caminos[M - 1] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
