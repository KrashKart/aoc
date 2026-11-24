from collections import Counter
from utils import ints, printParts, readRaw, timeFunction

def blink(c):
    out = Counter()
    for s, k in c.items():
        if s == 0:
            out[1] += k
        elif (l := len(str(s))) % 2 == 0:
            m = 10 ** (l // 2)
            out[s // m] += k
            out[s % m] += k
        else:
            out[s * 2024] += k
    return out

@timeFunction
def main():
    c = Counter(ints(readRaw()))
    for i in range(75):
        if i == 25:
            one = c.total()
        c = blink(c)
    printParts(one, c.total())

if __name__ == "__main__":
    main()
