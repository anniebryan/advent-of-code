"""
Advent of Code 2025
Day 1: Secret Entrance
"""

import re


def parse_input(puzzle_input: list[str], part_2: bool):
    directions = []
    for line in puzzle_input:
        match = re.match(r"(?P<dir>[LR])(?P<num>\d+)", line)
        assert match is not None
        d = match.group("dir")
        n = int(match.group("num"))
        directions.append((d, n))
    return directions


def solve_part_1(puzzle_input: list[str]):
    directions = parse_input(puzzle_input, False)
    points_at_zero = 0
    curr = 50
    for (d, n) in directions:
        curr += n * {"L": -1, "R": 1}[d]
        curr %= 100
        if curr == 0:
            points_at_zero += 1
    return points_at_zero


def solve_part_2(puzzle_input: list[str]):
    directions = parse_input(puzzle_input, True)
    points_at_zero = 0
    curr = 50
    for (d, n) in directions:
        start = curr
        curr += n * {"L": -1, "R": 1}[d]
        points_at_zero += abs(curr) // 100
        if d == "L" and start != 0 and n >= start:
            points_at_zero += 1
        curr %= 100
    return points_at_zero
