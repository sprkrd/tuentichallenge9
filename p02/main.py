#!/usr/bin/env python3

from collections import deque


def getNumberOfDifferentPaths(graph):
    npaths = {"Galactica": 1}
    queue = deque(["Galactica"])
    while q:
        planet = queue.popleft()

        # for destination 


def main():
    q = deque(["a","b","c"])
    print(q)
    while q:
        q.popleft()
        print(q)
    # C = int(input())
    # for i in range(1,C+1):
        # P = int(input())
        # graph = {}
        # for _ in range(P):
            # origin, tail = input().split(":")
            # for destination in tail.split(","):
                # try:
                    # graph[origin].append(destination)
                # except KeyError:
                    # graph[origin] = [destination]
        # print("Case #{}: {}".format(i, getNumberOfDifferentPaths(graph)))

if __name__ == "__main__":
    main()

