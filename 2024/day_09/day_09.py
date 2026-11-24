from heapq import heappop, heappush
from utils import printParts, readRaw, timeFunction

def compact_blocks(disk):
    mem = [i // 2 if i % 2 == 0 else -1 for i, n in enumerate(disk) for _ in range(n)]
    l, r = 0, len(mem) - 1
    while True:
        while mem[l] != -1:
            l += 1
        while mem[r] == -1:
            r -= 1
        if l >= r:
            return sum(i * v for i, v in enumerate(mem) if v != -1)
        mem[l], mem[r] = mem[r], -1

def compact_files(disk):
    # gaps[s] is a min-heap of start positions of free spans of length s
    files, gaps, pos = [], [[] for _ in range(10)], 0
    for i, n in enumerate(disk):
        if i % 2 == 0:
            files.append([pos, n, i // 2])
        elif n:
            heappush(gaps[n], pos)
        pos += n
    for f in reversed(files):
        p, n, _ = f
        best = min(((gaps[s][0], s) for s in range(n, 10) if gaps[s]), default=None)
        if best and best[0] < p:
            start, s = best
            heappop(gaps[s])
            f[0] = start
            if s > n:
                heappush(gaps[s - n], start + n)
    return sum(i * (p * n + n * (n - 1) // 2) for p, n, i in files)

@timeFunction
def main():
    disk = list(map(int, readRaw().strip()))
    printParts(compact_blocks(disk), compact_files(disk))

if __name__ == "__main__":
    main()
