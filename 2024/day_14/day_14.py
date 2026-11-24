from math import prod
from statistics import pvariance
from utils import crt, ints, printParts, readFile, timeFunction

W, H = 101, 103

@timeFunction
def main():
    bots = [ints(l) for l in readFile(toList=False) if l]
    quads = [0] * 4
    for px, py, vx, vy in bots:
        x, y = (px + 100 * vx) % W, (py + 100 * vy) % H
        if x != W // 2 and y != H // 2:
            quads[(x > W // 2) + 2 * (y > H // 2)] += 1
    # x repeats every W steps and y every H; the tree is where both bunch up most, so combine with CRT
    tx = min(range(W), key=lambda t: pvariance([(px + t * vx) % W for px, _, vx, _ in bots]))
    ty = min(range(H), key=lambda t: pvariance([(py + t * vy) % H for _, py, _, vy in bots]))
    printParts(prod(quads), crt([tx, ty], [W, H])[0])

if __name__ == "__main__":
    main()
