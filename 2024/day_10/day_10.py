from utils import Grid, printParts, readRaw, timeFunction

@timeFunction
def main():
    g = Grid.from_digits(readRaw())
    d, n, nb = g.data, len(g.data), g.nbr4_fn()
    # sweep from height 9 down so every uphill neighbour is finished before its predecessor
    peaks, paths = [set() for _ in range(n)], [0] * n
    for i in sorted(range(n), key=lambda i: -d[i]):
        if d[i] == 9:
            peaks[i], paths[i] = {i}, 1
            continue
        for j in nb(i):
            if d[j] == d[i] + 1:
                peaks[i] |= peaks[j]
                paths[i] += paths[j]
    heads = [i for i in range(n) if d[i] == 0]
    printParts(sum(len(peaks[i]) for i in heads), sum(paths[i] for i in heads))

if __name__ == "__main__":
    main()
