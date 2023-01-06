from copy import copy
from time import time

###############################################################################
# Classes
###############################################################################

class Rock:
    """
    Contains properties of falling rocks.
    Rock shape is implemented in reverse to match the room being reversed

        shape       type of rock
        height      height of rock
        width       width of rock
        falling     whether the rock has stopped moving

    """
    def rock_type(code):
        rock_shapes = { \
            'h' : [[1, 1, 1, 1]],\
            
            't' : [[0, 1, 0],\
                   [1, 1, 1],\
                   [0, 1, 0]],\
            
            'l' : [[0, 0, 1],\
                   [0, 0, 1],\
                   [1, 1, 1]],\

            'v' : [[1],\
                   [1],\
                   [1],\
                   [1]],\

            'b' : [[1, 1],\
                   [1, 1]]
            }

        return rock_shapes[code]

    def __init__(self, code):
        self.shape = Rock.rock_type(code)
        self.shape.reverse()
        self.height = len(self.shape)
        self.width = len(self.shape[0])
        self.falling = True

    def __repr__(self):
        string = ''
        sep = ''
        for x in self.shape:
            string += sep + str(x)
            sep = '\n'
        return string

    def __getitem__(self, index):
        return self.shape[index]

    def __iter__(self):
        return iter(self.shape)

class Room:
    """
    Contains properties of room.
    Implemented in reverse so lower row index is closer to floor

        room        2D array of room (0 denotes rock, 1 denotes air)
        height      height of rock pile
        current     current falling rock
        top         starting point for falling rock
        
    """
    ROW = [1, 0, 0, 0, 0, 0, 0, 0, 1]

    def __init__(self, ceil=10):
        self.room = [[1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.height = 0
        self.add_height(ceil)
        self.current = None

    def __repr__(self):
        rev_room = self.room.copy()
        rev_room.reverse()
        string = ''
        sep = ''
        for x in rev_room:
            string += sep + str(x)
            sep = '\n'
        return string

    def __getitem__(self, index):
        return self.room[index]

    @property
    def top(self):
        return self.height + 4

    def add_height(self, num=10):
        """
        Increases size of 2D room array
        """
        rows = [Room.ROW.copy() for _ in range(num)]
        self.room.extend(rows)

    def new_rock(self, rock):
        """
        Starts a new falling rock from starting position of room
        """
        if len(self.room) < self.top + rock.height:
            self.add_height()

        self.current = [rock, (self.top, 3)]

    def valid_move(self, new_coords):
        """
        Checks potential coordinates against rock shape to see if move is valid

        new_coords      potential new coordinates

        """
        valid = True
        rock = self.current[0]
        r, c = new_coords

        for i in range(0, rock.height):
            for j in range(0, rock.width):
                if self.room[r + i][j + c] and rock[i][j]:
                    valid = False
                    break
            if not(valid):
                break

        return valid

    def left(self):
        """
        Calls valid_move on position to the left
        
        """
        r, c = self.current[1]

        if self.valid_move((r, c - 1)):
            self.current[1] = (r, c - 1)

    def right(self):
        """
        Calls valid_move on position to the right
        
        """
        r, c = self.current[1]

        if self.valid_move((r, c + 1)):
            self.current[1] = (r, c + 1)

    def down(self):
        """
        Calls valid_move on position below. Sets falling to false if invalid
        
        """
        r, c = self.current[1]

        if self.valid_move((r - 1, c)):
            self.current[1] = (r - 1, c)
        else:
            self.current[0].falling = False

    def commit(self):
        """
        When rock has stopped moving, it is added to the 2D room array as 1's
        for rock.

        """
        rock = self.current[0]
        r, c = self.current[1]

        for i in range(0, rock.height):
            for j in range(0, rock.width):
                self.room[r + i][c + j] |= rock[i][j]

        self.height = max(self.height, r + rock.height - 1)

###############################################################################
# Functions
###############################################################################

def test(func, result):
    """
    Runs part_1 and part_2 against sample input/output
    
    """
    pattern = parse_jets("sample_input.txt")
    num = 2022 if func.__name__ == 'part_1' else 1000000000000

    ans = func(pattern, num)

    if ans == result:
        message = "Passed {}".format(func.__name__)
    else:
        message = "Failed {}, with {}".format(func.__name__, ans)

    print(message)

def parse_jets(filename):
    """
    Parses jet input

    """
    infile = open(filename, "r")
    pattern = [x for x in infile.read() if x != '\n']
    infile.close()
    return pattern

def part_1(jets, max_rocks):
    """
    Naive approach, carries out simulation step-by-step
    """
    room = Room()

    rocks = [Rock('h'), Rock('t'), Rock('l'), Rock('v'), Rock('b')]
    move = {'<' : room.left, '>' : room.right}

    rock_count = 0
    rock_index = 0
    jet_index = 0

    while rock_count < max_rocks:
        rock_index = rock_index % len(rocks)
        rock = copy(rocks[rock_index])
        room.new_rock(rock)

        jet_index = jet_index % len(jets)

        while rock.falling:
            jet_index = jet_index % len(jets)
            move[jets[jet_index]]()
            room.down()

            jet_index += 1

        room.commit()

        rock_index += 1
        rock_count += 1

    return room.height


def part_2(jets, max_rocks):
    """
    Same as part_1, but takes advantage of cycle of rocks/jets to allow
    for skipping thousands of iterations.

    visited dict counts the number of times a (rock_index, jet_index) combo
    has been seen. After two times, a cycle is locked in, and the height
    increase since the last time it was seen can be multiplied by the number
    of times that cycle will repeat in the max_rock count.

    visited is then reinitialized to an empty dict so that the last partial
    cycle can be completed. The sum of the height and the multiplied cycle
    are returned.

    """
    room = Room()

    rocks = [Rock('h'), Rock('t'), Rock('l'), Rock('v'), Rock('b')]
    move = {'<' : room.left, '>' : room.right}

    visited = dict()

    rock_count = 0
    rock_index = 0
    jet_index = 0
    height = 0

    while rock_count < max_rocks:
        temp_height = 0

        rock_index = rock_index % len(rocks)
        rock = copy(rocks[rock_index])
        room.new_rock(rock)

        jet_index = jet_index % len(jets)

        last_index, last_height, times_seen = \
            visited.setdefault((rock_index, jet_index), \
                (rock_count, room.height, 0))
        
        if times_seen == 2:
            visited = dict()
            height_diff = room.height - last_height
            repeat = (max_rocks - last_index) // (rock_count - last_index)
            remainder = (max_rocks - last_index) % (rock_count - last_index)

            temp_height = height_diff * (repeat - 1)
            rock_count = max_rocks - remainder
            height += temp_height

        else:
            visited[(rock_index, jet_index)] = \
                (rock_count, room.height, times_seen + 1)

            while rock.falling:
                jet_index = jet_index % len(jets)
                move[jets[jet_index]]()
                room.down()

                jet_index += 1

            room.commit()

            rock_index += 1
            rock_count += 1

    return room.height + height

###############################################################################
# Implementation
###############################################################################

def main():
    test(part_1, 3068)
    test(part_2, 1514285714288)

    jets = parse_jets("input.txt")

    start = time()
    print(part_1(jets, 2022))
    print("Part 1 completed in {:.2f} seconds".format(time() - start))

    start = time()
    print(part_2(jets, 1000000000000))
    print("Part 2 completed in {:.2f} seconds".format(time() - start))

if __name__ == '__main__': main()