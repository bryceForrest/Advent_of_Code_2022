###############################################################################
# Functions:
###############################################################################

# uses a character code l, r, u, d for left, right, up, down, respectively.
# returns a count of the "visibility score" for that direction
def check_dir(height, matrix, i, j, ch):
    code = {'l' : [0, -1, i, 0], 'r' : [0, 1, i, len(matrix[0]) - 1], \
            'u' : [-1, 0, 0, j], 'd' : [1, 0, len(matrix) - 1, j]}

    i += code[ch][0]
    j += code[ch][1]
    score = 1

    while not(i == code[ch][2] and j == code[ch][3]) and height > matrix[i][j]:
        i += code[ch][0]
        j += code[ch][1]

        score += 1

    return score

# calls check_dir for all directions, multiplies scores
# returns product of scores
def check(height, matrix, i, j):
    score = check_dir(height, matrix, i, j, 'l') * \
            check_dir(height, matrix, i, j, 'r') * \
            check_dir(height, matrix, i, j, 'u') * \
            check_dir(height, matrix, i, j, 'd')

    return score

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

best = 0

# check each inside tree in the matrix
for i in range(1, len(matrix) - 1):
    for j in range(1, len(matrix[0]) - 1):
        height = matrix[i][j]

        best = max(check(height, matrix, i, j), best)
        
print(best)

infile.close()