from utils import DIRS4, picks_interior, printParts, readFile, shoelace, timeFunction

PIPES = {"|": ((0, -1), (0, 1)), "-": ((-1, 0), (1, 0)), "L": ((0, -1), (1, 0)),
         "J": ((0, -1), (-1, 0)), "7": ((0, 1), (-1, 0)), "F": ((0, 1), (1, 0))}

@timeFunction
def main():
    g = readFile(toList=False)
    sy = next(y for y, r in enumerate(g) if "S" in r)
    sx = g[sy].index("S")
    dx, dy = next((dx, dy) for dx, dy in DIRS4 if 0 <= sy + dy < len(g) and 0 <= sx + dx < len(g[0])
                  and (-dx, -dy) in PIPES.get(g[sy + dy][sx + dx], ()))
    x, y, n, verts = sx, sy, 0, [(sx, sy)]
    while True:
        x, y, n = x + dx, y + dy, n + 1
        if (c := g[y][x]) == "S":
            break
        a, b = PIPES[c]
        dx, dy = b if a == (-dx, -dy) else a
        if c in "LJ7F":
            verts.append((x, y))
    printParts(n // 2, picks_interior(shoelace(verts), n))

if __name__ == "__main__":
    main()
