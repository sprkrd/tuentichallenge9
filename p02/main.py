#!/usr/bin/env python3

from collections import deque


def getTopologicalOrder(graph):
    """ Uses DFS to extract topological sort """
    topological_order = []
    marked = set()
    stack = [("Galactica", False)]
    while stack:
        planet, expanded = stack.pop()
        if planet in marked:
            continue
        if expanded:
            marked.add(planet)
            topological_order.append(planet)
        else:
            stack.append((planet, True))
            for successor in graph.get(planet, []):
                stack.append((successor, False))
    topological_order.reverse()
    return topological_order


def getNumberOfDifferentPaths(graph):
    """ Uses Dynamic Programming to find number of different paths to each
    node """
    topological_order = getTopologicalOrder(graph)
    number_of_different_paths = {planet: 0 for planet in topological_order}
    number_of_different_paths["Galactica"] = 1
    for planet in topological_order:
        for successor in graph.get(planet, []):
            number_of_different_paths[successor] += number_of_different_paths[planet]
    return number_of_different_paths["New Earth"]


def main():
    C = int(input())
    for i in range(1,C+1):
        P = int(input())
        graph = {}
        for _ in range(P):
            origin, tail = input().split(":")
            for destination in tail.split(","):
                try:
                    graph[origin].append(destination)
                except KeyError:
                    graph[origin] = [destination]
        print("Case #{}: {}".format(i, getNumberOfDifferentPaths(graph)))

if __name__ == "__main__":
    main()

