"""
Advent of Code 2017
Day 2: Corruption Checksum
"""


def parse_input(puzzle_input: list[str], part_2: bool):
    return [[int(x) for x in line.split()] for line in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    rows = parse_input(puzzle_input, False)
    checksum = 0
    for row in rows:
        checksum += max(row) - min(row)
    return checksum


def solve_part_2(puzzle_input: list[str]):
    rows = parse_input(puzzle_input, False)
    checksum = 0
    for row in rows:
        for i, a in enumerate(row):
            for j, b in enumerate(row):
                if i != j and a % b == 0:
                    checksum += a // b
    return checksum
