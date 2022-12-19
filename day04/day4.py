in_file = open("input.txt", "r")

elf_pair = in_file.readline()

count = 0

while elf_pair:
  groups = elf_pair.split(",")

  start_1, end_1 = groups[0].split("-")
  start_2, end_2 = groups[1].split("-")

  if int(start_1) >= int(start_2) and \
     int(start_1) <= int(end_2):
    count += 1
  elif int(start_2) >= int(start_1) and \
       int(start_2) <= int(end_1):
    count += 1

  elf_pair = in_file.readline()

print(count)
