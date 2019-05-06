#!/usr/bin/env python3

characters = []
fusions = []
all_skills = set()
with open("almanac.data", "r") as f:
    C, F = map(int, f.readline().split())
    for _ in range(C):
        line_split = f.readline().split()
        name = line_split[0]
        level = int(line_split[1])
        cost = int(line_split[2])
        skills = line_split[4:]
        all_skills.update(skills)
        characters.append((name, level, cost, skills))
    for _ in range(F):
        result, char0, char1 = f.readline().split()
        fusions.append((char0, char1, result))


def getTemplate():
    template = "(define (problem character-6-problem)\n(:domain character-6)\n"
    template += "(:objects {} - character {} - skill)\n".format(
            " ".join(char[0] for char in characters),
            " ".join(all_skills))
    template += "(:init\n(empty-slot slot0)\n(empty-slot slot1)"
    for name,_,_,skills in characters:
        for s in skills:
            template += "\n(HAS-SKILL {} {})".format(name,s)
    for f in fusions:
        template += "\n(CAN-BE-FUSED-INTO {} {} {})".format(*f)
    for name,_,cost,_ in characters:
        template += "\n(= (cost {}) {})".format(name, cost)
    template += "\n(= (total-cost) 0))\n"
    return template
template = getTemplate()


def main():
    N = int(input())
    for i in range(1,N+1):
        line = input().split()
        G = int(line[0])
        character = line[1]
        skills = line[3:]
        goal = "(:goal (and (contains-character slot0 {}) ".format(character)
        goal += " ".join("(assigned-skill slot0 {})".format(s) for s in skills)
        goal +="))\n(:metric minimize (total-cost)))"
        problem = template+goal
        with open("problem.pddl","w") as f:
            f.write(problem)



if __name__ == "__main__":
    main()


