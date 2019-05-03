#!/usr/bin/env python3
# -*- coding: utf-8 -*-


characters_1_to_9 = ("一","二","三","四","五","六","七","八","九")
characters_10_to_10000 = ("十","百","千","万")
def westernToJapaneseNumeral(western_numeral):
    # In: 1 <= numeral <= 99999 (int)
    # Out: Japanese numeral (string)
    digits = [] # from least to most significative
    n = western_numeral
    while n:
        digits.append(n%10)
        n = n//10
    japanese_numeral = []
    for i, d in enumerate(digits):
        if d != 0:
            if i > 0:
                japanese_numeral.append(characters_10_to_10000[i-1])
            if i == 0 or i == 4 or d > 1:
                japanese_numeral.append(characters_1_to_9[d-1])
    japanese_numeral.reverse()
    return "".join(japanese_numeral)


kanji_index = {
        "一": 0,  #     1
        "二": 1,  #     2
        "三": 2,  #     3
        "四": 3,  #     4
        "五": 4,  #     5
        "六": 5,  #     6
        "七": 6,  #     7
        "八": 7,  #     8
        "九": 8,  #     9
        "十": 9,  #    10
        "百": 10, #   100
        "千": 11, #  1000
        "万": 12, # 10000
}
def getVectorOfOccurrences(japanese_numeral):
    number_of_occurrences = [0]*13
    for kanji in japanese_numeral:
        number_of_occurrences[kanji_index[kanji]] += 1
    return tuple(number_of_occurrences)


possible_numbers = {}
for i in range(1, 100000):
    japanese_numeral = westernToJapaneseNumeral(i)
    vector_of_occurrences = getVectorOfOccurrences(japanese_numeral)
    try:
        possible_numbers[vector_of_occurrences].append(i)
    except KeyError:
        possible_numbers[vector_of_occurrences] = [i]
def solveProblem(scrambled_a, scrambled_b, scrambled_c):
    domain_a = possible_numbers[getVectorOfOccurrences(scrambled_a)]
    domain_b = possible_numbers[getVectorOfOccurrences(scrambled_b)]
    domain_c = possible_numbers[getVectorOfOccurrences(scrambled_c)]
    for a in domain_a:
        for b in domain_b:
            for c in domain_c:
                if a+b == c:
                    return (a,b,c,"+")
                if a-b == c:
                    return (a,b,c,"-")
                if a*b == c:
                    return (a,b,c,"*")
    assert False, "This shouldn't happen!!"


def main():
    N = int(input())
    for i in range(1,N+1):
        scrambled_a, _, scrambled_b, _, scrambled_c = input().split()
        a,b,c,op = solveProblem(scrambled_a, scrambled_b, scrambled_c)
        print("Case #{}: {} {} {} = {}".format(i,a,op,b,c))


if __name__ == "__main__":
    main()


