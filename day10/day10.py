infile = open("input.txt", "r")

line = infile.readline().split()

# number of cycles per operation
cycle_num = {"noop" : 1, "addx" : 2}
cycle_count = 0     # cycle counter
x = 1               # register x
cycle_mark = 20     # tracking important cycles
values = []         # value at important cycles

while line:
    curr_cyc = cycle_num[line[0]]                   # number of cycles
    v = 0 if line[0] == "noop" else int(line[1])    # 0 if noop, V if addx

    # loop for number of cycles
    # if it's an important cycle, add it to the list
    for i in range(curr_cyc):
        cycle_count += 1

        if cycle_count == cycle_mark:
            values.append(x * cycle_mark)
            cycle_mark += 40

    # add V to X register
    x += v

    line = infile.readline().split()

# print the sum of signal strengths
print(sum(values))

infile.close