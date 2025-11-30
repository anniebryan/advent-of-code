"""
Advent of Code 2023
Day 18: Lavaduct Lagoon
"""

import ast
import copy
import heapq
import operator
import os
import re
import string
import sys
from collections import Counter, defaultdict, deque
from collections.abc import Iterator
from enum import Enum
from functools import cmp_to_key, lru_cache, reduce
from itertools import combinations, cycle
from math import lcm, prod
from pathlib import Path
from statistics import median
from typing import Callable, Iterable, Iterator, Literal

import click
import numpy
import regex

from aoc_utils import DirectedGraph, DirectedWeightedGraph, Grid, IntRangeMap, IntRangeSet, Shape


def parse_input(puzzle_input: list[str], part_2: bool) -> list[tuple[str, int]]:
    dig_plan = []
    for line in puzzle_input:
        if part_2:
            match = re.match(r"[UDLR] \d+ \(#(?P<hex>.*)\)", line)
            assert match is not None
            hex = match.group("hex")
            direction = "RDLU"[int(hex[-1])]
            num_steps = int(hex[:-1], 16)
        else:
            direction = line[0]
            num_steps = int(line.split()[1])
        dig_plan.append((direction, num_steps))
    return dig_plan


def construct_perimeter(dig_plan: list[tuple[str, int]]) -> set[tuple[int, int]]:
    start = (0, 0)
    perimeter: set[tuple[int, int]] = set([start])
    last_point = start
    for direction, num_steps in dig_plan:
        x, y = last_point
        dx, dy = {
            "U": (0, -1),
            "D": (0, 1),
            "R": (1, 0),
            "L": (-1, 0),
        }[direction]
        for i in range(1, num_steps + 1):
            perimeter.add((x + dx * i, y + dy * i))
        last_point = (x + dx * num_steps, y + dy * num_steps)
    return perimeter


def _solve(puzzle_input: list[str], part_2: bool) -> int:
    dig_plan = parse_input(puzzle_input, part_2)
    perimeter = construct_perimeter(dig_plan)
    shape = Shape(set(perimeter))
    interior = shape.get_interior_points()
    return len(interior)


def solve_part_1(puzzle_input: list[str]):
    return _solve(puzzle_input, part_2=False)


def solve_part_2(puzzle_input: list[str]):
    return _solve(puzzle_input, part_2=True)
