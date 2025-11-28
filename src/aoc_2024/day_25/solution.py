"""
Advent of Code 2024
Day 25: Code Chronicle
"""

from collections import defaultdict


def get_values(lines: list[str]) -> list[int]:
    d = defaultdict(int)
    for line in lines:
        for i, val in enumerate(line):
            if val == "#":
                d[i] += 1
    return [d[k] - 1 for k in sorted(d)]


def parse_input(puzzle_input: list[str]):
    keys, locks, curr_lines = [], [], []
    is_first_line, is_key, is_lock = True, False, False
    for line in puzzle_input + [""]:
        if line == "":
            if is_key:
                keys.append(get_values(curr_lines[::-1]))
            elif is_lock:
                locks.append(get_values(curr_lines))
            curr_lines = []
            is_first_line, is_key, is_lock = True, False, False
        else:
            curr_lines.append(line)
            if is_first_line:
                is_first_line = False
                is_lock = (set(line) == {"#"})
                is_key = (set(line) == {"."})
    return keys, locks


def fit(key: list[int], lock: list[int]) -> bool:
    sums = [k + l for (k, l) in zip(key, lock)]
    return max(sums) <= 5


def solve_part_1(puzzle_input: list[str]):
    keys, locks = parse_input(puzzle_input)
    num_fits = 0
    for key in keys:
        for lock in locks:
            if fit(key, lock):
                num_fits += 1
    return num_fits


def solve_part_2(puzzle_input: list[str]):
    return
