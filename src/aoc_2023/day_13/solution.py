"""
Advent of Code 2023
Day 13: Point of Incidence
"""

import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import click


def parse_input(puzzle_input: list[str]):
    i = 1
    rows = {}
    cols = defaultdict(list)
    for row in puzzle_input:
        if row == "":
            cols = {i: "".join(col) for i, col in cols.items()}
            yield rows, cols
            i = 1
            rows = {}
            cols = defaultdict(list)
            continue
        rows[i] = row
        for j, val in enumerate(row):
            cols[j + 1].append(val)
        i += 1
    cols = {i: "".join(col) for i, col in cols.items()}
    yield rows, cols


def lines_different(d: dict[int, str], indices_equal: dict[tuple[int, int]: bool], mirror: int) -> int:
    lines = set()
    i = mirror
    j = mirror + 1
    while i >= 1 and j <= len(d):
        if not indices_equal[(i, j)]:
            lines.add((i, j))
        i -= 1
        j += 1
    return lines


def num_chars_different(a: str, b: str) -> int:
    num = 0
    for sa, sb in zip(a, b):
        if sa != sb:
            num += 1
    return num


def get_mirror(d: dict[int, str]) -> int:
    indices_equal = {(i, j): d[i] == d[j] for i in d for j in d}
    for mirror in range(1, len(d)):
        if len(lines_different(d, indices_equal, mirror)) == 0:
            return mirror
    return None


def get_new_mirror(d: dict[int, str]) -> int:
    indices_equal = {(i, j): d[i] == d[j] for i in d for j in d}
    for mirror in range(1, len(d)):
        l = lines_different(d, indices_equal, mirror)
        if len(l) == 1:
            a, b = min(l)
            if num_chars_different(d[a], d[b]) == 1:
                return mirror
    return None


def calc_total(mirrors: Iterable) -> int:
    tot = 0
    for horiz_mirror, vert_mirror in mirrors:
        if horiz_mirror is not None:
            tot += horiz_mirror * 100
        if vert_mirror is not None:
            tot += vert_mirror
    return tot


def solve_part_1(puzzle_input: list[str]) -> int:
    mirrors = ((get_mirror(rows), get_mirror(cols)) for rows, cols in parse_input(puzzle_input))
    return calc_total(mirrors)


def solve_part_2(puzzle_input: list[str]) -> int:
    mirrors = ((get_new_mirror(rows), get_new_mirror(cols)) for rows, cols in parse_input(puzzle_input))
    return calc_total(mirrors)
