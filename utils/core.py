import re
import sys
import time
from bisect import bisect_left
from fractions import Fraction
from functools import wraps
from operator import sub
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_INT_RE = re.compile(r"-?\d+")
_DAY_RE = re.compile(r"\d+")


def infer_year():
    """Return the year from the running script's path (2024/day_07/day_07.py -> 2024)."""
    return int(Path(sys.argv[0]).resolve().parent.parent.name)


def infer_day():
    """Return the day from the running script's folder name (2024/day_07/day_07.py -> 7)."""
    return int(_DAY_RE.search(Path(sys.argv[0]).resolve().parent.name)[0])


def input_path(day=None, year=None, isTest=False, name=None):
    """Return <year>/day_XX/<file>.txt, where file is name, else "test" if isTest, else "day_XX".

    day and year default to the running script's.
    """
    d = f"day_{day or infer_day():02}"
    return ROOT / str(year or infer_year()) / d / f"{name or ('test' if isTest else d)}.txt"


def readFile(day=None, year=None, splitOn="", isTest=False, toStrip=True, toList=True, name=None):
    """Read an input file into a list of lines.

    day/year/isTest/name: pick the file (see input_path).
    toStrip: strip each line. splitOn: split each line on this string (r"\\w" splits on any whitespace).
    toList: turn each unsplit line into a list of characters.
    """
    lines = input_path(day, year, isTest, name).read_text(encoding="utf-8-sig").splitlines()
    if toStrip:
        lines = [l.strip() for l in lines]
    if splitOn:
        return [l.split() for l in lines] if splitOn == r"\w" else [l.split(splitOn) for l in lines]
    return [list(l) for l in lines] if toList else lines


def readRaw(day=None, year=None, isTest=False, name=None):
    """Return the whole input file as one string without the trailing newline."""
    return input_path(day, year, isTest, name).read_text(encoding="utf-8-sig").rstrip("\n")


def blocks(text):
    """Split text into the chunks separated by blank lines."""
    return text.split("\n\n")


def ints(s):
    """Return every (possibly negative) integer in string s."""
    return list(map(int, _INT_RE.findall(s)))


def windows(seq, n):
    """Iterate over every length-n sliding window of a sliceable seq, as tuples."""
    return zip(*(seq[i:] for i in range(n)))


def transpose(rows):
    """Return the columns of a list of equal-length rows, as tuples."""
    return list(zip(*rows))


def timeFunction(func):
    """Decorator that prints how long func took, in ms."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.perf_counter()
        res = func(*args, **kwargs)
        print(f"Time taken ({func.__name__}): {(time.perf_counter() - t) * 1000:.3f} ms")
        return res
    return wrapper


def printParts(part1, part2):
    """Print the answers for part 1 and part 2 (check.py parses these lines)."""
    print(f"Part 1: {part1}\nPart 2: {part2}")


def manhattan(a, b):
    """Manhattan distance between two equal-length coordinate tuples."""
    return sum(map(abs, map(sub, a, b)))


def sign(x):
    """Return -1, 0 or 1 according to the sign of x."""
    return (x > 0) - (x < 0)


def shoelace(pts):
    """Area of a simple polygon given its vertices in order (int when exact, else float)."""
    s = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])))
    return s / 2 if s & 1 else s // 2


def picks_interior(area, boundary):
    """Number of interior lattice points from a lattice polygon's area and boundary point count (Pick's theorem)."""
    return (int(2 * area) - boundary) // 2 + 1


def crt(rems, mods):
    """Solve x = rems[i] (mod mods[i]) for pairwise-coprime mods; returns (x, product of mods)."""
    x, m = 0, 1
    for r, n in zip(rems, mods):
        x += m * ((r - x) * pow(m, -1, n) % n)
        m *= n
    return x % m, m


def solve_linear(A, b):
    """Solve the n x n system Ax = b exactly; returns a list of Fractions, or None if A is singular. O(n^3)."""
    n = len(A)
    M = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(A, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c]), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        inv = 1 / M[c][c]
        pr = M[c] = [v * inv for v in M[c]]
        for r in range(n):
            if r != c and (f := M[r][c]):
                M[r] = [a - f * q for a, q in zip(M[r], pr)]
    return [row[n] for row in M]


def merge_intervals(ivs):
    """Merge overlapping or adjacent inclusive integer (lo, hi) intervals; returns sorted [lo, hi] lists."""
    out = []
    for lo, hi in sorted(ivs):
        if out and lo <= out[-1][1] + 1:
            if hi > out[-1][1]:
                out[-1][1] = hi
        else:
            out.append([lo, hi])
    return out


def bisect_pred(lo, hi, pred):
    """Return the first integer in [lo, hi) where the monotonic pred becomes True, or hi if none."""
    return lo + bisect_left(range(lo, hi), True, key=pred)


def find_cycle(state, step, n):
    """Return the state after applying step n times, skipping ahead once a (hashable) state repeats."""
    seen, hist = {}, []
    for i in range(n):
        if (mu := seen.get(state)) is not None:
            # hist[i] is the state after i steps; the cycle starts at mu and has length i - mu
            return hist[mu + (n - mu) % (i - mu)]
        seen[state] = i
        hist.append(state)
        state = step(state)
    return state
