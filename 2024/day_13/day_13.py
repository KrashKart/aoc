from utils import blocks, ints, printParts, readRaw, timeFunction

def tokens(ax, ay, bx, by, px, py):
    # Cramer's rule; only whole non-negative presses count
    det = ax * by - ay * bx
    a, b = px * by - py * bx, ax * py - ay * px
    if det and a % det == 0 and b % det == 0 and a // det >= 0 and b // det >= 0:
        return 3 * (a // det) + b // det
    return 0

@timeFunction
def main():
    ms = [ints(b) for b in blocks(readRaw())]
    off = 10_000_000_000_000
    printParts(sum(tokens(*m) for m in ms), sum(tokens(*m[:4], m[4] + off, m[5] + off) for m in ms))

if __name__ == "__main__":
    main()
