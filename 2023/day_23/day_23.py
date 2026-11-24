from utils import DIRMAP, DIRS4, printParts, readFile, timeFunction


def condense(g, nodes, slopes):
    """Map each junction to [(next junction, corridor length)], optionally obeying slopes."""
    h = len(g)

    def nb(x, y):
        c = g[y][x]
        for dx, dy in (DIRMAP[c],) if slopes and c in DIRMAP else DIRS4:
            if 0 <= y + dy < h and g[y + dy][x + dx] != "#":
                yield x + dx, y + dy

    adj = {n: [] for n in nodes}
    for s in nodes:
        for p in nb(*s):
            prev, cur, d = s, p, 1
            while cur not in adj:
                if not (nxt := [q for q in nb(*cur) if q != prev]):
                    break
                prev, cur, d = cur, nxt[0], d + 1
            else:
                adj[s].append((cur, d))
    return adj


def longest(adj, start, end):
    idx = {n: i for i, n in enumerate(adj)}
    A = [[(idx[v], d) for v, d in adj[n]] for n in adj]
    # the junction before end must step straight to end, or end is cut off
    pen, pd = next((idx[n], d) for n in adj for v, d in adj[n] if v == end)
    best, stack = 0, [(idx[start], 1 << idx[start], 0)]
    while stack:
        u, seen, d = stack.pop()
        if u == pen:
            best = max(best, d + pd)
            continue
        for v, c in A[u]:
            if not seen >> v & 1:
                stack.append((v, seen | 1 << v, d + c))
    return best


@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    start, end = (g[0].index("."), 0), (g[-1].index("."), h - 1)
    nodes = [start, end] + [(x, y) for y in range(1, h - 1) for x in range(1, w - 1) if g[y][x] != "#"
                            and sum(g[y + dy][x + dx] != "#" for dx, dy in DIRS4) > 2]
    printParts(*(longest(condense(g, nodes, s), start, end) for s in (True, False)))


if __name__ == "__main__":
    main()
