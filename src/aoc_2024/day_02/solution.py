"""
Advent of Code 2024
Day 2: Red-Nosed Reports
"""

def is_safe(nums: list[int]) -> bool:
    all_increasing = True
    all_decreasing = True
    for a, b in zip(nums, nums[1:]):
        if abs(a - b) not in {1, 2, 3}:
            return False
        if a < b:
            all_decreasing = False
        if a > b:
            all_increasing = False
    return all_increasing or all_decreasing


def solve_part_1(puzzle_input: list[str]):
    num_safe = 0
    for line in puzzle_input:
        nums = [int(d) for d in line.split()]
        if is_safe(nums):
            num_safe += 1
    return num_safe


def solve_part_2(puzzle_input: list[str]):
    num_safe = 0
    for line in puzzle_input:
        nums = [int(d) for d in line.split()]
        if is_safe(nums):
            num_safe += 1
        else:
            for i in range(len(nums)):
                nums_ex_i = nums[:i] + nums[i + 1:]
                if is_safe(nums_ex_i):
                    num_safe += 1
                    break
    return num_safe
