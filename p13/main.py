#!/usr/bin/env python3

from heapq import heappush, heappop
from itertools import combinations
import tqdm


class Character:
    def __init__(self, name, level, cost, skills):
        self.name = name
        self.level = level
        self.cost = cost
        self.skills = skills

    def __str__(self):
        return "<name:{},level:{},costs:{},skills:[{}]>".format(
                self.name, self.level, self.cost, ", ".join(self.skills))


def getAllSubsets(elements):
    for r in range(len(elements)+1):
        for comb in combinations(elements, r):
            yield frozenset(comb)


def getAllPartitions(elements, nsets):
    elements = list(elements)
    for i in range(nsets**len(elements)):
        partition = [set() for _ in range(nsets)]
        n = i
        for j in range(len(elements)):
            partition[n%nsets].add(elements[j])
            n = n//nsets
        yield [frozenset(s) for s in partition]


def readAlmanac():
    with open("almanac.data", "r") as f:
        C, F = map(int, f.readline().split())
        characters = []
        for _ in range(C):
            line_split = f.readline().split()
            name = line_split[0]
            level = int(line_split[1])
            cost = int(line_split[2])
            skills = frozenset(line_split[4:])
            characters.append(Character(name, level, cost, skills))
        fusions = {char.name: [] for char in characters}
        for _ in range(F):
            result, char0, char1 = f.readline().split()
            fusions[result].append((char0,char1))
    return characters, fusions


characters, fusions = readAlmanac()
char_index = {char.name: char for char in characters}


def getReachableCharactersSortedByLevel(root_char):
    reachable = set()
    stack = [root_char]
    while stack:
        top = stack.pop()
        if top in reachable:
            continue
        reachable.add(top)
        for char0,char1 in fusions[top]:
            stack.append(char0)
            stack.append(char1)
    return sorted((char_index[c] for c in reachable), key=lambda char: char.level)


inf = 999999999
def findMinimumGold(goal_char_name, goal_skills):
    minimum_gold = {}
    all_skill_subsets = list(getAllSubsets(goal_skills))
    all_skill_partitions = list(getAllPartitions(goal_skills, 3))
    reachable_characters = getReachableCharactersSortedByLevel(goal_char_name)
    for char in reachable_characters:
        for skill_subset in all_skill_subsets:
            minimum_gold[(char.name, skill_subset)] = inf
    for char in reachable_characters:
        char_skill_subsets = list(getAllSubsets(char.skills&goal_skills))
        for skill_subset in char_skill_subsets:
            minimum_gold[(char.name, skill_subset)] = char.cost
        for subchar_name0, subchar_name1 in fusions[char.name]:
            subchar0 = char_index[subchar_name0]
            subchar1 = char_index[subchar_name1]
            for skills0, skills1, _ in all_skill_partitions:
                cost0 = minimum_gold[(subchar_name0, skills0)]
                cost1 = minimum_gold[(subchar_name1, skills1)]
                for skill_subset in char_skill_subsets:
                    combined_skills = skill_subset|skills0|skills1
                    old_value = minimum_gold[(char.name, combined_skills)]
                    minimum_gold[(char.name, combined_skills)] = min(old_value, cost0+cost1)
    return minimum_gold[(goal_char_name,goal_skills)]


def main():
    N = int(input())
    for i in tqdm.trange(1,N+1):
        line = input().split()
        G = int(line[0])
        goal_char_name = line[1]
        goal_skills = frozenset(line[3:])
        minimum_gold = findMinimumGold(goal_char_name, goal_skills)
        print("Case #{}: {}".format(i, minimum_gold if minimum_gold <= G else "IMPOSSIBLE"))

if __name__ == "__main__":
    main()


