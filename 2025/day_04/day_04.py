from utils import Grid, printParts, readRaw, timeFunction

@timeFunction
def main():
    g = Grid.from_chars(readRaw())
    rolls = {p for p in g.find_all("@")}
    nbrs = {p: [q for q in g.neighbours8(*p) if q in rolls] for p in rolls}
    deg = {p: len(v) for p, v in nbrs.items()}
    # peel rolls with < 4 neighbours; removal order doesn't change what is eventually removable
    stack = [p for p in rolls if deg[p] < 4]
    removed = set(stack)
    one = len(stack)
    while stack:
        for q in nbrs[stack.pop()]:
            deg[q] -= 1
            if q not in removed and deg[q] < 4:
                removed.add(q)
                stack.append(q)
    printParts(one, len(removed))

if __name__ == "__main__":
    main()
