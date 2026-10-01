"""
Advent of Code 2017
Day 4: High-Entropy Passphrases
"""


def parse_input(puzzle_input: list[str]):
    return [line.split() for line in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    lines = parse_input(puzzle_input)
    num_valid = 0
    for line in lines:
        unique_words = set(line)
        if len(unique_words) == len(line):
            num_valid += 1
    return num_valid


def solve_part_2(puzzle_input: list[str]):
    lines = parse_input(puzzle_input)
    num_valid = 0
    for line in lines:
        unique_words = set("".join(sorted(word)) for word in line)
        if len(unique_words) == len(line):
            num_valid += 1
    return num_valid
