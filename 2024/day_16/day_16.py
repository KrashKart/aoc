from utils import Grid, dijkstra_all, on_shortest_paths, printParts, readRaw, timeFunction

@timeFunction
def main():
    g = Grid.from_chars(readRaw())
    d, wall = g.data, ord("#")
    si, ei = g.idx(*g.find("S")), g.idx(*g.find("E"))
    off = (1, g.w, -1, -g.w)

    def nb(u):
        # state (flat index, facing); facing indexes off, same order as DIRS4
        i, f = u
        if d[j := i + off[f]] != wall:
            yield (j, f), 1
        yield (i, (f + 1) % 4), 1000
        yield (i, (f - 1) % 4), 1000

    dist, parents, end = dijkstra_all((si, 0), nb, lambda u: u[0] == ei)
    best = dist[end]
    ends = [u for u, c in dist.items() if u[0] == ei and c == best]
    printParts(best, len({i for i, _ in on_shortest_paths(parents, ends)}))

if __name__ == "__main__":
    main()
