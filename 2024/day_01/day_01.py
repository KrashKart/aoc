from collections import Counter
from utils import ints, printParts, readFile, timeFunction

@timeFunction
def main():
    a, b = map(sorted, zip(*(ints(l) for l in readFile(toList=False) if l)))
    c = Counter(b)
    printParts(sum(abs(x - y) for x, y in zip(a, b)), sum(x * c[x] for x in a))

if __name__ == "__main__":
    main()
