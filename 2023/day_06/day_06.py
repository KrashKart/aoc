from math import prod
from utils import bisect_pred, ints, printParts, readFile, timeFunction

def ways(t, d):
    # distance i*(t-i) rises until t/2, so find the first winning hold time and mirror it
    return t - 2 * bisect_pred(0, t // 2 + 1, lambda i: i * (t - i) > d) + 1

@timeFunction
def main():
    l = readFile(toList=False)
    times, dists = map(ints, l)
    one = prod(map(ways, times, dists))
    two = ways(*(int("".join(map(str, ints(r)))) for r in l))
    printParts(one, two)

if __name__ == "__main__":
    main()
