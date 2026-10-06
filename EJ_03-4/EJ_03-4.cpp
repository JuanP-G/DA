#include <iostream>
#include <queue>
#include <vector>
#include <functional>
using namespace std;

bool resolverCaso() {
    int primero, parejas;
    cin >> primero >> parejas;

    if (primero == 0 && parejas == 0) return false;

    priority_queue<int> menores;                             // max-heap
    priority_queue<int, vector<int>, greater<int>> mayores;  // min-heap
    int lider = primero;

    for (int i = 0; i < parejas; ++i) {
        for (int j = 0; j < 2; ++j) {
            int edad; cin >> edad;

            if (edad < lider) menores.push(edad);
            else mayores.push(edad);
        }
        if (menores.size() > mayores.size()) {
            mayores.push(lider);
            lider = menores.top(); menores.pop();
        }
        else if (mayores.size() > menores.size()) {
            menores.push(lider);
            lider = mayores.top(); mayores.pop();
        }
        cout << lider << (i + 1 < parejas ? ' ' : '\n');
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resolverCaso());
    return 0;
}