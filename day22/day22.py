import re
import numpy as np
from time import time

###############################################################################
# Functions
###############################################################################

def test(func, soln):
    """
    Tests against sample input/output

    The sample cube for part 2 is folded differently than the real input
    so part 2 doesn't work on the sample input. Sad.
    
    """
    infile = open('sample_input.txt', 'r')
    board, path = parse(infile)
    infile.close()
    result = func(board, path)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)

    print(msg)

def parse(infile):
    """
    Parses input into a board and path

    """
    line = infile.readline()
    board = list()

    while line != '\n':
        board.append(list(line.rstrip()))
        line = infile.readline()

    # normalize board size
    width = max([len(x) for x in board])
    for row in board:
        diff = width - len(row)
        row += [' '] * diff

    line = infile.readline().strip()
    path = tuple(zip(map(int, re.split('[A-Z]', line)),
                     re.split('[0-9]+', line)))

    return board, path

def part_1(board, path):
    """
    Adds a direction to the current coordinate and checks it for validity.
    If it's a ' ', loop around and iterate until we find the next '.'.
    If it's a '#', don't change the current coordinate, because we're stuck
    If it's a '.', it's a valid move, so update the coordinates
    
    """
    # find start position
    for i, ch in enumerate(board[0]):
        if ch != ' ':
            break

    facing = ((0, 1), (1, 0), (0, -1), (-1, 0))
    facing_index = 0
    current = (0, i)
    height = len(board)
    width = len(board[0])

    new_dir = lambda x, y : (x + {'R' : 1, 'L' : -1, '' : 0}[y]) % 4
    add_dir = lambda a, b : tuple((x + y for x, y in zip(a, b)))

    # get the distance and direction of the next move
    for dist, dir in path:
        facing_index = new_dir(facing_index, dir)

        # then move that direction, dist many times
        for _ in range(dist):
            temp_r, temp_c = add_dir(current, facing[facing_index])
            temp_r %= height
            temp_c %= width

            # if we hit a blank, iterate to the next valid '.' space
            while board[temp_r][temp_c] == ' ':
                temp_r, temp_c = add_dir((temp_r, temp_c), facing[facing_index])
                temp_r %= height
                temp_c %= width

            if board[temp_r][temp_c] == '.':
                current = (temp_r, temp_c)

    row, col = current
    return (1000 * (row + 1) + (4 * (col + 1) + facing_index))

