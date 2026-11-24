from functools import cache
from utils import ints, printParts, readFile, timeFunction

@cache
def arrangements(s, g):
    if not g:
        return "#" not in s
    if not s:
        return 0
    res = arrangements(s[1:], g) if s[0] in ".?" else 0
    n = g[0]
    if s[0] in "#?" and n <= len(s) and "." not in s[:n] and (n == len(s) or s[n] != "#"):
        res += arrangements(s[n + 1:], g[1:])
    return res

@timeFunction
def main():
    rows = [(s, tuple(ints(r))) for s, r in readFile(splitOn=" ")]
    one = sum(arrangements(s, g) for s, g in rows)
    two = sum(arrangements("?".join([s] * 5), g * 5) for s, g in rows)
    printParts(one, two)

if __name__ == "__main__":
    main()
