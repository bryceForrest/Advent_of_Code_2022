f_stream = open("input.txt", "r")

game = f_stream.readline()

lose =  {"A" : "Z", "B" : "X", "C" : "Y"}
win = {"A" : "Y", "B" : "Z", "C" : "X"}
draw = {"A" : "X", "B" : "Y", "C" : "Z"}
shape = {"A" : 1, "B" : 2, "C" : 3, "X" : 1, "Y": 2, "Z" : 3}

score = 0

while game:
  elf = game[0]

  outcome = game[2]

  if outcome == "X":
    me = lose[elf]
    score += shape[me]
  elif outcome == "Y":
    me = draw[elf]
    score += 3 + shape[me]
  else:
    me = win[elf]
    score += 6 + shape[me]

  ### part 1 ###
  # if win[elf] == me:
  #   score += 6 + shape[me]
  # elif lose[elf] == me:
  #   score += shape[me]
  # else:
  #   score += 3 + shape[me]

  game = f_stream.readline()

print(score)
