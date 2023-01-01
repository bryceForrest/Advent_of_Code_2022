import re
import time
import copy
import itertools

###############################################################################
# Classes
###############################################################################

class Volcano:
    """
    Organize system of tunnels
    """
    def __init__(self):
        self.network = dict()

    def __copy__(self):
        copy_class = Volcano()
        copy_class.network = self.network.copy()
        return copy_class

    def __getitem__(self, key):
        return self.network[key]

    def __setitem__(self, key, value):
        self.network[key] = value

    def __repr__(self):
        return str(self.network)

    def __iter__(self):
        for n in self.network.keys():
            yield n
    
    def __len__(self):
        return len(self.network)

class Tunnel:
    """
    Organize data for a given tunnel/valve
    """
    def __init__(self, paths, flow):
        self.name = paths[0]
        self.paths = paths[1:]
        self.dist = dict()
        self.flow = flow

    def __repr__(self):
        output = "Valve: {}, Flow: {}, Network: {}"
        return output.format(self.name, self.flow, self.paths)

    def __bool__(self):
        return self.valve

###############################################################################
# Functions
###############################################################################
def test(func, result):
    """
    Runs function against sample input and compares result to expected output.
    
        func        function being tested
        
        result      expected output
    """
    sample_input = open('sample_input.txt', 'r')
    test_result = func(parse(sample_input))
    if (test_result == result):
        message = "Passed"
        detail = ""
    else:
        message = "Failed"
        detail = ", with {}".format(test_result)
    sample_input.close()

    print("{} {} for sample input{}.".format(message, func.__name__, detail))    

def parse(infile):
    """
    Parse input file into tunnels.

        infile      file to be parsed
        
        return      volcano of tunnels
    """
    line = infile.readline()
    volcano = Volcano()
    while line:
        valve = re.findall('[A-Z][A-Z]', line)
        flow = int(re.search('\d+', line).group(0))
        volcano[valve[0]] = (Tunnel(valve, flow))
        line = infile.readline()

    return volcano

def dijkstra(graph, source):
    """
    Dijkstras algorithm to find shortest path between starting node and
    all nodes in node_list. Assumes every path has a weight of 1
    
        graph       graph of nodes
        source      starting node
        node_list   nodes to be reached

        return      dictionary of distance
    """
    dist = {x : float('inf') for x in graph}
    visited = {x : False for x in graph}

    queue = [(source, 0)]

    while queue:
        u = min(queue, key=lambda x : x[1])
        queue.remove(u)
        visited[u[0]] = True
        dist[u[0]] = u[1]

        for v in graph[u[0]].paths:
            if visited[v] == False:
                dist[v] = min(dist[v], dist[u[0]] + 1)
                queue.append((v, dist[v]))

    return dist

def dfs(graph, vertex, minutes, visited):
    """
    Depth First Search to find best path. Recursively called on neighbors,
    with preference for path with maximum flow.

        graph       graph of nodes
        vertex      current node
        minutes     remaining time
        visited     nodes already visited

        return      flow from path
    """
    visited.append(vertex)
    pressure = 0

    paths = [x for x in graph[vertex].dist \
             if x not in visited \
             and graph[x].flow \
             and (minutes - graph[vertex].dist[x] - 1) > 0]

    if paths:
        pressure = max([dfs(graph, p, \
                            minutes - graph[vertex].dist[p] - 1, \
                            visited.copy()) \
                            for p in paths
                        ])
    
    return pressure + graph[vertex].flow * minutes

def part_1(volcano):
    """
    Part 1 solution. Refactors graph as having path to every node via the
    shortest sum of paths through connecting nodes, using Dijkstra on every
    node in graph. Then uses dfs to find the path with maximum flow

        volcano     graph of nodes

        return      max flow from best path
    """
    for s in volcano:
        volcano[s].dist = (dijkstra(volcano, s))

    max_pressure = dfs(volcano, 'AA', 30, [])

    return max_pressure

def part_2(volcano):
    """
    Part 2 solution. Very similar to part 1, but generates every subset
    combination of nodes, and divides them between me and the elephant.
    Each subset is then loaded into the visited list of seperate dfs
    calls. This ensures that I will not visit any valves that the
    elephant visits. The maximum sum of the two calls is returned.

        volcano     graph of nodes

        return      max flow from best path
    """
    neighbors = [x for x in volcano if volcano[x].flow]
    max_flow = 0

    for s in volcano:
        volcano[s].dist = (dijkstra(volcano, s))

    # assume that splitting up the nodes 50/50 will yield the max flow
    subsets = itertools.combinations(neighbors, len(neighbors) // 2)

    for s in subsets:
        m = set(s)                  # my nodes to visit
        e = set(neighbors) - m      # elephant's nodes

        max_flow = max(max_flow, \
                        dfs(volcano, 'AA', 26, list(e)) + \
                        dfs(volcano, 'AA', 26, list(m)) \
                        )
        
    return max_flow
###############################################################################
# Implementation
###############################################################################

input_file = open("input.txt", "r")
volcano = parse(input_file)

test(part_1, 1651)
test(part_2, 1707)

print('*' * 40)

start = time.time()
print("Part 1 results: {}".format(part_1(copy.copy(volcano))))
print("Runtime: {:.2f} seconds".format(time.time() - start))

print('*' * 40)

start = time.time()
print("Part 2 results: {}".format(part_2(copy.copy(volcano))))
print("Runtime: {:.2f} seconds".format(time.time() - start))

input_file.close()
