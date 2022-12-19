maxCal = 0
elfCount = 0
bestElves = set()
current = 0

inFile = open("input.txt", "r")
line = inFile.readline()

while line:
    if line == '\n':
        bestElves.add(current)

        current = 0
        elfCount += 1
    else:
        current += int(line)

    line = inFile.readline()

bestElves.add(current)

sortedElves = sorted(bestElves)
sum = 0
for i in range(0,3):
    sum += sortedElves.pop()

print(sum)