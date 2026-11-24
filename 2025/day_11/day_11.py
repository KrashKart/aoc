from functools import cache
from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    E = {}
    for line in readFile(toList=False):
        if line:
            u, vs = line.split(":")
            E[u.strip()] = vs.split()

    @cache
    def paths(u, end):
        return 1 if u == end else sum(paths(v, end) for v in E.get(u, ()))

    def via(*stops):
        n = 1
        for a, b in zip(stops, stops[1:]):
            n *= paths(a, b)
        return n

    printParts(paths("you", "out"), via("svr", "dac", "fft", "out") + via("svr", "fft", "dac", "out"))

if __name__ == "__main__":
    main()
