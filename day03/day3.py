import math
from time import time


def parse():
    in_file = open("input.txt", "r")
    rucksack = list()
    while line := in_file.readline().strip():
        rucksack.append(line)

    in_file.close()

    return rucksack


def part_1():
    rucksack = parse()
    total_priority = 0

    for line in rucksack:
        compartment_1 = line[:math.floor(len(line) / 2)]
        compartment_2 = line[math.floor(len(line) / 2):]

        item = ""

        for i in compartment_1:
            index = compartment_2.find(i)
            if index != -1:
                item = compartment_2[index]
                break

        if item.isupper():
            total_priority += ord(item) - 38
        else:
            total_priority += ord(item) - 96

    return total_priority


def part_2():
    rucksack = parse()
    total_priority = 0

    for i in range(0, len(rucksack), 3):
        rucksack_1 = rucksack[i]
        rucksack_2 = rucksack[i + 1]
        rucksack_3 = rucksack[i + 2]
        for j in rucksack_1:
            index_1 = rucksack_2.find(j)
            index_2 = rucksack_3.find(j)

            if index_1 != -1 and index_2 != -1:
                item = rucksack_2[index_1]
                break

        if item.isupper():
            total_priority += ord(item) - 38
        else:
            total_priority += ord(item) - 96

    return total_priority


start = time()
print("Results for part 1:", part_1())
print("Time taken: {:.2f}".format(time() - start))

start = time()
print("Results for part 2:", part_2())
print("Time taken: {:.2f}".format(time() - start))
