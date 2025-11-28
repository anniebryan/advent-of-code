"""
Advent of Code 2024
Day 5: Print Queue
"""

import os
from pathlib import Path

import click

from utils import DirectedGraph


def parse_input(puzzle_input: list[str]) -> tuple[DirectedGraph, list[list[int]]]:
    g = DirectedGraph()
    updates = []
    end_of_rules = None
    for i, line in enumerate(puzzle_input):
        if line == "":
            end_of_rules = i
        elif end_of_rules is None:
            [x, y] = [int(d) for d in line.split("|")]
            g.insert_edge(x, y)
        else:
            updates.append([int(d) for d in line.split(",")])
    return g, updates


def middle_number(line: list[int]) -> int:
    return line[len(line) // 2]


def solve_part_1(puzzle_input: list[str]):
    g, updates = parse_input(puzzle_input)

    middle_nums = []
    for line in updates:
        if g.exact_path_exists(line):
            middle_nums.append(middle_number(line))

    return sum(middle_nums)


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    g, updates = parse_input(puzzle_input)

    middle_nums = []
    for line in updates:
        if not g.exact_path_exists(line):
            ordered_line = g.reorder(line)
            assert g.exact_path_exists(ordered_line)
            middle_nums.append(middle_number(ordered_line))

    return sum(middle_nums)
