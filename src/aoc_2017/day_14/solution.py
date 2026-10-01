"""
Advent of Code 2017
Day 14: Disk Defragmentation
"""

from aoc_2017.day_10.solution import calc_knot_hash
from aoc_utils import UndirectedGraph


def parse_input(puzzle_input: list[str]):
    key_string = puzzle_input[0].strip()
    rows = []
    for i in range(128):
        knot_hash = calc_knot_hash(f"{key_string}-{i}")
        row = []
        for ch in knot_hash:
            for bit in f"{int(ch, 16):04b}":
                row.append({"0": ".", "1": "#"}[bit])
        rows.append(row)
    return rows


def solve_part_1(puzzle_input: list[str]):
    rows = parse_input(puzzle_input)
    num_squares = 0
    for row in rows:
        for ch in row:
            if ch == "#":
                num_squares += 1
    return num_squares


def solve_part_2(puzzle_input: list[str]):
    rows = parse_input(puzzle_input)
    squares = set()
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            if ch == "#":
                squares.add((i, j))

    g = UndirectedGraph()
    for (i, j) in squares:
        g.nodes.add((i, j))
        for (i2, j2) in [(i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j)]:
            if (i2, j2) in squares:
                g.insert_edge((i, j), (i2, j2))
    return g.num_connected_components()
