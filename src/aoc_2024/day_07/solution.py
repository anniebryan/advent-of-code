"""
Advent of Code 2024
Day 7: Bridge Repair
"""

def parse_input(puzzle_input: list[str]):
    equations = []
    for line in puzzle_input:
        value, nums = line.split(": ")
        equations.append((int(value), tuple([int(n) for n in nums.split()])))
    return equations


def can_be_true(value: int, nums: tuple[int], memo: dict, part_2: bool) -> bool:
    if (value, nums) in memo:
        return memo[(value, nums)]

    if len(nums) == 2:
        a, b = nums
        if part_2:
            memo[(value, nums)] = (a + b == value) or (a * b == value) or (int(f"{a}{b}") == value)
        else:
            memo[(value, nums)] = (a + b == value) or (a * b == value)
        return memo[(value, nums)]

    if value % nums[-1] == 0:
        if can_be_true(int(value / nums[-1]), nums[:-1], memo, part_2):
            memo[(value, nums)] = True
            return True

    if can_be_true(value - nums[-1], nums[:-1], memo, part_2):
        memo[(value, nums)] = True
        return True

    if part_2:
        if str(value).endswith(str(nums[-1])):
            if can_be_true(int(str(value)[:-len(str(nums[-1]))]), nums[:-1], memo, part_2):
                memo[(value, nums)] = True
                return True

    memo[(value, nums)] = False
    return False


def solve_part_1(puzzle_input: list[str]):
    equations = parse_input(puzzle_input)
    tot = 0
    for (value, nums) in equations:
        if can_be_true(value, nums, {}, False):
            tot += value
    return tot


def solve_part_2(puzzle_input: list[str]):
    equations = parse_input(puzzle_input)
    tot = 0
    for (value, nums) in equations:
        if can_be_true(value, nums, {}, True):
            tot += value
    return tot
