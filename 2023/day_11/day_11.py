from utils import printParts, readFile, timeFunction


def spread(cs, f):
    """Sum of pairwise distances along one axis after widening every empty line to f lines."""
    cs = sorted(cs)
    rank = {v: i for i, v in enumerate(sorted(set(cs)))}
    pos = [c + (f - 1) * (c - rank[c]) for c in cs]
    return sum(p * (2 * i - len(pos) + 1) for i, p in enumerate(pos))


@timeFunction
def main():
    gals = [(x, y) for y, r in enumerate(readFile(toList=False)) for x, c in enumerate(r) if c == "#"]
    xs, ys = zip(*gals)
    printParts(*(spread(xs, f) + spread(ys, f) for f in (2, 1_000_000)))


if __name__ == "__main__":
    main()
