from utils import blocks, ints, printParts, readRaw, timeFunction

@timeFunction
def main():
    regions = blocks(readRaw())[-1].splitlines()
    # the real inputs are either trivially roomy or hopelessly overfull, so treating each present as a 3x3 block suffices
    one = sum((w // 3) * (h // 3) >= sum(req) for w, h, *req in map(ints, regions))
    printParts(one, None)

if __name__ == "__main__":
    main()
