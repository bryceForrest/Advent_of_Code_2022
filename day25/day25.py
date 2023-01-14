from time import time

def test(func, soln):
    infile = open("sample_input.txt", "r")
    input = parse(infile)
    infile.close()
    result = func(input)
    msg = "Passed {}".format(func.__name__) if result == soln else \
          "Failed {} with {}".format(func.__name__, result)
    print(msg)

def parse(infile):
    nums = list()
    while line := infile.readline().strip():
        nums.append(line)

    return nums

def from_snafu(num):
    sum = 0
    minus = {'-' : -1, '=' : -2}

    for i, digit in enumerate(reversed(num)):
        if digit.isdigit():
            sum += int(digit) * (5**i)
        else:
            sum += minus[digit] * (5**i)
    
    return sum

def to_snafu(num):
    rem = num
    snafu = str()
    digs = ['0', '1', '2', '=', '-']

    while rem != 0:
        x = rem % 5

        if x == (4):
            rem = (rem + 1) // 5
        elif x == (3):
            rem = (rem + 2) // 5
        else:
            rem //= 5
        
        snafu += digs[x]

    return snafu[::-1]


def part_1(input):
    sum = 0

    for num in input:
        x = from_snafu(num)
        sum += x

    return to_snafu(sum)

def part_2(input):
    pass

def main():
    test(part_1, '2=-1=0')
    # test(part_2, 0)

    infile = open("input.txt", "r")
    input = parse(infile)
    infile.close()

    start = time()
    print("Results for part 1:", part_1(input))
    print("Time taken: {:.2f}".format(time() - start))

    # start = time()
    # print("Results for part 2:", part_2(input))
    # print("Time taken: {:.2f}".format(time() - start))

if __name__ == "__main__": main()