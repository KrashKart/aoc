import numpy as np
from utils import ints, printParts, readRaw, timeFunction

M, B = 0xFFFFFF, 19

@timeFunction
def main():
    s = np.array(ints(readRaw()), dtype=np.int64)
    n = len(s)
    prices = np.empty((2001, n), dtype=np.int64)
    for i in range(2001):
        prices[i] = s % 10
        if i < 2000:
            s = (s ^ (s << 6)) & M
            s ^= s >> 5
            s = (s ^ (s << 11)) & M
    d = np.diff(prices, axis=0) + 9
    key = ((d[:-3] * B + d[1:-2]) * B + d[2:-1]) * B + d[3:]
    # tag each key with its buyer so np.unique's first-occurrence index finds each buyer's first sighting of a sequence
    tagged = (key.T + np.arange(n)[:, None] * B ** 4).ravel()
    uniq, first = np.unique(tagged, return_index=True)
    bananas = np.bincount(uniq % B ** 4, weights=prices[4:].T.ravel()[first], minlength=B ** 4)
    printParts(int(s.sum()), int(bananas.max()))

if __name__ == "__main__":
    main()
