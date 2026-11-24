from utils import DIRS4, picks_interior, printParts, readFile, shoelace, timeFunction

DIRS = dict(zip("RDLU", DIRS4))


def lagoon(steps):
    x = y = b = 0
    pts = []
    for (dx, dy), n in steps:
        x, y, b = x + dx * n, y + dy * n, b + n
        pts.append((x, y))
    return picks_interior(shoelace(pts), b) + b


@timeFunction
def main():
    l = readFile(splitOn=" ")
    one = lagoon((DIRS[d], int(n)) for d, n, _ in l)
    two = lagoon((DIRS4[int(c[-2])], int(c[2:7], 16)) for *_, c in l)
    printParts(one, two)


if __name__ == "__main__":
    main()
