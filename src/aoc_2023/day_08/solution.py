"""
Advent of Code 2023
Day 8: Haunted Wasteland
"""

from itertools import cycle
from math import lcm
from typing import Callable

import regex as re


class Graph:

    def __init__(self):
        self.nodes = set()
        self.left_edges = {}
        self.right_edges = {}

    def add_node(self, node, left_edge, right_edge):
        self.nodes.add(node)
        self.nodes.add(left_edge)
        self.nodes.add(right_edge)
        self.left_edges[node] = left_edge
        self.right_edges[node] = right_edge

    def move_left(self, node):
        return self.left_edges[node]

    def move_right(self, node):
        return self.right_edges[node]

    def move(self, inst, node):
        if inst == "L":
            return self.move_left(node)
        elif inst == "R":
            return self.move_right(node)
        else:
            raise ValueError(f"Invalid instruction {inst}, expected L or R.")

    def all_nodes_ending_with(self, letter: str) -> set[str]:
        nodes_ending_with_letter = set()
        for node in self.nodes:
            if node.endswith(letter):
                nodes_ending_with_letter.add(node)
        return nodes_ending_with_letter


def parse_input(puzzle_input: list[str]):
    inst_ls = list(puzzle_input[0])
    graph = Graph()
    for line in puzzle_input[2:]:
        match = re.match(r'(?P<node>.*) = \((?P<left>.*), (?P<right>.*)\)', line)
        node = match.group('node')
        left = match.group('left')
        right = match.group('right')
        graph.add_node(node, left, right)
    return inst_ls, graph


def solve(start_node: str, end_cond: Callable[[str], bool], graph: Graph, instr_cycle: cycle) -> int:
    num_steps = 0
    curr_node = start_node
    while not end_cond(curr_node):
        num_steps += 1
        curr_node = graph.move(next(instr_cycle), curr_node)
    return num_steps


def solve_part_1(puzzle_input: list[str]):
    inst_ls, graph = parse_input(puzzle_input)
    start_node = "AAA"
    if start_node not in graph.nodes:
        return "N/A"
    return solve(start_node, lambda node: node == "ZZZ", graph, cycle(inst_ls))


def solve_part_2(puzzle_input: list[str]):
    inst_ls, graph = parse_input(puzzle_input)
    cycle_lens = []
    for start_node in graph.all_nodes_ending_with("A"):
        cycle_lens.append(solve(start_node, lambda node: node.endswith("Z"), graph, cycle(inst_ls)))
    return lcm(*cycle_lens)
