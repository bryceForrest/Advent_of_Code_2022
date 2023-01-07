from time import time

def test(func, soln):
    """
    Tests against sample input/output
    
    """
    infile = open("sample_input.txt", "r")
    cubes = parse(infile)
    result = func(cubes)
    output = "Passed {}".format(func.__name__) if result == soln else \
             "Failed {} with {}".format(func.__name__, result)
    infile.close()

    print(output)

def parse(infile):
    """
    Parses input into list of coordinates

    """
    line = infile.readline().strip()
    cubes = list()

    while line:
        cubes.append(tuple([int(x) for x in line.split(',')]))
        line = infile.readline().strip()

    return cubes

def neighbors(cube):
    """
    Returns list of neighbors (above, below, left, right, front, back)
    
    """
    check = [[1, 0, 0], [-1, 0, 0],
             [0, 1, 0], [0, -1, 0],
             [0, 0, 1], [0, 0, -1]]

    return [add(cube, c) for c in check]

def add(a, b):
    """
    Adds lists/sets/tuples element-wise
    
    """
    return tuple([x + y for x, y in zip(a, b)])


def inside(coord, bounds):
    """
    Used by flood-fill to determine if a coordinate is in-bounds
    (think paint bucket tool)
    
    """
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    x, y, z = coord

    if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
        return True
    else:
        return False

def find_bounds(cubes):
    """
    Returns max and min boundary of cubes
    
    """
    min_x = min(cubes, key=lambda x : x[0])[0] - 1
    min_y = min(cubes, key=lambda x : x[1])[1] - 1
    min_z = min(cubes, key=lambda x : x[2])[2] - 1
    max_x = max(cubes, key=lambda x : x[0])[0] + 1
    max_y = max(cubes, key=lambda x : x[1])[1] + 1
    max_z = max(cubes, key=lambda x : x[2])[2] + 1

    return (min_x, min_y, min_z, max_x, max_y, max_z)

def find_air(cubes):
    """
    Flood-fill to establish outer-boundary of air for part 2 (thanks Wikipedia)
    
    """
    q = list()
    air = set()

    start = (min(cubes, key=lambda x : x[0])[0],
             min(cubes, key=lambda x : x[1])[1],
             min(cubes, key=lambda x : x[2])[2])

    q.append(start)
    bounds = find_bounds(cubes)

    while q:
        curr = q.pop(0)
        if inside(curr, bounds) and curr not in cubes and curr not in air:
            air.add(curr)
            q.extend(neighbors(curr))

    return air

    

def part_1(cubes):
    """
    For each cube in cubes, if the neighbor is in the list of cubes, that
    side is not exposed. If it is not, add it to the cound of sides

    """
    sides = 0
    for cube in cubes:
        nbors = neighbors(cube)
        for nbor in nbors:
            if nbor not in cubes:
                sides += 1

    return sides

def part_2(cubes):
    """
    Basically the same as part 1, but establishes an outer layer of "air"
    For each cube in cubes, if the neighbor is not in the list of cubes of air,
    that side is not exposed. If it is, add it to the cound of sides

    """

    sides = 0

    air = find_air(cubes)

    for cube in cubes:
        nbors = neighbors(cube)
        for nbor in nbors:
            if nbor in air:
                sides += 1

    return sides

def main():
    test(part_1, 64)
    test(part_2, 58)

    infile = open("input.txt", "r")
    cubes = parse(infile)
    infile.close()

    start = time()
    print("Results for part 1:", part_1(cubes))
    print("Part 1 completed in {:.2f} seconds".format(time() - start))

    start = time()
    print("Results for part 2:", part_2(cubes))
    print("Part 2 completed in {:.2f} seconds".format(time() - start))
    
if __name__ == '__main__': main()