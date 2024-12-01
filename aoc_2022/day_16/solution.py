"""
Advent of Code 2022
Day 16: Proboscidea Volcanium
"""

from itertools import combinations
import re


class Valve:
    def __init__(self, name, flow_rate, tunnels):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels

    def __repr__(self):
        return f"Valve({self.name}, {self.flow_rate}, {self.tunnels})"


def parse_puzzle_input(puzzle_input):
    valves = {}
    for row in puzzle_input:
        values = re.match("Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", row).groups()
        name = values[0]
        flow_rate = int(values[1])
        tunnels = values[2].split(", ")
        valve = Valve(name, flow_rate, tunnels)
        valves[name] = valve
    return valves


def get_dist_graph(valves):

    def init_dist(v1, v2): 
        if v1 == v2:
            return 0
        if v2 in valves[v1].tunnels:
            return 1
        return float('inf')

    # set initial values
    d = {v1: {v2: init_dist(v1, v2) for v2 in valves} for v1 in valves}
    
    # floyd warshall
    for k in valves:
        for i in valves:
            for j in valves:
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def get_max_pressure(valves, dist, unvisited, start_valve, time_remaining, memo):
    key = (tuple(sorted(unvisited)), start_valve, time_remaining)

    if key in memo:
        return memo[key]

    best_path, best_pressure = ([], 0)

    for valve in unvisited:
        t = time_remaining - dist[start_valve][valve] - 1
        if t > 0:
            path, pressure = get_max_pressure(valves, dist, unvisited - {valve}, valve, t, memo)
            total_path = [valve] + path
            total_pressure = (t * valves[valve].flow_rate) + pressure
            if total_pressure > best_pressure:
                (best_path, best_pressure) = (total_path, total_pressure)

    memo[key] = (best_path, best_pressure)
    return memo[key]
    

def part_1(puzzle_input):
    valves = parse_puzzle_input(puzzle_input)
    dist = get_dist_graph(valves)
    unvisited = {v for v in valves if valves[v].flow_rate != 0}
    best_path, max_pressure = get_max_pressure(valves, dist, unvisited, "AA", 30, {})
    return max_pressure


def part_2(puzzle_input):  # TODO speedup
    valves = parse_puzzle_input(puzzle_input)
    dist = get_dist_graph(valves)
    unvisited = {v for v in valves if valves[v].flow_rate != 0}

    # O(2^|unvisited|), |unvisited| = 15 -> 2^15 = 32768 iterations (about 3 minutes)
    (best_path_1, best_path_2, max_pressure) = (None, None, 0)
    for i in range(len(valves)):
        for c in combinations(unvisited, i):
            visit_1 = set(c)
            visit_2 = unvisited - visit_1
            path_1, pressure_1 = get_max_pressure(valves, dist, visit_1, "AA", 26, {})
            path_2, pressure_2 = get_max_pressure(valves, dist, visit_2, "AA", 26, {})
            total_pressure = pressure_1 + pressure_2
            if total_pressure > max_pressure:
                (best_path_1, best_path_2, max_pressure) = (path_1, path_2, total_pressure)
    return max_pressure
