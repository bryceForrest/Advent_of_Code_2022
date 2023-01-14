from time import time
from math import gcd
import heapq

# just a container for all the goods
class Valley:
    def __init__(self, start, end, blizzards, height, width):
        self.start = start
        self.end = end
        self.blizzards = blizzards
        self.height = height
        self.width = width

    def move_storms(self):
        add = lambda a, b : tuple(x + y for x, y in zip(a, b))

        for bliz in self.blizzards:
            temp_r, temp_c = add(bliz[0], bliz[1])
            if temp_r == 0:
                temp_r = self.height - 2
            elif temp_r == self.height - 1:
                temp_r = 1
            elif temp_c == 0:
                temp_c = self.width - 2
            elif temp_c == self.width - 1:
                temp_c = 1
                
            bliz[0] = (temp_r, temp_c)

# allows for a heapq priority queue of coordinates
class Coord:
    def __init__(self, pos, dist_to, minutes):
        man_dist = lambda a, b : sum((abs(x - y) for x, y in zip(a, b)))
        self.pos = pos
        self.dist = man_dist(self.pos, dist_to)
        self.minutes = minutes

    def __lt__(self, obj):
        return (self.dist + self.minutes < obj.dist + obj.minutes)
###############################################################################
# Functions
###############################################################################

def test(func, soln):
    """
    Tests against sample input/output

    """
    infile = open("sample_input.txt", "r")
    input = parse(infile)
    infile.close()
    result = func(input)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    """
    Parses input into start/end points, blizzard coordinates and directions,
    and the width and height of the valley
    
    """   
    blizzards = list()
    r, c = (0, 0)
    start = (0, 0)
    end = (0, 0)
    dirs = {'>' : (0, 1), '<' : (0, -1), '^' : (-1, 0), 'v' : (1, 0)}

    grid = list()
    while line := infile.readline().strip():
        grid.append(list(line))

    start = (0, grid[0].index('.'))
    end = (len(grid) - 1, grid[-1].index('.'))

    # find blizzards
    for row in grid:
        for ch in row:
            if ch != '.' and ch != '#':
                blizzards.append([(r, c), dirs[ch]])
            c += 1
        r += 1
        c = 0
    
    return Valley(start, end, blizzards, len(grid), len(grid[0]))

def journey(valley, blizzards, start, end, start_time):
    """
    A* traversal of valley, iterating through blizzard position with
    respect to time
    
    """
    add = lambda a, b : tuple(x + y for x, y in zip(a, b))

    repeat = len(blizzards)
    q = [Coord(start, end, start_time)]
    heapq.heapify(q)
    seen = dict()

    while q:
        curr_coord = heapq.heappop(q)
        curr = curr_coord.pos
        minutes = curr_coord.minutes

        if curr == end:
            break

        next_blizzards = blizzards[(minutes + 1) % repeat]

        nbors = (add(curr, (-1, 0)), add(curr, (1,0)),
                 add(curr, (0, 1)), add(curr, (0, -1)), curr)

        for r, c in nbors:
            if (r, c) == start or (r, c) == end or \
               not(r <= 0 or r == valley.height - 1 or \
               c <= 0 or c == valley.width - 1 or \
               next_blizzards.setdefault((r, c), False) or \
               seen.setdefault(((r, c), minutes + 1), False)):
                    heapq.heappush(q, Coord((r, c), end, minutes + 1))
                    seen[((r, c), minutes + 1)] = True

    return minutes - start_time

def part_1(valley):
    """
    Generates every position of the blizzard with respect to time,
    and calls traversal function.
    
    """
    height = valley.height - 2
    width = valley.width - 2
    # pattern repeats after lcm of height and width
    repeat = (height * width) // gcd(height, width)

    # generate all possible positions of blizzards
    blizzards = []
    for _ in range(repeat):
        blizzards.append({x[0] : True for x in valley.blizzards})
        valley.move_storms()

    return journey(valley, blizzards, valley.start, valley.end, 0)

def part_2(valley):
    """
    Generates every position of the blizzard with respect to time,
    and calls traversal function from start to end, back to start,
    and back to end.
    
    """
    height = valley.height - 2
    width = valley.width - 2
    start = valley.start
    end = valley.end
    # pattern repeats after lcm of height and width
    repeat = (height * width) // gcd(height, width)

    # generate all possible positions of blizzards
    blizzards = []
    for _ in range(repeat):
        blizzards.append({x[0] : True for x in valley.blizzards})
        valley.move_storms()

    trip_1 = journey(valley, blizzards, start, end, 0)
    trip_2 = journey(valley, blizzards, end, start, trip_1)
    trip_3 = journey(valley, blizzards, start, end, trip_1 + trip_2)

    return trip_1 + trip_2 + trip_3

###############################################################################
# Implementation
###############################################################################

def main():
    test(part_1, 18)
    test(part_2, 54)

    infile = open("input.txt", "r")
    valley = parse(infile)
    infile.close()

    start = time()
    print("Results for part 1:", part_1(valley))
    print("Time taken: {:.2f}".format(time() - start))

    infile = open("input.txt", "r")
    valley = parse(infile)
    infile.close()

    start = time()
    print("Results for part 2:", part_2(valley))
    print("Time taken: {:.2f}".format(time() - start))

if __name__ == "__main__": main()