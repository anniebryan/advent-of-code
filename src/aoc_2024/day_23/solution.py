"""
Advent of Code 2024
Day 23: LAN Party
"""

import os
from pathlib import Path

import click

from utils import DirectedGraph


def parse_input(puzzle_input: list[str]) -> DirectedGraph:
    g = DirectedGraph()
    for line in puzzle_input:
        a, b = line.split("-")
        g.insert_edge(a, b)
        g.insert_edge(b, a)
    return g


def get_cycles(g: DirectedGraph, n: int) -> set[tuple[str, ...]]:
    def dfs(path: list[str], start_node: str, visited: set[str]):
        node = path[-1]
        if len(path) == n and start_node in g.neighbors(node):
            yield tuple(sorted(path))

        if len(path) < n:
            for neighbor in g.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    yield from dfs(path + [neighbor], start_node, visited)
                    visited.remove(neighbor)

    cycles = set()
    for start_node in g.graph:
        if start_node.startswith("t"):
            for cycle in dfs([start_node], start_node, set()):
                cycles.add(cycle)
    return cycles

def get_largest_fully_connected_component_helper(g: DirectedGraph, component: set[str], memo: dict[str, set[str]]) -> set[str]:
    component_str = ",".join(sorted(component))
    if component_str in memo:
        return memo[component_str]

    largest_component = component
    for n in set(g.graph) - component:
        if component - g.neighbors(n) == set():
            # n is neighbors with all items already in component
            new_component = get_largest_fully_connected_component_helper(g, component | {n}, memo)
            if len(new_component) > len(largest_component):
                largest_component = new_component

    memo[component_str] = largest_component
    return largest_component


def get_largest_fully_connected_component(g: DirectedGraph) -> set[str]:
    largest_component = set()
    memo = {}
    for start_node in g.graph:
        component = get_largest_fully_connected_component_helper(g, {start_node}, memo)
        if len(component) > len(largest_component):
            largest_component = component

    return largest_component


def solve_part_1(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    return len(get_cycles(g, 3))


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    return ",".join(sorted(get_largest_fully_connected_component(g)))
