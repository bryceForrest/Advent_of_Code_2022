# Advent of Code 2022 Day 5, pt. 1 solution
in_file = open("input2.txt", "r")

line = in_file.readline()
data_in = []

# collect data for crates
while line[1] != '1':
  data_in.append(list(line[slice(1, len(line), 4)]))

  line = in_file.readline()

# build crates
crates = []
for c in range(0, len(data_in[0])):
  temp = []
  for r in range(0, len(data_in)):
    if data_in[r][c] != ' ':
      temp.insert(0, data_in[r][c])

  crates.append(temp)

in_file.readline() # clear out blank line
line = in_file.readline()

while line:
  inst = line.split()
  inst = inst[slice(1, len(inst), 2)]

  for i in range(0, int(inst[0])):
    crates[int(inst[2]) - 1].append(crates[int(inst[1]) - 1].pop())

  line = in_file.readline()

result = ""
for i in crates:
  result += i.pop()

print(result)