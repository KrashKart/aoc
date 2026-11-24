from math import prod
from utils import printParts, readRaw, timeFunction

@timeFunction
def main():
    lines = readRaw().splitlines()
    w = max(map(len, lines))
    *rows, ops = [l.ljust(w) for l in lines]
    # problems are separated by columns that are blank in every row
    cuts = [-1] + [c for c in range(w) if all(r[c] == " " for r in rows)] + [w]
    one = two = 0
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 2:
            continue
        f = prod if "*" in ops[a + 1:b] else sum
        one += f(int(r[a + 1:b]) for r in rows)
        two += f(int("".join(r[c] for r in rows)) for c in range(a + 1, b))
    printParts(one, two)

if __name__ == "__main__":
    main()
