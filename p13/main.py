#!/usr/bin/env python3

from heapq import heappush, heappop
import tqdm


class Character:
    def __init__(self, name, level, cost, skills):
        self.name = name
        self.level = level
        self.cost = cost
        self.skills = set(skills)
        self.reachable_skills = set(skills)


# preprocess almanac

characters = {}
fusions = {}
with open("almanac.data", "r") as f:
    C, F = map(int, f.readline().split())
    for _ in range(C):
        line_split = f.readline().split()
        name = line_split[0]
        level = int(line_split[1])
        cost = int(line_split[2])
        skills = line_split[4:]
        characters[name] = Character(name,level,cost,skills)
    fusions = {char:[] for char in characters}
    for _ in range(F):
        result, char0, char1 = f.readline().split()
        fusions[result].append((char0,char1))


def relax(character):
    relaxed = False
    len_skills_before = len(character.reachable_skills)
    for name0, name1 in fusions[character.name]:
        char0 = characters[name0]
        char1 = characters[name1]
        if character.cost > char0.cost+char1.cost:
            character.cost = char0.cost+char1.cost
            relaxed = True
        character.reachable_skills.update(char0.reachable_skills)
        character.reachable_skills.update(char1.reachable_skills)
    relaxed = relaxed or len(character.reachable_skills) > len_skills_before
    return relaxed


while True:
    relaxed = False
    for character in characters.values():
        relaxed = relaxed or relax(character)
    if not relaxed:
        break


class State:
    def __init__(self, leaves, remaining_skills, cost=None):
        self._state = (frozenset(leaves), frozenset(remaining_skills))
        self.cost = cost or sum(characters[char].cost for char in leaves)

    @property
    def leaves(self):
        return self._state[0]

    @property
    def remaining_skills(self):
        return self._state[1]

    def isGoal(self):
        return not self.remaining_skills

    def getSuccessors(self, budget=9999999):
        for leaf in self.leaves:
            for name0, name1 in fusions[leaf]:
                root_char = characters[leaf]
                char0 = characters[name0]
                char1 = characters[name1]
                cost = self.cost - root_char.cost + char0.cost + char1.cost
                if cost > budget:
                    continue
                if not self.remaining_skills.intersection(char0.reachable_skills|char1.reachable_skills):
                    continue
                combined_skills = char0.skills | char1.skills
                yield State(
                        [name0,name1,*filter(lambda l: l!=leaf, self.leaves)],
                        [s for s in self.remaining_skills if s not in combined_skills],
                        cost)

    def __eq__(self, other):
        return self._state == other._state

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash(self._state)

    def __str__(self):
        return "<leaves: ({}), remaining_skills: ({}), cost: {}>".format(
                ", ".join(self.leaves),
                ", ".join(self.remaining_skills),
                self.cost)


def dijkstra(state, budget):
    closed = set()
    queue = [state]
    while queue:
        node = heappop(queue)
        if node.isGoal():
            return node
        closed.add(state)
        for successor in node.getSuccessors(budget):
            if successor in closed:
                continue
            heappush(queue, successor)
    return None


def main():
    # state = State(["phoenix"], ["dark", "ice"]) 
    # print(state)
    # for succ in state.getSuccessors():
        # print("  "+str(succ))
        # for succ_ in succ.getSuccessors():
            # print("    "+str(succ_))
    N = int(input())
    for i in tqdm.trange(1,N+1):
        line = input().split()
        G = int(line[0])
        name = line[1]
        skills = [s for s in line[3:] if s not in characters[name].skills]
        state = State([name], skills)
        solution = dijkstra(state, G)
        print("Case #{}: ".format(i), end="")
        if solution is None:
            print("IMPOSSIBLE")
        else:
            print(solution.cost)



if __name__ == "__main__":
    main()


