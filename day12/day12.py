import functools
from functools import total_ordering

import sys

###############################################################################
# Classes
###############################################################################

# abstracts a list into a priority queue
class Priorityq:
    def __init__(self):
        self.q = list()

    def __repr__(self):
        return str(self.q)

    def __bool__(self):
        return len(self.q) != 0

    def dequeue(self):
        return self.q.pop(0)

    def queue(self, item):
        self.q.append(item)
        self.q.sort()   # might not the most efficient, but...

# information contained by each vertex
class Vertex:
    def __init__(self, coordinates, height, dist = float('inf')):
        self.coordinates = coordinates
        self.dist = dist
        self.visited = False
        self.height = height

    def __lt__(self, obj):
        return self.dist < obj.dist

    def __repr__(self):
        return str([self.coordinates, self.height, self.dist])

# information contained about the vertices and edges of the graph
class Graph:
    def __init__(self):
        self.g = []
        self.start = tuple()
        self.end = tuple()
        self.lookup = {}

    def __repr__(self):
        s = str()
        delim = ''
        for i in self.g:
            s += delim + str(i)
            delim = '\n'
        return s

    def at(self, coordinates):
        return self.g[coordinates[0]][coordinates[1]]

    def shape(self):
        return len(self.g), len(self.g[0])

    def reset(self):
        for v in self.lookup.values():
            # account for out of bound coordinates that were set to false
            if v:
                v.visited = False
                v.dist = float('inf')

###############################################################################
# Functions
###############################################################################

# dijkstra's shortest path algorithm
def dijkstra(graph, start):
    current = start
    current.dist = 0
    pq = Priorityq()
    pq.queue(current)

    while pq:
        current = pq.dequeue()
        reachable(graph, current, pq)
        current.visited = True
        graph.g[current.coordinates[0]][current.coordinates[1]] = str(current.dist)

# updates the priority queue based on reachable vertices from the current vertex
def reachable(graph, vertex, priorityq):
    surroundings = ((1,0), (-1,0), (0, -1), (0, 1))
    for k in surroundings:
        temp = [x + y for x,y in zip(vertex.coordinates, k)]
        next = graph.lookup.setdefault(tuple(temp), False)
        
        if next and not(next.visited) and next.height <= (vertex.height + 1) \
            and (vertex.dist + 1) < next.dist:
                next.dist = vertex.dist + 1
                priorityq.queue(next)   

###############################################################################
# Implementation
###############################################################################

infile = open('input.txt', 'r')

graph = Graph()
line = []
[i, j] = [0, 0]         # starting values for coordinates

# for part 2
part2 = False
starts = list()     
ends = list()

# for command line arguments (part1 or part2)
if len(sys.argv) == 1:
    part2 = False
else:
    test = {'part1' : False, 'part2' : True}
    part2 = test.setdefault(sys.argv[1], False)

ch = infile.read(1)

# build graph
while ch:
    line.append(ch)
    v = Vertex((i, j), 0)

    # set height of vertex based on character
    if ch == 'S':
        graph.start = graph.lookup[tuple([i,j])] = v
    elif ch == 'E':
        graph.end = graph.lookup[tuple([i,j])] = v
        v.height = 25
    else:
        graph.lookup[tuple([i,j])] = v
        v.height = ord(ch) - ord('a')

    if v.height == 0:
        starts.append(v)

    j += 1
    ch = infile.read(1)

    # if we have reached the end of the line or eof:
    if ch == '\n' or ch == '':
        graph.g.append(line)
        ch = infile.read(1)
        line = []
        
        i += 1
        j = 0

# if part 2, run dijkstra on every starting value,
# else just on 'S'
if part2:
    for s in starts:
        dijkstra(graph, s)
        ends.append(graph.end.dist)
        graph.reset()

    print(min(ends))
else:
    dijkstra(graph, graph.start)
    print(graph.end.dist) 

infile.close