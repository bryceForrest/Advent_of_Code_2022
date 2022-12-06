in_file = open("input.txt", "r")

rucksack_1 = in_file.readline()
rucksack_2 = in_file.readline()
rucksack_3 = in_file.readline()

total_priority = 0

while rucksack_3:
  item = ""

  for i in rucksack_1:
    index_1 = rucksack_2.find(i)
    index_2 = rucksack_3.find(i)

    if index_1 != -1 and index_2 != -1:
      item = rucksack_2[index_1]
      break

  if item.isupper():
    total_priority += ord(item) - 38
  else:
    total_priority += ord(item) - 96

  rucksack_1 = in_file.readline()
  rucksack_2 = in_file.readline()
  rucksack_3 = in_file.readline()

print(total_priority)
