import numpy as np
from utils import DIRS4, bfs, printParts, readFile, timeFunction

SAVE = 100

def cheats(D, r):
    """Count (start, end) track pairs within Manhattan distance r whose shortcut saves >= SAVE, one offset at a time."""
    h, w = D.shape
    tot = 0
    for dy in range(-r, r + 1):
        for dx in range(abs(dy) - r, r - abs(dy) + 1):
            if (c := abs(dx) + abs(dy)) < 2 or abs(dx) >= w or abs(dy) >= h:
                continue
            y0, y1, x0, x1 = max(0, -dy), h - max(0, dy), max(0, -dx), w - max(0, dx)
            src, dst = D[y0:y1, x0:x1], D[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
            tot += np.count_nonzero((src >= 0) & (dst - src - c >= SAVE))
    return tot

@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    sy = next(y for y, r in enumerate(g) if "S" in r)

    def nb(p):
        for dx, dy in DIRS4:
            x, y = p[0] + dx, p[1] + dy
            if 0 <= x < w and 0 <= y < h and g[y][x] != "#":
                yield x, y

    D = np.full((h, w), -1, dtype=np.int32)
    for (x, y), c in bfs((g[sy].index("S"), sy), nb).items():
        D[y, x] = c
    printParts(cheats(D, 2), cheats(D, 20))

if __name__ == "__main__":
    main()
