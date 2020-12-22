from typing import List


def score(c: List[int]) -> int:
    return sum([x*(i+1) for i, x in enumerate(reversed(c))])


p1d, p2d = open('22.example1').read().split("\n\n")

p1 = [int(x) for x in p1d.splitlines()[1:]]
p2 = [int(x) for x in p2d.splitlines()[1:]]


def rec_combat(p1: List[int], p2: List[int]):
    seen = set()

    while len(p1) > 0 and len(p2) > 0:
        key = str(p1) + '|' + str(p2)

        if key in seen:
            return 1, score(p1)

        seen.add(key)

        p1c = p1.pop(0)
        p2c = p2.pop(0)

        if len(p1) >= p1c and len(p2) >= p2c:
            winner = rec_combat(p1[:p1c], p2[:p2c])

            if winner == 1:
                p1.extend([p1c, p2c])
            else:
                p2.extend([p2c, p1c])
        else:
            if p1c > p2c:
                p1.extend([p1c, p2c])
            else:
                p2.extend([p2c, p1c])

    return score(p1), score(p2)


print(rec_combat(p1, p2))
