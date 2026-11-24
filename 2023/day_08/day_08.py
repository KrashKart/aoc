import re
from itertools import cycle
from math import lcm

from utils import printParts, readFile, readRaw, timeFunction


@timeFunction
def main():
    dirs = readRaw(name="dir").strip()
    nodes = {a: (b, c) for a, b, c in (re.findall(r"\w+", l) for l in readFile(toList=False, name="nodes") if l)}

    def steps(cur, done):
        for i, d in enumerate(cycle(dirs)):
            if done(cur):
                return i
            cur = nodes[cur][d == "R"]

    one = steps("AAA", lambda c: c == "ZZZ")
    two = lcm(*(steps(n, lambda c: c[-1] == "Z") for n in nodes if n[-1] == "A"))
    printParts(one, two)


if __name__ == "__main__":
    main()
