from bisect import bisect_right
from utils import blocks, merge_intervals, printParts, readRaw, timeFunction

@timeFunction
def main():
    r, ids = blocks(readRaw())
    ivs = merge_intervals(tuple(map(int, l.split("-"))) for l in r.splitlines())
    los = [lo for lo, _ in ivs]
    one = sum((i := bisect_right(los, x) - 1) >= 0 and x <= ivs[i][1] for x in map(int, ids.split()))
    printParts(one, sum(hi - lo + 1 for lo, hi in ivs))

if __name__ == "__main__":
    main()
