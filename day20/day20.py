from time import time

###############################################################################
# Functions
###############################################################################

def test(func, soln):
    """
    Tests functions against sample input/output
    
    """
    infile = open("sample_input.txt", "r")
    nums = parse(infile)
    infile.close
    result = func(nums)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    """
    Parses input into list of numbers
    
    """
    nums = list()
    line = infile.readline()

    while line:
        nums.append(int(line))
        line = infile.readline()

    return nums

def part_1(nums):
    """
    Builds list of numbers along with original index (accounts for duplicates)
    Places number in appropriate position, and returns sum of 1000th, 2000th,
    and 3000th index

    """
    orig = [(x, y) for x, y in enumerate(nums)]
    lst = orig.copy()

    for i, n in orig:
        new_i = lst.index((i, n))
        lst.pop(new_i)
        lst.insert((new_i + n) % len(lst), (i, n))

    new_lst = [x for _, x in lst]
    z_index = new_lst.index(0)

    sum = 0

    for xth in range (1000, 3001, 1000):
        sum += new_lst[(z_index + xth) % len(new_lst)]
    
    return sum

def part_2(nums):
    """
    Basically the same as part 1, but applies decryption key, and "mixes"
    list 10 times

    """
    KEY = 811589153
    orig = [(x, y * KEY) for x, y in enumerate(nums)]
    lst = orig.copy()

    for _ in range(10):
        for i, n in orig:
            new_i = lst.index((i, n))
            lst.pop(new_i)
            lst.insert((new_i + n) % len(lst), (i, n))

    new_lst = [x for _, x in lst]
    z_index = new_lst.index(0)

    sum = 0

    for xth in range (1000, 3001, 1000):
        sum += new_lst[(z_index + xth) % len(new_lst)]
    
    return sum

###############################################################################
# Implementation
###############################################################################

def main():
    test(part_1, 3)
    test(part_2, 1623178306)

    infile = open("input.txt", "r")
    nums = parse(infile)
    infile.close()

    start = time()
    print("The solution for part 1 is:", part_1(nums))
    print("Time taken: {:.2f}".format(time() - start))

    start = time()
    print("The solution for part 2 is:", part_2(nums))
    print("Time taken: {:.2f}".format(time() - start))

if __name__ == '__main__': main()