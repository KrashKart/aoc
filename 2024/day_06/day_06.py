from math import inf
from utils import DIRS4, printParts, readFile, timeFunction

@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    sy = next(y for y, r in enumerate(g) if "^" in r)
    sx = g[sy].index("^")

    # stop[d][p]: last cell before a wall walking direction d from p, or None if that walk leaves the grid
    stop = []
    for dx, dy in DIRS4:
        s = {}
        for x, y in sorted(((x, y) for y in range(h) for x in range(w)), key=lambda p: -(p[0] * dx + p[1] * dy)):
            nx, ny = x + dx, y + dy
            s[x, y] = None if not (0 <= nx < w and 0 <= ny < h) else (x, y) if g[ny][nx] == "#" else s[nx, ny]
        stop.append(s)

    x, y, d, seen = sx, sy, 3, set()
    while True:
        seen.add((x, y))
        dx, dy = DIRS4[d]
        if not (0 <= x + dx < w and 0 <= y + dy < h):
            break
        if g[y + dy][x + dx] == "#":
            d = (d + 1) % 4
        else:
            x, y = x + dx, y + dy

    def loops(ox, oy):
        x, y, d, turns = sx, sy, 3, set()
        while True:
            dx, dy = DIRS4[d]
            t = stop[d][x, y]
            # the extra obstacle cuts this straight run short if it lies on it
            if (oy - y) * dx == 0 and (ox - x) * dy == 0 and (k := (ox - x) * dx + (oy - y) * dy) > 0:
                if k <= (inf if t is None else (t[0] - x) * dx + (t[1] - y) * dy):
                    t = (ox - dx, oy - dy)
            if t is None:
                return False
            if (t, d) in turns:
                return True
            turns.add((t, d))
            (x, y), d = t, (d + 1) % 4

    printParts(len(seen), sum(loops(*p) for p in seen if p != (sx, sy)))

if __name__ == "__main__":
    main()
