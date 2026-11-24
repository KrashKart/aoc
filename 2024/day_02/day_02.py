from itertools import pairwise
from utils import ints, printParts, readFile, timeFunction

def safe(r):
    ds = [b - a for a, b in pairwise(r)]
    return all(1 <= d <= 3 for d in ds) or all(-3 <= d <= -1 for d in ds)

@timeFunction
def main():
    rs = [ints(l) for l in readFile(toList=False) if l]
    one = sum(map(safe, rs))
    two = sum(any(safe(r[:i] + r[i + 1:]) for i in range(len(r))) for r in rs)
    printParts(one, two)

if __name__ == "__main__":
    main()
