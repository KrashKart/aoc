from utils import DIRS8, printParts, readFile, timeFunction

@timeFunction
def main():
    g = readFile(toList=False)
    h, w = len(g), len(g[0])
    one = sum(all(0 <= x + k * dx < w and 0 <= y + k * dy < h and g[y + k * dy][x + k * dx] == c
                  for k, c in enumerate("XMAS"))
              for y in range(h) for x in range(w) if g[y][x] == "X" for dx, dy in DIRS8)
    ms = {"M", "S"}
    two = sum(g[y][x] == "A" and {g[y - 1][x - 1], g[y + 1][x + 1]} == ms == {g[y - 1][x + 1], g[y + 1][x - 1]}
              for y in range(1, h - 1) for x in range(1, w - 1))
    printParts(one, two)

if __name__ == "__main__":
    main()
