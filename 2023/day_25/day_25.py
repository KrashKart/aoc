from collections import defaultdict, deque
from utils import printParts, readFile, timeFunction

def s_side(adj, s, t, k=3):
    """If the s-t min cut is exactly k (unit edges), return the nodes on s's side, else None."""
    flow = set()
    for i in range(k + 1):
        par, q = {s: None}, deque((s,))
        while q and t not in par:
            u = q.popleft()
            for v in adj[u]:
                if v not in par and (u, v) not in flow:
                    par[v] = u
                    q.append(v)
        if t not in par:
            return par if i == k else None
        v = t
        while (u := par[v]) is not None:
            # pushing along u->v cancels any existing v->u flow instead of stacking
            if (v, u) in flow:
                flow.remove((v, u))
            else:
                flow.add((u, v))
            v = u
    return None

@timeFunction
def main():
    adj = defaultdict(set)
    for line in readFile(toList=False):
        a, bs = line.split(": ")
        for b in bs.split():
            adj[a].add(b)
            adj[b].add(a)
    s, *rest = adj
    side = next(p for t in rest if (p := s_side(adj, s, t)))
    printParts(len(side) * (len(adj) - len(side)), None)

if __name__ == "__main__":
    main()
