import numpy as np

def touching(h, t):
    ret = False
    diff = np.subtract(np.array(h), np.array(t))
    if all(np.less_equal(np.absolute(diff), np.array([1,1]))):
        ret = True

    return ret

def move(h,t):
    diff = np.subtract(np.array(h), np.array(t))
    direction = np.sign(diff)

    return direction

infile = open("input.txt", "r")
line = infile.readline().split()

h = np.array([0,0])         # head index
t = np.array([0,0])         # tail index

# for pt. 1, knots = 2
KNOTS = 10
rope = [np.array([0,0]) for x in range(KNOTS)]

code = {'U' : [1, 0], 'D' : [-1, 0], 'L' : [0, -1], 'R' : [0, 1]}
tail_pos = set()

while line:
    hm = np.array(code[line[0]])    # hm is head move
    n = int(line[1])                # n is number of times

    # for the number of times n, move the head in direction hm
    for i in range(0, n):
        # move head
        rope[0] = np.add(rope[0], hm)

        for k in range(1, KNOTS):
            if not(touching(rope[k - 1], rope[k])):
                tm = move(rope[k - 1], rope[k])
                rope[k] = np.add(rope[k], tm)

            # add tail position to tail_pos set to track number visited         
            tail_pos.add(tuple(rope[KNOTS - 1]))

    line = infile.readline().split()

print(len(tail_pos))
infile.close()