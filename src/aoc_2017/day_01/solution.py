"""
Advent of Code 2017
Day 1: Inverse Captcha
"""


def parse_input(puzzle_input: list[str]):
    return [int(digit) for digit in puzzle_input[0].strip()]


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    digits = parse_input(puzzle_input)
    for num_a, num_b in zip(digits, digits[1:] + [digits[0]], strict=True):
        if num_a == num_b:
            tot += num_a
    return tot


def solve_part_2(puzzle_input: list[str]):
    tot = 0
    digits = parse_input(puzzle_input)
    num_steps = len(digits) // 2
    for num_a, num_b in zip(digits, digits[num_steps:] + digits[:num_steps], strict=True):
        if num_a == num_b:
            tot += num_a
    return tot
