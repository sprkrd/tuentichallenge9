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


def findCharacterPrecedencies(words):
    trie_root = PrefixTree()
    alphabet = set()
    for index, word in enumerate(words):
        trie_root.addWord(word, index)
        alphabet.update(word)
    graph = {c:set() for c in alphabet}
    stack = [trie_root]
    while stack:
        trie = stack.pop()
        sorted_chars = sorted(trie._children, key=lambda char: trie._children[char]._index)
        for char_before, char_after in zip(sorted_chars, sorted_chars[1:]):
            graph[char_before].add(char_after)
        for child in trie._children.values():
            stack.append(child)
    return graph


def findTopologicalOrder(graph):
    unmarked = set(graph.keys())
    order = []
    while unmarked:
        stack = [(next(iter(unmarked)), False)]
        while stack:
            node, expanded = stack.pop()
            if node not in unmarked:
                continue
            if expanded:
                order.append(node)
                unmarked.remove(node)
            else:
                stack.append((node, True))
                for successor in graph[node]:
                    stack.append((successor, False))
    order.reverse()
    return order


def isTopologicalOrderUnique(graph, order):
    for from_, to in zip(order,order[1:]):
        if to not in graph[from_]:
            return False
    return True


def main():
    N = int(input())
    for i in range(1, N+1):
        M = int(input())
        words = []
        for _ in range(M):
            words.append(input())
        graph = findCharacterPrecedencies(words)
        order = findTopologicalOrder(graph)
        print("Case #{}: ".format(i), end="")
        if isTopologicalOrderUnique(graph, order):
            print(" ".join(order))
        else:
            print("AMBIGUOUS")


if __name__ == "__main__":
    main()

