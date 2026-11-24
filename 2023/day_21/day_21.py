from utils import DIRS4, printParts, readFile, timeFunction

STEPS = 26501365


def reachable(g, start, n):
    """counts[s] = plots reachable in exactly s steps on the infinitely tiled grid, for s in 0..n."""
    h, w = len(g), len(g[0])
    seen, frontier, par, counts = {start}, [start], [0, 0], []
    for s in range(n + 1):
        par[s & 1] += len(frontier)
        counts.append(par[s & 1])
        nxt = []
        for x, y in frontier:
            for dx, dy in DIRS4:
                if (p := (x + dx, y + dy)) not in seen and g[p[1] % h][p[0] % w] != "#":
                    seen.add(p)
                    nxt.append(p)
        frontier = nxt
    return counts


@timeFunction
def main():
    g = readFile(toList=False)
    sy = next(y for y, r in enumerate(g) if "S" in r)
    w = len(g[0])
    r, s = STEPS % w, STEPS // w
    counts = reachable(g, (g[sy].index("S"), sy), r + 2 * w)
    # the count grows quadratically in whole tiles walked, so extrapolate from 3 samples (see derivation.jpg)
    y0, y1, y2 = (counts[r + k * w] for k in range(3))
    printParts(counts[64], y0 + (y1 - y0) * s + (y2 - 2 * y1 + y0) * s * (s - 1) // 2)


if __name__ == "__main__":
    main()
