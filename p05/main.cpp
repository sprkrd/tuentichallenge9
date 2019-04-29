#include <iostream>
#include <string>
#include <algorithm>
#include <array>
using namespace std;

struct Vec2i {
  int x, y;
  Vec2i operator-(const Vec2i& other) const {
    return Vec2i{x-other.x, y-other.y};
  }
};

class TypewriterLayout {
  public:
    static const TypewriterLayout& getInstance() {
      static const TypewriterLayout instance;
      return instance;
    }

    // accessor with wrap-around
    char operator()(const Vec2i& vec) const {
      int x = ( vec.x%10 + 10 )%10;
      int y = ( vec.y%4 + 4 )%4;
      return _layout[y][x];
    }

    Vec2i getPositionOf(char c) const {
      return _inverse_map[c];
    }

  private:
    TypewriterLayout() : _layout{"1234567890", 
                                 "QWERTYUIOP",
                                 "ASDFGHJKL;",
                                 "ZXCVBNM,.-"} {
      for (int row = 0; row < 4; ++row) {
        for (int col = 0; col < 10; ++col)
          _inverse_map[_layout[row][col]] = {col, row};
      }
    }

    array<const char*, 4> _layout;
    array<Vec2i, 128> _inverse_map;
};

int main() {
  const TypewriterLayout& layout = TypewriterLayout::getInstance();
  int N;
  cin >> N;
  for (int i = 1; i <= N; ++i) {
    char sender;
    cin >> sender; cin.ignore();
    string encoded_message, decoded_message;
    getline(cin, encoded_message);
    decoded_message.reserve(encoded_message.size());
    auto senderPos = layout.getPositionOf(sender);
    auto targetPos = layout.getPositionOf(encoded_message.back());
    auto offset = targetPos - senderPos;
    transform(encoded_message.begin(), encoded_message.end(),
        back_inserter(decoded_message), [&](char c) {
      return c == ' '? c : layout(layout.getPositionOf(c)-offset);
    });
    cout << "Case #" << i << ": " << decoded_message << endl;
  }
}

