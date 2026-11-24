from collections import Counter
from utils import printParts, readFile, timeFunction

def strength(hand, order, joker):
    c = Counter(hand)
    j = c.pop("J", 0) if joker else 0
    counts = sorted(c.values(), reverse=True) or [0]
    counts[0] += j
    return counts, [order.index(ch) for ch in hand]

@timeFunction
def main():
    hands = [(h, int(b)) for h, b in readFile(splitOn=" ")]

    def winnings(order, joker):
        ranked = sorted(hands, key=lambda hb: strength(hb[0], order, joker))
        return sum(i * b for i, (_, b) in enumerate(ranked, 1))

    printParts(winnings("23456789TJQKA", False), winnings("J23456789TQKA", True))

if __name__ == "__main__":
    main()
