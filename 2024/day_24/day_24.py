from collections import defaultdict
from utils import blocks, printParts, readRaw, timeFunction

@timeFunction
def main():
    init, gl = blocks(readRaw())
    vals = {k: int(v) for k, v in (l.split(": ") for l in init.splitlines())}
    gates = {c: (a, op, b) for a, op, b, _, c in map(str.split, gl.splitlines())}

    def val(w):
        if w not in vals:
            a, op, b = gates[w]
            x, y = val(a), val(b)
            vals[w] = x & y if op == "AND" else x | y if op == "OR" else x ^ y
        return vals[w]

    zs = sorted((w for w in gates if w[0] == "z"), reverse=True)
    one = int("".join(str(val(z)) for z in zs), 2)

    # in a ripple-carry adder every gate's role is fixed by its inputs; flag outputs that break the pattern
    uses = defaultdict(set)
    for a, op, b in gates.values():
        uses[a].add(op)
        uses[b].add(op)
    wrong = set()
    for c, (a, op, b) in gates.items():
        xy, first = a[0] in "xy" and b[0] in "xy", "x00" in (a, b)
        if c[0] == "z" and op != "XOR" and c != zs[0]:
            wrong.add(c)
        elif op == "XOR" and not xy and c[0] != "z":
            wrong.add(c)
        elif op == "XOR" and xy and not first and "XOR" not in uses[c]:
            wrong.add(c)
        elif op == "AND" and not first and "OR" not in uses[c]:
            wrong.add(c)
    printParts(one, ",".join(sorted(wrong)))

if __name__ == "__main__":
    main()
