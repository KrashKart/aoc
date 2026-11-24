from collections import defaultdict
from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    adj = defaultdict(set)
    for l in readFile(toList=False):
        if l:
            a, b = l.split("-")
            adj[a].add(b)
            adj[b].add(a)
    tris = {frozenset((a, b, c)) for a in adj if a[0] == "t" for b in adj[a] for c in adj[a] & adj[b]}

    def bron_kerbosch(r, p, x):
        if not p and not x:
            yield r
            return
        u = max(p | x, key=lambda v: len(adj[v] & p))
        for v in list(p - adj[u]):
            yield from bron_kerbosch(r | {v}, p & adj[v], x & adj[v])
            p.remove(v)
            x.add(v)

    best = max(bron_kerbosch(set(), set(adj), set()), key=len)
    printParts(len(tris), ",".join(sorted(best)))

if __name__ == "__main__":
    main()
