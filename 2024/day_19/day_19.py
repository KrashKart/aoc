from functools import cache
from utils import blocks, printParts, readRaw, timeFunction

@timeFunction
def main():
    t, d = blocks(readRaw())
    towels = set(t.split(", "))
    L = max(map(len, towels))

    @cache
    def ways(s):
        return 1 if not s else sum(ways(s[k:]) for k in range(1, min(L, len(s)) + 1) if s[:k] in towels)

    counts = [ways(s) for s in d.splitlines()]
    printParts(sum(map(bool, counts)), sum(counts))

if __name__ == "__main__":
    main()
