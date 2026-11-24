from itertools import combinations
from utils import ints, printParts, readFile, solve_linear, timeFunction

LO, HI = 200000000000000, 400000000000000

def crosses(a, b):
    px1, py1, _, vx1, vy1, _ = a
    px2, py2, _, vx2, vy2, _ = b
    if not (det := vx1 * vy2 - vy1 * vx2):
        return False
    dx, dy = px2 - px1, py2 - py1
    t, s = (dx * vy2 - dy * vx2) / det, (dx * vy1 - dy * vx1) / det
    return t >= 0 and s >= 0 and LO <= px1 + t * vx1 <= HI and LO <= py1 + t * vy1 <= HI

def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def crossmat(b):
    """Matrix M with M @ a == a x b."""
    return [[0, b[2], -b[1]], [-b[2], 0, b[0]], [b[1], -b[0], 0]]

@timeFunction
def main():
    hails = [ints(l) for l in readFile(toList=False) if l]
    one = sum(crosses(a, b) for a, b in combinations(hails, 2))

    # (P - p_i) x (V - v_i) = 0; differencing hail pairs cancels P x V, leaving
    # P x (v_j - v_i) + (p_j - p_i) x V = p_j x v_j - p_i x v_i  (linear in P, V)
    A, b = [], []
    (p0, v0), *rest = ((h[:3], h[3:]) for h in hails[:3])
    for pj, vj in rest:
        mv = crossmat([q - r for q, r in zip(vj, v0)])
        mp = crossmat([q - r for q, r in zip(pj, p0)])
        A += [rv + [-x for x in rp] for rv, rp in zip(mv, mp)]
        b += [q - r for q, r in zip(cross(pj, vj), cross(p0, v0))]
    printParts(one, int(sum(solve_linear(A, b)[:3])))

if __name__ == "__main__":
    main()
