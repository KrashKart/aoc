from itertools import pairwise
from utils import printParts, readFile, timeFunction

DIR = {"^": (1, 0), "A": (2, 0), "<": (0, 1), "v": (1, 1), ">": (2, 1)}
NUM = {"7": (0, 0), "8": (1, 0), "9": (2, 0), "4": (0, 1), "5": (1, 1), "6": (2, 1),
       "1": (0, 2), "2": (1, 2), "3": (2, 2), "0": (1, 3), "A": (2, 3)}

def presses(cost, seq):
    return sum(cost[a, b] for a, b in pairwise("A" + seq))

def table(robots):
    """cost[a, b]: fewest human presses to move from a to b and press b on the outermost keypad."""
    cost = {(a, b): 1 for a in DIR for b in DIR}
    for layer in range(robots + 1):
        pad, gap = (NUM, (0, 3)) if layer == robots else (DIR, (0, 0))
        new = {}
        for a, (x1, y1) in pad.items():
            for b, (x2, y2) in pad.items():
                hz = ("<" if x2 < x1 else ">") * abs(x2 - x1)
                vt = ("^" if y2 < y1 else "v") * abs(y2 - y1)
                # only all-horizontal-then-vertical or the reverse can be optimal; skip whichever crosses the gap
                new[a, b] = min(presses(cost, s + "A") for s, corner in ((hz + vt, (x2, y1)), (vt + hz, (x1, y2)))
                                if corner != gap)
        cost = new
    return cost

@timeFunction
def main():
    codes = [l for l in readFile(toList=False) if l]
    one, two = (sum(presses(t, c) * int(c[:-1]) for c in codes) for t in (table(2), table(25)))
    printParts(one, two)

if __name__ == "__main__":
    main()
