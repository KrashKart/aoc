from utils import ints, printParts, readFile, timeFunction

def solvable(t, ns, cat):
    """Work backwards from the target, undoing the last operator, which prunes far more than going forwards."""
    *rest, last = ns
    if not rest:
        return t == last
    if t > last and solvable(t - last, rest, cat):
        return True
    if t % last == 0 and solvable(t // last, rest, cat):
        return True
    m = 10 ** len(str(last))
    return cat and t > last and t % m == last and solvable(t // m, rest, cat)

@timeFunction
def main():
    eqs = [ints(l) for l in readFile(toList=False) if l]
    one = sum(t for t, *ns in eqs if solvable(t, ns, False))
    two = sum(t for t, *ns in eqs if solvable(t, ns, True))
    printParts(one, two)

if __name__ == "__main__":
    main()
