from utils import DIRS4, bfs, bisect_pred, ints, printParts, readFile, timeFunction

N, FIRST = 71, 1024
GOAL = (N - 1, N - 1)

@timeFunction
def main():
    falls = [tuple(ints(l)) for l in readFile(toList=False) if l]

    def steps(n):
        blocked = set(falls[:n])

        def nb(p):
            for dx, dy in DIRS4:
                q = (p[0] + dx, p[1] + dy)
                if 0 <= q[0] < N and 0 <= q[1] < N and q not in blocked:
                    yield q
        return bfs((0, 0), nb, GOAL).get(GOAL)

    n = bisect_pred(FIRST, len(falls) + 1, lambda n: steps(n) is None)
    printParts(steps(FIRST), ",".join(map(str, falls[n - 1])))

if __name__ == "__main__":
    main()
