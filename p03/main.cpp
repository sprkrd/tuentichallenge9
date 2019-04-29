#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <algorithm>
using namespace std;

typedef tuple<int,int> Punch;

struct Paper {
  int W, H;
  string folds;
  vector<Punch> punches;
};

struct PunchTransform {
  int w0, w1, h0, h1;
  Punch operator()(const Punch& punch) {
    return Punch{w0+w1*get<0>(punch), h0+h1*get<1>(punch)};
  }
};

ostream& operator<<(ostream& out, const Paper& paper) {
  vector<string> matrix(paper.H, string(paper.W, 'x'));
  for (const Punch& punch : paper.punches)
    matrix[get<1>(punch)][get<0>(punch)] = 'o';
  bool first = true;
  for (const string& row : matrix) {
    if (not first) out << '\n';
    out << row;
    first = false;
  }
  return out;
}

void unfold(Paper& paper) {
  char fold = paper.folds[0];
  vector<Punch> new_punches(paper.punches.size()*2);
  PunchTransform transform1{0, 1, 0, 1}, transform2{0, 1, 0, 1};
  switch (fold) {
    case 'L':
      transform1 = PunchTransform{paper.W, 1, 0, 1};
      transform2 = PunchTransform{paper.W-1, -1, 0, 1};
      paper.W *= 2;
      break;
    case 'R':
      transform2 = PunchTransform{2*paper.W-1, -1, 0, 1};
      paper.W *= 2;
      break;
    case 'T':
      transform1 = PunchTransform{0, 1, paper.H, 1};
      transform2 = PunchTransform{0, 1, paper.H-1, -1};
      paper.H *= 2;
      break;
    case 'B':
      transform2 = PunchTransform{0, 1, 2*paper.H-1, -1};
      paper.H *= 2;
  }
  for (size_t i = 0; i < paper.punches.size(); ++i) {
    new_punches[2*i] = transform1(paper.punches[i]);
    new_punches[2*i+1] = transform2(paper.punches[i]);
  }
  paper.punches = move(new_punches);
  paper.folds = paper.folds.substr(1);
}

int main() {
  int N;
  cin >> N;
  for (int i = 1; i <= N; ++i) {
    Paper paper;
    int F, P;
    cin >> paper.W >> paper.H >> F >> P;
    paper.folds.resize(F);
    for (char& f : paper.folds)
      cin >> f;
    paper.punches.resize(P);
    for (Punch& punch : paper.punches)
      cin >> get<0>(punch) >> get<1>(punch);
    //cerr << paper << "\n\n";
    while (not paper.folds.empty()) {
      unfold(paper);
      //cerr << paper << "\n\n";
    }
    sort(paper.punches.begin(), paper.punches.end());
    cout << "Case #" << i << ":\n";
    for (const Punch& punch : paper.punches) {
      cout << get<0>(punch) << ' ' << get<1>(punch) << '\n';
    }
  }
}

