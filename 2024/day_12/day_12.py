from utils import DIRS4, Grid, components, printParts, readRaw, timeFunction

@timeFunction
def main():
    g = Grid.from_chars(readRaw())
    d, nb = g.data, g.nbr4_fn()
    one = two = 0
    for comp in components(range(len(d)), lambda i: (j for j in nb(i) if d[j] == d[i])):
        s = {g.xy(i) for i in comp}
        per = corners = 0
        for x, y in s:
            for k, (ax, ay) in enumerate(DIRS4):
                bx, by = DIRS4[(k + 1) % 4]
                a, b = (x + ax, y + ay) in s, (x + bx, y + by) in s
                per += not a
                # sides == corners: convex where both arms are outside, concave where both are inside but the diagonal isn't
                corners += (not a and not b) or (a and b and (x + ax + bx, y + ay + by) not in s)
        one += len(s) * per
        two += len(s) * corners
    printParts(one, two)

if __name__ == "__main__":
    main()
