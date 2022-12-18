infile = open("input.txt", "r")

line = infile.readline().split()

# number of cycles per operation
cycle_num = {"noop" : 1, "addx" : 2}
cycle_count = 0     # cycle counter
x = 1               # register x
cycle_mark = 20     # tracking important cycles
values = []         # value at important cycles

# constant screen dimensions
ROWS = 6
COLS = 40

# double comprehension to make a list of lists
screen = list(list("." for x in range(COLS)) for y in range(ROWS))
scr_index = 0

while line:
    curr_cyc = cycle_num[line[0]]                   # number of cycles
    v = 0 if line[0] == "noop" else int(line[1])    # 0 if noop, V if addx

    # loop for number of cycles
    for i in range(curr_cyc):
        pos = x % COLS      # x is horizontal position of sprite

        # sprite is 3 pixels wide, so check the range around x
        # if in range, print a '#'
        if scr_index % COLS in range(pos - 1, pos + 2):
            screen[scr_index // COLS][scr_index % COLS] = '#'

        # update cycle_count and scr_index
        cycle_count += 1
        scr_index += 1

    # add V to X register
    x += v
    line = infile.readline().split()

# print the screen
for i in screen:
    print(*i)

infile.close