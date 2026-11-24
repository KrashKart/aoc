from collections import defaultdict
from itertools import permutations
from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    ants = defaultdict(list)
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if c != ".":
                ants[c].append((x, y))
    one, two = set(), set()
    for ps in ants.values():
        for (x1, y1), (x2, y2) in permutations(ps, 2):
            dx, dy = x2 - x1, y2 - y1
            if 0 <= x2 + dx < w and 0 <= y2 + dy < h:
                one.add((x2 + dx, y2 + dy))
            x, y = x2, y2
            while 0 <= x < w and 0 <= y < h:
                two.add((x, y))
                x, y = x + dx, y + dy
    printParts(len(one), len(two))

if __name__ == "__main__":
    main()
