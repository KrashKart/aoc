from utils import DIRS4, printParts, readFile, timeFunction

def energize(g, start):
    # d indexes DIRS4: 0 right, 1 down, 2 left, 3 up
    w, h = len(g[0]), len(g)
    seen, stack = set(), [start]
    while stack:
        s = stack.pop()
        x, y, d = s
        if s in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add(s)
        match g[y][x]:
            case "/": nds = (3 - d,)
            case "\\": nds = (d ^ 1,)
            case "|" if d % 2 == 0: nds = (1, 3)
            case "-" if d % 2: nds = (0, 2)
            case _: nds = (d,)
        for nd in nds:
            dx, dy = DIRS4[nd]
            stack.append((x + dx, y + dy, nd))
    return len({(x, y) for x, y, _ in seen})

@timeFunction
def main():
    g = readFile(toList=False)
    w, h = len(g[0]), len(g)
    starts = ([(0, y, 0) for y in range(h)] + [(w - 1, y, 2) for y in range(h)]
              + [(x, 0, 1) for x in range(w)] + [(x, h - 1, 3) for x in range(w)])
    printParts(energize(g, (0, 0, 0)), max(energize(g, s) for s in starts))

if __name__ == "__main__":
    main()
