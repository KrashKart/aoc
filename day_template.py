from utils import DIRS4, Grid, bfs, blocks, ints, printParts, readFile, readRaw, timeFunction


@timeFunction
def main():
    one, two = 0, 0
    t = False
    l = readFile(isTest=t, toList=False)

    printParts(one, two)


if __name__ == "__main__":
    main()
