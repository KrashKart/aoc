from utils import blocks, ints, printParts, readRaw, timeFunction


def lowest(rngs, maps):
    """Push half-open [lo, hi) ranges through every map, splitting them where they straddle a rule."""
    for m in maps:
        out = []
        while rngs:
            lo, hi = rngs.pop()
            for d, s, n in m:
                a, b = max(lo, s), min(hi, s + n)
                if a < b:
                    out.append((a - s + d, b - s + d))
                    if lo < a:
                        rngs.append((lo, a))
                    if b < hi:
                        rngs.append((b, hi))
                    break
            else:
                out.append((lo, hi))
        rngs = out
    return min(lo for lo, _ in rngs)


@timeFunction
def main():
    seeds, *maps = blocks(readRaw())
    seeds = ints(seeds)
    maps = [[ints(l) for l in b.splitlines()[1:]] for b in maps]
    one = lowest([(s, s + 1) for s in seeds], maps)
    two = lowest([(s, s + n) for s, n in zip(seeds[::2], seeds[1::2])], maps)
    printParts(one, two)


if __name__ == "__main__":
    main()
