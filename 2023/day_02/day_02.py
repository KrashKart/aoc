import re
from math import prod

from utils import ints, printParts, readFile, timeFunction

LIMIT = {"red": 12, "green": 13, "blue": 14}


@timeFunction
def main():
    one = two = 0
    for line in readFile(toList=False):
        mx = {c: max(map(int, re.findall(rf"(\d+) {c}", line)), default=0) for c in LIMIT}
        if all(mx[c] <= LIMIT[c] for c in LIMIT):
            one += ints(line)[0]
        two += prod(mx.values())
    printParts(one, two)


if __name__ == "__main__":
    main()
