"""
Advent of Code 2019
Day 4: Secure Container
"""

import os
from pathlib import Path

import click
import regex as re


def get_min_max_r(puzzle_input):
    min_r, max_r = (int(x) for x in re.findall(r"(\d+)-(\d+)", puzzle_input[0])[0])
    return min_r, max_r


def adjacent_digits(n):
    s = str(n)
    adjacent = [s[i] == s[i + 1] for i in range(len(s) - 1)]
    return any(adjacent)


def never_decreases(n):
    s = str(n)
    decreases = [s[i] > s[i + 1] for i in range(len(s) - 1)]
    return not any(decreases)


def contains_double(n):
    s = str(n)
    lengths = []
    current = 1
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            current += 1
        else:
            lengths.append(current)
            current = 1
    lengths.append(current)
    return 2 in lengths


def solve_part_1(puzzle_input: list[str]):
    min_r, max_r = get_min_max_r(puzzle_input)
    valid_passwords = [n for n in range(min_r, max_r + 1) if adjacent_digits(n) and never_decreases(n)]
    return len(valid_passwords)


def solve_part_2(puzzle_input: list[str]):
    min_r, max_r = get_min_max_r(puzzle_input)
    valid_passwords = [n for n in range(min_r, max_r + 1) if contains_double(n) and never_decreases(n)]
    return len(valid_passwords)
