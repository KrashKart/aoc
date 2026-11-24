from utils import blocks, printParts, readRaw, timeFunction, transpose


def mirror(rows, smudges):
    for i in range(1, len(rows)):
        if sum(a != b for r1, r2 in zip(rows[i - 1::-1], rows[i:]) for a, b in zip(r1, r2)) == smudges:
            return i
    return 0


def score(p, smudges):
    return 100 * mirror(p, smudges) or mirror(transpose(p), smudges)


@timeFunction
def main():
    pats = [b.splitlines() for b in blocks(readRaw())]
    printParts(sum(score(p, 0) for p in pats), sum(score(p, 1) for p in pats))


if __name__ == "__main__":
    main()
