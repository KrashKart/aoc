from collections import deque
from graphlib import TopologicalSorter
from heapq import heappop, heappush
from math import inf

def bfs(start, neighbours, goal=None):
    """Unweighted shortest distances from start; neighbours(node) yields adjacent nodes.

    Returns {node: distance}, stopping as soon as goal is reached.
    """
    dist = {start: 0}
    q = deque((start,))
    pop, push = q.popleft, q.append
    while q:
        u = pop()
        if u == goal:
            break
        d = dist[u] + 1
        for v in neighbours(u):
            if v not in dist:
                dist[v] = d
                push(v)
    return dist

def _goal_test(goal):
    """Helper to standardize goal as a predicate."""
    return goal if callable(goal) else (lambda u: u == goal) if goal is not None else (lambda u: False)

def dijkstra(start, neighbours, goal=None):
    """Weighted shortest paths; neighbours(node) yields (node, cost) and nodes must be orderable.

    goal is a node or a predicate. Returns (dist, parents, reached goal node or None).
    """
    done = _goal_test(goal)
    dist, parents = {start: 0}, {start: None}
    heap = [(0, start)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            # repeat entry, so continue and skip
            continue
        if done(u):
            return dist, parents, u
        for v, c in neighbours(u):
            nd = d + c
            if nd < dist.get(v, inf):
                dist[v] = nd
                parents[v] = u
                heappush(heap, (nd, v))
    return dist, parents, None

def dijkstra_all(start, neighbours, goal=None):
    """Like dijkstra, but parents[node] lists every predecessor on a shortest path (for all_shortest_paths).

    Stopping at goal only keeps parents[goal] complete when every edge cost is positive.
    """
    done = _goal_test(goal)
    dist, parents = {start: 0}, {start: []}
    heap = [(0, start)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        if done(u):
            return dist, parents, u
        for v, c in neighbours(u):
            nd = d + c
            if nd < (od := dist.get(v, inf)):
                dist[v] = nd
                parents[v] = [u]
                heappush(heap, (nd, v))
            elif nd == od:
                parents[v].append(u)
    return dist, parents, None

def reconstruct(parents, end):
    """Return the start..end path from dijkstra/astar parents."""
    path = []
    while end is not None:
        path.append(end)
        end = parents[end]
    return path[::-1]

def all_shortest_paths(parents, end):
    """Yield every shortest start..end path from dijkstra_all parents (can be exponentially many)."""
    stack = [(end, [end])]
    while stack:
        u, path = stack.pop()
        if ps := parents[u]:
            stack.extend((p, path + [p]) for p in ps)
        else:
            yield path[::-1]

def on_shortest_paths(parents, ends):
    """Return the set of nodes on any shortest path to any node in ends, from dijkstra_all parents."""
    seen = set(ends)
    stack = list(seen)
    while stack:
        for p in parents[stack.pop()]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen

def astar(start, goal, neighbours, h):
    """A* search; neighbours(node) yields (node, cost), h(node) is an admissible heuristic.

    Returns (cost to goal or None, parents).
    """
    g, parents = {start: 0}, {start: None}
    heap = [(h(start), 0, start)]
    while heap:
        _, d, u = heappop(heap)
        if d > g[u]:
            continue
        if u == goal:
            return d, parents
        for v, c in neighbours(u):
            nd = d + c
            if nd < g.get(v, inf):
                g[v] = nd
                parents[v] = u
                heappush(heap, (nd + h(v), nd, v))
    return None, parents

def components(nodes, neighbours):
    """Group nodes into connected components (lists) by flood fill; neighbours(node) yields connected nodes."""
    seen, out = set(), []
    for s in nodes:
        if s in seen:
            continue
        seen.add(s)
        comp, stack = [s], [s]
        while stack:
            for v in neighbours(stack.pop()):
                if v not in seen:
                    seen.add(v)
                    comp.append(v)
                    stack.append(v)
        out.append(comp)
    return out

class UnionFind:
    """Disjoint sets over 0..n-1 (pass an int) or over arbitrary hashable nodes (pass an iterable)."""
    __slots__ = ("parent", "size", "count")

    def __init__(self, nodes):
        """nodes: an int n for 0..n-1, or an iterable of hashable nodes."""
        if isinstance(nodes, int):
            self.parent, self.size = list(range(nodes)), [1] * nodes
        else:
            self.parent = {x: x for x in nodes}
            self.size = dict.fromkeys(self.parent, 1)
        self.count = len(self.parent)

    def find(self, x):
        """Return the root of x's set."""
        p = self.parent
        while (q := p[x]) != x:
            # path halving: point x at its grandparent, then jump there
            p[x] = x = p[q]
        return x

    def union(self, a, b):
        """Merge the sets containing a and b; returns False if they were already joined."""
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        s = self.size
        if s[a] < s[b]:
            a, b = b, a
        self.parent[b] = a
        s[a] += s[b]
        self.count -= 1
        return True

def topo_sort(deps):
    """Order nodes so every node comes after its prerequisites; deps maps node -> iterable of prerequisites."""
    return list(TopologicalSorter(deps).static_order())
