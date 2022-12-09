###############################################################################
# Functions:
###############################################################################

# uses a character code l, r, u, d for left, right, up, down, respectively.
# returns a bool value of whether the tree is visible
def check_dir(height, matrix, i, j, ch):
    visible = False
    code = {'l' : [0, -1, i, -1], 'r' : [0, 1, i, len(matrix[0])], \
            'u' : [-1, 0, -1, j], 'd' : [1, 0, len(matrix), j]}

    i += code[ch][0]
    j += code[ch][1]

    while not(i == code[ch][2] and j == code[ch][3]) and height > matrix[i][j]:
        i += code[ch][0]
        j += code[ch][1]

        if i == code[ch][2] and j == code[ch][3]:
            visible = True
            break 

    return visible

# calls check_dir for all directions
def check(height, matrix, i, j):
    visible = False
    if check_dir(height, matrix, i, j, 'l') or \
       check_dir(height, matrix, i, j, 'r') or \
       check_dir(height, matrix, i, j, 'u') or \
       check_dir(height, matrix, i, j, 'd'):
        visible = True

    return visible

###############################################################################
# Implementation:
###############################################################################

infile = open("input.txt", "r")

line = infile.readline()
matrix = []

# build matrix
while line:
    matrix.append(list(line.strip()))
    line = infile.readline()

count = 0

# check each inside tree in the matrix
for i in range(1, len(matrix) - 1):
    for j in range(1, len(matrix[0]) - 1):
        height = matrix[i][j]

        if check(height, matrix, i, j):
            count += 1
        
# account for outside trees
outside = 2 * len(matrix) + 2 * (len(matrix[0]) - 2)

print(outside + count)

infile.close()