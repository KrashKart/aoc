from itertools import combinations
from utils import blocks, printParts, readRaw, timeFunction

@timeFunction
def main():
    # two locks always clash on their top row and two keys on their bottom row, so checking every pair is safe
    masks = [int(b.replace("\n", "").translate(str.maketrans("#.", "10")), 2) for b in blocks(readRaw())]
    printParts(sum(not a & b for a, b in combinations(masks, 2)), None)

if __name__ == "__main__":
    main()
