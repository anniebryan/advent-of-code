"""
Advent of Code 2017
Day 12: Digital Plumber
"""

from aoc_utils import UndirectedGraph


def parse_input(puzzle_input: list[str]) -> UndirectedGraph:
    g = UndirectedGraph()
    for line in puzzle_input:
        line_parts = line.split(" <-> ")
        if len(line_parts) != 2:
            raise ValueError(f"Invalid {line=}")
        program = int(line_parts[0])
        connecting_programs = [int(x) for x in line_parts[1].split(", ")]
        for p in connecting_programs:
            g.insert_edge(program, p)
    return g


def solve_part_1(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    dists = g.dijkstra(0)
    return len(dists)


def solve_part_2(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    return g.num_connected_components()
