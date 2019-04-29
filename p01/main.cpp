#include <iostream>
using namespace std;

int main() {
  int C;
  cin >> C;
  for (int i = 1; i <= C; ++i) {
    int N, M;
    cin >> N >> M;
    cout << "Case #" << i << ": " << ( (N+1)/2 + (M+1)/2 ) << endl;
  }
}


