import re
from utils import printParts, readRaw, timeFunction

@timeFunction
def main():
    one = two = 0
    on = True
    for m in re.finditer(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)", readRaw()):
        match m[0]:
            case "do()": on = True
            case "don't()": on = False
            case _:
                p = int(m[1]) * int(m[2])
                one += p
                two += p * on
    printParts(one, two)

if __name__ == "__main__":
    main()
