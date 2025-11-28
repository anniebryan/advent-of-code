"""
Advent of Code 2021
Day 7: The Threachery of Whales
"""

import os
from pathlib import Path

import click


def get_positions(puzzle_input):
    return [int(val) for val in puzzle_input[0].split(',')]


def min_distance(puzzle_input, distance_fn):
    positions = get_positions(puzzle_input)
    return min([distance_fn(i, positions) for i in range(max(positions))])


def solve_part_1(puzzle_input: list[str]):
    abs_distance = lambda i, positions: int(sum([abs(p - i) for p in positions]))
    return min_distance(puzzle_input, abs_distance)


def solve_part_2(puzzle_input: list[str]):
    distance = lambda i, positions: int(sum([abs(p - i) * (abs(p - i) + 1) / 2 for p in positions]))
    return min_distance(puzzle_input, distance)