def part_2(board, path):
    """
    Bit of a disaster-piece. Mangled part 1 to cooperate with "folding" the 
    board into a cube.
    Used numpy to split board into n x n sized boards, to act as
    cube faces.
    Then I did some disgusting if elif elif elif to establish what moving
    off of one cube face onto another will do to the coordinates and direction.

    """
    facing = ((0, 1), (1, 0), (0, -1), (-1, 0))
    facing_index = 0

    height = len(board)
    width = len(board[0])
    face = int(((height * width) / 12) ** 0.5)

    # split board into cube faces
    temp_board = np.vsplit(np.array(board), height // face)   

    new_board = []
    for row in temp_board:
        new_row = np.hsplit(row, width // face)
        new_board += new_row

    # build cube
    cube = []
    coords = []

    for i, block in enumerate(new_board):
        if not(np.all(block == ' ')):
            cube.append(block)
            coords.append((((i * face) // width) * face, ((i * face) % width)))


    new_dir = lambda x, y : (x + {'R' : 1, 'L' : -1, '' : 0}[y]) % 4
    add_dir = lambda a, b : tuple((x + y for x, y in zip(a, b)))

    curr_face = 0
    current = (0,0)

    # get the distance and direction of the next move
    for dist, dir in path:
        facing_index = new_dir(facing_index, dir)

        # then move that direction, dist many times
        for _ in range(dist):
            r, c = current
            temp_r, temp_c = add_dir(current, facing[facing_index])
            next_face = curr_face
            next_dir = facing_index

            # detect edge-crossing
            if temp_r < 0 or temp_r == face or \
               temp_c < 0 or temp_c == face:

                # lord, forgive me my sins
                if curr_face == 0:
                    if facing_index == 0:
                        next_face = 1
                        temp_r, temp_c = (r, 0)
                        next_dir = 0
                    elif facing_index == 1:
                        next_face = 2
                        temp_r, temp_c = (0, c)
                        next_dir = 1
                    elif facing_index == 2:
                        next_face = 3
                        temp_r, temp_c = (face - r - 1, 0)
                        next_dir = 0
                    elif facing_index == 3:
                        next_face = 5
                        temp_r, temp_c = (c, 0)
                        next_dir = 0

                elif curr_face == 1:
                    if facing_index == 0:
                        next_face = 4
                        temp_r, temp_c = (face - r - 1, face - 1)
                        next_dir = 2
                    elif facing_index == 1:
                        next_face = 2
                        temp_r, temp_c = (c, face - 1)
                        next_dir = 2
                    elif facing_index == 2:
                        next_face = 0
                        temp_r, temp_c = (r, face - 1)
                        next_dir = 2
                    elif facing_index == 3:
                        next_face = 5
                        temp_r, temp_c = (face - 1, c)
                        next_dir = 3

                elif curr_face == 2:
                    if facing_index == 0:
                        next_face = 1
                        temp_r, temp_c = (face - 1, r)
                        next_dir = 3
                    elif facing_index == 1:
                        next_face = 4
                        temp_r, temp_c = (0, c)
                        next_dir = 1
                    elif facing_index == 2:
                        next_face = 3
                        temp_r, temp_c = (0, r)
                        next_dir = 1
                    elif facing_index == 3:
                        next_face = 0
                        temp_r, temp_c = (face - 1, c)
                        next_dir = 3

                elif curr_face == 3:
                    if facing_index == 0:
                        next_face = 4
                        temp_r, temp_c = (r, 0)
                        next_dir = 0
                    elif facing_index == 1:
                        next_face = 5
                        temp_r, temp_c = (0, c)
                        next_dir = 1
                    elif facing_index == 2:
                        next_face = 0
                        temp_r, temp_c = (face - r - 1, 0)
                        next_dir = 0
                    elif facing_index == 3:
                        next_face = 2
                        temp_r, temp_c = (c, 0)
                        next_dir = 0

                elif curr_face == 4:
                    if facing_index == 0:
                        next_face = 1
                        temp_r, temp_c = (face - r - 1, face - 1)
                        next_dir = 2
                    elif facing_index == 1:
                        next_face = 5
                        temp_r, temp_c = (c, face - 1)
                        next_dir = 2
                    elif facing_index == 2:
                        next_face = 3
                        temp_r, temp_c = (r, face - 1)
                        next_dir = 2
                    elif facing_index == 3:
                        next_face = 2
                        temp_r, temp_c = (face - 1, c)
                        next_dir = 3

                elif curr_face == 5:
                    if facing_index == 0:
                        next_face = 4
                        temp_r, temp_c = (face - 1, r)
                        next_dir = 3
                    elif facing_index == 1:
                        next_face = 1
                        temp_r, temp_c = (0, c)
                        next_dir = 1
                    elif facing_index == 2:
                        next_face = 0
                        temp_r, temp_c = (0, r)
                        next_dir = 1
                    elif facing_index == 3:
                        next_face = 3
                        temp_r, temp_c = (face - 1, c)
                        next_dir = 3


            if cube[next_face][temp_r][temp_c] == '.':
                current = (temp_r, temp_c)
                facing_index = next_dir
                curr_face = next_face

    r, c = current
    row = coords[curr_face][0] + r
    col = coords[curr_face][1] + c

    return (1000 * (row + 1) + (4 * (col + 1) + facing_index))

###############################################################################
# Implementation
###############################################################################

def main():
    test(part_1, 6032)
    test(part_2, 5031)

    infile = open("input.txt", "r")
    board, path = parse(infile)


    start = time()
    print("Solution for part 1:", part_1(board.copy(), path))
    print("Time taken: {:.2f}".format(time() - start))

    start = time()
    print("Solution for part 2:", part_2(board.copy(), path))
    print("Time taken: {:.2f}".format(time() - start))

if __name__ == '__main__': main()