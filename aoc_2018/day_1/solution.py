"""
Advent of Code 2018
Day 1: Chronal Calibration
"""

def part_1(puzzle_input):
    return sum([int(x) for x in puzzle_input])


def part_2(puzzle_input):
    nums = [int(x) for x in puzzle_input]
    sums = set()
    s, i = 0, 0
    while True:
        s += nums[i % len(nums)]
        if s not in sums:
            sums.add(s)
            i += 1
        else:
            return s
