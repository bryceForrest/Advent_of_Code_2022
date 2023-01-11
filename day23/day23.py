from time import time

def test(func, soln):
    """
    Test against sample input/output
    
    """
    infile = open("sample_input.txt", "r")
    elves = parse(infile)
    infile.close()

    result = func(elves)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    """
    Parses input into the coordinate of all elves

    """
    elves = []
    r, c = 0, 0

    while ch := infile.read(1):
        if ch == '\n':
            r += 1
            c = 0
            continue
        elif ch == '#':
            elves.append([r, c])
        
        c += 1

    return elves

def valid_move(curr, elves, check_dirs):
    """
    Does most of the heavy lifting: checks the surrounding spaces
    according to the rules and returns the proposed new position.
    
    """
    # define cardinal direction moves for readability
    dirs = {'N' : (-1, 0), 'NE' : (-1, 1), 'NW' : (-1, -1),
            'S' : (1, 0), 'SE' : (1, 1), 'SW' : (1, -1),
            'W' : (0, -1), 'E' : (0, 1)}

    # adds tuples element-wise (coordinate + directional move)
    add = lambda a, b : [x + y for x, y in zip(a, b)]

    proposed = curr
    found_move = False

    # check the eight surrounding spots
    found = False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j == 0:
                continue

            if add(curr, (i, j)) in elves:
                found = True
        
        if found:
            break
    else:
        return curr

    # if the eight surrounding spots are not open, explore
    # other options
    for check in check_dirs:
        if found_move:
            break

        for c in check:
            temp_coord = add(curr, dirs[c])
            if temp_coord in elves:
                break
        else:
            proposed = add(curr, dirs[check[0]])
            found_move = True

    return proposed
            


def part_1(elves):
    """
    Runs 10 rounds of iterating through elves and making a list of
    proposed moves. Any proposed moves for which only one elf proposed,
    becomes that elves new position.
    At the end, calculate the area covered by the elves
    
    """
    check = [('N', 'NE', 'NW'), ('S', 'SE', 'SW'), 
             ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]

    # simulate 10 rounds
    for _ in range(10):
        proposed_moves = []
        for elf in elves:
            proposed = valid_move(elf, elves, check)
            proposed_moves.append(proposed)

        for i in range(len(elves)):
            if proposed_moves.count(proposed_moves[i]) == 1:
                elves[i] = proposed_moves[i]

        check = check[1:] + check[:1]

    # find the perimeter formed by the elves
    top = min(elves, key=lambda x : x[0])[0]
    bottom = max(elves, key=lambda x : x[0])[0]
    left = min(elves, key=lambda x : x[1])[1]
    right = max(elves, key=lambda x : x[1])[1]

    # generate the total area, and subtract the spaces covered by elves
    area = (bottom - top + 1) * (right - left + 1)

    return area - len(elves)


def part_2(elves):
    """
    Essentially identical to part 1, but we're only interested in how many
    rounds passed until not elves move

    """
    check = [('N', 'NE', 'NW'), ('S', 'SE', 'SW'), 
             ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]

    # keep track of rounds
    counter = 0

    while True:
        counter += 1
        prev_elves = elves.copy()
        proposed_moves = []
        for elf in elves:
            proposed = valid_move(elf, elves, check)
            proposed_moves.append(proposed)

        for i in range(len(elves)):
            if proposed_moves.count(proposed_moves[i]) == 1:
                elves[i] = proposed_moves[i]

        # see if any elves moved... if not, we're done
        if prev_elves == elves:
            break

        check = check[1:] + check[:1]

    return counter

def main():
    test(part_1, 110)
    test(part_2, 20)

    infile = open("input.txt", "r")
    elves = parse(infile)
    infile.close()

    start = time()
    print("Results for part 1:", part_1(elves.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

    start = time()
    print("Results for part 2:", part_2(elves.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

if __name__ == "__main__": main()