from utils import printParts, readFile, timeFunction

@timeFunction
def main():
    one = two = 0
    p = 50
    for line in readFile(toList=False):
        if not line:
            continue
        n = int(line[1:])
        if line[0] == "R":
            two += (p + n) // 100
            p = (p + n) % 100
        else:
            # clicks k in 1..n land on 0 when k = p, p + 100, ... (k = 100, 200, ... from 0)
            two += (-p % 100 + n) // 100
            p = (p - n) % 100
        one += p == 0
    printParts(one, two)

if __name__ == "__main__":
    main()
