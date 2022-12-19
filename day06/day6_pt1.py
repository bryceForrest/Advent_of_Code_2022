def is_unique(string):
  unique = True
  
  for i in range(0, len(string)):
    if string.find(string[i], i + 1) != -1:
      unique = False
      #break
  return unique


in_file = open("input.txt", "r")
buffer = in_file.read()

for i in range(0, len(buffer)):
  # part 1 start-of-marker is 4 unique characters (i + 4)
  marker = buffer[slice(i, i + 4)]
  if is_unique(marker):
    break
    
print(i + 4)