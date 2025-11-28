"""
Advent of Code 2021
Day 1: Sonar Sweep
"""

import os
from pathlib import Path

import click


def get_measurements(puzzle_input):
	return [int(n) for n in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    measurements = get_measurements(puzzle_input)
    return sum([x < y for x, y in zip(measurements, measurements[1:])])


def solve_part_2(puzzle_input: list[str]):
    measurements = get_measurements(puzzle_input)
    sums = [i + j + k for (i, j, k) in zip(measurements, measurements[1:], measurements[2:])]
    return sum([x < y for x, y in zip(sums, sums[1:])])
