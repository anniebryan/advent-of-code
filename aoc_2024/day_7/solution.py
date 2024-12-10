"""
Advent of Code 2024
Day 7: Bridge Repair
"""

import click
import os
import pathlib


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


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = pathlib.Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
