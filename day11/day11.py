###############################################################################
# Classes
###############################################################################

# self contains all relevant details about a monkey: what they are holding,
# who they might pass it to, what operation they increase the worry level by,
# and how many inspections they've done
class Monkey():
    def __init__(self):
        self.items = list()
        self.throw = dict()
        self.test_val = 1                   # dummy placeholder
        self.operation = lambda a : a       # dummy placeholder
        self.inspections = 0

    def __str__(self):
        return str(self.items)

    def test(self, x):
        return True if x % self.test_val == 0 else False

###############################################################################
# Functions
###############################################################################

# builds the current monkey
def parse(infile):
    monkey = Monkey()
    infile.readline() # Monkey X:
    
    monkey.items = [int(i) for i in \
        infile.readline().replace(',', '').split() if i.isdigit()]
    
    # coolest one: reads in a string, turns it into the operation expression
    # example: "new = old * 10" => lambda old : old * 10
    op = infile.readline()
    monkey.operation = lambda old : eval(op.split('=')[1])
    
    monkey.test_val = int(infile.readline().split()[-1])

    monkey.throw[True] = int(infile.readline().split()[-1])
    monkey.throw[False] = int(infile.readline().split()[-1])
    infile.readline() # blank line

    return monkey

# iterates through the list of monkeys, inspects and passes each item
def play(monkeys, part2):
    divisors = [m.test_val for m in monkeys]
    prod = 1
    for d in divisors:
        prod *= d
    for m in monkeys:
        while m.items:
            m.inspections += 1
            current = m.items.pop(0)
            current = m.operation(current)
            if not(part2):
                current = current // 3
            else:
                current = current % prod
            pass_to = m.throw[m.test(current)]
            

            monkeys[pass_to].items.append(current)

def part(rounds, part2):
    for i in range(rounds):
        play(monkeys, part2)

    monkey_business = [x.inspections for x in monkeys]
    monkey_business.sort()
    print(monkey_business[-1] * monkey_business[-2])


###############################################################################
# Implementation
###############################################################################
infile = open("input.txt", "r")
monkeys = []

place = infile.tell()       # keeps track of place to restore (peek())

while infile.readline():
    infile.seek(place)
    monkeys.append(parse(infile))
    place = infile.tell()

#part(20, part2 = False)
part(10000, part2 = True)
infile.close()