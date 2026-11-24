import re
from utils import printParts, readFile, timeFunction

WORDS = "one two three four five six seven eight nine".split()
VAL = {w: str(i) for i, w in enumerate(WORDS, 1)} | {str(i): str(i) for i in range(1, 10)}
P1 = re.compile(r"[1-9]")
# lookahead so overlapping words like "twone" yield both matches
P2 = re.compile(rf"(?=([1-9]|{'|'.join(WORDS)}))")

def calibrate(lines, pat):
    return sum(int(VAL[(m := pat.findall(l))[0]] + VAL[m[-1]]) for l in lines)

@timeFunction
def main():
    l = readFile(toList=False)
    printParts(calibrate(l, P1), calibrate(l, P2))

if __name__ == "__main__":
    main()
