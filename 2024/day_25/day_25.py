import aocutils
from itertools import product 

def sumHeights(item):
	res = [-1 for _ in item[0]]
	for line in item:
		for idx, pin in enumerate(line):
			res[idx] += 1 if pin == "#" else 0
	return res

def canFit(lock, key):
	for i, j in zip(lock, key):
		if i + j > 5:
			return False
	return True

@aocutils.timeFunction
def main():
	ref = aocutils.readFile(25, isTest=False)
	locks, keys = [], []
	for r in range(0, len(ref), 8):
		curr = ref[r:r + 7]
		if all([i == "#" for i in curr[0]]):
			locks.append(sumHeights(curr))
		else:
			keys.append(sumHeights(curr))
	
	total = 0
	for lock, key in product(locks, keys):
		if canFit(lock, key):
			total += 1

	print(f"Final: {total}")

if __name__ == "__main__":
	main()