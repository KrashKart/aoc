from functools import cmp_to_key
from utils import blocks, ints, printParts, readRaw, timeFunction

@timeFunction
def main():
    r, u = blocks(readRaw())
    rules = {tuple(ints(l)) for l in r.splitlines()}
    key = cmp_to_key(lambda a, b: -1 if (a, b) in rules else (b, a) in rules)
    one = two = 0
    for up in map(ints, u.splitlines()):
        s = sorted(up, key=key)
        if s == up:
            one += up[len(up) // 2]
        else:
            two += s[len(s) // 2]
    printParts(one, two)

if __name__ == "__main__":
    main()
