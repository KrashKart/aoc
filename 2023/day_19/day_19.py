from math import prod

from utils import ints, printParts, readFile, timeFunction


@timeFunction
def main():
    flows = {}
    for line in readFile(toList=False, name="workflows"):
        if line:
            name, rest = line[:-1].split("{")
            *rules, last = rest.split(",")
            flows[name] = ([(r[0], r[1], int(r[2:(c := r.index(":"))]), r[c + 1:]) for r in rules], last)
    parts = [dict(zip("xmas", ints(l))) for l in readFile(toList=False, name="parts") if l]

    def accepted(p):
        cur = "in"
        while cur not in ("A", "R"):
            rules, last = flows[cur]
            cur = next((t for v, op, n, t in rules if (p[v] < n if op == "<" else p[v] > n)), last)
        return cur == "A"

    def combos(cur, rng):
        if cur == "R":
            return 0
        if cur == "A":
            return prod(hi - lo + 1 for lo, hi in rng.values())
        rules, last = flows[cur]
        tot = 0
        for v, op, n, t in rules:
            lo, hi = rng[v]
            yes, no = ((lo, min(hi, n - 1)), (max(lo, n), hi)) if op == "<" else ((max(lo, n + 1), hi), (lo, min(hi, n)))
            if yes[0] <= yes[1]:
                tot += combos(t, rng | {v: yes})
            if no[0] > no[1]:
                return tot
            rng = rng | {v: no}
        return tot + combos(last, rng)

    printParts(sum(sum(p.values()) for p in parts if accepted(p)), combos("in", dict.fromkeys("xmas", (1, 4000))))


if __name__ == "__main__":
    main()
