"""
Advent of Code 2023
Day 25: Snowverload
"""

from itertools import combinations
from math import prod

import networkx as nx


def parse_input(puzzle_input: list[str]):
    graph = nx.DiGraph()
    for line in puzzle_input:
        node, neighbors = line.split(": ")
        for neighbor in neighbors.split():
            graph.add_edge(node, neighbor, capacity=1)
            graph.add_edge(neighbor, node, capacity=1)
    return graph


def solve_part_1(puzzle_input: list[str]):
    graph = parse_input(puzzle_input)
    for (node_1, node_2) in combinations(graph.nodes, 2):
        try:
            cut_value, partition = nx.minimum_cut(graph, node_1, node_2)
            if cut_value == 3:
                reachable, non_reachable = partition
                cutset = set()
                for u, nbrs in ((n, graph[n]) for n in reachable):
                    cutset.update((u, v) for v in nbrs if v in non_reachable)
                for edge in cutset:
                    graph.remove_edge(*edge)
                component_sizes = [len(component) for component in nx.strongly_connected_components(graph)]
                return prod(component_sizes)
        except nx.NetworkXUnbounded:
            continue
    return


def solve_part_2(puzzle_input: list[str]):
    return
