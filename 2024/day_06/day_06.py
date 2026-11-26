from utils import Grid, printParts, readRaw, timeFunction

@timeFunction
def main():
    g = Grid.from_chars(readRaw())
    d, w, n = g.data, g.w, len(g.data)
    start = g.idx(*g.find("^"))
    # DIRS4 order (right, down, left, up) as flat offsets, each with a test that the step stays on the grid
    steps = ((1, lambda i: (i + 1) % w), (w, lambda i: i + w < n), (-1, lambda i: i % w), (-w, lambda i: i >= w))

    # stop[k][i]: last cell before a wall walking direction k from i, or -1 if that walk leaves the grid
    stop = []
    for o, inside in steps:
        s = [-1] * n
        for i in range(n - 1, -1, -1) if o > 0 else range(n):
            if inside(i):
                s[i] = i if d[i + o] == 35 else s[i + o]
        stop.append(s)

    i, k, seen = start, 3, set()
    while True:
        seen.add(i)
        o, inside = steps[k]
        if not inside(i):
            break
        if d[i + o] == 35:
            k = (k + 1) % 4
        else:
            i += o

    def loops(ob):
        i, k, turns = start, 3, set()
        while True:
            o, t = steps[k][0], stop[k][i]
            # the extra obstacle cuts this straight run short if it lies ahead on it, before the wall
            if (ob // w == i // w if k % 2 == 0 else ob % w == i % w) and (m := (ob - i) // o) > 0 and (t < 0 or m <= (t - i) // o):
                t = ob - o
            if t < 0:
                return False
            if (key := t * 4 + k) in turns:
                return True
            turns.add(key)
            i, k = t, (k + 1) % 4

    printParts(len(seen), sum(loops(p) for p in seen if p != start))

if __name__ == "__main__":
    main()
