#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

struct Vec2d {
  double x,y;

  static Vec2d fromPolar(double d, double theta) {
    return Vec2d{d*cos(theta), d*sin(theta)};
  }

  Vec2d operator-(const Vec2d& other) {
    return Vec2d{x-other.x, y-other.y};
  }

  double magnitude() {
    return sqrt(x*x+y*y);
  }
};

struct Moon {
  double d, r, t, u;

  Vec2d position(double time) const {
    return Vec2d::fromPolar(d, r+2*M_PI*time/t);
  }
};

struct World {
  vector<Moon> moons;
  int C;
  double R;

  vector<int> getSortedLoads(const vector<int>& traversal) const {
    vector<int> loads;
    for (int moon : traversal)
      loads.push_back(moons[moon].u);
    sort(loads.begin(), loads.end());
    return loads;
  }
};

struct State {
  const World* world;
  vector<int> visited_moons;
  double time, payload, remaining_range;

  double getDistanceFromShip(int moon, double dt = 0) const {
    if (visited_moons.empty())
      return world->moons[moon].d;
    auto ship_position = world->moons[visited_moons.back()].position(time+dt);
    return (world->moons[moon].position(time+dt)-ship_position).magnitude();
  }

  bool moonHasBeenVisited(int moon) const {
    auto it = find(visited_moons.begin(), visited_moons.end(), moon);
    return it != visited_moons.end();
  }

  bool canLoadAllMineral(int moon) const {
    return world->moons[moon].u <= world->C-payload;
  }

  bool isVisitable(int moon) const {
    if (moonHasBeenVisited(moon))
      return false; // the moon has already been visited
    if (getDistanceFromShip(moon)+world->moons[moon].d > remaining_range)
      return false; // not enough fuel to go to moon and back to base
    if (not canLoadAllMineral(moon))
      return false; // cannot load all the mineral
    return true;
  }

  vector<int> getVisitableMoons() const {
    vector<int> visitable_moons;
    for (size_t i = 0; i < world->moons.size(); ++i) {
      if (isVisitable(i))
        visitable_moons.push_back(i);
    }
    return visitable_moons;
  }

  void update(int next_moon) {
    // pre: can travel to this moon (i.e. argument comes from getVisitableMoons)
    double traveled_distance = getDistanceFromShip(next_moon);
    visited_moons.push_back(next_moon);
    time += 6;
    payload += world->moons[next_moon].u;
    remaining_range -= traveled_distance;
  }

  void undo() {
    // pre: visited_moons is not empty
    int last_moon = visited_moons.back();
    visited_moons.pop_back();
    time -= 6;
    payload -= world->moons[last_moon].u;
    remaining_range += getDistanceFromShip(last_moon);
  }
};


void dfs(State& current, State& best) {
  auto successors = current.getVisitableMoons();
  if (successors.empty()) {
    if (current.payload > best.payload)
      best = current;
  }
  else {
    for (int moon : successors) {
      current.update(moon);
      dfs(current, best);
      current.undo();
    }
  }
}

vector<int> optimizedMoonTraversal(const World& world) {
  State current{&world, {}, 0, 0, world.R};
  State best = current;
  dfs(current, best);
  return best.visited_moons;
}

ostream& operator<<(ostream& out, const vector<int>& v) {
  for (size_t i = 0; i < v.size(); ++i) {
    if (i > 0) out << ' ';
    out << v[i];
  }
  if (v.empty())
    out << "None";
  return out;
}

int main() {
  int N;
  cin >> N;
  for (int i = 1; i <= N; ++i) {
    int M;
    cin >> M;
    World world{vector<Moon>(M), 0, 0};
    for (int j = 0; j < M; ++j)
      cin >> world.moons[j].d;
    for (int j = 0; j < M; ++j)
      cin >> world.moons[j].r;
    for (int j = 0; j < M; ++j)
      cin >> world.moons[j].t;
    for (int j = 0; j < M; ++j)
      cin >> world.moons[j].u;
    cin >> world.C >> world.R;
    auto traversal = optimizedMoonTraversal(world);
    auto sorted_loads = world.getSortedLoads(traversal);
    cout << "Case #" << i << ": " << sorted_loads << endl;
  }
}

