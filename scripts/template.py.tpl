"""
Advent of Code $YEAR
Day $DAY
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

from aoc_utils import DirectedGraph, Grid, IntRangeMap, IntRangeSet


def parse_input(puzzle_input: list[str], part_2: bool):
    return


def solve_part_1(puzzle_input: list[str]):
    _ = parse_input(puzzle_input, False)
    return


def solve_part_2(puzzle_input: list[str]):
    _ = parse_input(puzzle_input, True)
    return
