import re
import time

# parse input into coordinate list
def parse(infile):
    coord_lst = list()

    line = infile.readline()

    while line:
        coord = list(map(int, re.findall(r"([\-\d]+)", line)))
        coord.append(manhattan(coord[0], coord[1], coord[2], coord[3]))
        coord_lst.append(coord)
        line = infile.readline()

    return coord_lst

# manhattan distance
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# checks coordinate on line y_val directly below a sensor, (x1, y_val), and
# fills in values in each direction for the difference between the 
# manhattan distance and the distance to the point (x1, y_val)
def part_1(coord_list, y_val):
    no_beacon = set()

    for x1, y1, x2, y2, dist in coord_list:
        temp_dist = manhattan(x1, y1, x1, y_val)
        if dist >= temp_dist:
            diff = dist - temp_dist
            for r in range(x1 - diff, x1 + diff + 1):
                if (r, y_val) != (x2, y2):
                    no_beacon.add((r, y_val))

    return no_beacon

# bound check, nothing fancy
def in_bounds(x, y, lower, upper):
    return lower <= x <= upper and lower <= y <= upper

# perfect opportunity to implement a function using yield.
# iterates through each direction of manhattan distance "radius"
def boundary(x, y, dist):
    xp, yp = (x, y + dist)

    while (xp, yp) != (x + dist, y):
        xp, yp = (xp + 1, yp - 1)
        yield (xp, yp)
    
    while (xp, yp) != (x, y - dist):
        xp, yp = (xp - 1, yp - 1)
        yield (xp, yp)

    while (xp, yp) != (x - dist, y):
        xp, yp = (xp - 1, yp + 1)
        yield (xp, yp)

    while (xp, yp) != (x, y + dist):
        xp, yp = (xp + 1, yp + 1)
        yield (xp, yp)

# what an absolute nightmare this was
# assumes there will be only one point that is valid... walks around
# the "radius" of each sensor and collects points just outside
# compares distance of those points to manhattan distance of each sensor
# and its closest beacon to ensure its not within another sensors radius
# as soon and we find one that is not, we stop looking and return the
# coordinate and frequency
def part_2(coord_list, bound):
    for x1, y1, _, _, dist in coord_list:
        for xp, yp in boundary(x1, y1, dist + 1):
            if in_bounds(xp, yp, 0, bound):
                for x2, y2, _, _, dist2 in coord_list:
                    if manhattan(x2, y2, xp, yp) <= dist2:
                        break
                else:
                    return (xp, yp)

infile = open('input.txt', 'r')
coord_list = parse(infile)

start_time = time.time()
print("Part 1 solution:", len(part_1(coord_list, 2000000)))
print("Part 1 runtime:", format(time.time() - start_time, '.2f'), "seconds")

start_time = time.time()
xp, yp = part_2(coord_list, 4000000)
freq = xp * 4000000 + yp
print("Part 2 solution: Freq. of {} at ({}, {})".format(freq, xp, yp))
print("Part 2 runtime:", format(time.time() - start_time, '.2f'), "seconds")

infile.close()