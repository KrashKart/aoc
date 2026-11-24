from utils import printParts, readFile, timeFunction

def joltage(s, n):
    """Largest n-digit number keeping s's order: greedily take the biggest digit that leaves room for the rest."""
    out, i = "", 0
    for r in range(n, 0, -1):
        window = s[i:len(s) - r + 1]
        c = max(window)
        i += window.index(c) + 1
        out += c
    return int(out)

@timeFunction
def main():
    banks = [l for l in readFile(toList=False) if l]
    printParts(sum(joltage(b, 2) for b in banks), sum(joltage(b, 12) for b in banks))

if __name__ == "__main__":
    main()
