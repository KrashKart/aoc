from aocutils import readFile, timeFunction, printParts

@timeFunction
def main():
    one, two = 0, 0
    t = False
    l = readFile(1, toList=False, isTest=t)

    printParts(one, two)
    pass
    
if __name__ == "__main__":
    main()