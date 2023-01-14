from time import time


def parse():
    bestElves = set()
    current = 0
    inFile = open("input.txt", "r")
    while line := inFile.readline():
        if line == "\n":
            bestElves.add(current)
            current = 0
        else:
            current += int(line)

    return (bestElves, current)


bestElves, current = parse()

start = time()

print("Results for part 1:", max(bestElves))
print("Time taken: {:.2f} seconds".format(time() - start))

start = time()

sortedElves = sorted(bestElves, reverse=True)
sum = sum(sortedElves[:3])

print("Results for part 2:", sum)
print("Time taken: {:.2f} seconds".format(time() - start))
