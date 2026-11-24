from collections import Counter
from itertools import combinations
from math import prod
from utils import UnionFind, ints, printParts, readFile, timeFunction

PAIRS = 1000

@timeFunction
def main():
    pts = [tuple(ints(l)) for l in readFile(toList=False) if l]
    pairs = sorted(combinations(range(len(pts)), 2), key=lambda p: sum((a - b) ** 2 for a, b in zip(pts[p[0]], pts[p[1]])))
    uf = UnionFind(len(pts))
    for k, (i, j) in enumerate(pairs, 1):
        uf.union(i, j)
        if k == PAIRS:
            one = prod(sorted(Counter(map(uf.find, range(len(pts)))).values())[-3:])
        if uf.count == 1:
            break
    printParts(one, pts[i][0] * pts[j][0])

if __name__ == "__main__":
    main()
