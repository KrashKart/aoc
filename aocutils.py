import time
import typing

def readFile(day: int, splitOn: str = "", isTest: bool = False, toStrip: bool = True, toList: bool = True) -> list[str]:
    """Reads input file given the day. Ensure file is stored as txts/day-XX.txt or txts/day-XX_test.txt for test input. 
    
    Arguments:
    day - the day of the challenge (1-25)
    splitOn - the string to split each line on (default: "")
    isTest - whether to read the test input file (default: False)
    toStrip - whether to strip whitespace from each line (default: True)
    toList - whether to convert each line to a list (default: True)

    Returns a list of strings, one for each line in the file.
    """
    res = []
    filename = f"txts/day-{day:02}.txt" if not isTest else f"txts/day-{day:02}_test.txt"
    with open(filename, "r") as f:
        for line in f:
            if toStrip:
                line = line.strip()
            if splitOn:
                if splitOn == r"\w":
                    line = line.split()
                else:
                    line = line.split(splitOn)
            if toList:
                line = list(line)
            res.append(line)
    return res

def timeFunction(func):
    """Wrapper to time main() in day.py files"""
    def wrapper(*args, **kwargs):
        startTime = time.time()
        res = func(*args, **kwargs)
        print(f"Time taken ({func.__name__}): {time.time() - startTime}")
        return res
    return wrapper

def printParts(part1, part2):
    """Prints the results of part 1 and part 2."""
    print("Part 1: " + str(part1))
    print("Part 2: " + str(part2))