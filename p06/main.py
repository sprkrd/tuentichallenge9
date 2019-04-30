#!/usr/bin/env python3


class PrefixTree:
    def __init__(self, word="", index=-1):
        self._index = index
        self._children = {}
        if word:
            self._children[word[0]] = PrefixTree(word[1:], index)

    def addWord(self, word, index):
        if word:
            try:
                self._children[word[0]].addWord(word[1:], index)
            except KeyError:
                self._children[word[0]] = PrefixTree(word[1:], index)

    def _str_indented(self, indent):
        s = str(self._index) + "\n"
        if self._children:
            s += " "*indent
        s += ("\n"+" "*indent).join(k+": "+v._str_indented(indent+2) for k,v in self._children.items())
        return s

    def __str__(self):
        return self._str_indented(0)


def findCharacterPrecedencies(alphabet, root):
    graph = {c:set() for c in alphabet}
    stack = [root]
    while stack:
        trie = stack.pop()
        for child in trie._children.values:
            stack.append(child)
        sorted_chars = sorted(trie._children, key=lambda char: trie._children[char]._index)
        for char_before, char_after in zip(sorted_chars, sorted_chars[1:]):
            graph[char_before].add(char_after)
    return graph


def main():
    N = int(input())
    for i in range(1, N+1):
        alphabet = set()
        trie = PrefixTree()
        M = int(input())
        for index in range(M):
            word = input()
            trie.addWord(word, index)
            alphabet.update(word)
        graph = {c:[] for c in alphabet}
        stack = [trie]
        while stack:


if __name__ == "__main__":
    main()

