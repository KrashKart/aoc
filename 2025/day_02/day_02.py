from utils import printParts, readRaw, timeFunction

def invalid(lo, hi, halves_only):
    """IDs in [lo, hi] that are some digit block repeated (exactly twice if halves_only)."""
    out = set()
    for L in range(len(str(lo)), len(str(hi)) + 1):
        for k in ([L // 2] if L % 2 == 0 else []) if halves_only else [k for k in range(1, L) if L % k == 0]:
            rep = (10 ** L - 1) // (10 ** k - 1)
            for p in range(max(10 ** (k - 1), -(-lo // rep)), min(10 ** k - 1, hi // rep) + 1):
                out.add(p * rep)
    return out

@timeFunction
def main():
    rngs = [tuple(map(int, r.split("-"))) for r in readRaw().strip().split(",")]
    printParts(*(sum(sum(invalid(lo, hi, h)) for lo, hi in rngs) for h in (True, False)))

if __name__ == "__main__":
    main()
