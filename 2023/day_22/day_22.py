from utils import ints, printParts, readFile, timeFunction


@timeFunction
def main():
    bricks = sorted((ints(l) for l in readFile(toList=False) if l), key=lambda b: b[2])
    top, sup = {}, []
    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        cells = [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
        z = max((top[c][0] for c in cells if c in top), default=0)
        sup.append({top[c][1] for c in cells if c in top and top[c][0] == z})
        for c in cells:
            top[c] = (z + z2 - z1 + 1, i)
    one = len(bricks) - len({next(iter(s)) for s in sup if len(s) == 1})
    two = 0
    # supporters always have a lower index, so one forward pass settles each chain reaction
    for i in range(len(bricks)):
        fallen = {i}
        for j in range(i + 1, len(bricks)):
            if sup[j] and sup[j] <= fallen:
                fallen.add(j)
        two += len(fallen) - 1
    printParts(one, two)


if __name__ == "__main__":
    main()
