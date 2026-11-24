from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    lines = readFile(toList=False)
    beams = [0] * len(lines[0])
    beams[lines[0].index("S")] = 1
    splits = 0
    # beams[i] counts the timelines whose beam is in column i
    for line in lines[1:]:
        for i, c in enumerate(line):
            if c == "^" and (n := beams[i]):
                beams[i - 1] += n
                beams[i + 1] += n
                beams[i] = 0
                splits += 1
    printParts(splits, sum(beams))

if __name__ == "__main__":
    main()
