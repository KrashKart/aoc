from collections import deque
from math import lcm
from utils import printParts, readFile, timeFunction

def machine(typ, dests):
    """Return a fresh press() generator factory yielding every (src, dst, high) pulse of one button press."""
    on = dict.fromkeys(typ, False)
    mem = {n: {} for n, t in typ.items() if t == "&"}
    for n, ds in dests.items():
        for d in ds:
            if d in mem:
                mem[d][n] = False

    def press():
        q = deque((("button", "broadcaster", False),))
        while q:
            src, n, p = q.popleft()
            yield src, n, p
            match typ.get(n):
                case "%":
                    if p:
                        continue
                    on[n] = out = not on[n]
                case "&":
                    mem[n][src] = p
                    out = not all(mem[n].values())
                case "":
                    out = p
                case _:
                    continue
            q.extend((n, d, out) for d in dests[n])
    return press

@timeFunction
def main():
    typ, dests = {}, {}
    for line in readFile(toList=False):
        n, d = line.split(" -> ")
        t, n = (n[0], n[1:]) if n[0] in "%&" else ("", n)
        typ[n], dests[n] = t, d.split(", ")

    press, cnt = machine(typ, dests), [0, 0]
    for _ in range(1000):
        for *_, p in press():
            cnt[p] += 1

    # rx is fed by one conjunction; it fires low once all its inputs go high together, so lcm their periods
    hub = next(n for n, ds in dests.items() if "rx" in ds)
    feeders = {n for n, ds in dests.items() if hub in ds}
    press, first, i = machine(typ, dests), {}, 0
    while len(first) < len(feeders):
        i += 1
        for src, n, p in press():
            if n == hub and p:
                first.setdefault(src, i)
    printParts(cnt[0] * cnt[1], lcm(*first.values()))

if __name__ == "__main__":
    main()
