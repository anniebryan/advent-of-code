"""
Advent of Code 2018
Day 1: Chronal Calibration
"""

def parse_input(puzzle_input: list[str]) -> list[int]:
    return [int(x) for x in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    nums = parse_input(puzzle_input)
    return sum(nums)


def solve_part_2(puzzle_input: list[str]):
    nums = parse_input(puzzle_input)
    sums = set()
    s, i = 0, 0
    while True:
        s += nums[i % len(nums)]
        if s not in sums:
            sums.add(s)
            i += 1
        else:
            return s
