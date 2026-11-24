from collections import defaultdict
from functools import cache
from math import inf
from utils import ints, printParts, readFile, timeFunction

def machine(lights, buttons, jolts):
    n = len(jolts)
    # every subset of buttons pressed once: its total effect per counter, grouped by the parity it leaves
    eff = [(0,) * n]
    for b in buttons:
        vec = tuple(int(i in b) for i in range(n))
        eff += [tuple(map(sum, zip(e, vec))) for e in eff]
    size = [m.bit_count() for m in range(len(eff))]
    by_parity = defaultdict(list)
    for m, e in enumerate(eff):
        by_parity[tuple(v & 1 for v in e)].append((size[m], e))

    target = tuple(int(c == "#") for c in lights)
    one = min(c for c, _ in by_parity[target])

    @cache
    def presses(j):
        # pressing a button twice is parity-neutral, so fix parity with a 0/1 subset, then halve what remains
        if not any(j):
            return 0
        best = inf
        for c, e in by_parity[tuple(v & 1 for v in j)]:
            if all(a <= b for a, b in zip(e, j)):
                best = min(best, c + 2 * presses(tuple((b - a) // 2 for a, b in zip(e, j))))
        return best

    return one, presses(tuple(jolts))

@timeFunction
def main():
    one = two = 0
    for line in readFile(toList=False):
        if line:
            toks = line.split()
            a, b = machine(toks[0][1:-1], [ints(t) for t in toks[1:-1]], ints(toks[-1]))
            one, two = one + a, two + b
    printParts(one, two)

if __name__ == "__main__":
    main()
