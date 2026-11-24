from itertools import pairwise
from utils import ints, printParts, readFile, timeFunction

def extrapolate(s):
    return s[-1] + extrapolate([b - a for a, b in pairwise(s)]) if any(s) else 0

@timeFunction
def main():
    seqs = [ints(l) for l in readFile(toList=False)]
    printParts(sum(map(extrapolate, seqs)), sum(extrapolate(s[::-1]) for s in seqs))

if __name__ == "__main__":
    main()
