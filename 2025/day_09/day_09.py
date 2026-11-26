from itertools import combinations, pairwise
from utils import Grid, bfs, ints, printParts, readFile, timeFunction

@timeFunction
def main():
    pts = [tuple(ints(l)) for l in readFile(toList=False) if l]
    area = lambda a, b: (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

    # compress coordinates (odd indices are corner rows/cols, even ones the gaps between), with a padding ring
    xs, ys = sorted({x for x, _ in pts}), sorted({y for _, y in pts})
    X, Y = {x: 2 * i + 1 for i, x in enumerate(xs)}, {y: 2 * i + 1 for i, y in enumerate(ys)}
    W, H = 2 * len(xs) + 1, 2 * len(ys) + 1
    g = Grid.blank(W, H, 0, "B")
    for (x1, y1), (x2, y2) in pairwise(pts + pts[:1]):
        for cy in range(min(Y[y1], Y[y2]), max(Y[y1], Y[y2]) + 1):
            for cx in range(min(X[x1], X[x2]), max(X[x1], X[x2]) + 1):
                g.set(cx, cy, 1)
    outside = bfs(0, g.nbr4_fn((1,)))

    # P[y][x] = outside cells in the compressed rectangle [0, x) x [0, y)
    P = [[0] * (W + 1) for _ in range(H + 1)]
    for cy in range(H):
        run = 0
        for cx in range(W):
            run += cy * W + cx in outside
            P[cy + 1][cx + 1] = P[cy][cx + 1] + run

    def inside(a, b):
        x1, x2 = sorted((X[a[0]], X[b[0]]))
        y1, y2 = sorted((Y[a[1]], Y[b[1]]))
        return not P[y2 + 1][x2 + 1] - P[y1][x2 + 1] - P[y2 + 1][x1] + P[y1][x1]

    printParts(max(area(a, b) for a, b in combinations(pts, 2)),
               max(area(a, b) for a, b in combinations(pts, 2) if inside(a, b)))

if __name__ == "__main__":
    main()
