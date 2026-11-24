import re
from collections import defaultdict
from math import prod
from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    one, gears = 0, defaultdict(list)
    for y, row in enumerate(g):
        for m in re.finditer(r"\d+", row):
            n = int(m[0])
            syms = [(x, yy) for yy in range(max(y - 1, 0), min(y + 2, h))
                    for x in range(max(m.start() - 1, 0), min(m.end() + 1, w))
                    if not (g[yy][x].isdigit() or g[yy][x] == ".")]
            if syms:
                one += n
            for x, yy in syms:
                if g[yy][x] == "*":
                    gears[x, yy].append(n)
    printParts(one, sum(prod(v) for v in gears.values() if len(v) == 2))

if __name__ == "__main__":
    main()
