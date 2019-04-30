#include <algorithm>
#include <iostream>
#include <array>
#include <cstdint>
using namespace std;

typedef array<uint64_t,31> Array31u;

struct Fraction {
  uint64_t numerator, denominator;
  void simplify();
};

ostream& operator<<(ostream& out, const Fraction& fraction) {
  return out << fraction.numerator << '/' << fraction.denominator;
}

uint64_t greatestCommonDivisor(uint64_t a, uint64_t b) {
  if (a < b) swap(a,b);
  while (b) {
    uint64_t r = a%b;
    a = b;
    b = r;
  }
  return a;
}

void Fraction::simplify() {
  auto gcd = greatestCommonDivisor(numerator, denominator);
  numerator /= gcd;
  denominator /= gcd;
}

uint64_t leastCommonMultiple(uint64_t a, uint64_t b) {
  return a*( b/greatestCommonDivisor(a,b) );
}

template<typename Collection>
uint64_t leastCommonMultiple(const Collection& elements) {
  uint64_t result = 1;
  for (uint64_t el : elements)
    result = leastCommonMultiple(result, el);
  return result;
}

uint64_t findMinimumNumberOfRepetitions(const Array31u& occurrences) {
  Array31u minimumPerElement{1};
  for (uint64_t i = 1; i < 31; ++i)
    minimumPerElement[i] = occurrences[i]?
      leastCommonMultiple(i,occurrences[i]) : 1;
  return leastCommonMultiple(minimumPerElement);
}

Fraction findAverageOfCandiesPerPerson(const Array31u& occurrences) {
  uint64_t minimum_repetitions = findMinimumNumberOfRepetitions(occurrences);
  Fraction average{0,0};
  for (uint64_t i = 1; i < 31; ++i) {
    uint64_t n_candies = occurrences[i]*minimum_repetitions;
    uint64_t n_persons = ( occurrences[i]*minimum_repetitions )/i;
    average.numerator += n_candies;
    average.denominator += n_persons;
  }
  average.simplify();
  return average;
}

int main() {
  int C;
  cin >> C;
  for (int i = 1; i <= C; ++i) {
    Array31u occurrences{0};
    int N;
    cin >> N;
    for (int j = 0; j < N; ++j) {
      int M;
      cin >> M;
      occurrences[M] += 1;
    }
    auto average = findAverageOfCandiesPerPerson(occurrences);
    cout << "Case #" << i << ": " << average << endl;
  }
}

