#######################################
# Functions
#######################################
def is_unique(string):
  unique = True
  
  for i in range(0, len(string)):
    if string.find(string[i], i + 1) != -1:
      unique = False
      break
  return unique

def find_start(string, index, length):
  for i in range(index, len(string)):
    marker = string[slice(i, i + length)]
    if is_unique(marker):
      break
   
  return i + length

#######################################
# Implementation
#######################################
in_file = open("input.txt", "r")
buffer = in_file.read()

packet = find_start(buffer, 0, 4)
message = find_start(buffer, packet, 14)

print(message)