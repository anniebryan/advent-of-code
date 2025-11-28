"""
Advent of Code 2023
Day 9: Mirage Maintenance
"""

def parse_input(puzzle_input: list[str]):
    return [[int(n) for n in line.split()] for line in puzzle_input]


def predict_next_value(seq: list[int]) -> int:
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    if set(diffs) == {0}:
        return seq[-1]
    return seq[-1] + predict_next_value(diffs)


def predict_first_value(seq: list[int]) -> int:
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    if set(diffs) == {0}:
        return seq[0]
    return seq[0] - predict_first_value(diffs)


def solve_part_1(puzzle_input: list[str]):
    sequences = parse_input(puzzle_input)
    next_values = []
    for seq in sequences:
        next_values.append(predict_next_value(seq))
    return sum(next_values)


def solve_part_2(puzzle_input: list[str]):
    sequences = parse_input(puzzle_input)
    first_values = []
    for seq in sequences:
        first_values.append(predict_first_value(seq))
    return sum(first_values)
