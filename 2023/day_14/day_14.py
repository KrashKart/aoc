from utils import find_cycle, printParts, readFile, timeFunction

def roll(rows):
    """Slide every O to the start of each row, stopping at #."""
    return ["#".join("".join(sorted(s, reverse=True)) for s in "".join(r).split("#")) for r in rows]

def spin(g):
    # transpose + roll = tilt north; reversing each row then completes a clockwise rotation
    for _ in range(4):
        g = tuple(r[::-1] for r in roll(zip(*g)))
    return g

@timeFunction
def main():
    g = tuple(readFile(toList=False))
    one = sum(len(c) - i for c in roll(zip(*g)) for i, ch in enumerate(c) if ch == "O")
    final = find_cycle(g, spin, 1_000_000_000)
    two = sum((len(final) - y) * r.count("O") for y, r in enumerate(final))
    printParts(one, two)

if __name__ == "__main__":
    main()
