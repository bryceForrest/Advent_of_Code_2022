###############################################################################
# Class defintions:
###############################################################################

class Directory:
    def __init__(self, name = '', parent = None):
        self.name = name
        self.parent = parent
        self.dirs = {}
        self.files = []

    def __str__(self):
        identity = ''
        delim = ''
        for i in self.files:
            identity += delim + i.name
            delim = ' '

        key_list = self.dirs.keys()
        for i in key_list:
            identity += delim + i
            delim = ' '
        return (identity)

    def size(self):
        sum = 0
        for i in self.dirs.values():
            sum += i.size()

        for i in self.files:
            sum += i.size
        return sum

    def head(self):
        current = self
        while current.parent != None:
            current = current.parent

        return current

    def addFile(self, item):
        self.files.append(item)

    def addDir(self, dir):
        self.dirs[dir.name] = dir


class File:
    def __init__(self, name = '', size = 0):
        self.name = name
        self.size = size

    def __str__(self):
        return (self.name + ' ' + str(self.size))

###############################################################################
# Function definitions
###############################################################################

def traverse(directory, dir_list, limit):
    if directory.size() >= limit:
        dir_list.append(directory)
    for i in directory.dirs.values():
        traverse(i, dir_list, limit)

###############################################################################
# Implementation:
###############################################################################

TOTAL_DISK = 70000000
REQ_SPACE = 30000000

infile = open("input.txt", "r")
line = infile.readline()
current = Directory('/')

# parsing input, building directory
while line:
    command = line.split()
    
    if command[0] == "$":               # $ means user input
        if command[1] == "cd":          # cd means we're moving
            if command[2] == "/":       # / means we just started
                pass
            elif command[2] == "..":    # .. means backwards
                current = current.parent
            else:                       # any other cd is forwards
                current = current.dirs[command[2]]
    elif command[0] == "dir":
        newDir = Directory(command[1], current)
        current.addDir(newDir)
    else:
        newFile = File(command[1], int(command[0]))
        current.addFile(newFile)

    line = infile.readline()

space_needed = REQ_SPACE - (TOTAL_DISK - current.head().size())

dir_list = []
traverse(current.head(), dir_list, space_needed)

min = TOTAL_DISK                        # obviously won't be larger than this
for i in dir_list:
    sz = i.size()
    if sz < min:
        min = sz

print(min)