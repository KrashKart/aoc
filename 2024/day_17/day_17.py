from utils import ints, printParts, readRaw, timeFunction

def run(prog, a, b, c):
    ip, out = 0, []
    while ip < len(prog):
        op, x = prog[ip], prog[ip + 1]
        combo = (0, 1, 2, 3, a, b, c, 0)[x]
        match op:
            case 0: a >>= combo
            case 1: b ^= x
            case 2: b = combo & 7
            case 3 if a:
                ip = x
                continue
            case 4: b ^= c
            case 5: out.append(combo & 7)
            case 6: b = a >> combo
            case 7: c = a >> combo
        ip += 2
    return out

@timeFunction
def main():
    a, b, c, *prog = ints(readRaw())
    # each loop prints one digit then shifts A right 3 bits, so build A 3 bits at a time from the last output
    cands = [0]
    for k in range(len(prog) - 1, -1, -1):
        cands = [n for a8 in cands for t in range(8) if run(prog, n := a8 * 8 + t, b, c) == prog[k:]]
    printParts(",".join(map(str, run(prog, a, b, c))), min(cands))

if __name__ == "__main__":
    main()
