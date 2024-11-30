"""
Advent of Code 2021
Day 15: Chiton
"""

import sys
from collections import deque
import heapq


def get_risk_levels(puzzle_input, part_2):
    num_cols, num_rows = len(puzzle_input[0].strip()), len(puzzle_input)
    risk_levels = {}
    for i in range(num_rows):
        for j in range(num_cols):
            if part_2:
                for x in range(5):
                    for y in range(5):
                        risk_levels[i + num_cols * x, j + num_rows * y] = (int(puzzle_input[i][j]) + x + y - 1) % 9 + 1
            else:
                risk_levels[i, j] = int(puzzle_input[i][j])
    return risk_levels


class Graph:
    def __init__(self, risk_levels):
        self.nodes = risk_levels.keys()
        self.width = max(risk_levels, key=lambda x: x[0])[0]
        self.height = max(risk_levels, key=lambda x: x[1])[1]
        self.graph = self.generate_graph(risk_levels)
    
    def generate_graph(self, risk_levels):
        graph = {}
        for node in risk_levels.keys():
            d = {}
            for neighbor in self.get_neighbors(node):
                d[neighbor] = risk_levels[neighbor]
            graph[node] = d
        return graph

    def get_neighbors(self, node):
        i, j = node
        left, right, up, down = ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
        locs = set()
        if i != 0: locs.add(left)
        if i != self.width: locs.add(right)
        if j != 0: locs.add(up)
        if j != self.height: locs.add(down)
        return locs

    def get_nodes(self):
        return self.nodes

    def get_outgoing_edges(self, node):
        return self.graph[node].items()
    
    def end_node(self):
        return (self.height, self.width)

def dijkstra(graph, start_node):
    min_risk = {} # maps (i, j) to min risk so far
    max_value = sys.maxsize
    for node in graph.get_nodes():
        min_risk[node] = max_value
    min_risk[start_node] = 0

    q = [(0, start_node)] # min priority queue
    while q:
        risk, node = heapq.heappop(q)
        if risk <= min_risk[node]:
            for neighbor, weight in graph.get_outgoing_edges(node):
                new_risk = risk + weight
                if new_risk < min_risk[neighbor]:
                    min_risk[neighbor] = new_risk
                    heapq.heappush(q, (new_risk, neighbor))

    return min_risk

def min_risk(risk_levels):
    graph = Graph(risk_levels)
    start_node = (0,0)
    end_node = graph.end_node()
    return dijkstra(graph, start_node)[end_node]

def part_1(puzzle_input):
    risk_levels = get_risk_levels(puzzle_input, False)
    return min_risk(risk_levels)

def part_2(puzzle_input):
    risk_levels = get_risk_levels(puzzle_input, True)
    return min_risk(risk_levels)
