from utils import DIRMAP, blocks, printParts, readRaw, timeFunction

WIDEN = str.maketrans({"#": "##", ".": "..", "O": "[]", "@": "@."})

def gps(rows, moves):
    grid = {(x, y): c for y, r in enumerate(rows.splitlines()) for x, c in enumerate(r)}
    pos = next(p for p, c in grid.items() if c == "@")
    for m in moves:
        dx, dy = DIRMAP[m]
        # collect everything the robot would shove; a wide box drags its other half along
        push, seen = [pos], {pos}
        for x, y in push:
            n = (x + dx, y + dy)
            match grid[n]:
                case "#":
                    break
                case "O" | "[" | "]" as c:
                    for q in (n, (n[0] + (1 if c == "[" else -1), n[1])) if c != "O" else (n,):
                        if q not in seen:
                            seen.add(q)
                            push.append(q)
        else:
            moved = {(x + dx, y + dy): grid[x, y] for x, y in push}
            grid.update(dict.fromkeys(push, "."))
            grid.update(moved)
            pos = (pos[0] + dx, pos[1] + dy)
    return sum(100 * y + x for (x, y), c in grid.items() if c in "O[")

@timeFunction
def main():
    rows, moves = blocks(readRaw())
    moves = moves.replace("\n", "")
    printParts(gps(rows, moves), gps(rows.translate(WIDEN), moves))

if __name__ == "__main__":
    main()
