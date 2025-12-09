"""
Advent of Code 2025
Day 9: Movie Theater
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

from aoc_utils import DirectedGraph, DirectedWeightedGraph, Grid, IntRangeMap, IntRangeSet


def parse_input(puzzle_input: list[str], part_2: bool):
    locs = []
    for line in puzzle_input:
        x, y = line.split(",")
        locs.append((int(x), int(y)))
    return locs


def solve_part_1(puzzle_input: list[str]):
    locs = parse_input(puzzle_input, False)
    max_rect_size = 0
    for (x1, y1) in locs:
        for (x2, y2) in locs:
            rect_size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_rect_size = max(max_rect_size, rect_size)
    return max_rect_size


def get_start_point(tiles_at_y: dict[int, IntRangeSet]) -> tuple[int, int]:
    for y, s in tiles_at_y.items():
        if s.num_ranges == 2 and s.num_values == 2:
            assert s.min_value is not None
            x = s.min_value + 1
            return (x, y)
    assert False


def solve_part_2(puzzle_input: list[str]):
    locs = parse_input(puzzle_input, True)

    vert_edges = defaultdict(lambda: IntRangeSet())
    horiz_edges = defaultdict(lambda: IntRangeSet())

    for (x1, y1), (x2, y2) in zip(locs, locs[1:] + [locs[0]]):
        if x1 == x2:
            vert_edges[x1].add_range(min(y1, y2), abs(y2 - y1))
        elif y1 == y2:
            horiz_edges[y1].add_range(min(x1, x2), abs(x2 - x1))
        else:
            raise ValueError(f"Received adjacent locs with different x's and different y's: {(x1, y1)} and {(x2, y2)}")

    print(dict(horiz_edges))
    print(dict(vert_edges))

    # TODO solve part 2

    return
