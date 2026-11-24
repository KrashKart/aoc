from utils import Grid, dijkstra, printParts, readRaw, timeFunction

AXES = (((1, 0), (-1, 0)), ((0, 1), (0, -1)))

def least_heat(g, lo, hi):
    # state (x, y, axis last moved on); each move turns onto the other axis and goes lo..hi cells
    w, h, data = g.w, g.h, g.data

    def nb(u):
        x, y, a = u
        for na, dirs in enumerate(AXES):
            if na == a:
                continue
            for dx, dy in dirs:
                nx, ny, cost = x, y, 0
                for k in range(1, hi + 1):
                    nx, ny = nx + dx, ny + dy
                    if not (0 <= nx < w and 0 <= ny < h):
                        break
                    cost += data[ny * w + nx]
                    if k >= lo:
                        yield (nx, ny, na), cost

    dist, _, end = dijkstra((0, 0, -1), nb, lambda u: u[0] == w - 1 and u[1] == h - 1)
    return dist[end]

@timeFunction
def main():
    g = Grid.from_digits(readRaw())
    printParts(least_heat(g, 1, 3), least_heat(g, 4, 10))

if __name__ == "__main__":
    main()
