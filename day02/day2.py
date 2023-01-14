from time import time

lose = {"A": "Z", "B": "X", "C": "Y"}
win = {"A": "Y", "B": "Z", "C": "X"}
draw = {"A": "X", "B": "Y", "C": "Z"}
shape = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}


def part_1(f_stream):
    score = 0

    while game := f_stream.readline():
        elf = game[0]
        me = game[2]
        if win[elf] == me:
            score += 6 + shape[me]
        elif lose[elf] == me:
            score += shape[me]
        else:
            score += 3 + shape[me]

    return score


def part_2(f_stream):
    score = 0

    while game := f_stream.readline():
        elf = game[0]

        outcome = game[2]

        if outcome == "X":
            me = lose[elf]
            score += shape[me]
        elif outcome == "Y":
            me = draw[elf]
            score += 3 + shape[me]
        else:
            me = win[elf]
            score += 6 + shape[me]

    return score


start = time()
f_stream = open("input.txt", "r")
print("Result for part 1:", part_1(f_stream))
print("Time taken: {:.2f} seconds".format(time() - start))
f_stream.close()

start = time()
f_stream = open("input.txt", "r")
print("Result for part 2:", part_2(f_stream))
print("Time taken: {:.2f} seconds".format(time() - start))
f_stream.close()
