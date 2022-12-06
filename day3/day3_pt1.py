import math

in_file = open("input.txt", "r")

rucksack = in_file.readline()

total_priority = 0


while rucksack:
  top_half = slice(0, math.floor(len(rucksack) / 2))
  bottom_half = slice(math.floor(len(rucksack) / 2), len(rucksack) - 1)

  compartment_1 = rucksack[top_half]
  compartment_2 = rucksack[bottom_half]

  item = ""
  
  for i in compartment_1:
    index = compartment_2.find(i)
    if index != -1:
      item = compartment_2[index]
      break

  priority = 0
    
  if item.isupper():
    total_priority += ord(item) - 38
  else:
    total_priority += ord(item) - 96
  
  rucksack = in_file.readline()

print(total_priority)