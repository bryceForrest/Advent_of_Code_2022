from functools import total_ordering, cmp_to_key
from itertools import zip_longest

class Buffer:
    def __init__(self, string):
        self.buffer = list(string)

    def read(self):
        ret = ''
        if self.buffer:
            ret = self.buffer.pop(0)
        return ret

    def peek(self):
        ret = ''
        if self.buffer:
            ret = self.buffer[0]
        return ret

# Global consts

VALID = -1
INVALID = 1
CONT = 0

# Functions
def build_list(stream):
    lst = list()
    ch = stream.read()

    while ch:
        if ch == ']':
            return lst
        if ch == '[':
            lst.append(build_list(stream))
        if ch.isdigit():
            str_num = ch
            while stream.peek().isdigit():
                ch = stream.read()
                str_num += ch
            lst.append(int(str_num))
        ch = stream.read()

    return lst if len(lst) > 1 else lst[0]

# taken from "What’s New In Python 3.0"
def cmp(a, b):
    return (a > b) - (a < b) 

def rules(left, right):
    valid = CONT

    if left is None:
        return VALID
    elif right is None:
        return INVALID

    if isinstance(left, int) and isinstance(right, int):
        return cmp(left, right)

    elif isinstance(left, list) and isinstance(right, list):
        for i, j in zip_longest(left, right):
            valid = rules(i, j)
            if valid != CONT:
                return valid
        return CONT
    else:
        left = [left] if isinstance(left, int) else left
        right = [right] if isinstance(right, int) else right
        return rules(left, right)

# Implementation
infile = open('input.txt', 'r')

input_1 = infile.readline()
input_2 = infile.readline()
index = 1
sum = 0

#part 2
packets = list()
dividers = [[[2]], [[6]]]

while input_1 and input_2:
    left = build_list(Buffer(input_1))
    right = build_list(Buffer(input_2))

    packets.append(left)
    packets.append(right)

    if rules(left, right) == VALID:
        sum += index

    index += 1

    infile.readline() # blank line
    input_1 = infile.readline()
    input_2 = infile.readline()  

print(sum)      # part 1

packets.extend(dividers)
packets.sort(key = cmp_to_key(rules))

decoder = 1
for d in dividers:
    decoder *= packets.index(d) + 1

print(decoder)

infile.close