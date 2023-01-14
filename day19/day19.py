from time import time
from math import ceil
import re
import heapq

class Blueprint:
    """
    Arranges the list parsed from the input into relevant data for a given
    blueprint: the "ingredients" for each bot, a list of bots so each can
    be accessed using an index, and a list of the maximum amount of each
    ingredient needed, so we don't build more robots than is useful
    
    """
    def __init__(self, lst):
        self.id_num = lst[0]
        self.ore_bot = [lst[1], 0, 0, 0]
        self.clay_bot = [lst[2], 0, 0, 0]
        self.obs_bot = [lst[3], lst[4], 0, 0]
        self.geode_bot = [lst[5], 0, lst[6], 0]

        self.bot_lst = [self.ore_bot, self.clay_bot,
                        self.obs_bot, self.geode_bot]

        self.max_lst = [max([x[i] for x in self.bot_lst]) for i in range(4)]
        self.max_lst[3] = float('inf')

    def __repr__(self):
        return str(vars(self))

class State:
    """
    Arranges the data for a given "state" into an object, so they can be
    processed in a min heap priority queue

    """
    def __init__(self, minerals, bots, minutes):
        self.minerals = minerals
        self.bots = bots
        self.minutes = minutes
        self.tup = tuple((self.minerals, self.bots, self.minutes))
    
    def __lt__(self, obj):
        """
        In this case, more geode bots means higher priority

        """
        return self.bots[3] > obj.bots[3]

    def __repr__(self):
        return str(self.tup)

def test(func, soln):
    """
    Tests against sample input/output
    
    """
    infile = open("sample_input.txt", "r")
    blueprints = parse(infile)
    infile.close()
    result = func(blueprints)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    """
    Parses input into blueprint lists, as follows:
    [
        id, 
        ore robot cost in ore, 
        clay robot cost in ore,
        obsidian robot cost in ore,
        obsidian robot cost in clay,
        geode robot cost in ore,
        geode robot cost in obsidian
    ]

    """
    blueprints = list()
    while line := infile.readline():
        curr = Blueprint(list(map(int, re.findall('\d+', line))))
        blueprints.append(curr)

    return blueprints


def collect(bp, start_mins):
    """
    I was terrible at this

    Praise be to this guy:
    https://todd.ginsberg.com/post/advent-of-code/2022/day19/
    who explained his logic well enough for me to implement something
    similar. I probably would have been stuck on this forever, though
    now it seems so clear:

    Push "states" onto a queue. That is, a list of hypothetical situations
    and how they may turn out. "What if we build a clay robot? What if we
    don't?" etc etc

    It's not useful to have more robots producing a mineral than you 
    could possibly use in a turn... since you can only build one robot
    per turn, the limit is whatever the max amount of a mineral needed
    for any given robot is. That said, if we don't have the maximum, we
    can push a state onto the queue of if we built another.

    Once we start building geode robots we can clear out a lot of states
    quickly. The priority queue will prioritize states with more geode
    robots, and if the current state couldn't possible produce more geodes
    even if it produced a new geode robot every minute, we skip it.

    We return the max number of geodes from any state

    """
    add = lambda a, b : [x + y for x, y in zip(a, b)]
    sub = lambda a, b : [x - y for x, y in zip(a, b)]

    bot_keys = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    geode_count = 0

    states = [State([0, 0, 0, 0], [1, 0, 0, 0], start_mins)]
    heapq.heapify(states)

    while states:
        curr_state = heapq.heappop(states)
        minerals = curr_state.minerals
        bots = curr_state.bots
        minutes = curr_state.minutes

        # if we couldn't get it in the best case scenario, just move on
        if minerals[3] + bots[3] * minutes + sum(range(minutes)) < geode_count:
            continue

        geode_count = max(geode_count, minerals[3] + bots[3] * minutes)

        # consider some things to build next
        for i in range(4):
            if bots[i] < bp.max_lst[i]:
                build_time = build(bp, minerals, bots, i)
                if build_time is not None and minutes - build_time > 0:
                    temp_minerals = [build_time * x for x in bots]
                    temp_minerals = add(minerals, temp_minerals)
                    heapq.heappush(states, 
                                   State(sub(temp_minerals, bp.bot_lst[i]),
                                   add(bots, bot_keys[i]), 
                                   minutes - build_time))

    return geode_count

def build(bp, minerals, bots, idx):
    """
    Calculates the time needed to build a given robot, based on the ingredients
    needed to build it. Avoids division by zero by returning None if any of
    the necessary bots are zero. Else it returns the maximum of cost / bots
    rounded up.
    
    """
    sub = lambda a, b : [x - y for x, y in zip(a, b)]
    enough = list(x >= y for x, y in zip(minerals, bp.bot_lst[idx]))
    
    if all(enough):
        return 1

    cost = sub(bp.bot_lst[idx], minerals)
    wait_time = 0

    for c, b in zip(cost, bots):
        if c == 0:
            continue
        if b == 0:
            return None
        wait_time = max(wait_time, ceil(c / b))

    return wait_time + 1
    
def part_1(bp):
    """
    Simply calculates the maximum geodes, multiplies by the blueprint id,
    and returns the sum
    
    """
    sum = 0

    for b in enumerate(bp):
        sum += (collect(b, 24) * b.id_num)

    return sum

def part_2(bp):
    """
    Calculates the maximum geodes and returns the product.
    bp_count added out of neuroticism to enable test function to work
    (since the sample input only has two blueprints)
    
    """
    prod = 1
    bp_count = min(len(bp), 3)

    for i in range(bp_count):
        prod *= collect(bp[i], 32)

    return prod
    

def main():
    test(part_1, 33)
    test(part_2, 3472)

    infile = open("input.txt", "r")
    blueprints = parse(infile)
    infile.close()

    start = time()
    print("Results for part 1:", part_1(blueprints.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

    start = time()
    print("Results for part 2:", part_2(blueprints.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

if __name__ == "__main__": main()