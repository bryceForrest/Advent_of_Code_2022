from time import time
import sympy

def test(func, soln):
    """
    Tests functions against sample input/output

    """
    infile = open("sample_input.txt", "r")
    monkeys = parse(infile)
    infile.close
    result = func(monkeys)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    """
    Parses input into dictionary of monkeys and their expressions
    """
    line = infile.readline()
    monkeys = dict()

    while line:
        name, expr = line.strip().split(': ')
        monkeys.update({name : expr})
        line = infile.readline()

    return monkeys


def path_compress(curr, monkeys):
    """
    Recursively performs "path compression" on expressions until it reaches
    a numeric value.

    Added "if curr == 'x'" for part 2, so that we can solve for x symbolically
    
    """
    operations = '+-*/'
    try:
        return str(int(curr))
    except:
        if curr == 'x':
            return curr
        else:
            expr = str()
            for n in curr.split():
                if n in operations:
                    expr += n
                else:
                    expr += '({})'.format(path_compress(monkeys[n], monkeys))

            return expr

def part_1(monkeys):
    """
    Simply compresses expressions using path compression, and evaluates
    resulting expression
    
    """
    num = eval(path_compress(monkeys['root'], monkeys))
            
    return int(num)

def part_2(monkeys):
    """
    Very similar to part 1, but assumes resulting expression will contain
    an 'x' to solve for. Sets humn to x, sets root to '-', since numpy.solve
    finds roots (thus in order for the two parts to be equal, they must equal
    zero when one is subtracted from the other)

    Not sure how one would pull this off without symbolic library...!
    
    """
    monkeys['root'] = monkeys['root'].replace('+', '-')
    monkeys['humn'] = 'x'

    num, = sympy.solve(path_compress(monkeys['root'], monkeys), 'x')
    
    return num

def main():
    test(part_1, 152)
    test(part_2, 301)

    infile = open("input.txt", "r")
    monkeys = parse(infile)
    infile.close()

    start = time()
    print("Result for part 1:", part_1(monkeys.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

    start = time()
    print("Result for part 2:", part_2(monkeys.copy()))
    print("Time taken: {:.2f} seconds".format(time() - start))

if __name__ == "__main__": main()