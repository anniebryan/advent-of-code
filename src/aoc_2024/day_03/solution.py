"""
Advent of Code 2024
Day 3: Mull It Over
"""

import os
from pathlib import Path

import click
import regex as re

PATTERN = r'mul\((?P<n1>\d+),(?P<n2>\d+)\)'


def get_enabled_indices(mem: str) -> set[int]:
    enabled_indices = set()
    is_enabled = True
    for i in range(len(mem)):
        if mem[i:].startswith("do()"):
            is_enabled = True
        elif mem[i:].startswith("don't()"):
            is_enabled = False
        
        if is_enabled:
            enabled_indices.add(i)
    return enabled_indices


def solve_part_1(puzzle_input: list[str]):
    mem = "".join(puzzle_input)

    results = []
    nums = re.findall(PATTERN, mem)
    for (n1, n2) in nums:
        res = int(n1) * int(n2)
        results.append(res)
    return sum(results)


def solve_part_2(puzzle_input: list[str]):
    mem = "".join(puzzle_input)
    enabled_indices = get_enabled_indices(mem)

    results = []
    nums = re.finditer(PATTERN, mem)
    for num in nums:
        ix = num.start(0)
        n1, n2 = num.group("n1"), num.group("n2")
        if ix in enabled_indices:
            res = int(n1) * int(n2)
            results.append(res)
    return sum(results)
