from utils import printParts, readFile, timeFunction


@timeFunction
def main():
    wins = []
    for line in readFile(toList=False):
        a, b = line.split(":")[1].split("|")
        wins.append(len(set(a.split()) & set(b.split())))
    copies = [1] * len(wins)
    for i, n in enumerate(wins):
        for j in range(i + 1, min(i + 1 + n, len(wins))):
            copies[j] += copies[i]
    printParts(sum(1 << n >> 1 for n in wins), sum(copies))


if __name__ == "__main__":
    main()
