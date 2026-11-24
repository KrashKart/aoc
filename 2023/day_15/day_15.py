from functools import reduce
from utils import printParts, readRaw, timeFunction

def hsh(s):
    return reduce(lambda a, c: (a + ord(c)) * 17 % 256, s, 0)

@timeFunction
def main():
    steps = readRaw().strip().split(",")
    boxes = [{} for _ in range(256)]
    for s in steps:
        if s[-1] == "-":
            boxes[hsh(s[:-1])].pop(s[:-1], None)
        else:
            k, v = s.split("=")
            boxes[hsh(k)][k] = int(v)
    two = sum(i * j * v for i, b in enumerate(boxes, 1) for j, v in enumerate(b.values(), 1))
    printParts(sum(map(hsh, steps)), two)

if __name__ == "__main__":
    main()
