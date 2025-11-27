"""
Advent of Code 2024
Day 2: Red-Nosed Reports
"""

import os
from pathlib import Path

import click


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


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
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
