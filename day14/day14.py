import numpy as np

###############################################################################
# Functions
###############################################################################

# builds rock formations based on input
# uses a dict to state whether sand can move through coordinate (air, true)
# or cannot (rock, false)
def build(infile):
    path = infile.readline().strip().split(' -> ')
    rocks = dict()

    while all(path):
        path = np.array([x.split(',') for x in path]).astype('int')

        # from one coordinate to next, iterate through and set coordinates
        # to false to denote rock.
        # Uses np.sign to determine direction
        for i in range(1, len(path)):
            curr = path[i]
            prev = path[i - 1]
            diff = np.subtract(curr, prev)
            sign = np.sign(diff)

            # set position as rock, then all the others until we hit
            # next coordinate
            rocks[tuple(prev)] = False
            while not(np.array_equal(prev, curr)):
                prev = np.add(prev, sign)
                rocks[tuple(prev)] = False

        path = infile.readline().strip().split(' -> ')

    return rocks

def part1(rocks):
    # far edges of rocks to detect falling into the abyss
    bottom = max(rocks.keys(), key = lambda x : x[1])[1]

    # falling into the abyss flag
    abyss = False
    # sand either goes straight down, diagonal left, or diagonal right
    moves = [[0, 1], [-1, 1], [1, 1]]
    # sand unit count
    units = 0

    while not(abyss):
        sand = np.array([500, 0])  # starting point
        falling = True

        while falling:
            # check for abyss
            if sand[1] > bottom:
                abyss = True
                break

            # store current sand position in case we hit a rock
            prev = sand

            # iterate through possible moves until we continue falling
            # or get stuck
            for m in moves:
                sand = np.add(prev, m)
                falling = rocks.setdefault(tuple(sand), True)

                if falling:
                    break
            else:
                rocks[tuple(prev)] = False
        
        # if we are falling into the abyss we won't count current unit
        if not(abyss): units += 1

    return units

# slight variation from day 1 to account for the floor
def part2(rocks):
    # floor
    floor = max(rocks.keys(), key = lambda x : x[1])[1] + 2

    # fell to the floor flag
    filled = False
    # sand either goes straight down, diagonal left, or diagonal right
    moves = [[0, 1], [-1, 1], [1, 1]]
    # sand unit count
    units = 0
    start = np.array([500, 0])  # starting point

    while not(filled):
        sand = start      
        falling = True

        while falling:
            # store current sand position in case we hit a rock
            prev = sand

            # iterate through possible moves until we continue falling
            # or get stuck
            for m in moves:
                sand = np.add(prev, m)

                # if the y coordinate is the floor, assume false
                if sand[1] != floor:
                    falling = rocks.setdefault(tuple(sand), True)
                else:
                    falling = False

                if falling:
                    break
            else:
                rocks[tuple(prev)] = False

            if not(falling) and np.array_equal(prev, start):
                filled = True
        
        # count the units fallen
        units += 1

    return units

###############################################################################
# Main Implementation
###############################################################################

def main():
    infile = open('input.txt', 'r')
    rocks = build(infile)

    # print(part1(rocks))
    print(part2(rocks))
    infile.close()

if __name__=="__main__":
    main()